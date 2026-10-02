from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_closeout_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_closeout_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_review_contract()
    )

    assert out["closeout_path"] == review.CLOSEOUT_PATH
    assert out["closeout_git_blob"] == review.CLOSEOUT_GIT_BLOB
    assert out["closeout_test_path"] == review.CLOSEOUT_TEST_PATH
    assert out["closeout_test_git_blob"] == review.CLOSEOUT_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.CLOSEOUT_PATH).read_bytes()) == (
        review.CLOSEOUT_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.CLOSEOUT_TEST_PATH).read_bytes()) == (
        review.CLOSEOUT_TEST_GIT_BLOB
    )


def test_review_closes_consumed_attempt_and_preservation_authorization():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_reviewed"
    ] is True
    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["preservation_receipt_sha256"] == (
        "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
    )

    assert out["attempt_consumed"] is True
    assert out["attempt_reusable"] is False
    assert out["attempt_authorization_reusable"] is False
    assert out["preservation_authorization_consumed"] is True
    assert out["preservation_authorization_reusable"] is False
    assert out["preservation_lineage_closed"] is True


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "new_execution_request_opened",
    ),
)
def test_review_grants_no_runtime_or_follow_on_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_review_contract()
    )
    assert out[field] is False


def test_review_requires_fresh_execution_authorization_for_any_future_run():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_review_contract()
    )

    assert out["fresh_execution_authorization_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FRESH_EXECUTION_REQUEST_REQUIRED"
    )


def test_request_or_reopen_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionPreservationCloseoutReviewHold,
        match="ADAPTER_REJECTION_FRESH_EXECUTION_REQUEST_REQUIRED",
    ):
        review.request_or_reopen()
