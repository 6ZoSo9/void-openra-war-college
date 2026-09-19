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


if __name__ == "__main__":
    unittest.main()
