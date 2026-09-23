"""Source-only review of consumed pair-06 V8 failed-attempt preservation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_generation2
    as preservation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-review-contract.v1"
)

PRESERVATION_GIT_BLOB = "ff4de10454fc958d5ca459bd7a3eea6a27a17e64"
PRESERVATION_SOURCE_SHA256 = (
    "05f11516233d7c602244878e8aa066f1a8aae7ea59e3c0641f0cbe494f518c26"
)
PRESERVATION_TEST_GIT_BLOB = "25cd570a90b105e3eca8e95d84e8547e37ff0b26"
PRESERVATION_TEST_SHA256 = (
    "d2f1845dcb29b1f62618e34c36532ae62613f66a6138304937b7ee93df48fb62"
)

NEXT_GATE = "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_pair06_v8_failed_attempt_preservation"


class Pair06V8FailedAttemptPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8FailedAttemptPreservationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_cached() -> dict[str, Any]:
    contract = preservation.pair06_v8_failed_attempt_preservation_contract()
    _require(
        contract.get("attempt_marker_sha256")
        == "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930",
        "pair06 failed-attempt marker drift",
    )
    for field in (
        "exact_failed_tree_required",
        "exact_registered_clean_detached_worktrees_required",
        "non_force_worktree_removal_implemented",
        "atomic_same_filesystem_rename_implemented",
        "inode_identity_preservation_checked",
        "marker_warm_start_trajectory_rehashed_after_archive",
    ):
        _require(contract.get(field) is True, f"preservation invariant drift: {field}")

    for field in (
        "failed_attempt_deletion_implemented",
        "runtime_retry_implemented_by_this_source",
        "runtime_retry_authorized",
        "automatic_retry",
        "runtime_start_implemented",
        "model_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "training_implemented",
        "weights_update_implemented",
        "automatic_policy_promotion_implemented",
        "deployment_implemented",
        "void_chain_mutation_implemented",
        "wallet_or_funds_action_implemented",
    ):
        _require(contract.get(field) is False, f"preservation boundary drift: {field}")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "preservation review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_failed_attempt_preservation_review_contract() -> dict[str, Any]:
    validated = _validate_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "preservation_test_sha256": PRESERVATION_TEST_SHA256,
        "pair06_v8_failed_attempt_preservation_source_binding_present": True,
        "pair06_v8_failed_attempt_preservation_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "failed_attempt_deletion_authorized": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_preservation": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def invoke_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8FailedAttemptPreservationReviewHold(NEXT_GATE)
