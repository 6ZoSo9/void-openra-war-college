"""Source-only review of the third pair-06 failed-attempt preservation gate."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_generation2
    as preservation,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-preservation-source-binding-review-contract.v1"
)

PRESERVATION_GIT_BLOB = "2c00cf095fcd3a675f84fe08b8b72346186fe06f"
PRESERVATION_SOURCE_SHA256 = (
    "bff90c9c8eb7080fe7c5db793ad6df25e897ee589b0445952abe255a2a8cba29"
)
PRESERVATION_TEST_GIT_BLOB = "563e1a6dbefc6af34426b9d32bd2d4711bd89b2d"
PRESERVATION_TEST_SHA256 = (
    "242a98aec886c36d94f91e5e1e764aa2a3e0a644a333ba6d66294e299878d175"
)

NEXT_GATE = "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_PRECISION_EXECUTION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_third_failed_attempt_preservation"


class Pair06V8ThirdFailedAttemptPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ThirdFailedAttemptPreservationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = preservation.pair06_v8_third_failed_attempt_preservation_contract()

    _require(
        out.get("forensics_acceptance_git_blob")
        == "053e311c286a904b26e3ef407e76e46b565d3c81",
        "third preservation forensic acceptance blob drift",
    )
    _require(
        out.get("forensics_acceptance_source_sha256")
        == "75a11e237915dd22eb15f6cf0347ad44bfe1644e667e1562e0827e9d57b15f0e",
        "third preservation forensic acceptance SHA drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3",
        "third preservation attempt marker drift",
    )
    _require(
        out.get("archive_name") == "baseline-3ad564f9",
        "third preservation archive name drift",
    )

    for field in (
        "marker_only_claims_required",
        "empty_runs_required",
        "exact_registered_clean_detached_worktrees_required",
        "non_force_worktree_removal_implemented",
        "atomic_same_filesystem_rename_implemented",
        "inode_identity_preservation_checked",
        "marker_rehashed_after_archive",
        "both_prior_failed_attempt_archives_revalidated_before_and_after",
    ):
        _require(out.get(field) is True, "third preservation invariant drift: " + field)

    _require(
        out.get("failed_attempt_deletion_implemented") is False,
        "third preservation unexpectedly deletes evidence",
    )
    _require(
        out.get("runtime_retry_implemented_by_this_source") is False
        and out.get("runtime_retry_authorized") is False
        and out.get("automatic_retry") is False,
        "third preservation unexpectedly authorizes retry",
    )

    for field in (
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
        _require(
            out.get(field) is False,
            "third preservation capability drift: " + field,
        )

    _require(
        out.get("next_gate")
        == "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "third preservation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_third_failed_attempt_preservation_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "preservation_test_sha256": PRESERVATION_TEST_SHA256,
        "pair06_v8_third_failed_attempt_preservation_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "archive_name": validated["archive_name"],
        "marker_only_claims_required": True,
        "empty_runs_required": True,
        "non_force_worktree_removal_required": True,
        "atomic_archive_rename_required": True,
        "evidence_inode_preservation_required": True,
        "prior_archives_must_remain_unchanged": True,
        "failed_attempt_deleted": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "model_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_preservation": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ThirdFailedAttemptPreservationReviewHold(NEXT_GATE)
