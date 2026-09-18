"""Source-only review of failed pair-03 baseline preservation.

Pins the exact preservation implementation, Precision CLI, and tests.  This
review performs no host mutation and grants no retry authority.  It advances
only to explicit failed-attempt preservation invocation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_generation2
    as preservation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-attempt-preservation-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-attempt-preservation-review.v1"
)

PRESERVATION_GIT_BLOB = "a00bea0b49121664988a80e85db10ea4496b0779"
PRESERVATION_SOURCE_SHA256 = (
    "6dae62de49f2757bbd216e22db9f42c983735fa47f90e85f26b8fa888ba1fdaf"
)
PRECISION_CLI_GIT_BLOB = "0e0fbf7b1bd76ea392a90c80bb9bcbfcb55fc17c"
PRECISION_CLI_SOURCE_SHA256 = (
    "d07eb7761f727df66bf61a8a29fb839a14c1e40b130dd0585e7a90179a83443b"
)
PRESERVATION_TEST_GIT_BLOB = "b742b2f56a72e2d8259213c61dff8c3cb81c5586"
PRESERVATION_TEST_SHA256 = (
    "54a20aee0cb55f096a2c9cc55b13fe961e6daf9e90ef34b24b5f450740ff5cb1"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_failed_attempt_preservation"


class V2R13Pair03BaselineFailedAttemptPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineFailedAttemptPreservationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_preservation_cached() -> dict[str, Any]:
    contract = preservation.v2r13_pair03_baseline_failed_attempt_preservation_contract()

    _require(
        contract.get("forensics_sha256")
        == "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d",
        "forensic identity drift",
    )
    _require(
        contract.get("warm_start_sha256")
        == "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28",
        "warm-start identity drift",
    )
    _require(contract.get("warm_start_bytes") == 223319, "warm-start byte drift")

    for field in (
        "exact_failed_tree_required",
        "atomic_same_filesystem_rename_implemented",
        "inode_identity_preservation_checked",
    ):
        _require(contract.get(field) is True, f"preservation requirement missing: {field}")

    for field in (
        "archived_tree_mutation_after_rename",
        "failed_attempt_deletion_implemented",
        "runtime_retry_implemented_by_this_source",
        "runtime_retry_authorized",
        "automatic_retry",
        "runtime_start_implemented",
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
        == "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pre-review preservation gate drift",
    )
    return deepcopy(contract)


def v2r13_pair03_baseline_failed_attempt_preservation_review() -> dict[str, Any]:
    validated = _validate_preservation_cached()
    return {
        "schema": REVIEW_SCHEMA,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "preservation_test_sha256": PRESERVATION_TEST_SHA256,
        "preservation_source_identity_pinned_by_git_blob": True,
        "preservation_source_identity_pinned_by_sha256": True,
        "precision_cli_identity_pinned": True,
        "preservation_test_identity_pinned": True,
        "separate_review_instrument": True,
        "preservation_reviewed": True,
        "failed_attempt_deletion_authorized": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "runtime_execution_performed": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_preservation_contract": validated,
    }


def v2r13_pair03_baseline_failed_attempt_preservation_review_contract() -> dict[str, Any]:
    review = v2r13_pair03_baseline_failed_attempt_preservation_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_source_sha256": PRESERVATION_SOURCE_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "preservation_test_sha256": PRESERVATION_TEST_SHA256,
        "preservation_source_binding_present": True,
        "preservation_reviewed": True,
        "preservation_invoked": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": review,
    }


def invoke_preservation(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineFailedAttemptPreservationReviewHold(NEXT_GATE)
