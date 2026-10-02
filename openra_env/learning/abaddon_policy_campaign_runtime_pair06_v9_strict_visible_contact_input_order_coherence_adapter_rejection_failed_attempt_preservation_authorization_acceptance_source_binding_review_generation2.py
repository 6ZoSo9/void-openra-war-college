"""Exact-blob review of explicit failed-attempt preservation authorization.

Pins the audit-only acceptance source and focused tests. The review confirms the
exact user authorization digest/length, exact canonical main snapshot at
authorization time, exact reviewed request binding, and the narrow preservation
mutation envelope.

The acceptance record itself performs no host mutation. Runtime retry,
execution, training, deployment, chain, wallet/funds, and scheduler authority
remain false.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-authorization-acceptance-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "b6ef6ae9f3a5f6ce83ba18f07dbab7026d44d116"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_authorization_acceptance_generation2.py"
)
ACCEPTANCE_GIT_BLOB = "992332060f4040ada4e34d8119e84bd4c641a9f4"

ACCEPTANCE_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_authorization_acceptance_generation2.py"
)
ACCEPTANCE_TEST_GIT_BLOB = "845d4aaa8b62f3b7376571db596e86342af220d3"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_authorized_preservation_launcher"
)


class Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        acceptance
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract()
    )

    _require(
        out.get("authorization_record_kind") == "explicit_user_authorization"
        and out.get("authorization_accepted") is True
        and out.get("preservation_authorization_accepted") is True
        and out.get("preservation_authorized") is True,
        "preservation authorization acceptance missing",
    )
    _require(
        out.get("authorization_text_sha256")
        == "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
        and out.get("authorization_text_bytes") == 35,
        "preservation authorization text binding drift",
    )
    _require(
        out.get("authorized_main_head")
        == "b36cafe6044012656d9a122653c2ddb5b9831f63"
        and out.get("authorized_main_tree")
        == "03b0a1ae8d8b050e50429c1f1617fb12953ebf1e"
        and out.get("canonical_main_bound_at_authorization_time") is True,
        "preservation authorization main binding drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d",
        "preservation authorized marker identity drift",
    )

    for field in (
        "exact_evidence_validation_required_before_mutation",
        "non_force_git_worktree_removal_authorized",
        "engine_removed_before_source_authorized",
        "remaining_evidence_manifest_hashing_authorized",
        "atomic_baseline_archive_rename_authorized",
        "marker_and_run_inode_preservation_required",
        "create_only_preservation_receipt_authorized",
    ):
        _require(
            out.get(field) is True,
            "preservation authorized invariant drift: " + field,
        )

    for field in (
        "file_content_deletion_authorized",
        "force_worktree_removal_authorized",
        "runtime_retry_authorized",
        "automatic_retry",
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
        "filesystem_mutation_performed_by_this_record",
        "git_worktree_mutation_performed_by_this_record",
        "archive_rename_performed_by_this_record",
        "preservation_receipt_created_by_this_record",
        "preservation_performed_by_this_record",
        "authorization_reusable_after_preservation",
    ):
        _require(
            out.get(field) is False,
            "preservation acceptance effect/authority drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (ACCEPTANCE_PATH, ACCEPTANCE_GIT_BLOB),
        (ACCEPTANCE_TEST_PATH, ACCEPTANCE_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "acceptance_path": ACCEPTANCE_PATH,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_test_path": ACCEPTANCE_TEST_PATH,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_preservation_authorization_acceptance_reviewed": True,
        "authorization_text_sha256": validated["authorization_text_sha256"],
        "authorization_text_bytes": validated["authorization_text_bytes"],
        "authorized_reviewed_request_sha256": (
            validated["authorized_reviewed_request_sha256"]
        ),
        "authorized_reviewed_request_bytes": (
            validated["authorized_reviewed_request_bytes"]
        ),
        "authorized_main_head": validated["authorized_main_head"],
        "authorized_main_tree": validated["authorized_main_tree"],
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "archive_path": validated["archive_path"],
        "preservation_receipt_path": validated["preservation_receipt_path"],
        "preservation_authorization_accepted": True,
        "preservation_authorized": True,
        "non_force_git_worktree_removal_authorized": True,
        "atomic_baseline_archive_rename_authorized": True,
        "create_only_preservation_receipt_authorized": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_request_opened": False,
        "runtime_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "preservation_performed": False,
        "authorization_reusable_after_preservation": False,
        "validated_acceptance": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceReviewHold(
        NEXT_GATE
    )
