"""Exact-blob review of the authorized second V2 exhaustion preservation launcher."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_authorized_preservation_launcher_generation2
    as launcher,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "authorized-preservation-launcher-review.v1"
)

ACCEPTED_BASE_HEAD = "a6d6c0da398be2ee5f0fbc537311b7495d46364b"

LAUNCHER_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_authorized_"
    "preservation_launcher_generation2.py"
)
LAUNCHER_GIT_BLOB = "aaaa495ef234f5d24400851b109bc2ed09f31bee"

LAUNCHER_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_authorized_"
    "preservation_launcher_generation2.py"
)
LAUNCHER_TEST_GIT_BLOB = "ccbb44cd8af792de03ab6ec6ad6b5c33cdcbd555"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "AUTHORIZED_HOST_PRESERVATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "authorized_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "host_preservation"
)


class Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        launcher
        .pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_contract()
    )

    _require(
        out.get("authorized_preservation_launcher_implemented") is True,
        "second V2 authorized preservation launcher missing",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176",
        "second V2 authorized preservation launcher marker drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
        and out.get("authorization_text_bytes") == 682,
        "second V2 authorized preservation authorization binding drift",
    )

    for field in (
        "exact_current_main_required",
        "exact_launcher_source_sha256_required",
        "explicit_launcher_confirmation_token_required",
        "reviewed_preservation_authorization_required",
        "reviewed_preservation_implementation_required",
        "preservation_delegation_exactly_once",
        "non_force_worktree_removal_required",
        "engine_before_source_removal_required",
        "atomic_archive_rename_required",
        "create_only_preservation_receipt_required",
    ):
        _require(
            out.get(field) is True,
            "second V2 authorized preservation launcher invariant drift: " + field,
        )

    _require(
        out.get("first_v2_archive_mutation_authorized") is False,
        "first V2 archive mutation unexpectedly authorized",
    )

    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "preservation_performed_by_contract_inspection",
        "host_io_performed_by_contract_inspection",
        "authorization_reusable_after_preservation",
    ):
        _require(
            out.get(field) is False,
            "second V2 authorized preservation launcher authority/effect drift: "
            + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (LAUNCHER_PATH, LAUNCHER_GIT_BLOB),
        (LAUNCHER_TEST_PATH, LAUNCHER_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "launcher_path": LAUNCHER_PATH,
        "launcher_git_blob": LAUNCHER_GIT_BLOB,
        "launcher_test_path": LAUNCHER_TEST_PATH,
        "launcher_test_git_blob": LAUNCHER_TEST_GIT_BLOB,
        "pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_reviewed": True,
        "attempt_marker_sha256": out["attempt_marker_sha256"],
        "authorization_text_sha256": out["authorization_text_sha256"],
        "authorization_text_bytes": out["authorization_text_bytes"],
        "exact_current_main_required": True,
        "exact_launcher_source_sha256_required": True,
        "explicit_launcher_confirmation_token_required": True,
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
        "preservation_performed": False,
        "authorization_reusable_after_preservation": False,
        "validated_launcher": out,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherReviewHold(
        NEXT_GATE
    )
