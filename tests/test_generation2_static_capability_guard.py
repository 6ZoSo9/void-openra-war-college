from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from openra_env.learning.generation2_static_capability_guard import (
    CapabilityGuardError,
    HELD_ENTRYPOINTS,
    PROTECTED_FALSE_FIELDS,
    TargetSpec,
    audit_repository,
    audit_source,
)


def _source(*, overrides: dict[str, str] | None = None, entrypoint_body: str | None = None) -> bytes:
    values = {field: "False" for field in PROTECTED_FALSE_FIELDS}
    values.update(overrides or {})
    fields = "\n".join(f'        "{field}": {value},' for field, value in values.items())
    body = entrypoint_body or "raise Hold(NEXT_GATE)"
    entrypoints = "\n\n".join(
        f"def {name}(*args, **kwargs):\n    {body}" for name in HELD_ENTRYPOINTS
    )
    return (
        "NEXT_GATE = 'RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED'\n\n"
        "class Hold(ValueError):\n    pass\n\n"
        "def contract():\n    return {\n"
        f"{fields}\n"
        "    }\n\n"
        f"{entrypoints}\n"
    ).encode()


def _spec(source: bytes) -> TargetSpec:
    return TargetSpec(
        path="fixture.py",
        sha256=hashlib.sha256(source).hexdigest(),
        contract_function="contract",
        gate_name="NEXT_GATE",
        gate_value="RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        hold_exception="Hold",
        protected_false_fields=PROTECTED_FALSE_FIELDS,
        held_entrypoints=HELD_ENTRYPOINTS,
    )


def _git_blob_oid(source: bytes) -> str:
    header = f"blob {len(source)}\0".encode("ascii")
    return hashlib.sha1(header + source).hexdigest()


class StaticCapabilityGuardTests(unittest.TestCase):
    def test_accepts_literal_false_flags_and_held_entrypoints(self):
        source = _source()
        receipt = audit_source(source, _spec(source))
        self.assertEqual(receipt["protected_false_field_count"], len(PROTECTED_FALSE_FIELDS))
        self.assertEqual(receipt["held_entrypoint_count"], len(HELD_ENTRYPOINTS))
        self.assertIs(receipt["module_imported"], False)
        self.assertIs(receipt["runtime_execution"], False)

    def test_rejects_each_protected_flag_flip(self):
        for field in PROTECTED_FALSE_FIELDS:
            with self.subTest(field=field):
                source = _source(overrides={field: "True"})
                with self.assertRaisesRegex(
                    CapabilityGuardError,
                    f"protected field not literal false: {field}",
                ):
                    audit_source(source, _spec(source))

    def test_rejects_missing_protected_field(self):
        source = _source()
        text = source.decode().replace('        "runtime_started": False,\n', "")
        changed = text.encode()
        with self.assertRaisesRegex(CapabilityGuardError, "protected field missing: runtime_started"):
            audit_source(changed, _spec(changed))

    def test_rejects_executable_entrypoint_replacement(self):
        source = _source(entrypoint_body="return 'executable'")
        with self.assertRaisesRegex(CapabilityGuardError, "must raise authority hold"):
            audit_source(source, _spec(source))

    def test_rejects_gate_drift(self):
        source = _source().replace(
            b"RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            b"RUNTIME_EXECUTION_AUTHORIZED",
            1,
        )
        with self.assertRaisesRegex(CapabilityGuardError, "next gate drift"):
            audit_source(source, _spec(source))

    def test_rejects_direct_host_execution_surfaces(self):
        for statement in ("import subprocess", "from os import system", "open('x')"):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden"):
                    audit_source(source, spec)

    def test_rejects_indirect_host_execution_imports(self):
        for statement in (
            "import builtins\nbuiltins.open('x')",
            "from builtins import exec as run_code\nrun_code('pass')",
            "import importlib\nimportlib.import_module('openra_env.learning.fixture_dependency')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_builtin_introspection_and_filesystem_escapes(self):
        for statement in (
            "__builtins__['open']('x')",
            "(lambda: None).__globals__['__builtins__']['open']('x')",
            "getattr((lambda: None), '__globals__')",
            "import pathlib\npathlib.Path('x').write_text('x')",
            "import sys\nsys.modules['builtins'].open('x')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden"):
                    audit_source(source, spec)

    def test_rejects_traceback_and_frame_introspection_escapes(self):
        for statement in (
            "exc.__traceback__.tb_frame.f_builtins['open']('x')",
            "frame.f_globals['__builtins__']['eval']('1 + 1')",
            "generator.gi_frame.f_builtins['open']('x')",
            "coroutine.cr_frame.f_globals",
            "async_generator.ag_frame.f_globals",
            "function.__code__",
            "function.__closure__",
            "object.__getattribute__((lambda: None), '__globals__')",
            "type.__getattribute__(Exception, '__mro__')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(
                    CapabilityGuardError,
                    "forbidden introspection attribute",
                ):
                    audit_source(source, spec)

    def test_rejects_reflective_helpers_and_interactive_builtins(self):
        for statement in (
            "import operator\noperator.attrgetter('__globals__')(lambda: None)",
            "from operator import methodcaller\nmethodcaller('__subclasses__')(object)",
            "import inspect\ninspect.getclosurevars(lambda: None)",
            "from inspect import currentframe\ncurrentframe()",
            "import gc\ngc.get_referrers(object())",
            "breakpoint()",
            "input('prompt')",
            "help(object)",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden"):
                    audit_source(source, spec)

    def test_rejects_import_loader_introspection_escapes(self):
        for statement in (
            "import json\njson.__loader__.load_module('os').system('id')",
            "import json\njson.__spec__.loader.find_spec('os')",
            "import json\njson.__spec__.loader.exec_module(module)",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(
                    CapabilityGuardError,
                    "forbidden introspection attribute",
                ):
                    audit_source(source, spec)

    def test_rejects_additional_host_capability_modules(self):
        for statement in (
            "import code\ncode.interact()",
            "import codeop\ncodeop.compile_command('open(\\'x\\')')",
            "import concurrent.futures\nconcurrent.futures.ProcessPoolExecutor()",
            "import io\nio.open('x')",
            "import pickle\npickle.loads(b'payload')",
            "import pydoc\npydoc.help(object)",
            "import runpy\nrunpy.run_path('x.py')",
            "import webbrowser\nwebbrowser.open('https://example.invalid')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)


    def test_rejects_aliased_builtin_capabilities(self):
        for statement in (
            "runner = open\nrunner('x')",
            "evaluate = eval\nevaluate('1 + 1')",
            "resolve = getattr\nresolve(object(), '__class__')",
            "loader = __import__\nloader('pathlib')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(
                    CapabilityGuardError,
                    "forbidden builtin capability reference",
                ):
                    audit_source(source, spec)

    def test_rejects_interpreter_native_host_capability_modules(self):
        for statement in (
            "import _io\n_io.open('x', 'w')",
            "import _socket\n_socket.socket()",
            "import _ctypes\n_ctypes.dlopen('libc.so.6')",
            "import _posixsubprocess\n_posixsubprocess.fork_exec()",
            "import posix\nposix.system('id')",
            "import nt\nnt.system('whoami')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_posix_process_memory_and_terminal_capability_modules(self):
        for statement in (
            "import fcntl\nfcntl.ioctl(0, 0)",
            "import mmap\nmmap.mmap(-1, 1)",
            "import pty\npty.spawn(['/bin/sh'])",
            "import resource\nresource.setrlimit(resource.RLIMIT_NOFILE, (1, 1))",
            "import signal\nsignal.raise_signal(signal.SIGTERM)",
            "import termios\ntermios.tcgetattr(0)",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_terminal_and_network_io_capability_modules(self):
        for statement in (
            "import getpass\ngetpass.getpass('secret')",
            "import readline\nreadline.set_startup_hook(lambda: None)",
            "import select\nselect.select([], [], [], 0)",
            "import selectors\nselectors.DefaultSelector()",
            "import ssl\nssl.create_default_context()",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_protocol_client_and_server_capability_modules(self):
        for statement in (
            "import ftplib\nftplib.FTP('example.invalid')",
            "import imaplib\nimaplib.IMAP4('example.invalid')",
            "import nntplib\nnntplib.NNTP('example.invalid')",
            "import poplib\npoplib.POP3('example.invalid')",
            "import smtplib\nsmtplib.SMTP('example.invalid')",
            "import socketserver\nsocketserver.TCPServer(('127.0.0.1', 0), object)",
            "import telnetlib\ntelnetlib.Telnet('example.invalid')",
            "import xmlrpc.client\nxmlrpc.client.ServerProxy('https://example.invalid')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_persistence_and_archive_capability_modules(self):
        for statement in (
            "import dbm\ndbm.open('state', 'c')",
            "import shelve\nshelve.open('state')",
            "import sqlite3\nsqlite3.connect('state.db')",
            "import tarfile\ntarfile.open('bundle.tar', 'w')",
            "import zipfile\nzipfile.ZipFile('bundle.zip', 'w')",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_code_object_reconstruction_modules(self):
        for statement in (
            "import marshal\nmarshal.loads(b'payload')",
            "from types import FunctionType\nFunctionType(code_object, {})",
        ):
            with self.subTest(statement=statement):
                source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(source), sha256=hashlib.sha256(source).hexdigest())
                with self.assertRaisesRegex(CapabilityGuardError, "forbidden import"):
                    audit_source(source, spec)

    def test_rejects_sha_drift_before_parsing(self):
        source = _source()
        spec = replace(_spec(source), sha256="0" * 64)
        with self.assertRaisesRegex(CapabilityGuardError, "SHA-256 drift"):
            audit_source(source, spec)


    def test_binds_complete_local_dependency_graph(self):
        dependency_path = "openra_env/learning/fixture_dependency.py"
        target_path = "openra_env/learning/fixture_target.py"
        dependency_source = b"VALUE = 1\n"
        target_source = (
            b"from openra_env.learning import fixture_dependency as dependency\n"
            + _source()
        )
        spec = replace(
            _spec(target_source),
            path=target_path,
            dependency_blobs=((dependency_path, _git_blob_oid(dependency_source)),),
        )

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / target_path
            dependency = root / dependency_path
            target.parent.mkdir(parents=True)
            target.write_bytes(target_source)
            dependency.write_bytes(dependency_source)

            receipt = audit_repository(root, (spec,))
            self.assertEqual(receipt["dependency_count"], 1)
            self.assertEqual(receipt["targets"][0]["dependency_count"], 1)

            unused_spec = replace(
                spec,
                dependency_blobs=spec.dependency_blobs
                + (("openra_env/learning/unused_fixture.py", "0" * 40),),
            )
            with self.assertRaisesRegex(
                CapabilityGuardError,
                "unused dependency binding",
            ):
                audit_repository(root, (unused_spec,))

            with self.assertRaisesRegex(CapabilityGuardError, "unbound local dependency"):
                audit_repository(root, (replace(spec, dependency_blobs=()),))

            dependency.write_bytes(b"VALUE = 2\n")
            with self.assertRaisesRegex(CapabilityGuardError, "dependency blob drift"):
                audit_repository(root, (spec,))


    def test_rejects_relative_local_dependency_import(self):
        target_path = "openra_env/learning/fixture_target.py"
        target_source = b"from . import fixture_dependency\n" + _source()
        spec = replace(_spec(target_source), path=target_path)

        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / target_path
            target.parent.mkdir(parents=True)
            target.write_bytes(target_source)

            with self.assertRaisesRegex(CapabilityGuardError, "relative local import"):
                audit_repository(root, (spec,))

    def test_rejects_ambiguous_local_package_imports(self):
        target_path = "openra_env/learning/fixture_target.py"
        for statement in (
            "import openra_env",
            "import openra_env.learning",
            "from openra_env import learning",
        ):
            with self.subTest(statement=statement):
                target_source = statement.encode() + b"\n" + _source()
                spec = replace(_spec(target_source), path=target_path)

                with TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    target = root / target_path
                    target.parent.mkdir(parents=True)
                    target.write_bytes(target_source)

                    with self.assertRaisesRegex(
                        CapabilityGuardError,
                        "ambiguous local package import",
                    ):
                        audit_repository(root, (spec,))


if __name__ == "__main__":
    unittest.main()
