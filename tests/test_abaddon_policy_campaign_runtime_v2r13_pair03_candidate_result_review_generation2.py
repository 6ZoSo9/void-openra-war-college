from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_result_review_generation2
    as review,
)


def test_result_review_pins_exact_upstream_reviews():
    out = review.v2r13_pair03_candidate_result_review_contract()
    assert out["candidate_evidence_review_git_blob"] == (
        "0c25ccc2b9d678d764fb6ddbb9848d2f1ee274ea"
    )
    assert out["candidate_evidence_review_source_sha256"] == (
        "ddbafc3fe5bf915aea640708790850ec75d15a1e553c36e670b139b776225332"
    )
    assert out["candidate_evidence_review_test_git_blob"] == (
        "940872a77acc9f5e639bbacb93008992d9d840cc"
    )
    assert out["candidate_evidence_review_test_sha256"] == (
        "72366f8cf4dc16740d707f08d34e5f4aaea5986e47fac24b6f4c5e7a622b6688"
    )
    assert out["baseline_result_review_git_blob"] == (
        "877c9dd0969b1b2220f5d886da7521aa756a9742"
    )
    assert out["baseline_result_review_source_sha256"] == (
        "83cf29600bc11a15cfbbde0e56a7f09b2fb3aa60ec508c85c540634b766b217f"
    )


def test_pair03_candidate_and_baseline_are_complete_pairwise_measurements():
    out = review.v2r13_pair03_candidate_result_review_contract()
    assert out["candidate_result_reviewed"] is True
    assert out["pair_slot"] == 3
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


def test_pair03_comparison_is_non_decisive():
    out = review.v2r13_pair03_candidate_result_review_contract()
    assert out["baseline_game_outcome"] == "DRAW_OR_UNFINISHED"
    assert out["candidate_game_outcome"] == "DRAW_OR_UNFINISHED"
    assert out["baseline_game_outcome_decisive"] is False
    assert out["candidate_game_outcome_decisive"] is False
    assert out["decisive_candidate_advantage_observed"] is False
    assert out["pairwise_policy_disposition_made"] is False


def test_exact_observed_pairwise_deltas_are_recorded():
    out = review.v2r13_pair03_candidate_result_review_contract()
    assert out["candidate_minus_baseline"] == {
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


def test_exact_candidate_and_baseline_hashes_remain_bound():
    out = review.v2r13_pair03_candidate_result_review_contract()
    candidate = out["candidate_evidence_review"]
    baseline = out["baseline_review"]
    assert candidate["trajectory_sha256"] == (
        "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65"
    )
    assert candidate["summary_sha256"] == (
        "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0"
    )
    assert baseline["baseline_trajectory_sha256"] == (
        "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
    )
    assert baseline["baseline_summary_sha256"] == (
        "d37ab54fa8db2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
    )


def test_result_review_keeps_all_follow_on_authority_closed():
    out = review.v2r13_pair03_candidate_result_review_contract()
    assert out["candidate_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["pair09_execution_authorized"] is False
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


def test_result_review_stops_at_policy_disposition_gate():
    out = review.v2r13_pair03_candidate_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_v2r13_pair03_candidate_policy_disposition"
    )


def test_follow_on_action_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03CandidateResultReviewHold,
        match="V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_REQUIRED",
    ):
        review.authorize_follow_on_action()
