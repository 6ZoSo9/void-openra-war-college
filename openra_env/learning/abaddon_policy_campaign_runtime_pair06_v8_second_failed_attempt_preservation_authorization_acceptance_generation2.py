"""Audit-only acceptance of exact second pair-06 V8 failed-attempt preservation authority.

This record binds the user's explicit preservation authorization to the exact
second consumed attempt and exact canonical War College main head. It remains
off canonical main until after preservation because merging it would change the
main SHA the user authorized.

This module does not invoke preservation, remove worktrees, rename evidence,
retry runtime, load a model, run inference, execute a game, train, promote,
deploy, mutate VOID-chain state, or touch wallets/funds.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-preservation-authorization-acceptance-contract.v1"
)

PRESERVATION_REVIEW_GIT_BLOB = "e8268c5b14c38600f9f08a5f798ba51122a85abe"
PRESERVATION_GIT_BLOB = "653521100d1b88f84e16cb1a233b3a9da48fee17"
PRESERVATION_SOURCE_SHA256 = (
    "888228244f81370f0f1199e2c5f9de7a6281da178f3e119bff93d2718adbcd4c"
)

AUTHORIZED_MAIN_HEAD = "88edd6d4b69e6d6869b74dca85df3fc3b0bd5a23"
AUTHORIZED_ATTEMPT_MARKER_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)
AUTHORIZED_ARCHIVE_NAME = "baseline-20260923T235031Z-446d8f92"
AUTHORIZATION_TEXT_SHA256 = (
    "5c2f8ddd1893a88bf706666ad5482b236bd4a5b4e6a0c8dfa52f6948ac2561fc"
)
AUTHORIZATION_TEXT_BYTES = 745

NEXT_GATE = "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_AUTHORIZED"


class Pair06V8SecondFailedAttemptPreservationAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8SecondFailedAttemptPreservationAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_preservation() -> dict[str, Any]:
    reviewed = (
        preservation_review
        .pair06_v8_second_failed_attempt_preservation_review_contract()
    )
    _require(
        reviewed.get("pair06_v8_second_failed_attempt_preservation_reviewed")
        is True,
        "second pair06 failed-attempt preservation not reviewed",
    )
    _require(
        reviewed.get("attempt_marker_sha256")
        == AUTHORIZED_ATTEMPT_MARKER_SHA256,
        "second pair06 failed-attempt marker drift",
    )
    _require(
        reviewed.get("archive_name") == AUTHORIZED_ARCHIVE_NAME,
        "second pair06 failed-attempt archive name drift",
    )
    _require(
        reviewed.get("prior_failed_attempt_archive_revalidated_before_and_after")
        is True,
        "prior pair06 archive revalidation invariant missing",
    )
    _require(
        reviewed.get("failed_attempt_deletion_authorized") is False,
        "second pair06 failed-attempt deletion unexpectedly authorized",
    )
    _require(
        reviewed.get("runtime_retry_authorized") is False
        and reviewed.get("automatic_retry") is False,
        "second pair06 preservation review unexpectedly authorizes retry",
    )
    _require(
        reviewed.get("runtime_execution_performed") is False
        and reviewed.get("model_inference_performed") is False
        and reviewed.get("game_execution_performed") is False,
        "second pair06 preservation review crossed execution boundary",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
        "second pair06 preservation authorization frontier drift",
    )
    return deepcopy(reviewed)


def pair06_v8_second_failed_attempt_preservation_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_preservation()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_review_git_blob": PRESERVATION_REVIEW_GIT_BLOB,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "pair06_v8_second_failed_attempt_preservation_authorization_accepted": True,
        "authorization_record_kind": "explicit_user_authorization",
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_attempt_marker_sha256": AUTHORIZED_ATTEMPT_MARKER_SHA256,
        "authorized_archive_name": AUTHORIZED_ARCHIVE_NAME,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "pair_slot": 6,
        "arm": "baseline",
        "failed_attempt_preservation_authorized": True,
        "non_force_worktree_cleanup_authorized": True,
        "atomic_evidence_archive_authorized": True,
        "prior_failed_attempt_revalidation_authorized": True,
        "preservation_receipt_creation_authorized": True,
        "failed_attempt_deletion_authorized": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
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
        "preservation_performed": False,
        "reviewed_preservation": reviewed,
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
    }


def preserve_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8SecondFailedAttemptPreservationAuthorizationAcceptanceHold(
        NEXT_GATE
    )
