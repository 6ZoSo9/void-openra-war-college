"""Proposal-only request for one repaired pair-06 V8 baseline execution.

This request is distinct from the spent request
a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae.
It binds the archived consumed attempt and the offload-safe repaired invocation
chain. Matching these bytes never grants authority.

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
    abaddon_policy_campaign_runtime_pair06_v8_baseline_execution_authorization_request_source_binding_review_generation2
    as base_request_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_result_source_binding_review_generation2
    as preservation_result_review,
)

REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-repaired-baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-repaired-baseline-execution-authorization-request-validation.v1"
)

BASE_REQUEST_REVIEW_GIT_BLOB = "1be69f86e01f45f088a11e519a083e1161b4a939"
BASE_REQUEST_SOURCE_SHA256 = (
    "b9958a25d2bf83968a647fd00d0cf9e4f783fdba7267550fc54fc2845c429548"
)
PRESERVATION_RESULT_REVIEW_GIT_BLOB = "0557b777c42e63237eb1b012f233ddf4b9d386a7"

SPENT_REQUEST_SHA256 = (
    "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae"
)
SPENT_ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
PRESERVATION_RECEIPT_LOGICAL_SHA256 = (
    "29af061dbf3362eb2d5e79b0c94cd8f2be7d89d7dc271f72cf1fbd775913094f"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "d32cc7779fb1570ac2085031e296817059ce51d35de43ca3875becf9d032ccff"
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
    "pair06_repaired_baseline_specific_authorization_accepted",
    "pair06_repaired_baseline_execution_authorized",
    "pair06_repaired_baseline_execution_performed",
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

NEXT_GATE = "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"


class Pair06V8RepairedBaselineExecutionAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8RepairedBaselineExecutionAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    base = base_request_review.pair06_v8_baseline_execution_authorization_request_review_contract()
    preservation = preservation_result_review.pair06_v8_failed_attempt_preservation_result_review_contract()

    _require(
        base.get("pair06_v8_baseline_execution_authorization_request_reviewed") is True,
        "repaired pair06 base request not reviewed",
    )
    _require(
        base.get("request_source_sha256") == BASE_REQUEST_SOURCE_SHA256,
        "repaired pair06 base request source drift",
    )
    _require(
        base.get("pair_slot") == PAIR_SLOT
        and base.get("arm") == ARM
        and base.get("held_out") is False,
        "repaired pair06 base request scope drift",
    )
    _require(
        base.get("maximum_attempts") == 1
        and base.get("maximum_automatic_retries") == 0,
        "repaired pair06 base request cardinality drift",
    )
    _require(
        base.get("matching_request_digest_grants_authority") is False,
        "repaired pair06 base request digest unexpectedly grants authority",
    )

    _require(
        preservation.get("pair06_v8_failed_attempt_preservation_result_reviewed") is True,
        "pair06 preservation result not reviewed",
    )
    _require(
        preservation.get("attempt_marker_sha256") == SPENT_ATTEMPT_MARKER_SHA256,
        "pair06 spent attempt marker drift",
    )
    _require(preservation.get("failed_attempt_archived") is True, "pair06 spent attempt not archived")
    _require(preservation.get("failed_attempt_deleted") is False, "pair06 spent attempt deleted")
    _require(
        preservation.get("fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt") is True,
        "pair06 fresh baseline root not available",
    )
    _require(preservation.get("runtime_retry_authorized") is False, "pair06 preservation unexpectedly authorizes retry")
    _require(preservation.get("automatic_retry") is False, "pair06 preservation automatic retry drift")
    _require(
        preservation.get("next_gate")
        == "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
        "pair06 repaired request frontier drift",
    )
    return {
        "base_request_review": deepcopy(base),
        "preservation_result_review": deepcopy(preservation),
    }


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "repair_lineage": {
            "spent_request_sha256": SPENT_REQUEST_SHA256,
            "spent_attempt_marker_sha256": SPENT_ATTEMPT_MARKER_SHA256,
            "spent_attempt_reusable": False,
            "failure_class": "v8_input_embedding_cpu_vs_encoded_cuda_device_mismatch",
            "failed_attempt_archived": True,
            "preservation_receipt_logical_sha256": PRESERVATION_RECEIPT_LOGICAL_SHA256,
            "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
            "offload_safe_generate_binding_required": True,
            "hard_coded_cuda_input_transfer_allowed": False,
            "fresh_attempt_required": True,
        },
        "source_binding": {
            "base_request_review_git_blob": BASE_REQUEST_REVIEW_GIT_BLOB,
            "base_request_source_sha256": BASE_REQUEST_SOURCE_SHA256,
            "preservation_result_review_git_blob": PRESERVATION_RESULT_REVIEW_GIT_BLOB,
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
            "exact_repaired_authorization_request_source_reviewed",
            "pair06_repaired_baseline_specific_operator_authorization_accepted",
            "exact_current_main_required",
            "fresh_baseline_arm_root",
            "fresh_v8_environment_and_17_assets",
            "offload_safe_generate_adapter_reviewed_and_bound",
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


def build_pair06_v8_repaired_baseline_execution_authorization_request() -> bytes:
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


def validate_pair06_v8_repaired_baseline_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v8_repaired_baseline_execution_authorization_request()
    _require(payload == expected, "request bytes differ from fixed repaired proposal")
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair06_v8_repaired_baseline_execution_authorization_request_contract() -> dict[str, Any]:
    result = validate_pair06_v8_repaired_baseline_execution_authorization_request(
        build_pair06_v8_repaired_baseline_execution_authorization_request()
    )
    return {
        **result,
        "pair06_v8_repaired_baseline_execution_authorization_request_implemented": True,
        "pair06_repaired_baseline_specific_authorization_accepted": False,
        "pair06_repaired_baseline_execution_authorized": False,
        "pair06_repaired_baseline_execution_performed": False,
        "spent_request_reusable": False,
        "spent_attempt_reusable": False,
        "matching_request_digest_grants_authority": False,
        "request": _request_record(),
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RepairedBaselineExecutionAuthorizationRequestHold(NEXT_GATE)
