from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_requirements_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_requirements_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract()
    )

    assert out["requirements_path"] == review.REQUIREMENTS_PATH
    assert out["requirements_git_blob"] == review.REQUIREMENTS_GIT_BLOB
    assert out["requirements_test_path"] == review.REQUIREMENTS_TEST_PATH
    assert out["requirements_test_git_blob"] == review.REQUIREMENTS_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.REQUIREMENTS_PATH).read_bytes()) == (
        review.REQUIREMENTS_GIT_BLOB
    )
    assert _git_blob_sha1(
        (ROOT / review.REQUIREMENTS_TEST_PATH).read_bytes()
    ) == review.REQUIREMENTS_TEST_GIT_BLOB


def test_review_keeps_acceptance_unaccepted_until_specific_authorization():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_reviewed"
    ] is True
    assert out["exact_user_authorization_text_required"] is True
    assert out["authorization_text_sha256_binding_required"] is True
    assert out["authorization_text_byte_length_binding_required"] is True
    assert out["canonical_main_head_binding_required"] is True
    assert out["canonical_main_tree_binding_required"] is True
    assert out["canonical_main_must_be_bound_at_authorization_time"] is True
    assert out["authorization_must_reference_exact_reviewed_request"] is True
    assert (
        out["general_source_work_authorization_is_preservation_authorization"]
        is False
    )
    assert out["preservation_authorization_accepted"] is False
    assert out["preservation_performed"] is False


def test_review_binds_consumed_v2_evidence():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract()
    )

    assert out["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["attempt_marker_bytes"] == 2208
    assert out["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert out["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )
    assert out["failure_class"] == "strict_contact_actionable_feedback_v2_exhausted"
    assert out["failure_round"] == 6


@pytest.mark.parametrize(
    "field",
    (
        "preservation_authorization_accepted",
        "preservation_performed",
        "runtime_retry_authorized",
        "execution_request_opened",
        "runtime_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract()
    )
    assert out[field] is False


def test_review_stops_at_explicit_v2_preservation_authorization():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_preserve_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2PreservationAcceptanceRequirementsReviewHold,
        match="PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        review.accept_or_preserve()
