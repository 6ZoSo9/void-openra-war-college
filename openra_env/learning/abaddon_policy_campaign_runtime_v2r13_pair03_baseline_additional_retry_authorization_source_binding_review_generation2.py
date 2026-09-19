"""Source-only review of one additional pair-03 baseline retry authorization."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_authorization_acceptance_generation2
    as authorization,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-additional-retry-authorization-review-contract.v1"
)

AUTHORIZATION_GIT_BLOB = "231d234462a701a89be6cf8201f7fce738e929c5"
AUTHORIZATION_SOURCE_SHA256 = (
    "373988ef8981dadbbc83c5d0a5aeae4b137c110dd2699692067f979079a96c4a"
)
AUTHORIZATION_TEST_GIT_BLOB = "19534bc00e64e67537d431c5b785657d77f0fb50"
AUTHORIZATION_TEST_SHA256 = (
    "b3ea36f3bc1e6807b778bed33f17cb9969dd9a8ae2f485b7a993661a0656f3ab"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_additional_retry_invocation"


class V2R13Pair03BaselineAdditionalRetryAuthorizationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineAdditionalRetryAuthorizationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_authorization_cached() -> dict[str, Any]:
    contract = (
        authorization
        .v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract()
    )

    _require(contract.get("pair_slot") == 3, "additional retry pair-slot drift")
    _require(contract.get("arm") == "baseline", "additional retry arm drift")
    _require(contract.get("held_out") is False, "additional retry became held-out")
    _require(contract.get("retry_index") == 2, "additional retry index drift")
    _require(
        contract.get("additional_retry_authorization_accepted") is True,
        "additional retry authorization missing",
    )
    _require(
        contract.get("authorization_scope")
        == "exactly_one_additional_pair03_baseline_retry",
        "additional retry authorization scope drift",
    )
    _require(
        contract.get("max_additional_retry_executions") == 1,
        "additional retry count drift",
    )
    _require(
        contract.get("total_retry_executions_authorized") == 2,
        "total retry authorization count drift",
    )
    _require(
        contract.get("prior_retry_authorization_consumed") is True,
        "prior retry authorization consumption missing",
    )
    _require(
        contract.get("failed_retry_preservation_evidence_reviewed") is True,
        "failed retry preservation evidence review missing",
    )
    _require(
        contract.get("automatic_retry") is False,
        "automatic retry enabled",
    )
    _require(
        contract.get("additional_retry_execution_authorized_now") is False,
        "acceptance source prematurely authorizes execution",
    )
    _require(
        contract.get("additional_retry_execution_performed") is False,
        "acceptance source unexpectedly records execution",
    )

    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"additional retry scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair03_baseline_additional_retry_authorization_review_contract() -> dict[str, Any]:
    validated = _validate_authorization_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_git_blob": AUTHORIZATION_GIT_BLOB,
        "authorization_source_sha256": AUTHORIZATION_SOURCE_SHA256,
        "authorization_test_git_blob": AUTHORIZATION_TEST_GIT_BLOB,
        "authorization_test_sha256": AUTHORIZATION_TEST_SHA256,
        "authorization_source_binding_present": True,
        "authorization_reviewed": True,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 2,
        "single_additional_pair03_baseline_retry_authorized": True,
        "max_additional_retry_executions": 1,
        "total_retry_executions_authorized": 2,
        "automatic_retry": False,
        "additional_retry_execution_authorized_now": True,
        "additional_retry_execution_performed": False,
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
        "validated_authorization": validated,
    }


def execute_additional_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineAdditionalRetryAuthorizationReviewHold(NEXT_GATE)
