from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry2_execution_evidence_acceptance_generation2
    as acceptance,
)


def test_exact_retry2_evidence_is_accepted():
    out = acceptance.v2r13_pair03_baseline_retry2_execution_evidence_acceptance_contract()
    assert out["retry2_execution_evidence_accepted"] is True
    assert out["launcher_sha256"] == (
        "e48dff60a089ed3cfa75729ecaec60cb52d41037663eb46cb1a8929540ac833c"
    )
    assert out["execution_main_head"] == (
        "3432cc19f7612f7e3819eefe2c207d302cd4b580"
    )


def test_retry2_receipts_and_run_artifact_are_exact():
    out = acceptance.accept_pair03_baseline_retry2_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    evidence = out["evidence"]
    assert evidence["additional_retry_invocation_receipt_sha256"] == (
        "9075720e81a55afe02d285d541c559e5cd9b03a32251d36d39c4ef4362052e74"
    )
    assert evidence["underlying_invocation_receipt_sha256"] == (
        "2f242dbd6ff5840074b74b554cf330c59755a29cfd17d35feda182a6424e3694"
    )
    assert evidence["underlying_executor_receipt_sha256"] == (
        "352677479e3a2864ee5a792bc2557b77bcfeccb0f497920f9784a8b82cd75e4d"
    )
    assert evidence["execution_receipt_file_sha256"] == (
        "0bf4fd6f780eaddec758c785f16b456cd4707a67ad01fd7a0d8af7bafb06da86"
    )
    assert evidence["trajectory_sha256"] == (
        "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
    )
    assert evidence["summary_sha256"] == (
        "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
    )


def test_retry2_completed_once_and_consumed_authority():
    out = acceptance.accept_pair03_baseline_retry2_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["retry_index"] == 2
    assert out["additional_retry_authorization_consumed"] is True
    assert out["additional_retry_execution_performed"] is True
    assert out["remaining_additional_retry_executions"] == 0
    assert out["runtime_execution_performed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["runtime_cleanup_completed"] is True
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36


def test_retry2_acceptance_grants_no_follow_on_execution():
    out = acceptance.accept_pair03_baseline_retry2_execution_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["automatic_retry"] is False
    assert out["recursive_retry"] is False
    assert out["another_retry_authorized"] is False
    assert out["candidate_arm_authorized"] is False
    assert out["candidate_arm_executed"] is False
    assert out["held_out_arm_authorized"] is False
    assert out["held_out_arm_executed"] is False


def test_retry2_acceptance_grants_no_training_or_promotion():
    out = acceptance.accept_pair03_baseline_retry2_execution_evidence(
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
        ("additional_retry_authorization_consumed", False),
        ("additional_retry_execution_performed", False),
        ("remaining_additional_retry_executions", 1),
        ("runtime_execution_performed", False),
        ("fresh_runtime_readiness_admitted", False),
        ("runtime_cleanup_completed", False),
        ("candidate_arm_executed", True),
        ("held_out_arm_executed", True),
        ("training_performed", True),
        ("automatic_policy_promotion", True),
        ("ollama_active_after", "active"),
        ("activation_permit_present_after", True),
    ],
)
def test_tampered_retry2_evidence_is_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair03BaselineRetry2ExecutionEvidenceAcceptanceHold,
        match=f"retry-2 evidence drift: {field}",
    ):
        acceptance.accept_pair03_baseline_retry2_execution_evidence(evidence)


def test_retry2_evidence_field_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["candidate_execution_authorized"] = True
    with pytest.raises(
        acceptance.V2R13Pair03BaselineRetry2ExecutionEvidenceAcceptanceHold,
        match="retry-2 evidence field-set drift",
    ):
        acceptance.accept_pair03_baseline_retry2_execution_evidence(evidence)


def test_acceptance_advances_only_to_source_binding_review():
    out = acceptance.v2r13_pair03_baseline_retry2_execution_evidence_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_RETRY2_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_follow_on_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair03BaselineRetry2ExecutionEvidenceAcceptanceHold,
        match=(
            "V2R13_PAIR03_BASELINE_RETRY2_EXECUTION_EVIDENCE_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
    ):
        acceptance.authorize_candidate_or_retry()
