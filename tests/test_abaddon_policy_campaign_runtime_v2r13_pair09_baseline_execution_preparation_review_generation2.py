from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_execution_preparation_review_generation2
    as review,
)


def test_preparation_pins_exact_design_and_hardened_capability_sources():
    out = review.v2r13_pair09_baseline_execution_preparation_review_contract()
    assert out["design_review_git_blob"] == "08a1a20a16dcceb2feb183d402edaff96f0cadfa"
    assert out["design_review_source_sha256"] == (
        "015f6ba4f845e17f88f71f0c76d1ed3debea1c5102786cdcf5c66731b4fda449"
    )
    assert out["first_baseline_invocation_git_blob"] == (
        "5b790efaf4085deb15eaef538635fd11f5cad9a5"
    )


def test_pair09_baseline_preparation_is_exact_and_nonheld():
    out = review.v2r13_pair09_baseline_execution_preparation_review_contract()
    assert out["pair09_baseline_execution_preparation_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["candidate_execution_must_wait_for_baseline_result_review"] is True


def test_hardened_pair03_capabilities_are_reused_without_inheriting_authority():
    out = review.v2r13_pair09_baseline_execution_preparation_review_contract()
    assert out["historical_pair03_runtime_authority_sufficient_for_pair09"] is False
    assert out["hardened_host_readiness_capabilities_reusable"] is True
    for field in (
        "fresh_current_main_preflight_required",
        "cached_sudo_required",
        "revocation_sentinel_absent_required",
        "isolated_grpc_python_required",
        "restricted_git_backend_required",
        "exact_model_preload_before_readiness_required",
        "preload_must_not_perform_inference",
        "canonical_worktree_observation_required",
        "fresh_canonical_live_readiness_required",
    ):
        assert out[field] is True


def test_pair09_baseline_command_remains_source_only_and_nonexecuting():
    out = review.v2r13_pair09_baseline_execution_preparation_review_contract()
    command = out["baseline_command"]
    assert out["pair09_baseline_command_source_only"] is True
    assert command["pair_slot"] == 9
    assert command["arm"] == "baseline"
    assert command["workdir_token"] == "generation2/pair-09/baseline"
    assert command["runtime_execution_authorized"] is False
    assert command["runtime_started"] is False
    assert command["command_execution_performed"] is False
    assert command["model_inference_performed"] is False
    assert command["game_execution_performed"] is False
    assert command["training_performed"] is False


def test_pair09_candidate_heldout_and_followon_authority_remain_closed():
    out = review.v2r13_pair09_baseline_execution_preparation_review_contract()
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["pair09_baseline_execution_performed"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["pair09_candidate_execution_performed"] is False
    assert out["candidate_replay_permitted"] is False
    assert out["held_out_execution_authorized"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_preparation_stops_at_explicit_pair09_baseline_authorization():
    out = review.v2r13_pair09_baseline_execution_preparation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "trusted_operator_v2r13_pair09_baseline_execution_authorization"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09BaselineExecutionPreparationReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_baseline()
