"""Review the completed V2R13 pair-03 baseline measurement.

This source consumes independently reviewed retry-2 execution evidence and
classifies the baseline measurement as complete but non-decisive at the round
limit. It does not authorize or execute the candidate arm, another retry,
training, weight changes, promotion, deployment, VOID mutation, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry2_execution_evidence_source_binding_review_generation2
    as evidence_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-result-review-contract.v1"
)

RETRY2_EVIDENCE_REVIEW_GIT_BLOB = "680ca2f26b5214aef13423cfb62ae7b0874a2080"
RETRY2_EVIDENCE_REVIEW_SOURCE_SHA256 = (
    "5df776e043413f9418e3f3732197f0e519717e40cdd54a372b41a603d3a0568d"
)
RETRY2_EVIDENCE_REVIEW_TEST_GIT_BLOB = (
    "954aae23d4c97dd3ba186242105099b0b6e86186"
)
RETRY2_EVIDENCE_REVIEW_TEST_SHA256 = (
    "22ef74770e929ec71f5bec0c8df9d7fd59725e7424ecb7fc3f36b48c466132d3"
)

NEXT_GATE = "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_candidate_execution_authorization"


class V2R13Pair03BaselineResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineResultReviewHold(message)


@lru_cache(maxsize=1)
def _validate_evidence_review_cached() -> dict[str, Any]:
    reviewed = (
        evidence_review
        .v2r13_pair03_baseline_retry2_execution_evidence_review_contract()
    )

    _require(
        reviewed.get("retry2_execution_evidence_source_binding_present") is True,
        "retry-2 evidence review binding missing",
    )
    _require(
        reviewed.get("retry2_execution_evidence_reviewed") is True,
        "retry-2 evidence not reviewed",
    )
    _require(reviewed.get("pair_slot") == 3, "baseline result pair-slot drift")
    _require(reviewed.get("arm") == "baseline", "baseline result arm drift")
    _require(reviewed.get("retry_index") == 2, "baseline result retry-index drift")
    _require(
        reviewed.get("outcome") == "DRAW_OR_UNFINISHED",
        "baseline outcome drift",
    )
    _require(reviewed.get("rounds_completed") == 36, "baseline round-count drift")
    _require(
        reviewed.get("retry_authorization_consumed") is True,
        "retry authorization consumption missing",
    )
    _require(
        reviewed.get("remaining_retry_executions") == 0,
        "retry authority is not exhausted",
    )
    _require(
        reviewed.get("another_retry_authorized") is False,
        "another retry unexpectedly authorized",
    )
    _require(
        reviewed.get("candidate_arm_authorized") is False,
        "candidate arm prematurely authorized",
    )
    _require(
        reviewed.get("candidate_arm_executed") is False,
        "candidate arm prematurely executed",
    )
    _require(
        reviewed.get("held_out_arm_authorized") is False,
        "held-out arm prematurely authorized",
    )
    _require(
        reviewed.get("held_out_arm_executed") is False,
        "held-out arm prematurely executed",
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
        _require(reviewed.get(field) is False, f"baseline review scope drift: {field}")

    return deepcopy(reviewed)


def v2r13_pair03_baseline_result_review_contract() -> dict[str, Any]:
    reviewed = _validate_evidence_review_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "retry2_evidence_review_git_blob": RETRY2_EVIDENCE_REVIEW_GIT_BLOB,
        "retry2_evidence_review_source_sha256": (
            RETRY2_EVIDENCE_REVIEW_SOURCE_SHA256
        ),
        "retry2_evidence_review_test_git_blob": (
            RETRY2_EVIDENCE_REVIEW_TEST_GIT_BLOB
        ),
        "retry2_evidence_review_test_sha256": (
            RETRY2_EVIDENCE_REVIEW_TEST_SHA256
        ),
        "baseline_result_reviewed": True,
        "pair_slot": 3,
        "arm": "baseline",
        "baseline_measurement_complete": True,
        "baseline_measurement_reproducibly_bound": True,
        "baseline_game_outcome": "DRAW_OR_UNFINISHED",
        "baseline_game_outcome_decisive": False,
        "baseline_round_limit_reached": True,
        "baseline_rounds_completed": 36,
        "baseline_trajectory_sha256": reviewed["trajectory_sha256"],
        "baseline_summary_sha256": reviewed["summary_sha256"],
        "baseline_valid_for_pairwise_comparison": True,
        "retry_authority_exhausted": True,
        "another_retry_authorized": False,
        "candidate_execution_authorized": False,
        "candidate_execution_performed": False,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
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
        "reviewed_retry2_evidence": reviewed,
    }


def authorize_candidate_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineResultReviewHold(NEXT_GATE)
