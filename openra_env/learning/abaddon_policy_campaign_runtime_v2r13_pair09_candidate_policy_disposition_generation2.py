"""Source-only policy disposition for the completed V2R13 pair-09 candidate.

The pair-09 baseline and candidate are exact, matched measurements. Both reached
the same 36-round limit with DRAW_OR_UNFINISHED. Candidate-minus-baseline facts
are mixed: Abaddon explores slightly more and loses fewer units, but kills fewer
units and less value while Apollyon finishes with more cash, army value, and
assets.

Disposition: preserve the candidate as evidence, neither promote nor reject it,
and require a separately reviewed post-pair-09 bounded evaluation design.

This module does not authorize candidate replay, held-out execution, training,
weight updates, promotion, deployment, VOID-chain mutation, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_result_review_generation2
    as result_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-policy-disposition-contract.v1"
)

RESULT_REVIEW_GIT_BLOB = "372d935810b11e8a5046e21fe7049f3efbfa2f54"
RESULT_REVIEW_SOURCE_SHA256 = (
    "faf47727b5b314d9877fb83f6e5da11ce31ddaeeba34e8faaca5273931c3079d"
)

DISPOSITION = "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION"

EXPECTED_DELTAS = {
    "abaddon_explored_percent": 0.4629631042480469,
    "abaddon_units_killed": -2,
    "abaddon_kills_cost": -200,
    "apollyon_cash": 157,
    "apollyon_explored_percent": -1.1739425659179688,
    "apollyon_army_value": 200,
    "apollyon_assets_value": 700,
    "apollyon_units_lost": -2,
    "apollyon_deaths_cost": -200,
}

NEXT_GATE = (
    "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair09_candidate_policy_disposition_source_binding_review"
)


class V2R13Pair09CandidatePolicyDispositionHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidatePolicyDispositionHold(message)


@lru_cache(maxsize=1)
def _validate_result_review_cached() -> dict[str, Any]:
    reviewed = result_review.v2r13_pair09_candidate_result_review_contract()

    _require(reviewed.get("candidate_result_reviewed") is True, "candidate result review missing")
    _require(reviewed.get("pair_slot") == 9, "pair-slot drift")
    _require(reviewed.get("candidate_arm") == "candidate", "candidate arm drift")
    _require(reviewed.get("baseline_arm") == "baseline", "baseline arm drift")
    _require(
        reviewed.get("candidate_measurement_complete") is True,
        "candidate measurement incomplete",
    )
    _require(
        reviewed.get("candidate_measurement_reproducibly_bound") is True,
        "candidate binding incomplete",
    )
    _require(
        reviewed.get("candidate_valid_for_pairwise_comparison") is True,
        "candidate not pairwise-valid",
    )
    _require(
        reviewed.get("baseline_valid_for_pairwise_comparison") is True,
        "baseline not pairwise-valid",
    )
    _require(reviewed.get("same_pair_slot") is True, "pair mismatch")
    _require(reviewed.get("same_seed") is True, "seed mismatch")
    _require(reviewed.get("same_round_limit") is True, "round-limit mismatch")
    _require(reviewed.get("same_final_tick") is True, "final-tick mismatch")
    _require(
        reviewed.get("baseline_game_outcome") == "DRAW_OR_UNFINISHED",
        "baseline outcome drift",
    )
    _require(
        reviewed.get("candidate_game_outcome") == "DRAW_OR_UNFINISHED",
        "candidate outcome drift",
    )
    _require(
        reviewed.get("baseline_game_outcome_decisive") is False,
        "baseline unexpectedly decisive",
    )
    _require(
        reviewed.get("candidate_game_outcome_decisive") is False,
        "candidate unexpectedly decisive",
    )
    _require(
        reviewed.get("decisive_candidate_advantage_observed") is False,
        "decisive candidate advantage unexpectedly present",
    )
    _require(
        reviewed.get("mixed_metric_deltas_observed") is True,
        "mixed metric evidence missing",
    )
    _require(
        reviewed.get("pairwise_policy_disposition_made") is False,
        "policy disposition already made",
    )
    _require(
        reviewed.get("candidate_minus_baseline") == EXPECTED_DELTAS,
        "pairwise deltas drift",
    )

    for field in (
        "candidate_replay_permitted",
        "another_candidate_execution_authorized",
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
        reviewed.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_REQUIRED",
        "pre-disposition frontier drift",
    )
    return deepcopy(reviewed)


def v2r13_pair09_candidate_policy_disposition_contract() -> dict[str, Any]:
    reviewed = _validate_result_review_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "result_review_git_blob": RESULT_REVIEW_GIT_BLOB,
        "result_review_source_sha256": RESULT_REVIEW_SOURCE_SHA256,
        "pair_slot": 9,
        "baseline_arm": "baseline",
        "candidate_arm": "candidate",
        "policy_disposition_made": True,
        "policy_disposition": DISPOSITION,
        "pair09_measurement_conclusive": False,
        "candidate_preserved_as_evidence": True,
        "candidate_promoted": False,
        "candidate_rejected": False,
        "candidate_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "additional_bounded_evaluation_required": True,
        "post_pair09_evaluation_design_required": True,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
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
            "held_out_evidence_used": False,
        },
        "result_review": deepcopy(reviewed),
        "source_binding_reviewed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_held_out_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidatePolicyDispositionHold(
        "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def replay_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidatePolicyDispositionHold(
        "V2R13_PAIR09_CANDIDATE_REPLAY_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidatePolicyDispositionHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
