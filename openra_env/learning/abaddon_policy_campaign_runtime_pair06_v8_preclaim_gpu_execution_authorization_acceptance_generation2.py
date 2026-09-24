"""Audit-only acceptance of one GPU-gated pair-06 V8 execution authorization.

This record binds the user's exact explicit authorization to the reviewed
GPU-gated request and canonical War College main. It performs no host I/O,
GPU observation, service/process action, attempt claim, model load, inference,
game execution, training, deployment, VOID-chain mutation, or wallet/funds
action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-preclaim-gpu-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
)
AUTHORIZED_REQUEST_BYTES = 4785
AUTHORIZED_MAIN_HEAD = "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
AUTHORIZATION_TEXT_SHA256 = (
    "3cdbfa07fcc1fa14ab0ce01a7e5456b1bf16583ceda5baee16a0191e8a3cf011"
)
AUTHORIZATION_TEXT_BYTES = 1127

REQUEST_REVIEW_GIT_BLOB = "03b0d2cd22a9f54dcbad1ac165f1b04c645f3497"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "61a77ac4fb302004802daa4047f686d0f70282c412dfb1738d21916f16cac3e5"
)
INVOCATION_REVIEW_GIT_BLOB = "77dbac309565beb804ac1c2936799574efe5de82"
INVOCATION_SOURCE_SHA256 = (
    "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386"
)

SPENT_RECEIPT_BOUND_REQUEST_SHA256 = (
    "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
)
SPENT_OOM_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)

NEXT_GATE = "PAIR06_V8_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED"


class Pair06V8PreclaimGpuAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    _require(
        out.get(
            "pair06_v8_preclaim_gpu_baseline_execution_authorization_request_reviewed"
        )
        is True,
        "GPU-gated pair06 request review missing",
    )
    _require(
        out.get("request_sha256") == AUTHORIZED_REQUEST_SHA256
        and out.get("request_byte_length") == AUTHORIZED_REQUEST_BYTES,
        "GPU-gated authorized request identity drift",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False,
        "GPU-gated authorized request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "GPU-gated authorized request cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "GPU-gated authorized request observation policy drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "GPU-gated authorized request free-memory threshold drift",
    )
    _require(
        out.get("historical_clean_gpu_observation_reusable") is False,
        "historical GPU observation unexpectedly reusable",
    )
    _require(
        out.get("spent_receipt_bound_request_sha256")
        == SPENT_RECEIPT_BOUND_REQUEST_SHA256
        and out.get("spent_receipt_bound_request_reusable") is False,
        "spent request lineage drift",
    )
    _require(
        out.get("spent_oom_attempt_marker_sha256")
        == SPENT_OOM_ATTEMPT_MARKER_SHA256
        and out.get("spent_oom_attempt_reusable") is False,
        "spent OOM attempt lineage drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly grants authority without this acceptance",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
            "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
        ),
        "GPU-gated request authorization frontier drift",
    )
    return deepcopy(out)


def pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_request_bytes": AUTHORIZED_REQUEST_BYTES,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "gpu_admission_failure_must_not_create_attempt_marker": True,
        "gpu_admission_failure_must_not_load_model": True,
        "gpu_admission_failure_must_not_execute_inference": True,
        "gpu_admission_failure_must_not_execute_game": True,
        "historical_clean_gpu_observation_reusable": False,
        "receipt_bound_preclaim_gpu_execution_authorized": True,
        "attempt_marker_creation_authorized_after_fresh_gpu_admission": True,
        "runtime_load_authorized_after_fresh_gpu_admission": True,
        "model_inference_authorized_after_fresh_gpu_admission": True,
        "game_execution_authorized_after_fresh_gpu_admission": True,
        "spent_receipt_bound_request_sha256": SPENT_RECEIPT_BOUND_REQUEST_SHA256,
        "spent_receipt_bound_request_reusable": False,
        "spent_oom_attempt_marker_sha256": SPENT_OOM_ATTEMPT_MARKER_SHA256,
        "spent_oom_attempt_reusable": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "attempt_marker_created_by_this_record": False,
        "gpu_observation_performed_by_this_record": False,
        "runtime_load_performed_by_this_record": False,
        "model_inference_performed_by_this_record": False,
        "game_execution_performed_by_this_record": False,
        "authorization_reusable_after_attempt_claim": False,
        "reviewed_request": reviewed,
        "next_gate": NEXT_GATE,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuAuthorizationAcceptanceHold(NEXT_GATE)
