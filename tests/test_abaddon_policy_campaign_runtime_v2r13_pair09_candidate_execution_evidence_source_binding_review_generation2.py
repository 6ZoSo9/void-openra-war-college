from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_execution_evidence_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_tests():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == (
        "6ef46ea61b3725c846c56ebc16d7bdf3b8d8fcc9"
    )
    assert out["acceptance_source_sha256"] == (
        "408edb01b2bc50f6ed56c8c00de17476172056d52cd4a8f2d65b4e31d77809e1"
    )
    assert out["acceptance_test_git_blob"] == (
        "9ff4bff07170beeab6a3c86f7c5cc63624193802"
    )
    assert out["acceptance_test_sha256"] == (
        "689feeffa60a66e2ecb2664baad6ab19da54a2170030a2b66c1c1967a9af27f0"
    )


def test_review_accepts_exact_pair09_candidate_execution_scope():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
    assert out["candidate_execution_evidence_source_binding_present"] is True
    assert out["candidate_execution_evidence_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["attempt_consumed"] is True
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["baseline_rerun"] is False


def test_review_binds_completed_candidate_result():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["seed"] == 1496195137
    assert out["warm_start_sha256"] == (
        "e6f648dbf6710766869b5e5a3b0ec79c60e856d7c959e78cd93b1df8cfb3f1f8"
    )
    assert out["trajectory_sha256"] == (
        "d8de375133687e1296ff0f740bd9901eee24c65332ae8600ab03f724edcd0eae"
    )
    assert out["summary_sha256"] == (
        "15f4e21c8b2d9988c26f90a9fd3021ff017faef2ac1f6b289d0582cd6748f7e3"
    )
    assert out["result_file_sha256"] == (
        "68d86cea4a9806fca60a0bff765dce1227962acb923d6e4da3b5f7b1ab5ccb74"
    )


def test_review_binds_candidate_policy_and_preserves_history():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
    assert out["candidate_genome_sha256"] == (
        "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
    )
    assert out["pair03_baseline_preserved"] is True
    assert out["pair03_candidate_preserved"] is True
    assert out["pair09_baseline_preserved"] is True
    assert out["runtime_execution_performed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["runtime_cleanup_completed"] is True


def test_review_keeps_replay_and_followon_execution_closed():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
    assert out["candidate_execution_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False


def test_review_grants_no_training_promotion_or_external_authority():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
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


def test_review_advances_only_to_candidate_result_review():
    out = review.v2r13_pair09_candidate_execution_evidence_review_contract()
    assert out["candidate_result_review_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_RESULT_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_PAIR09_CANDIDATE_RESULT_REVIEW_REQUIRED"


def test_followon_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateExecutionEvidenceReviewHold,
        match="V2R13_PAIR09_CANDIDATE_RESULT_REVIEW_REQUIRED",
    ):
        review.authorize_follow_on_execution()
