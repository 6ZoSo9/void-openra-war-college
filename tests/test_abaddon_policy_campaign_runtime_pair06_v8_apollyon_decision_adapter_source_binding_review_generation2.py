from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_apollyon_decision_adapter_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_adapter_source_and_tests():
    out = review.pair06_v8_apollyon_decision_adapter_review_contract()
    assert out["adapter_git_blob"] == "4c8296f6ca642bbaa72b88c1c308e56b8810ce62"
    assert out["adapter_source_sha256"] == (
        "13eb9fcceb18b168b54ee9468a4bb770a8cf2738db3982eb3ccdec8bb6ca0650"
    )
    assert out["adapter_test_git_blob"] == "477476c84356c20c4df5a77ae9e15a37899ff6cf"
    assert out["adapter_test_sha256"] == (
        "39d7c1773a2fa726921912d22623b6f74c6a3d6ad6cfe12ad3973474e1eea656"
    )


def test_review_binds_observed_legacy_typed_boundary():
    out = review.pair06_v8_apollyon_decision_adapter_review_contract()
    assert out["pair06_v8_apollyon_decision_adapter_reviewed"] is True
    assert out["legacy_hook_symbol"] == "apollyon_decision_typed"
    assert out["legacy_typed_tool_builder_symbol"] == "apollyon_tools_typed"
    assert out["legacy_host_validator_symbol"] == "decision_to_commands_typed"
    assert out["legacy_ollama_tool_call_used"] is False
    assert out["max_attempts"] == 6


def test_review_preserves_current_state_tools_feedback_and_host_validation():
    out = review.pair06_v8_apollyon_decision_adapter_review_contract()
    assert out["current_compact_state_only"] is True
    assert out["current_typed_tool_list_only"] is True
    assert out["current_tool_contract_only"] is True
    assert out["host_rejection_feedback_forwarded"] is True
    assert out["world_mutation_before_host_validation"] is False
    assert out["host_validation_unchanged"] is True
    assert out["legacy_return_shape_preserved"] is True
    assert out["in_memory_hook_only"] is True


def test_review_grants_no_execution_authority():
    out = review.pair06_v8_apollyon_decision_adapter_review_contract()
    for field in (
        "game_runner_adapter_implemented",
        "durable_game_attempt_claim_implemented",
        "operator_invocation_implemented",
        "game_coupled_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_review_advances_only_to_legacy_game_runner_composition():
    out = review.pair06_v8_apollyon_decision_adapter_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_LEGACY_GAME_RUNNER_COMPOSITION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_LEGACY_GAME_RUNNER_COMPOSITION_IMPLEMENTATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ApollyonDecisionAdapterReviewHold,
        match="PAIR06_V8_BASELINE_LEGACY_GAME_RUNNER_COMPOSITION_IMPLEMENTATION_REQUIRED",
    ):
        review.execute_game()
