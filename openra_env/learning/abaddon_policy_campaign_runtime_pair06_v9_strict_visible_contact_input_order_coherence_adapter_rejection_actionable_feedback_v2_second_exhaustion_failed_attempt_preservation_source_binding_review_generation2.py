"""Exact-blob review of the second actionable-feedback V2 exhaustion preservation gate."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_generation2
    as preservation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "second-exhaustion-failed-attempt-preservation-review.v1"
)
ACCEPTED_BASE_HEAD = "4ac5f41ff7632e847e79e3d8ebfd632aeb0633f2"

PRESERVATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_"
    "preservation_generation2.py"
)
PRESERVATION_GIT_BLOB = "963ebf0c9c7d8f3bae9143285cf781e8c6d92d24"
PRESERVATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_"
    "preservation_generation2.py"
)
PRESERVATION_TEST_GIT_BLOB = "7c4ea80ada8285d5cca931b9d2e571d1fe78a229"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_FAILED_ATTEMPT_"
    "PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v2_second_exhaustion_"
    "preservation_authorization_request"
)

class Pair06V9ActionableFeedbackV2SecondExhaustionPreservationReviewHold(ValueError):
    pass

def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2SecondExhaustionPreservationReviewHold(message)

def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = preservation.pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()

    _require(
        out.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and out.get("warm_start_sha256")
        == "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
        and out.get("trajectory_sha256")
        == "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04",
        "second V2 exhaustion evidence identity drift",
    )
    _require(
        out.get("authorized_attempt_main_head")
        == "4ac5f41ff7632e847e79e3d8ebfd632aeb0633f2"
        and out.get("authorized_attempt_main_tree")
        == "02d2f2ea0b81bf13981d8c49b7caf8ea4012f92a"
        and out.get("operator_source_sha256")
        == "fcc662cbaaa482651004523b73deb906947a73b296356cc291bb9150dddfc179",
        "second V2 exhaustion source lineage drift",
    )
    _require(
        out.get("predecessor_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
        and out.get("first_v2_archive_must_remain_present") is True
        and out.get("first_v2_preservation_receipt_must_match") is True,
        "first V2 archive continuity drift",
    )
    for field in (
        "exact_consumed_marker_required",
        "exact_run_artifacts_required",
        "result_must_be_absent",
        "closeout_must_be_absent",
        "summary_must_be_absent",
        "exact_clean_detached_registered_worktrees_required",
        "non_force_worktree_removal_only",
        "engine_removed_before_source",
        "remaining_evidence_manifest_hashed",
        "atomic_baseline_archive_rename_implemented",
        "attempt_marker_inode_preserved",
        "run_artifact_inode_preserved",
        "create_only_preservation_receipt_implemented",
        "preservation_requires_explicit_authority",
        "preservation_confirmation_token_required",
    ):
        _require(out.get(field) is True, "preservation invariant drift: " + field)

    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        _require(out.get(field) is False, "preservation authority drift: " + field)

    root = Path(__file__).parents[2]
    for rel, expected in (
        (PRESERVATION_PATH, PRESERVATION_GIT_BLOB),
        (PRESERVATION_TEST_PATH, PRESERVATION_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(_git_blob_sha1(target.read_bytes()) == expected, "reviewed source blob drift: " + rel)
    return deepcopy(out)

def pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "preservation_path": PRESERVATION_PATH,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_test_path": PRESERVATION_TEST_PATH,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_reviewed": True,
        "attempt_marker_sha256": out["attempt_marker_sha256"],
        "attempt_marker_bytes": out["attempt_marker_bytes"],
        "warm_start_sha256": out["warm_start_sha256"],
        "warm_start_bytes": out["warm_start_bytes"],
        "trajectory_sha256": out["trajectory_sha256"],
        "trajectory_bytes": out["trajectory_bytes"],
        "failure_class": out["failure_class"],
        "failure_round": out["failure_round"],
        "maximum_decision_attempts": out["maximum_decision_attempts"],
        "terminal_feedback": out["terminal_feedback"],
        "archive_name": out["archive_name"],
        "archive_path": out["archive_path"],
        "preservation_receipt_path": out["preservation_receipt_path"],
        "predecessor_preservation_receipt_sha256": out["predecessor_preservation_receipt_sha256"],
        "preservation_authorization_accepted": False,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "new_execution_request_opened": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }

def request_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2SecondExhaustionPreservationReviewHold(NEXT_GATE)
