"""Source-only acceptance requirements for preserving the second actionable-feedback V2 exhaustion.

Consumes the reviewed proposal-only preservation request and defines the exact
bindings a later preservation-specific explicit user authorization acceptance
must capture. No preservation authority is accepted here and no host mutation
is performed.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-authorization-acceptance-requirements.v1"
)

REQUEST_REVIEW_GIT_BLOB = "be55d59172141f1d0c3bee9a8dcfca320afca5ab"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "preservation_explicit_authorization"
)


class Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_request_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_v2_second_exhaustion_preservation_authorization_request_reviewed"
        )
        is True,
        "second V2 exhaustion preservation request review missing",
    )
    _require(
        out.get("request_git_blob")
        == "e86550a6b2676befa6d77484ec33f5c2c1f21919"
        and out.get("request_test_git_blob")
        == "a12014899704c5237a301b13007518fce94b6d90",
        "second V2 exhaustion preservation request source identity drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and out.get("attempt_marker_bytes") == 2208
        and out.get("warm_start_sha256")
        == "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
        and out.get("trajectory_sha256")
        == "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04",
        "second V2 exhaustion preservation evidence drift",
    )
    _require(
        out.get("predecessor_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e",
        "second V2 exhaustion predecessor preservation drift",
    )
    _require(
        out.get("preservation_authorization_requested") is True
        and out.get("fresh_explicit_user_authorization_required") is True
        and out.get(
            "general_source_work_authorization_is_preservation_authorization"
        )
        is False
        and out.get("prior_preservation_authorization_reusable") is False
        and out.get("prior_execution_authorization_reusable") is False,
        "second V2 exhaustion preservation authorization boundary drift",
    )
    _require(
        out.get("preservation_authorization_accepted") is False
        and out.get("preservation_performed") is False
        and out.get("runtime_retry_authorized") is False
        and out.get("execution_request_opened") is False,
        "second V2 exhaustion preservation request unexpectedly grants authority",
    )

    return deepcopy(out)


def pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()

    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "acceptance_requirements_implemented": True,
        "reviewed_request_sha256": reviewed["request_sha256"],
        "reviewed_request_bytes": reviewed["request_bytes"],
        "attempt_marker_sha256": reviewed["attempt_marker_sha256"],
        "attempt_marker_bytes": reviewed["attempt_marker_bytes"],
        "warm_start_sha256": reviewed["warm_start_sha256"],
        "trajectory_sha256": reviewed["trajectory_sha256"],
        "predecessor_preservation_receipt_sha256": reviewed[
            "predecessor_preservation_receipt_sha256"
        ],
        "archive_path": reviewed["archive_path"],
        "preservation_receipt_path": reviewed["preservation_receipt_path"],
        "exact_user_authorization_text_required": True,
        "authorization_text_sha256_binding_required": True,
        "authorization_text_byte_length_binding_required": True,
        "canonical_main_head_binding_required": True,
        "canonical_main_tree_binding_required": True,
        "canonical_main_must_be_bound_at_authorization_time": True,
        "authorization_must_reference_exact_reviewed_request": True,
        "general_source_work_authorization_is_preservation_authorization": False,
        "matching_request_digest_grants_authority": False,
        "matching_request_bytes_grant_authority": False,
        "prior_preservation_authorization_reusable": False,
        "prior_execution_authorization_reusable": False,
        "preservation_authorization_accepted": False,
        "preservation_authorized": False,
        "filesystem_mutation_authorized": False,
        "git_worktree_mutation_authorized": False,
        "archive_rename_authorized": False,
        "preservation_receipt_creation_authorized": False,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "reviewed_request": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsHold(
        NEXT_GATE
    )
