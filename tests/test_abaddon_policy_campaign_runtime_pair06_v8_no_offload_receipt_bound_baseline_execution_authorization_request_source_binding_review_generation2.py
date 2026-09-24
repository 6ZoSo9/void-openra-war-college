from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_replacement_request_bytes():
    out = review.pair06_v8_no_offload_receipt_bound_request_review_contract()
    assert out["request_git_blob"] == "d6bb79437e0dd7cbff669ec3b21aadbf2365bf70"
    assert out["request_source_sha256"] == (
        "78a93d011f2c7b14e370387e5d5d2479b5d6837ecd55da143460f257b167f278"
    )
    assert out["request_test_git_blob"] == "78714d94cd9428ba43f91bcd24f8076b2199efe4"
    assert out["request_test_sha256"] == (
        "55dd521cb2201df14890f748c3a806e923c58a34494e21ae576f05ff73a2657f"
    )
    assert out["request_bytes_sha256"] == (
        "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
    )
    assert out["request_byte_length"] == 4828
    assert out["request_sha256"] == out["request_bytes_sha256"]


def test_review_records_superseded_authorization_as_unconsumed():
    out = review.pair06_v8_no_offload_receipt_bound_request_review_contract()
    assert out["superseded_request_sha256"] == (
        "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
    )
    assert out["superseded_request_attempt_consumed"] is False
    assert out["superseded_request_reusable"] is False
    assert out["no_offload_parent_receipt_schema_bound"] is True
    assert out["inference_safe_placement_receipt_required"] is True


def test_review_is_still_proposal_only():
    out = review.pair06_v8_no_offload_receipt_bound_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["pair06_no_offload_baseline_specific_authorization_accepted"] is False
    assert out["pair06_no_offload_baseline_execution_authorized"] is False
    assert out["pair06_no_offload_baseline_execution_performed"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_stops_at_new_explicit_authorization():
    out = review.pair06_v8_no_offload_receipt_bound_request_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ReceiptBoundRequestReviewHold,
        match="RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
