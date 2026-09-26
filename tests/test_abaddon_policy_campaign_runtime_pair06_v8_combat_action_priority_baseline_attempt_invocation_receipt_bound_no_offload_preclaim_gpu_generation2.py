from __future__ import annotations

from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as legacy,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
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


def test_contract_binds_reviewed_parent_and_preclaim_gpu_lineage():
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()
    assert out["parent_wiring_review_main_head"] == (
        "beda5d24ad1e457d295ca4a28f3b49beba5e3f2f"
    )
    assert out["parent_wiring_review_git_blob"] == (
        "0e39c82eb1ba93ada017f7118da45318fd8ad84e"
    )
    assert out["parent_wiring_review_source_sha256"] == (
        "3a7e605f10670c1c5797706725a0097e8d5cd2a891fe52a899abe75ed7a551ed"
    )
    assert out["base_preclaim_gpu_review_git_blob"] == (
        "77dbac309565beb804ac1c2936799574efe5de82"
    )
    assert out["base_preclaim_gpu_review_source_sha256"] == (
        "beec87bea767fdb0c13c14ed7072d49b8fb18db08f6745c22172931ce8843cce"
    )


def test_combat_priority_evidence_namespace_is_distinct_from_spent_legacy_lane():
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()
    assert invocation.MARKER_NAME != legacy.MARKER_NAME
    assert invocation.RESULT_NAME != legacy.RESULT_NAME
    assert invocation.CLOSEOUT_NAME != legacy.CLOSEOUT_NAME
    assert invocation.RUNS_ROOT != Path(legacy.RUNS_ROOT)
    assert out["combat_priority_marker_namespace_distinct_from_legacy"] is True
    assert out["combat_priority_result_namespace_distinct_from_legacy"] is True
    assert out["combat_priority_closeout_namespace_distinct_from_legacy"] is True
    assert out["combat_priority_runs_root_distinct_from_legacy"] is True


def test_contract_preserves_strong_preclaim_gpu_and_one_attempt_envelope():
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()
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


def test_execution_authorization_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["execution_authorization_accepted"] = False
    with pytest.raises(
        invocation.Pair06V8CombatPriorityInvocationHold,
        match="EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_baseline_game(**kwargs)


def test_policy_activation_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["policy_activation_authorization_accepted"] = False
    with pytest.raises(
        invocation.Pair06V8CombatPriorityInvocationHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_baseline_game(**kwargs)


def test_execution_confirmation_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["execution_confirm"] = "WRONG"
    with pytest.raises(
        invocation.Pair06V8CombatPriorityInvocationHold,
        match="EXECUTION_CONFIRMATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_baseline_game(**kwargs)


def test_policy_confirmation_gate_holds_before_host_io():
    kwargs = _call_kwargs()
    kwargs["policy_confirm"] = "WRONG"
    with pytest.raises(
        invocation.Pair06V8CombatPriorityInvocationHold,
        match="POLICY_CONFIRMATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_baseline_game(**kwargs)


def test_contract_grants_no_attempt_marker_or_runtime_authority():
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()
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


def test_contract_requires_two_distinct_explicit_confirmations():
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()
    assert out["explicit_execution_authorization_boolean_required"] is True
    assert out["explicit_policy_activation_authorization_boolean_required"] is True
    assert out["explicit_execution_confirmation_token_required"] is True
    assert out["explicit_policy_confirmation_token_required"] is True
    assert out["execution_and_policy_confirmation_tokens_distinct"] is True
    assert invocation.EXECUTION_CONFIRM_TOKEN != invocation.POLICY_CONFIRM_TOKEN


def test_invocation_advances_only_to_source_binding_review():
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        invocation.Pair06V8CombatPriorityInvocationHold,
        match="PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        invocation.authorize_or_execute()
