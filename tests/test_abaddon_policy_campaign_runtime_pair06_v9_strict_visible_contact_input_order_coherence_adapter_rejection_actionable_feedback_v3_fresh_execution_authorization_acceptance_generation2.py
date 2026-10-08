from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_fresh_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_user_authorization_and_main_snapshot():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_contract()
    )

    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True
    assert out["actionable_feedback_v3_activation_authorization_accepted"] is True

    assert out["authorization_text_sha256"] == (
        "9fa7ed99b41b74f6ccfc161f8b2b20cc1fc76391b4a806e75583c6b3ee0ae932"
    )
    assert out["authorization_text_bytes"] == 624
    assert acceptance.AUTHORIZATION_TEXT_ENCODING == "UTF-8"
    assert acceptance.AUTHORIZATION_TEXT_ADDED_TRAILING_NEWLINE is False
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
    assert out["canonical_main_bound_at_authorization_time"] is True


def test_acceptance_binds_five_distinct_confirmation_tokens():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_contract()
    )

    assert out["five_distinct_confirmation_tokens_required"] is True
    assert out["execution_confirmation_token"] == "EXECUTION=CONFIRM"
    assert out["policy_confirmation_token"] == "STRICT_CONTACT_POLICY=CONFIRM"
    assert out["order_coherence_confirmation_token"] == (
        "INPUT_ORDER_COHERENCE=CONFIRM"
    )
    assert out["repair_confirmation_token"] == "ADAPTER_REJECTION_REPAIR=CONFIRM"
    assert out["actionable_feedback_v3_confirmation_token"] == (
        "ACTIONABLE_FEEDBACK_V3=CONFIRM"
    )


def test_acceptance_preserves_fresh_namespace_and_one_attempt():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_contract()
    )

    assert out["fresh_actionable_feedback_v3_evidence_namespace_required"] is True
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
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_contract()
    )

    for field in (
        "attempt_marker_creation_authorized_after_fresh_gpu_admission",
        "policy_activation_authorized_after_fresh_gpu_admission",
        "order_coherence_activation_authorized_after_fresh_gpu_admission",
        "repair_activation_authorized_after_fresh_gpu_admission",
        "actionable_feedback_v3_activation_authorized_after_fresh_gpu_admission",
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
        "gpu_admission_failure_must_not_activate_actionable_feedback_v3",
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
        "actionable_feedback_v3_activation_performed_by_this_record",
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
        "actionable_feedback_v3_activation_authorization_reusable_after_attempt_claim",
    ),
)
def test_acceptance_record_performs_no_effect_and_grants_no_follow_on_authority(
    field,
):
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_contract()
    )
    assert out[field] is False


def test_acceptance_advances_only_to_authorized_execution_launcher():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        acceptance.Pair06V9ActionableFeedbackV3FreshExecutionAuthorizationAcceptanceHold,
        match="ACTIONABLE_FEEDBACK_V3_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED",
    ):
        acceptance.execute()
