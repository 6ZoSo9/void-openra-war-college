"""Source-only review of accepted V2R13 pair-03 candidate execution evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-execution-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "79f9a674272a2bf67f315d79cc61778a8f53408d"
ACCEPTANCE_SOURCE_SHA256 = (
    "97d5d6127fa450207e32d4262d21490d8bcc15633779644142af27fdba8d57de"
)
ACCEPTANCE_TEST_GIT_BLOB = "cb35ebdddcefa6110baf3b1fa5d63df60911fcfc"
ACCEPTANCE_TEST_SHA256 = (
    "e087428b5a9469ec234ba0cdc32f4010e1f0405655c1140d750e142a82f86317"
)

NEXT_GATE = "V2R13_PAIR03_CANDIDATE_RESULT_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_candidate_result_review"


class V2R13Pair03CandidateExecutionEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidateExecutionEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = acceptance.v2r13_pair03_candidate_execution_evidence_acceptance_contract()
    _require(
        contract.get("candidate_execution_evidence_accepted") is True,
        "candidate evidence acceptance missing",
    )
    _require(contract.get("pair_slot") == 3, "candidate pair-slot drift")
    _require(contract.get("arm") == "candidate", "candidate arm drift")
    _require(contract.get("held_out") is False, "candidate held-out drift")
    _require(
        contract.get("candidate_attempt_consumed") is True,
        "candidate attempt consumption missing",
    )
    _require(
        contract.get("candidate_execution_performed") is True,
        "candidate execution missing",
    )
    _require(
        contract.get("candidate_completed_result_present") is True,
        "candidate completed result missing",
    )
    _require(
        contract.get("candidate_execution_replay_required") is False,
        "candidate replay unexpectedly required",
    )
    _require(
        contract.get("candidate_execution_replay_permitted") is False,
        "candidate replay unexpectedly permitted",
    )
    _require(
        contract.get("runtime_cleanup_completed") is True,
        "candidate runtime cleanup missing",
    )
    _require(
        contract.get("fresh_runtime_readiness_admitted") is True,
        "candidate fresh readiness missing",
    )
    _require(
        contract.get("completed_baseline_preserved") is True,
        "candidate run did not preserve baseline",
    )
    _require(
        contract.get("outcome") == "DRAW_OR_UNFINISHED",
        "candidate outcome drift",
    )
    _require(contract.get("rounds_completed") == 36, "candidate round-count drift")
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("another_candidate_execution_authorized") is False,
        "another candidate execution unexpectedly authorized",
    )
    _require(
        contract.get("pair09_execution_authorized") is False,
        "pair09 execution unexpectedly authorized",
    )
    _require(
        contract.get("held_out_execution_authorized") is False,
        "held-out execution unexpectedly authorized",
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
        _require(contract.get(field) is False, f"candidate evidence scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair03_candidate_execution_evidence_review_contract() -> dict[str, Any]:
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
        "pair_slot": 3,
        "arm": "candidate",
        "held_out": False,
        "execution_main_head": accepted["execution_main_head"],
        "validation_main_head": accepted["validation_main_head"],
        "outcome": accepted["outcome"],
        "rounds_completed": accepted["rounds_completed"],
        "seed": accepted["seed"],
        "run_id": accepted["run_id"],
        "trajectory_sha256": accepted["trajectory_sha256"],
        "summary_sha256": accepted["summary_sha256"],
        "baseline_trajectory_sha256": accepted["baseline_trajectory_sha256"],
        "baseline_summary_sha256": accepted["baseline_summary_sha256"],
        "candidate_attempt_consumed": True,
        "candidate_execution_performed": True,
        "candidate_completed_result_present": True,
        "candidate_execution_replay_required": False,
        "candidate_execution_replay_permitted": False,
        "runtime_cleanup_completed": True,
        "fresh_runtime_readiness_admitted": True,
        "completed_baseline_preserved": True,
        "automatic_retry": False,
        "another_candidate_execution_authorized": False,
        "pair09_execution_authorized": False,
        "held_out_execution_authorized": False,
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
        "validated_acceptance": deepcopy(validated),
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidateExecutionEvidenceReviewHold(NEXT_GATE)
