from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_evidence_acceptance_generation2
    as acceptance,
)


def test_exact_candidate_evidence_is_accepted():
    out = acceptance.v2r13_pair03_candidate_execution_evidence_acceptance_contract()
    assert out["candidate_execution_evidence_accepted"] is True
    assert out["execution_main_head"] == "ea218d29cf6ae55058754379159d318cd1be71aa"
    assert out["validation_main_head"] == "f32437d2dbbb3a5e702f661494e427c30f6e6136"
    assert out["pair_slot"] == 3
    assert out["arm"] == "candidate"
    assert out["held_out"] is False


def test_completed_candidate_receipts_and_artifacts_are_exact():
    out = acceptance.accept_pair03_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    evidence = out["evidence"]
    assert evidence["attempt_marker_sha256"] == (
        "0ab9062efa497457a6e7d42a149e302b3809887f54c7b1e1112b86b5ec2d7f79"
    )
    assert evidence["result_file_sha256"] == (
        "9be2b3a74205cd6102f5839171638431ef25cb4f57db1028033ef2498f740829"
    )
    assert evidence["executor_receipt_sha256"] == (
        "396c9e535ab92ada204aee31e1442fa68841adcbd2b231709d945f72c0bf78f9"
    )
    assert evidence["warm_start_sha256"] == (
        "334846e59a956c1f8e059979f56c1775b39e1d51ef42c172e09fc7ab022a8a3a"
    )
    assert evidence["trajectory_sha256"] == (
        "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65"
    )
    assert evidence["summary_sha256"] == (
        "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0"
    )


def test_candidate_execution_completed_once_and_is_not_replayable():
    out = acceptance.accept_pair03_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["candidate_attempt_consumed"] is True
    assert out["candidate_execution_performed"] is True
    assert out["candidate_completed_result_present"] is True
    assert out["candidate_execution_replay_required"] is False
    assert out["candidate_execution_replay_permitted"] is False
    assert out["runtime_cleanup_completed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["completed_baseline_preserved"] is True
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36


def test_candidate_acceptance_keeps_all_follow_on_authority_closed():
    out = acceptance.accept_pair03_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["automatic_retry"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["pair09_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
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


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("candidate_attempt_consumed", False),
        ("candidate_completed_result_present", False),
        ("candidate_execution_performed", False),
        ("candidate_execution_replay_permitted", True),
        ("runtime_cleanup_completed", False),
        ("fresh_runtime_readiness_admitted", False),
        ("completed_baseline_preserved", False),
        ("automatic_retry", True),
        ("training_performed", True),
        ("automatic_policy_promotion", True),
        ("wallet_or_funds_action_performed", True),
    ],
)
def test_tampered_candidate_evidence_is_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair03CandidateExecutionEvidenceAcceptanceHold,
        match=f"candidate evidence drift: {field}",
    ):
        acceptance.accept_pair03_candidate_execution_evidence(evidence)


def test_candidate_evidence_field_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["promotion_permit"] = True
    with pytest.raises(
        acceptance.V2R13Pair03CandidateExecutionEvidenceAcceptanceHold,
        match="candidate evidence field-set drift",
    ):
        acceptance.accept_pair03_candidate_execution_evidence(evidence)


def test_acceptance_advances_only_to_source_binding_review():
    out = acceptance.v2r13_pair03_candidate_execution_evidence_acceptance_contract()
    assert out["candidate_result_review_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_follow_on_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair03CandidateExecutionEvidenceAcceptanceHold,
        match=(
            "V2R13_PAIR03_CANDIDATE_EXECUTION_EVIDENCE_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
    ):
        acceptance.authorize_follow_on_execution()
