"""Exact-blob review of explicit preservation authorization for the second V2 exhaustion."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-authorization-acceptance-review.v1"
)

ACCEPTED_BASE_HEAD = "69538ff6c0e2d82d7ab4e0ecdfe28b867ef48e35"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_"
    "authorization_acceptance_generation2.py"
)
ACCEPTANCE_GIT_BLOB = "717f9ef02f89085a560ad31ba8b18218acc06ac5"

ACCEPTANCE_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_"
    "authorization_acceptance_generation2.py"
)
ACCEPTANCE_TEST_GIT_BLOB = "411a06ef61d51040c4bb33cd0039d10a8953af14"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
    "AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "authorized_preservation_launcher"
)


class Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        acceptance
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract()
    )

    _require(
        out.get("authorization_record_kind") == "explicit_user_authorization"
        and out.get("authorization_accepted") is True
        and out.get("preservation_authorization_accepted") is True
        and out.get("preservation_authorized") is True,
        "second V2 preservation authorization acceptance missing",
    )
    _require(
        out.get("authorization_text_sha256")
        == "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
        and out.get("authorization_text_bytes") == 682,
        "second V2 preservation authorization text drift",
    )
    _require(
        out.get("authorized_request_sha256")
        == "dc9ed1487e2d218001d178eab66b29958d98c1fa7eb30760bfaf7998fe679dfc"
        and out.get("authorized_request_bytes") == 3473,
        "second V2 preservation request identity drift",
    )
    _require(
        out.get("authorized_main_head")
        == "69538ff6c0e2d82d7ab4e0ecdfe28b867ef48e35"
        and out.get("authorized_main_tree")
        == "be5ed71f0f1f5feaf86107964ebd6746fb9c1512"
        and out.get("canonical_main_bound_at_authorization_time") is True,
        "second V2 preservation main binding drift",
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
        "second V2 preservation evidence binding drift",
    )

    for field in (
        "filesystem_mutation_authorized",
        "git_worktree_mutation_authorized",
        "archive_rename_authorized",
        "preservation_receipt_creation_authorized",
        "exact_evidence_validation_authorized",
        "non_force_reviewed_worktree_removal_authorized",
        "engine_before_source_removal_required",
        "atomic_archive_rename_authorized",
        "inode_preservation_required",
        "create_only_preservation_receipt_authorized",
    ):
        _require(
            out.get(field) is True,
            "second V2 preservation authorized scope drift: " + field,
        )

    _require(
        out.get("first_v2_archive_mutation_authorized") is False
        and out.get("prior_preservation_authorization_reusable") is False
        and out.get("prior_execution_authorization_reusable") is False
        and out.get("preservation_performed_by_this_record") is False,
        "second V2 preservation lineage/effect drift",
    )

    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "execution_request_opened",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "second V2 preservation extra authority drift: " + field,
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


def pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "acceptance_path": ACCEPTANCE_PATH,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_test_path": ACCEPTANCE_TEST_PATH,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_reviewed": True,
        "authorization_text_sha256": out["authorization_text_sha256"],
        "authorization_text_bytes": out["authorization_text_bytes"],
        "authorized_request_sha256": out["authorized_request_sha256"],
        "authorized_request_bytes": out["authorized_request_bytes"],
        "authorized_main_head": out["authorized_main_head"],
        "authorized_main_tree": out["authorized_main_tree"],
        "attempt_marker_sha256": out["attempt_marker_sha256"],
        "attempt_marker_bytes": out["attempt_marker_bytes"],
        "warm_start_sha256": out["warm_start_sha256"],
        "trajectory_sha256": out["trajectory_sha256"],
        "predecessor_preservation_receipt_sha256": out[
            "predecessor_preservation_receipt_sha256"
        ],
        "archive_path": out["archive_path"],
        "preservation_receipt_path": out["preservation_receipt_path"],
        "preservation_authorization_accepted": True,
        "preservation_authorized": True,
        "filesystem_mutation_authorized": True,
        "git_worktree_mutation_authorized": True,
        "archive_rename_authorized": True,
        "preservation_receipt_creation_authorized": True,
        "first_v2_archive_mutation_authorized": False,
        "prior_preservation_authorization_reusable": False,
        "prior_execution_authorization_reusable": False,
        "preservation_performed_by_this_record": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_acceptance": out,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceReviewHold(
        NEXT_GATE
    )
