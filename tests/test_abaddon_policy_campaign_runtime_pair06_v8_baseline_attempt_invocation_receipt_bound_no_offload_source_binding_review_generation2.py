from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_receipt_bound_invocation_source_and_test():
    out = review.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_review_contract()
    assert out["invocation_git_blob"] == "f22313cc3481b806a30dee5a7009b62c25293f17"
    assert out["invocation_source_sha256"] == (
        "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
    )
    assert out["invocation_test_git_blob"] == "1f106f83502e6d802fd6cbffacf175985ee59ab6"
    assert out["invocation_test_sha256"] == (
        "d62591daee8896648686ee865587a945ba1c63471b464a3f45b6b5ec5bbe21af"
    )


def test_review_requires_receipt_schema_and_cuda_placement_evidence():
    out = review.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_review_contract()
    assert out["pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed"] is True
    assert out["no_offload_parent_receipt_schema_required"] is True
    assert out["inference_safe_placement_receipt_required"] is True
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["attempt_marker_create_only"] is True
    assert out["postclaim_reset_or_resume_available"] is False


def test_review_remains_non_authorizing():
    out = review.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_review_contract()
    assert out["explicit_authorization_required"] is True
    assert out["pair06_baseline_specific_authorization_accepted"] is False
    assert out["runtime_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False


def test_review_advances_only_to_replacement_request():
    out = review.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ReceiptBoundInvocationReviewHold,
        match="RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.execute_or_authorize()
