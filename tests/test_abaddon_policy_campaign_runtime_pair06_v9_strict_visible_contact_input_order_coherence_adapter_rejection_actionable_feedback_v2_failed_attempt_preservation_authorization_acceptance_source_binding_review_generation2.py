from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_review_contract()
    )

    assert out["acceptance_path"] == review.ACCEPTANCE_PATH
    assert out["acceptance_git_blob"] == review.ACCEPTANCE_GIT_BLOB
    assert out["acceptance_test_path"] == review.ACCEPTANCE_TEST_PATH
    assert out["acceptance_test_git_blob"] == review.ACCEPTANCE_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_PATH).read_bytes()) == (
        review.ACCEPTANCE_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_TEST_PATH).read_bytes()) == (
        review.ACCEPTANCE_TEST_GIT_BLOB
    )


def test_review_binds_exact_authorization_and_canonical_main():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_reviewed"
    ] is True
    assert out["reviewed_request_sha256"] == (
        "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
    )
    assert out["reviewed_request_bytes"] == 3288
    assert out["authorization_text_sha256"] == (
        "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
    )
    assert out["authorization_text_bytes"] == 186
    assert out["canonical_main_head_at_authorization"] == (
        "000a8a01c29a8b42e91cb30f935ef63b72407f02"
    )
    assert out["canonical_main_tree_at_authorization"] == (
        "49b201ba723bcd4b8cab162f2d2d954534da6621"
    )


def test_review_accepts_only_preservation_authority():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_review_contract()
    )

    assert out["preservation_authorization_accepted"] is True
    assert out["preservation_authorized"] is True
    assert out["authority_scope_exact_reviewed_preservation_only"] is True
    assert out["preservation_performed"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["execution_request_opened"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["training_authorized"] is False
    assert out["deployment_authorized"] is False
    assert out["void_chain_mutation_authorized"] is False
    assert out["wallet_or_funds_action_authorized"] is False
    assert out["scheduler_mutation_authorized"] is False


def test_review_stops_at_authorized_host_preservation():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_HOST_EXECUTION_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceReviewHold,
        match="PRESERVATION_HOST_EXECUTION_REQUIRED",
    ):
        review.review_or_execute()
