from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_execution_evidence_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_candidate_execution_evidence():
    out = acceptance.v2r13_pair09_candidate_execution_evidence_acceptance_contract()
    assert out["pair09_candidate_execution_evidence_accepted"] is True
    assert out["launcher_sha256"] == (
        "0705afdb696da7e2c3208f981a13a4e179548e9c526352475728001486137d94"
    )
    assert out["execution_main_head"] == (
        "7d5bf4c41c8a210a05fd9948f898c6cd8e5702d5"
    )
    assert out["attempt_consumed"] is True
    assert out["maximum_attempts"] == 1
    assert out["candidate_execution_replay_permitted"] is False


def test_accepted_evidence_pins_result_run_and_candidate_binding():
    out = acceptance.accept_pair09_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["attempt_marker_sha256"] == (
        "b7bd2dc0ac29bfe1095fe1d03e117708184a97499832859a9b068ecde13d5ce9"
    )
    assert out["result_file_sha256"] == (
        "68d86cea4a9806fca60a0bff765dce1227962acb923d6e4da3b5f7b1ab5ccb74"
    )
    assert out["run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260923T115438Z-feinter-s1496195137"
    )
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
    assert out["candidate_genome_sha256"] == (
        "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
    )


def test_candidate_measurement_completed_inside_reviewed_boundaries():
    out = acceptance.accept_pair09_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["runtime_execution_performed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["runtime_cleanup_completed"] is True
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["automatic_retry"] is False
    assert out["baseline_rerun"] is False


def test_predecessor_evidence_preserved_and_followon_authority_closed():
    out = acceptance.accept_pair09_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair03_baseline_preserved"] is True
    assert out["pair03_candidate_preserved"] is True
    assert out["pair09_baseline_preserved"] is True
    assert out["candidate_execution_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False


def test_acceptance_grants_no_training_promotion_or_external_authority():
    out = acceptance.accept_pair09_candidate_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
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
        ("attempt_consumed", False),
        ("result_present", False),
        ("pair_slot", 3),
        ("arm", "baseline"),
        ("automatic_retry", True),
        ("baseline_rerun", True),
        ("runtime_cleanup_completed", False),
        ("pair09_baseline_preserved", False),
        ("candidate_genome_sha256", "0" * 64),
        ("training_performed", True),
        ("automatic_abaddon_policy_promotion", True),
    ],
)
def test_evidence_mutation_is_rejected(field, value):
    evidence = dict(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair09CandidateExecutionEvidenceAcceptanceHold,
        match="pair09 candidate evidence drift",
    ):
        acceptance.accept_pair09_candidate_execution_evidence(evidence)


def test_acceptance_advances_only_to_separate_source_review():
    out = acceptance.v2r13_pair09_candidate_execution_evidence_acceptance_contract()
    assert out["candidate_result_review_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_followon_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair09CandidateExecutionEvidenceAcceptanceHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.authorize_follow_on_execution()
