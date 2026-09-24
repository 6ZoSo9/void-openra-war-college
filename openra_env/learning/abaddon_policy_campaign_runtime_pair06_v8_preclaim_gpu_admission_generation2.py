"""Source-only pre-claim GPU admission for a future pair-06 V8 baseline attempt.

The most recent authorized pair-06 V8 baseline attempt was consumed after
claim and then failed while loading the model because CUDA:0 was already
occupied by another compute process. This contract adds a fail-closed
admission rule for any future invocation generation before it may create a
single-use attempt marker.

This source performs no host I/O. A separately reviewed read-only observer
must supply the GPU snapshot. Passing this contract does not authorize a
retry, create a claim, load a model, run inference, execute a game, train,
promote, deploy, mutate VOID, or move funds.
"""

from __future__ import annotations

from typing import Any, Mapping


OBSERVATION_SCHEMA = (
    "void.abaddon.generation2.pair06-v8-preclaim-gpu-observation.v1"
)
CONTRACT_SCHEMA = (
    "void.abaddon.generation2.pair06-v8-preclaim-gpu-admission-contract.v1"
)
ADMISSION_SCHEMA = (
    "void.abaddon.generation2.pair06-v8-preclaim-gpu-admission.v1"
)

PAIR_SLOT = 6
GPU_INDEX = 0

MIN_FREE_FRACTION_NUMERATOR = 9
MIN_FREE_FRACTION_DENOMINATOR = 10

PRIOR_CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)
PRIOR_PRECLAIM_FREE_MEMORY_BYTES = 5756354560
PRIOR_FOREIGN_COMPUTE_PID = 2850305
PRIOR_FAILURE_TYPE = "OutOfMemoryError"
PRIOR_FAILURE_STAGE = "transformers.caching_allocator_warmup"

NEXT_GATE = "PAIR06_V8_PRECLAIM_GPU_ADMISSION_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_preclaim_gpu_admission_source_binding_review"
)


class Pair06V8PreclaimGpuAdmissionHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuAdmissionHold(message)


def _validate_processes(value: Any) -> list[dict[str, int]]:
    _require(
        type(value) is list,
        "PAIR06_V8_PRECLAIM_GPU_PROCESS_LIST_HOLD",
    )
    normalized: list[dict[str, int]] = []
    seen_pids: set[int] = set()
    for item in value:
        _require(
            isinstance(item, Mapping)
            and set(item) == {"pid", "used_memory_bytes"},
            "PAIR06_V8_PRECLAIM_GPU_PROCESS_SHAPE_HOLD",
        )
        pid = item.get("pid")
        used_memory_bytes = item.get("used_memory_bytes")
        _require(
            type(pid) is int and pid > 0,
            "PAIR06_V8_PRECLAIM_GPU_PROCESS_PID_HOLD",
        )
        _require(
            type(used_memory_bytes) is int and used_memory_bytes >= 0,
            "PAIR06_V8_PRECLAIM_GPU_PROCESS_MEMORY_HOLD",
        )
        _require(
            pid not in seen_pids,
            "PAIR06_V8_PRECLAIM_GPU_PROCESS_DUPLICATE_HOLD",
        )
        seen_pids.add(pid)
        normalized.append(
            {
                "pid": pid,
                "used_memory_bytes": used_memory_bytes,
            }
        )
    return normalized


def evaluate_pair06_v8_preclaim_gpu_observation(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _require(
        isinstance(evidence, Mapping),
        "PAIR06_V8_PRECLAIM_GPU_EVIDENCE_OBJECT_HOLD",
    )
    supplied = dict(evidence)
    expected_fields = {
        "schema",
        "pair_slot",
        "gpu_index",
        "total_memory_bytes",
        "free_memory_bytes",
        "compute_processes",
        "observation_read_only",
        "attempt_marker_created",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    }
    _require(
        set(supplied) == expected_fields,
        "PAIR06_V8_PRECLAIM_GPU_EVIDENCE_FIELD_SET_HOLD",
    )
    _require(
        supplied.get("schema") == OBSERVATION_SCHEMA,
        "PAIR06_V8_PRECLAIM_GPU_SCHEMA_HOLD",
    )
    _require(
        supplied.get("pair_slot") == PAIR_SLOT,
        "PAIR06_V8_PRECLAIM_GPU_PAIR_SCOPE_HOLD",
    )
    _require(
        supplied.get("gpu_index") == GPU_INDEX,
        "PAIR06_V8_PRECLAIM_GPU_INDEX_HOLD",
    )

    total_memory_bytes = supplied.get("total_memory_bytes")
    free_memory_bytes = supplied.get("free_memory_bytes")
    _require(
        type(total_memory_bytes) is int and total_memory_bytes > 0,
        "PAIR06_V8_PRECLAIM_GPU_TOTAL_MEMORY_HOLD",
    )
    _require(
        type(free_memory_bytes) is int
        and 0 <= free_memory_bytes <= total_memory_bytes,
        "PAIR06_V8_PRECLAIM_GPU_FREE_MEMORY_HOLD",
    )

    processes = _validate_processes(supplied.get("compute_processes"))
    _require(
        len(processes) == 0,
        "PAIR06_V8_PRECLAIM_GPU_FOREIGN_COMPUTE_PROCESS_HOLD",
    )
    _require(
        free_memory_bytes * MIN_FREE_FRACTION_DENOMINATOR
        >= total_memory_bytes * MIN_FREE_FRACTION_NUMERATOR,
        "PAIR06_V8_PRECLAIM_GPU_FREE_FRACTION_HOLD",
    )

    _require(
        supplied.get("observation_read_only") is True,
        "PAIR06_V8_PRECLAIM_GPU_OBSERVER_MUTATION_HOLD",
    )
    for field in (
        "attempt_marker_created",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    ):
        _require(
            supplied.get(field) is False,
            "PAIR06_V8_PRECLAIM_GPU_TOO_LATE_HOLD:" + field,
        )

    return {
        "schema": ADMISSION_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "gpu_index": GPU_INDEX,
        "preclaim_gpu_admitted": True,
        "foreign_compute_process_count": 0,
        "total_memory_bytes": total_memory_bytes,
        "free_memory_bytes": free_memory_bytes,
        "required_free_fraction": {
            "numerator": MIN_FREE_FRACTION_NUMERATOR,
            "denominator": MIN_FREE_FRACTION_DENOMINATOR,
        },
        "observation_read_only": True,
        "attempt_marker_created": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "execution_authorized": False,
        "automatic_retry": False,
    }


def pair06_v8_preclaim_gpu_admission_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_preclaim_gpu_admission_implemented": True,
        "pair06_v8_preclaim_gpu_admission_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "gpu_index": GPU_INDEX,
        "foreign_compute_processes_allowed": False,
        "minimum_free_memory_fraction": {
            "numerator": MIN_FREE_FRACTION_NUMERATOR,
            "denominator": MIN_FREE_FRACTION_DENOMINATOR,
        },
        "admission_must_precede_attempt_marker": True,
        "read_only_observer_required": True,
        "prior_consumed_attempt_marker_sha256": (
            PRIOR_CONSUMED_ATTEMPT_MARKER_SHA256
        ),
        "prior_preclaim_free_memory_bytes": PRIOR_PRECLAIM_FREE_MEMORY_BYTES,
        "prior_foreign_compute_pid": PRIOR_FOREIGN_COMPUTE_PID,
        "prior_failure_type": PRIOR_FAILURE_TYPE,
        "prior_failure_stage": PRIOR_FAILURE_STAGE,
        "prior_attempt_reusable": False,
        "retry_authorized": False,
        "execution_authorized": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuAdmissionHold(NEXT_GATE)
