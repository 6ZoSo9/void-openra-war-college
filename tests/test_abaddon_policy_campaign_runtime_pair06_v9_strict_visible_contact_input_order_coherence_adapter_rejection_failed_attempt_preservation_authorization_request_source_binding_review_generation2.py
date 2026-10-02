from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_request_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_request_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_request_review_contract()
    )

    assert out["request_path"] == review.REQUEST_PATH
    assert out["request_git_blob"] == review.REQUEST_GIT_BLOB
    assert out["request_test_path"] == review.REQUEST_TEST_PATH
    assert out["request_test_git_blob"] == review.REQUEST_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.REQUEST_PATH).read_bytes()) == (
        review.REQUEST_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.REQUEST_TEST_PATH).read_bytes()) == (
        review.REQUEST_TEST_GIT_BLOB
    )


def test_review_exposes_exact_deterministic_request_identity():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_request_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_preservation_authorization_request_reviewed"
    ] is True
    assert isinstance(out["request_sha256"], str)
    assert len(out["request_sha256"]) == 64
    assert out["request_bytes"] > 0
    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )


def test_review_requires_fresh_explicit_user_authorization():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_request_review_contract()
    )

    assert out["preservation_authorization_requested"] is True
    assert out["fresh_explicit_user_authorization_required"] is True
    assert (
        out["general_source_work_authorization_is_preservation_authorization"]
        is False
    )
    assert out["preservation_authorization_accepted"] is False
    assert out["preservation_performed"] is False


@pytest.mark.parametrize(
    "field",
    (
        "preservation_authorization_accepted",
        "preservation_performed",
        "runtime_retry_authorized",
        "execution_request_opened",
        "runtime_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_mutation_or_runtime_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_request_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorization_acceptance():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_request_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_AUTHORIZATION_ACCEPTANCE_REQUIRED"
    )


def test_accept_or_preserve_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionPreservationAuthorizationRequestReviewHold,
        match="PRESERVATION_AUTHORIZATION_ACCEPTANCE_REQUIRED",
    ):
        review.accept_or_preserve()
