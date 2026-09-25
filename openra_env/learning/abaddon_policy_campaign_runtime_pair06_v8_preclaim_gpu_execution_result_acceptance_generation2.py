"""Source-only acceptance of the successful GPU-gated pair-06 V8 execution.

Binds the exact terminal emitted by the authorized one-shot Precision run.
This record performs no host I/O, retry, attempt claim, model load, inference,
game execution, training, promotion, deployment, VOID-chain mutation, or
wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_authorization_acceptance_generation2
    as authorization,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_result_source_binding_review_generation2
    as preservation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-preclaim-gpu-execution-result-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
)
AUTHORIZED_MAIN_HEAD = "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"

ATTEMPT_MARKER_SHA256 = (
    "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
)
RESULT_FILE_SHA256 = (
    "f1a3a1ffec2957b984212e5c11067a477934a1c484020dcb2e6398764a117440"
)
CLOSEOUT_FILE_SHA256 = (
    "f0227597d44ecfc5ae07fdc473a2ca9bda71085fba9970279dedf31d5ac24920"
)

RUN_ID = "warmstart-apollyon-vs-abaddon-20260925T070348Z-feinter-s208354846"
WARM_START_SHA256 = (
    "8ce4205d4d61a36a7aab503f5ff1b298020d564e08ab6e9e2302cd5623f679f8"
)
TRAJECTORY_SHA256 = (
    "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
)
SUMMARY_SHA256 = (
    "ae9692fbddd48fb95b9ee1d4737b1ad6ed1aae3ddb2eff80c45a7efde548b6f8"
)

PRECLAIM_GPU_FREE_MEMORY_BYTES = 11647582208
PRECLAIM_GPU_TOTAL_MEMORY_BYTES = 12820938752
PRECLAIM_GPU_COMPUTE_PROCESS_COUNT = 0
MODEL_INFERENCE_COUNT = 36

NEXT_GATE = (
    "PAIR06_V8_PRECLAIM_GPU_EXECUTION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_preclaim_gpu_execution_result_review"
)


class Pair06V8PreclaimGpuExecutionResultAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuExecutionResultAcceptanceHold(message)


def _validate_dependencies() -> dict[str, Any]:
    auth = (
        authorization
        .pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    )
    preserved = (
        preservation_review
        .pair06_v8_third_preservation_result_review_contract()
    )

    _require(auth.get("authorization_accepted") is True, "authorization missing")
    _require(
        auth.get("authorized_request_sha256") == AUTHORIZED_REQUEST_SHA256,
        "authorized request drift",
    )
    _require(
        auth.get("authorized_main_head") == AUTHORIZED_MAIN_HEAD,
        "authorized main drift",
    )
    _require(
        auth.get("maximum_attempts") == 1
        and auth.get("automatic_retry") is False,
        "authorization cardinality drift",
    )
    _require(
        auth.get("fresh_preclaim_gpu_observation_required") is True
        and auth.get("zero_foreign_cuda0_compute_processes_required") is True
        and auth.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and auth.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "GPU admission policy drift",
    )

    _require(
        preserved.get("pair06_v8_third_preservation_result_reviewed") is True,
        "third preservation result review missing",
    )
    _require(
        preserved.get("fresh_baseline_arm_root_available") is True,
        "fresh baseline root not available",
    )
    _require(
        preserved.get("existing_gpu_gated_authorization_accepted") is True,
        "existing GPU-gated authorization not rebound",
    )
    _require(
        preserved.get("authorized_request_sha256") == AUTHORIZED_REQUEST_SHA256
        and preserved.get("authorized_main_head") == AUTHORIZED_MAIN_HEAD,
        "preservation/authorization binding drift",
    )
    return {
        "authorization": deepcopy(auth),
        "preservation_review": deepcopy(preserved),
    }


def pair06_v8_preclaim_gpu_execution_result_acceptance_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_preclaim_gpu_execution_result_accepted": True,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "round_limit": 36,
        "ticks_per_round": 25,
        "run_id": RUN_ID,
        "outcome": "DRAW_OR_UNFINISHED",
        "rounds_completed": 36,
        "final_tick": 3551,
        "attempt_consumed": True,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "result_file_sha256": RESULT_FILE_SHA256,
        "closeout_file_sha256": CLOSEOUT_FILE_SHA256,
        "warm_start_sha256": WARM_START_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "preclaim_gpu_free_memory_bytes": PRECLAIM_GPU_FREE_MEMORY_BYTES,
        "preclaim_gpu_total_memory_bytes": PRECLAIM_GPU_TOTAL_MEMORY_BYTES,
        "preclaim_gpu_compute_process_count": PRECLAIM_GPU_COMPUTE_PROCESS_COUNT,
        "fresh_preclaim_gpu_admitted": True,
        "model_inference_count": MODEL_INFERENCE_COUNT,
        "child_retirement_terminal": "natural_exit",
        "execution_result_green": True,
        "post_run_frozen_worktrees_green": True,
        "session_destroyed": True,
        "engine_container_removed": True,
        "warm_start_spar_cleanup_complete": True,
        "actual_apollyon_vs_actual_abaddon": True,
        "controller_rows_joint_same_tick": True,
        "warm_start_rows_excluded_from_agent_training": True,
        "runtime_output_candidate_only": True,
        "automatic_corpus_admission": False,
        "candidate_execution_performed": False,
        "held_out_execution_performed": False,
        "automatic_retry_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "authorization_reusable_after_attempt_claim": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_promote(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuExecutionResultAcceptanceHold(NEXT_GATE)
