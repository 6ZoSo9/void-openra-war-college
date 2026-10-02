"""Exact-blob review of the completed failed-attempt preservation closeout.

Pins the source-only closeout and focused tests. The review closes the consumed
input-order failure and its preservation authorization permanently.

It grants no runtime retry, replay, training, deployment, chain, wallet/funds,
or scheduler authority. A later fresh execution request must use the distinct
adapter-rejection lineage and must obtain its own fresh execution authorization.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_closeout_generation2
    as closeout,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-closeout-review.v1"
)

ACCEPTED_BASE_HEAD = "43f95480eafa642c8203552fbc00d8edd522d74c"

CLOSEOUT_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_closeout_generation2.py"
)
CLOSEOUT_GIT_BLOB = "674d9c9925d4c95c6f48875e8065eae9fe7a6cc8"

CLOSEOUT_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_closeout_generation2.py"
)
CLOSEOUT_TEST_GIT_BLOB = "c5286a4849a9d94619bd7483704dbece295cfe1c"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FRESH_EXECUTION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_fresh_execution_request"
)


class Pair06V9AdapterRejectionPreservationCloseoutReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionPreservationCloseoutReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = closeout.pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()

    _require(
        out.get("record_kind") == "source_only_host_preservation_closeout",
        "preservation closeout record kind drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
        and out.get("preservation_receipt_sha256")
        == "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181",
        "preservation closeout artifact identity drift",
    )
    _require(
        out.get("attempt_consumed") is True
        and out.get("attempt_reusable") is False
        and out.get("attempt_authorization_reusable") is False
        and out.get("preservation_authorization_consumed") is True
        and out.get("preservation_authorization_reusable") is False,
        "preservation closeout lineage reuse drift",
    )
    for field in (
        "archive_atomic_rename_performed",
        "attempt_marker_inode_preserved",
        "warm_start_inode_preserved",
        "trajectory_inode_preserved",
        "single_authorized_preservation_consumed",
        "runtime_output_observed",
    ):
        _require(out.get(field) is True, "preservation closeout invariant drift: " + field)

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
        _require(out.get(field) is False, "preservation closeout boundary drift: " + field)

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


def pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "closeout_path": CLOSEOUT_PATH,
        "closeout_git_blob": CLOSEOUT_GIT_BLOB,
        "closeout_test_path": CLOSEOUT_TEST_PATH,
        "closeout_test_git_blob": CLOSEOUT_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_reviewed": True,
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
    raise Pair06V9AdapterRejectionPreservationCloseoutReviewHold(NEXT_GATE)
