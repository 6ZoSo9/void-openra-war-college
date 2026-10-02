from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_user_authorization_and_main_snapshot():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract()
    )

    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True

    assert out["authorization_text_sha256"] == (
        "2364e9c7c7e9e11d9dcdacbe68722b202eb0d5790b5d54cac6b92a995fcb94e8"
    )
    assert out["authorization_text_bytes"] == 286
    assert out["authorized_main_head"] == (
        "e61d66b64eccc4f52a6a951e68a3df7cdf75ce0b"
    )
    assert out["authorized_main_tree"] == (
        "27f5520c3a4018a66d6cf180f80d35ef655647fe"
    )
    assert out["canonical_main_bound_at_authorization_time"] is True


def test_acceptance_preserves_fresh_namespace_and_one_attempt():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract()
    )

    assert out["fresh_adapter_rejection_evidence_namespace_required"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["automatic_retry"] is False

    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10


def test_authorization_effects_are_gated_after_fresh_gpu_admission():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract()
    )

    for field in (
        "attempt_marker_creation_authorized_after_fresh_gpu_admission",
        "policy_activation_authorized_after_fresh_gpu_admission",
        "order_coherence_activation_authorized_after_fresh_gpu_admission",
        "repair_activation_authorized_after_fresh_gpu_admission",
        "runtime_load_authorized_after_fresh_gpu_admission",
        "model_inference_authorized_after_fresh_gpu_admission",
        "game_execution_authorized_after_fresh_gpu_admission",
    ):
        assert out[field] is True

    for field in (
        "gpu_admission_failure_must_not_create_attempt_marker",
        "gpu_admission_failure_must_not_activate_policy",
        "gpu_admission_failure_must_not_activate_order_coherence",
        "gpu_admission_failure_must_not_activate_repair",
        "gpu_admission_failure_must_not_load_model",
        "gpu_admission_failure_must_not_execute_inference",
        "gpu_admission_failure_must_not_execute_game",
    ):
        assert out[field] is True


@pytest.mark.parametrize(
    "field",
    (
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "order_coherence_activation_performed_by_this_record",
        "repair_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "execution_authorization_reusable_after_attempt_claim",
        "policy_activation_authorization_reusable_after_attempt_claim",
        "order_coherence_activation_authorization_reusable_after_attempt_claim",
        "repair_activation_authorization_reusable_after_attempt_claim",
    ),
)
def test_acceptance_record_performs_no_effect_and_grants_no_follow_on_authority(field):
    out = (
        acceptance
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract()
    )
    assert out[field] is False


def test_acceptance_advances_only_to_authorized_execution_launcher():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        acceptance.Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceHold,
        match="ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED",
    ):
        acceptance.execute()
