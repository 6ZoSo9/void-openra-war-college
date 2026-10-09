from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_unit_ids_canonicalization_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_repair_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract()
    )
    assert out["repair_git_blob"] == review.REPAIR_GIT_BLOB
    assert out["repair_test_git_blob"] == review.REPAIR_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.REPAIR_PATH).read_bytes()) == (
        review.REPAIR_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.REPAIR_TEST_PATH).read_bytes()) == (
        review.REPAIR_TEST_GIT_BLOB
    )


def test_review_binds_consumed_v3_failure_identity():
    out = (
        review
        .pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract()
    )
    assert out[
        "pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_reviewed"
    ] is True
    assert out["consumed_v3_main_head"] == (
        "e983220f85e35c024bcc0da8dec418bcd8342e03"
    )
    assert out["observed_v3_failed_round"] == 6
    assert out["observed_v3_max_attempts"] == 6
    assert out["observed_v3_terminal_feedback"].startswith(
        "function_not_offered:"
    )


def test_review_requires_owned_ids_and_frozen_v8_revalidation():
    out = (
        review
        .pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract()
    )
    assert out["canonicalizable_bare_positive_integer"] is True
    assert out[
        "canonicalizable_nonempty_distinct_positive_integer_list"
    ] is True
    assert out["all_candidate_ids_must_be_currently_owned"] is True
    assert out["foreign_ids_fail_closed"] is True
    assert out["duplicate_ids_fail_closed"] is True
    assert out["canonical_output_revalidated_by_frozen_v8_translator"] is True
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
        "replay_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_opens_no_runtime_or_extra_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract()
    )
    assert out[field] is False


def test_review_stops_at_v4_runtime_integration():
    out = (
        review
        .pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V4_RUNTIME_INTEGRATION_REQUIRED"
    )


def test_integrate_or_execute_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationReviewHold,
        match="ACTIONABLE_FEEDBACK_V4_RUNTIME_INTEGRATION_REQUIRED",
    ):
        review.integrate_or_execute()
