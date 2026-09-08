#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest

from scripts import verify_designated_host_provisioning_plan_v1 as verifier


class ProvisioningPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(verifier.PLAN_PATH.read_text(encoding="utf-8"))
        self.binding = json.loads(verifier.BINDING_PATH.read_text(encoding="utf-8"))

    def assert_hold(self, plan, code):
        report = verifier.verify_plan(plan, self.binding)
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_exact_source_plan_is_green_and_non_authorizing(self):
        report = verifier.verify_plan(self.plan, self.binding)
        self.assertEqual(report["contract"], "GREEN")
        self.assertTrue(report["plan_only"])
        self.assertFalse(report["materialization_authorized"])
        self.assertFalse(report["daemon_reload_authorized"])
        self.assertFalse(report["service_start_authorized"])
        self.assertFalse(report["runtime_execution_authorized"])
        self.assertFalse(report["private_key_access"])

    def test_runtime_generation_substitution_fails_closed(self):
        candidate = copy.deepcopy(self.plan)
        candidate["runtime_worktree"]["source_commit"] = "0" * 40
        self.assert_hold(candidate, "HOLD_PROVISIONING_RUNTIME_COMMIT")

    def test_artifact_target_substitution_fails_closed(self):
        candidate = copy.deepcopy(self.plan)
        candidate["artifacts"][0]["target_path"] = "/tmp/not-the-unit"
        self.assert_hold(
            candidate,
            "HOLD_PROVISIONING_ARTIFACT_SYSTEMD_USER_UNIT_DRIFT",
        )

    def test_nonmatching_existing_artifacts_cannot_be_overwritten(self):
        candidate = copy.deepcopy(self.plan)
        candidate["materialization"]["overwrite_nonmatching_existing"] = True
        self.assert_hold(candidate, "HOLD_PROVISIONING_MATERIALIZATION_POLICY")

    def test_daemon_reload_is_required_but_not_authorized(self):
        self.assertTrue(
            self.plan["daemon_reload"]["required_after_unit_materialization"]
        )
        self.assertFalse(self.plan["daemon_reload"]["authorized"])
        candidate = copy.deepcopy(self.plan)
        candidate["daemon_reload"]["authorized"] = True
        self.assert_hold(candidate, "HOLD_PROVISIONING_DAEMON_RELOAD_POLICY")

    def test_post_provision_requires_loaded_exact_fragment(self):
        post = self.plan["post_provision_preflight"]
        self.assertEqual(post["required_systemd_load_state"], "loaded")
        self.assertEqual(
            post["required_systemd_fragment_path"],
            self.binding["installed_unit_path"],
        )
        self.assertEqual(post["required_dropin_paths"], [])
        self.assertFalse(post["required_need_daemon_reload"])
        self.assertFalse(post["required_service_started"])
        self.assertFalse(post["required_mutation_performed"])
        self.assertEqual(
            post["preflight_contract_path"],
            "config/war-college/designated-host-runtime-preflight-v1.json",
        )
        self.assertEqual(
            post["preflight_contract_git_blob"],
            "531d3aecbe92e8a84ad8324d54053b88de6d5c4a",
        )

    def test_post_preflight_contract_substitution_fails_closed(self):
        candidate = copy.deepcopy(self.plan)
        candidate["post_provision_preflight"]["preflight_contract_git_blob"] = (
            "0" * 40
        )
        self.assert_hold(candidate, "HOLD_PROVISIONING_POST_PREFLIGHT_POLICY")


if __name__ == "__main__":
    unittest.main()
