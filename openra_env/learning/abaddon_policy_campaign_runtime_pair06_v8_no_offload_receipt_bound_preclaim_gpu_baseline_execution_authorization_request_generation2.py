"""Proposal-only request for one GPU-gated pair-06 V8 baseline execution.

This request binds the reviewed receipt-bound no-offload invocation that now
performs a fresh CUDA:0 observation and admission immediately before any
create-only attempt marker. It supersedes all prior pair-06 execution requests,
including the receipt-bound request whose authorized attempt was consumed by
an out-of-memory failure.

Matching these bytes never grants authority. Importing or inspecting this
source performs no host observation, process action, attempt claim, model load,
inference, game execution, training, deployment, VOID-chain mutation, or
wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as invocation_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request-validation.v1"
)

INVOCATION_REVIEW_GIT_BLOB = "77dbac309565beb804ac1c2936799574efe5de82"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "beec87bea767fdb0c13c14ed7072d49b8fb18db08f6745c22172931ce8843cce"
)
INVOCATION_SOURCE_SHA256 = (
    "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386"
)

FIRST_SPENT_REQUEST_SHA256 = (
    "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae"
)
SECOND_SPENT_REQUEST_SHA256 = (
    "31c0069869915eb01221d7ea0aa867c0517df0a702eeff58ca69f70dec07a410"
)
HELD_SUPERSEDED_REQUEST_SHA256 = (
    "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
)
SPENT_RECEIPT_BOUND_REQUEST_SHA256 = (
    "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
)
SPENT_RECEIPT_BOUND_AUTHORIZATION_TEXT_SHA256 = (
    "bc898d1349d281a83ee094563f34b7f21d6f4c02891014029d4a8a3fc6d28f0f"
)

FIRST_SPENT_ATTEMPT_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
SECOND_SPENT_ATTEMPT_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)
SPENT_OOM_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)

HISTORICAL_CLEAN_GPU_EVIDENCE_SHA256 = (
    "8ccd26d5a90cda5e75d6b7ce93501ddb240f5d9da2cf56f518f5ce9c96519237"
)
OOM_PRECLAIM_FREE_MEMORY_BYTES = 5756354560
OOM_FOREIGN_COMPUTE_PID = 2850305
OOM_FAILURE_TYPE = "OutOfMemoryError"
OOM_FAILURE_STAGE = "transformers.caching_allocator_warmup"

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
DOCTRINE = "FEINTER"
SEED = 208354846
ROUNDS = 36
TICKS_PER_ROUND = 25
STARTER_INFANTRY = 4
STAGING_MAX_TICKS = 800
RUNTIME_SELECTION_KEY = "apollyon-v3-v8-accepted-model-control"

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "pair06_preclaim_gpu_baseline_specific_authorization_accepted",
    "pair06_preclaim_gpu_baseline_execution_authorized",
    "pair06_preclaim_gpu_baseline_execution_performed",
    "attempt_consumed",
    "attempt_marker_creation_authorized",
    "runtime_load_authorized",
    "model_inference_authorized",
    "game_execution_authorized",
    "child_spawn_authorized",
    "candidate_execution_authorized",
    "candidate_execution_performed",
    "pair15_execution_authorized",
    "pair15_execution_performed",
    "pair03_replay_authorized",
    "pair09_replay_authorized",
    "automatic_retry",
    "training_authorized",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)

NEXT_GATE = (
    "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
    "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
)


class Pair06V8PreclaimGpuBaselineExecutionAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuBaselineExecutionAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    invocation = (
        invocation_review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )

    _require(
        invocation.get(
            "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_"
            "preclaim_gpu_reviewed"
        )
        is True,
        "GPU-gated pair06 invocation not reviewed",
    )
    _require(
        invocation.get("invocation_source_sha256") == INVOCATION_SOURCE_SHA256,
        "GPU-gated pair06 invocation source drift",
    )
    _require(
        invocation.get("pair_slot") == PAIR_SLOT
        and invocation.get("arm") == ARM
        and invocation.get("held_out") is False,
        "GPU-gated pair06 invocation scope drift",
    )
    _require(
        invocation.get("maximum_attempts") == 1
        and invocation.get("maximum_automatic_retries") == 0,
        "GPU-gated pair06 invocation cardinality drift",
    )
    _require(
        invocation.get("fresh_preclaim_gpu_observation_required") is True
        and invocation.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True,
        "GPU-gated pair06 fresh observation requirement missing",
    )
    _require(
        invocation.get("zero_foreign_cuda0_compute_processes_required") is True,
        "GPU-gated pair06 foreign-process policy drift",
    )
    _require(
        invocation.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and invocation.get("minimum_cuda0_free_memory_fraction_denominator")
        == 10,
        "GPU-gated pair06 free-memory threshold drift",
    )
    _require(
        invocation.get("historical_gpu_observation_reusable") is False,
        "historical GPU observation unexpectedly reusable",
    )
    _require(
        invocation.get("spent_receipt_bound_request_sha256")
        == SPENT_RECEIPT_BOUND_REQUEST_SHA256
        and invocation.get("spent_receipt_bound_request_reusable") is False,
        "spent receipt-bound request lineage drift",
    )
    _require(
        invocation.get("spent_oom_attempt_marker_sha256")
        == SPENT_OOM_ATTEMPT_MARKER_SHA256
        and invocation.get("spent_oom_attempt_reusable") is False,
        "spent OOM attempt lineage drift",
    )
    _require(
        invocation.get("pair06_baseline_specific_authorization_accepted")
        is False
        and invocation.get("attempt_marker_creation_authorized") is False
        and invocation.get("runtime_load_authorized") is False
        and invocation.get("game_execution_authorized") is False,
        "GPU-gated invocation unexpectedly grants authority",
    )
    _require(
        invocation.get("next_gate")
        == (
            "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
            "BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
        ),
        "GPU-gated request frontier drift",
    )
    return {"invocation_review": deepcopy(invocation)}


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "lineage": {
            "first_spent_request_sha256": FIRST_SPENT_REQUEST_SHA256,
            "second_spent_request_sha256": SECOND_SPENT_REQUEST_SHA256,
            "held_superseded_request_sha256": HELD_SUPERSEDED_REQUEST_SHA256,
            "spent_receipt_bound_request_sha256": (
                SPENT_RECEIPT_BOUND_REQUEST_SHA256
            ),
            "spent_receipt_bound_authorization_text_sha256": (
                SPENT_RECEIPT_BOUND_AUTHORIZATION_TEXT_SHA256
            ),
            "first_spent_attempt_sha256": FIRST_SPENT_ATTEMPT_SHA256,
            "second_spent_attempt_sha256": SECOND_SPENT_ATTEMPT_SHA256,
            "spent_oom_attempt_marker_sha256": SPENT_OOM_ATTEMPT_MARKER_SHA256,
            "first_spent_request_reusable": False,
            "second_spent_request_reusable": False,
            "held_superseded_request_reusable": False,
            "spent_receipt_bound_request_reusable": False,
            "first_spent_attempt_reusable": False,
            "second_spent_attempt_reusable": False,
            "spent_oom_attempt_reusable": False,
            "spent_receipt_bound_request_was_authorized": True,
            "spent_receipt_bound_attempt_consumed": True,
            "spent_oom_failure_type": OOM_FAILURE_TYPE,
            "spent_oom_failure_stage": OOM_FAILURE_STAGE,
            "spent_oom_preclaim_free_memory_bytes": (
                OOM_PRECLAIM_FREE_MEMORY_BYTES
            ),
            "spent_oom_foreign_compute_pid": OOM_FOREIGN_COMPUTE_PID,
            "repair_reason": (
                "fresh_cuda0_admission_required_before_create_only_marker"
            ),
        },
        "source_binding": {
            "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
            "invocation_review_source_sha256": (
                INVOCATION_REVIEW_SOURCE_SHA256
            ),
            "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        },
        "gpu_admission_policy": {
            "gpu_index": 0,
            "fresh_observation_required": True,
            "fresh_observation_precedes_attempt_marker": True,
            "zero_foreign_compute_processes_required": True,
            "minimum_free_memory_fraction": {
                "numerator": 9,
                "denominator": 10,
            },
            "historical_clean_gpu_evidence_sha256": (
                HISTORICAL_CLEAN_GPU_EVIDENCE_SHA256
            ),
            "historical_clean_gpu_observation_reusable": False,
            "gpu_admission_hold_must_not_consume_attempt": True,
        },
        "proposed_scope": {
            "pair_slot": PAIR_SLOT,
            "arm": ARM,
            "held_out": HELD_OUT,
            "doctrine": DOCTRINE,
            "seed": SEED,
            "rounds": ROUNDS,
            "ticks_per_round": TICKS_PER_ROUND,
            "starter_infantry": STARTER_INFANTRY,
            "staging_max_ticks": STAGING_MAX_TICKS,
            "runtime_selection_key": RUNTIME_SELECTION_KEY,
            "maximum_attempts": 1,
            "maximum_automatic_retries": 0,
            "candidate_arm_included": False,
            "held_out_pair15_included": False,
            "pair03_replay_included": False,
            "pair09_replay_included": False,
        },
        "required_runtime_gates": [
            "exact_gpu_gated_request_source_reviewed",
            "pair06_preclaim_gpu_baseline_specific_operator_authorization_accepted",
            "exact_gpu_gated_invocation_source_reviewed_and_canonical",
            "exact_current_main_required",
            "fresh_baseline_arm_root",
            "fresh_v8_environment_and_17_assets",
            "preclaim_exact_frozen_worktree_materialization",
            "fresh_cuda0_readonly_observation",
            "zero_foreign_cuda0_compute_processes",
            "minimum_90_percent_cuda0_memory_free",
            "fresh_gpu_admission_before_attempt_marker",
            "gpu_admission_hold_cleanup_without_attempt_consumption",
            "create_only_single_use_attempt_marker",
            "marker_sha256_bound_as_attempt_id",
            "authority_rechecked_after_claim",
            "authority_rechecked_before_each_inference",
            "private_child_process_group",
            "legacy_ollama_not_started_or_contacted",
            "inference_safe_cuda0_placement_receipt_required",
            "durable_execution_result_before_worktree_cleanup",
            "success_only_owned_worktree_cleanup",
            "durable_cleanup_closeout",
        ],
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "request_validation_performs_host_io": False,
        "next_gate": NEXT_GATE,
    }


def build_pair06_v8_preclaim_gpu_baseline_execution_authorization_request() -> bytes:
    _dependencies()
    return (
        json.dumps(
            _request_record(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def validate_pair06_v8_preclaim_gpu_baseline_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v8_preclaim_gpu_baseline_execution_authorization_request()
    _require(payload == expected, "request bytes differ from fixed GPU-gated proposal")
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract() -> dict[str, Any]:
    payload = build_pair06_v8_preclaim_gpu_baseline_execution_authorization_request()
    result = (
        validate_pair06_v8_preclaim_gpu_baseline_execution_authorization_request(
            payload
        )
    )
    return {
        **result,
        "pair06_v8_preclaim_gpu_baseline_execution_authorization_request_implemented": True,
        "pair06_preclaim_gpu_baseline_specific_authorization_accepted": False,
        "pair06_preclaim_gpu_baseline_execution_authorized": False,
        "pair06_preclaim_gpu_baseline_execution_performed": False,
        "spent_receipt_bound_request_reusable": False,
        "spent_oom_attempt_reusable": False,
        "fresh_preclaim_gpu_observation_required": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "historical_clean_gpu_observation_reusable": False,
        "matching_request_digest_grants_authority": False,
        "request": _request_record(),
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuBaselineExecutionAuthorizationRequestHold(NEXT_GATE)
