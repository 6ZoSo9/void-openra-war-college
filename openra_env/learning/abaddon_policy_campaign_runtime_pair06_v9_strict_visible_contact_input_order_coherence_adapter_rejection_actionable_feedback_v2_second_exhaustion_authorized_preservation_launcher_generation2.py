"""Authorized one-shot launcher for second actionable-feedback V2 exhaustion preservation.

This launcher binds the reviewed preservation authorization acceptance to the
reviewed second-exhaustion preservation implementation. Import and contract
inspection are inert.

Operational preservation requires the exact launcher confirmation token, exact
current canonical main, exact launcher source SHA-256, reviewed authorization
acceptance, and exact reviewed preservation source identities.

The launcher delegates exactly once to preservation. It grants no runtime
retry, execution request, model/game execution, training, deployment,
VOID-chain mutation, wallet/funds action, or scheduler mutation.
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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_generation2
    as preservation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_source_binding_review_generation2
    as acceptance_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "authorized-preservation-launcher.v1"
)

SOURCE_ROOT = Path(base_invocation.SOURCE_ROOT)
SELF_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_authorized_"
    "preservation_launcher_generation2.py"
)

ACCEPTANCE_REVIEW_GIT_BLOB = "a0563d865ec950324e205de7904243560d6f1cb3"
PRESERVATION_GIT_BLOB = "963ebf0c9c7d8f3bae9143285cf781e8c6d92d24"
PRESERVATION_REVIEW_GIT_BLOB = "5275908efb8c8d01295e5fee5284f84c6e452698"

ATTEMPT_MARKER_SHA256 = (
    "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
)
AUTHORIZATION_TEXT_SHA256 = (
    "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
)
AUTHORIZATION_TEXT_BYTES = 682

LAUNCHER_CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "AUTHORIZED_PRESERVE_EE1B4FC5_ONCE"
)

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "AUTHORIZED_PRESERVATION_LAUNCHER_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "authorized_preservation_launcher_review"
)


class Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherHold(
            message
        )


def _acceptance() -> dict[str, Any]:
    accepted = (
        acceptance_review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract()
    )
    reviewed_preservation = (
        preservation_review
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract()
    )

    _require(
        accepted.get(
            "pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_reviewed"
        )
        is True,
        "second V2 preservation authorization acceptance review missing",
    )
    _require(
        accepted.get("preservation_authorization_accepted") is True
        and accepted.get("preservation_authorized") is True,
        "second V2 preservation authorization not accepted",
    )
    _require(
        accepted.get("authorization_text_sha256") == AUTHORIZATION_TEXT_SHA256
        and accepted.get("authorization_text_bytes") == AUTHORIZATION_TEXT_BYTES,
        "second V2 preservation authorization text binding drift",
    )
    _require(
        accepted.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "second V2 preservation authorization marker drift",
    )
    _require(
        accepted.get("filesystem_mutation_authorized") is True
        and accepted.get("git_worktree_mutation_authorized") is True
        and accepted.get("archive_rename_authorized") is True
        and accepted.get("preservation_receipt_creation_authorized") is True,
        "second V2 preservation mutation envelope not authorized",
    )
    _require(
        accepted.get("first_v2_archive_mutation_authorized") is False
        and accepted.get("prior_preservation_authorization_reusable") is False
        and accepted.get("prior_execution_authorization_reusable") is False,
        "second V2 preservation lineage reuse drift",
    )
    _require(
        accepted.get("runtime_retry_authorized") is False
        and accepted.get("execution_request_opened") is False
        and accepted.get("training_authorized") is False
        and accepted.get("deployment_authorized") is False
        and accepted.get("void_chain_mutation_authorized") is False
        and accepted.get("wallet_or_funds_action_authorized") is False
        and accepted.get("scheduler_mutation_authorized") is False,
        "second V2 preservation acceptance extra authority drift",
    )

    _require(
        reviewed_preservation.get(
            "pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_reviewed"
        )
        is True,
        "second V2 reviewed preservation implementation missing",
    )
    _require(
        reviewed_preservation.get("preservation_git_blob")
        == PRESERVATION_GIT_BLOB,
        "second V2 preservation source identity drift",
    )
    _require(
        reviewed_preservation.get("attempt_marker_sha256")
        == ATTEMPT_MARKER_SHA256,
        "second V2 reviewed preservation marker identity drift",
    )
    _require(
        reviewed_preservation.get("runtime_retry_authorized") is False
        and reviewed_preservation.get("new_execution_request_opened") is False,
        "second V2 reviewed preservation unexpectedly grants runtime authority",
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
        "second V2 authorized preservation launcher expected source SHA invalid",
    )
    source = SOURCE_ROOT / SELF_PATH
    _require(
        Path(__file__) == source,
        "second V2 authorized preservation launcher origin hold",
    )
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    _require(
        actual == expected_source_sha256,
        "second V2 authorized preservation launcher source drift",
    )
    return actual


def execute_authorized_preservation_once(
    *,
    expected_main_head: str,
    expected_launcher_source_sha256: str,
    launcher_confirm: str,
) -> dict[str, Any]:
    _require(
        isinstance(launcher_confirm, str)
        and launcher_confirm == LAUNCHER_CONFIRM_TOKEN,
        "PAIR06_V9_V2_SECOND_EXHAUSTION_AUTHORIZED_PRESERVATION_CONFIRMATION_REQUIRED",
    )

    dependencies = _acceptance()
    source_sha = _verify_self(expected_launcher_source_sha256)
    main = base_invocation._current_main(expected_main_head)

    result = (
        preservation
        .preserve_pair06_v9_actionable_feedback_v2_second_exhaustion(
            preservation_authorized=True,
            confirm=preservation.CONFIRM_TOKEN,
        )
    )

    _require(isinstance(result, dict), "authorized preservation result missing")
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
        "authorized preservation result effect boundary drift",
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


def pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_contract() -> dict[str, Any]:
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
        "engine_before_source_removal_required": True,
        "atomic_archive_rename_required": True,
        "create_only_preservation_receipt_required": True,
        "first_v2_archive_mutation_authorized": False,
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
    raise Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherHold(
        NEXT_GATE
    )
