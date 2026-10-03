from __future__ import annotations

import unittest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_feedback_proto_child_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_generation2
    as historical,
)


class AdapterFeedbackProtoChildWiringTest(unittest.TestCase):
    def test_contract_preserves_source_and_authority_boundaries(self) -> None:
        out = wiring.pair06_v9_adapter_feedback_proto_child_wiring_contract()

        self.assertTrue(out["adapter_feedback_proto_child_wiring_implemented"])
        self.assertFalse(out["historical_input_order_proto_child_source_modified"])
        self.assertFalse(out["historical_input_order_proto_child_review_modified"])
        self.assertFalse(out["feedback_overlay_source_modified"])
        self.assertTrue(out["feedback_decision_hook_bound"])
        self.assertTrue(out["exact_sentinel_retry_feedback_preserved"])
        self.assertEqual(out["sentinel_retry_feedback"], "unit_ids invalid")

        for field in (
            "process_global_child_hook_factory_mutated",
            "process_global_child_run_function_mutated",
            "new_concurrency_scope_leak_introduced",
            "consumed_v9_attempt_retry_authorized",
            "new_execution_request_opened",
            "attempt_created",
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

    def test_scoped_v8_child_run_binds_feedback_hook_only_locally(self) -> None:
        original_builder = historical._scoped_v8_child_run
        original_hooks = historical.Pair06V9InputOrderCoherentProtoChildHooks

        scoped = wiring._scoped_feedback_v8_child_run()

        self.assertIs(
            scoped.__globals__["Pair06V8ProtoChildHooks"],
            wiring.Pair06V9AdapterFeedbackProtoChildHooks,
        )
        self.assertIs(historical._scoped_v8_child_run, original_builder)
        self.assertIs(
            historical.Pair06V9InputOrderCoherentProtoChildHooks,
            original_hooks,
        )

    def test_input_order_child_run_code_is_reused_call_scopingly(self) -> None:
        original = historical.run_pair06_v9_input_order_coherence_proto_game_child
        scoped = wiring._scoped_input_order_child_run()

        self.assertIs(scoped.__code__, original.__code__)
        self.assertIs(
            scoped.__globals__["_scoped_v8_child_run"],
            wiring._scoped_feedback_v8_child_run,
        )
        self.assertIs(
            historical.run_pair06_v9_input_order_coherence_proto_game_child,
            original,
        )

    def test_next_gate_is_source_binding_review_only(self) -> None:
        out = wiring.pair06_v9_adapter_feedback_proto_child_wiring_contract()
        self.assertTrue(out["source_frontier_closed"])
        self.assertEqual(
            out["next_gate"],
            "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
            "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
        )

    def test_review_or_execute_holds(self) -> None:
        with self.assertRaises(
            wiring.Pair06V9AdapterFeedbackProtoChildWiringHold
        ):
            wiring.review_or_execute()


if __name__ == "__main__":
    unittest.main(verbosity=2)
