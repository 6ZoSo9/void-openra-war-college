from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_lineage_operator_generation2
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
        "execution_confirm": operator.EXECUTION_CONFIRM_TOKEN,
        "policy_confirm": operator.POLICY_CONFIRM_TOKEN,
        "order_confirm": operator.ORDER_CONFIRM_TOKEN,
        "repair_confirm": operator.REPAIR_CONFIRM_TOKEN,
    }


def test_contract_is_fresh_lineage_and_inert():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_contract()
    )

    assert out[
        "pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_implemented"
    ] is True
    assert out[
        "pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_reviewed"
    ] is False

    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"

    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0

    assert out[
        "adapter_rejection_evidence_namespace_distinct_from_consumed_input_order"
    ] is True
    assert out["prior_input_order_attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["prior_input_order_attempt_reusable"] is False
    assert out["prior_input_order_authorization_reusable"] is False

    assert out[
        "prior_failed_attempt_preservation_required_before_execution_request"
    ] is True
    assert out["execution_request_created"] is False

    assert out["attempt_consumed"] is False
    assert out["attempt_marker_creation_authorized"] is False
    assert out["runtime_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["game_execution_performed"] is False


def test_fresh_namespace_names_do_not_reuse_consumed_order_names():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_contract()
    )

    assert "adapter-rejection" in out["adapter_rejection_runs_root"]
    assert "adapter-rejection" in out["adapter_rejection_marker_name"]
    assert "adapter-rejection" in out["adapter_rejection_result_name"]
    assert "adapter-rejection" in out["adapter_rejection_closeout_name"]

    assert out["adapter_rejection_marker_name"] != (
        "pair06-v9-strict-visible-contact-input-order-coherence-"
        "baseline-game-attempt-v1.json"
    )


def test_four_explicit_authorizations_and_distinct_tokens_are_required():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_contract()
    )

    assert out["explicit_execution_authorization_boolean_required"] is True
    assert out["explicit_policy_activation_authorization_boolean_required"] is True
    assert out[
        "explicit_order_coherence_activation_authorization_boolean_required"
    ] is True
    assert out["explicit_repair_activation_authorization_boolean_required"] is True

    assert out["explicit_execution_confirmation_token_required"] is True
    assert out["explicit_policy_confirmation_token_required"] is True
    assert out["explicit_order_coherence_confirmation_token_required"] is True
    assert out["explicit_repair_confirmation_token_required"] is True
    assert out["all_confirmation_tokens_distinct"] is True

    assert len(
        {
            operator.EXECUTION_CONFIRM_TOKEN,
            operator.POLICY_CONFIRM_TOKEN,
            operator.ORDER_CONFIRM_TOKEN,
            operator.REPAIR_CONFIRM_TOKEN,
        }
    ) == 4


def test_repair_authorization_is_rejected_before_dependency_or_host_work():
    kwargs = _call_kwargs()
    kwargs["repair_activation_authorization_accepted"] = False

    with pytest.raises(
        operator.Pair06V9InputOrderAdapterRejectionFreshLineageOperatorHold,
        match="ADAPTER_REJECTION_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        operator.execute_pair06_v9_input_order_adapter_rejection_fresh_lineage_baseline_game(
            **kwargs
        )


def test_repair_confirmation_is_rejected_before_dependency_or_host_work():
    kwargs = _call_kwargs()
    kwargs["repair_confirm"] = "wrong"

    with pytest.raises(
        operator.Pair06V9InputOrderAdapterRejectionFreshLineageOperatorHold,
        match="ADAPTER_REJECTION_CONFIRMATION_REQUIRED",
    ):
        operator.execute_pair06_v9_input_order_adapter_rejection_fresh_lineage_baseline_game(
            **kwargs
        )


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
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
        "execution_request_created",
    ),
)
def test_contract_grants_no_authority(field):
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_contract()
    )
    assert out[field] is False


def test_contract_advances_only_to_source_binding_review():
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FRESH_LINEAGE_OPERATOR_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_preserve_review_or_request_holds():
    with pytest.raises(
        operator.Pair06V9InputOrderAdapterRejectionFreshLineageOperatorHold,
        match="ADAPTER_REJECTION_FRESH_LINEAGE_OPERATOR_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        operator.preserve_review_or_request()
