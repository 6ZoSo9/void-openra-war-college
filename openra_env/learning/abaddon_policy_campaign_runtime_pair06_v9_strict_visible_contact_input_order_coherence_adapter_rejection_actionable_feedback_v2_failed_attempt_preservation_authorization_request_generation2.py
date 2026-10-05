"""Proposal-only authorization request for actionable-feedback V2 failed-attempt preservation.

This request binds the exact reviewed Pair-06 V9 actionable-feedback V2 failed
attempt preservation gate to the exact consumed marker, exact run artifacts,
and exact archive destination.

It is a proposal only. Matching request bytes or digest grant no filesystem
mutation, Git worktree mutation, archive rename, receipt creation, runtime
retry, model/game execution, training, deployment, chain, wallet/funds, or
scheduler authority.

General source-work authorization is explicitly not preservation authorization.
A later acceptance requires fresh explicit user authorization for this exact
preservation request.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_generation2
    as preservation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-authorization-request-validation.v1"
)

PRESERVATION_STACK_HEAD = "ee6a45530e6982771cfc3ec92e838fa224885cc3"
PRESERVATION_GIT_BLOB = "92981d23b580059fd3419cfe95daea561aab6add"
PRESERVATION_REVIEW_GIT_BLOB = "62f21456cbd358cf8cff9d621d4530485b9531f5"

ATTEMPT_MARKER_SHA256 = (
    "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
)
ATTEMPT_MARKER_BYTES = 2208
WARM_START_SHA256 = (
    "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
)
WARM_START_BYTES = 229255
TRAJECTORY_SHA256 = (
    "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
)
TRAJECTORY_BYTES = 58075

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "preservation_authorization_accepted",
    "preservation_authorized",
    "filesystem_mutation_authorized",
    "git_worktree_mutation_authorized",
    "archive_rename_authorized",
    "preservation_receipt_creation_authorized",
    "runtime_retry_authorized",
    "execution_request_opened",
    "runtime_load_authorized",
    "model_inference_authorized",
    "game_execution_authorized",
    "training_authorized",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
    "scheduler_mutation_authorized",
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_authorization_request_review"
)


class Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestHold(
            message
        )


def _dependencies() -> dict[str, Any]:
    reviewed = (
        preservation_review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract()
    )

    _require(
        reviewed.get(
            "pair06_v9_actionable_feedback_v2_failed_attempt_preservation_reviewed"
        )
        is True,
        "actionable-feedback V2 failed-attempt preservation review missing",
    )
    _require(
        reviewed.get("preservation_git_blob") == PRESERVATION_GIT_BLOB,
        "actionable-feedback V2 preservation source identity drift",
    )
    _require(
        reviewed.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256
        and reviewed.get("attempt_marker_bytes") == ATTEMPT_MARKER_BYTES
        and reviewed.get("warm_start_sha256") == WARM_START_SHA256
        and reviewed.get("warm_start_bytes") == WARM_START_BYTES
        and reviewed.get("trajectory_sha256") == TRAJECTORY_SHA256
        and reviewed.get("trajectory_bytes") == TRAJECTORY_BYTES,
        "actionable-feedback V2 preservation evidence identity drift",
    )
    _require(
        reviewed.get("non_force_worktree_removal_only") is True
        and reviewed.get("atomic_baseline_archive_rename_reviewed") is True
        and reviewed.get("evidence_inode_preservation_reviewed") is True
        and reviewed.get("create_only_preservation_receipt_reviewed") is True,
        "actionable-feedback V2 preservation safety invariant drift",
    )
    _require(
        reviewed.get("preservation_authorization_accepted") is False
        and reviewed.get("preservation_performed") is False
        and reviewed.get("runtime_retry_authorized") is False
        and reviewed.get("new_execution_request_opened") is False,
        "actionable-feedback V2 preservation review unexpectedly grants authority",
    )
    _require(
        reviewed.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
            "PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
        ),
        "actionable-feedback V2 preservation request frontier drift",
    )

    return {"preservation_review": deepcopy(reviewed)}


def _request_record() -> dict[str, Any]:
    reviewed = _dependencies()["preservation_review"]

    record = {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_binding": {
            "preservation_stack_head": PRESERVATION_STACK_HEAD,
            "preservation_git_blob": PRESERVATION_GIT_BLOB,
            "preservation_review_git_blob": PRESERVATION_REVIEW_GIT_BLOB,
            "canonical_main_must_be_bound_by_later_authorization": True,
        },
        "failed_attempt": {
            "pair_slot": 6,
            "arm": "baseline",
            "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
            "failure_class": reviewed["failure_class"],
            "failure_round": reviewed["failure_round"],
            "maximum_decision_attempts": reviewed["maximum_decision_attempts"],
            "terminal_feedback": reviewed["terminal_feedback"],
            "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
            "attempt_marker_bytes": ATTEMPT_MARKER_BYTES,
            "warm_start_sha256": WARM_START_SHA256,
            "warm_start_bytes": WARM_START_BYTES,
            "trajectory_sha256": TRAJECTORY_SHA256,
            "trajectory_bytes": TRAJECTORY_BYTES,
            "result_present": False,
            "closeout_present": False,
            "attempt_consumed": True,
            "attempt_reusable": False,
            "authorization_reusable": False,
        },
        "requested_preservation": {
            "archive_name": preservation.ARCHIVE_NAME,
            "archive_path": str(preservation.ARCHIVE_ROOT),
            "preservation_receipt_path": str(
                preservation.PRESERVATION_RECEIPT
            ),
            "exact_marker_and_run_artifacts_required": True,
            "exact_clean_detached_registered_worktrees_required": True,
            "engine_removed_before_source": True,
            "non_force_git_worktree_remove_only": True,
            "remaining_evidence_manifest_hashed": True,
            "atomic_baseline_archive_rename_requested": True,
            "marker_and_run_inode_preservation_required": True,
            "create_only_preservation_receipt_requested": True,
            "file_content_deletion_requested": False,
            "force_worktree_removal_requested": False,
            "runtime_retry_requested": False,
        },
        "authorization_boundary": {
            "preservation_authorization_requested": True,
            "fresh_explicit_user_authorization_required": True,
            "general_source_work_authorization_is_preservation_authorization": False,
            "matching_request_digest_grants_authority": False,
            "matching_request_bytes_grant_authority": False,
        },
    }

    for field in FALSE_AUTHORITY_FIELDS:
        record[field] = False

    return record


def preservation_authorization_request() -> dict[str, Any]:
    request = _request_record()
    raw = (
        json.dumps(
            request,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")

    _require(len(raw) <= MAX_REQUEST_BYTES, "V2 preservation request too large")

    return {
        "schema": VALIDATION_SCHEMA,
        "request": deepcopy(request),
        "request_sha256": hashlib.sha256(raw).hexdigest(),
        "request_bytes": len(raw),
        "preservation_authorization_requested": True,
        "preservation_authorization_accepted": False,
        "request_grants_authority": False,
        "host_io_performed": False,
        "filesystem_mutation_performed": False,
        "git_worktree_mutation_performed": False,
        "archive_rename_performed": False,
        "preservation_receipt_created": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "runtime_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestHold(
        NEXT_GATE
    )
