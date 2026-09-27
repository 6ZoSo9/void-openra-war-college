from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_v2_invocation_source_and_tests():
    out = review.pair06_v8_combat_priority_coherent_v2_invocation_review_contract()
    assert out["invocation_main_head"] == (
        "6f21cb30d46016f8e6bd362f6bb8d996ff0215cc"
    )
    assert out["invocation_git_blob"] == (
        "9b5db375d5ae8e133de73603ffd3745352789018"
    )
    assert out["invocation_source_sha256"] == (
        "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
    )
    assert out["invocation_test_git_blob"] == (
        "bb32d3e436ea40c2c36f46d369533a3e5e9c7d52"
    )
    assert out["invocation_test_sha256"] == (
        "4a9f369155c7808d8df67ecdbbd6271e39fe404e24260e998ebd8d273584c0bf"
    )


def test_review_confirms_v2_mapping_coherence_and_fresh_one_shot_envelope():
    out = review.pair06_v8_combat_priority_coherent_v2_invocation_review_contract()
    assert out["v1_production_function_pruning_required"] is True
    assert out["v2_legal_building_reconstruction_required"] is True
    assert out["v2_legal_unit_reconstruction_required"] is True
    assert out["translator_legal_building_mapping_coherence_required"] is True
    assert out["translator_legal_unit_mapping_coherence_required"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_evidence_namespace_required"] is True


def test_review_seals_consumed_v1_coherent_attempt_and_prior_authorization():
    out = review.pair06_v8_combat_priority_coherent_v2_invocation_review_contract()
    assert out["consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["failed_run_reusable_as_authority"] is False
    assert out["failed_run_preserved"] is True
    assert out["prior_authorization_reusable"] is False
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True


def test_review_grants_no_attempt_or_runtime_authority():
    out = review.pair06_v8_combat_priority_coherent_v2_invocation_review_contract()
    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_fresh_v2_authorization_request():
    out = review.pair06_v8_combat_priority_coherent_v2_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentV2InvocationReviewHold,
        match="BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_authorization_or_execute()
