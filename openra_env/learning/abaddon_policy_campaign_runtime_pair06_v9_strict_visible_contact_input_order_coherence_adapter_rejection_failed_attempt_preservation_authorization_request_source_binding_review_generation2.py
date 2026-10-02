"""Exact-blob review of the failed-attempt preservation authorization request.

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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-authorization-request-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "4efcb4c4a87aee68758710ce0d064d9d26ad24f7"

REQUEST_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_authorization_request_generation2.py"
)
REQUEST_GIT_BLOB = "e4cafb9a1eba3e70b6c21e7c8ecc398a39d4483b"

REQUEST_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_authorization_request_generation2.py"
)
REQUEST_TEST_GIT_BLOB = "4aa673130e71321f69afe7fc6f4ab6a238ff159d"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_AUTHORIZATION_ACCEPTANCE_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_preservation_authorization_acceptance"
)


class Pair06V9AdapterRejectionPreservationAuthorizationRequestReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionPreservationAuthorizationRequestReviewHold(
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
        "preservation request record kind drift",
    )
    _require(
        record["source_binding"]["preservation_git_blob"]
        == "342118e0e9edbba7472820ae99ff4c05203143d0"
        and record["source_binding"]["preservation_review_git_blob"]
        == "fcb0d97852bf0de74d4c3d502a363cc8b9e02687",
        "preservation request source binding drift",
    )
    _require(
        record["failed_attempt"]["attempt_marker_sha256"]
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
        and record["failed_attempt"]["attempt_consumed"] is True
        and record["failed_attempt"]["attempt_reusable"] is False
        and record["failed_attempt"]["authorization_reusable"] is False,
        "preservation request lineage drift",
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
            "preservation request invariant drift: " + field,
        )
    _require(
        requested.get("file_content_deletion_requested") is False
        and requested.get("force_worktree_removal_requested") is False
        and requested.get("runtime_retry_requested") is False,
        "preservation request unsafe mutation drift",
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
        "preservation authorization boundary drift",
    )

    for field in request.FALSE_AUTHORITY_FIELDS:
        _require(
            record.get(field) is False,
            "preservation request record authority drift: " + field,
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
            "validated preservation request authority drift: " + field,
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


def pair06_v9_adapter_rejection_preservation_authorization_request_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    record = deepcopy(validated["request"])

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "request_path": REQUEST_PATH,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_test_path": REQUEST_TEST_PATH,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_preservation_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "request_bytes": validated["request_bytes"],
        "attempt_marker_sha256": (
            record["failed_attempt"]["attempt_marker_sha256"]
        ),
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
    raise Pair06V9AdapterRejectionPreservationAuthorizationRequestReviewHold(
        NEXT_GATE
    )
