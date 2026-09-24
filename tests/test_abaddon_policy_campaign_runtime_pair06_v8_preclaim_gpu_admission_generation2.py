from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_admission_generation2
    as admission,
)


GIB = 1024**3


def clean_observation():
    return {
        "schema": admission.OBSERVATION_SCHEMA,
        "pair_slot": 6,
        "gpu_index": 0,
        "total_memory_bytes": 12 * GIB,
        "free_memory_bytes": 11 * GIB,
        "compute_processes": [],
        "observation_read_only": True,
        "attempt_marker_created": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def test_clean_idle_gpu_is_preclaim_admissible_only():
    out = admission.evaluate_pair06_v8_preclaim_gpu_observation(
        clean_observation()
    )
    assert out["preclaim_gpu_admitted"] is True
    assert out["foreign_compute_process_count"] == 0
    assert out["free_memory_bytes"] == 11 * GIB
    assert out["execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_foreign_compute_process_fails_closed_before_claim():
    evidence = clean_observation()
    evidence["free_memory_bytes"] = admission.PRIOR_PRECLAIM_FREE_MEMORY_BYTES
    evidence["compute_processes"] = [
        {
            "pid": admission.PRIOR_FOREIGN_COMPUTE_PID,
            "used_memory_bytes": 5 * GIB,
        }
    ]
    with pytest.raises(
        admission.Pair06V8PreclaimGpuAdmissionHold,
        match="FOREIGN_COMPUTE_PROCESS_HOLD",
    ):
        admission.evaluate_pair06_v8_preclaim_gpu_observation(evidence)


def test_less_than_ninety_percent_free_fails_closed():
    evidence = clean_observation()
    evidence["free_memory_bytes"] = (12 * GIB * 89) // 100
    with pytest.raises(
        admission.Pair06V8PreclaimGpuAdmissionHold,
        match="FREE_FRACTION_HOLD",
    ):
        admission.evaluate_pair06_v8_preclaim_gpu_observation(evidence)


@pytest.mark.parametrize(
    "field",
    [
        "attempt_marker_created",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    ],
)
def test_observation_must_be_strictly_preclaim(field):
    evidence = clean_observation()
    evidence[field] = True
    with pytest.raises(
        admission.Pair06V8PreclaimGpuAdmissionHold,
        match="TOO_LATE_HOLD",
    ):
        admission.evaluate_pair06_v8_preclaim_gpu_observation(evidence)


def test_contract_binds_consumed_oom_without_granting_retry():
    out = admission.pair06_v8_preclaim_gpu_admission_contract()
    assert out["prior_consumed_attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["prior_preclaim_free_memory_bytes"] == 5756354560
    assert out["prior_foreign_compute_pid"] == 2850305
    assert out["prior_failure_type"] == "OutOfMemoryError"
    assert out["prior_failure_stage"] == "transformers.caching_allocator_warmup"
    assert out["prior_attempt_reusable"] is False
    assert out["retry_authorized"] is False


def test_contract_preserves_all_execution_and_mutation_boundaries():
    out = admission.pair06_v8_preclaim_gpu_admission_contract()
    for field in (
        "execution_authorized",
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
    assert out["host_io_performed_by_contract_inspection"] is False


def test_contract_advances_only_to_source_binding_review():
    out = admission.pair06_v8_preclaim_gpu_admission_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECLAIM_GPU_ADMISSION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECLAIM_GPU_ADMISSION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_runtime_entrypoint_holds():
    with pytest.raises(
        admission.Pair06V8PreclaimGpuAdmissionHold,
        match="PAIR06_V8_PRECLAIM_GPU_ADMISSION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        admission.observe_or_execute()
