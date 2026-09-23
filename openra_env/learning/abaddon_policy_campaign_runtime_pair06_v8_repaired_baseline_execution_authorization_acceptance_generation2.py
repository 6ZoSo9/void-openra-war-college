"""Audit-only acceptance of one exact repaired pair-06 V8 baseline execution.

This record binds the user's explicit authorization to the reviewed repaired
request and exact canonical War College main head. It is intentionally kept
off canonical main until after execution because merging it would change the
main SHA the user authorized.

This module does not create an attempt marker, load a model, run inference,
execute OpenRA, retry a spent attempt, train, promote, deploy, mutate VOID-chain
state, or touch wallets/funds.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_repaired_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-repaired-baseline-execution-authorization-acceptance-contract.v1"
)

REQUEST_REVIEW_GIT_BLOB = "43c11accf9ce7490f13d84c1d0d9a50dfc6bbd5f"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "c367dda58dba309be78326a645ebc8be2dba185c5eb210caeb4463fa2d6652f5"
)
AUTHORIZED_REQUEST_SHA256 = (
    "31c0069869915eb01221d7ea0aa867c0517df0a702eeff58ca69f70dec07a410"
)
AUTHORIZED_MAIN_HEAD = "cb022ce0d32455c2f94f3ff2460bb88d3fb5c08c"
AUTHORIZATION_TEXT_SHA256 = (
    "80a422164e3e1a51194d32ed06a2e15b5396711be7640fd0b03b57dddba6cc55"
)
AUTHORIZATION_TEXT_BYTES = 692

SPENT_REQUEST_SHA256 = (
    "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae"
)
SPENT_ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
MAXIMUM_ATTEMPTS = 1
MAXIMUM_AUTOMATIC_RETRIES = 0

NEXT_GATE = "PAIR06_V8_REPAIRED_BASELINE_AUTHORIZED_INVOCATION_READY"


class Pair06V8RepairedBaselineExecutionAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8RepairedBaselineExecutionAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    reviewed = (
        request_review
        .pair06_v8_repaired_baseline_execution_authorization_request_review_contract()
    )
    _require(
        reviewed.get(
            "pair06_v8_repaired_baseline_execution_authorization_request_reviewed"
        )
        is True,
        "repaired pair06 authorization request not reviewed",
    )
    _require(
        reviewed.get("request_sha256") == AUTHORIZED_REQUEST_SHA256,
        "repaired pair06 authorization request digest drift",
    )
    _require(
        reviewed.get("request_bytes_sha256") == AUTHORIZED_REQUEST_SHA256,
        "repaired pair06 request byte digest drift",
    )
    _require(
        reviewed.get("pair_slot") == PAIR_SLOT
        and reviewed.get("arm") == ARM
        and reviewed.get("held_out") is False,
        "repaired pair06 authorization scope drift",
    )
    _require(
        reviewed.get("maximum_attempts") == MAXIMUM_ATTEMPTS
        and reviewed.get("maximum_automatic_retries")
        == MAXIMUM_AUTOMATIC_RETRIES,
        "repaired pair06 authorization cardinality drift",
    )
    _require(
        reviewed.get("spent_request_reusable") is False
        and reviewed.get("spent_attempt_reusable") is False,
        "spent pair06 lineage became reusable",
    )
    _require(
        reviewed.get("offload_safe_generate_binding_required") is True,
        "offload-safe repaired binding requirement missing",
    )
    _require(
        reviewed.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly self-authorizes",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
        "repaired pair06 authorization frontier drift",
    )
    return deepcopy(reviewed)


def pair06_v8_repaired_baseline_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "pair06_v8_repaired_baseline_execution_authorization_accepted": True,
        "authorization_record_kind": "explicit_user_authorization",
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "spent_request_sha256": SPENT_REQUEST_SHA256,
        "spent_attempt_marker_sha256": SPENT_ATTEMPT_MARKER_SHA256,
        "spent_request_reusable": False,
        "spent_attempt_reusable": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "maximum_attempts": MAXIMUM_ATTEMPTS,
        "maximum_automatic_retries": MAXIMUM_AUTOMATIC_RETRIES,
        "fresh_attempt_required": True,
        "offload_safe_generate_binding_required": True,
        "baseline_execution_authorized": True,
        "runtime_load_authorized": True,
        "model_inference_authorized": True,
        "game_execution_authorized": True,
        "child_spawn_authorized": True,
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
        "automatic_retry": False,
        "attempt_consumed": False,
        "game_execution_performed": False,
        "reviewed_request": reviewed,
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RepairedBaselineExecutionAuthorizationAcceptanceHold(NEXT_GATE)
