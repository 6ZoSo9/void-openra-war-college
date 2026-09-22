"""Review the completed V2R13 pair-09 baseline measurement.

The pair-09 baseline completed exactly one authorized attempt and reached the
36-round limit with DRAW_OR_UNFINISHED. This review records the reproducibly
bound baseline and a small set of directly observed summary facts for later
matched candidate comparison.

It does not authorize or execute the candidate arm, another baseline attempt,
held-out execution, training, weight changes, promotion, deployment, VOID
mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_execution_evidence_source_binding_review_generation2
    as evidence_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-result-review-contract.v1"
)

EVIDENCE_REVIEW_GIT_BLOB = "6ce171fad08ce663086f4fa2c698add058e1cb43"
EVIDENCE_REVIEW_SOURCE_SHA256 = (
    "edbd14375a4d5885c7dade9c30dd1857482bc6e054ad4e0824ae90fe5e5845d8"
)
EVIDENCE_REVIEW_TEST_GIT_BLOB = (
    "b6f4a89cbef244fae9d86e1d6c429d96b09135e9"
)
EVIDENCE_REVIEW_TEST_SHA256 = (
    "ccabf5faaf5990250ed8d57e7b9187b37e4c1fcbb1b9cf7a48d09351bb03703d"
)

BASELINE_FACTS = {
    "outcome": "DRAW_OR_UNFINISHED",
    "rounds_completed": 36,
    "final_tick": 3551,
    "seed": 1496195137,
    "abaddon_explored_percent": 11.97089958190918,
    "abaddon_units_killed": 4,
    "abaddon_kills_cost": 400,
    "apollyon_cash": 2178,
    "apollyon_explored_percent": 13.492064476013184,
    "apollyon_army_value": 1100,
    "apollyon_assets_value": 5750,
    "apollyon_units_lost": 4,
    "apollyon_deaths_cost": 400,
}

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_execution_authorization"


class V2R13Pair09BaselineResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineResultReviewHold(message)


@lru_cache(maxsize=1)
def _validate_evidence_review_cached() -> dict[str, Any]:
    reviewed = (
        evidence_review
        .v2r13_pair09_baseline_execution_evidence_review_contract()
    )
    _require(
        reviewed.get("pair09_baseline_execution_evidence_source_binding_present")
        is True,
        "pair09 baseline evidence review binding missing",
    )
    _require(
        reviewed.get("pair09_baseline_execution_evidence_reviewed") is True,
        "pair09 baseline evidence not reviewed",
    )
    _require(reviewed.get("pair_slot") == 9, "pair09 baseline result slot drift")
    _require(reviewed.get("arm") == "baseline", "pair09 baseline result arm drift")
    _require(reviewed.get("held_out") is False, "pair09 baseline held-out drift")
    _require(reviewed.get("attempt_consumed") is True, "pair09 attempt not consumed")
    _require(reviewed.get("maximum_attempts") == 1, "pair09 attempt count drift")
    _require(
        reviewed.get("outcome") == "DRAW_OR_UNFINISHED",
        "pair09 baseline outcome drift",
    )
    _require(reviewed.get("rounds_completed") == 36, "pair09 baseline round-count drift")
    _require(reviewed.get("final_tick") == 3551, "pair09 baseline final-tick drift")
    _require(
        reviewed.get("runtime_execution_performed") is True,
        "pair09 baseline runtime execution missing",
    )
    _require(
        reviewed.get("runtime_cleanup_completed") is True,
        "pair09 baseline cleanup missing",
    )
    _require(
        reviewed.get("pair03_baseline_preserved") is True
        and reviewed.get("pair03_candidate_preserved") is True,
        "pair03 evidence preservation drift",
    )
    _require(
        reviewed.get("another_baseline_execution_authorized") is False,
        "another pair09 baseline unexpectedly authorized",
    )
    _require(
        reviewed.get("candidate_execution_authorized") is False,
        "pair09 candidate prematurely authorized",
    )
    _require(
        reviewed.get("candidate_execution_performed") is False,
        "pair09 candidate prematurely executed",
    )
    _require(
        reviewed.get("held_out_execution_authorized") is False,
        "held-out prematurely authorized",
    )
    _require(
        reviewed.get("held_out_execution_performed") is False,
        "held-out prematurely executed",
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
        _require(reviewed.get(field) is False, f"pair09 baseline scope drift: {field}")

    return deepcopy(reviewed)


def v2r13_pair09_baseline_result_review_contract() -> dict[str, Any]:
    reviewed = _validate_evidence_review_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "evidence_review_git_blob": EVIDENCE_REVIEW_GIT_BLOB,
        "evidence_review_source_sha256": EVIDENCE_REVIEW_SOURCE_SHA256,
        "evidence_review_test_git_blob": EVIDENCE_REVIEW_TEST_GIT_BLOB,
        "evidence_review_test_sha256": EVIDENCE_REVIEW_TEST_SHA256,
        "baseline_result_reviewed": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "baseline_measurement_complete": True,
        "baseline_measurement_reproducibly_bound": True,
        "baseline_game_outcome": "DRAW_OR_UNFINISHED",
        "baseline_game_outcome_decisive": False,
        "baseline_round_limit_reached": True,
        "baseline_rounds_completed": 36,
        "baseline_final_tick": 3551,
        "baseline_seed": 1496195137,
        "baseline_warm_start_sha256": reviewed["warm_start_sha256"],
        "baseline_trajectory_sha256": reviewed["trajectory_sha256"],
        "baseline_summary_sha256": reviewed["summary_sha256"],
        "baseline_result_file_sha256": reviewed["result_file_sha256"],
        "baseline_valid_for_pairwise_comparison": True,
        "baseline_facts": deepcopy(BASELINE_FACTS),
        "baseline_attempt_consumed": True,
        "baseline_attempt_exhausted": True,
        "another_baseline_execution_authorized": False,
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
        "reviewed_execution_evidence": deepcopy(reviewed),
    }


def authorize_candidate_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineResultReviewHold(NEXT_GATE)
