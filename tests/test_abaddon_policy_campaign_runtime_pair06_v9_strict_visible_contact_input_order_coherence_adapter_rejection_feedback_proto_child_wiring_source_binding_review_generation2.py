from __future__ import annotations

import unittest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_feedback_proto_child_wiring_source_binding_review_generation2
    as review,
)


class AdapterFeedbackProtoChildWiringReviewTest(unittest.TestCase):
    def test_review_accepts_exact_lineage(self) -> None:
        out = review.pair06_v9_adapter_feedback_proto_child_wiring_review_contract()

        self.assertTrue(
            out["pair06_v9_adapter_feedback_proto_child_wiring_reviewed"]
        )
        self.assertTrue(out["feedback_decision_hook_reviewed"])
        self.assertTrue(
            out["historical_input_order_child_run_code_reused_reviewed"]
        )
        self.assertTrue(out["call_scoped_feedback_hook_binding_reviewed"])

    def test_review_pins_all_dependency_blobs(self) -> None:
        out = review.pair06_v9_adapter_feedback_proto_child_wiring_review_contract()

        self.assertEqual(
            out["wiring_git_blob"],
            "64af11733bb384959cc7cc5f11d18dab2d9e2c1c",
        )
        self.assertEqual(
            out["wiring_test_git_blob"],
            "27e7f692117a8d4dde9e0a8cc2271218a26fa22a",
        )
        self.assertEqual(
            out["feedback_overlay_git_blob"],
            "f720d70d2f7068eeeb05324d3a89aaf6b86daa84",
        )
        self.assertEqual(
            out["historical_wiring_git_blob"],
            "1b87cb5596c219e6118f4b69845dbecaa29a3ace",
        )
        self.assertEqual(
            out["historical_wiring_review_git_blob"],
            "7e96e32361b64f71ccf5c2cfd3c10a33c15429a1",
        )

    def test_review_grants_no_execution_or_follow_on_authority(self) -> None:
        out = review.pair06_v9_adapter_feedback_proto_child_wiring_review_contract()

        for field in (
            "process_global_child_hook_factory_mutated",
            "process_global_child_run_function_mutated",
            "consumed_v9_attempt_retry_authorized",
            "parent_supervisor_wiring_implemented",
            "operator_wiring_implemented",
            "runtime_activation_authorized",
            "runtime_execution_authorized",
            "replay_authorized",
            "automatic_retry",
            "training_authorized",
            "automatic_corpus_admission",
            "weights_update_authorized",
            "automatic_policy_promotion_authorized",
            "deployment_authorized",
            "void_chain_mutation_authorized",
            "wallet_or_funds_action_authorized",
            "scheduler_mutation_authorized",
        ):
            self.assertFalse(out[field], field)

    def test_review_advances_only_to_new_parent_wiring(self) -> None:
        out = review.pair06_v9_adapter_feedback_proto_child_wiring_review_contract()

        self.assertTrue(out["source_frontier_closed"])
        self.assertEqual(
            out["next_gate"],
            "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED",
        )

    def test_wire_parent_or_execute_holds(self) -> None:
        with self.assertRaises(
            review.Pair06V9AdapterFeedbackProtoChildWiringReviewHold
        ):
            review.wire_parent_or_execute()


if __name__ == "__main__":
    unittest.main(verbosity=2)
