"""Source-only review of accepted clean pair-06 Precision GPU evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_preclaim_gpu_observation_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-preclaim-gpu-observation-source-binding-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "d7ce43d57a0640a15f84a9de66f4897bf0b71307"
ACCEPTANCE_SOURCE_SHA256 = (
    "169223f26bf706bc87d48c365549e6a5148bf3bd755709e4eb4e35d729172daf"
)
ACCEPTANCE_TEST_GIT_BLOB = "7e296d2fffc3d3e56c89aed9eef6f21c4482e701"
ACCEPTANCE_TEST_SHA256 = (
    "04bb4a78053b201a44a571d38343d7086cb1ffb0b12aa9559702e793df92980c"
)

NEXT_GATE = "PAIR06_V8_PRECLAIM_GPU_INVOCATION_INTEGRATION_SOURCE_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_preclaim_gpu_invocation_integration"
)


class Pair06V8PrecisionPreclaimGpuObservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PrecisionPreclaimGpuObservationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = acceptance.pair06_v8_precision_preclaim_gpu_observation_acceptance_contract()

    _require(
        out.get("pair06_v8_precision_preclaim_gpu_observation_accepted") is True,
        "pair06 Precision GPU observation acceptance missing",
    )
    _require(
        out.get("observer_sha256")
        == "899c77ff6dfa9d2708152754a1b073f9f856703e6eebffd282599a1672eec156",
        "pair06 Precision GPU observer artifact SHA drift",
    )
    _require(
        out.get("canonical_main_head")
        == "b75d7a056d3aa6742532697c21758bcf733ab28b",
        "pair06 Precision GPU observation main-head drift",
    )
    _require(
        out.get("accepted_evidence_sha256")
        == "8ccd26d5a90cda5e75d6b7ce93501ddb240f5d9da2cf56f518f5ce9c96519237",
        "pair06 Precision GPU accepted-evidence SHA drift",
    )
    _require(out.get("pair_slot") == 6, "pair06 Precision GPU slot drift")
    _require(out.get("gpu_index") == 0, "pair06 Precision GPU index drift")
    _require(
        out.get("free_fraction_ppm") == 909708,
        "pair06 Precision GPU free-fraction drift",
    )
    _require(
        out.get("compute_process_count") == 0,
        "pair06 Precision GPU compute-process count drift",
    )
    _require(
        out.get("preclaim_gpu_admitted_at_observation") is True,
        "pair06 Precision GPU observation was not admitted",
    )
    _require(
        out.get("historical_observation_only") is True,
        "pair06 Precision GPU observation lost historical-only status",
    )
    _require(
        out.get("observation_reusable_for_future_claim") is False,
        "pair06 Precision GPU observation became reusable",
    )
    _require(
        out.get("fresh_reobservation_required_before_attempt_marker") is True,
        "pair06 Precision GPU fresh re-observation requirement missing",
    )

    for field in (
        "retry_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(
            out.get(field) is False,
            "pair06 Precision GPU acceptance authority drift: " + field,
        )

    _require(
        out.get("next_gate")
        == "PAIR06_V8_PRECISION_PRECLAIM_GPU_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 Precision GPU observation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_precision_preclaim_gpu_observation_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "separate_review_instrument": True,
        "observation_source_identity_pinned_by_git_blob": True,
        "observation_source_identity_pinned_by_sha256": True,
        "observation_test_identity_pinned_by_git_blob": True,
        "observation_test_identity_pinned_by_sha256": True,
        "pair06_v8_precision_preclaim_gpu_observation_reviewed": True,
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
        "reviewed_acceptance": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def claim_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionPreclaimGpuObservationReviewHold(NEXT_GATE)
