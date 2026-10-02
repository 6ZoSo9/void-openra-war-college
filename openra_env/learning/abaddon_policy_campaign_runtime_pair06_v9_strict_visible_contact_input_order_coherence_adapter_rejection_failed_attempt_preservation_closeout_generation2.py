"""Source-only closeout for the completed Pair-06 V9 failed-attempt preservation.

This record captures the exact terminal identities printed by the reviewed
single-use Precision preservation launcher. It does not read host state and it
does not grant runtime retry, game execution, training, deployment, chain,
wallet/funds, or scheduler authority.

The consumed input-order attempt, its failed runtime artifacts, and the
preservation authorization are permanently spent and non-reusable.
"""

from __future__ import annotations

from typing import Any


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-closeout.v1"
)

AUTHORIZED_MAIN_HEAD = "43f95480eafa642c8203552fbc00d8edd522d74c"
AUTHORIZED_MAIN_TREE = "50db944a47dc386fa7f8814aad45683df907f259"

AUTHORIZATION_TEXT_SHA256 = (
    "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
)
AUTHORIZATION_TEXT_BYTES = 35

LAUNCHER_SOURCE_SHA256 = (
    "1456f8b30d9af526b8f4e6937bc20a417a5f58ba6dbfa7dfdbe0e11738273c84"
)

ATTEMPT_MARKER_SHA256 = (
    "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
)
WARM_START_SHA256 = (
    "9ad33940dcc8199a61b6fa8bb5fb68f2eb8cc846fb745cf7e64c27e6e053b0e1"
)
TRAJECTORY_SHA256 = (
    "4aaa1e944a2004b87c420d6a25d361bcd5316d992479d9a934cc1b10739b867a"
)
PRESERVATION_RECEIPT_SHA256 = (
    "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
)

ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    "baseline-v9-input-order-adapter-rejection-78e3008f"
)
PRESERVATION_RECEIPT_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    "baseline-v9-input-order-adapter-rejection-78e3008f-preservation-receipt.json"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_CLOSEOUT_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_preservation_closeout_review"
)


def pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "record_kind": "source_only_host_preservation_closeout",
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_main_tree": AUTHORIZED_MAIN_TREE,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
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
