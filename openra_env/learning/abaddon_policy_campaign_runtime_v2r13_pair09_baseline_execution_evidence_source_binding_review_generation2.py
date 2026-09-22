"""Source-only review of accepted V2R13 pair-09 baseline execution evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_execution_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-execution-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "cba3efec7f8884065b412d362f05048ccb2f2887"
ACCEPTANCE_SOURCE_SHA256 = (
    "b3f5089079b01ba4f9ec928c20a094dabccfd506ae0d3827c32a8cc985d9030d"
)
ACCEPTANCE_TEST_GIT_BLOB = "deb05a86cda34d75486fe0a2e53785add85784bc"
ACCEPTANCE_TEST_SHA256 = (
    "e7c8041d05208ac747963b4cc738987e2bb69b490bd13eb861efa0488eedaacb"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_RESULT_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_baseline_result_review"


class V2R13Pair09BaselineExecutionEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineExecutionEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = (
        acceptance
        .v2r13_pair09_baseline_execution_evidence_acceptance_contract()
    )
    _require(
        contract.get("pair09_baseline_execution_evidence_accepted") is True,
        "pair09 baseline evidence acceptance missing",
    )
    _require(
        contract.get("launcher_sha256")
        == "1ef774f2de9323eb7ef01762574d1fc8ec1df8b557bf9b6e083028ca2388a945",
        "pair09 launcher SHA drift",
    )
    _require(
        contract.get("execution_main_head")
        == "361b5e8a4033515d6bdd3a7f50456c778df5aa5f",
        "pair09 execution-main drift",
    )
    _require(contract.get("attempt_consumed") is True, "pair09 attempt not consumed")
    _require(contract.get("maximum_attempts") == 1, "pair09 attempt cardinality drift")
    _require(
        contract.get("another_baseline_execution_authorized") is False,
        "another pair09 baseline execution unexpectedly authorized",
    )
    _require(
        contract.get("candidate_execution_authorized") is False,
        "pair09 candidate prematurely authorized",
    )
    _require(
        contract.get("held_out_execution_authorized") is False,
        "held-out execution prematurely authorized",
    )
    _require(contract.get("automatic_retry") is False, "pair09 automatic retry enabled")
    _require(
        contract.get("baseline_result_review_required") is True,
        "pair09 baseline result review requirement missing",
    )

    accepted = contract.get("accepted_evidence")
    _require(isinstance(accepted, dict), "accepted pair09 evidence missing")
    _require(accepted.get("pair_slot") == 9, "accepted pair09 slot drift")
    _require(accepted.get("arm") == "baseline", "accepted pair09 arm drift")
    _require(accepted.get("held_out") is False, "accepted pair09 held-out drift")
    _require(
        accepted.get("runtime_execution_performed") is True,
        "accepted pair09 runtime execution missing",
    )
    _require(
        accepted.get("fresh_runtime_readiness_admitted") is True,
        "accepted pair09 fresh readiness missing",
    )
    _require(
        accepted.get("runtime_cleanup_completed") is True,
        "accepted pair09 runtime cleanup missing",
    )
    _require(
        accepted.get("outcome") == "DRAW_OR_UNFINISHED",
        "accepted pair09 outcome drift",
    )
    _require(
        accepted.get("rounds_completed") == 36,
        "accepted pair09 round count drift",
    )
    _require(
        accepted.get("pair03_baseline_preserved") is True
        and accepted.get("pair03_candidate_preserved") is True,
        "pair03 preserved evidence drift",
    )
    _require(
        accepted.get("candidate_execution_performed") is False,
        "pair09 candidate unexpectedly executed",
    )
    _require(
        accepted.get("held_out_execution_performed") is False,
        "held-out unexpectedly executed",
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
        _require(accepted.get(field) is False, f"pair09 evidence scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair09_baseline_execution_evidence_review_contract() -> dict[str, Any]:
    validated = _validate_acceptance_cached()
    accepted = validated["accepted_evidence"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_source_git_blob": ACCEPTANCE_SOURCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "pair09_baseline_execution_evidence_source_binding_present": True,
        "pair09_baseline_execution_evidence_reviewed": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "attempt_consumed": True,
        "maximum_attempts": 1,
        "outcome": accepted["outcome"],
        "rounds_completed": accepted["rounds_completed"],
        "final_tick": accepted["final_tick"],
        "warm_start_sha256": accepted["warm_start_sha256"],
        "trajectory_sha256": accepted["trajectory_sha256"],
        "summary_sha256": accepted["summary_sha256"],
        "result_file_sha256": accepted["result_file_sha256"],
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "pair03_baseline_preserved": True,
        "pair03_candidate_preserved": True,
        "another_baseline_execution_authorized": False,
        "candidate_execution_authorized": False,
        "candidate_execution_performed": False,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
        "automatic_retry": False,
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
    raise V2R13Pair09BaselineExecutionEvidenceReviewHold(NEXT_GATE)
