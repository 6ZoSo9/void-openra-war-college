"""Review the completed V2R13 pair-09 candidate measurement.

This source compares the exact accepted candidate measurement with the reviewed
pair-09 baseline. Both use pair slot 9, seed 1496195137, a 36-round limit, and
the same final tick. Both reached DRAW_OR_UNFINISHED.

The observed deltas are mixed: the candidate preserves more Abaddon units and
explores slightly more, but produces materially fewer kills while Apollyon
finishes with more cash, army value, and assets. This review records no decisive
candidate advantage and makes no promotion or rejection decision.

No replay, held-out execution, training, promotion, deployment, VOID-chain,
wallet, or funds authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_result_review_generation2
    as baseline_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_execution_evidence_source_binding_review_generation2
    as candidate_evidence_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-result-review-contract.v1"
)

CANDIDATE_EVIDENCE_REVIEW_GIT_BLOB = (
    "86c26d97b3616d271137c7efa2975d0ffa90d241"
)
CANDIDATE_EVIDENCE_REVIEW_SOURCE_SHA256 = (
    "a29db7feef79398dae63f138243c42c91871f7df5cfa590fdd22a1f32119851a"
)
CANDIDATE_EVIDENCE_REVIEW_TEST_GIT_BLOB = (
    "f4ddbc58c494c27a88d7633a109ab6d5aa9eb336"
)
CANDIDATE_EVIDENCE_REVIEW_TEST_SHA256 = (
    "e0d157f5271943aec74729e84c64fc590f6248866f9253815caef6159d9f4250"
)
BASELINE_RESULT_REVIEW_GIT_BLOB = (
    "e0f663b144aa2036d7dba2a8d001f8f061f2f892"
)
BASELINE_RESULT_REVIEW_SOURCE_SHA256 = (
    "acda9a94d229e73381aa45e6898f55b7eb066b67bb1bc29685276518026b9431"
)

BASELINE_TRAJECTORY_SHA256 = (
    "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
)
BASELINE_SUMMARY_SHA256 = (
    "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
)
BASELINE_RESULT_FILE_SHA256 = (
    "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
)
CANDIDATE_TRAJECTORY_SHA256 = (
    "d8de375133687e1296ff0f740bd9901eee24c65332ae8600ab03f724edcd0eae"
)
CANDIDATE_SUMMARY_SHA256 = (
    "15f4e21c8b2d9988c26f90a9fd3021ff017faef2ac1f6b289d0582cd6748f7e3"
)
CANDIDATE_RESULT_FILE_SHA256 = (
    "68d86cea4a9806fca60a0bff765dce1227962acb923d6e4da3b5f7b1ab5ccb74"
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

CANDIDATE_FACTS = {
    "outcome": "DRAW_OR_UNFINISHED",
    "rounds_completed": 36,
    "final_tick": 3551,
    "seed": 1496195137,
    "abaddon_explored_percent": 12.433862686157227,
    "abaddon_units_killed": 2,
    "abaddon_kills_cost": 200,
    "apollyon_cash": 2335,
    "apollyon_explored_percent": 12.318121910095215,
    "apollyon_army_value": 1300,
    "apollyon_assets_value": 6450,
    "apollyon_units_lost": 2,
    "apollyon_deaths_cost": 200,
}

PAIRWISE_DELTAS = {
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

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_policy_disposition"


class V2R13Pair09CandidateResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateResultReviewHold(message)


@lru_cache(maxsize=1)
def _candidate_review_cached() -> dict[str, Any]:
    reviewed = (
        candidate_evidence_review
        .v2r13_pair09_candidate_execution_evidence_review_contract()
    )
    _require(
        reviewed.get("candidate_execution_evidence_source_binding_present") is True,
        "candidate evidence review binding missing",
    )
    _require(
        reviewed.get("candidate_execution_evidence_reviewed") is True,
        "candidate evidence not reviewed",
    )
    _require(reviewed.get("pair_slot") == 9, "candidate pair-slot drift")
    _require(reviewed.get("arm") == "candidate", "candidate arm drift")
    _require(reviewed.get("held_out") is False, "candidate held-out drift")
    _require(reviewed.get("seed") == 1496195137, "candidate seed drift")
    _require(
        reviewed.get("outcome") == "DRAW_OR_UNFINISHED",
        "candidate outcome drift",
    )
    _require(reviewed.get("rounds_completed") == 36, "candidate round-count drift")
    _require(reviewed.get("final_tick") == 3551, "candidate final-tick drift")
    _require(
        reviewed.get("trajectory_sha256") == CANDIDATE_TRAJECTORY_SHA256,
        "candidate trajectory drift",
    )
    _require(
        reviewed.get("summary_sha256") == CANDIDATE_SUMMARY_SHA256,
        "candidate summary drift",
    )
    _require(
        reviewed.get("result_file_sha256") == CANDIDATE_RESULT_FILE_SHA256,
        "candidate result-file drift",
    )
    _require(
        reviewed.get("candidate_execution_replay_permitted") is False,
        "candidate replay unexpectedly permitted",
    )
    return deepcopy(reviewed)


@lru_cache(maxsize=1)
def _baseline_review_cached() -> dict[str, Any]:
    reviewed = baseline_review.v2r13_pair09_baseline_result_review_contract()
    _require(reviewed.get("baseline_result_reviewed") is True, "baseline result review missing")
    _require(reviewed.get("pair_slot") == 9, "baseline pair-slot drift")
    _require(reviewed.get("arm") == "baseline", "baseline arm drift")
    _require(reviewed.get("held_out") is False, "baseline held-out drift")
    _require(
        reviewed.get("baseline_measurement_complete") is True,
        "baseline measurement incomplete",
    )
    _require(
        reviewed.get("baseline_valid_for_pairwise_comparison") is True,
        "baseline not valid for pairwise comparison",
    )
    _require(reviewed.get("baseline_seed") == 1496195137, "baseline seed drift")
    _require(
        reviewed.get("baseline_game_outcome") == "DRAW_OR_UNFINISHED",
        "baseline outcome drift",
    )
    _require(
        reviewed.get("baseline_rounds_completed") == 36,
        "baseline round-count drift",
    )
    _require(reviewed.get("baseline_final_tick") == 3551, "baseline final-tick drift")
    _require(
        reviewed.get("baseline_trajectory_sha256") == BASELINE_TRAJECTORY_SHA256,
        "baseline trajectory drift",
    )
    _require(
        reviewed.get("baseline_summary_sha256") == BASELINE_SUMMARY_SHA256,
        "baseline summary drift",
    )
    _require(
        reviewed.get("baseline_result_file_sha256") == BASELINE_RESULT_FILE_SHA256,
        "baseline result-file drift",
    )
    _require(
        reviewed.get("baseline_facts") == BASELINE_FACTS,
        "baseline comparison facts drift",
    )
    return deepcopy(reviewed)


def v2r13_pair09_candidate_result_review_contract() -> dict[str, Any]:
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
        "pair_slot": 9,
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
        "mixed_metric_deltas_observed": True,
        "pairwise_policy_disposition_made": False,
        "candidate_replay_permitted": False,
        "another_candidate_execution_authorized": False,
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
    raise V2R13Pair09CandidateResultReviewHold(NEXT_GATE)
