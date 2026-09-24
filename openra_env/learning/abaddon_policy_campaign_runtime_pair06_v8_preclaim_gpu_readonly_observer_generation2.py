"""Read-only CUDA:0 observer for pair-06 V8 pre-claim admission.

This source implements the reviewed observation boundary required by the
pair-06 V8 pre-claim GPU admission contract. It can query only NVIDIA device
memory and compute-process state through exact nvidia-smi argument vectors.

Import and contract inspection perform no host I/O. Observation requires an
explicit boolean before the supplied command runner is called. The bundled
host runner uses no shell and implements no signal, process termination,
service action, model load, inference, game execution, training, promotion,
deployment, VOID mutation, wallet action, or funds movement.

The returned object is the exact observation shape consumed by the separately
reviewed pre-claim GPU admission validator. The observer itself does not grant
admission or execution authority.
"""

from __future__ import annotations

from copy import deepcopy
import subprocess
from typing import Any, Mapping, Protocol, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_admission_generation2
    as admission,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_admission_source_binding_review_generation2
    as admission_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-preclaim-gpu-readonly-observer-contract.v1"
)

ADMISSION_REVIEW_GIT_BLOB = "00876b15ce0317d548b14e98dd5c3a480f11c84f"
ADMISSION_REVIEW_SOURCE_SHA256 = (
    "3991a1bcb2ffe855495cb983c3a4540f947d2079d60c7bf8fd1283b8a6ca06ba"
)

PAIR_SLOT = 6
GPU_INDEX = 0
NVIDIA_SMI = "/usr/bin/nvidia-smi"
DEFAULT_TIMEOUT_SECONDS = 5.0
MAX_STDOUT_BYTES = 65536
MIB = 1024 * 1024

DEVICE_QUERY = (
    NVIDIA_SMI,
    "--query-gpu=index,uuid,memory.total,memory.free",
    "--format=csv,noheader,nounits",
)
PROCESS_QUERY = (
    NVIDIA_SMI,
    "--query-compute-apps=gpu_uuid,pid,used_gpu_memory",
    "--format=csv,noheader,nounits",
)

NEXT_GATE = "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_preclaim_gpu_readonly_observer_source_binding_review"
)


class Pair06V8PreclaimGpuReadonlyObserverHold(ValueError):
    pass


class CommandRunner(Protocol):
    def __call__(
        self,
        argv: Sequence[str],
        *,
        timeout_seconds: float,
        maximum_stdout_bytes: int,
    ) -> Mapping[str, Any]:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuReadonlyObserverHold(message)


def _validated_admission_review() -> dict[str, Any]:
    out = admission_review.pair06_v8_preclaim_gpu_admission_review_contract()
    _require(
        out.get("pair06_v8_preclaim_gpu_admission_reviewed") is True,
        "PAIR06_V8_GPU_OBSERVER_ADMISSION_REVIEW_REQUIRED",
    )
    _require(out.get("pair_slot") == PAIR_SLOT, "PAIR06_V8_GPU_OBSERVER_PAIR_DRIFT")
    _require(out.get("gpu_index") == GPU_INDEX, "PAIR06_V8_GPU_OBSERVER_INDEX_DRIFT")
    _require(
        out.get("foreign_compute_processes_allowed") is False,
        "PAIR06_V8_GPU_OBSERVER_FOREIGN_PROCESS_POLICY_DRIFT",
    )
    _require(
        out.get("minimum_free_memory_fraction")
        == {"numerator": 9, "denominator": 10},
        "PAIR06_V8_GPU_OBSERVER_FREE_FRACTION_POLICY_DRIFT",
    )
    _require(
        out.get("admission_must_precede_attempt_marker") is True
        and out.get("read_only_observer_required") is True,
        "PAIR06_V8_GPU_OBSERVER_ORDERING_POLICY_DRIFT",
    )
    for field in (
        "retry_authorized",
        "execution_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(
            out.get(field) is False,
            "PAIR06_V8_GPU_OBSERVER_AUTHORITY_DRIFT:" + field,
        )
    _require(
        out.get("next_gate") == "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_REQUIRED",
        "PAIR06_V8_GPU_OBSERVER_FRONTIER_DRIFT",
    )
    return deepcopy(out)


def _parse_nonnegative_int(value: str, *, label: str) -> int:
    text = value.strip()
    _require(text.isdigit(), label + "_NOT_INTEGER")
    number = int(text)
    _require(number >= 0, label + "_NEGATIVE")
    return number


def _parse_positive_int(value: str, *, label: str) -> int:
    number = _parse_nonnegative_int(value, label=label)
    _require(number > 0, label + "_NOT_POSITIVE")
    return number


def _validate_runner_result(
    result: Mapping[str, Any],
    *,
    label: str,
    maximum_stdout_bytes: int,
) -> bytes:
    _require(isinstance(result, Mapping), label + "_RESULT_OBJECT_REQUIRED")
    _require(
        set(result) == {"returncode", "stdout", "stderr"},
        label + "_RESULT_FIELD_SET_HOLD",
    )
    _require(result.get("returncode") == 0, label + "_NONZERO_EXIT")
    stdout = result.get("stdout")
    stderr = result.get("stderr")
    _require(type(stdout) is bytes, label + "_STDOUT_BYTES_REQUIRED")
    _require(type(stderr) is bytes, label + "_STDERR_BYTES_REQUIRED")
    _require(len(stdout) <= maximum_stdout_bytes, label + "_STDOUT_LIMIT_HOLD")
    _require(len(stderr) <= maximum_stdout_bytes, label + "_STDERR_LIMIT_HOLD")
    try:
        stdout.decode("utf-8", errors="strict")
        stderr.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise Pair06V8PreclaimGpuReadonlyObserverHold(
            label + "_UTF8_HOLD"
        ) from exc
    return stdout


def _device_row(stdout: bytes) -> dict[str, Any]:
    text = stdout.decode("utf-8")
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    parsed: list[dict[str, Any]] = []
    seen_indexes: set[int] = set()

    for row in rows:
        parts = [part.strip() for part in row.split(",")]
        _require(len(parts) == 4, "PAIR06_V8_GPU_OBSERVER_DEVICE_ROW_SHAPE_HOLD")
        index = _parse_nonnegative_int(
            parts[0],
            label="PAIR06_V8_GPU_OBSERVER_DEVICE_INDEX",
        )
        uuid = parts[1]
        total_mib = _parse_positive_int(
            parts[2],
            label="PAIR06_V8_GPU_OBSERVER_TOTAL_MIB",
        )
        free_mib = _parse_nonnegative_int(
            parts[3],
            label="PAIR06_V8_GPU_OBSERVER_FREE_MIB",
        )
        _require(
            free_mib <= total_mib,
            "PAIR06_V8_GPU_OBSERVER_FREE_EXCEEDS_TOTAL",
        )
        _require(
            index not in seen_indexes,
            "PAIR06_V8_GPU_OBSERVER_DUPLICATE_DEVICE_INDEX",
        )
        _require(
            uuid.startswith("GPU-") and len(uuid) > 4,
            "PAIR06_V8_GPU_OBSERVER_DEVICE_UUID_HOLD",
        )
        seen_indexes.add(index)
        parsed.append(
            {
                "index": index,
                "uuid": uuid,
                "total_memory_bytes": total_mib * MIB,
                "free_memory_bytes": free_mib * MIB,
            }
        )

    matches = [row for row in parsed if row["index"] == GPU_INDEX]
    _require(
        len(matches) == 1,
        "PAIR06_V8_GPU_OBSERVER_EXACT_CUDA0_REQUIRED",
    )
    return matches[0]


def _compute_processes(
    stdout: bytes,
    *,
    gpu_uuid: str,
) -> list[dict[str, int]]:
    text = stdout.decode("utf-8")
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    result: list[dict[str, int]] = []
    seen_pids: set[int] = set()

    for row in rows:
        parts = [part.strip() for part in row.split(",")]
        _require(
            len(parts) == 3,
            "PAIR06_V8_GPU_OBSERVER_PROCESS_ROW_SHAPE_HOLD",
        )
        row_uuid = parts[0]
        _require(
            row_uuid.startswith("GPU-") and len(row_uuid) > 4,
            "PAIR06_V8_GPU_OBSERVER_PROCESS_UUID_HOLD",
        )
        pid = _parse_positive_int(
            parts[1],
            label="PAIR06_V8_GPU_OBSERVER_PROCESS_PID",
        )
        used_mib = _parse_nonnegative_int(
            parts[2],
            label="PAIR06_V8_GPU_OBSERVER_PROCESS_MIB",
        )
        if row_uuid != gpu_uuid:
            continue
        _require(
            pid not in seen_pids,
            "PAIR06_V8_GPU_OBSERVER_DUPLICATE_PROCESS_PID",
        )
        seen_pids.add(pid)
        result.append(
            {
                "pid": pid,
                "used_memory_bytes": used_mib * MIB,
            }
        )

    return result


def host_nvidia_smi_readonly_runner(
    argv: Sequence[str],
    *,
    timeout_seconds: float,
    maximum_stdout_bytes: int,
) -> Mapping[str, Any]:
    """Run only one of the two reviewed nvidia-smi read-only queries."""

    exact = tuple(argv)
    _require(
        exact in (DEVICE_QUERY, PROCESS_QUERY),
        "PAIR06_V8_GPU_OBSERVER_COMMAND_NOT_REVIEWED",
    )
    _require(
        0.0 < timeout_seconds <= DEFAULT_TIMEOUT_SECONDS,
        "PAIR06_V8_GPU_OBSERVER_TIMEOUT_BOUND_HOLD",
    )
    _require(
        0 < maximum_stdout_bytes <= MAX_STDOUT_BYTES,
        "PAIR06_V8_GPU_OBSERVER_STDOUT_BOUND_HOLD",
    )

    try:
        completed = subprocess.run(
            exact,
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            shell=False,
            env={
                "PATH": "/usr/bin:/bin",
                "LC_ALL": "C",
                "LANG": "C",
            },
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise Pair06V8PreclaimGpuReadonlyObserverHold(
            "PAIR06_V8_GPU_OBSERVER_NVIDIA_SMI_EXECUTION_HOLD"
        ) from exc

    stdout = bytes(completed.stdout)
    stderr = bytes(completed.stderr)
    _require(
        len(stdout) <= maximum_stdout_bytes,
        "PAIR06_V8_GPU_OBSERVER_HOST_STDOUT_LIMIT_HOLD",
    )
    _require(
        len(stderr) <= maximum_stdout_bytes,
        "PAIR06_V8_GPU_OBSERVER_HOST_STDERR_LIMIT_HOLD",
    )
    return {
        "returncode": completed.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }


def observe_pair06_v8_preclaim_gpu_readonly(
    *,
    observation_authorized: bool,
    command_runner: CommandRunner,
) -> dict[str, Any]:
    """Observe CUDA:0 memory/process state without admitting or executing."""

    _require(
        observation_authorized is True,
        "PAIR06_V8_GPU_OBSERVER_OBSERVATION_NOT_AUTHORIZED",
    )
    _require(
        callable(command_runner),
        "PAIR06_V8_GPU_OBSERVER_COMMAND_RUNNER_REQUIRED",
    )
    _validated_admission_review()

    device_raw = command_runner(
        DEVICE_QUERY,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        maximum_stdout_bytes=MAX_STDOUT_BYTES,
    )
    device_stdout = _validate_runner_result(
        device_raw,
        label="PAIR06_V8_GPU_OBSERVER_DEVICE_QUERY",
        maximum_stdout_bytes=MAX_STDOUT_BYTES,
    )
    device = _device_row(device_stdout)

    process_raw = command_runner(
        PROCESS_QUERY,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        maximum_stdout_bytes=MAX_STDOUT_BYTES,
    )
    process_stdout = _validate_runner_result(
        process_raw,
        label="PAIR06_V8_GPU_OBSERVER_PROCESS_QUERY",
        maximum_stdout_bytes=MAX_STDOUT_BYTES,
    )
    processes = _compute_processes(
        process_stdout,
        gpu_uuid=device["uuid"],
    )

    return {
        "schema": admission.OBSERVATION_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "gpu_index": GPU_INDEX,
        "total_memory_bytes": device["total_memory_bytes"],
        "free_memory_bytes": device["free_memory_bytes"],
        "compute_processes": processes,
        "observation_read_only": True,
        "attempt_marker_created": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def pair06_v8_preclaim_gpu_readonly_observer_contract() -> dict[str, Any]:
    reviewed = _validated_admission_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "admission_review_git_blob": ADMISSION_REVIEW_GIT_BLOB,
        "admission_review_source_sha256": ADMISSION_REVIEW_SOURCE_SHA256,
        "pair06_v8_preclaim_gpu_readonly_observer_implemented": True,
        "pair06_v8_preclaim_gpu_readonly_observer_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "gpu_index": GPU_INDEX,
        "nvidia_smi_path": NVIDIA_SMI,
        "device_query": DEVICE_QUERY,
        "process_query": PROCESS_QUERY,
        "host_nvidia_smi_readonly_runner_present": True,
        "automatic_command_runner_selection": False,
        "observation_requires_explicit_authority": True,
        "maximum_timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
        "maximum_stdout_bytes": MAX_STDOUT_BYTES,
        "observer_output_matches_admission_schema": True,
        "observer_grants_gpu_admission": False,
        "process_signal_implemented": False,
        "process_termination_implemented": False,
        "service_action_implemented": False,
        "attempt_marker_creation_implemented": False,
        "runtime_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "policy_promotion_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "validated_admission_review": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuReadonlyObserverHold(NEXT_GATE)
