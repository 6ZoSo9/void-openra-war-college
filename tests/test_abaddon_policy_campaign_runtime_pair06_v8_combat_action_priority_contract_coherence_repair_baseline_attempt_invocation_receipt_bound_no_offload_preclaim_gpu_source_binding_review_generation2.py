from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_invocation_source_and_tests():
    out = review.pair06_v8_combat_priority_coherent_invocation_review_contract()
    assert out["invocation_main_head"] == (
        "c16084544dc908707316d84a0fa01a7d48228efa"
    )
    assert out["invocation_git_blob"] == (
        "bdf23aac7e6f51a2c7ca678a1d16c9c351c12ede"
    )
    assert out["invocation_source_sha256"] == (
        "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095"
    )
    assert out["invocation_test_git_blob"] == (
        "056e48c8174c0bc2f3b916209273f7fdd56f3eb2"
    )
    assert out["invocation_test_sha256"] == (
        "6f614411346728a93b7e911a9dd900b05289fd316380c25887f7f3c5772a7839"
    )


def test_review_confirms_fresh_one_shot_gpu_envelope():
    out = review.pair06_v8_combat_priority_coherent_invocation_review_contract()
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_evidence_namespace_required"] is True


def test_review_seals_consumed_attempt_and_prior_authorization():
    out = review.pair06_v8_combat_priority_coherent_invocation_review_contract()
    assert out["consumed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert out["failed_run_reusable_as_authority"] is False
    assert out["prior_authorization_reusable"] is False
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True


def test_review_grants_no_attempt_or_runtime_authority():
    out = review.pair06_v8_combat_priority_coherent_invocation_review_contract()
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


def test_review_advances_only_to_fresh_authorization_request():
    out = review.pair06_v8_combat_priority_coherent_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentInvocationReviewHold,
        match="BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_authorization_or_execute()
