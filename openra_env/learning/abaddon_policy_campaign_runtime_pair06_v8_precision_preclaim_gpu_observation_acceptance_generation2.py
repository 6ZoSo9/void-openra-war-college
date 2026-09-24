"""Source-only acceptance of the exact clean Precision pair-06 GPU observation.

The accepted evidence was produced by the separately reviewed read-only CUDA:0
observer after the promoted Apollyon runtime was deliberately stopped through
systemd. The observer reported zero CUDA:0 compute processes and 90.9708%
free device memory, satisfying the reviewed pre-claim GPU admission policy.

This acceptance is historical evidence only. GPU state is transient, so this
observation is explicitly non-reusable for a future attempt claim. Any future
pair-06 invocation must re-observe and re-admit CUDA:0 immediately before a
create-only attempt marker.

Importing or inspecting this source performs no host observation, service
action, process signal, attempt claim, model load, inference, game execution,
training, promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_readonly_observer_source_binding_review_generation2
    as observer_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-preclaim-gpu-observation-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-preclaim-gpu-observation-acceptance.v1"
)

OBSERVER_REVIEW_GIT_BLOB = "37ea632d973d6bba7e4cc7210dedcfc7c1fd8025"
OBSERVER_REVIEW_SOURCE_SHA256 = (
    "81a676bdd69694282d9d36d1f673ea07fe600bba736b1958064c04a0c075ebfb"
)

PRECISION_OBSERVER_ARTIFACT_SHA256 = (
    "899c77ff6dfa9d2708152754a1b073f9f856703e6eebffd282599a1672eec156"
)
CANONICAL_MAIN_HEAD = "b75d7a056d3aa6742532697c21758bcf733ab28b"

EXPECTED_EVIDENCE = {
    "observer_sha256": PRECISION_OBSERVER_ARTIFACT_SHA256,
    "canonical_main_head": CANONICAL_MAIN_HEAD,
    "pair_slot": 6,
    "gpu_index": 0,
    "total_memory_bytes": 12820938752,
    "free_memory_bytes": 11663310848,
    "free_fraction_ppm": 909708,
    "compute_process_count": 0,
    "compute_processes": (),
    "observation_read_only": True,
    "attempt_marker_created": False,
    "model_load_performed": False,
    "model_inference_performed": False,
    "game_execution_performed": False,
    "preclaim_gpu_admitted": True,
    "admission_hold": "NONE",
    "observation_result": "GREEN",
    "observation_reusable_for_future_claim": False,
    "retry_authorized": False,
    "execution_authorized": False,
}

NEXT_GATE = (
    "PAIR06_V8_PRECISION_PRECLAIM_GPU_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_precision_preclaim_gpu_observation_source_binding_review"
)


class Pair06V8PrecisionPreclaimGpuObservationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PrecisionPreclaimGpuObservationAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def _validate_observer_review() -> dict[str, Any]:
    reviewed = observer_review.pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    _require(
        reviewed.get("pair06_v8_preclaim_gpu_readonly_observer_reviewed") is True,
        "pair06 GPU observer source review missing",
    )
    _require(reviewed.get("pair_slot") == 6, "pair06 GPU observer slot drift")
    _require(reviewed.get("gpu_index") == 0, "pair06 GPU observer index drift")
    _require(
        reviewed.get("nvidia_smi_path") == "/usr/bin/nvidia-smi",
        "pair06 GPU observer path drift",
    )
    _require(
        reviewed.get("observation_requires_explicit_authority") is True,
        "pair06 GPU observer authority requirement drift",
    )
    _require(
        reviewed.get("automatic_command_runner_selection") is False,
        "pair06 GPU observer unexpectedly selects backend automatically",
    )
    for field in (
        "observer_grants_gpu_admission",
        "process_signal_implemented",
        "process_termination_implemented",
        "attempt_marker_creation_implemented",
        "runtime_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "retry_authorized",
        "execution_authorized",
    ):
        _require(
            reviewed.get(field) is False,
            "pair06 GPU observer boundary drift: " + field,
        )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_PRECLAIM_GPU_PRECISION_OBSERVATION_REQUIRED",
        "pair06 GPU observer frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair06_v8_precision_preclaim_gpu_observation(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    reviewed = _validate_observer_review()
    _require(isinstance(evidence, Mapping), "pair06 GPU evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair06 GPU evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            "pair06 GPU evidence drift: " + field,
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair06 GPU evidence digest drift",
    )
    _require(
        supplied["compute_process_count"] == len(supplied["compute_processes"]) == 0,
        "pair06 GPU evidence unexpectedly contains compute process",
    )
    _require(
        supplied["free_fraction_ppm"] >= 900000,
        "pair06 GPU evidence below reviewed 90 percent threshold",
    )
    _require(
        supplied["free_memory_bytes"] * 1_000_000
        // supplied["total_memory_bytes"]
        == supplied["free_fraction_ppm"],
        "pair06 GPU free fraction arithmetic drift",
    )
    _require(
        supplied["observation_reusable_for_future_claim"] is False,
        "pair06 GPU observation must remain non-reusable",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_precision_preclaim_gpu_observation_accepted": True,
        "accepted_evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": PRECISION_OBSERVER_ARTIFACT_SHA256,
        "canonical_main_head": CANONICAL_MAIN_HEAD,
        "pair_slot": 6,
        "gpu_index": 0,
        "total_memory_bytes": supplied["total_memory_bytes"],
        "free_memory_bytes": supplied["free_memory_bytes"],
        "free_fraction_ppm": supplied["free_fraction_ppm"],
        "compute_process_count": 0,
        "compute_processes": (),
        "preclaim_gpu_admitted_at_observation": True,
        "historical_observation_only": True,
        "observation_reusable_for_future_claim": False,
        "fresh_reobservation_required_before_attempt_marker": True,
        "retry_authorized": False,
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
        "reviewed_observer": reviewed,
        "accepted_evidence": deepcopy(supplied),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def pair06_v8_precision_preclaim_gpu_observation_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_precision_preclaim_gpu_observation(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "observer_review_git_blob": OBSERVER_REVIEW_GIT_BLOB,
        "observer_review_source_sha256": OBSERVER_REVIEW_SOURCE_SHA256,
        "pair06_v8_precision_preclaim_gpu_observation_accepted": True,
        "accepted_evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": PRECISION_OBSERVER_ARTIFACT_SHA256,
        "canonical_main_head": CANONICAL_MAIN_HEAD,
        "pair_slot": 6,
        "gpu_index": 0,
        "free_fraction_ppm": 909708,
        "compute_process_count": 0,
        "preclaim_gpu_admitted_at_observation": True,
        "historical_observation_only": True,
        "observation_reusable_for_future_claim": False,
        "fresh_reobservation_required_before_attempt_marker": True,
        "retry_authorized": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_observation": accepted,
    }


def claim_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionPreclaimGpuObservationAcceptanceHold(NEXT_GATE)
