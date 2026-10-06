"""Audit-only acceptance of explicit preservation authorization for the second actionable-feedback V2 exhaustion."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_request_source_binding_review_generation2
    as request_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_requirements_source_binding_review_generation2
    as requirements_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-authorization-acceptance.v1"
)

AUTHORIZED_MAIN_HEAD = "69538ff6c0e2d82d7ab4e0ecdfe28b867ef48e35"
AUTHORIZED_MAIN_TREE = "be5ed71f0f1f5feaf86107964ebd6746fb9c1512"

AUTHORIZATION_TEXT_SHA256 = (
    "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
)
AUTHORIZATION_TEXT_BYTES = 682

REQUEST_SHA256 = (
    "dc9ed1487e2d218001d178eab66b29958d98c1fa7eb30760bfaf7998fe679dfc"
)
REQUEST_BYTES = 3473

REQUEST_REVIEW_GIT_BLOB = "be55d59172141f1d0c3bee9a8dcfca320afca5ab"
REQUIREMENTS_REVIEW_GIT_BLOB = "d995a0c8fd181da0099272b85a57bb0f5f6452b2"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "authorized_preservation_launcher"
)


class Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed() -> dict[str, Any]:
    request = (
        request_review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_request_review_contract()
    )
    requirements = (
        requirements_review
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_review_contract()
    )

    _require(
        request.get(
            "pair06_v9_v2_second_exhaustion_preservation_authorization_request_reviewed"
        )
        is True,
        "second V2 preservation request review missing",
    )
    _require(
        requirements.get(
            "pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_reviewed"
        )
        is True,
        "second V2 preservation acceptance requirements review missing",
    )
    _require(
        request.get("request_sha256") == REQUEST_SHA256
        and request.get("request_bytes") == REQUEST_BYTES
        and requirements.get("reviewed_request_sha256") == REQUEST_SHA256
        and requirements.get("reviewed_request_bytes") == REQUEST_BYTES,
        "second V2 preservation request identity drift",
    )
    _require(
        request.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and request.get("warm_start_sha256")
        == "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
        and request.get("trajectory_sha256")
        == "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
        and request.get("predecessor_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e",
        "second V2 preservation evidence identity drift",
    )
    for field in (
        "exact_user_authorization_text_required",
        "authorization_text_sha256_binding_required",
        "authorization_text_byte_length_binding_required",
        "canonical_main_head_binding_required",
        "canonical_main_tree_binding_required",
        "canonical_main_must_be_bound_at_authorization_time",
        "authorization_must_reference_exact_reviewed_request",
    ):
        _require(
            requirements.get(field) is True,
            "second V2 preservation acceptance requirement drift: " + field,
        )
    _require(
        requirements.get("prior_preservation_authorization_reusable") is False
        and requirements.get("prior_execution_authorization_reusable") is False
        and requirements.get(
            "general_source_work_authorization_is_preservation_authorization"
        )
        is False,
        "second V2 preservation authority reuse drift",
    )
    for field in (
        "preservation_authorization_accepted",
        "preservation_performed",
        "runtime_retry_authorized",
        "execution_request_opened",
    ):
        _require(
            requirements.get(field) is False,
            "second V2 preservation requirements unexpectedly self-authorize: "
            + field,
        )

    return {
        "request_review": deepcopy(request),
        "requirements_review": deepcopy(requirements),
    }


def pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed()
    request = reviewed["request_review"]
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "preservation_authorization_accepted": True,
        "preservation_authorized": True,
        "filesystem_mutation_authorized": True,
        "git_worktree_mutation_authorized": True,
        "archive_rename_authorized": True,
        "preservation_receipt_creation_authorized": True,
        "authorized_request_sha256": REQUEST_SHA256,
        "authorized_request_bytes": REQUEST_BYTES,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_main_tree": AUTHORIZED_MAIN_TREE,
        "canonical_main_bound_at_authorization_time": True,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "requirements_review_git_blob": REQUIREMENTS_REVIEW_GIT_BLOB,
        "attempt_marker_sha256": request["attempt_marker_sha256"],
        "attempt_marker_bytes": request["attempt_marker_bytes"],
        "warm_start_sha256": request["warm_start_sha256"],
        "trajectory_sha256": request["trajectory_sha256"],
        "predecessor_preservation_receipt_sha256": request[
            "predecessor_preservation_receipt_sha256"
        ],
        "archive_path": request["archive_path"],
        "preservation_receipt_path": request["preservation_receipt_path"],
        "exact_evidence_validation_authorized": True,
        "non_force_reviewed_worktree_removal_authorized": True,
        "engine_before_source_removal_required": True,
        "atomic_archive_rename_authorized": True,
        "inode_preservation_required": True,
        "create_only_preservation_receipt_authorized": True,
        "first_v2_archive_mutation_authorized": False,
        "prior_preservation_authorization_reusable": False,
        "prior_execution_authorization_reusable": False,
        "preservation_performed_by_this_record": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_request_opened": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "reviewed": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceHold(
        NEXT_GATE
    )
