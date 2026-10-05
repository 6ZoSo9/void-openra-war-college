"""Exact-blob review of actionable-feedback V2 preservation acceptance requirements.

Pins the non-authorizing requirements source and focused tests. The review
confirms that exact user authorization text digest/length plus canonical main
head/tree must be bound by a later preservation-specific acceptance.

No authorization is accepted here. No preservation, host mutation, runtime
retry, execution request, model/game execution, training, deployment, chain,
wallet/funds, or scheduler action is performed or authorized.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_requirements_generation2
    as requirements,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-authorization-acceptance-requirements-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "4f19ec52290170de3cb4a5be8938e0d6afccb80f"

REQUIREMENTS_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_authorization_"
    "acceptance_requirements_generation2.py"
)
REQUIREMENTS_GIT_BLOB = "95a4a3455c6e5e15bed61489121b0f6b9a64ccdb"

REQUIREMENTS_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_authorization_"
    "acceptance_requirements_generation2.py"
)
REQUIREMENTS_TEST_GIT_BLOB = "ad75eaef22ec84cef2461df18ba21a6a3fd35506"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_explicit_authorization"
)


class Pair06V9ActionableFeedbackV2PreservationAcceptanceRequirementsReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PreservationAcceptanceRequirementsReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_contract()
    )

    _require(
        out.get("acceptance_requirements_implemented") is True,
        "actionable-feedback V2 preservation acceptance requirements missing",
    )
    _require(
        out.get("request_review_git_blob")
        == "f076dd3082d2a1ba092e99877e74f2c3a0f6db30",
        "actionable-feedback V2 request review identity drift",
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
            "actionable-feedback V2 preservation acceptance requirement drift: "
            + field,
        )

    _require(
        out.get("general_source_work_authorization_is_preservation_authorization")
        is False
        and out.get("matching_request_digest_grants_authority") is False
        and out.get("matching_request_bytes_grant_authority") is False,
        "actionable-feedback V2 preservation acceptance authority boundary drift",
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
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        _require(
            out.get(field) is False,
            "actionable-feedback V2 preservation acceptance requirements "
            "authority drift: " + field,
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


def pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "requirements_path": REQUIREMENTS_PATH,
        "requirements_git_blob": REQUIREMENTS_GIT_BLOB,
        "requirements_test_path": REQUIREMENTS_TEST_PATH,
        "requirements_test_git_blob": REQUIREMENTS_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_reviewed": True,
        "reviewed_request_sha256": validated["reviewed_request_sha256"],
        "reviewed_request_bytes": validated["reviewed_request_bytes"],
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "attempt_marker_bytes": validated["attempt_marker_bytes"],
        "warm_start_sha256": validated["warm_start_sha256"],
        "trajectory_sha256": validated["trajectory_sha256"],
        "failure_class": validated["failure_class"],
        "failure_round": validated["failure_round"],
        "archive_path": validated["archive_path"],
        "preservation_receipt_path": validated["preservation_receipt_path"],
        "exact_user_authorization_text_required": True,
        "authorization_text_sha256_binding_required": True,
        "authorization_text_byte_length_binding_required": True,
        "canonical_main_head_binding_required": True,
        "canonical_main_tree_binding_required": True,
        "canonical_main_must_be_bound_at_authorization_time": True,
        "authorization_must_reference_exact_reviewed_request": True,
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
        "validated_requirements": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PreservationAcceptanceRequirementsReviewHold(
        NEXT_GATE
    )
