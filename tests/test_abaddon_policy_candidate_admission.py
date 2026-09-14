from __future__ import annotations

from openra_env.learning.abaddon_policy_candidate_admission import (
    REVIEW_SCHEMA,
    classify_abaddon_policy_candidate_pair_for_training,
    pair_sha256,
)
from openra_env.learning.general_brain_generation import (
    classify_abaddon_from_apollyon_v22_pair,
)

PAIR_SCHEMA = "void.abaddon.policy-candidate-pair-comparison.v1"


def pair(*, good=True):
    return {
        "schema": PAIR_SCHEMA,
        "candidate_only": True,
        "review_required": True,
        "candidate": {
            "trajectory_sha256": "1" * 64,
            "candidate_genome_sha256": "2" * 64,
            "candidate_file_sha256": "3" * 64,
            "wrapper_sha256": "4" * 64,
            "legacy_runner_sha256": "5" * 64,
            "abaddon_controller_sha256": "6" * 64,
            "abaddon_refiner_sha256": "7" * 64,
        },
        "comparison": {
            "verdict": "BETTER" if good else "TIE",
            "force_preservation_pass": good,
            "protocol_clean": True,
            "productive_contact_pass": good,
            "host_acceptance_pass": True,
            "review_candidate_pass": good,
        },
        "authority": {
            "training_performed": False,
            "weights_updated": False,
            "automatic_corpus_admission": False,
            "automatic_weight_mutation": False,
            "automatic_promotion": False,
        },
    }


def review_for(value):
    return {
        "schema": REVIEW_SCHEMA,
        "general_id": "abaddon",
        "pair_sha256": pair_sha256(value),
        "reviewer": "human-review-fixture",
        "review_complete": True,
        "candidate_identity_reviewed": True,
        "comparison_reviewed": True,
        "training_use_approved": True,
    }


def test_raw_pair_without_review_stays_ineligible():
    result = classify_abaddon_policy_candidate_pair_for_training(pair())
    assert result["eligible"] is False
    assert "ABADDON_REVIEW_REQUIRED" in result["reasons"]
    assert result["automatic_corpus_admission"] is False
    assert result["automatic_weight_mutation"] is False
    assert result["automatic_promotion"] is False


def test_review_pair_digest_mismatch_is_rejected():
    value = pair()
    review = review_for(value)
    review["pair_sha256"] = "0" * 64
    result = classify_abaddon_policy_candidate_pair_for_training(
        value,
        review=review,
    )
    assert result["eligible"] is False
    assert "ABADDON_REVIEW_PAIR_SHA_MISMATCH" in result["reasons"]


def test_complete_manual_review_can_admit_valid_better_pair():
    value = pair()
    result = classify_abaddon_policy_candidate_pair_for_training(
        value,
        review=review_for(value),
    )
    assert result["eligible"] is True
    assert result["training_role"] == "positive_tactical_example"
    assert result["candidate_trajectory_sha256"] == "1" * 64
    assert result["candidate_genome_sha256"] == "2" * 64
    assert result["reviewed_pair_sha256"] == pair_sha256(value)
    assert result["authority_envelope_trainable"] is False


def test_failed_comparison_remains_ineligible_even_with_review():
    value = pair(good=False)
    result = classify_abaddon_policy_candidate_pair_for_training(
        value,
        review=review_for(value),
    )
    assert result["eligible"] is False
    assert "ABADDON_NOT_BETTER" in result["reasons"]
    assert "ABADDON_REVIEW_CANDIDATE_FAILED" in result["reasons"]


def test_legacy_apollyon_pair_classifier_remains_fail_closed():
    result = classify_abaddon_from_apollyon_v22_pair({})
    assert result["eligible"] is False
    assert result["reasons"] == [
        "ABADDON_REQUIRES_SYMMETRIC_REVIEWED_CHALLENGER_EVIDENCE"
    ]
