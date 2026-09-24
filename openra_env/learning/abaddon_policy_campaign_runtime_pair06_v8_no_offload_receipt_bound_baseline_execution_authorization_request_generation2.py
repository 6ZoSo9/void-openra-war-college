"""Proposal-only replacement request for one receipt-bound no-offload pair-06 V8 baseline execution.

This request is distinct from both spent pair-06 execution requests, both
consumed attempts, and the later no-offload request that was explicitly
authorized but held pre-claim after a receipt-schema mismatch was discovered.
It binds the repaired reviewed invocation generation. Matching these bytes
never grants authority.

No host observation, worktree mutation, attempt consumption, model load,
inference, game execution, child spawn, training, deployment, VOID-chain
mutation, wallet action, or funds action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_source_binding_review_generation2
    as invocation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_result_source_binding_review_generation2
    as preservation_result_review,
)

REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-receipt-bound-baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-receipt-bound-baseline-execution-authorization-request-validation.v1"
)

INVOCATION_REVIEW_GIT_BLOB = "dbe0390492520ec3307e4c9238136f5637962bbb"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "f5b7e9ceeddf07a98b74a8701802851fb46587a95aba7e6d3f866b1128c3b475"
)
PRESERVATION_RESULT_REVIEW_GIT_BLOB = "16fe141898537776be87654d32f4e7b67c34e880"
PRESERVATION_RESULT_REVIEW_SOURCE_SHA256 = (
    "f22a25a097e739ca1f661f207d69b4c98d69f26227fa5a43d8c84010de91f66a"
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
HELD_SUPERSEDED_REQUEST_AUTHORIZATION_TEXT_SHA256 = (
    "1159b0b9f8e1914c69343ee2091f72bac573ce11a04b1543bd3b44b65b1722f5"
)
FIRST_SPENT_ATTEMPT_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
SECOND_SPENT_ATTEMPT_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)
FIRST_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "d32cc7779fb1570ac2085031e296817059ce51d35de43ca3875becf9d032ccff"
)
SECOND_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bb0bbfe5c7441706ce61924a718c4055a8e2c991c117f699ad5aa0c7863339b4"
)
SECOND_PRESERVATION_RECEIPT_LOGICAL_SHA256 = (
    "d14d65eb507a8d86c55e866cf227c96989e0ee327ce62955cf958183bb51572b"
)

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
    "pair06_no_offload_baseline_specific_authorization_accepted",
    "pair06_no_offload_baseline_execution_authorized",
    "pair06_no_offload_baseline_execution_performed",
    "attempt_consumed",
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

NEXT_GATE = "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"


class Pair06V8NoOffloadReceiptBoundBaselineExecutionAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8NoOffloadReceiptBoundBaselineExecutionAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    invocation = (
        invocation_review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_review_contract()
    )
    preservation = (
        preservation_result_review
        .pair06_v8_second_preservation_result_review_contract()
    )

    _require(
        invocation.get("pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed")
        is True,
        "no-offload pair06 invocation not reviewed",
    )
    _require(
        invocation.get("invocation_source_sha256")
        == "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b",
        "no-offload pair06 invocation source drift",
    )
    _require(
        invocation.get("pair_slot") == PAIR_SLOT
        and invocation.get("arm") == ARM
        and invocation.get("held_out") is False,
        "no-offload pair06 invocation scope drift",
    )
    _require(
        invocation.get("maximum_attempts") == 1
        and invocation.get("automatic_retry") is False,
        "no-offload pair06 invocation cardinality drift",
    )
    _require(
        invocation.get("no_offload_parent_generation_required") is True,
        "no-offload pair06 parent requirement missing",
    )
    _require(
        invocation.get("second_preservation_result_review_required") is True,
        "no-offload pair06 preservation requirement missing",
    )
    _require(
        invocation.get("no_offload_parent_receipt_schema_required") is True
        and invocation.get("inference_safe_placement_receipt_required") is True,
        "no-offload pair06 receipt binding requirement missing",
    )

    _require(
        preservation.get("pair06_v8_second_preservation_result_reviewed") is True,
        "second pair06 preservation result not reviewed",
    )
    _require(
        preservation.get("second_failed_attempt_archived") is True
        and preservation.get("second_failed_attempt_deleted") is False
        and preservation.get("prior_failed_attempt_archive_unchanged") is True,
        "pair06 preservation lineage drift",
    )
    _require(
        preservation.get(
            "fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt"
        )
        is True,
        "fresh pair06 baseline root unavailable",
    )
    _require(
        preservation.get("runtime_retry_authorized") is False
        and preservation.get("automatic_retry") is False,
        "pair06 preservation unexpectedly authorizes retry",
    )
    _require(
        preservation.get("next_gate")
        == "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED",
        "pair06 no-offload request frontier drift",
    )

    return {
        "invocation_review": deepcopy(invocation),
        "preservation_result_review": deepcopy(preservation),
    }


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "repair_lineage": {
            "first_spent_request_sha256": FIRST_SPENT_REQUEST_SHA256,
            "second_spent_request_sha256": SECOND_SPENT_REQUEST_SHA256,
            "held_superseded_request_sha256": HELD_SUPERSEDED_REQUEST_SHA256,
            "held_superseded_request_authorization_text_sha256": (
                HELD_SUPERSEDED_REQUEST_AUTHORIZATION_TEXT_SHA256
            ),
            "held_superseded_request_authorized": True,
            "held_superseded_request_preclaim": True,
            "held_superseded_request_attempt_consumed": False,
            "held_superseded_request_reusable": False,
            "held_superseded_request_supersede_reason": (
                "no_offload_parent_receipt_schema_vs_invocation_validator_mismatch"
            ),
            "first_spent_attempt_sha256": FIRST_SPENT_ATTEMPT_SHA256,
            "second_spent_attempt_sha256": SECOND_SPENT_ATTEMPT_SHA256,
            "first_spent_request_reusable": False,
            "second_spent_request_reusable": False,
            "first_spent_attempt_reusable": False,
            "second_spent_attempt_reusable": False,
            "first_preservation_receipt_file_sha256": (
                FIRST_PRESERVATION_RECEIPT_FILE_SHA256
            ),
            "second_preservation_receipt_file_sha256": (
                SECOND_PRESERVATION_RECEIPT_FILE_SHA256
            ),
            "second_preservation_receipt_logical_sha256": (
                SECOND_PRESERVATION_RECEIPT_LOGICAL_SHA256
            ),
            "first_failure_class": "v8_input_embedding_cpu_vs_encoded_cuda_device_mismatch",
            "second_failure_class": "qwen35_gated_delta_triton_cpu_pointer",
            "both_failed_attempts_archived": True,
            "prior_archives_must_remain_unchanged": True,
            "fresh_attempt_required": True,
            "no_offload_parent_generation_required": True,
            "no_offload_parent_receipt_schema_bound": True,
            "inference_safe_placement_receipt_required": True,
            "single_gpu_cuda0_placement_required": True,
            "cpu_disk_meta_parameter_offload_allowed": False,
        },
        "source_binding": {
            "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
            "invocation_review_source_sha256": INVOCATION_REVIEW_SOURCE_SHA256,
            "invocation_source_sha256": (
                "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
            ),
            "preservation_result_review_git_blob": (
                PRESERVATION_RESULT_REVIEW_GIT_BLOB
            ),
            "preservation_result_review_source_sha256": (
                PRESERVATION_RESULT_REVIEW_SOURCE_SHA256
            ),
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
            "exact_no_offload_authorization_request_source_reviewed",
            "pair06_no_offload_baseline_specific_operator_authorization_accepted",
            "exact_no_offload_invocation_source_reviewed_and_canonical",
            "no_offload_parent_receipt_schema_bound",
            "inference_safe_placement_receipt_required",
            "exact_current_main_required",
            "both_prior_failed_attempts_archived",
            "fresh_baseline_arm_root",
            "fresh_v8_environment_and_17_assets",
            "single_gpu_cuda0_placement_required",
            "cpu_disk_meta_parameter_offload_forbidden",
            "preclaim_exact_frozen_worktree_materialization",
            "create_only_single_use_attempt_marker",
            "marker_sha256_bound_as_attempt_id",
            "authority_rechecked_after_claim",
            "authority_rechecked_before_each_inference",
            "private_child_process_group",
            "legacy_ollama_not_started_or_contacted",
            "durable_execution_result_before_worktree_cleanup",
            "success_only_owned_worktree_cleanup",
            "durable_cleanup_closeout",
        ],
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "request_validation_performs_host_io": False,
        "next_gate": NEXT_GATE,
    }


def build_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request() -> bytes:
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


def validate_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request()
    _require(payload == expected, "request bytes differ from fixed no-offload proposal")
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_contract() -> dict[str, Any]:
    result = validate_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request(
        build_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request()
    )
    return {
        **result,
        "pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_implemented": True,
        "pair06_no_offload_baseline_specific_authorization_accepted": False,
        "pair06_no_offload_baseline_execution_authorized": False,
        "pair06_no_offload_baseline_execution_performed": False,
        "first_spent_request_reusable": False,
        "second_spent_request_reusable": False,
        "first_spent_attempt_reusable": False,
        "second_spent_attempt_reusable": False,
        "held_superseded_request_reusable": False,
        "held_superseded_request_attempt_consumed": False,
        "receipt_schema_binding_repaired": True,
        "inference_safe_placement_receipt_required": True,
        "matching_request_digest_grants_authority": False,
        "request": _request_record(),
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8NoOffloadReceiptBoundBaselineExecutionAuthorizationRequestHold(NEXT_GATE)
