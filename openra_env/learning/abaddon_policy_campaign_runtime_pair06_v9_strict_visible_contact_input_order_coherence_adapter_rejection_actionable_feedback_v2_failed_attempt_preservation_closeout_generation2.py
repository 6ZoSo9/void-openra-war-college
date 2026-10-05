"""Source-only closeout for the completed Pair-06 V9 actionable-feedback V2 failed-attempt preservation.

This record captures the exact terminal identities printed by the reviewed
single-use Precision preservation launcher. It does not read host state and it
does not grant runtime retry, game execution, training, deployment, chain,
wallet/funds, or scheduler authority.

The consumed actionable-feedback V2 attempt, its failed runtime artifacts, and
the preservation authorization are permanently spent and non-reusable.
"""

from __future__ import annotations

from typing import Any


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-closeout.v1"
)

EXECUTION_CONTROL_MAIN_HEAD = "e203d56e627fbcddb7f7b6d44652657b3ab58b46"
EXECUTION_CONTROL_MAIN_TREE = "0483d9ac42b65a0f2bde501bee0aa8aae30dae18"

AUTHORIZATION_TEXT_SHA256 = (
    "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
)
AUTHORIZATION_TEXT_BYTES = 186

REVIEWED_REQUEST_SHA256 = (
    "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
)
REVIEWED_REQUEST_BYTES = 3288

LAUNCHER_SOURCE_SHA256 = (
    "1f8cdf4be60d581d3d7994f3d47e450e314d917658e7cfa310a6552e5a338d92"
)

ATTEMPT_MARKER_SHA256 = (
    "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
)
WARM_START_SHA256 = (
    "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
)
TRAJECTORY_SHA256 = (
    "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
)
PRESERVATION_RECEIPT_SHA256 = (
    "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
)

ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
)
PRESERVATION_RECEIPT_PATH = (
    ARCHIVE_PATH + "-preservation-receipt.json"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_CLOSEOUT_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_closeout_review"
)


def pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "record_kind": "source_only_host_preservation_closeout",
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "failure_class": "strict_contact_actionable_feedback_v2_exhausted",
        "failure_round": 6,
        "execution_control_main_head": EXECUTION_CONTROL_MAIN_HEAD,
        "execution_control_main_tree": EXECUTION_CONTROL_MAIN_TREE,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "reviewed_request_sha256": REVIEWED_REQUEST_SHA256,
        "reviewed_request_bytes": REVIEWED_REQUEST_BYTES,
        "launcher_source_sha256": LAUNCHER_SOURCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "warm_start_sha256": WARM_START_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "archive_path": ARCHIVE_PATH,
        "preservation_receipt_path": PRESERVATION_RECEIPT_PATH,
        "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
        "attempt_consumed": True,
        "attempt_reusable": False,
        "attempt_authorization_reusable": False,
        "preservation_authorization_consumed": True,
        "preservation_authorization_reusable": False,
        "archive_atomic_rename_performed": True,
        "attempt_marker_inode_preserved": True,
        "warm_start_inode_preserved": True,
        "trajectory_inode_preserved": True,
        "source_worktree_removed_non_force": True,
        "engine_worktree_removed_non_force": True,
        "single_authorized_preservation_consumed": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "new_execution_request_opened": False,
        "runtime_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "scheduler_mutation_performed": False,
        "runtime_output_observed": True,
        "repo_side_local_artifact_rehash_performed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_reopen(*args: Any, **kwargs: Any) -> None:
    raise RuntimeError(NEXT_GATE)
