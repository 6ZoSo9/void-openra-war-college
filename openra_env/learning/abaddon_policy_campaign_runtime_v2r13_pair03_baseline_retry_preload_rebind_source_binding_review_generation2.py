"""Source-only review of the pair-03 retry rebind to V2R13 model preload repair."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_invocation_generation2
    as retry,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry-preload-rebind-review-contract.v1"
)

REBOUND_RETRY_GIT_BLOB = "f75bcc19120db9044dbdafe629ab2c625b6a19a9"
REBOUND_RETRY_SOURCE_SHA256 = (
    "cc69c2c231f2c520184ddafe966989d23b002f853c1b3b9a311600cef5119b46"
)
REBOUND_RETRY_TEST_GIT_BLOB = "76620e62259670cc63ac1d254e0600a3dd828536"
REBOUND_RETRY_TEST_SHA256 = (
    "54cb2515d6d8901a90a0600a32229887459f67f1c9bff79445907b9fa61571d4"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_RETRY_FORENSICS_REQUIRED"
NEXT_CHANGE_CLASS = "precision_read_only_v2r13_pair03_baseline_failed_retry_forensics"


class V2R13Pair03BaselineRetryPreloadRebindReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetryPreloadRebindReviewHold(message)


@lru_cache(maxsize=1)
def _validate_retry_cached() -> dict[str, Any]:
    contract = retry.v2r13_pair03_baseline_retry_invocation_contract()

    _require(contract.get("pair_slot") == 3, "retry pair-slot drift")
    _require(contract.get("arm") == "baseline", "retry arm drift")
    _require(contract.get("retry_index") == 1, "retry index drift")
    _require(contract.get("max_retry_executions") == 1, "retry count drift")
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("worktree_readiness_repair_review_required") is True,
        "worktree repair review dependency missing",
    )
    _require(
        contract.get("model_preload_repair_review_required") is True,
        "model-preload repair review dependency missing",
    )
    _require(
        contract.get("exact_v2r13_model_preload_before_readiness_required") is True,
        "exact V2R13 model preload dependency missing",
    )
    _require(
        contract.get("model_preload_inference_forbidden") is True,
        "model-preload inference prohibition missing",
    )

    dependencies = contract.get("dependencies")
    _require(isinstance(dependencies, dict), "retry dependency bundle missing")
    worktree = dependencies.get("worktree_repair_review")
    preload = dependencies.get("model_preload_repair_review")
    _require(isinstance(worktree, dict), "worktree repair review missing")
    _require(isinstance(preload, dict), "model-preload repair review missing")
    _require(worktree.get("repair_reviewed") is True, "worktree repair not reviewed")
    _require(preload.get("repair_reviewed") is True, "model-preload repair not reviewed")
    _require(
        preload.get("exact_v2r13_model_preload_reviewed") is True,
        "model preload not reviewed",
    )
    _require(
        preload.get("model_inference_during_preload") is False,
        "model preload crosses inference boundary",
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
        _require(contract.get(field) is False, f"retry scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair03_baseline_retry_preload_rebind_review_contract() -> dict[str, Any]:
    validated = _validate_retry_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "rebound_retry_git_blob": REBOUND_RETRY_GIT_BLOB,
        "rebound_retry_source_sha256": REBOUND_RETRY_SOURCE_SHA256,
        "rebound_retry_test_git_blob": REBOUND_RETRY_TEST_GIT_BLOB,
        "rebound_retry_test_sha256": REBOUND_RETRY_TEST_SHA256,
        "retry_preload_rebind_source_binding_present": True,
        "retry_preload_rebind_reviewed": True,
        "worktree_readiness_repair_review_required": True,
        "model_preload_repair_review_required": True,
        "exact_v2r13_model_preload_before_readiness_required": True,
        "model_preload_inference_forbidden": True,
        "automatic_retry": False,
        "additional_retry_authorized": False,
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
        "failed_retry_forensics_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_retry_contract": validated,
    }


def execute_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineRetryPreloadRebindReviewHold(NEXT_GATE)
