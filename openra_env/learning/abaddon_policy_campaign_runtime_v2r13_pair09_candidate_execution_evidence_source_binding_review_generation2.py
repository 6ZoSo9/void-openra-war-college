"""Source-only review of accepted V2R13 pair-09 candidate execution evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_execution_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-execution-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "6ef46ea61b3725c846c56ebc16d7bdf3b8d8fcc9"
ACCEPTANCE_SOURCE_SHA256 = (
    "408edb01b2bc50f6ed56c8c00de17476172056d52cd4a8f2d65b4e31d77809e1"
)
ACCEPTANCE_TEST_GIT_BLOB = "9ff4bff07170beeab6a3c86f7c5cc63624193802"
ACCEPTANCE_TEST_SHA256 = (
    "689feeffa60a66e2ecb2664baad6ab19da54a2170030a2b66c1c1967a9af27f0"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_RESULT_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_result_review"


class V2R13Pair09CandidateExecutionEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateExecutionEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = (
        acceptance
        .v2r13_pair09_candidate_execution_evidence_acceptance_contract()
    )
    _require(
        contract.get("pair09_candidate_execution_evidence_accepted") is True,
        "pair09 candidate evidence acceptance missing",
    )
    _require(
        contract.get("launcher_sha256")
        == "0705afdb696da7e2c3208f981a13a4e179548e9c526352475728001486137d94",
        "pair09 candidate launcher SHA drift",
    )
    _require(
        contract.get("execution_main_head")
        == "7d5bf4c41c8a210a05fd9948f898c6cd8e5702d5",
        "pair09 candidate execution-main drift",
    )
    _require(contract.get("attempt_consumed") is True, "candidate attempt not consumed")
    _require(contract.get("maximum_attempts") == 1, "candidate attempt cardinality drift")
    _require(
        contract.get("candidate_execution_replay_permitted") is False,
        "candidate replay unexpectedly permitted",
    )
    _require(
        contract.get("another_candidate_execution_authorized") is False,
        "another candidate execution unexpectedly authorized",
    )
    _require(
        contract.get("held_out_execution_authorized") is False,
        "held-out execution unexpectedly authorized",
    )
    _require(contract.get("automatic_retry") is False, "candidate automatic retry enabled")
    _require(
        contract.get("candidate_result_review_required") is True,
        "candidate result review requirement missing",
    )

    accepted = contract.get("accepted_evidence")
    _require(isinstance(accepted, dict), "accepted pair09 candidate evidence missing")
    _require(accepted.get("pair_slot") == 9, "accepted pair09 candidate slot drift")
    _require(accepted.get("arm") == "candidate", "accepted pair09 candidate arm drift")
    _require(accepted.get("held_out") is False, "accepted pair09 candidate held-out drift")
    _require(
        accepted.get("runtime_execution_performed") is True,
        "accepted candidate runtime execution missing",
    )
    _require(
        accepted.get("fresh_runtime_readiness_admitted") is True,
        "accepted candidate fresh readiness missing",
    )
    _require(
        accepted.get("runtime_cleanup_completed") is True,
        "accepted candidate runtime cleanup missing",
    )
    _require(
        accepted.get("outcome") == "DRAW_OR_UNFINISHED",
        "accepted candidate outcome drift",
    )
    _require(
        accepted.get("rounds_completed") == 36,
        "accepted candidate round count drift",
    )
    _require(
        accepted.get("candidate_genome_sha256")
        == "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089",
        "accepted candidate genome drift",
    )
    _require(
        accepted.get("pair03_baseline_preserved") is True
        and accepted.get("pair03_candidate_preserved") is True
        and accepted.get("pair09_baseline_preserved") is True,
        "preserved predecessor evidence drift",
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
        _require(accepted.get(field) is False, f"candidate evidence scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair09_candidate_execution_evidence_review_contract() -> dict[str, Any]:
    validated = _validate_acceptance_cached()
    accepted = validated["accepted_evidence"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_source_git_blob": ACCEPTANCE_SOURCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "candidate_execution_evidence_source_binding_present": True,
        "candidate_execution_evidence_reviewed": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "attempt_consumed": True,
        "maximum_attempts": 1,
        "outcome": accepted["outcome"],
        "rounds_completed": accepted["rounds_completed"],
        "final_tick": accepted["final_tick"],
        "seed": accepted["seed"],
        "warm_start_sha256": accepted["warm_start_sha256"],
        "trajectory_sha256": accepted["trajectory_sha256"],
        "summary_sha256": accepted["summary_sha256"],
        "result_file_sha256": accepted["result_file_sha256"],
        "candidate_file_sha256": accepted["candidate_file_sha256"],
        "candidate_genome_sha256": accepted["candidate_genome_sha256"],
        "wrapper_sha256": accepted["wrapper_sha256"],
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "pair03_baseline_preserved": True,
        "pair03_candidate_preserved": True,
        "pair09_baseline_preserved": True,
        "candidate_execution_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
        "automatic_retry": False,
        "baseline_rerun": False,
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
        "candidate_result_review_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_acceptance": validated,
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateExecutionEvidenceReviewHold(NEXT_GATE)
