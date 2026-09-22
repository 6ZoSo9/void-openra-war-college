from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_result_review_generation2
    as review,
)


def test_baseline_result_review_pins_exact_evidence_review():
    out = review.v2r13_pair09_baseline_result_review_contract()
    assert out["evidence_review_git_blob"] == (
        "6ce171fad08ce663086f4fa2c698add058e1cb43"
    )
    assert out["evidence_review_source_sha256"] == (
        "edbd14375a4d5885c7dade9c30dd1857482bc6e054ad4e0824ae90fe5e5845d8"
    )
    assert out["evidence_review_test_git_blob"] == (
        "b6f4a89cbef244fae9d86e1d6c429d96b09135e9"
    )
    assert out["evidence_review_test_sha256"] == (
        "ccabf5faaf5990250ed8d57e7b9187b37e4c1fcbb1b9cf7a48d09351bb03703d"
    )


def test_pair09_baseline_measurement_is_complete_but_nondecisive():
    out = review.v2r13_pair09_baseline_result_review_contract()
    assert out["baseline_result_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["baseline_measurement_complete"] is True
    assert out["baseline_measurement_reproducibly_bound"] is True
    assert out["baseline_game_outcome"] == "DRAW_OR_UNFINISHED"
    assert out["baseline_game_outcome_decisive"] is False
    assert out["baseline_round_limit_reached"] is True
    assert out["baseline_rounds_completed"] == 36
    assert out["baseline_final_tick"] == 3551
    assert out["baseline_seed"] == 1496195137
    assert out["baseline_valid_for_pairwise_comparison"] is True


def test_pair09_baseline_hashes_are_exact():
    out = review.v2r13_pair09_baseline_result_review_contract()
    assert out["baseline_warm_start_sha256"] == (
        "d40816f63f86b5103b9d181ecc31e6b694005c1f3032a1b3fc614a209f2d7790"
    )
    assert out["baseline_trajectory_sha256"] == (
        "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
    )
    assert out["baseline_summary_sha256"] == (
        "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
    )
    assert out["baseline_result_file_sha256"] == (
        "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
    )


def test_pair09_baseline_facts_are_preserved_for_candidate_comparison():
    out = review.v2r13_pair09_baseline_result_review_contract()
    assert out["baseline_facts"] == {
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


def test_baseline_attempt_is_exhausted_and_candidate_remains_closed():
    out = review.v2r13_pair09_baseline_result_review_contract()
    assert out["baseline_attempt_consumed"] is True
    assert out["baseline_attempt_exhausted"] is True
    assert out["another_baseline_execution_authorized"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False


def test_result_review_does_not_expand_mutation_scope():
    out = review.v2r13_pair09_baseline_result_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_result_review_advances_only_to_candidate_authorization():
    out = review.v2r13_pair09_baseline_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_candidate_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09BaselineResultReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_candidate_execution()
