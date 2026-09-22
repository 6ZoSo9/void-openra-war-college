"""Review the completed V2R13 pair-03 candidate measurement.

This source compares the accepted candidate measurement with the already
reviewed pair-03 baseline using exact preserved identities and a small set of
directly observed summary facts. Both measurements reached the same 36-round
limit with DRAW_OR_UNFINISHED, so this review records a non-decisive comparison
and intentionally makes no promotion, training, pair-09, or held-out decision.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_result_review_generation2
    as baseline_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_evidence_source_binding_review_generation2
    as candidate_evidence_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-result-review-contract.v1"
)

CANDIDATE_EVIDENCE_REVIEW_GIT_BLOB = (
    "0c25ccc2b9d678d764fb6ddbb9848d2f1ee274ea"
)
CANDIDATE_EVIDENCE_REVIEW_SOURCE_SHA256 = (
    "ddbafc3fe5bf915aea640708790850ec75d15a1e553c36e670b139b776225332"
)
CANDIDATE_EVIDENCE_REVIEW_TEST_GIT_BLOB = (
    "940872a77acc9f5e639bbacb93008992d9d840cc"
)
CANDIDATE_EVIDENCE_REVIEW_TEST_SHA256 = (
    "72366f8cf4dc16740d707f08d34e5f4aaea5986e47fac24b6f4c5e7a622b6688"
)
BASELINE_RESULT_REVIEW_GIT_BLOB = (
    "877c9dd0969b1b2220f5d886da7521aa756a9742"
)
BASELINE_RESULT_REVIEW_SOURCE_SHA256 = (
    "83cf29600bc11a15cfbbde0e56a7f09b2fb3aa60ec508c85c540634b766b217f"
)

BASELINE_TRAJECTORY_SHA256 = (
    "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
)
BASELINE_SUMMARY_SHA256 = (
    "d37ab54fa8db2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
)
CANDIDATE_TRAJECTORY_SHA256 = (
    "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65"
)
CANDIDATE_SUMMARY_SHA256 = (
    "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0"
)

BASELINE_FACTS = {
    "outcome": "DRAW_OR_UNFINISHED",
    "rounds_completed": 36,
    "final_tick": 3551,
    "abaddon_explored_percent": 13.111773490905762,
    "abaddon_units_killed": 4,
    "abaddon_kills_cost": 400,
    "apollyon_cash": 2296,
    "apollyon_explored_percent": 13.458993911743164,
    "apollyon_army_value": 1100,
    "apollyon_assets_value": 5600,
    "apollyon_units_lost": 4,
    "apollyon_deaths_cost": 400,
}

CANDIDATE_FACTS = {
    "outcome": "DRAW_OR_UNFINISHED",
    "rounds_completed": 36,
    "final_tick": 3551,
    "abaddon_explored_percent": 13.971561431884766,
    "abaddon_units_killed": 3,
    "abaddon_kills_cost": 300,
    "apollyon_cash": 2445,
    "apollyon_explored_percent": 12.33465576171875,
    "apollyon_army_value": 1200,
    "apollyon_assets_value": 5700,
    "apollyon_units_lost": 3,
    "apollyon_deaths_cost": 300,
}

PAIRWISE_DELTAS = {
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

NEXT_GATE = "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_candidate_policy_disposition"


class V2R13Pair03CandidateResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidateResultReviewHold(message)


@lru_cache(maxsize=1)
def _candidate_review_cached() -> dict[str, Any]:
    reviewed = (
        candidate_evidence_review
        .v2r13_pair03_candidate_execution_evidence_review_contract()
    )
    _require(
        reviewed.get("candidate_execution_evidence_source_binding_present") is True,
        "candidate evidence review binding missing",
    )
    _require(
        reviewed.get("candidate_execution_evidence_reviewed") is True,
        "candidate evidence not reviewed",
    )
    _require(reviewed.get("pair_slot") == 3, "candidate pair-slot drift")
    _require(reviewed.get("arm") == "candidate", "candidate arm drift")
    _require(reviewed.get("held_out") is False, "candidate held-out drift")
    _require(
        reviewed.get("outcome") == "DRAW_OR_UNFINISHED",
        "candidate outcome drift",
    )
    _require(reviewed.get("rounds_completed") == 36, "candidate round-count drift")
    _require(
        reviewed.get("trajectory_sha256") == CANDIDATE_TRAJECTORY_SHA256,
        "candidate trajectory drift",
    )
    _require(
        reviewed.get("summary_sha256") == CANDIDATE_SUMMARY_SHA256,
        "candidate summary drift",
    )
    _require(
        reviewed.get("candidate_execution_replay_permitted") is False,
        "candidate replay unexpectedly permitted",
    )
    return deepcopy(reviewed)


@lru_cache(maxsize=1)
def _baseline_review_cached() -> dict[str, Any]:
    reviewed = baseline_review.v2r13_pair03_baseline_result_review_contract()
    _require(reviewed.get("baseline_result_reviewed") is True, "baseline result review missing")
    _require(
        reviewed.get("baseline_measurement_complete") is True,
        "baseline measurement incomplete",
    )
    _require(
        reviewed.get("baseline_valid_for_pairwise_comparison") is True,
        "baseline not valid for pairwise comparison",
    )
    _require(
        reviewed.get("baseline_game_outcome") == "DRAW_OR_UNFINISHED",
        "baseline outcome drift",
    )
    _require(
        reviewed.get("baseline_rounds_completed") == 36,
        "baseline round-count drift",
    )
    _require(
        reviewed.get("baseline_trajectory_sha256") == BASELINE_TRAJECTORY_SHA256,
        "baseline trajectory drift",
    )
    _require(
        reviewed.get("baseline_summary_sha256") == BASELINE_SUMMARY_SHA256,
        "baseline summary drift",
    )
    return deepcopy(reviewed)


def v2r13_pair03_candidate_result_review_contract() -> dict[str, Any]:
    candidate = _candidate_review_cached()
    baseline = _baseline_review_cached()

    return {
        "schema": CONTRACT_SCHEMA,
        "candidate_evidence_review_git_blob": CANDIDATE_EVIDENCE_REVIEW_GIT_BLOB,
        "candidate_evidence_review_source_sha256": (
            CANDIDATE_EVIDENCE_REVIEW_SOURCE_SHA256
        ),
        "candidate_evidence_review_test_git_blob": (
            CANDIDATE_EVIDENCE_REVIEW_TEST_GIT_BLOB
        ),
        "candidate_evidence_review_test_sha256": (
            CANDIDATE_EVIDENCE_REVIEW_TEST_SHA256
        ),
        "baseline_result_review_git_blob": BASELINE_RESULT_REVIEW_GIT_BLOB,
        "baseline_result_review_source_sha256": (
            BASELINE_RESULT_REVIEW_SOURCE_SHA256
        ),
        "candidate_result_reviewed": True,
        "pair_slot": 3,
        "candidate_arm": "candidate",
        "baseline_arm": "baseline",
        "candidate_measurement_complete": True,
        "candidate_measurement_reproducibly_bound": True,
        "candidate_valid_for_pairwise_comparison": True,
        "baseline_valid_for_pairwise_comparison": True,
        "same_pair_slot": True,
        "same_seed": True,
        "same_round_limit": True,
        "same_final_tick": True,
        "baseline_game_outcome": "DRAW_OR_UNFINISHED",
        "candidate_game_outcome": "DRAW_OR_UNFINISHED",
        "baseline_game_outcome_decisive": False,
        "candidate_game_outcome_decisive": False,
        "decisive_candidate_advantage_observed": False,
        "pairwise_policy_disposition_made": False,
        "candidate_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "pair09_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "baseline_facts": deepcopy(BASELINE_FACTS),
        "candidate_facts": deepcopy(CANDIDATE_FACTS),
        "candidate_minus_baseline": deepcopy(PAIRWISE_DELTAS),
        "baseline_review": deepcopy(baseline),
        "candidate_evidence_review": deepcopy(candidate),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_follow_on_action(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidateResultReviewHold(NEXT_GATE)
