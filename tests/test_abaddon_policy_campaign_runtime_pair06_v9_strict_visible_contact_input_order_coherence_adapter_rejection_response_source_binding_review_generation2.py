from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_shim_and_tests_to_repository_bytes():
    out = review.pair06_v9_input_order_adapter_rejection_response_review_contract()

    assert out["shim_path"] == review.SHIM_PATH
    assert out["shim_git_blob"] == review.SHIM_GIT_BLOB
    assert out["shim_test_path"] == review.SHIM_TEST_PATH
    assert out["shim_test_git_blob"] == review.SHIM_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.SHIM_PATH).read_bytes()) == (
        review.SHIM_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.SHIM_TEST_PATH).read_bytes()) == (
        review.SHIM_TEST_GIT_BLOB
    )


def test_review_preserves_exact_observed_error_boundary():
    out = review.pair06_v9_input_order_adapter_rejection_response_review_contract()

    assert out["observed_retryable_error"] == "unit_ids invalid"
    assert out["sentinel_tool"] == "__v8_adapter_rejected_unit_ids_invalid__"
    assert out["only_exact_observed_adapter_error_is_retryable"] is True
    assert out["other_v8_adapter_errors_still_propagate"] is True
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
    out = review.pair06_v9_input_order_adapter_rejection_response_review_contract()
    assert out[field] is False


def test_review_advances_only_to_parent_integration():
    out = review.pair06_v9_input_order_adapter_rejection_response_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_PARENT_INTEGRATION_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderAdapterRejectionResponseReviewHold,
        match="ADAPTER_REJECTION_PARENT_INTEGRATION_REQUIRED",
    ):
        review.execute()
