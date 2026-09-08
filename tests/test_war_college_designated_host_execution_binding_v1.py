#!/usr/bin/env python3
from __future__ import annotations

import unittest

from scripts import verify_designated_host_execution_binding_v1 as verifier


def clean_report():
    b = verifier.load_binding()

    def artifact(path_key, sha_key, mode_key):
        return {
            "path": b[path_key],
            "exists": True,
            "is_regular": True,
            "is_symlink": False,
            "uid": 1000,
            "gid": 1000,
            "mode": b[mode_key],
            "group_or_other_writable": False,
            "sha256": b[sha_key],
        }

    return {
        "marker": "VOID_WAR_COLLEGE_DESIGNATED_HOST_EXECUTION_BINDING_DISCOVERY_V1",
        "schema_version": 1,
        "service_template_name": b["service_template_name"],
        "systemd_query_error": None,
        "systemd_load_state": "loaded",
        "systemd_fragment_path": b["installed_unit_path"],
        "dropin_paths": [],
        "need_daemon_reload": False,
        "unit_artifact": artifact(
            "installed_unit_path", "unit_sha256", "unit_required_mode"
        ),
        "environment_artifact": artifact(
            "installed_environment_path",
            "environment_sha256",
            "environment_required_mode",
        ),
        "wrapper_artifact": artifact(
            "installed_wrapper_path", "wrapper_sha256", "wrapper_required_mode"
        ),
        "working_directory": b["working_directory"],
        "void_data_dir": b["void_data_dir"],
        "runtime_source_commit": b["runtime_source_commit"],
        "runtime_worktree_dirty": False,
        "runtime_artifact_git_blobs": dict(b["runtime_artifact_git_blobs"]),
        "private_key_read": False,
        "mutation_performed": False,
        "service_started": False,
    }


class ExecutionBindingTests(unittest.TestCase):
    def assert_hold(self, report, code):
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_source_binding_self_validates_exact_execstart(self):
        b = verifier.load_binding()
        self.assertEqual(
            b["exec_start_line"],
            "ExecStart=/usr/bin/python3 -I -B "
            "/home/zoso/.local/libexec/void-war-college-evidence-verifier-v1.py %i",
        )
        self.assertEqual(
            b["semantic_parent_head"],
            "436dddc9d85efcaf3e4646fc25462667ba04104c",
        )
        self.assertFalse(b["runtime_execution_authorized"])
        supervisor = verifier.json.loads(
            (
                verifier.ROOT / b["supervisor_contract_path"]
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(supervisor["service_name"], b["service_template_name"])
        self.assertEqual(
            supervisor["service_instance_id_regex"],
            b["request_id_regex"],
        )

    def test_clean_installed_binding_is_green_without_starting_service(self):
        report = verifier.verify_installed_binding(clean_report())
        self.assertEqual(report["contract"], "GREEN")
        self.assertTrue(report["execution_path_bound"])
        self.assertFalse(report["runtime_execution_authorized"])

    def test_unit_hash_substitution_fails_closed(self):
        candidate = clean_report()
        candidate["unit_artifact"]["sha256"] = "0" * 64
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_UNIT_ARTIFACT_SHA256_MISMATCH")

    def test_wrapper_hash_substitution_fails_closed(self):
        candidate = clean_report()
        candidate["wrapper_artifact"]["sha256"] = "0" * 64
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_WRAPPER_ARTIFACT_SHA256_MISMATCH")

    def test_environment_mode_substitution_fails_closed(self):
        candidate = clean_report()
        candidate["environment_artifact"]["mode"] = "0o640"
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_ENVIRONMENT_ARTIFACT_MODE_MISMATCH")

    def test_service_must_be_loaded_from_exact_bound_fragment(self):
        candidate = clean_report()
        candidate["systemd_load_state"] = "not-found"
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_SERVICE_NOT_LOADED")

        candidate = clean_report()
        candidate["systemd_fragment_path"] = "/tmp/wrong.service"
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_SERVICE_FRAGMENT_PATH_MISMATCH")

    def test_systemd_query_error_fails_closed(self):
        candidate = clean_report()
        candidate["systemd_query_error"] = "systemctl_show_failed"
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_SERVICE_QUERY_ERROR")

    def test_any_dropin_fails_closed(self):
        candidate = clean_report()
        candidate["dropin_paths"] = ["/tmp/override.conf"]
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_SERVICE_DROPINS_PRESENT")

    def test_daemon_reload_required_fails_closed(self):
        candidate = clean_report()
        candidate["need_daemon_reload"] = True
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_SERVICE_DAEMON_RELOAD_REQUIRED")

    def test_runtime_blob_substitution_fails_closed(self):
        candidate = clean_report()
        blobs = dict(candidate["runtime_artifact_git_blobs"])
        key = sorted(blobs)[0]
        blobs[key] = "0" * 40
        candidate["runtime_artifact_git_blobs"] = blobs
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_EXECUTION_RUNTIME_ARTIFACT_BLOB_MISMATCH")

    def test_discovery_that_started_service_is_not_source_only(self):
        candidate = clean_report()
        candidate["service_started"] = True
        report = verifier.verify_installed_binding(candidate)
        self.assert_hold(report, "HOLD_EXECUTION_DISCOVERY_SERVICE_STARTED")


if __name__ == "__main__":
    unittest.main()
