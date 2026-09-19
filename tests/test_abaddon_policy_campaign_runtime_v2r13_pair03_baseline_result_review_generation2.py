from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_result_review_generation2
    as review,
)


def test_baseline_result_review_binds_retry2_evidence():
    out = review.v2r13_pair03_baseline_result_review_contract()
    assert out["retry2_evidence_review_git_blob"] == (
        "680ca2f26b5214aef13423cfb62ae7b0874a2080"
    )
    assert out["retry2_evidence_review_source_sha256"] == (
        "5df776e043413f9418e3f3732197f0e519717e40cdd54a372b41a603d3a0568d"
    )
    assert out["retry2_evidence_review_test_git_blob"] == (
        "954aae23d4c97dd3ba186242105099b0b6e86186"
    )
    assert out["retry2_evidence_review_test_sha256"] == (
        "22ef74770e929ec71f5bec0c8df9d7fd59725e7424ecb7fc3f36b48c466132d3"
    )


def test_baseline_measurement_is_complete_but_nondeсisive():
    out = review.v2r13_pair03_baseline_result_review_contract()
    assert out["baseline_result_reviewed"] is True
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["baseline_measurement_complete"] is True
    assert out["baseline_measurement_reproducibly_bound"] is True
    assert out["baseline_game_outcome"] == "DRAW_OR_UNFINISHED"
    assert out["baseline_game_outcome_decisive"] is False
    assert out["baseline_round_limit_reached"] is True
    assert out["baseline_rounds_completed"] == 36
    assert out["baseline_valid_for_pairwise_comparison"] is True


def test_retry_authority_is_exhausted():
    out = review.v2r13_pair03_baseline_result_review_contract()
    assert out["retry_authority_exhausted"] is True
    assert out["another_retry_authorized"] is False


def test_candidate_remains_unexecuted_and_unauthorized():
    out = review.v2r13_pair03_baseline_result_review_contract()
    assert out["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False


def test_result_review_does_not_expand_mutation_scope():
    out = review.v2r13_pair03_baseline_result_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_result_review_advances_only_to_candidate_authorization():
    out = review.v2r13_pair03_baseline_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_candidate_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineResultReviewHold,
        match="V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_candidate_execution()
