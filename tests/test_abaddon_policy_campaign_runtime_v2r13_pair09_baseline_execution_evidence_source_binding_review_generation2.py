from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_execution_evidence_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_tests():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == (
        "cba3efec7f8884065b412d362f05048ccb2f2887"
    )
    assert out["acceptance_source_sha256"] == (
        "b3f5089079b01ba4f9ec928c20a094dabccfd506ae0d3827c32a8cc985d9030d"
    )
    assert out["acceptance_test_git_blob"] == (
        "deb05a86cda34d75486fe0a2e53785add85784bc"
    )
    assert out["acceptance_test_sha256"] == (
        "e7c8041d05208ac747963b4cc738987e2bb69b490bd13eb861efa0488eedaacb"
    )


def test_review_accepts_exact_pair09_baseline_execution_scope():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
    assert out["pair09_baseline_execution_evidence_source_binding_present"] is True
    assert out["pair09_baseline_execution_evidence_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["attempt_consumed"] is True
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False


def test_review_binds_exact_completed_result():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["warm_start_sha256"] == (
        "d40816f63f86b5103b9d181ecc31e6b694005c1f3032a1b3fc614a209f2d7790"
    )
    assert out["trajectory_sha256"] == (
        "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
    )
    assert out["summary_sha256"] == (
        "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
    )
    assert out["result_file_sha256"] == (
        "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
    )


def test_review_confirms_runtime_completion_and_pair03_preservation():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
    assert out["runtime_execution_performed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["runtime_cleanup_completed"] is True
    assert out["pair03_baseline_preserved"] is True
    assert out["pair03_candidate_preserved"] is True


def test_review_exhausts_baseline_attempt_and_keeps_followon_closed():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
    assert out["another_baseline_execution_authorized"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False


def test_review_grants_no_training_promotion_or_external_authority():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
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


def test_review_advances_only_to_baseline_result_review():
    out = review.v2r13_pair09_baseline_execution_evidence_review_contract()
    assert out["baseline_result_review_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_RESULT_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_PAIR09_BASELINE_RESULT_REVIEW_REQUIRED"


def test_followon_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09BaselineExecutionEvidenceReviewHold,
        match="V2R13_PAIR09_BASELINE_RESULT_REVIEW_REQUIRED",
    ):
        review.authorize_follow_on_execution()
