"""Source-only review of the one-shot V2R13 pair-03 baseline retry invocation."""

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
    "v2r13-pair03-baseline-retry-invocation-review-contract.v1"
)

RETRY_INVOCATION_GIT_BLOB = "8a4db072d6238e7820d1b94048d0df151002de7b"
RETRY_INVOCATION_SOURCE_SHA256 = (
    "7caf6bfe0c5cf7c1e4df1d1f196cac7b5488d25ac119c5d841b59d81eb76934e"
)
PRECISION_CLI_GIT_BLOB = "d9d30a856e958b423951fc602e55b7b24926f3ab"
PRECISION_CLI_SOURCE_SHA256 = (
    "84bbf23334fbe154b16345a2f60fa5763f9a1c9f3f5714bc1be6e186b0872935"
)
RETRY_TEST_GIT_BLOB = "c8db66b3db36c359f54376a9186ad4a5f6096e13"
RETRY_TEST_SHA256 = (
    "6f87962e39d03ad0386def73e36463b8baa0a71ece7d2decb1ee4c0c9783bcd7"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_retry_invocation"


class V2R13Pair03BaselineRetryInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetryInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_retry_cached() -> dict[str, Any]:
    contract = retry.v2r13_pair03_baseline_retry_invocation_contract()

    _require(contract.get("pair_slot") == 3, "retry pair-slot drift")
    _require(contract.get("arm") == "baseline", "retry arm drift")
    _require(contract.get("held_out") is False, "retry baseline became held-out")
    _require(contract.get("retry_index") == 1, "retry index drift")
    _require(contract.get("max_retry_executions") == 1, "retry count drift")
    _require(contract.get("live_preservation_recheck_required") is True, "live preservation recheck missing")
    _require(contract.get("repaired_first_baseline_executor_reused") is True, "repaired executor reuse missing")
    _require(contract.get("retry_execution_authorized") is True, "retry authority missing")
    _require(
        contract.get("retry_execution_performed_by_contract_inspection") is False,
        "retry executed during source inspection",
    )
    _require(
        contract.get("remaining_retry_executions_before_invocation") == 1,
        "remaining retry count drift",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")

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

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pre-review retry gate drift",
    )
    return deepcopy(contract)


def v2r13_pair03_baseline_retry_invocation_review_contract() -> dict[str, Any]:
    validated = _validate_retry_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "retry_invocation_git_blob": RETRY_INVOCATION_GIT_BLOB,
        "retry_invocation_source_sha256": RETRY_INVOCATION_SOURCE_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "retry_test_git_blob": RETRY_TEST_GIT_BLOB,
        "retry_test_sha256": RETRY_TEST_SHA256,
        "retry_invocation_source_binding_present": True,
        "retry_invocation_reviewed": True,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 1,
        "max_retry_executions": 1,
        "live_preservation_recheck_reviewed": True,
        "repaired_first_baseline_executor_reuse_reviewed": True,
        "retry_execution_authorized": True,
        "retry_execution_invoked": False,
        "retry_execution_performed": False,
        "automatic_retry": False,
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
        "validated_retry_contract": validated,
    }


def invoke_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineRetryInvocationReviewHold(NEXT_GATE)
