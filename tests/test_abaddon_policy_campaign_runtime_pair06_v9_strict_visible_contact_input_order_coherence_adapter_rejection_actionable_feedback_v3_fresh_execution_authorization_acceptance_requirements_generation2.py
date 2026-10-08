from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_fresh_execution_authorization_acceptance_requirements_generation2
    as requirements,
)


def test_requirements_bind_exact_reviewed_request_and_scope():
    out = requirements.pair06_v9_actionable_feedback_v3_fresh_execution_acceptance_requirements_contract()
    assert out["request_review_git_blob"] == requirements.REQUEST_REVIEW_GIT_BLOB
    assert out["acceptance_requirements_implemented"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["intervention_id"] == (
        "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v3"
    )
    assert out["reviewed_request_sha256"]
    assert out["reviewed_request_bytes"] > 0


def test_requirements_preserve_lineage_and_one_attempt_safety():
    out = requirements.pair06_v9_actionable_feedback_v3_fresh_execution_acceptance_requirements_contract()
    assert out["prior_attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["preservation_receipt_sha256"] == (
        "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
    )
    assert out["fresh_actionable_feedback_v3_evidence_namespace_required"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0


def test_requirements_demand_exact_user_text_main_and_all_five_gates():
    out = requirements.pair06_v9_actionable_feedback_v3_fresh_execution_acceptance_requirements_contract()
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
        "authorization_must_explicitly_cover_actionable_feedback_v3_activation",
        "five_distinct_confirmation_tokens_required",
    ):
        assert out[field] is True


def test_requirements_refuse_general_or_prior_authorization_reuse():
    out = requirements.pair06_v9_actionable_feedback_v3_fresh_execution_acceptance_requirements_contract()
    assert out["general_source_work_authorization_is_execution_authorization"] is False
    assert out["prior_authorization_text_reusable"] is False
    assert out["preservation_authorization_reusable_as_execution_authority"] is False
    assert out["matching_request_digest_grants_authority"] is False
    assert out["matching_request_bytes_grant_authority"] is False


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v3_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "attempt_created",
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
    out = requirements.pair06_v9_actionable_feedback_v3_fresh_execution_acceptance_requirements_contract()
    assert out[field] is False


def test_requirements_stop_at_explicit_user_authorization():
    out = requirements.pair06_v9_actionable_feedback_v3_fresh_execution_acceptance_requirements_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_FRESH_EXECUTION_"
        "EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_execute_holds():
    with pytest.raises(
        requirements.Pair06V9ActionableFeedbackV3FreshExecutionAcceptanceRequirementsHold,
        match="ACTIONABLE_FEEDBACK_V3_FRESH_EXECUTION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        requirements.accept_or_execute()
