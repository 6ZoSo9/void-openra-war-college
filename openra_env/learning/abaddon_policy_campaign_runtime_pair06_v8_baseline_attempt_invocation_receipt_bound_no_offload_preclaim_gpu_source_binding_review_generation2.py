"""Source-only review of GPU-gated receipt-bound pair-06 invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-attempt-invocation-receipt-bound-no-offload-"
    "preclaim-gpu-review-contract.v1"
)

INVOCATION_GIT_BLOB = "ef9ed62758db399d6d59e6b782df8ed5587ed9bb"
INVOCATION_SOURCE_SHA256 = (
    "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386"
)
INVOCATION_TEST_GIT_BLOB = "509d5876606bdedae34a4307b9dc5dd32c59a428"
INVOCATION_TEST_SHA256 = (
    "05d4cacf12c1ee1ee4510b932e68975bf57f0a35be0474da19bebc2295d3c8f4"
)

SPENT_RECEIPT_BOUND_REQUEST_SHA256 = (
    "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
)
SPENT_OOM_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)

NEXT_GATE = (
    "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
    "BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_no_offload_receipt_bound_preclaim_gpu_"
    "baseline_execution_authorization_request"
)


class Pair06V8PreclaimGpuInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()

    _require(
        out.get(
            "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_implemented"
        )
        is True,
        "GPU-gated pair06 invocation missing",
    )
    _require(
        out.get(
            "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed"
        )
        is False,
        "GPU-gated pair06 invocation unexpectedly self-reviewed",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False,
        "GPU-gated pair06 invocation scope drift",
    )

    for field in (
        "preclaim_worktree_materialization_implemented",
        "preclaim_materialization_cleanup_on_hold_implemented",
        "reviewed_preclaim_gpu_observer_required",
        "historical_gpu_observation_nonreusable",
        "fresh_preclaim_gpu_observation_implemented",
        "fresh_preclaim_gpu_admission_required",
        "fresh_preclaim_gpu_observation_occurs_after_materialization",
        "fresh_preclaim_gpu_observation_precedes_attempt_marker",
        "gpu_admission_hold_cleans_materialization_before_claim",
        "zero_foreign_cuda0_compute_processes_required",
        "durable_create_only_attempt_marker_implemented",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "marker_sha256_is_attempt_id",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "no_offload_parent_receipt_schema_required",
        "inference_safe_placement_receipt_required",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
    ):
        _require(out.get(field) is True, "GPU-gated invocation invariant drift: " + field)

    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "GPU-gated invocation free-memory threshold drift",
    )
    _require(out.get("maximum_attempts") == 1, "GPU-gated attempt cardinality drift")
    _require(out.get("automatic_retry") is False, "GPU-gated automatic retry drift")

    for field in (
        "pair06_baseline_specific_authorization_accepted",
        "attempt_consumed",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
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
        _require(
            out.get(field) is False,
            "GPU-gated invocation authority drift: " + field,
        )

    deps = out.get("dependencies")
    _require(isinstance(deps, dict), "GPU-gated invocation dependencies missing")
    history = deps.get("historical_precision_gpu_observation_review")
    _require(isinstance(history, dict), "GPU observation history review missing")
    _require(
        history.get("historical_observation_only") is True
        and history.get("observation_reusable_for_future_claim") is False
        and history.get("fresh_reobservation_required_before_attempt_marker") is True,
        "GPU historical observation reuse policy drift",
    )
    _require(
        history.get("retry_authorized") is False
        and history.get("attempt_marker_creation_authorized") is False,
        "GPU historical observation unexpectedly grants authority",
    )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_"
            "PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "GPU-gated invocation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "historical_gpu_observation_reusable": False,
        "spent_receipt_bound_request_sha256": SPENT_RECEIPT_BOUND_REQUEST_SHA256,
        "spent_receipt_bound_request_reusable": False,
        "spent_oom_attempt_marker_sha256": SPENT_OOM_ATTEMPT_MARKER_SHA256,
        "spent_oom_attempt_reusable": False,
        "explicit_authorization_required": True,
        "pair06_baseline_specific_authorization_accepted": False,
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
        "validated_invocation": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuInvocationReviewHold(NEXT_GATE)
