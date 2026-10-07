from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_operator_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_operator_integration_and_tests_to_exact_bytes():
    out = review.pair06_v9_actionable_feedback_v3_operator_integration_review_contract()

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


def test_review_binds_v3_parent_and_historical_operator_invariants():
    out = review.pair06_v9_actionable_feedback_v3_operator_integration_review_contract()

    assert out["pair06_v9_actionable_feedback_v3_operator_integration_reviewed"] is True
    assert out["reviewed_v2_operator_integration_reused"] is True
    assert out["historical_operator_code_object_reused"] is True
    assert out["call_scoped_dependency_binding_upgraded_to_v3"] is True
    assert out["call_scoped_parent_binding_upgraded_to_v3"] is True
    assert out["reviewed_actionable_feedback_v3_parent_used"] is True
    assert out["historical_preclaim_gpu_ordering_preserved"] is True
    assert out["historical_one_attempt_cardinality_preserved"] is True
    assert out["historical_automatic_retry_remains_false"] is True
    assert out["structured_feedback_injected_into_user_prompt"] is True
    assert out["corrective_retry_transfer_prompt_preserved"] is True
    assert out["v2_adapter_rejection_fail_closed_shim_reused"] is True


def test_review_requires_fresh_v3_lineage_before_execution_request():
    out = review.pair06_v9_actionable_feedback_v3_operator_integration_review_contract()

    assert out["fresh_attempt_namespace_required_before_execution_request"] is True
    assert out["fresh_actionable_feedback_v3_activation_authorization_required"] is True
    assert out["fresh_operator_source_required_before_execution_request"] is True
    assert out["consumed_v2_namespace_reusable"] is False
    assert out["consumed_v2_attempt_retry_authorized"] is False
    assert out["new_execution_request_opened"] is False
    assert out["actionable_feedback_v3_activation_authorization_accepted"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_runtime_or_follow_on_authority(field):
    out = review.pair06_v9_actionable_feedback_v3_operator_integration_review_contract()
    assert out[field] is False


def test_review_advances_only_to_fresh_v3_operator():
    out = review.pair06_v9_actionable_feedback_v3_operator_integration_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_FRESH_LINEAGE_OPERATOR_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9ActionableFeedbackV3OperatorIntegrationReviewHold,
        match="V3_FRESH_LINEAGE_OPERATOR_REQUIRED",
    ):
        review.build_fresh_operator_or_execute()
