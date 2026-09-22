"""Source-only policy disposition for the completed V2R13 pair-03 candidate.

The pair-03 baseline and candidate are exact, reproducibly bound measurements.
Both reached the same 36-round limit with DRAW_OR_UNFINISHED and the observed
summary deltas are mixed rather than a decisive candidate advantage.

Disposition: preserve the candidate as evidence, neither promote nor reject it,
and require a separately reviewed bounded follow-up evaluation design.

This module does not authorize pair-09 execution, held-out execution, replay,
training, weight updates, promotion, deployment, VOID mutation, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_result_review_generation2
    as result_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-policy-disposition-contract.v1"
)

RESULT_REVIEW_GIT_BLOB = "1078ff9771b6ba8ba3957b8005e5689d65d41709"
RESULT_REVIEW_SOURCE_SHA256 = (
    "c3b3f9141c5e5ecfeb21b201b978c7739b2ca656b4ae4ea5e35749208ceed6f2"
)

DISPOSITION = "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION"

EXPECTED_DELTAS = {
    "abaddon_explored_percent": 0.8597879409790039,
    "abaddon_units_killed": -1,
    "abaddon_kills_cost": -100,
    "apollyon_cash": 149,
    "apollyon_explored_percent": -1.124338150024414,
    "apollyon_army_value": 100,
    "apollyon_assets_value": 100,
    "apollyon_units_lost": -1,
    "apollyon_deaths_cost": -100,
}

NEXT_GATE = "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair03_candidate_policy_disposition_source_binding_review"
)


class V2R13Pair03CandidatePolicyDispositionHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidatePolicyDispositionHold(message)


@lru_cache(maxsize=1)
def _validate_result_review_cached() -> dict[str, Any]:
    reviewed = result_review.v2r13_pair03_candidate_result_review_contract()

    _require(reviewed.get("candidate_result_reviewed") is True, "candidate result review missing")
    _require(reviewed.get("pair_slot") == 3, "pair-slot drift")
    _require(reviewed.get("candidate_arm") == "candidate", "candidate arm drift")
    _require(reviewed.get("baseline_arm") == "baseline", "baseline arm drift")
    _require(reviewed.get("candidate_measurement_complete") is True, "candidate measurement incomplete")
    _require(reviewed.get("candidate_measurement_reproducibly_bound") is True, "candidate binding incomplete")
    _require(reviewed.get("candidate_valid_for_pairwise_comparison") is True, "candidate not pairwise-valid")
    _require(reviewed.get("baseline_valid_for_pairwise_comparison") is True, "baseline not pairwise-valid")
    _require(reviewed.get("same_pair_slot") is True, "pair mismatch")
    _require(reviewed.get("same_seed") is True, "seed mismatch")
    _require(reviewed.get("same_round_limit") is True, "round-limit mismatch")
    _require(reviewed.get("same_final_tick") is True, "final-tick mismatch")
    _require(reviewed.get("baseline_game_outcome") == "DRAW_OR_UNFINISHED", "baseline outcome drift")
    _require(reviewed.get("candidate_game_outcome") == "DRAW_OR_UNFINISHED", "candidate outcome drift")
    _require(reviewed.get("baseline_game_outcome_decisive") is False, "baseline unexpectedly decisive")
    _require(reviewed.get("candidate_game_outcome_decisive") is False, "candidate unexpectedly decisive")
    _require(reviewed.get("decisive_candidate_advantage_observed") is False, "decisive candidate advantage unexpectedly present")
    _require(reviewed.get("pairwise_policy_disposition_made") is False, "policy disposition already made")
    _require(reviewed.get("candidate_minus_baseline") == EXPECTED_DELTAS, "pairwise deltas drift")

    for field in (
        "candidate_replay_permitted",
        "another_candidate_execution_authorized",
        "pair09_execution_authorized",
        "held_out_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(reviewed.get(field) is False, f"pre-disposition authority drift: {field}")

    _require(
        reviewed.get("next_gate") == "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_REQUIRED",
        "pre-disposition frontier drift",
    )
    return deepcopy(reviewed)


def v2r13_pair03_candidate_policy_disposition_contract() -> dict[str, Any]:
    reviewed = _validate_result_review_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "result_review_git_blob": RESULT_REVIEW_GIT_BLOB,
        "result_review_source_sha256": RESULT_REVIEW_SOURCE_SHA256,
        "pair_slot": 3,
        "baseline_arm": "baseline",
        "candidate_arm": "candidate",
        "policy_disposition_made": True,
        "policy_disposition": DISPOSITION,
        "pair03_measurement_conclusive": False,
        "candidate_preserved_as_evidence": True,
        "candidate_promoted": False,
        "candidate_rejected": False,
        "candidate_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "additional_bounded_evaluation_required": True,
        "pair09_evaluation_design_required": True,
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
        "observed_pairwise_deltas": deepcopy(EXPECTED_DELTAS),
        "disposition_basis": {
            "baseline_outcome": "DRAW_OR_UNFINISHED",
            "candidate_outcome": "DRAW_OR_UNFINISHED",
            "rounds_completed": 36,
            "same_seed": True,
            "same_final_tick": True,
            "decisive_candidate_advantage_observed": False,
            "mixed_metric_deltas_observed": True,
        },
        "result_review": deepcopy(reviewed),
        "source_binding_reviewed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_pair09_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidatePolicyDispositionHold(
        "V2R13_PAIR09_EXECUTION_NOT_AUTHORIZED"
    )


def authorize_held_out_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidatePolicyDispositionHold(
        "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidatePolicyDispositionHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
