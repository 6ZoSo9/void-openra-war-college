"""Source-only review of accepted pair-03 baseline retry-2 execution evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry2_execution_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry2-execution-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "037730c77bc67cbd722becc30fc898b50cba842b"
ACCEPTANCE_SOURCE_SHA256 = (
    "189f500b329c852c69da6b78736e0ae028ca5c77dd28875f79023852ed033695"
)
ACCEPTANCE_TEST_GIT_BLOB = "8b2a70e4368b60b6182ea29f6fa82906bc936881"
ACCEPTANCE_TEST_SHA256 = (
    "5514ab6de3928165d1ce23cb08e562250aba0541a4ce59ac9051d3a53ebe5147"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_RESULT_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_result_review"


class V2R13Pair03BaselineRetry2ExecutionEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetry2ExecutionEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = (
        acceptance
        .v2r13_pair03_baseline_retry2_execution_evidence_acceptance_contract()
    )
    _require(
        contract.get("retry2_execution_evidence_accepted") is True,
        "retry-2 evidence acceptance missing",
    )
    _require(
        contract.get("launcher_sha256")
        == "e48dff60a089ed3cfa75729ecaec60cb52d41037663eb46cb1a8929540ac833c",
        "retry-2 launcher SHA drift",
    )
    _require(
        contract.get("execution_main_head")
        == "3432cc19f7612f7e3819eefe2c207d302cd4b580",
        "retry-2 execution-main drift",
    )
    _require(
        contract.get("additional_retry_authorization_consumed") is True,
        "retry-2 authorization consumption missing",
    )
    _require(
        contract.get("remaining_additional_retry_executions") == 0,
        "retry-2 remaining execution count drift",
    )
    _require(
        contract.get("another_retry_authorized") is False,
        "acceptance unexpectedly authorizes another retry",
    )
    _require(
        contract.get("candidate_arm_authorized") is False,
        "acceptance unexpectedly authorizes candidate",
    )
    _require(
        contract.get("held_out_arm_authorized") is False,
        "acceptance unexpectedly authorizes held-out arm",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(contract.get("recursive_retry") is False, "recursive retry enabled")
    _require(
        contract.get("baseline_result_review_required") is True,
        "baseline result review requirement missing",
    )

    accepted = contract.get("accepted_evidence")
    _require(isinstance(accepted, dict), "accepted retry-2 evidence bundle missing")
    _require(accepted.get("retry_index") == 2, "accepted retry index drift")
    _require(
        accepted.get("runtime_execution_performed") is True,
        "accepted runtime execution missing",
    )
    _require(
        accepted.get("fresh_runtime_readiness_admitted") is True,
        "accepted fresh readiness missing",
    )
    _require(
        accepted.get("runtime_cleanup_completed") is True,
        "accepted runtime cleanup missing",
    )
    _require(
        accepted.get("outcome") == "DRAW_OR_UNFINISHED",
        "accepted baseline outcome drift",
    )
    _require(accepted.get("rounds_completed") == 36, "accepted round count drift")
    _require(
        accepted.get("candidate_arm_executed") is False,
        "candidate arm unexpectedly executed",
    )
    _require(
        accepted.get("held_out_arm_executed") is False,
        "held-out arm unexpectedly executed",
    )

    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        _require(accepted.get(field) is False, f"retry-2 evidence scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair03_baseline_retry2_execution_evidence_review_contract() -> dict[str, Any]:
    validated = _validate_acceptance_cached()
    accepted = validated["accepted_evidence"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_source_git_blob": ACCEPTANCE_SOURCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "retry2_execution_evidence_source_binding_present": True,
        "retry2_execution_evidence_reviewed": True,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 2,
        "outcome": "DRAW_OR_UNFINISHED",
        "rounds_completed": 36,
        "trajectory_sha256": accepted["trajectory_sha256"],
        "summary_sha256": accepted["summary_sha256"],
        "retry_authorization_consumed": True,
        "remaining_retry_executions": 0,
        "another_retry_authorized": False,
        "candidate_arm_authorized": False,
        "candidate_arm_executed": False,
        "held_out_arm_authorized": False,
        "held_out_arm_executed": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "automatic_policy_promotion": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "baseline_result_review_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_acceptance": validated,
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineRetry2ExecutionEvidenceReviewHold(NEXT_GATE)
