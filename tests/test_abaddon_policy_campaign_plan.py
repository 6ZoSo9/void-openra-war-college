from __future__ import annotations

from collections import Counter

from openra_env.learning.abaddon_policy_campaign_plan import (
    CANDIDATE_FIXTURE_SHA256,
    CANDIDATE_GENOME_SHA256,
    EXPECTED_MUTATIONS,
    EXPECTED_SEEDS,
    PARENT_GENOME_SHA256,
    PLAN_INTERNAL_SHA256,
    derive_seed,
    precommitted_campaign_plan,
    validate_candidate_fixture,
)


def test_candidate_is_frozen_before_campaign_evidence():
    candidate = validate_candidate_fixture()
    assert candidate["generation"] == 1
    assert candidate["candidate_index"] == 0
    assert candidate["source"] == "bounded_deterministic_mutation"
    assert candidate["genome_sha256"] == CANDIDATE_GENOME_SHA256
    assert candidate["parent_genome_sha256"] == PARENT_GENOME_SHA256
    assert tuple(candidate["mutations"]) == EXPECTED_MUTATIONS
    assert candidate["profiles"]["FEINTER"]["scout_current_min"] == 12
    assert candidate["profiles"]["FEINTER"]["weap_power_min"] == 60


def test_seed_derivation_is_candidate_specific_and_precommitted():
    assert tuple(derive_seed(i) for i in range(6)) == EXPECTED_SEEDS
    assert len(set(EXPECTED_SEEDS)) == 6


def test_plan_is_12_matched_pairs_not_12_total_games():
    plan = precommitted_campaign_plan()
    summary = plan["summary"]
    assert plan["plan_sha256"] == PLAN_INTERNAL_SHA256
    assert summary["pair_slot_count"] == 12
    assert summary["baseline_execution_count"] == 12
    assert summary["candidate_execution_count"] == 12
    assert summary["total_eventual_game_executions"] == 24
    assert summary["unique_seed_count"] == 6


def test_every_pair_precommits_distinct_baseline_and_candidate_arms():
    plan = precommitted_campaign_plan()
    for index, slot in enumerate(plan["pair_slots"], 1):
        assert slot["pair_slot"] == index
        assert slot["execution_state"] == "NOT_EXECUTED"
        assert slot["baseline_arm"]["abaddon_genome_sha256"] == PARENT_GENOME_SHA256
        assert slot["baseline_arm"]["candidate_fixture_sha256"] is None
        assert slot["candidate_arm"]["abaddon_genome_sha256"] == CANDIDATE_GENOME_SHA256
        assert slot["candidate_arm"]["candidate_fixture_sha256"] == CANDIDATE_FIXTURE_SHA256
        assert all(slot["pair_binding"].values())


def test_opponent_distribution_and_holdout_are_fixed():
    plan = precommitted_campaign_plan()
    ids = Counter(slot["opponent_snapshot_id"] for slot in plan["pair_slots"])
    assert ids == {
        "apollyon-v13-v10-promoted": 6,
        "apollyon-v2r13-qualified-predecessor": 3,
        "apollyon-v3-v8-accepted-model-control": 3,
    }
    held = [slot for slot in plan["pair_slots"] if slot["held_out"]]
    assert len(held) == 4
    assert {slot["seed"] for slot in held} == {EXPECTED_SEEDS[4], EXPECTED_SEEDS[5]}


def test_plan_remains_nonexecuting_and_fail_closed():
    plan = precommitted_campaign_plan()
    assert plan["execution_eligible"] is False
    assert plan["pre_execution_gates"]["campaign_attempt_ledger_complete"] is True
    assert plan["pre_execution_gates"]["pair_arms_precommitted"] is True
    assert plan["pre_execution_gates"]["previous_champion_binding_complete"] is False
    assert plan["pre_execution_gates"]["opponent_runtime_realization_complete"] is False
    assert plan["pre_execution_gates"]["runtime_execution_authorized"] is False
    assert plan["authority"] == {
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
        "deployment": False,
        "game_started": False,
        "model_execution": False,
        "training": False,
        "weights_updated": False,
    }
