"""Audit-only acceptance of explicit failed-attempt preservation authorization.

This record binds the user's exact preservation authorization text to:
* the exact reviewed preservation acceptance requirements;
* the exact reviewed preservation request digest and byte length; and
* canonical War College main head/tree at authorization time.

It authorizes only the reviewed failed-attempt preservation operation:
non-force Git worktree removal, atomic archive rename, and create-only
preservation receipt creation after exact evidence validation.

This source performs no host I/O, filesystem mutation, Git worktree mutation,
archive rename, receipt creation, runtime retry, model load, inference, game
execution, training, deployment, VOID-chain mutation, wallet/funds action, or
scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_acceptance_requirements_source_binding_review_generation2
    as requirements_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-authorization-acceptance-contract.v1"
)

AUTHORIZED_MAIN_HEAD = "b36cafe6044012656d9a122653c2ddb5b9831f63"
AUTHORIZED_MAIN_TREE = "03b0a1ae8d8b050e50429c1f1617fb12953ebf1e"

AUTHORIZATION_TEXT_SHA256 = (
    "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
)
AUTHORIZATION_TEXT_BYTES = 35

REQUIREMENTS_REVIEW_GIT_BLOB = "670a94ce020d193e23d2b1c19c624c765a926a6e"
REQUIREMENTS_SOURCE_GIT_BLOB = "aa40644a2a3c76b53cbb9c76681c43bfd6a5a714"
REQUIREMENTS_TEST_GIT_BLOB = "7a896d4278ad148f0ca5056460f1d4d94eefd47e"
REQUIREMENTS_REVIEW_TEST_GIT_BLOB = "29a4d0c240d09de0b181937b5e776f5c870ffc45"

ATTEMPT_MARKER_SHA256 = (
    "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_authorized_preservation_launcher"
)


class Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_requirements() -> dict[str, Any]:
    out = (
        requirements_review
        .pair06_v9_adapter_rejection_preservation_acceptance_requirements_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_adapter_rejection_preservation_acceptance_requirements_reviewed"
        )
        is True,
        "preservation acceptance requirements review missing",
    )
    _require(
        out.get("requirements_git_blob") == REQUIREMENTS_SOURCE_GIT_BLOB
        and out.get("requirements_test_git_blob") == REQUIREMENTS_TEST_GIT_BLOB,
        "preservation acceptance requirements source identity drift",
    )
    _require(
        out.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "preservation acceptance attempt marker drift",
    )
    _require(
        out.get("exact_user_authorization_text_required") is True
        and out.get("authorization_text_sha256_binding_required") is True
        and out.get("authorization_text_byte_length_binding_required") is True
        and out.get("canonical_main_head_binding_required") is True
        and out.get("canonical_main_tree_binding_required") is True,
        "preservation acceptance binding requirement drift",
    )
    _require(
        out.get(
            "general_source_work_authorization_is_preservation_authorization"
        )
        is False
        and out.get("preservation_authorization_accepted") is False
        and out.get("preservation_performed") is False,
        "preservation requirements unexpectedly self-authorize",
    )
    _require(
        out.get("runtime_retry_authorized") is False
        and out.get("execution_request_opened") is False
        and out.get("runtime_execution_authorized") is False,
        "preservation requirements runtime boundary drift",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_EXPLICIT_USER_"
            "AUTHORIZATION_REQUIRED"
        ),
        "preservation explicit-authorization frontier drift",
    )

    return deepcopy(out)


def pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_requirements()

    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "preservation_authorization_accepted": True,
        "preservation_authorized": True,
        "authorized_reviewed_request_sha256": reviewed["reviewed_request_sha256"],
        "authorized_reviewed_request_bytes": reviewed["reviewed_request_bytes"],
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_main_tree": AUTHORIZED_MAIN_TREE,
        "canonical_main_bound_at_authorization_time": True,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "requirements_review_git_blob": REQUIREMENTS_REVIEW_GIT_BLOB,
        "requirements_source_git_blob": REQUIREMENTS_SOURCE_GIT_BLOB,
        "requirements_test_git_blob": REQUIREMENTS_TEST_GIT_BLOB,
        "requirements_review_test_git_blob": REQUIREMENTS_REVIEW_TEST_GIT_BLOB,
        "attempt_marker_sha256": reviewed["attempt_marker_sha256"],
        "archive_path": reviewed["archive_path"],
        "preservation_receipt_path": reviewed["preservation_receipt_path"],
        "exact_evidence_validation_required_before_mutation": True,
        "non_force_git_worktree_removal_authorized": True,
        "engine_removed_before_source_authorized": True,
        "remaining_evidence_manifest_hashing_authorized": True,
        "atomic_baseline_archive_rename_authorized": True,
        "marker_and_run_inode_preservation_required": True,
        "create_only_preservation_receipt_authorized": True,
        "file_content_deletion_authorized": False,
        "force_worktree_removal_authorized": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
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
        "filesystem_mutation_performed_by_this_record": False,
        "git_worktree_mutation_performed_by_this_record": False,
        "archive_rename_performed_by_this_record": False,
        "preservation_receipt_created_by_this_record": False,
        "preservation_performed_by_this_record": False,
        "authorization_reusable_after_preservation": False,
        "reviewed_requirements": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceHold(
        NEXT_GATE
    )
