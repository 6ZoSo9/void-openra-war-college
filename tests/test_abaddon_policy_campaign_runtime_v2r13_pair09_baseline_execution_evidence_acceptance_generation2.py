from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_execution_evidence_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_durable_execution_evidence():
    out = acceptance.v2r13_pair09_baseline_execution_evidence_acceptance_contract()
    assert out["pair09_baseline_execution_evidence_accepted"] is True
    assert out["launcher_sha256"] == (
        "1ef774f2de9323eb7ef01762574d1fc8ec1df8b557bf9b6e083028ca2388a945"
    )
    assert out["execution_main_head"] == (
        "361b5e8a4033515d6bdd3a7f50456c778df5aa5f"
    )
    assert out["attempt_consumed"] is True
    assert out["maximum_attempts"] == 1


def test_accepted_evidence_pins_marker_result_and_run_artifacts():
    out = acceptance.accept_pair09_baseline_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["attempt_marker_sha256"] == (
        "57f862fe39a8939f3d47d4184fe264e0b9cd3988143f4cdc3adb9973a0e2e41c"
    )
    assert out["result_file_sha256"] == (
        "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
    )
    assert out["run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260922T211556Z-feinter-s1496195137"
    )
    assert out["seed"] == 1496195137
    assert out["warm_start_sha256"] == (
        "d40816f63f86b5103b9d181ecc31e6b694005c1f3032a1b3fc614a209f2d7790"
    )
    assert out["trajectory_sha256"] == (
        "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
    )
    assert out["summary_sha256"] == (
        "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
    )


def test_pair09_baseline_measurement_is_complete_but_nondeci­sive():
    out = acceptance.accept_pair09_baseline_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["runtime_execution_performed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["runtime_cleanup_completed"] is True
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551


def test_pair03_evidence_is_preserved_and_no_followon_execution_is_authorized():
    out = acceptance.accept_pair09_baseline_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair03_baseline_preserved"] is True
    assert out["pair03_candidate_preserved"] is True
    assert out["another_baseline_execution_authorized"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False
    assert out["automatic_retry"] is False


def test_acceptance_grants_no_training_promotion_or_external_authority():
    out = acceptance.accept_pair09_baseline_execution_evidence(
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
        ("arm", "candidate"),
        ("automatic_retry", True),
        ("runtime_cleanup_completed", False),
        ("pair03_candidate_preserved", False),
        ("training_performed", True),
        ("automatic_abaddon_policy_promotion", True),
    ],
)
def test_evidence_mutation_is_rejected(field, value):
    evidence = dict(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair09BaselineExecutionEvidenceAcceptanceHold,
        match="pair09 baseline evidence drift",
    ):
        acceptance.accept_pair09_baseline_execution_evidence(evidence)


def test_acceptance_advances_only_to_separate_source_review():
    out = acceptance.v2r13_pair09_baseline_execution_evidence_acceptance_contract()
    assert out["baseline_result_review_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_followon_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair09BaselineExecutionEvidenceAcceptanceHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.authorize_follow_on_execution()
