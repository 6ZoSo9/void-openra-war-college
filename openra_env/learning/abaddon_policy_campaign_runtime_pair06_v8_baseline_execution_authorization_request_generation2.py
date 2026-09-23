"""Fixed proposal-only request for one pair-06 V8 baseline game execution.

Matching these bytes never grants authority. This request defines the exact
scope that may later be explicitly authorized after the reviewed one-shot
invocation is canonical.

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
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_source_binding_review_generation2
    as invocation_review,
)

REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-execution-authorization-request-validation.v1"
)

INVOCATION_REVIEW_GIT_BLOB = "c01fbd1426b523890fd5a6dbc1f24556abdc9a25"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "419e0a8e8fce1704c67ec2f1cc89da16b01dd103164033535cca6d87ac545806"
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

REQUIRED_RUNTIME_GATES = (
    "exact_authorization_request_source_reviewed",
    "pair06_baseline_specific_operator_authorization_accepted",
    "exact_attempt_invocation_source_reviewed_and_canonical",
    "exact_current_main_required",
    "exact_v8_parent_python",
    "exact_proto_game_child_python",
    "fresh_v8_environment_and_17_assets",
    "revocation_sentinel_absent",
    "preclaim_empty_runs_root",
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
)

FALSE_AUTHORITY_FIELDS = (
    "pair06_baseline_specific_authorization_accepted",
    "pair06_baseline_execution_authorized",
    "pair06_baseline_execution_performed",
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

NEXT_GATE = "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"


class Pair06V8BaselineExecutionAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineExecutionAuthorizationRequestHold(message)


def _reviewed_invocation() -> dict[str, Any]:
    reviewed = invocation_review.pair06_v8_baseline_attempt_invocation_review_contract()
    _require(
        reviewed.get("pair06_v8_baseline_attempt_invocation_reviewed") is True,
        "pair06 baseline invocation not reviewed",
    )
    _require(
        reviewed.get("pair_slot") == PAIR_SLOT
        and reviewed.get("arm") == ARM
        and reviewed.get("held_out") is False,
        "pair06 baseline invocation scope drift",
    )
    _require(
        reviewed.get("maximum_attempts") == 1
        and reviewed.get("automatic_retry") is False,
        "pair06 one-shot cardinality drift",
    )
    _require(
        reviewed.get("attempt_marker_create_only") is True
        and reviewed.get("attempt_marker_precedes_model_load_and_child_spawn") is True
        and reviewed.get("postclaim_reset_or_resume_available") is False,
        "pair06 attempt-consumption boundary drift",
    )
    _require(
        reviewed.get("explicit_authorization_required") is True
        and reviewed.get("pair06_baseline_specific_authorization_accepted") is False,
        "pair06 invocation prematurely authorized",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
        "pair06 authorization-request frontier drift",
    )
    return deepcopy(reviewed)


def _request_record() -> dict[str, Any]:
    reviewed = _reviewed_invocation()
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_binding": {
            "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
            "invocation_review_source_sha256": INVOCATION_REVIEW_SOURCE_SHA256,
            "invocation_source_sha256": reviewed["invocation_source_sha256"],
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
        "runtime_architecture": {
            "v8_parent_process": True,
            "proto_grpc_game_child_process": True,
            "separate_virtualenv_site_packages_preserved": True,
            "inherited_unix_socketpair_only": True,
            "private_child_process_group": True,
            "legacy_ollama_started": False,
            "legacy_ollama_contacted": False,
        },
        "evidence_order": {
            "preclaim_preparation_first": True,
            "durable_attempt_marker_before_model_load_or_child_spawn": True,
            "durable_execution_result_before_worktree_cleanup": True,
            "durable_cleanup_closeout_after_successful_cleanup": True,
            "runs_preserved": True,
        },
        "required_runtime_gates": list(REQUIRED_RUNTIME_GATES),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "request_validation_performs_host_io": False,
        "next_gate": NEXT_GATE,
    }


def build_pair06_v8_baseline_execution_authorization_request() -> bytes:
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


def validate_pair06_v8_baseline_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v8_baseline_execution_authorization_request()
    _require(payload == expected, "request bytes differ from fixed proposal")
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair06_v8_baseline_execution_authorization_request_contract() -> dict[str, Any]:
    result = validate_pair06_v8_baseline_execution_authorization_request(
        build_pair06_v8_baseline_execution_authorization_request()
    )
    return {
        **result,
        "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
        "invocation_review_source_sha256": INVOCATION_REVIEW_SOURCE_SHA256,
        "pair06_baseline_specific_authorization_accepted": False,
        "pair06_baseline_execution_authorized": False,
        "pair06_baseline_execution_performed": False,
        "matching_request_digest_grants_authority": False,
        "request": _request_record(),
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineExecutionAuthorizationRequestHold(NEXT_GATE)
