from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_v2_request_source_tests_and_bytes():
    out = review.pair06_v8_combat_priority_coherent_v2_request_review_contract()
    assert out["request_main_head"] == (
        "b56bcba2830523c4795c3f2a36241cc2692584f5"
    )
    assert out["request_git_blob"] == (
        "a51863da1233b54c92818c418d4412cd55d03538"
    )
    assert out["request_source_sha256"] == (
        "7b83e97af67c00394b872bf9aebb55198a38c728ab371f204f7a8cd1c46e45ae"
    )
    assert out["request_test_git_blob"] == (
        "160eb92af3d6707c5409d6d6938cda9c7fb60921"
    )
    assert out["request_test_sha256"] == (
        "286e0b3673262e66d3dd40b9743106e5970d194e0cd54fa9b32334f5859d6cf9"
    )
    assert out["request_bytes_sha256"] == (
        "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
    )
    assert out["request_byte_length"] == 5670


def test_review_confirms_exact_scope_mapping_and_gpu_boundary():
    out = review.pair06_v8_combat_priority_coherent_v2_request_review_contract()

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
    assert out["maximum_automatic_retries"] == 0

    assert out["v1_production_function_pruning_required"] is True
    assert out["v2_legal_building_reconstruction_required"] is True
    assert out["v2_legal_unit_reconstruction_required"] is True
    assert out["translator_legal_building_mapping_coherence_required"] is True
    assert out["translator_legal_unit_mapping_coherence_required"] is True
    assert out["normal_mode_identity_required"] is True

    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10


def test_review_seals_spent_v1_coherent_lineage():
    out = review.pair06_v8_combat_priority_coherent_v2_request_review_contract()

    assert out["consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["failed_run_preserved"] is True
    assert out["failed_run_reusable_as_authority"] is False
    assert out["prior_request_sha256"] == (
        "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
    )
    assert out["prior_request_reusable"] is False
    assert out["prior_authorization_text_sha256"] == (
        "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
    )
    assert out["prior_authorization_reusable"] is False


def test_review_grants_no_authority():
    out = review.pair06_v8_combat_priority_coherent_v2_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False

    for field in (
        "v2_coherent_execution_authorization_accepted",
        "v2_coherent_policy_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
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


def test_review_advances_only_to_explicit_fresh_authorization():
    out = review.pair06_v8_combat_priority_coherent_v2_request_review_contract()
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentV2RequestReviewHold,
        match="BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
