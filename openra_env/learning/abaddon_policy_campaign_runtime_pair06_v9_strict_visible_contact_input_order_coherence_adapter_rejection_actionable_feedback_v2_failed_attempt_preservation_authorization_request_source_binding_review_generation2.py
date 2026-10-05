"""Exact-blob review of the actionable-feedback V2 preservation authorization request.

Pins the proposal-only request source and focused tests, validates deterministic
request bytes, and confirms the request grants no preservation or runtime
authority. General source-work authorization remains explicitly distinct from
preservation authorization.

No host I/O or mutation is performed. The next gate is fresh explicit user
authorization acceptance for the exact reviewed preservation request.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-authorization-request-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "ee6a45530e6982771cfc3ec92e838fa224885cc3"

REQUEST_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_"
    "authorization_request_generation2.py"
)
REQUEST_GIT_BLOB = "d82749e6f4996d11065dcb74ee7a74a9b9926a43"

REQUEST_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_"
    "authorization_request_generation2.py"
)
REQUEST_TEST_GIT_BLOB = "cfba5df9a3a893fdc6ece0f554b9d0650538e437"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_AUTHORIZATION_ACCEPTANCE_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_authorization_acceptance"
)


class Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.preservation_authorization_request()
    record = out["request"]

    _require(
        record.get("record_kind") == "proposal_only_not_authorization",
        "V2 preservation request record kind drift",
    )
    _require(
        record["source_binding"]["preservation_stack_head"]
        == "ee6a45530e6982771cfc3ec92e838fa224885cc3"
        and record["source_binding"]["preservation_git_blob"]
        == "92981d23b580059fd3419cfe95daea561aab6add"
        and record["source_binding"]["preservation_review_git_blob"]
        == "62f21456cbd358cf8cff9d621d4530485b9531f5",
        "V2 preservation request source binding drift",
    )

    failed = record["failed_attempt"]
    _require(
        failed.get("attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and failed.get("attempt_marker_bytes") == 2208
        and failed.get("warm_start_sha256")
        == "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
        and failed.get("trajectory_sha256")
        == "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
        and failed.get("attempt_consumed") is True
        and failed.get("attempt_reusable") is False
        and failed.get("authorization_reusable") is False,
        "V2 preservation request lineage drift",
    )
    _require(
        failed.get("failure_class")
        == "strict_contact_actionable_feedback_v2_exhausted"
        and failed.get("failure_round") == 6
        and failed.get("maximum_decision_attempts") == 6,
        "V2 preservation request failure-shape drift",
    )

    requested = record["requested_preservation"]
    for field in (
        "exact_marker_and_run_artifacts_required",
        "exact_clean_detached_registered_worktrees_required",
        "engine_removed_before_source",
        "non_force_git_worktree_remove_only",
        "remaining_evidence_manifest_hashed",
        "atomic_baseline_archive_rename_requested",
        "marker_and_run_inode_preservation_required",
        "create_only_preservation_receipt_requested",
    ):
        _require(
            requested.get(field) is True,
            "V2 preservation request invariant drift: " + field,
        )
    _require(
        requested.get("file_content_deletion_requested") is False
        and requested.get("force_worktree_removal_requested") is False
        and requested.get("runtime_retry_requested") is False,
        "V2 preservation request unsafe mutation drift",
    )

    boundary = record["authorization_boundary"]
    _require(
        boundary.get("preservation_authorization_requested") is True
        and boundary.get("fresh_explicit_user_authorization_required") is True
        and boundary.get(
            "general_source_work_authorization_is_preservation_authorization"
        )
        is False
        and boundary.get("matching_request_digest_grants_authority") is False
        and boundary.get("matching_request_bytes_grant_authority") is False,
        "V2 preservation authorization boundary drift",
    )

    for field in request.FALSE_AUTHORITY_FIELDS:
        _require(
            record.get(field) is False,
            "V2 preservation request record authority drift: " + field,
        )

    for field in (
        "preservation_authorization_accepted",
        "request_grants_authority",
        "host_io_performed",
        "filesystem_mutation_performed",
        "git_worktree_mutation_performed",
        "archive_rename_performed",
        "preservation_receipt_created",
        "runtime_retry_authorized",
        "execution_request_opened",
        "runtime_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "validated V2 preservation request authority drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (REQUEST_PATH, REQUEST_GIT_BLOB),
        (REQUEST_TEST_PATH, REQUEST_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_preservation_authorization_request_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    record = deepcopy(validated["request"])

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "request_path": REQUEST_PATH,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_test_path": REQUEST_TEST_PATH,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_preservation_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "request_bytes": validated["request_bytes"],
        "attempt_marker_sha256": record["failed_attempt"]["attempt_marker_sha256"],
        "attempt_marker_bytes": record["failed_attempt"]["attempt_marker_bytes"],
        "warm_start_sha256": record["failed_attempt"]["warm_start_sha256"],
        "trajectory_sha256": record["failed_attempt"]["trajectory_sha256"],
        "failure_class": record["failed_attempt"]["failure_class"],
        "failure_round": record["failed_attempt"]["failure_round"],
        "archive_path": record["requested_preservation"]["archive_path"],
        "preservation_receipt_path": (
            record["requested_preservation"]["preservation_receipt_path"]
        ),
        "preservation_authorization_requested": True,
        "fresh_explicit_user_authorization_required": True,
        "general_source_work_authorization_is_preservation_authorization": False,
        "preservation_authorization_accepted": False,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "runtime_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestReviewHold(
        NEXT_GATE
    )
