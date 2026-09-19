from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_forensics_acceptance_generation2
    as acceptance,
)


def test_exact_failed_retry_forensics_are_accepted():
    out = (
        acceptance
        .v2r13_pair03_baseline_failed_retry_forensics_acceptance_contract()
    )
    assert out["failed_retry_forensics_accepted"] is True
    assert out["forensics_wrapper_sha256"] == (
        "9922da0e8d696bfde713c871924d3d27375776226965ac4bf15a3fb2a708f7dd"
    )
    assert out["forensics_sha256"] == (
        "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d"
    )


def test_failure_is_before_controller_inference():
    out = acceptance.accept_pair03_baseline_failed_retry_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["runtime_started"] is True
    assert out["warm_start_completed"] is True
    assert out["fresh_readiness_failed_before_controller_inference"] is True
    assert out["failure_was_ollama_ps_residency_gate"] is True
    assert out["catalog_model_alias_verified"] is True
    assert out["catalog_model_digest_verified"] is True
    assert out["controller_inference_performed"] is False
    assert out["controller_trajectory_present"] is False
    assert out["controller_summary_present"] is False
    assert out["successful_execution_receipt_present"] is False


def test_cleanup_is_complete_and_original_archive_survives():
    out = acceptance.accept_pair03_baseline_failed_retry_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["runtime_cleanup_completed"] is True
    assert out["source_worktree_cleaned"] is True
    assert out["engine_worktree_cleaned"] is True
    assert out["ollama_dormant_after_failure"] is True
    assert out["runtime_processes_remaining"] is False
    assert out["runtime_listeners_remaining"] is False
    assert out["runtime_containers_remaining"] is False
    assert out["first_attempt_archive_preserved"] is True
    assert out["first_attempt_preservation_receipt_preserved"] is True


def test_retry_authorization_is_consumed_and_no_new_retry_is_created():
    out = (
        acceptance
        .v2r13_pair03_baseline_failed_retry_forensics_acceptance_contract()
    )
    assert out["retry_authorization_consumed"] is True
    assert out["additional_retry_authorized"] is False
    assert out["additional_retry_performed"] is False
    assert out["failed_retry_preservation_required"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_REQUIRED",
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("retry_warm_start_present", False),
        ("execution_receipt_exists", True),
        ("retry_execution_receipt_present", True),
        ("retry_controller_inference_performed", True),
        ("source_worktree_exists", True),
        ("engine_worktree_registered", True),
        ("first_attempt_archive_present", False),
        ("additional_retry_performed", True),
        ("forensics_mutation_performed", True),
        ("ollama_active", "active"),
    ],
)
def test_tampered_failed_retry_forensics_are_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair03BaselineFailedRetryForensicsAcceptanceHold,
        match=f"failed-retry evidence drift: {field}",
    ):
        acceptance.accept_pair03_baseline_failed_retry_forensics(evidence)


def test_failed_retry_forensic_field_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["additional_retry_authorized"] = True
    with pytest.raises(
        acceptance.V2R13Pair03BaselineFailedRetryForensicsAcceptanceHold,
        match="failed-retry evidence field-set drift",
    ):
        acceptance.accept_pair03_baseline_failed_retry_forensics(evidence)


def test_preservation_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair03BaselineFailedRetryForensicsAcceptanceHold,
        match="V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_REQUIRED",
    ):
        acceptance.preserve_failed_retry()
