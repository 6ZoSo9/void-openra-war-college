#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

from scripts import verify_designated_host_supervisor_discovery_v1 as verifier


def clean_report() -> dict[str, object]:
    contract = verifier.load_contract()
    return {
        "marker": "VOID_WAR_COLLEGE_DESIGNATED_HOST_SUPERVISOR_DISCOVERY_V1",
        "schema_version": 1,
        "service": contract["service_name"],
        "active_state": "active",
        "sub_state": "running",
        "main_pid": 4242,
        "process": {
            "uid": contract["runtime_uid"],
            "gid": contract["runtime_gid"],
            "cwd": contract["runtime_repository"],
            "exe": "/usr/bin/python3",
        },
        "runtime_source_commit": contract["runtime_source_commit"],
        "runtime_worktree_dirty": False,
        "runtime_artifact_git_blobs": dict(contract["runtime_artifact_git_blobs"]),
        "runtime_void_data_dir": {
            "configured": True,
            "raw": contract["void_data_dir"],
            "is_absolute": True,
            "resolved": contract["void_data_dir"],
        },
        "runtime_data_dir_fallback": {
            "configured": False,
            "raw": None,
            "is_absolute": False,
            "resolved": None,
        },
        "resolved_void_data_dir_artifact": {
            "exists": True,
            "mode": contract["artifact_policy"]["data_dir_required_mode"],
            "uid": contract["runtime_uid"],
            "gid": contract["runtime_gid"],
            "is_regular": False,
            "is_directory": True,
            "is_symlink": False,
            "group_or_other_writable": False,
            "path": contract["void_data_dir"],
        },
        "service_artifacts": [
            {
                "exists": True,
                "mode": "0o600",
                "uid": contract["runtime_uid"],
                "gid": contract["runtime_gid"],
                "is_regular": True,
                "is_directory": False,
                "is_symlink": False,
                "group_or_other_writable": False,
                "path": "/home/zoso/.config/systemd/user/void-war-college-evidence-verifier.service",
                "sha256": "1" * 64,
            }
        ],
        "environment_file_artifacts": [
            {
                "exists": True,
                "mode": contract["artifact_policy"]["environment_file_required_mode"],
                "uid": contract["runtime_uid"],
                "gid": contract["runtime_gid"],
                "is_regular": True,
                "is_directory": False,
                "is_symlink": False,
                "group_or_other_writable": False,
                "path": "/home/zoso/.config/void-war-college/evidence-verifier.env",
                "sha256": "2" * 64,
            }
        ],
        "health_identity": {
            "queried": True,
            "ok": True,
            "node_id": contract["expected_node_id"],
            "expected_node_id": contract["expected_node_id"],
            "matches_expected": True,
        },
        "private_key_read": False,
        "full_process_environment_emitted": False,
        "environment_file_contents_emitted": False,
        "mutation_performed": False,
        "service_restart_performed": False,
    }


class SupervisorContractTests(unittest.TestCase):
    def assert_hold(self, report, code):
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_committed_contract_is_self_consistent_and_grants_no_authority(self):
        contract = verifier.load_contract()
        self.assertEqual(contract["runtime_source_commit"], "bae61935b956c5f7ebce005c0fef69ec86f69d09")
        self.assertTrue(contract["runtime_repository"].endswith("designated-host-runtime-bae61935"))
        self.assertEqual(contract["void_data_dir"], "/home/zoso/dev/void-node/data_a")
        self.assertTrue(
            contract["store_absolute_path"].endswith(
                "/war_college/controller_attempt_admission_v3.sqlite3"
            )
        )
        self.assertEqual(len(contract["runtime_artifact_git_blobs"]), 5)
        self.assertTrue(all(value is False for value in contract["authority"].values()))

    def test_clean_dedicated_supervisor_discovery_is_green(self):
        report = verifier.verify_discovery(clean_report())
        self.assertEqual(report["contract"], "GREEN")
        self.assertTrue(report["supervisor_contract_green"])
        self.assertFalse(report["runtime_execution_authorized"])

    def test_completed_oneshot_template_instance_is_inspectable(self):
        candidate = clean_report()
        candidate["sub_state"] = "exited"
        candidate["main_pid"] = 0
        candidate["process"] = None
        report = verifier.verify_discovery(candidate)
        self.assertEqual(report["contract"], "GREEN")
        self.assertTrue(report["supervisor_contract_green"])

    def test_existing_shared_void_node_service_is_rejected(self):
        candidate = clean_report()
        candidate["service"] = "void-node-live.service"
        candidate["runtime_void_data_dir"]["raw"] = "data_a"
        candidate["runtime_void_data_dir"]["is_absolute"] = False
        candidate["service_artifacts"][0]["mode"] = "0o664"
        candidate["service_artifacts"][0]["group_or_other_writable"] = True
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_SUPERVISOR_SERVICE_NAME_MISMATCH")
        self.assert_hold(report, "HOLD_VOID_DATA_DIR_NOT_ABSOLUTE")
        self.assert_hold(report, "HOLD_VOID_DATA_DIR_RAW_MISMATCH")
        self.assert_hold(report, "HOLD_SERVICE_ARTIFACT_0_GROUP_OR_OTHER_WRITABLE")

    def test_wrong_runtime_repository_fails_closed(self):
        candidate = clean_report()
        candidate["process"]["cwd"] = "/tmp/other"
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_SUPERVISOR_RUNTIME_REPOSITORY_MISMATCH")

    def test_wrong_runtime_source_commit_fails_closed(self):
        candidate = clean_report()
        candidate["runtime_source_commit"] = "0" * 40
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_RUNTIME_SOURCE_COMMIT_MISMATCH")

    def test_dirty_runtime_worktree_fails_closed(self):
        candidate = clean_report()
        candidate["runtime_worktree_dirty"] = True
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_RUNTIME_WORKTREE_NOT_CLEAN")

    def test_runtime_blob_substitution_fails_closed(self):
        candidate = clean_report()
        blobs = dict(candidate["runtime_artifact_git_blobs"])
        key = sorted(blobs)[0]
        blobs[key] = "0" * 40
        candidate["runtime_artifact_git_blobs"] = blobs
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_RUNTIME_ARTIFACT_BLOB_MISMATCH")

    def test_wrong_node_identity_fails_closed(self):
        candidate = clean_report()
        candidate["health_identity"]["node_id"] = "0" * 32
        candidate["health_identity"]["matches_expected"] = False
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_DESIGNATED_NODE_HEALTH_IDENTITY_MISMATCH")

    def test_relative_data_dir_fails_closed(self):
        candidate = clean_report()
        candidate["runtime_void_data_dir"]["raw"] = "data_a"
        candidate["runtime_void_data_dir"]["is_absolute"] = False
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_VOID_DATA_DIR_NOT_ABSOLUTE")
        self.assert_hold(report, "HOLD_VOID_DATA_DIR_RAW_MISMATCH")

    def test_group_writable_unit_fails_closed(self):
        candidate = clean_report()
        candidate["service_artifacts"][0]["mode"] = "0o664"
        candidate["service_artifacts"][0]["group_or_other_writable"] = True
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_SERVICE_ARTIFACT_0_GROUP_OR_OTHER_WRITABLE")

    def test_environment_file_must_be_mode_0600(self):
        candidate = clean_report()
        candidate["environment_file_artifacts"][0]["mode"] = "0o640"
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_ENVIRONMENT_ARTIFACT_0_MODE_MISMATCH")

    def test_probe_that_reads_private_key_fails_closed(self):
        candidate = clean_report()
        candidate["private_key_read"] = True
        report = verifier.verify_discovery(candidate)
        self.assert_hold(report, "HOLD_DISCOVERY_PRIVATE_KEY_READ")


if __name__ == "__main__":
    unittest.main()
