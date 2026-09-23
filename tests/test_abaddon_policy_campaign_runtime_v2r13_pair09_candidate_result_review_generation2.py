from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_result_review_generation2
    as review,
)


def test_result_review_pins_exact_candidate_evidence_review_and_baseline():
    out = review.v2r13_pair09_candidate_result_review_contract()
    assert out["candidate_evidence_review_git_blob"] == (
        "86c26d97b3616d271137c7efa2975d0ffa90d241"
    )
    assert out["candidate_evidence_review_source_sha256"] == (
        "a29db7feef79398dae63f138243c42c91871f7df5cfa590fdd22a1f32119851a"
    )
    assert out["candidate_evidence_review_test_git_blob"] == (
        "f4ddbc58c494c27a88d7633a109ab6d5aa9eb336"
    )
    assert out["candidate_evidence_review_test_sha256"] == (
        "e0d157f5271943aec74729e84c64fc590f6248866f9253815caef6159d9f4250"
    )
    assert out["baseline_result_review_git_blob"] == (
        "e0f663b144aa2036d7dba2a8d001f8f061f2f892"
    )


def test_pair09_measurements_are_matched_and_nondeci­sive():
    out = review.v2r13_pair09_candidate_result_review_contract()
    assert out["candidate_result_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["candidate_arm"] == "candidate"
    assert out["baseline_arm"] == "baseline"
    assert out["candidate_measurement_complete"] is True
    assert out["candidate_measurement_reproducibly_bound"] is True
    assert out["candidate_valid_for_pairwise_comparison"] is True
    assert out["baseline_valid_for_pairwise_comparison"] is True
    assert out["same_pair_slot"] is True
    assert out["same_seed"] is True
    assert out["same_round_limit"] is True
    assert out["same_final_tick"] is True
    assert out["baseline_game_outcome"] == "DRAW_OR_UNFINISHED"
    assert out["candidate_game_outcome"] == "DRAW_OR_UNFINISHED"
    assert out["baseline_game_outcome_decisive"] is False
    assert out["candidate_game_outcome_decisive"] is False
    assert out["decisive_candidate_advantage_observed"] is False
    assert out["mixed_metric_deltas_observed"] is True


def test_pair09_candidate_minus_baseline_deltas_are_exact():
    out = review.v2r13_pair09_candidate_result_review_contract()
    assert out["candidate_minus_baseline"] == {
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


def test_candidate_facts_capture_exact_terminal_summary():
    out = review.v2r13_pair09_candidate_result_review_contract()
    facts = out["candidate_facts"]
    assert facts["seed"] == 1496195137
    assert facts["abaddon_explored_percent"] == 12.433862686157227
    assert facts["abaddon_units_killed"] == 2
    assert facts["abaddon_kills_cost"] == 200
    assert facts["apollyon_cash"] == 2335
    assert facts["apollyon_explored_percent"] == 12.318121910095215
    assert facts["apollyon_army_value"] == 1300
    assert facts["apollyon_assets_value"] == 6450
    assert facts["apollyon_units_lost"] == 2
    assert facts["apollyon_deaths_cost"] == 200


def test_result_review_keeps_policy_disposition_and_execution_closed():
    out = review.v2r13_pair09_candidate_result_review_contract()
    assert out["pairwise_policy_disposition_made"] is False
    assert out["candidate_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_result_review_advances_only_to_policy_disposition():
    out = review.v2r13_pair09_candidate_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_REQUIRED"
    )


def test_followon_action_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateResultReviewHold,
        match="V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_REQUIRED",
    ):
        review.authorize_follow_on_action()
