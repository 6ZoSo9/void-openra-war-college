"""Source-only review of the one-shot pair-03 baseline retry-2 invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_invocation_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-additional-retry-invocation-review-contract.v1"
)

INVOCATION_GIT_BLOB = "a00a5b0a206203298386121b79f30234465a4c16"
INVOCATION_SOURCE_SHA256 = (
    "29e31bfe025ca9c1d57081e59d16c11373e5d9550757b872b9467e87e8975104"
)
PRECISION_CLI_GIT_BLOB = "5556ad98ff2c82bd8792ae79aa092f16334f4db4"
PRECISION_CLI_SOURCE_SHA256 = (
    "2ffd9a916752e0587e156180d796d6b299d47dec93130f9da2f9bce754b6c2e8"
)
INVOCATION_TEST_GIT_BLOB = "01b272ba4d58f8698489c7873532c856757d25f2"
INVOCATION_TEST_SHA256 = (
    "c5597ee7f6577733c99824ad328fe569b5d335dd104a0c6c8568a57b87807d4e"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_additional_retry_invocation"


class V2R13Pair03BaselineAdditionalRetryInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineAdditionalRetryInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_invocation_cached() -> dict[str, Any]:
    contract = invocation.v2r13_pair03_baseline_additional_retry_invocation_contract()

    _require(contract.get("pair_slot") == 3, "retry-2 pair-slot drift")
    _require(contract.get("arm") == "baseline", "retry-2 arm drift")
    _require(contract.get("held_out") is False, "retry-2 became held-out")
    _require(contract.get("retry_index") == 2, "retry-2 index drift")
    _require(
        contract.get("max_additional_retry_executions") == 1,
        "retry-2 count drift",
    )
    _require(
        contract.get("total_retry_executions_authorized") == 2,
        "total retry authorization count drift",
    )
    _require(
        contract.get("live_preserved_history_recheck_required") is True,
        "live preserved-history recheck missing",
    )
    _require(
        contract.get("first_failed_attempt_archive_recheck_required") is True,
        "first failed-attempt archive recheck missing",
    )
    _require(
        contract.get("retry1_failed_attempt_archive_recheck_required") is True,
        "retry-1 failed-attempt archive recheck missing",
    )
    _require(
        contract.get("repaired_first_baseline_executor_reused") is True,
        "repaired first-baseline executor reuse missing",
    )
    _require(
        contract.get("worktree_readiness_repair_review_required") is True,
        "worktree readiness repair dependency missing",
    )
    _require(
        contract.get("model_preload_repair_review_required") is True,
        "model preload repair dependency missing",
    )
    _require(
        contract.get("exact_v2r13_model_preload_before_readiness_required") is True,
        "exact V2R13 model preload requirement missing",
    )
    _require(
        contract.get("model_preload_inference_forbidden") is True,
        "model preload inference prohibition missing",
    )
    _require(
        contract.get("additional_retry_execution_authorized") is True,
        "retry-2 execution authorization missing",
    )
    _require(
        contract.get("additional_retry_execution_performed_by_contract_inspection")
        is False,
        "retry-2 unexpectedly executed during review",
    )
    _require(
        contract.get("remaining_additional_retry_executions_before_invocation") == 1,
        "retry-2 remaining execution count drift",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("recursive_retry_implemented") is False,
        "recursive retry implemented",
    )

    for field in (
        "candidate_arm_implemented_by_this_source",
        "held_out_arm_implemented_by_this_source",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"retry-2 scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair03_baseline_additional_retry_invocation_review_contract() -> dict[str, Any]:
    validated = _validate_invocation_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "invocation_source_binding_present": True,
        "invocation_reviewed": True,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 2,
        "single_additional_retry_invocation_reviewed": True,
        "live_preserved_history_recheck_reviewed": True,
        "first_failed_attempt_archive_recheck_reviewed": True,
        "retry1_failed_attempt_archive_recheck_reviewed": True,
        "repaired_readiness_path_reviewed": True,
        "automatic_retry": False,
        "recursive_retry": False,
        "runtime_execution_invoked": False,
        "runtime_execution_performed": False,
        "candidate_arm_authorized": False,
        "held_out_arm_authorized": False,
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
        "validated_invocation": validated,
    }


def execute_additional_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineAdditionalRetryInvocationReviewHold(NEXT_GATE)
