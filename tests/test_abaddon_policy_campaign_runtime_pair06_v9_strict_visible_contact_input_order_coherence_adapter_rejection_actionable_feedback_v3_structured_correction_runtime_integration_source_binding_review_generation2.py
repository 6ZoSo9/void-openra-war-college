from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_runtime_integration_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
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


def test_review_binds_exact_trigger_structured_feedback_and_transfer_prompt():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v3_runtime_integration_reviewed"
    ] is True
    assert out["exact_v2_feedback_trigger_only"] is True
    assert out["nonmatching_feedback_delegates_to_v2_unchanged"] is True
    assert out["structured_feedback_injected_into_user_prompt"] is True
    assert out["corrective_retry_transfer_prompt_preserved"] is True
    assert out["corrective_retry_legacy_prompt_fallback_used"] is False
    assert out["v2_adapter_rejection_fail_closed_shim_reused"] is True


@pytest.mark.parametrize(
    "field",
    (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "process_global_parent_run_function_mutated",
        "process_global_decision_response_mutated",
        "process_global_runtime_method_mutated",
        "consumed_v2_attempt_retry_authorized",
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
def test_review_grants_no_runtime_or_extra_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_v3_operator_integration():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_OPERATOR_INTEGRATION_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9ActionableFeedbackV3RuntimeIntegrationReviewHold,
        match="V3_OPERATOR_INTEGRATION_REQUIRED",
    ):
        review.integrate_operator_or_execute()
