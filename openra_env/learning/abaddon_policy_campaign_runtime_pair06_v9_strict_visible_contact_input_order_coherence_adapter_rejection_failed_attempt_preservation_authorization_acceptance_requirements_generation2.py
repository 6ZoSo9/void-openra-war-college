"""Source-only acceptance requirements for failed-attempt preservation.

This module consumes the reviewed preservation-authorization request and
publishes the exact bindings a later explicit authorization acceptance must
capture. It does not accept authorization and performs no preservation.

A later acceptance must bind:
* exact reviewed preservation request digest and byte length;
* exact user authorization text digest and byte length;
* canonical main head and tree at authorization time;
* exact consumed marker/archive/receipt scope.

General source-work authorization remains explicitly non-equivalent to
preservation authorization.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-authorization-acceptance-requirements-contract.v1"
)

REQUEST_REVIEW_GIT_BLOB = "6bdf38c47a5fd778709469b36f50119dea1a0a0e"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_preservation_explicit_authorization"
)


class Pair06V9AdapterRejectionPreservationAcceptanceRequirementsHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionPreservationAcceptanceRequirementsHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v9_adapter_rejection_preservation_authorization_request_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_adapter_rejection_preservation_authorization_request_reviewed"
        )
        is True,
        "preservation authorization request review missing",
    )
    _require(
        out.get("preservation_authorization_requested") is True
        and out.get("fresh_explicit_user_authorization_required") is True
        and out.get(
            "general_source_work_authorization_is_preservation_authorization"
        )
        is False,
        "preservation authorization request boundary drift",
    )
    _require(
        out.get("preservation_authorization_accepted") is False
        and out.get("preservation_performed") is False
        and out.get("runtime_retry_authorized") is False
        and out.get("execution_request_opened") is False
        and out.get("runtime_execution_authorized") is False,
        "preservation request review unexpectedly grants authority",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d",
        "preservation attempt marker identity drift",
    )

    return deepcopy(out)


def pair06_v9_adapter_rejection_preservation_acceptance_requirements_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()

    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "acceptance_requirements_implemented": True,
        "reviewed_request_sha256": reviewed["request_sha256"],
        "reviewed_request_bytes": reviewed["request_bytes"],
        "attempt_marker_sha256": reviewed["attempt_marker_sha256"],
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
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
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
    raise Pair06V9AdapterRejectionPreservationAcceptanceRequirementsHold(
        NEXT_GATE
    )
