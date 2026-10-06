"""Proposal-only authorization request for preservation of the second actionable-feedback V2 exhaustion.

This request binds the exact reviewed second-exhaustion preservation gate to
the consumed marker, exact run artifacts, predecessor preservation receipt,
and a distinct archive destination.

It grants no authority. Matching request bytes/digest and general source-work
authorization do not authorize filesystem mutation, worktree removal, archive
rename, receipt creation, runtime retry, model/game execution, training,
deployment, chain, wallet/funds, or scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_generation2
    as preservation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "second-exhaustion-preservation-authorization-request.v1"
)
VALIDATION_SCHEMA = REQUEST_SCHEMA + ".validation"

PRESERVATION_STACK_HEAD = "a9f3971045d78d6d51d14a233f80c83d5f69aadf"
PRESERVATION_GIT_BLOB = "963ebf0c9c7d8f3bae9143285cf781e8c6d92d24"
PRESERVATION_REVIEW_GIT_BLOB = "5275908efb8c8d01295e5fee5284f84c6e452698"

ATTEMPT_MARKER_SHA256 = (
    "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
)
ATTEMPT_MARKER_BYTES = 2208
WARM_START_SHA256 = (
    "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
)
WARM_START_BYTES = 229255
TRAJECTORY_SHA256 = (
    "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
)
TRAJECTORY_BYTES = 58075
PREDECESSOR_PRESERVATION_RECEIPT_SHA256 = (
    "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
)

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
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
    "scheduler_mutation_authorized",
)

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "PRESERVATION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "preservation_authorization_request_review"
)


class Pair06V9V2SecondExhaustionPreservationAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationAuthorizationRequestHold(
            message
        )


def _dependencies() -> dict[str, Any]:
    reviewed = (
        preservation_review
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract()
    )
    _require(
        reviewed.get(
            "pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_reviewed"
        )
        is True,
        "second V2 exhaustion preservation review missing",
    )
    _require(
        reviewed.get("preservation_git_blob") == PRESERVATION_GIT_BLOB,
        "second V2 exhaustion preservation source drift",
    )
    _require(
        reviewed.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256
        and reviewed.get("attempt_marker_bytes") == ATTEMPT_MARKER_BYTES
        and reviewed.get("warm_start_sha256") == WARM_START_SHA256
        and reviewed.get("warm_start_bytes") == WARM_START_BYTES
        and reviewed.get("trajectory_sha256") == TRAJECTORY_SHA256
        and reviewed.get("trajectory_bytes") == TRAJECTORY_BYTES,
        "second V2 exhaustion evidence drift",
    )
    _require(
        reviewed.get("predecessor_preservation_receipt_sha256")
        == PREDECESSOR_PRESERVATION_RECEIPT_SHA256,
        "second V2 exhaustion predecessor preservation drift",
    )
    _require(
        reviewed.get("preservation_authorization_accepted") is False
        and reviewed.get("preservation_performed") is False
        and reviewed.get("runtime_retry_authorized") is False
        and reviewed.get("new_execution_request_opened") is False,
        "second V2 exhaustion preservation review unexpectedly grants authority",
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
            "predecessor_preservation_receipt_sha256": (
                PREDECESSOR_PRESERVATION_RECEIPT_SHA256
            ),
            "result_present": False,
            "closeout_present": False,
            "attempt_consumed": True,
            "attempt_reusable": False,
            "execution_authorization_reusable": False,
        },
        "requested_preservation": {
            "archive_name": preservation.ARCHIVE_NAME,
            "archive_path": str(preservation.ARCHIVE_ROOT),
            "preservation_receipt_path": str(preservation.PRESERVATION_RECEIPT),
            "exact_marker_and_run_artifacts_required": True,
            "exact_clean_detached_registered_worktrees_required": True,
            "engine_removed_before_source": True,
            "non_force_git_worktree_remove_only": True,
            "remaining_evidence_manifest_hashed": True,
            "atomic_baseline_archive_rename_requested": True,
            "marker_and_run_inode_preservation_required": True,
            "create_only_preservation_receipt_requested": True,
            "first_v2_archive_must_remain_unchanged": True,
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
            "prior_preservation_authorization_reusable": False,
            "prior_execution_authorization_reusable": False,
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
    _require(len(raw) <= MAX_REQUEST_BYTES, "preservation request too large")
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
    raise Pair06V9V2SecondExhaustionPreservationAuthorizationRequestHold(
        NEXT_GATE
    )
