from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_fresh_execution_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out["acceptance_path"] == review.ACCEPTANCE_PATH
    assert out["acceptance_git_blob"] == review.ACCEPTANCE_GIT_BLOB
    assert out["acceptance_test_path"] == review.ACCEPTANCE_TEST_PATH
    assert out["acceptance_test_git_blob"] == review.ACCEPTANCE_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_PATH).read_bytes()) == (
        review.ACCEPTANCE_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_TEST_PATH).read_bytes()) == (
        review.ACCEPTANCE_TEST_GIT_BLOB
    )


def test_review_binds_exact_authorization_request_and_main_snapshot():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_reviewed"
    ] is True
    assert out["authorization_text_sha256"] == (
        "9fa7ed99b41b74f6ccfc161f8b2b20cc1fc76391b4a806e75583c6b3ee0ae932"
    )
    assert out["authorization_text_bytes"] == 624
    assert out["authorized_request_sha256"] == (
        "b3ff66271cabc9ed4d5be57c0a0fcd5b7e8cc69c65857fc0e35656f0c3464b2f"
    )
    assert out["authorized_request_bytes"] == 3113
    assert out["authorized_main_head"] == (
        "077c26ece41b2272fbf208d8e862df6a57462d39"
    )
    assert out["authorized_main_tree"] == (
        "0fe0093d6504591eaf94721aea662b3dfe923d05"
    )


def test_review_accepts_all_five_fresh_authorization_gates():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True
    assert out["actionable_feedback_v3_activation_authorization_accepted"] is True

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_actionable_feedback_v3_evidence_namespace_required"] is True


@pytest.mark.parametrize(
    "field",
    (
        "automatic_retry",
        "attempt_marker_created_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "execution_authorization_reusable_after_attempt_claim",
        "policy_activation_authorization_reusable_after_attempt_claim",
        "order_coherence_activation_authorization_reusable_after_attempt_claim",
        "repair_activation_authorization_reusable_after_attempt_claim",
        "actionable_feedback_v3_activation_authorization_reusable_after_attempt_claim",
    ),
)
def test_review_performs_no_effect_and_grants_no_follow_on_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorized_launcher():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV3FreshExecutionAuthorizationAcceptanceReviewHold,
        match="ACTIONABLE_FEEDBACK_V3_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED",
    ):
        review.execute()
