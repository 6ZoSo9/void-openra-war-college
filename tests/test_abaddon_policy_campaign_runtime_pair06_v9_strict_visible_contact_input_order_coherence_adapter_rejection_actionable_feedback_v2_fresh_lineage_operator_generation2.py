from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_generation2
    as operator,
)


def _call_kwargs() -> dict:
    return {
        "expected_main_head": "a" * 40,
        "expected_operator_source_sha256": "b" * 64,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "actionable_feedback_v2_activation_authorization_accepted": True,
        "execution_confirm": operator.EXECUTION_CONFIRM_TOKEN,
        "policy_confirm": operator.POLICY_CONFIRM_TOKEN,
        "order_confirm": operator.ORDER_CONFIRM_TOKEN,
        "repair_confirm": operator.REPAIR_CONFIRM_TOKEN,
        "feedback_v2_confirm": operator.FEEDBACK_V2_CONFIRM_TOKEN,
    }


def test_contract_is_fresh_v2_lineage_and_inert():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_contract()
    )

    assert out[
        "pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_implemented"
    ] is True
    assert out[
        "pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_reviewed"
    ] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["prior_failed_attempt_preservation_reviewed"] is True
    assert out["prior_failed_attempt_preservation_lineage_closed"] is True
    assert out["execution_request_created"] is False


def test_v2_namespace_does_not_reuse_consumed_adapter_rejection_names():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_contract()
    )
    assert "actionable-feedback-v2" in out["actionable_feedback_v2_runs_root"]
    assert "actionable-feedback-v2" in out["actionable_feedback_v2_marker_name"]
    assert "actionable-feedback-v2" in out["actionable_feedback_v2_result_name"]
    assert "actionable-feedback-v2" in out["actionable_feedback_v2_closeout_name"]
    assert out[
        "actionable_feedback_v2_evidence_namespace_distinct_from_consumed_adapter_rejection"
    ] is True


def test_preserved_failed_attempt_is_bound_non_reusable():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_contract()
    )
    assert out["prior_adapter_rejection_attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["prior_adapter_rejection_attempt_reusable"] is False
    assert out["prior_adapter_rejection_authorization_reusable"] is False
    assert out["prior_adapter_rejection_preservation_receipt_sha256"] == (
        "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
    )


def test_five_explicit_authorizations_and_distinct_tokens_are_required():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_contract()
    )
    for field in (
        "explicit_execution_authorization_boolean_required",
        "explicit_policy_activation_authorization_boolean_required",
        "explicit_order_coherence_activation_authorization_boolean_required",
        "explicit_repair_activation_authorization_boolean_required",
        "explicit_actionable_feedback_v2_activation_authorization_boolean_required",
        "explicit_execution_confirmation_token_required",
        "explicit_policy_confirmation_token_required",
        "explicit_order_coherence_confirmation_token_required",
        "explicit_repair_confirmation_token_required",
        "explicit_actionable_feedback_v2_confirmation_token_required",
    ):
        assert out[field] is True
    assert out["all_confirmation_tokens_distinct"] is True
    assert len(
        {
            operator.EXECUTION_CONFIRM_TOKEN,
            operator.POLICY_CONFIRM_TOKEN,
            operator.ORDER_CONFIRM_TOKEN,
            operator.REPAIR_CONFIRM_TOKEN,
            operator.FEEDBACK_V2_CONFIRM_TOKEN,
        }
    ) == 5


def test_v2_authorization_rejected_before_dependency_or_host_work():
    kwargs = _call_kwargs()
    kwargs["actionable_feedback_v2_activation_authorization_accepted"] = False
    with pytest.raises(
        operator.Pair06V9InputOrderAdapterRejectionActionableFeedbackV2FreshLineageOperatorHold,
        match="ACTIONABLE_FEEDBACK_V2_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        operator.execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_baseline_game(
            **kwargs
        )


def test_v2_confirmation_rejected_before_dependency_or_host_work():
    kwargs = _call_kwargs()
    kwargs["feedback_v2_confirm"] = "wrong"
    with pytest.raises(
        operator.Pair06V9InputOrderAdapterRejectionActionableFeedbackV2FreshLineageOperatorHold,
        match="ACTIONABLE_FEEDBACK_V2_CONFIRMATION_REQUIRED",
    ):
        operator.execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_baseline_game(
            **kwargs
        )


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "execution_request_created",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
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
def test_contract_grants_no_authority(field):
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_contract()
    )
    assert out[field] is False


def test_contract_advances_only_to_source_binding_review():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_LINEAGE_OPERATOR_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_preserve_review_or_request_holds():
    with pytest.raises(
        operator.Pair06V9InputOrderAdapterRejectionActionableFeedbackV2FreshLineageOperatorHold,
        match="ACTIONABLE_FEEDBACK_V2_FRESH_LINEAGE_OPERATOR_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        operator.preserve_review_or_request()
