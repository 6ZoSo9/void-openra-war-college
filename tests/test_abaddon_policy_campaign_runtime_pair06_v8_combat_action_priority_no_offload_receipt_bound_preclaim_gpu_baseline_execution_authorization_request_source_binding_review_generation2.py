from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_request_source_tests_and_exact_bytes():
    out = review.pair06_v8_combat_priority_execution_authorization_request_review_contract()
    assert out["request_main_head"] == (
        "4ad1831d4df9154601220b00ba394060756723fb"
    )
    assert out["request_git_blob"] == (
        "bcd8467870c97729a36565167f184f825d082e83"
    )
    assert out["request_source_sha256"] == (
        "e2325e74db689962ada7b97e7cba02e95988524568f9c726e3f2e157475a3a03"
    )
    assert out["request_test_git_blob"] == (
        "62cc0a0b5238696e36690a699d19c833eb003f6c"
    )
    assert out["request_test_sha256"] == (
        "fd470854d39afbdfdecfd154a8553e8262faa238c86fe2e87c65b503e4b58950"
    )
    assert out["request_bytes_sha256"] == (
        "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
    )
    assert out["request_byte_length"] == 5098


def test_review_confirms_one_shot_gpu_scope():
    out = review.pair06_v8_combat_priority_execution_authorization_request_review_contract()
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10


def test_review_requires_separate_execution_and_policy_authority():
    out = review.pair06_v8_combat_priority_execution_authorization_request_review_contract()
    assert out["separate_execution_authorization_required"] is True
    assert out["separate_policy_activation_authorization_required"] is True
    assert out["matching_request_digest_grants_authority"] is False


def test_review_grants_no_attempt_or_runtime_authority():
    out = review.pair06_v8_combat_priority_execution_authorization_request_review_contract()
    for field in (
        "combat_priority_execution_authorization_accepted",
        "combat_priority_policy_activation_authorization_accepted",
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


def test_review_advances_only_to_explicit_authorization():
    out = review.pair06_v8_combat_priority_execution_authorization_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityRequestReviewHold,
        match="BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
