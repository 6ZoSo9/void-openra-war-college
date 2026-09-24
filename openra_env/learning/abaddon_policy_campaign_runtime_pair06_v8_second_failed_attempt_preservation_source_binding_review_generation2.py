"""Source-only review of second consumed pair-06 V8 failed-attempt preservation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_generation2
    as preservation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-preservation-review-contract.v1"
)

PRESERVATION_GIT_BLOB = "653521100d1b88f84e16cb1a233b3a9da48fee17"
PRESERVATION_SOURCE_SHA256 = (
    "888228244f81370f0f1199e2c5f9de7a6281da178f3e119bff93d2718adbcd4c"
)
PRESERVATION_TEST_GIT_BLOB = "5be94aa349219daebbf6f9d2bade37312930524f"
PRESERVATION_TEST_SHA256 = (
    "8bcd5c5e6de6d872e85e35f32e6f6f65839ff1b0dcdc813509f4900a7937d437"
)

NEXT_GATE = "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_pair06_v8_second_failed_attempt_preservation"


class Pair06V8SecondFailedAttemptPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8SecondFailedAttemptPreservationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = preservation.pair06_v8_second_failed_attempt_preservation_contract()
    _require(
        out.get("attempt_marker_sha256")
        == "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1",
        "second failed-attempt marker drift",
    )
    _require(
        out.get("archive_name") == "baseline-20260923T235031Z-446d8f92",
        "second failed-attempt archive name drift",
    )
    for field in (
        "exact_failed_tree_required",
        "exact_registered_clean_detached_worktrees_required",
        "non_force_worktree_removal_implemented",
        "atomic_same_filesystem_rename_implemented",
        "inode_identity_preservation_checked",
        "marker_warm_start_trajectory_rehashed_after_archive",
        "prior_failed_attempt_archive_revalidated_before_and_after",
    ):
        _require(out.get(field) is True, f"second preservation invariant drift: {field}")

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
        _require(out.get(field) is False, f"second preservation boundary drift: {field}")

    _require(
        out.get("next_gate")
        == "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "second preservation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_second_failed_attempt_preservation_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "preservation_test_sha256": PRESERVATION_TEST_SHA256,
        "pair06_v8_second_failed_attempt_preservation_source_binding_present": True,
        "pair06_v8_second_failed_attempt_preservation_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "archive_name": validated["archive_name"],
        "prior_failed_attempt_archive_revalidated_before_and_after": True,
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
    raise Pair06V8SecondFailedAttemptPreservationReviewHold(NEXT_GATE)
