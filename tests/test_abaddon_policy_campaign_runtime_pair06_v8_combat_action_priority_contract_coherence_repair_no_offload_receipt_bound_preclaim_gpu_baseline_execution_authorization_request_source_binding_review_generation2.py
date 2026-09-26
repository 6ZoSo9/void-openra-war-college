from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_request_source_test_and_bytes():
    out = review.pair06_v8_combat_priority_coherent_request_review_contract()
    assert out["request_main_head"] == (
        "a481eba482d9077a457a1a2c9fc3dca744c49885"
    )
    assert out["request_git_blob"] == (
        "77e18883acc4c9035591100657012c97f44a92b8"
    )
    assert out["request_source_sha256"] == (
        "054c85fe9d078afb410d210d29f52362ef60a58f613a7256e2793b5e261b1951"
    )
    assert out["request_test_git_blob"] == (
        "a1539d2f3ada3037a18275d797858936b2c36d17"
    )
    assert out["request_test_sha256"] == (
        "42352e775ea97933b3f8e3662c5d53ce1a771e47e1b35ac80d0f4898f00bb699"
    )
    assert out["request_bytes_sha256"] == (
        "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
    )
    assert out["request_byte_length"] == 4998


def test_review_confirms_fresh_one_shot_gpu_scope():
    out = review.pair06_v8_combat_priority_coherent_request_review_contract()
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True


def test_review_seals_consumed_failed_lineage():
    out = review.pair06_v8_combat_priority_coherent_request_review_contract()
    assert out["consumed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert out["failed_run_reusable_as_authority"] is False
    assert out["prior_authorization_reusable"] is False


def test_review_grants_no_authority():
    out = review.pair06_v8_combat_priority_coherent_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    for field in (
        "coherent_execution_authorization_accepted",
        "coherent_policy_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "automatic_retry",
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


def test_review_advances_only_to_fresh_authorization():
    out = review.pair06_v8_combat_priority_coherent_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentRequestReviewHold,
        match="BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
