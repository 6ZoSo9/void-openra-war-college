from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_policy_disposition_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_disposition_source_and_tests():
    out = review.v2r13_pair09_candidate_policy_disposition_review_contract()
    assert out["disposition_git_blob"] == (
        "ed5a241c847d73da3669e00348b29bbed686b712"
    )
    assert out["disposition_source_sha256"] == (
        "47924e98b89eff71973b55a9f474a348da77f2d8e3797654e53c7727b5f13124"
    )
    assert out["disposition_test_git_blob"] == (
        "820157b51efa13673e3f051d419b86f843ea4a97"
    )
    assert out["disposition_test_sha256"] == (
        "37b1d77f4ef46cd33c6e8db48ad7b9628a6af3bcda5693e1f5f0ef9f610cba68"
    )


def test_review_preserves_inconclusive_pair09_disposition():
    out = review.v2r13_pair09_candidate_policy_disposition_review_contract()
    assert out["pair_slot"] == 9
    assert out["policy_disposition_reviewed"] is True
    assert out["policy_disposition"] == (
        "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION"
    )
    assert out["candidate_preserved_as_evidence"] is True
    assert out["candidate_promoted"] is False
    assert out["candidate_rejected"] is False
    assert out["candidate_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["additional_bounded_evaluation_required"] is True
    assert out["post_pair09_evaluation_design_required"] is True


def test_review_keeps_held_out_and_mutation_authority_closed():
    out = review.v2r13_pair09_candidate_policy_disposition_review_contract()
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False
    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_review_advances_only_to_post_pair09_design():
    out = review.v2r13_pair09_candidate_policy_disposition_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_POST_PAIR09_EVALUATION_DESIGN_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_POST_PAIR09_EVALUATION_DESIGN_REQUIRED"
    )


def test_prohibited_action_entrypoints_hold():
    for fn, message in (
        (
            review.authorize_held_out_execution,
            "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            review.replay_candidate,
            "V2R13_PAIR09_CANDIDATE_REPLAY_NOT_AUTHORIZED",
        ),
        (
            review.promote_or_train_candidate,
            "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            review.V2R13Pair09CandidatePolicyDispositionReviewHold,
            match=message,
        ):
            fn()
