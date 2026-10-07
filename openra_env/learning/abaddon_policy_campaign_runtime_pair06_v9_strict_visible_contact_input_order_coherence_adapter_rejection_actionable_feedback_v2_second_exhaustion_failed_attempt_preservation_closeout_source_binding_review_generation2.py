"""Exact-blob review of the completed second actionable-feedback V2 exhaustion preservation closeout."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_closeout_generation2
    as closeout,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-closeout-review.v1"
)

ACCEPTED_BASE_HEAD = "0ee0d6df2ef617bc4c49cc4c73205a2f75f5ad31"

CLOSEOUT_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_"
    "preservation_closeout_generation2.py"
)
CLOSEOUT_GIT_BLOB = "e7854447a8f5a09551d1547a22a517aabf695e5b"

CLOSEOUT_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_second_exhaustion_failed_attempt_"
    "preservation_closeout_generation2.py"
)
CLOSEOUT_TEST_GIT_BLOB = "a414aa1c1ccf4c16facea9efa0d26853193174a1"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_SOURCE_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v3_structured_correction"
)


class Pair06V9V2SecondExhaustionPreservationCloseoutReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9V2SecondExhaustionPreservationCloseoutReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = closeout.pair06_v9_v2_second_exhaustion_preservation_closeout_contract()

    _require(
        out.get("record_kind") == "source_only_host_preservation_closeout",
        "second V2 preservation closeout record kind drift",
    )
    _require(
        out.get("execution_control_main_head") == ACCEPTED_BASE_HEAD
        and out.get("execution_control_main_tree")
        == "2dd40a6fcc537401315181728183720e094be445",
        "second V2 preservation execution-control identity drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
        and out.get("authorization_text_bytes") == 682
        and out.get("reviewed_request_sha256")
        == "dc9ed1487e2d218001d178eab66b29958d98c1fa7eb30760bfaf7998fe679dfc"
        and out.get("reviewed_request_bytes") == 3473,
        "second V2 preservation authorization/request binding drift",
    )
    _require(
        out.get("launcher_source_sha256")
        == "70642c23a73f4f25775519f2e53a3751ae40816be5e42ab4a8f611b811cbb00b"
        and out.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and out.get("preservation_receipt_sha256")
        == "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021",
        "second V2 preservation closeout artifact identity drift",
    )
    _require(
        out.get("predecessor_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e",
        "second V2 preservation predecessor receipt drift",
    )
    _require(
        out.get("attempt_consumed") is True
        and out.get("attempt_reusable") is False
        and out.get("attempt_authorization_reusable") is False
        and out.get("preservation_authorization_consumed") is True
        and out.get("preservation_authorization_reusable") is False,
        "second V2 preservation closeout lineage reuse drift",
    )

    for field in (
        "archive_atomic_rename_performed",
        "attempt_marker_inode_preserved",
        "warm_start_inode_preserved",
        "trajectory_inode_preserved",
        "source_worktree_removed_non_force",
        "engine_worktree_removed_non_force",
        "single_authorized_preservation_consumed",
        "runtime_output_observed",
        "structured_correction_v3_required",
    ):
        _require(
            out.get(field) is True,
            "second V2 preservation closeout invariant drift: " + field,
        )

    _require(
        out.get("same_v2_retry_recommended") is False,
        "same V2 retry unexpectedly recommended",
    )

    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "scheduler_mutation_performed",
        "repo_side_local_artifact_rehash_performed",
    ):
        _require(
            out.get(field) is False,
            "second V2 preservation closeout authority drift: " + field,
        )

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate") == NEXT_GATE,
        "second V2 preservation closeout frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (CLOSEOUT_PATH, CLOSEOUT_GIT_BLOB),
        (CLOSEOUT_TEST_PATH, CLOSEOUT_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_v2_second_exhaustion_preservation_closeout_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "closeout_path": CLOSEOUT_PATH,
        "closeout_git_blob": CLOSEOUT_GIT_BLOB,
        "closeout_test_path": CLOSEOUT_TEST_PATH,
        "closeout_test_git_blob": CLOSEOUT_TEST_GIT_BLOB,
        "pair06_v9_v2_second_exhaustion_preservation_closeout_reviewed": True,
        "attempt_marker_sha256": out["attempt_marker_sha256"],
        "preservation_receipt_sha256": out["preservation_receipt_sha256"],
        "predecessor_preservation_receipt_sha256": out[
            "predecessor_preservation_receipt_sha256"
        ],
        "attempt_consumed": True,
        "attempt_reusable": False,
        "attempt_authorization_reusable": False,
        "preservation_authorization_consumed": True,
        "preservation_authorization_reusable": False,
        "preservation_lineage_closed": True,
        "same_v2_retry_recommended": False,
        "structured_correction_v3_required": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "new_execution_request_opened": False,
        "fresh_execution_authorization_required_for_any_future_run": True,
        "validated_closeout": out,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def request_or_reopen(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9V2SecondExhaustionPreservationCloseoutReviewHold(NEXT_GATE)
