"""Exact-blob review of the completed actionable-feedback V2 failed-attempt preservation closeout.

Pins the source-only closeout and focused tests. The review permanently closes
the consumed actionable-feedback V2 attempt and its preservation authorization.

It grants no runtime retry, replay, training, deployment, chain, wallet/funds,
or scheduler authority. Any future run requires a distinct fresh execution
request and fresh execution authorization.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_closeout_generation2
    as closeout,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-closeout-review.v1"
)

ACCEPTED_BASE_HEAD = "e203d56e627fbcddb7f7b6d44652657b3ab58b46"

CLOSEOUT_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_closeout_generation2.py"
)
CLOSEOUT_GIT_BLOB = "655ecff86859d70c83dffac0109b9e7a1d95ae00"

CLOSEOUT_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_closeout_generation2.py"
)
CLOSEOUT_TEST_GIT_BLOB = "76106d2c7c0765b2d349a41e3f00958100976a62"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_EXECUTION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_fresh_execution_request"
)


class Pair06V9ActionableFeedbackV2PreservationCloseoutReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PreservationCloseoutReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        closeout
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract()
    )

    _require(
        out.get("record_kind") == "source_only_host_preservation_closeout",
        "V2 preservation closeout record kind drift",
    )
    _require(
        out.get("execution_control_main_head") == ACCEPTED_BASE_HEAD
        and out.get("execution_control_main_tree")
        == "0483d9ac42b65a0f2bde501bee0aa8aae30dae18",
        "V2 preservation execution-control identity drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
        and out.get("authorization_text_bytes") == 186
        and out.get("reviewed_request_sha256")
        == "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
        and out.get("reviewed_request_bytes") == 3288,
        "V2 preservation authorization binding drift",
    )
    _require(
        out.get("launcher_source_sha256")
        == "1f8cdf4be60d581d3d7994f3d47e450e314d917658e7cfa310a6552e5a338d92"
        and out.get("attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and out.get("preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e",
        "V2 preservation closeout artifact identity drift",
    )
    _require(
        out.get("attempt_consumed") is True
        and out.get("attempt_reusable") is False
        and out.get("attempt_authorization_reusable") is False
        and out.get("preservation_authorization_consumed") is True
        and out.get("preservation_authorization_reusable") is False,
        "V2 preservation closeout lineage reuse drift",
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
    ):
        _require(
            out.get(field) is True,
            "V2 preservation closeout invariant drift: " + field,
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
            "V2 preservation closeout authority drift: " + field,
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


def pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "closeout_path": CLOSEOUT_PATH,
        "closeout_git_blob": CLOSEOUT_GIT_BLOB,
        "closeout_test_path": CLOSEOUT_TEST_PATH,
        "closeout_test_git_blob": CLOSEOUT_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "preservation_receipt_sha256": validated["preservation_receipt_sha256"],
        "attempt_consumed": True,
        "attempt_reusable": False,
        "attempt_authorization_reusable": False,
        "preservation_authorization_consumed": True,
        "preservation_authorization_reusable": False,
        "preservation_lineage_closed": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "new_execution_request_opened": False,
        "fresh_execution_authorization_required": True,
        "validated_closeout": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def request_or_reopen(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PreservationCloseoutReviewHold(NEXT_GATE)
