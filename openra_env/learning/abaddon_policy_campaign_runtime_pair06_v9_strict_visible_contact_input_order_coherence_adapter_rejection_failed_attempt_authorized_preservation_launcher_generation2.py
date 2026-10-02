"""Authorized one-shot launcher for Pair-06 V9 failed-attempt preservation.

This launcher binds the reviewed preservation authorization acceptance to the
reviewed failed-attempt preservation implementation.

Operational preservation requires all of:
* exact launcher confirmation token;
* exact current canonical main;
* exact launcher source SHA-256;
* reviewed preservation authorization acceptance;
* reviewed preservation source/review identities.

The launcher delegates exactly once to the reviewed preservation function. It
does not authorize runtime retry, model/game execution, training, deployment,
VOID-chain mutation, wallet/funds action, or scheduler mutation.

Import and contract inspection are inert.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as base_invocation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_generation2
    as preservation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_acceptance_source_binding_review_generation2
    as acceptance_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "authorized-preservation-launcher-contract.v1"
)

SOURCE_ROOT = Path(base_invocation.SOURCE_ROOT)
SELF_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_authorized_preservation_launcher_generation2.py"
)

ACCEPTANCE_REVIEW_GIT_BLOB = "a24eec0b15c263a2ce7e5dd0952187b4866bc8d6"
PRESERVATION_GIT_BLOB = "342118e0e9edbba7472820ae99ff4c05203143d0"
PRESERVATION_REVIEW_GIT_BLOB = "3913e75e1e2b86407601904f4fc69b6c2de22127"

ATTEMPT_MARKER_SHA256 = (
    "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
)
AUTHORIZATION_TEXT_SHA256 = (
    "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
)
AUTHORIZATION_TEXT_BYTES = 35

LAUNCHER_CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_INPUT_ORDER_ADAPTER_REJECTION_"
    "AUTHORIZED_PRESERVE_FAILED_ATTEMPT_ONCE"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_PRESERVATION_LAUNCHER_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_authorized_preservation_launcher_review"
)


class Pair06V9AdapterRejectionAuthorizedPreservationLauncherHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionAuthorizedPreservationLauncherHold(
            message
        )


def _acceptance() -> dict[str, Any]:
    accepted = (
        acceptance_review
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract()
    )
    reviewed_preservation = (
        preservation_review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract()
    )

    _require(
        accepted.get(
            "pair06_v9_adapter_rejection_preservation_authorization_acceptance_reviewed"
        )
        is True,
        "preservation authorization acceptance review missing",
    )
    _require(
        accepted.get("preservation_authorization_accepted") is True
        and accepted.get("preservation_authorized") is True,
        "preservation authorization not accepted",
    )
    _require(
        accepted.get("authorization_text_sha256") == AUTHORIZATION_TEXT_SHA256
        and accepted.get("authorization_text_bytes") == AUTHORIZATION_TEXT_BYTES,
        "preservation authorization text binding drift",
    )
    _require(
        accepted.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "preservation authorization attempt marker drift",
    )
    _require(
        accepted.get("non_force_git_worktree_removal_authorized") is True
        and accepted.get("atomic_baseline_archive_rename_authorized") is True
        and accepted.get("create_only_preservation_receipt_authorized") is True,
        "preservation mutation envelope not authorized",
    )
    _require(
        accepted.get("runtime_retry_authorized") is False
        and accepted.get("execution_request_opened") is False
        and accepted.get("runtime_execution_authorized") is False
        and accepted.get("authorization_reusable_after_preservation") is False,
        "preservation acceptance runtime/reuse boundary drift",
    )

    _require(
        reviewed_preservation.get(
            "pair06_v9_adapter_rejection_failed_attempt_preservation_reviewed"
        )
        is True,
        "reviewed preservation implementation missing",
    )
    _require(
        reviewed_preservation.get("preservation_git_blob")
        == PRESERVATION_GIT_BLOB,
        "preservation source identity drift",
    )
    _require(
        reviewed_preservation.get("attempt_marker_sha256")
        == ATTEMPT_MARKER_SHA256,
        "reviewed preservation marker identity drift",
    )
    _require(
        reviewed_preservation.get("non_force_worktree_removal_only") is True
        and reviewed_preservation.get("atomic_baseline_archive_rename_reviewed")
        is True
        and reviewed_preservation.get("create_only_preservation_receipt_reviewed")
        is True,
        "reviewed preservation safety boundary drift",
    )
    _require(
        reviewed_preservation.get("runtime_retry_authorized") is False
        and reviewed_preservation.get("new_execution_request_opened") is False,
        "reviewed preservation unexpectedly grants runtime authority",
    )

    return {
        "acceptance_review": deepcopy(accepted),
        "preservation_review": deepcopy(reviewed_preservation),
    }


def _verify_self(expected_source_sha256: str) -> str:
    _require(
        isinstance(expected_source_sha256, str)
        and len(expected_source_sha256) == 64
        and all(ch in "0123456789abcdef" for ch in expected_source_sha256),
        "authorized preservation launcher expected source SHA invalid",
    )
    source = SOURCE_ROOT / SELF_PATH
    _require(
        Path(__file__) == source,
        "authorized preservation launcher origin hold",
    )
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    _require(
        actual == expected_source_sha256,
        "authorized preservation launcher source drift",
    )
    return actual


def execute_authorized_preservation_once(
    *,
    expected_main_head: str,
    expected_launcher_source_sha256: str,
    launcher_confirm: str,
) -> dict[str, Any]:
    """Execute exactly one reviewed failed-attempt preservation operation."""
    _require(
        isinstance(launcher_confirm, str)
        and launcher_confirm == LAUNCHER_CONFIRM_TOKEN,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZED_PRESERVATION_CONFIRMATION_REQUIRED",
    )

    dependencies = _acceptance()
    source_sha = _verify_self(expected_launcher_source_sha256)
    main = base_invocation._current_main(expected_main_head)

    result = preservation.preserve_pair06_v9_input_order_adapter_rejection_failed_attempt(
        preservation_authorized=True,
        confirm=preservation.CONFIRM_TOKEN,
    )

    _require(
        isinstance(result, dict),
        "authorized preservation result must be object",
    )
    _require(
        result.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256
        and result.get("attempt_consumed") is True,
        "authorized preservation result marker drift",
    )
    _require(
        result.get("source_worktree_removed_non_force") is True
        and result.get("engine_worktree_removed_non_force") is True
        and result.get("archive_atomic_rename_performed") is True
        and result.get("attempt_marker_inode_preserved") is True
        and result.get("warm_start_inode_preserved") is True
        and result.get("trajectory_inode_preserved") is True,
        "authorized preservation result invariant drift",
    )
    _require(
        result.get("automatic_retry") is False
        and result.get("runtime_retry_authorized") is False
        and result.get("new_execution_request_opened") is False
        and result.get("game_execution_performed") is False
        and result.get("void_chain_mutation_performed") is False
        and result.get("wallet_or_funds_action_performed") is False
        and result.get("scheduler_mutation_performed") is False,
        "authorized preservation result runtime/effect boundary drift",
    )

    return {
        **deepcopy(result),
        "launcher_schema": CONTRACT_SCHEMA,
        "launcher_source_sha256": source_sha,
        "launcher_main": deepcopy(main),
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "single_authorized_preservation_consumed": True,
        "authorization_reusable_after_preservation": False,
        "dependencies": dependencies,
    }


def pair06_v9_adapter_rejection_authorized_preservation_launcher_contract() -> dict[str, Any]:
    dependencies = _acceptance()

    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_review_git_blob": ACCEPTANCE_REVIEW_GIT_BLOB,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_review_git_blob": PRESERVATION_REVIEW_GIT_BLOB,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "authorized_preservation_launcher_implemented": True,
        "exact_current_main_required": True,
        "exact_launcher_source_sha256_required": True,
        "explicit_launcher_confirmation_token_required": True,
        "reviewed_preservation_authorization_required": True,
        "reviewed_preservation_implementation_required": True,
        "preservation_delegation_exactly_once": True,
        "non_force_worktree_removal_required": True,
        "atomic_archive_rename_required": True,
        "create_only_preservation_receipt_required": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_request_opened": False,
        "runtime_execution_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "preservation_performed_by_contract_inspection": False,
        "host_io_performed_by_contract_inspection": False,
        "authorization_reusable_after_preservation": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionAuthorizedPreservationLauncherHold(
        NEXT_GATE
    )
