from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_review_contract()
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


def test_review_binds_exact_user_authorization_request_and_main():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_review_contract()
    )
    assert out[
        "pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_reviewed"
    ] is True
    assert out["authorization_text_sha256"] == (
        "ad844941da6c371a04c47bda2f77ad5bcbd46f667b5cb542916efe4d659cd765"
    )
    assert out["authorization_text_bytes"] == 760
    assert out["authorized_request_sha256"] == (
        "ae676de935142a83bbf8374621d5d41dcc81e9aa6910bf12507bcf6589ae8953"
    )
    assert out["authorized_request_bytes"] == 3814
    assert out["authorized_main_head"] == (
        "8aa35cc75c4474061ad591622879a0fd857009ff"
    )
    assert out["authorized_main_tree"] == (
        "517dea886ea30467a3c6a4be47e4f2e015743f37"
    )


def test_review_accepts_all_five_fresh_gates_and_preserves_spent_lineage():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_review_contract()
    )

    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True
    assert out["actionable_feedback_v2_activation_authorization_accepted"] is True

    assert out["prior_v2_attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["prior_v2_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert out["reviewed_operator_source_reuse_only"] is True
    assert out["prior_execution_authorization_reusable"] is False
    assert out["prior_preservation_authorization_reusable"] is False
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["automatic_retry"] is False


@pytest.mark.parametrize(
    "field",
    (
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
        "actionable_feedback_v2_activation_authorization_reusable_after_attempt_claim",
    ),
)
def test_review_performs_no_effect_and_grants_no_follow_on_authority(field):
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorized_launcher():
    out = (
        review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_review_contract()
    )
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_"
        "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2PostExhaustionAuthorizationAcceptanceReviewHold,
        match="AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED",
    ):
        review.execute()
