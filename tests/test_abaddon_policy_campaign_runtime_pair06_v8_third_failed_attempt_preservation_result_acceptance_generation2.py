from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_result_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_third_preservation_terminal():
    out = acceptance.pair06_v8_third_preservation_result_acceptance_contract()
    assert out["pair06_v8_third_preservation_result_accepted"] is True
    assert out["attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["archive_name"] == "baseline-3ad564f9"
    assert out["third_failed_attempt_archived"] is True
    assert out["third_failed_attempt_deleted"] is False
    assert out["prior_failed_attempt_archives_unchanged"] is True
    assert out["fresh_baseline_arm_root_available"] is True


def test_acceptance_binds_preservation_receipt_identity():
    out = acceptance.pair06_v8_third_preservation_result_acceptance_contract()[
        "accepted_evidence"
    ]
    assert out["preservation_receipt_logical_sha256"] == (
        "9a7ec01af0f80d7a0d0333c91fd5c07d9ae24e04eaf87455fb143385ec76070b"
    )
    assert out["preservation_receipt_file_sha256"] == (
        "12a2da73143db442f5620065f8c270ef8026a641da2afa938203e51ceeaa43f4"
    )
    assert out["preservation_receipt_bytes"] == 3130


def test_acceptance_preserves_execution_head_and_grants_no_retry():
    out = acceptance.pair06_v8_third_preservation_result_acceptance_contract()
    assert out["authorized_execution_head_preserved"] == (
        "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
    )
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_evidence_tampering_fails_closed():
    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["baseline_path_freed"] = False
    with pytest.raises(
        acceptance.Pair06V8ThirdPreservationResultAcceptanceHold,
        match="third preservation evidence drift: baseline_path_freed",
    ):
        acceptance.accept_pair06_v8_third_preservation_result(tampered)


def test_acceptance_advances_only_to_result_review():
    out = acceptance.pair06_v8_third_preservation_result_acceptance_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8ThirdPreservationResultAcceptanceHold,
        match="PRESERVATION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.request_or_execute()
