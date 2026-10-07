"""Source-only closeout for the completed second actionable-feedback V2 exhaustion preservation.

This record captures the exact terminal identities printed by the reviewed
single-use Precision preservation launcher. It performs no host I/O and grants
no runtime retry, execution request, model/game execution, training,
deployment, chain, wallet/funds, or scheduler authority.

The second actionable-feedback V2 attempt and its preservation authorization
are permanently spent. The next source frontier is a V3 structured-correction
repair, not another V2 execution request.
"""

from __future__ import annotations

from typing import Any


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-actionable-feedback-v2-second-exhaustion-"
    "preservation-closeout.v1"
)

EXECUTION_CONTROL_MAIN_HEAD = "0ee0d6df2ef617bc4c49cc4c73205a2f75f5ad31"
EXECUTION_CONTROL_MAIN_TREE = "2dd40a6fcc537401315181728183720e094be445"

AUTHORIZATION_TEXT_SHA256 = (
    "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
)
AUTHORIZATION_TEXT_BYTES = 682

REVIEWED_REQUEST_SHA256 = (
    "dc9ed1487e2d218001d178eab66b29958d98c1fa7eb30760bfaf7998fe679dfc"
)
REVIEWED_REQUEST_BYTES = 3473

LAUNCHER_SOURCE_SHA256 = (
    "70642c23a73f4f25775519f2e53a3751ae40816be5e42ab4a8f611b811cbb00b"
)

ATTEMPT_MARKER_SHA256 = (
    "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
)
WARM_START_SHA256 = (
    "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
)
TRAJECTORY_SHA256 = (
    "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
)
PRESERVATION_RECEIPT_SHA256 = (
    "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
)

ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-ee1b4fc5"
)
PRESERVATION_RECEIPT_PATH = ARCHIVE_PATH + "-preservation-receipt.json"

PREDECESSOR_PRESERVATION_RECEIPT_SHA256 = (
    "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_SOURCE_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v3_structured_correction"
)


def pair06_v9_v2_second_exhaustion_preservation_closeout_contract() -> dict[str, Any]:
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
        "predecessor_preservation_receipt_sha256": (
            PREDECESSOR_PRESERVATION_RECEIPT_SHA256
        ),
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
        "same_v2_retry_recommended": False,
        "structured_correction_v3_required": True,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_reopen(*args: Any, **kwargs: Any) -> None:
    raise RuntimeError(NEXT_GATE)
