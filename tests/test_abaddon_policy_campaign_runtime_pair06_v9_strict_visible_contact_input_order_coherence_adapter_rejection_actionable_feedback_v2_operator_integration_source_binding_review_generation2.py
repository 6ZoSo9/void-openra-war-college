from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_operator_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_integration_and_tests_to_exact_repository_bytes():
    out = review.pair06_v9_actionable_feedback_v2_operator_integration_review_contract()

    assert out["integration_path"] == review.INTEGRATION_PATH
    assert out["integration_git_blob"] == review.INTEGRATION_GIT_BLOB
    assert out["integration_test_path"] == review.INTEGRATION_TEST_PATH
    assert out["integration_test_git_blob"] == review.INTEGRATION_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.INTEGRATION_PATH).read_bytes()) == (
        review.INTEGRATION_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.INTEGRATION_TEST_PATH).read_bytes()) == (
        review.INTEGRATION_TEST_GIT_BLOB
    )


def test_review_binds_v1_operator_and_v2_parent_exact_lineage():
    out = review.pair06_v9_actionable_feedback_v2_operator_integration_review_contract()

    assert out["v1_operator_integration_git_blob"] == (
        review.V1_OPERATOR_INTEGRATION_GIT_BLOB
    )
    assert out["v1_operator_review_git_blob"] == review.V1_OPERATOR_REVIEW_GIT_BLOB
    assert out["v2_parent_integration_git_blob"] == (
        review.V2_PARENT_INTEGRATION_GIT_BLOB
    )
    assert out["v2_parent_review_git_blob"] == review.V2_PARENT_REVIEW_GIT_BLOB


def test_review_preserves_operator_and_closes_consumed_namespace():
    out = review.pair06_v9_actionable_feedback_v2_operator_integration_review_contract()

    assert out["pair06_v9_actionable_feedback_v2_operator_integration_reviewed"] is True
    assert out["reviewed_v1_operator_integration_reused"] is True
    assert out["historical_operator_code_object_reused"] is True
    assert out["call_scoped_dependency_binding_upgraded_to_v2"] is True
    assert out["call_scoped_parent_binding_upgraded_to_v2"] is True
    assert out["reviewed_actionable_feedback_v2_parent_used"] is True
    assert out["historical_preclaim_gpu_ordering_preserved"] is True
    assert out["historical_one_attempt_cardinality_preserved"] is True

    assert out["consumed_input_order_namespace_reusable"] is False
    assert out["consumed_input_order_attempt_retry_authorized"] is False
    assert out["fresh_attempt_namespace_required_before_execution_request"] is True
    assert out["fresh_actionable_feedback_v2_activation_authorization_required"] is True
    assert out["fresh_operator_source_required_before_execution_request"] is True


@pytest.mark.parametrize(
    "field",
    (
        "consumed_input_order_namespace_reusable",
        "consumed_input_order_attempt_retry_authorized",
        "new_execution_request_opened",
        "actionable_feedback_v2_activation_authorization_accepted",
        "attempt_created",
        "runtime_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_execution_or_follow_on_authority(field):
    out = review.pair06_v9_actionable_feedback_v2_operator_integration_review_contract()
    assert out[field] is False


def test_review_advances_to_v2_fresh_lineage_operator_not_request():
    out = review.pair06_v9_actionable_feedback_v2_operator_integration_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_LINEAGE_OPERATOR_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_input_order_adapter_rejection_"
        "actionable_feedback_v2_fresh_lineage_operator"
    )


def test_execute_or_request_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2OperatorIntegrationReviewHold,
        match="ACTIONABLE_FEEDBACK_V2_FRESH_LINEAGE_OPERATOR_REQUIRED",
    ):
        review.execute_or_request()
