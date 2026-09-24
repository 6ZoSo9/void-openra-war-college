"""Source-only review of pair-06 V8 pre-claim GPU read-only observer."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_readonly_observer_generation2
    as observer,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-preclaim-gpu-readonly-observer-source-binding-review-contract.v1"
)

OBSERVER_GIT_BLOB = "8cc439b59e31ca99e078c5bb96648826ac21edaf"
OBSERVER_SOURCE_SHA256 = (
    "e4006f0ba8959430dc0f8d83374c6743813a1956f7b31b69a9d361ee01e719e4"
)
OBSERVER_TEST_GIT_BLOB = "af6e5e8def82a5484e83eecb68a5cba99b0e69b5"
OBSERVER_TEST_SHA256 = (
    "d54eac1e08b856c2ef734ab29e29d9d9252499ac22b1e22812848c840c33564b"
)

ADMISSION_REVIEW_GIT_BLOB = "00876b15ce0317d548b14e98dd5c3a480f11c84f"
ADMISSION_REVIEW_SOURCE_SHA256 = (
    "3991a1bcb2ffe855495cb983c3a4540f947d2079d60c7bf8fd1283b8a6ca06ba"
)

NEXT_GATE = "PAIR06_V8_PRECLAIM_GPU_PRECISION_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "trusted_operator_pair06_v8_preclaim_gpu_precision_observation"
)


class Pair06V8PreclaimGpuReadonlyObserverReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuReadonlyObserverReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = observer.pair06_v8_preclaim_gpu_readonly_observer_contract()

    _require(
        out.get("pair06_v8_preclaim_gpu_readonly_observer_implemented") is True,
        "pair06 GPU read-only observer missing",
    )
    _require(
        out.get("pair06_v8_preclaim_gpu_readonly_observer_reviewed") is False,
        "pair06 GPU read-only observer unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "pair06 GPU observer slot drift")
    _require(out.get("gpu_index") == 0, "pair06 GPU observer index drift")
    _require(
        out.get("admission_review_git_blob") == ADMISSION_REVIEW_GIT_BLOB,
        "pair06 GPU observer admission-review blob drift",
    )
    _require(
        out.get("admission_review_source_sha256")
        == ADMISSION_REVIEW_SOURCE_SHA256,
        "pair06 GPU observer admission-review SHA drift",
    )
    _require(
        out.get("nvidia_smi_path") == "/usr/bin/nvidia-smi",
        "pair06 GPU observer nvidia-smi path drift",
    )
    _require(
        tuple(out.get("device_query", ())) == observer.DEVICE_QUERY,
        "pair06 GPU observer device query drift",
    )
    _require(
        tuple(out.get("process_query", ())) == observer.PROCESS_QUERY,
        "pair06 GPU observer process query drift",
    )
    _require(
        out.get("host_nvidia_smi_readonly_runner_present") is True
        and out.get("automatic_command_runner_selection") is False,
        "pair06 GPU observer runner policy drift",
    )
    _require(
        out.get("observation_requires_explicit_authority") is True,
        "pair06 GPU observer authority gate missing",
    )
    _require(
        out.get("maximum_timeout_seconds") == 5.0
        and out.get("maximum_stdout_bytes") == 65536,
        "pair06 GPU observer bounds drift",
    )
    _require(
        out.get("observer_output_matches_admission_schema") is True,
        "pair06 GPU observer output schema drift",
    )

    for field in (
        "observer_grants_gpu_admission",
        "process_signal_implemented",
        "process_termination_implemented",
        "service_action_implemented",
        "attempt_marker_creation_implemented",
        "runtime_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "training_implemented",
        "policy_promotion_implemented",
        "deployment_implemented",
        "void_chain_mutation_implemented",
        "wallet_or_funds_action_implemented",
    ):
        _require(
            out.get(field) is False,
            "pair06 GPU observer capability drift: " + field,
        )

    _require(
        out.get("next_gate")
        == "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 GPU observer review frontier drift",
    )

    return deepcopy(out)


def pair06_v8_preclaim_gpu_readonly_observer_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "observer_git_blob": OBSERVER_GIT_BLOB,
        "observer_source_sha256": OBSERVER_SOURCE_SHA256,
        "observer_test_git_blob": OBSERVER_TEST_GIT_BLOB,
        "observer_test_sha256": OBSERVER_TEST_SHA256,
        "admission_review_git_blob": ADMISSION_REVIEW_GIT_BLOB,
        "admission_review_source_sha256": ADMISSION_REVIEW_SOURCE_SHA256,
        "pair06_v8_preclaim_gpu_readonly_observer_source_binding_present": True,
        "pair06_v8_preclaim_gpu_readonly_observer_reviewed": True,
        "pair_slot": 6,
        "gpu_index": 0,
        "nvidia_smi_path": "/usr/bin/nvidia-smi",
        "device_query": observer.DEVICE_QUERY,
        "process_query": observer.PROCESS_QUERY,
        "observation_requires_explicit_authority": True,
        "automatic_command_runner_selection": False,
        "observer_grants_gpu_admission": False,
        "process_signal_implemented": False,
        "process_termination_implemented": False,
        "attempt_marker_creation_implemented": False,
        "runtime_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "retry_authorized": False,
        "execution_authorized": False,
        "validated_observer": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuReadonlyObserverReviewHold(NEXT_GATE)
