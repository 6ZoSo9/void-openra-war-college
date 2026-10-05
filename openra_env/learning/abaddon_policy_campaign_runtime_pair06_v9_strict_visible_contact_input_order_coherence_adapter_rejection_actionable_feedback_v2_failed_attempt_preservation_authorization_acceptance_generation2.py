"""Explicit authorization acceptance for the consumed Pair-06 V9 actionable-feedback V2 failed-attempt preservation.

This source-only contract binds the exact reviewed preservation request, the
exact user authorization text, and canonical main head/tree at authorization
time. It accepts authority only for the reviewed preservation operation.

No host I/O or preservation is performed by contract inspection. Runtime retry,
new execution, model/game execution, training, deployment, VOID-chain mutation,
wallet/funds action, and scheduler mutation remain unauthorized.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_requirements_source_binding_review_generation2
    as requirements_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_generation2
    as preservation,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-authorization-acceptance-contract.v1"
)

REQUIREMENTS_REVIEW_GIT_BLOB = "f1074bd076c09f48c59b4de62079806c4daa1600"

REVIEWED_REQUEST_SHA256 = (
    "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
)
REVIEWED_REQUEST_BYTES = 3288

AUTHORIZATION_TEXT = (
    "I explicitly authorize preservation of the consumed Pair-06 V9 "
    "actionable-feedback V2 failed attempt under the reviewed preservation "
    "request and the boundaries defined by merged PR #374."
)
AUTHORIZATION_TEXT_SHA256 = (
    "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
)
AUTHORIZATION_TEXT_BYTES = 186

CANONICAL_MAIN_HEAD_AT_AUTHORIZATION = (
    "000a8a01c29a8b42e91cb30f935ef63b72407f02"
)
CANONICAL_MAIN_TREE_AT_AUTHORIZATION = (
    "49b201ba723bcd4b8cab162f2d2d954534da6621"
)

ATTEMPT_MARKER_SHA256 = (
    "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
)
ATTEMPT_MARKER_BYTES = 2208
WARM_START_SHA256 = (
    "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
)
TRAJECTORY_SHA256 = (
    "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
)

ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v8-generation2/generation2/"
    "pair-06/failed-attempts/"
    "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
)
PRESERVATION_RECEIPT_PATH = (
    ARCHIVE_PATH + "-preservation-receipt.json"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "authorized_host_only_pair06_v9_strict_visible_contact_input_order_"
    "coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_execution"
)


class Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceHold(
            message
        )


def _validated_requirements() -> dict[str, Any]:
    out = (
        requirements_review
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_reviewed"
        )
        is True,
        "V2 preservation acceptance requirements review missing",
    )
    _require(
        out.get("reviewed_request_sha256") == REVIEWED_REQUEST_SHA256
        and out.get("reviewed_request_bytes") == REVIEWED_REQUEST_BYTES,
        "V2 reviewed preservation request identity drift",
    )
    _require(
        out.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256
        and out.get("attempt_marker_bytes") == ATTEMPT_MARKER_BYTES
        and out.get("warm_start_sha256") == WARM_START_SHA256
        and out.get("trajectory_sha256") == TRAJECTORY_SHA256,
        "V2 preservation evidence identity drift",
    )
    _require(
        out.get("archive_path") == ARCHIVE_PATH
        and out.get("preservation_receipt_path") == PRESERVATION_RECEIPT_PATH,
        "V2 preservation archive scope drift",
    )
    _require(
        out.get("exact_user_authorization_text_required") is True
        and out.get("authorization_text_sha256_binding_required") is True
        and out.get("authorization_text_byte_length_binding_required") is True
        and out.get("canonical_main_head_binding_required") is True
        and out.get("canonical_main_tree_binding_required") is True,
        "V2 preservation authorization binding requirements drift",
    )
    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _validated_requirements()

    raw = AUTHORIZATION_TEXT.encode("utf-8")
    _require(
        len(raw) == AUTHORIZATION_TEXT_BYTES,
        "V2 preservation authorization text byte length drift",
    )
    _require(
        hashlib.sha256(raw).hexdigest() == AUTHORIZATION_TEXT_SHA256,
        "V2 preservation authorization text SHA-256 drift",
    )

    _require(
        preservation.ARCHIVE_ROOT.as_posix() == ARCHIVE_PATH
        and preservation.PRESERVATION_RECEIPT.as_posix()
        == PRESERVATION_RECEIPT_PATH,
        "V2 preservation implementation target drift",
    )
    _require(
        preservation.ATTEMPT_MARKER_SHA256 == ATTEMPT_MARKER_SHA256
        and preservation.ATTEMPT_MARKER_BYTES == ATTEMPT_MARKER_BYTES
        and preservation.WARM_START_SHA256 == WARM_START_SHA256
        and preservation.TRAJECTORY_SHA256 == TRAJECTORY_SHA256,
        "V2 preservation implementation evidence drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "requirements_review_git_blob": REQUIREMENTS_REVIEW_GIT_BLOB,
        "reviewed_request_sha256": REVIEWED_REQUEST_SHA256,
        "reviewed_request_bytes": REVIEWED_REQUEST_BYTES,
        "authorization_text": AUTHORIZATION_TEXT,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "canonical_main_head_at_authorization": (
            CANONICAL_MAIN_HEAD_AT_AUTHORIZATION
        ),
        "canonical_main_tree_at_authorization": (
            CANONICAL_MAIN_TREE_AT_AUTHORIZATION
        ),
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "attempt_marker_bytes": ATTEMPT_MARKER_BYTES,
        "warm_start_sha256": WARM_START_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "archive_path": ARCHIVE_PATH,
        "preservation_receipt_path": PRESERVATION_RECEIPT_PATH,
        "preservation_authorization_accepted": True,
        "preservation_authorized": True,
        "filesystem_mutation_authorized": True,
        "git_worktree_mutation_authorized": True,
        "archive_rename_authorized": True,
        "preservation_receipt_creation_authorized": True,
        "authority_scope_exact_reviewed_preservation_only": True,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "validated_requirements": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorized_preservation_call() -> dict[str, Any]:
    pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    return {
        "preservation_authorized": True,
        "confirm": preservation.CONFIRM_TOKEN,
    }


def execute_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceHold(
        NEXT_GATE
    )
