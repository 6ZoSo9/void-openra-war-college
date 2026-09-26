from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_invocation_source_and_tests():
    out = review.pair06_v8_combat_priority_baseline_attempt_invocation_review_contract()
    assert out["invocation_main_head"] == (
        "589c83fbb2b9ef59c99a23e2830a252f78751186"
    )
    assert out["invocation_git_blob"] == (
        "b8a4c21703dad31e0b6b9768e7e4ba6ae1084abb"
    )
    assert out["invocation_source_sha256"] == (
        "db383a1a833599d2b444dc4a07d6d1c08ef75e6e5c5dc6fd50cbe173ce5e39dd"
    )
    assert out["invocation_test_git_blob"] == (
        "568548907f9b434d5d4ca45a2b01e3af9ea17a23"
    )
    assert out["invocation_test_sha256"] == (
        "b2be3d7a8da30708e70ae1b5611e04ed1a6ed8e4ffb900549c6ebee55decc9e5"
    )


def test_review_confirms_strong_one_shot_gpu_envelope():
    out = review.pair06_v8_combat_priority_baseline_attempt_invocation_review_contract()
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out[
        "combat_priority_evidence_namespace_distinct_from_spent_baseline"
    ] is True


def test_review_requires_separate_execution_and_policy_authority():
    out = review.pair06_v8_combat_priority_baseline_attempt_invocation_review_contract()
    assert out["explicit_execution_authorization_required"] is True
    assert out["explicit_policy_activation_authorization_required"] is True
    assert out[
        "distinct_execution_and_policy_confirmations_required"
    ] is True


def test_review_grants_no_attempt_or_runtime_authority():
    out = review.pair06_v8_combat_priority_baseline_attempt_invocation_review_contract()
    for field in (
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


def test_review_advances_only_to_authorization_request():
    out = review.pair06_v8_combat_priority_baseline_attempt_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityInvocationReviewHold,
        match="BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_or_execute()
