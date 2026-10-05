from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_request_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_request_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
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


def test_review_binds_latest_closed_v2_failure():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_reviewed"
    ] is True
    assert isinstance(out["request_sha256"], str)
    assert len(out["request_sha256"]) == 64
    assert out["request_bytes"] > 0
    assert out["prior_v2_attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["prior_v2_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert out["prior_v2_attempt_consumed"] is True
    assert out["prior_v2_attempt_reusable"] is False
    assert out["prior_v2_execution_authorization_reusable"] is False
    assert out["prior_v2_preservation_authorization_reusable"] is False
    assert out["prior_v2_preservation_lineage_closed"] is True


def test_review_allows_source_reuse_but_not_authorization_reuse():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
    )

    assert out["reviewed_operator_source_reuse_requested"] is True
    assert out["reviewed_operator_authorization_reuse_requested"] is False
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["five_fresh_authorization_gates_required"] is True
    assert out["fresh_user_authorization_text_required"] is True
    assert out["canonical_main_binding_required_at_authorization_time"] is True


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "runtime_retry_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_execution_or_follow_on_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_fresh_authorization():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_FRESH_EXECUTION_"
        "AUTHORIZATION_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestReviewHold,
        match="POST_EXHAUSTION_FRESH_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.accept_or_execute()
