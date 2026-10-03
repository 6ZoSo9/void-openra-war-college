from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_v2_and_tests_to_exact_bytes():
    out = review.pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract()

    assert out["v2_path"] == review.V2_PATH
    assert out["v2_git_blob"] == review.V2_GIT_BLOB
    assert out["v2_test_path"] == review.V2_TEST_PATH
    assert out["v2_test_git_blob"] == review.V2_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.V2_PATH).read_bytes()) == (
        review.V2_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.V2_TEST_PATH).read_bytes()) == (
        review.V2_TEST_GIT_BLOB
    )


def test_review_binds_exact_actionable_feedback():
    out = review.pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract()

    assert out[
        "pair06_v9_adapter_rejection_actionable_feedback_v2_reviewed"
    ] is True
    assert out["v1_sentinel_tool"] == (
        "__v8_adapter_rejected_unit_ids_invalid__"
    )
    assert out["v2_sentinel_tool"] == (
        "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
        "not_json_array_or_bare_integer__"
    )
    assert out["expected_child_feedback"] == (
        "function_not_offered:"
        "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
        "not_json_array_or_bare_integer__"
    )

    assert out["feedback_requires_quoted_unit_ids_string"] is True
    assert out["feedback_rejects_json_array_unit_ids"] is True
    assert out["feedback_rejects_bare_integer_unit_ids"] is True


@pytest.mark.parametrize(
    "field",
    (
        "v1_source_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "six_attempt_decision_bound_modified",
        "host_validation_modified",
        "consumed_attempt_retry_authorized",
        "new_execution_request_opened",
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
    out = review.pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract()
    assert out[field] is False


def test_review_advances_only_to_v2_parent_integration():
    out = review.pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_PARENT_INTEGRATION_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionActionableFeedbackV2ReviewHold,
        match="ACTIONABLE_FEEDBACK_V2_PARENT_INTEGRATION_REQUIRED",
    ):
        review.execute()
