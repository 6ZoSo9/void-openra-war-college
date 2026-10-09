from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_runtime_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_runtime_integration_and_tests_to_exact_bytes():
    out = review.pair06_v9_actionable_feedback_v4_runtime_integration_review_contract()
    assert out["integration_git_blob"] == review.INTEGRATION_GIT_BLOB
    assert out["integration_test_git_blob"] == review.INTEGRATION_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.INTEGRATION_PATH).read_bytes()) == (
        review.INTEGRATION_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.INTEGRATION_TEST_PATH).read_bytes()) == (
        review.INTEGRATION_TEST_GIT_BLOB
    )


def test_review_binds_only_the_exact_v4_correction_path():
    out = review.pair06_v9_actionable_feedback_v4_runtime_integration_review_contract()
    assert out[
        "pair06_v9_actionable_feedback_v4_runtime_integration_reviewed"
    ] is True
    assert out["exact_terminal_feedback_trigger_only"] is True
    assert out["v4_repair_only_after_exact_unit_ids_invalid"] is True
    assert out["current_owned_ids_required_for_repair"] is True
    assert out["canonical_output_revalidated_by_frozen_v8_translator"] is True
    assert out["other_v8_translation_errors_propagate"] is True
    assert out["unsafe_or_ambiguous_unit_ids_fail_closed"] is True
    assert out["host_validator_modified"] is False
    assert out["host_validator_bypassed"] is False


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v3_attempt_retry_authorized",
        "new_execution_request_opened",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_runtime_or_extra_authority(field):
    out = review.pair06_v9_actionable_feedback_v4_runtime_integration_review_contract()
    assert out[field] is False


def test_review_stops_at_operator_integration():
    out = review.pair06_v9_actionable_feedback_v4_runtime_integration_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V4_OPERATOR_INTEGRATION_REQUIRED"
    )


def test_operational_entrypoint_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV4RuntimeIntegrationReviewHold,
        match="ACTIONABLE_FEEDBACK_V4_OPERATOR_INTEGRATION_REQUIRED",
    ):
        review.integrate_operator_or_execute()
