from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_backend_and_invocation_sources():
    out = review.pair06_v8_baseline_attempt_invocation_review_contract()
    assert out["git_backend_git_blob"] == "3a405630789528ca5411d04ba9b0fcac0b27e590"
    assert out["git_backend_source_sha256"] == (
        "8d0291a497c1f87d9cd11bc88a821b11d166d03967f2f611dd143e35bd425f9a"
    )
    assert out["git_backend_test_git_blob"] == "2d8472ea3630f8e9e46159ba9e48e781f8ba7288"
    assert out["git_backend_test_sha256"] == (
        "c0444208d94936826ca1ea8ffa30216432053c4a127e23c51763c52e13d3031d"
    )
    assert out["invocation_git_blob"] == "7d5ca142b9be1e97fa288eef2a91fe0ebc73da33"
    assert out["invocation_source_sha256"] == (
        "58fa705393c4f0fe4b1c50c004d020b0682ada2a4f7d8cafe89d76c28e13fdb7"
    )
    assert out["invocation_test_git_blob"] == "cff9dcd3450103e2c139addd0c93dc82182c2c22"
    assert out["invocation_test_sha256"] == (
        "5cc335acbd63b00cc243f396a55283c184a1f5d411563d5cf89e2edbc2b2309c"
    )


def test_review_confirms_one_shot_evidence_and_cleanup_ordering():
    out = review.pair06_v8_baseline_attempt_invocation_review_contract()
    assert out["pair06_v8_baseline_attempt_invocation_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["preclaim_materialization_cleanup_on_hold"] is True
    assert out["attempt_marker_create_only"] is True
    assert out["attempt_marker_precedes_model_load_and_child_spawn"] is True
    assert out["postclaim_reset_or_resume_available"] is False
    assert out["durable_execution_result_before_cleanup"] is True
    assert out["success_only_worktree_cleanup"] is True
    assert out["durable_cleanup_closeout"] is True
    assert out["runs_preserved"] is True


def test_review_remains_non_authorizing():
    out = review.pair06_v8_baseline_attempt_invocation_review_contract()
    assert out["explicit_authorization_required"] is True
    assert out["pair06_baseline_specific_authorization_accepted"] is False
    assert out["attempt_consumed"] is False
    assert out["runtime_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["game_execution_performed"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False


def test_review_preserves_external_boundaries():
    out = review.pair06_v8_baseline_attempt_invocation_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_authorization_request():
    out = review.pair06_v8_baseline_attempt_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8BaselineAttemptInvocationReviewHold,
        match="PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.execute_or_authorize()
