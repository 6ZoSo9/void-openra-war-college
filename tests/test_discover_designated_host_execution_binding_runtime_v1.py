#!/usr/bin/env python3
"""Source-only tests for designated-host runtime preflight discovery."""

from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "discover_designated_host_execution_binding_runtime_v1.py"
SPEC = importlib.util.spec_from_file_location("runtime_preflight", SOURCE)
assert SPEC is not None and SPEC.loader is not None
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


def exact_artifact(path: str, sha256: str, mode: str) -> dict:
    return {
        "path": path,
        "exists": True,
        "is_regular": True,
        "is_symlink": False,
        "uid": 1000,
        "gid": 1000,
        "mode": mode,
        "group_or_other_writable": False,
        "sha256": sha256,
    }


def synthetic_binding(root: Path) -> dict:
    return {
        "service_template_name": "void-war-college-evidence-verifier@.service",
        "installed_unit_path": str(root / "unit.service"),
        "installed_environment_path": str(root / "evidence.env"),
        "installed_wrapper_path": str(root / "wrapper.py"),
        "unit_sha256": "1" * 64,
        "environment_sha256": "2" * 64,
        "wrapper_sha256": "3" * 64,
        "unit_required_mode": "0o600",
        "environment_required_mode": "0o600",
        "wrapper_required_mode": "0o500",
        "working_directory": str(root / "runtime"),
        "void_data_dir": str(root / "data"),
        "runtime_source_commit": "a" * 40,
        "runtime_artifact_git_blobs": {
            "scripts/a.py": "b" * 40,
            "scripts/b.py": "c" * 40,
        },
        "exec_start_line": "ExecStart=/usr/bin/python3 wrapper.py %i",
    }


class RuntimePreflightTests(unittest.TestCase):
    def test_repository_contract_binds_exact_existing_dependencies(self):
        contract = PREFLIGHT.load_preflight_contract()
        self.assertEqual(
            contract["semantic_parent_head"],
            "5b1f2f1ec391ee68add8aa600658074a3fb95a52",
        )
        self.assertTrue(contract["read_only"])
        for field in (
            "private_key_access",
            "service_install_authorized",
            "daemon_reload_authorized",
            "service_start_authorized",
            "runtime_execution_authorized",
        ):
            self.assertFalse(contract[field])

    def test_systemd_probe_uses_show_only(self):
        calls = []

        def fake_run(args):
            calls.append(list(args))
            return SimpleNamespace(
                returncode=0,
                stdout=(
                    "LoadState=loaded\n"
                    "FragmentPath=/tmp/unit.service\n"
                    "DropInPaths=\n"
                    "NeedDaemonReload=no\n"
                ),
                stderr="",
            )

        record = PREFLIGHT.systemd_snapshot(
            "void-war-college-evidence-verifier@.service",
            run_command=fake_run,
        )
        self.assertEqual(record["dropin_paths"], [])
        self.assertFalse(record["need_daemon_reload"])
        self.assertEqual(len(calls), 1)
        self.assertIn("show", calls[0])
        for forbidden in ("start", "restart", "reload", "enable", "disable", "stop"):
            self.assertNotIn(forbidden, calls[0])

    def test_missing_install_fails_closed_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            binding = synthetic_binding(Path(directory))
            report = PREFLIGHT.run_preflight(
                binding,
                systemd_override={
                    "load_state": "not-found",
                    "fragment_path": None,
                    "dropin_paths": [],
                    "need_daemon_reload": False,
                    "query_error": None,
                },
                runtime_override={
                    "runtime_source_commit": None,
                    "runtime_worktree_dirty": True,
                    "runtime_artifact_git_blobs": {},
                    "runtime_query_error": "runtime_repository_unavailable",
                },
            )
            self.assertEqual(report["verification"]["contract"], "HOLD")
            self.assertFalse(report["discovery"]["mutation_performed"])
            self.assertFalse(report["discovery"]["service_started"])
            self.assertFalse(report["private_key_access"])

    def test_exact_synthetic_installed_generation_is_green(self):
        with tempfile.TemporaryDirectory() as directory:
            binding = synthetic_binding(Path(directory))
            artifacts = {
                "unit_artifact": exact_artifact(
                    binding["installed_unit_path"], binding["unit_sha256"], "0o600"
                ),
                "environment_artifact": exact_artifact(
                    binding["installed_environment_path"],
                    binding["environment_sha256"],
                    "0o600",
                ),
                "wrapper_artifact": exact_artifact(
                    binding["installed_wrapper_path"],
                    binding["wrapper_sha256"],
                    "0o500",
                ),
            }
            report = PREFLIGHT.run_preflight(
                binding,
                systemd_override={
                    "load_state": "loaded",
                    "fragment_path": binding["installed_unit_path"],
                    "dropin_paths": [],
                    "need_daemon_reload": False,
                    "query_error": None,
                },
                runtime_override={
                    "runtime_source_commit": binding["runtime_source_commit"],
                    "runtime_worktree_dirty": False,
                    "runtime_artifact_git_blobs": binding["runtime_artifact_git_blobs"],
                    "runtime_query_error": None,
                },
                artifact_overrides=artifacts,
            )
            self.assertEqual(report["verification"]["contract"], "GREEN")
            self.assertTrue(report["verification"]["execution_path_bound"])
            self.assertFalse(report["runtime_execution_authorized"])
            self.assertFalse(report["service_start_authorized"])

    def test_daemon_reload_requirement_is_a_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            binding = synthetic_binding(Path(directory))
            artifacts = {
                "unit_artifact": exact_artifact(
                    binding["installed_unit_path"], binding["unit_sha256"], "0o600"
                ),
                "environment_artifact": exact_artifact(
                    binding["installed_environment_path"],
                    binding["environment_sha256"],
                    "0o600",
                ),
                "wrapper_artifact": exact_artifact(
                    binding["installed_wrapper_path"],
                    binding["wrapper_sha256"],
                    "0o500",
                ),
            }
            report = PREFLIGHT.run_preflight(
                binding,
                systemd_override={
                    "load_state": "loaded",
                    "fragment_path": binding["installed_unit_path"],
                    "dropin_paths": [],
                    "need_daemon_reload": True,
                    "query_error": None,
                },
                runtime_override={
                    "runtime_source_commit": binding["runtime_source_commit"],
                    "runtime_worktree_dirty": False,
                    "runtime_artifact_git_blobs": binding["runtime_artifact_git_blobs"],
                    "runtime_query_error": None,
                },
                artifact_overrides=artifacts,
            )
            self.assertEqual(report["verification"]["contract"], "HOLD")
            self.assertIn(
                "HOLD_SERVICE_DAEMON_RELOAD_REQUIRED",
                report["verification"]["holds"],
            )

    def test_artifact_probe_rejects_symlink_without_following(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.write_bytes(b"test-bytes")
            link = root / "link"
            link.symlink_to(target)
            before = hashlib.sha256(target.read_bytes()).hexdigest()
            record = PREFLIGHT.artifact_record(link)
            after = hashlib.sha256(target.read_bytes()).hexdigest()
            self.assertTrue(record["exists"])
            self.assertTrue(record["is_symlink"])
            self.assertFalse(record["is_regular"])
            self.assertIsNone(record["sha256"])
            self.assertEqual(before, after)

    def test_regular_artifact_probe_is_read_only_and_hash_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "artifact"
            payload = b"frozen-artifact\n"
            path.write_bytes(payload)
            path.chmod(0o600)
            before = path.stat()
            record = PREFLIGHT.artifact_record(path)
            after = path.stat()
            self.assertTrue(record["is_regular"])
            self.assertFalse(record["is_symlink"])
            self.assertEqual(record["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(record["mode"], "0o600")
            self.assertEqual(
                (before.st_dev, before.st_ino, before.st_size),
                (after.st_dev, after.st_ino, after.st_size),
            )

    def test_dependency_identity_uses_git_blob_and_rejects_dirty_dependency(self):
        relative = Path(
            "config/war-college/designated-host-execution-binding-v1.json"
        )
        expected = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", f"HEAD:{relative.as_posix()}"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        self.assertEqual(PREFLIGHT._git_dependency_identity(relative), expected)

        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "test@example.invalid"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "test"],
                check=True,
            )
            dependency = repo / "dep.txt"
            dependency.write_text("one\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "dep.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-q", "-m", "fixture"],
                check=True,
            )
            dependency.write_text("two\n", encoding="utf-8")

            original_root = PREFLIGHT.ROOT
            try:
                PREFLIGHT.ROOT = repo
                with self.assertRaisesRegex(
                    PREFLIGHT.RuntimePreflightError,
                    "working tree differs from HEAD",
                ):
                    PREFLIGHT._git_dependency_identity(Path("dep.txt"))
            finally:
                PREFLIGHT.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
