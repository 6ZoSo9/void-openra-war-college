from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_implementation_source_and_tests():
    out = review.pair06_v8_combat_action_priority_policy_review_contract()
    assert out["implementation_main_head"] == (
        "e8961c6096e4e0971582ca7c576182a5339156d1"
    )
    assert out["implementation_git_blob"] == (
        "15cef31b57c4402e151053086e38c76c3226bd1d"
    )
    assert out["implementation_source_sha256"] == (
        "856f3391eb705998bcfeacb738ab7355c1a42581e64232c07be42ff2cc60f8b0"
    )
    assert out["implementation_test_git_blob"] == (
        "4a7b778bf9cd95604afa321dfafaabbda6269c70"
    )
    assert out["implementation_test_sha256"] == (
        "1025ca0ab48cac27504f769fceb3a2b6b3bfd6338d78af0df5404b94912e2e63"
    )


def test_review_confirms_pure_nonintegrated_implementation():
    out = review.pair06_v8_combat_action_priority_policy_review_contract()
    assert out["pair06_v8_combat_action_priority_policy_reviewed"] is True
    assert out["implementation_layer"] == (
        "pure_pre_inference_tool_surface_transform"
    )
    assert out["runtime_integration_implemented"] is False
    assert out["model_call_implemented"] is False
    assert out["host_command_implemented"] is False
    assert out["game_execution_implemented"] is False


def test_review_grants_no_activation_execution_or_training_authority():
    out = review.pair06_v8_combat_action_priority_policy_review_contract()
    for field in (
        "policy_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_source_runtime_integration():
    out = review.pair06_v8_combat_action_priority_policy_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatActionPriorityPolicyReviewHold,
        match="COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_REQUIRED",
    ):
        review.integrate_or_execute()
