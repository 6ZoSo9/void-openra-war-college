from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_post_pair09_evaluation_design_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_design_source_and_tests():
    out = review.v2r13_post_pair09_evaluation_design_review_contract()
    assert out["design_git_blob"] == "36c618c2172993b0ce8bf0b0c4e5af7677e5f81c"
    assert out["design_source_sha256"] == (
        "6255385bd6a65d044fa2a2c4cb7a3370a47dead3c918ed40287a95107969a2e4"
    )
    assert out["design_test_git_blob"] == (
        "169fe65510dd9a698b88fc542fd67fba6953c24e"
    )
    assert out["design_test_sha256"] == (
        "92b29523d46da66dafaf78aa68416f9cb3cb2ebaa36a947b646c1dd443f93869"
    )


def test_review_confirms_nonheldout_capacity_exhaustion():
    out = review.v2r13_post_pair09_evaluation_design_review_contract()
    assert out["post_pair09_evaluation_design_reviewed"] is True
    assert out["authorized_pair_slots"] == (3, 9, 15)
    assert out["held_out_pair_slots"] == (15,)
    assert out["nonheldout_pair_slots"] == (3, 9)
    assert out["existing_nonheldout_capacity_exhausted"] is True


def test_review_preserves_pair15_from_tuning_use():
    out = review.v2r13_post_pair09_evaluation_design_review_contract()
    assert out["held_out_pair15_preserved"] is True
    assert out["held_out_contamination_prohibited"] is True
    assert out["held_out_use_as_tuning_tiebreaker_allowed"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["pair15_execution_performed"] is False


def test_review_requires_new_nonheldout_allocation_without_execution_authority():
    out = review.v2r13_post_pair09_evaluation_design_review_contract()
    assert out["new_nonheldout_evaluation_allocation_required"] is True
    assert out["new_nonheldout_execution_authorized"] is False
    assert out["pair03_replay_authorized"] is False
    assert out["pair09_replay_authorized"] is False
    assert out["candidate_promoted"] is False
    assert out["candidate_rejected"] is False


def test_review_grants_no_training_promotion_or_external_authority():
    out = review.v2r13_post_pair09_evaluation_design_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_frontier_is_new_nonheldout_allocation():
    out = review.v2r13_post_pair09_evaluation_design_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED"
    )


def test_prohibited_action_entrypoints_hold():
    for fn, message in (
        (
            review.execute_pair15,
            "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            review.replay_existing_pair,
            "V2R13_EXISTING_PAIR_REPLAY_NOT_AUTHORIZED",
        ),
        (
            review.promote_or_train_candidate,
            "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            review.V2R13PostPair09EvaluationDesignReviewHold,
            match=message,
        ):
            fn()
