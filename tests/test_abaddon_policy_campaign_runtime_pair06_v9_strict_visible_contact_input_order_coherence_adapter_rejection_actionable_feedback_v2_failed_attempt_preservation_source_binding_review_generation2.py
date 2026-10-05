from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_preservation_and_test_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract()
    )

    assert out["preservation_path"] == review.PRESERVATION_PATH
    assert out["preservation_git_blob"] == review.PRESERVATION_GIT_BLOB
    assert out["preservation_test_path"] == review.PRESERVATION_TEST_PATH
    assert out["preservation_test_git_blob"] == review.PRESERVATION_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.PRESERVATION_PATH).read_bytes()) == (
        review.PRESERVATION_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.PRESERVATION_TEST_PATH).read_bytes()) == (
        review.PRESERVATION_TEST_GIT_BLOB
    )


def test_review_binds_exact_v2_failed_attempt_evidence():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v2_failed_attempt_preservation_reviewed"
    ] is True
    assert out["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["attempt_marker_bytes"] == 2208
    assert out["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert out["warm_start_bytes"] == 229255
    assert out["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )
    assert out["trajectory_bytes"] == 58075


def test_review_binds_terminal_failure():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract()
    )

    assert out["failure_class"] == "strict_contact_actionable_feedback_v2_exhausted"
    assert out["failure_round"] == 6
    assert out["maximum_decision_attempts"] == 6
    assert out["terminal_feedback"] == (
        "function_not_offered:"
        "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
        "not_json_array_or_bare_integer__"
    )


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "preservation_authorization_accepted",
        "preservation_performed",
    ),
)
def test_review_grants_no_mutation_or_retry_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_preservation_authorization_request():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_request_or_preserve_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2FailedAttemptPreservationReviewHold,
        match="PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_or_preserve()
