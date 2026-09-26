from __future__ import annotations

from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as legacy,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as spent_combat,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)


def _call_kwargs() -> dict:
    return {
        "expected_main_head": "a" * 40,
        "expected_invocation_source_sha256": "b" * 64,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "execution_confirm": invocation.EXECUTION_CONFIRM_TOKEN,
        "policy_confirm": invocation.POLICY_CONFIRM_TOKEN,
    }


def test_contract_binds_coherent_parent_and_preclaim_gpu_lineage():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    assert out["parent_wiring_review_main_head"] == (
        "cee72ef93d919022ef2af837627f7c843742cb58"
    )
    assert out["parent_wiring_review_git_blob"] == (
        "bb619f70732a5cb476a34b0429ce9041bc3d3598"
    )
    assert out["parent_wiring_review_source_sha256"] == (
        "cf85f48f9aac4388de5345043ef51bb0ca210ba76b32150f165744a3b956b591"
    )
    assert out["base_preclaim_gpu_review_git_blob"] == (
        "77dbac309565beb804ac1c2936799574efe5de82"
    )
    assert out["base_preclaim_gpu_review_source_sha256"] == (
        "beec87bea767fdb0c13c14ed7072d49b8fb18db08f6745c22172931ce8843cce"
    )


def test_coherent_evidence_namespace_is_fresh_against_both_prior_lanes():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    assert invocation.MARKER_NAME != legacy.MARKER_NAME
    assert invocation.RESULT_NAME != legacy.RESULT_NAME
    assert invocation.CLOSEOUT_NAME != legacy.CLOSEOUT_NAME
    assert invocation.RUNS_ROOT != Path(legacy.RUNS_ROOT)

    assert invocation.MARKER_NAME != spent_combat.MARKER_NAME
    assert invocation.RESULT_NAME != spent_combat.RESULT_NAME
    assert invocation.CLOSEOUT_NAME != spent_combat.CLOSEOUT_NAME
    assert invocation.RUNS_ROOT != Path(spent_combat.RUNS_ROOT)

    assert out["combat_priority_marker_namespace_distinct_from_legacy"] is True
    assert out["combat_priority_result_namespace_distinct_from_legacy"] is True
    assert out["combat_priority_closeout_namespace_distinct_from_legacy"] is True
    assert out["combat_priority_runs_root_distinct_from_legacy"] is True
    assert out[
        "coherent_marker_namespace_distinct_from_spent_combat_priority"
    ] is True
    assert out[
        "coherent_result_namespace_distinct_from_spent_combat_priority"
    ] is True
    assert out[
        "coherent_closeout_namespace_distinct_from_spent_combat_priority"
    ] is True
    assert out[
        "coherent_runs_root_distinct_from_spent_combat_priority"
    ] is True


def test_contract_seals_consumed_attempt_and_prior_authorization():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    assert out["consumed_combat_priority_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_combat_priority_attempt_reusable"] is False
    assert out["failed_combat_priority_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert out["failed_combat_priority_run_reusable_as_authority"] is False
    assert out["prior_authorization_reusable"] is False
    assert out["fresh_evidence_namespace_required"] is True
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True


def test_contract_preserves_strong_preclaim_gpu_and_one_attempt_envelope():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    assert out["fresh_preclaim_gpu_observation_implemented"] is True
    assert out["fresh_preclaim_gpu_admission_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["durable_create_only_attempt_marker_implemented"] is True
    assert out["attempt_marker_precedes_model_load_and_child_spawn"] is True
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["reviewed_combat_priority_coherent_parent_wiring_used"] is True


def test_execution_authorization_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["execution_authorization_accepted"] = False
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentInvocationHold,
        match="EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_coherent_baseline_game(
            **kwargs
        )


def test_policy_activation_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["policy_activation_authorization_accepted"] = False
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentInvocationHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_coherent_baseline_game(
            **kwargs
        )


def test_execution_confirmation_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["execution_confirm"] = "WRONG"
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentInvocationHold,
        match="EXECUTION_CONFIRMATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_coherent_baseline_game(
            **kwargs
        )


def test_policy_confirmation_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["policy_confirm"] = "WRONG"
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentInvocationHold,
        match="POLICY_CONFIRMATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_coherent_baseline_game(
            **kwargs
        )


def test_contract_grants_no_attempt_marker_or_runtime_authority():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
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
        "host_io_performed_by_contract_inspection",
    ):
        assert out[field] is False


def test_contract_requires_two_distinct_fresh_confirmations():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    assert out["explicit_execution_authorization_boolean_required"] is True
    assert out["explicit_policy_activation_authorization_boolean_required"] is True
    assert out["explicit_execution_confirmation_token_required"] is True
    assert out["explicit_policy_confirmation_token_required"] is True
    assert out["execution_and_policy_confirmation_tokens_distinct"] is True
    assert invocation.EXECUTION_CONFIRM_TOKEN != invocation.POLICY_CONFIRM_TOKEN
    assert invocation.EXECUTION_CONFIRM_TOKEN != spent_combat.EXECUTION_CONFIRM_TOKEN
    assert invocation.POLICY_CONFIRM_TOKEN != spent_combat.POLICY_CONFIRM_TOKEN


def test_invocation_advances_only_to_source_binding_review():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentInvocationHold,
        match="REPAIR_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        invocation.authorize_or_execute()
