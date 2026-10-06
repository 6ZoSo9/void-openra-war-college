"""Exact-blob review of the second V2 exhaustion preservation acceptance requirements."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_requirements_generation2
    as requirements,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-authorization-acceptance-requirements-review.v1"
)

ACCEPTED_BASE_HEAD = "9ea0126d1d2291b1bf4d69a9d0be7be6a7c6a166"

REQUIREMENTS_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_"
    "authorization_acceptance_requirements_generation2.py"
)
REQUIREMENTS_GIT_BLOB = "53a85a1b0e4e3209413de5e614d0422b3837d97a"

REQUIREMENTS_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_"
    "authorization_acceptance_requirements_generation2.py"
)
REQUIREMENTS_TEST_GIT_BLOB = "a1ee1660f265332ebd2a508dc7c1a259ab4d180d"

REQUEST_REVIEW_GIT_BLOB = "be55d59172141f1d0c3bee9a8dcfca320afca5ab"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "preservation_explicit_authorization"
)


class Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        requirements
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract()
    )

    _require(
        out.get("acceptance_requirements_implemented") is True,
        "second V2 exhaustion preservation acceptance requirements missing",
    )
    _require(
        out.get("request_review_git_blob") == REQUEST_REVIEW_GIT_BLOB,
        "second V2 exhaustion request review identity drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and out.get("warm_start_sha256")
        == "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
        and out.get("trajectory_sha256")
        == "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
        and out.get("predecessor_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e",
        "second V2 exhaustion preservation evidence drift",
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
            out.get(field) is True,
            "second V2 preservation acceptance requirement drift: " + field,
        )

    _require(
        out.get("general_source_work_authorization_is_preservation_authorization")
        is False
        and out.get("matching_request_digest_grants_authority") is False
        and out.get("matching_request_bytes_grant_authority") is False
        and out.get("prior_preservation_authorization_reusable") is False
        and out.get("prior_execution_authorization_reusable") is False,
        "second V2 preservation authority reuse boundary drift",
    )

    for field in (
        "preservation_authorization_accepted",
        "preservation_authorized",
        "filesystem_mutation_authorized",
        "git_worktree_mutation_authorized",
        "archive_rename_authorized",
        "preservation_receipt_creation_authorized",
        "preservation_performed",
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
        "host_io_performed_by_contract_inspection",
    ):
        _require(
            out.get(field) is False,
            "second V2 preservation requirements self-authorized: " + field,
        )

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate") == NEXT_GATE,
        "second V2 preservation requirements frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (REQUIREMENTS_PATH, REQUIREMENTS_GIT_BLOB),
        (REQUIREMENTS_TEST_PATH, REQUIREMENTS_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "requirements_path": REQUIREMENTS_PATH,
        "requirements_git_blob": REQUIREMENTS_GIT_BLOB,
        "requirements_test_path": REQUIREMENTS_TEST_PATH,
        "requirements_test_git_blob": REQUIREMENTS_TEST_GIT_BLOB,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_reviewed": True,
        "reviewed_request_sha256": out["reviewed_request_sha256"],
        "reviewed_request_bytes": out["reviewed_request_bytes"],
        "attempt_marker_sha256": out["attempt_marker_sha256"],
        "attempt_marker_bytes": out["attempt_marker_bytes"],
        "warm_start_sha256": out["warm_start_sha256"],
        "trajectory_sha256": out["trajectory_sha256"],
        "predecessor_preservation_receipt_sha256": out[
            "predecessor_preservation_receipt_sha256"
        ],
        "archive_path": out["archive_path"],
        "preservation_receipt_path": out["preservation_receipt_path"],
        "exact_user_authorization_text_required": True,
        "authorization_text_sha256_binding_required": True,
        "authorization_text_byte_length_binding_required": True,
        "canonical_main_head_binding_required": True,
        "canonical_main_tree_binding_required": True,
        "canonical_main_must_be_bound_at_authorization_time": True,
        "authorization_must_reference_exact_reviewed_request": True,
        "general_source_work_authorization_is_preservation_authorization": False,
        "prior_preservation_authorization_reusable": False,
        "prior_execution_authorization_reusable": False,
        "preservation_authorization_accepted": False,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "validated_requirements": out,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsReviewHold(
        NEXT_GATE
    )
