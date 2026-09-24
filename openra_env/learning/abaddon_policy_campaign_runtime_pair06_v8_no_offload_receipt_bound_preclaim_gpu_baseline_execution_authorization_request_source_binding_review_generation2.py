"""Source-only review of the GPU-gated pair-06 execution request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request-review-contract.v1"
)

REQUEST_GIT_BLOB = "6fd00cbca51eb08eda313e5996154033ab6c1275"
REQUEST_SOURCE_SHA256 = (
    "bbfc9f51c115b6b86e150f458bf95ab318d12d6408f9b731a1c16e2b7aee3298"
)
REQUEST_TEST_GIT_BLOB = "3d45b74c57fd97151f7ee29e1f2745098a2e332c"
REQUEST_TEST_SHA256 = (
    "c486db92a3c35fac2c1a3fcd2d91fded4052946d3c616a74753141b55daf9705"
)
REQUEST_BYTES_SHA256 = (
    "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
)
REQUEST_BYTE_LENGTH = 4785

SPENT_RECEIPT_BOUND_REQUEST_SHA256 = (
    "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
)
SPENT_OOM_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)

NEXT_GATE = (
    "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
    "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "explicit_pair06_v8_no_offload_receipt_bound_preclaim_gpu_"
    "baseline_execution_authorization"
)


class Pair06V8PreclaimGpuRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract()
    proposal = out.get("request")

    _require(
        out.get(
            "pair06_v8_preclaim_gpu_baseline_execution_authorization_request_implemented"
        )
        is True,
        "GPU-gated pair06 request missing",
    )
    _require(
        isinstance(proposal, dict)
        and proposal.get("record_kind") == "proposal_only_not_authorization",
        "GPU-gated pair06 request not proposal-only",
    )
    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "GPU-gated pair06 request digest drift",
    )
    _require(
        out.get("request_byte_length") == REQUEST_BYTE_LENGTH,
        "GPU-gated pair06 request byte-length drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "GPU-gated request digest unexpectedly grants authority",
    )

    binding = proposal.get("source_binding")
    _require(isinstance(binding, dict), "GPU-gated source binding missing")
    _require(
        binding.get("invocation_review_git_blob")
        == "77dbac309565beb804ac1c2936799574efe5de82"
        and binding.get("invocation_review_source_sha256")
        == "beec87bea767fdb0c13c14ed7072d49b8fb18db08f6745c22172931ce8843cce"
        and binding.get("invocation_source_sha256")
        == "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386",
        "GPU-gated invocation source binding drift",
    )

    lineage = proposal.get("lineage")
    _require(isinstance(lineage, dict), "GPU-gated request lineage missing")
    _require(
        lineage.get("spent_receipt_bound_request_sha256")
        == SPENT_RECEIPT_BOUND_REQUEST_SHA256
        and lineage.get("spent_receipt_bound_request_reusable") is False,
        "spent receipt-bound request lineage drift",
    )
    _require(
        lineage.get("spent_oom_attempt_marker_sha256")
        == SPENT_OOM_ATTEMPT_MARKER_SHA256
        and lineage.get("spent_oom_attempt_reusable") is False,
        "spent OOM attempt lineage drift",
    )
    _require(
        lineage.get("spent_receipt_bound_request_was_authorized") is True
        and lineage.get("spent_receipt_bound_attempt_consumed") is True,
        "spent OOM authorization/claim state drift",
    )
    _require(
        lineage.get("spent_oom_failure_type") == "OutOfMemoryError"
        and lineage.get("spent_oom_failure_stage")
        == "transformers.caching_allocator_warmup",
        "spent OOM terminal evidence drift",
    )

    policy = proposal.get("gpu_admission_policy")
    _require(isinstance(policy, dict), "GPU admission policy missing")
    _require(
        policy.get("gpu_index") == 0
        and policy.get("fresh_observation_required") is True
        and policy.get("fresh_observation_precedes_attempt_marker") is True
        and policy.get("zero_foreign_compute_processes_required") is True,
        "GPU admission policy scope drift",
    )
    _require(
        policy.get("minimum_free_memory_fraction")
        == {"numerator": 9, "denominator": 10},
        "GPU admission free-memory threshold drift",
    )
    _require(
        policy.get("historical_clean_gpu_observation_reusable") is False
        and policy.get("gpu_admission_hold_must_not_consume_attempt") is True,
        "GPU observation reuse/claim policy drift",
    )

    scope = proposal.get("proposed_scope")
    _require(
        isinstance(scope, dict)
        and scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("seed") == 208354846
        and scope.get("doctrine") == "FEINTER"
        and scope.get("rounds") == 36
        and scope.get("ticks_per_round") == 25
        and scope.get("maximum_attempts") == 1
        and scope.get("maximum_automatic_retries") == 0,
        "GPU-gated pair06 scope drift",
    )

    authority = out.get("authority")
    _require(
        isinstance(authority, dict)
        and authority
        and all(value is False for value in authority.values()),
        "GPU-gated request authority drift",
    )
    _require(
        out.get("next_gate") == NEXT_GATE,
        "GPU-gated request frontier drift",
    )
    return deepcopy(out)


def pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "request_bytes_sha256": REQUEST_BYTES_SHA256,
        "request_byte_length": REQUEST_BYTE_LENGTH,
        "pair06_v8_preclaim_gpu_baseline_execution_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
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
        "historical_clean_gpu_observation_reusable": False,
        "spent_receipt_bound_request_sha256": SPENT_RECEIPT_BOUND_REQUEST_SHA256,
        "spent_receipt_bound_request_reusable": False,
        "spent_oom_attempt_marker_sha256": SPENT_OOM_ATTEMPT_MARKER_SHA256,
        "spent_oom_attempt_reusable": False,
        "matching_request_digest_grants_authority": False,
        "pair06_preclaim_gpu_baseline_specific_authorization_accepted": False,
        "pair06_preclaim_gpu_baseline_execution_authorized": False,
        "pair06_preclaim_gpu_baseline_execution_performed": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuRequestReviewHold(NEXT_GATE)
