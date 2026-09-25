from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_proposal_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_proposal_source_and_tests():
    out = review.pair06_v8_combat_action_priority_policy_proposal_review_contract()
    assert out["proposal_main_head"] == (
        "46dd688fca16235a847ab9b9165b800606b6b9d0"
    )
    assert out["proposal_git_blob"] == (
        "f230f77c5b78e47b5d8872870f5c87a040861c15"
    )
    assert out["proposal_source_sha256"] == (
        "937da96c490e658f5fce7847e27bfb6833c01fff82a92aa222657297eda6d291"
    )
    assert out["proposal_test_git_blob"] == (
        "e81a3faf32143425baf9c81c31b931140d40258c"
    )
    assert out["proposal_test_sha256"] == (
        "cebe7a3f27786d2a6b9fbebf5d5031a1b09d4a51f00e8a51b003baf67ffad42c"
    )


def test_review_preserves_exact_policy_surfaces():
    out = review.pair06_v8_combat_action_priority_policy_proposal_review_contract()
    assert out["policy_id"] == "pair06-v8-combat-action-priority-envelope-v1"
    assert out["intervention_layer"] == "pre_inference_current_tool_surface"
    assert out["recovery_surface"] == "only_currently_offered_train_unit_functions"
    assert out["visible_contact_surface"] == (
        "current_engagement_plus_tactical_control_plus_train_unit_functions"
    )
    assert out["normal_surface"] == "exact_current_reviewed_offered_tool_surface"


def test_review_preserves_runtime_invariants():
    out = review.pair06_v8_combat_action_priority_policy_proposal_review_contract()
    for field in (
        "host_validation_must_remain_unchanged",
        "six_attempt_fail_closed_retry_must_remain_unchanged",
        "frozen_world_state_across_rejected_attempts_must_remain_unchanged",
        "typed_production_legality_must_remain_unchanged",
        "normal_mode_surface_must_remain_unchanged",
    ):
        assert out[field] is True


def test_review_grants_no_runtime_or_training_authority():
    out = review.pair06_v8_combat_action_priority_policy_proposal_review_contract()
    assert out["implementation_present"] is False
    for field in (
        "policy_change_authorized",
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


def test_review_advances_only_to_source_implementation():
    out = review.pair06_v8_combat_action_priority_policy_proposal_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatActionPriorityPolicyProposalReviewHold,
        match="COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_REQUIRED",
    ):
        review.implement_or_execute()
