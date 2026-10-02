"""Exact-blob review of preservation authorization acceptance requirements.

Pins the non-authorizing requirements source and focused tests. The review
confirms that exact user text digest/length plus canonical main head/tree must
be bound by a later preservation-specific acceptance.

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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_acceptance_requirements_generation2
    as requirements,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-authorization-acceptance-requirements-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "240bbb182819b0ca09b2c2d8df53b045de0435fd"

REQUIREMENTS_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_authorization_acceptance_requirements_generation2.py"
)
REQUIREMENTS_GIT_BLOB = "aa40644a2a3c76b53cbb9c76681c43bfd6a5a714"

REQUIREMENTS_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_authorization_acceptance_requirements_generation2.py"
)
REQUIREMENTS_TEST_GIT_BLOB = "7a896d4278ad148f0ca5056460f1d4d94eefd47e"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_preservation_explicit_authorization"
)


class Pair06V9AdapterRejectionPreservationAcceptanceRequirementsReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionPreservationAcceptanceRequirementsReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        requirements
        .pair06_v9_adapter_rejection_preservation_acceptance_requirements_contract()
    )

    _require(
        out.get("acceptance_requirements_implemented") is True,
        "preservation acceptance requirements missing",
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
            "preservation acceptance requirement drift: " + field,
        )

    _require(
        out.get("general_source_work_authorization_is_preservation_authorization")
        is False
        and out.get("matching_request_digest_grants_authority") is False
        and out.get("matching_request_bytes_grant_authority") is False,
        "preservation acceptance authority boundary drift",
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
            "preservation acceptance requirements authority drift: " + field,
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


def pair06_v9_adapter_rejection_preservation_acceptance_requirements_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "requirements_path": REQUIREMENTS_PATH,
        "requirements_git_blob": REQUIREMENTS_GIT_BLOB,
        "requirements_test_path": REQUIREMENTS_TEST_PATH,
        "requirements_test_git_blob": REQUIREMENTS_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_preservation_acceptance_requirements_reviewed": True,
        "reviewed_request_sha256": validated["reviewed_request_sha256"],
        "reviewed_request_bytes": validated["reviewed_request_bytes"],
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "archive_path": validated["archive_path"],
        "preservation_receipt_path": validated["preservation_receipt_path"],
        "exact_user_authorization_text_required": True,
        "authorization_text_sha256_binding_required": True,
        "authorization_text_byte_length_binding_required": True,
        "canonical_main_head_binding_required": True,
        "canonical_main_tree_binding_required": True,
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
    raise Pair06V9AdapterRejectionPreservationAcceptanceRequirementsReviewHold(
        NEXT_GATE
    )
