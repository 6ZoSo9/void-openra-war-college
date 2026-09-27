from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_preclaim_gpu_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_fresh_authorization_and_request():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )
    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
    )
    assert out["authorized_request_bytes"] == 5670
    assert out["authorized_main_head"] == (
        "d8b16f1c23a74803ac4ace94045fed147c3c69fe"
    )
    assert out["authorization_text_sha256"] == (
        "6cfe4dd78c02a55c2499163b01de6f5714e0b8573100b7a888177ff1a568d139"
    )
    assert out["authorization_text_bytes"] == 533


def test_acceptance_pins_exact_merged_request_review_and_invocation():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )
    assert out["request_review_git_blob"] == (
        "18e69f90b4020a775de6bb9f1b7b5346e4e531fd"
    )
    assert out["request_review_source_sha256"] == (
        "5b97f48b1ad6220bd615194b55f74f17865090c251ae08a257906678e754f862"
    )
    assert out["request_review_test_git_blob"] == (
        "1171d47ea8f9990c6bcb7b0419b8edf8f10779c1"
    )
    assert out["request_review_test_sha256"] == (
        "86cceb10e97147bbed2fe3eb900dbc582ad677df56dddaef7e7a2c099cf700ce"
    )
    assert out["invocation_source_sha256"] == (
        "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
    )


def test_acceptance_preserves_exact_scope_and_v2_mapping_coherence():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )
    assert out["policy_id"] == "pair06-v8-combat-action-priority-envelope-v1"
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-qwen35-4b-lora-v1"
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False

    assert out["v1_production_function_pruning_required"] is True
    assert out["v2_legal_building_reconstruction_required"] is True
    assert out["v2_legal_unit_reconstruction_required"] is True
    assert out["translator_legal_building_mapping_coherence_required"] is True
    assert out["translator_legal_unit_mapping_coherence_required"] is True
    assert out["normal_mode_identity_required"] is True


def test_acceptance_requires_fresh_gpu_before_claim_and_execution():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10

    for field in (
        "gpu_admission_failure_must_not_create_attempt_marker",
        "gpu_admission_failure_must_not_activate_policy",
        "gpu_admission_failure_must_not_load_model",
        "gpu_admission_failure_must_not_execute_inference",
        "gpu_admission_failure_must_not_execute_game",
    ):
        assert out[field] is True

    assert out["attempt_marker_creation_authorized_after_fresh_gpu_admission"] is True
    assert out["policy_activation_authorized_after_fresh_gpu_admission"] is True
    assert out["runtime_load_authorized_after_fresh_gpu_admission"] is True
    assert out["model_inference_authorized_after_fresh_gpu_admission"] is True
    assert out["game_execution_authorized_after_fresh_gpu_admission"] is True


def test_acceptance_seals_prior_consumed_lineage():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )
    assert out["prior_consumed_request_sha256"] == (
        "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
    )
    assert out["prior_consumed_request_reusable"] is False
    assert out["prior_consumed_authorization_text_sha256"] == (
        "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
    )
    assert out["prior_consumed_authorization_reusable"] is False
    assert out["prior_consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["prior_consumed_attempt_reusable"] is False
    assert out["prior_consumed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["prior_consumed_run_preserved"] is True
    assert out["prior_consumed_run_reusable_as_authority"] is False


def test_acceptance_record_performs_no_runtime_action_and_excludes_other_lanes():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )

    for field in (
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False

    assert out["execution_authorization_reusable_after_attempt_claim"] is False
    assert out["policy_activation_authorization_reusable_after_attempt_claim"] is False


def test_next_gate_is_authorized_preclaim_execution():
    out = (
        acceptance
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract()
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED"
    )


def test_execute_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8CombatPriorityCoherentV2AuthorizationAcceptanceHold,
        match="RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED",
    ):
        acceptance.execute()
