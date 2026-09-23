"""Audit record accepting one exact pair-06 V8 baseline execution authorization.

This record binds the user's explicit authorization to the already-reviewed
proposal and the exact canonical War College main head. It is intentionally
kept off canonical main until after execution because merging it would change
the main SHA the user authorized.

This module does not execute the game, create an attempt marker, load a model,
spawn a child, mutate worktrees, train, deploy, mutate VOID-chain state, or
touch wallets/funds.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-execution-authorization-acceptance-contract.v1"
)

REQUEST_REVIEW_GIT_BLOB = "5c4cec2809a10c1292085034bbcac363a8371ad1"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "96c492f6e798c932590bf5c2901856ee15c7c6b77eb265fcadc65a8366bd35d1"
)
AUTHORIZED_REQUEST_SHA256 = (
    "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae"
)
AUTHORIZED_MAIN_HEAD = "0635e319b811975caec8c60fd6eabedc892dc981"
AUTHORIZATION_TEXT_SHA256 = (
    "87aa4cb74c81e9d29242c7586aac014cef79fb43205fca0935dcb49b053e2195"
)
AUTHORIZATION_TEXT_BYTES = 441

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
MAXIMUM_ATTEMPTS = 1
MAXIMUM_AUTOMATIC_RETRIES = 0

NEXT_GATE = "PAIR06_V8_BASELINE_AUTHORIZED_INVOCATION_READY"


class Pair06V8BaselineExecutionAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineExecutionAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    reviewed = (
        request_review
        .pair06_v8_baseline_execution_authorization_request_review_contract()
    )
    _require(
        reviewed.get(
            "pair06_v8_baseline_execution_authorization_request_reviewed"
        )
        is True,
        "pair06 authorization request not reviewed",
    )
    _require(
        reviewed.get("request_sha256") == AUTHORIZED_REQUEST_SHA256,
        "pair06 authorization request digest drift",
    )
    _require(
        reviewed.get("pair_slot") == PAIR_SLOT
        and reviewed.get("arm") == ARM
        and reviewed.get("held_out") is False,
        "pair06 authorization scope drift",
    )
    _require(
        reviewed.get("maximum_attempts") == MAXIMUM_ATTEMPTS
        and reviewed.get("maximum_automatic_retries")
        == MAXIMUM_AUTOMATIC_RETRIES,
        "pair06 authorization cardinality drift",
    )
    _require(
        reviewed.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly self-authorizes",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
        "pair06 authorization acceptance frontier drift",
    )
    return deepcopy(reviewed)


def pair06_v8_baseline_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "pair06_v8_baseline_execution_authorization_accepted": True,
        "authorization_record_kind": "explicit_user_authorization",
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "maximum_attempts": MAXIMUM_ATTEMPTS,
        "maximum_automatic_retries": MAXIMUM_AUTOMATIC_RETRIES,
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
    raise Pair06V8BaselineExecutionAuthorizationAcceptanceHold(NEXT_GATE)
