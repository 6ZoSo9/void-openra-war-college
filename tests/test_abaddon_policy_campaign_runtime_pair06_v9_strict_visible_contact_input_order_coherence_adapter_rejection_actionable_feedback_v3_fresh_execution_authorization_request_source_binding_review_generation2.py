from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_fresh_execution_authorization_request_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_request_and_tests_to_exact_bytes():
    out = review.pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract()
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


def test_review_binds_v2_operator_and_closed_failed_lineage():
    out = review.pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract()
    assert out["pair06_v9_actionable_feedback_v3_fresh_execution_request_reviewed"] is True
    assert out["fresh_operator_git_blob"] == review.FRESH_OPERATOR_GIT_BLOB
    assert out["fresh_operator_review_git_blob"] == review.FRESH_OPERATOR_REVIEW_GIT_BLOB
    assert out["prior_attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["preservation_receipt_sha256"] == (
        "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
    )
    assert out["fresh_actionable_feedback_v3_evidence_namespace_required"] is True


def test_review_preserves_runtime_safety_and_five_authorizations():
    out = review.pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract()
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["five_explicit_authorizations_required"] is True
    assert out["five_distinct_confirmation_tokens_required"] is True
    assert out["fresh_user_authorization_text_required"] is True


def test_review_refuses_general_or_prior_authorization_reuse():
    out = review.pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract()
    assert out["general_source_work_authorization_is_execution_authorization"] is False
    assert out["prior_authorization_text_reusable"] is False
    assert out["preservation_authorization_reusable_as_execution_authority"] is False


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v3_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_execution_or_follow_on_authority(field):
    out = review.pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract()
    assert out[field] is False


def test_review_advances_only_to_fresh_execution_authorization():
    out = review.pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_FRESH_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_execute_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV3FreshExecutionRequestReviewHold,
        match="ACTIONABLE_FEEDBACK_V3_FRESH_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.accept_or_execute()
