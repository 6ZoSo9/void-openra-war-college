"""Exact-blob review of the second V2 exhaustion preservation authorization request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-authorization-request-review.v1"
)
ACCEPTED_BASE_HEAD = "a9f3971045d78d6d51d14a233f80c83d5f69aadf"

REQUEST_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_"
    "preservation_authorization_request_generation2.py"
)
REQUEST_GIT_BLOB = "e86550a6b2676befa6d77484ec33f5c2c1f21919"
REQUEST_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_"
    "preservation_authorization_request_generation2.py"
)
REQUEST_TEST_GIT_BLOB = "a12014899704c5237a301b13007518fce94b6d90"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "PRESERVATION_AUTHORIZATION_ACCEPTANCE_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "preservation_authorization_acceptance"
)


class Pair06V9V2SecondExhaustionPreservationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationRequestReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.preservation_authorization_request()
    record = out["request"]
    failed = record["failed_attempt"]
    scope = record["requested_preservation"]
    boundary = record["authorization_boundary"]

    _require(
        record.get("record_kind") == "proposal_only_not_authorization",
        "second-exhaustion request record kind drift",
    )
    _require(
        failed.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and failed.get("warm_start_sha256")
        == "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
        and failed.get("trajectory_sha256")
        == "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
        and failed.get("predecessor_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e",
        "second-exhaustion request evidence identity drift",
    )
    _require(
        failed.get("attempt_consumed") is True
        and failed.get("attempt_reusable") is False
        and failed.get("execution_authorization_reusable") is False,
        "second-exhaustion request attempt reuse drift",
    )
    for field in (
        "exact_marker_and_run_artifacts_required",
        "exact_clean_detached_registered_worktrees_required",
        "engine_removed_before_source",
        "non_force_git_worktree_remove_only",
        "remaining_evidence_manifest_hashed",
        "atomic_baseline_archive_rename_requested",
        "marker_and_run_inode_preservation_required",
        "create_only_preservation_receipt_requested",
        "first_v2_archive_must_remain_unchanged",
    ):
        _require(scope.get(field) is True, "preservation request invariant drift: " + field)
    _require(
        scope.get("file_content_deletion_requested") is False
        and scope.get("force_worktree_removal_requested") is False
        and scope.get("runtime_retry_requested") is False,
        "preservation request mutation boundary drift",
    )
    _require(
        boundary.get("preservation_authorization_requested") is True
        and boundary.get("fresh_explicit_user_authorization_required") is True
        and boundary.get(
            "general_source_work_authorization_is_preservation_authorization"
        )
        is False
        and boundary.get("matching_request_digest_grants_authority") is False
        and boundary.get("matching_request_bytes_grant_authority") is False
        and boundary.get("prior_preservation_authorization_reusable") is False
        and boundary.get("prior_execution_authorization_reusable") is False,
        "preservation request authorization boundary drift",
    )

    for field in request.FALSE_AUTHORITY_FIELDS:
        _require(record.get(field) is False, "request authority drift: " + field)

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
        _require(out.get(field) is False, "request effect drift: " + field)

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


def pair06_v9_v2_second_exhaustion_preservation_authorization_request_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    record = deepcopy(validated["request"])
    failed = record["failed_attempt"]
    scope = record["requested_preservation"]
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "request_path": REQUEST_PATH,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_test_path": REQUEST_TEST_PATH,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "pair06_v9_v2_second_exhaustion_preservation_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "request_bytes": validated["request_bytes"],
        "attempt_marker_sha256": failed["attempt_marker_sha256"],
        "attempt_marker_bytes": failed["attempt_marker_bytes"],
        "warm_start_sha256": failed["warm_start_sha256"],
        "warm_start_bytes": failed["warm_start_bytes"],
        "trajectory_sha256": failed["trajectory_sha256"],
        "trajectory_bytes": failed["trajectory_bytes"],
        "predecessor_preservation_receipt_sha256": failed[
            "predecessor_preservation_receipt_sha256"
        ],
        "archive_path": scope["archive_path"],
        "preservation_receipt_path": scope["preservation_receipt_path"],
        "preservation_authorization_requested": True,
        "fresh_explicit_user_authorization_required": True,
        "general_source_work_authorization_is_preservation_authorization": False,
        "prior_preservation_authorization_reusable": False,
        "prior_execution_authorization_reusable": False,
        "preservation_authorization_accepted": False,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionPreservationRequestReviewHold(NEXT_GATE)
