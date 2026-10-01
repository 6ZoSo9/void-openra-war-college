from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_integration_and_tests_to_repository_bytes():
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_parent_integration_review_contract()
    )

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


def test_review_preserves_scoped_parent_binding_only():
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_parent_integration_review_contract()
    )

    assert out[
        "pair06_v9_input_order_adapter_rejection_parent_integration_reviewed"
    ] is True
    assert out["historical_parent_run_code_reused"] is True
    assert out["call_scoped_child_command_binding_reused"] is True
    assert out["call_scoped_decision_response_binding_implemented"] is True
    assert out["process_global_parent_run_function_mutated"] is False
    assert out["process_global_child_command_builder_mutated"] is False
    assert out["process_global_decision_response_mutated"] is False
    assert out["malformed_unit_ids_coerced"] is False
    assert out["malformed_unit_ids_accepted"] is False


@pytest.mark.parametrize(
    "field",
    (
        "consumed_input_order_attempt_retry_authorized",
        "new_execution_request_opened",
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
def test_review_grants_no_runtime_or_follow_on_authority(field):
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_parent_integration_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_operator_integration():
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_parent_integration_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_OPERATOR_INTEGRATION_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderAdapterRejectionParentIntegrationReviewHold,
        match="ADAPTER_REJECTION_OPERATOR_INTEGRATION_REQUIRED",
    ):
        review.execute()
