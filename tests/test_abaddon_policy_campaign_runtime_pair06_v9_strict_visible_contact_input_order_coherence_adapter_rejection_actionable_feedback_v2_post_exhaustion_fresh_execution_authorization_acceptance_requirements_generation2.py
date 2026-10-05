from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_acceptance_requirements_generation2
    as requirements,
)


def test_requirements_bind_exact_reviewed_request_and_latest_closed_v2_lineage():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_contract()
    )
    assert out["request_review_git_blob"] == requirements.REQUEST_REVIEW_GIT_BLOB
    assert out["acceptance_requirements_implemented"] is True
    assert isinstance(out["reviewed_request_sha256"], str)
    assert len(out["reviewed_request_sha256"]) == 64
    assert out["reviewed_request_bytes"] > 0
    assert out["prior_v2_attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["prior_v2_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert out["reviewed_operator_source_reuse_only"] is True
    assert out["prior_execution_authorization_reusable"] is False
    assert out["prior_preservation_authorization_reusable"] is False


def test_requirements_keep_one_attempt_zero_retry():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_contract()
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0


def test_requirements_demand_exact_user_text_main_and_five_gates():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_contract()
    )
    for field in (
        "exact_user_authorization_text_required",
        "authorization_text_sha256_binding_required",
        "authorization_text_byte_length_binding_required",
        "canonical_main_head_binding_required",
        "canonical_main_tree_binding_required",
        "canonical_main_must_be_bound_at_authorization_time",
        "authorization_must_reference_exact_reviewed_request",
        "authorization_must_explicitly_cover_execution",
        "authorization_must_explicitly_cover_policy_activation",
        "authorization_must_explicitly_cover_order_coherence_activation",
        "authorization_must_explicitly_cover_repair_activation",
        "authorization_must_explicitly_cover_actionable_feedback_v2_activation",
        "five_distinct_confirmation_tokens_required",
    ):
        assert out[field] is True


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_requirements_accept_no_authority(field):
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_contract()
    )
    assert out[field] is False


def test_requirements_stop_at_explicit_user_authorization():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_FRESH_EXECUTION_"
        "EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )

    with pytest.raises(
        requirements.Pair06V9ActionableFeedbackV2PostExhaustionAcceptanceRequirementsHold,
        match="EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        requirements.accept_or_execute()
