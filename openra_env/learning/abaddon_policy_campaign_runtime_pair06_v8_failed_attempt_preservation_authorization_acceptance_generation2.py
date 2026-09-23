"""Audit-only acceptance of exact pair-06 V8 failed-attempt preservation authority.

This record binds the user's explicit preservation authorization to the exact
consumed attempt and exact canonical War College main head. It is intentionally
kept off canonical main until after preservation because merging it would
change the main SHA the user authorized.

This module does not invoke preservation, remove worktrees, rename evidence,
retry runtime, load a model, run inference, execute a game, train, promote,
deploy, mutate VOID-chain state, or touch wallets/funds.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-authorization-acceptance-contract.v1"
)

PRESERVATION_REVIEW_GIT_BLOB = "0d1cc869cfe906cfe6f0ca841cefa76d6a21c100"
PRESERVATION_GIT_BLOB = "ff4de10454fc958d5ca459bd7a3eea6a27a17e64"
PRESERVATION_SOURCE_SHA256 = (
    "05f11516233d7c602244878e8aa066f1a8aae7ea59e3c0641f0cbe494f518c26"
)

AUTHORIZED_MAIN_HEAD = "344f6e146e839582aa600b11ca5d1c31e46b124a"
AUTHORIZED_ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
AUTHORIZATION_TEXT_SHA256 = (
    "9830b62787aa5c8fb84af7c0394b62aec25d6154e53cb2b339af7bb38826ecbb"
)
AUTHORIZATION_TEXT_BYTES = 600

NEXT_GATE = "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_AUTHORIZED"


class Pair06V8FailedAttemptPreservationAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8FailedAttemptPreservationAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_preservation() -> dict[str, Any]:
    reviewed = preservation_review.pair06_v8_failed_attempt_preservation_review_contract()
    _require(
        reviewed.get("pair06_v8_failed_attempt_preservation_reviewed") is True,
        "pair06 failed-attempt preservation not reviewed",
    )
    _require(
        reviewed.get("attempt_marker_sha256")
        == AUTHORIZED_ATTEMPT_MARKER_SHA256,
        "pair06 failed-attempt marker drift",
    )
    _require(
        reviewed.get("failed_attempt_deletion_authorized") is False,
        "pair06 failed-attempt deletion unexpectedly authorized",
    )
    _require(
        reviewed.get("runtime_retry_authorized") is False
        and reviewed.get("automatic_retry") is False,
        "pair06 preservation review unexpectedly authorizes retry",
    )
    _require(
        reviewed.get("runtime_execution_performed") is False
        and reviewed.get("model_inference_performed") is False
        and reviewed.get("game_execution_performed") is False,
        "pair06 preservation review crossed execution boundary",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
        "pair06 preservation authorization frontier drift",
    )
    return deepcopy(reviewed)


def pair06_v8_failed_attempt_preservation_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_preservation()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_review_git_blob": PRESERVATION_REVIEW_GIT_BLOB,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "pair06_v8_failed_attempt_preservation_authorization_accepted": True,
        "authorization_record_kind": "explicit_user_authorization",
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_attempt_marker_sha256": AUTHORIZED_ATTEMPT_MARKER_SHA256,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "pair_slot": 6,
        "arm": "baseline",
        "failed_attempt_preservation_authorized": True,
        "non_force_worktree_cleanup_authorized": True,
        "atomic_evidence_archive_authorized": True,
        "preservation_receipt_creation_authorized": True,
        "failed_attempt_deletion_authorized": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
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
        "preservation_performed": False,
        "reviewed_preservation": reviewed,
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
    }


def preserve_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8FailedAttemptPreservationAuthorizationAcceptanceHold(NEXT_GATE)
