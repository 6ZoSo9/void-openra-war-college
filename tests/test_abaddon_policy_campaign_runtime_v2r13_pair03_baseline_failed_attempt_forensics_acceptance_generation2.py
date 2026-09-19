from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_forensics_acceptance_generation2
    as acceptance,
)


def test_exact_forensics_are_accepted():
    out = acceptance.v2r13_pair03_baseline_failed_attempt_forensics_acceptance_contract()
    assert out["failed_attempt_forensics_accepted"] is True
    assert out["forensics_wrapper_sha256"] == (
        "24364e9ea26e67720d1f2e14310426a749cd891bca1564fc73809c78c4431bf3"
    )
    assert out["forensics_sha256"] == (
        "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d"
    )


def test_failure_is_classified_before_controller_inference():
    out = acceptance.accept_pair03_baseline_failed_attempt_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["runtime_started"] is True
    assert out["warm_start_completed"] is True
    assert out["fresh_readiness_failed_before_controller_inference"] is True
    assert out["controller_inference_performed"] is False
    assert out["controller_trajectory_present"] is False
    assert out["controller_summary_present"] is False
    assert out["successful_execution_receipt_present"] is False


def test_runtime_cleanup_is_complete_and_dormant():
    out = acceptance.accept_pair03_baseline_failed_attempt_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["runtime_cleanup_completed"] is True
    assert out["frozen_source_worktree_cleaned"] is True
    assert out["engine_worktree_cleaned"] is True
    assert out["ollama_dormant_after_failure"] is True
    assert out["runtime_processes_remaining"] is False
    assert out["runtime_listeners_remaining"] is False
    assert out["runtime_containers_remaining"] is False


def test_surviving_warm_start_artifact_is_exact():
    out = acceptance.accept_pair03_baseline_failed_attempt_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["warm_start_sha256"] == (
        "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
    )
    assert out["warm_start_bytes"] == 223319


def test_forensics_does_not_authorize_retry():
    out = acceptance.v2r13_pair03_baseline_failed_attempt_forensics_acceptance_contract()
    assert out["automatic_retry_performed"] is False
    assert out["retry_authorized"] is False
    assert out["failed_attempt_preservation_required_before_retry"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("arm_root_exists", False),
        ("warm_start_completed", False),
        ("controller_inference_performed", True),
        ("controller_trajectory_present", True),
        ("controller_summary_present", True),
        ("runtime_execution_receipt_present", True),
        ("frozen_source_worktree_exists", True),
        ("engine_worktree_registered", True),
        ("automatic_retry_performed", True),
        ("forensics_mutation_performed", True),
    ],
)
def test_tampered_forensics_are_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair03BaselineFailedAttemptForensicsAcceptanceHold,
        match=f"forensic evidence drift: {field}",
    ):
        acceptance.accept_pair03_baseline_failed_attempt_forensics(evidence)


def test_evidence_field_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["retry_allowed"] = True
    with pytest.raises(
        acceptance.V2R13Pair03BaselineFailedAttemptForensicsAcceptanceHold,
        match="forensic evidence field-set drift",
    ):
        acceptance.accept_pair03_baseline_failed_attempt_forensics(evidence)


def test_preservation_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair03BaselineFailedAttemptForensicsAcceptanceHold,
        match="V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    ):
        acceptance.preserve_failed_attempt()
