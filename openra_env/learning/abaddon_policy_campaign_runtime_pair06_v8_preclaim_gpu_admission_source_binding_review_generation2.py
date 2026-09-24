"""Source-only review of pair-06 V8 pre-claim GPU admission."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_admission_generation2
    as admission,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-preclaim-gpu-admission-source-binding-review-contract.v1"
)

ADMISSION_GIT_BLOB = "af50d685fcb3eb8d1879289e5cf2667743a117ed"
ADMISSION_SOURCE_SHA256 = (
    "8ed38a671cba24940d6612d2cdb15cf813db67ad82ee817774f9450eb547dd29"
)
ADMISSION_TEST_GIT_BLOB = "061ee4e89413d0ecd79eea62da89111afe52cb8d"
ADMISSION_TEST_SHA256 = (
    "8c842e15c21eb10f148e9296fe76c6f8d4b22dbd91dba4482a9621fa75cd1a57"
)

NEXT_GATE = "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_preclaim_gpu_readonly_observer"


class Pair06V8PreclaimGpuAdmissionReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuAdmissionReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = admission.pair06_v8_preclaim_gpu_admission_contract()

    _require(
        out.get("pair06_v8_preclaim_gpu_admission_implemented") is True,
        "pair06 preclaim GPU admission missing",
    )
    _require(
        out.get("pair06_v8_preclaim_gpu_admission_reviewed") is False,
        "pair06 preclaim GPU admission unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "pair06 preclaim GPU slot drift")
    _require(out.get("gpu_index") == 0, "pair06 preclaim GPU index drift")
    _require(
        out.get("foreign_compute_processes_allowed") is False,
        "pair06 preclaim GPU foreign-process policy drift",
    )
    _require(
        out.get("minimum_free_memory_fraction")
        == {"numerator": 9, "denominator": 10},
        "pair06 preclaim GPU free-memory threshold drift",
    )
    _require(
        out.get("admission_must_precede_attempt_marker") is True,
        "pair06 preclaim GPU ordering invariant missing",
    )
    _require(
        out.get("read_only_observer_required") is True,
        "pair06 preclaim GPU read-only observer requirement missing",
    )
    _require(
        out.get("prior_consumed_attempt_marker_sha256")
        == "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3",
        "pair06 preclaim GPU prior attempt identity drift",
    )
    _require(
        out.get("prior_preclaim_free_memory_bytes") == 5756354560,
        "pair06 preclaim GPU prior free-memory evidence drift",
    )
    _require(
        out.get("prior_foreign_compute_pid") == 2850305,
        "pair06 preclaim GPU prior foreign-process evidence drift",
    )
    _require(
        out.get("prior_failure_type") == "OutOfMemoryError"
        and out.get("prior_failure_stage")
        == "transformers.caching_allocator_warmup",
        "pair06 preclaim GPU prior failure evidence drift",
    )
    _require(
        out.get("prior_attempt_reusable") is False,
        "pair06 preclaim GPU prior attempt became reusable",
    )

    for field in (
        "retry_authorized",
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
        "host_io_performed_by_contract_inspection",
    ):
        _require(out.get(field) is False, f"pair06 preclaim GPU authority drift: {field}")

    _require(
        out.get("next_gate")
        == "PAIR06_V8_PRECLAIM_GPU_ADMISSION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 preclaim GPU review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_preclaim_gpu_admission_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "admission_git_blob": ADMISSION_GIT_BLOB,
        "admission_source_sha256": ADMISSION_SOURCE_SHA256,
        "admission_test_git_blob": ADMISSION_TEST_GIT_BLOB,
        "admission_test_sha256": ADMISSION_TEST_SHA256,
        "pair06_v8_preclaim_gpu_admission_source_binding_present": True,
        "pair06_v8_preclaim_gpu_admission_reviewed": True,
        "pair_slot": 6,
        "gpu_index": 0,
        "foreign_compute_processes_allowed": False,
        "minimum_free_memory_fraction": {
            "numerator": 9,
            "denominator": 10,
        },
        "admission_must_precede_attempt_marker": True,
        "read_only_observer_required": True,
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
        "validated_admission": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuAdmissionReviewHold(NEXT_GATE)
