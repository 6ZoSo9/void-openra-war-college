from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_authorization_binds_exact_request_main_and_text():
    out = acceptance.pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    assert out["authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
    )
    assert out["authorized_request_bytes"] == 4785
    assert out["authorized_main_head"] == (
        "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
    )
    assert out["authorization_text_sha256"] == (
        "3cdbfa07fcc1fa14ab0ce01a7e5456b1bf16583ceda5baee16a0191e8a3cf011"
    )
    assert out["authorization_text_bytes"] == 1127


def test_authorization_binds_reviewed_request_and_invocation():
    out = acceptance.pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    assert out["request_review_git_blob"] == (
        "03b0d2cd22a9f54dcbad1ac165f1b04c645f3497"
    )
    assert out["request_review_source_sha256"] == (
        "61a77ac4fb302004802daa4047f686d0f70282c412dfb1738d21916f16cac3e5"
    )
    assert out["invocation_review_git_blob"] == (
        "77dbac309565beb804ac1c2936799574efe5de82"
    )
    assert out["invocation_source_sha256"] == (
        "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386"
    )


def test_authorization_is_one_fresh_gpu_gated_attempt_only():
    out = acceptance.pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["receipt_bound_preclaim_gpu_execution_authorized"] is True
    assert out["attempt_marker_creation_authorized_after_fresh_gpu_admission"] is True
    assert out["runtime_load_authorized_after_fresh_gpu_admission"] is True
    assert out["model_inference_authorized_after_fresh_gpu_admission"] is True
    assert out["game_execution_authorized_after_fresh_gpu_admission"] is True


def test_gpu_hold_must_remain_preclaim_and_nonexecuting():
    out = acceptance.pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    assert out["gpu_admission_failure_must_not_create_attempt_marker"] is True
    assert out["gpu_admission_failure_must_not_load_model"] is True
    assert out["gpu_admission_failure_must_not_execute_inference"] is True
    assert out["gpu_admission_failure_must_not_execute_game"] is True
    assert out["historical_clean_gpu_observation_reusable"] is False


def test_spent_lineage_and_exclusions_remain_closed():
    out = acceptance.pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    assert out["spent_receipt_bound_request_reusable"] is False
    assert out["spent_oom_attempt_reusable"] is False
    for field in (
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
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
        "authorization_reusable_after_attempt_claim",
    ):
        assert out[field] is False


def test_execution_entrypoint_holds_at_authorized_gate():
    with pytest.raises(
        acceptance.Pair06V8PreclaimGpuAuthorizationAcceptanceHold,
        match="PAIR06_V8_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED",
    ):
        acceptance.execute()
