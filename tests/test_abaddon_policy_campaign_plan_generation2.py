from __future__ import annotations

from collections import Counter

from openra_env.learning.abaddon_policy_campaign_plan import (
    PLAN_INTERNAL_SHA256 as GENERATION1_PLAN_SHA256,
    precommitted_campaign_plan as generation1_plan,
)
from openra_env.learning.abaddon_policy_campaign_plan_generation2 import (
    CANDIDATE_GENOME_SHA256,
    EXPECTED_MUTATIONS,
    EXPECTED_SEEDS,
    PLAN_INTERNAL_SHA256,
    precommitted_campaign_plan,
)


def test_generation2_plan_is_frozen_parallel_and_not_execution_eligible():
    gen1 = generation1_plan()
    plan = precommitted_campaign_plan()

    assert GENERATION1_PLAN_SHA256 == "2a3f13699b29f1f8fcc4a5d4e31609ada0bc8524f42e0cf9e86642dc1d374e98"
    assert gen1["plan_sha256"] == GENERATION1_PLAN_SHA256

    assert plan["plan_sha256"] == PLAN_INTERNAL_SHA256 == "64e5003fa0d339ea1bea14eb0e4026e0dfe3455e86f38ef0fb9c0a26fbc4c594"
    assert plan["candidate"]["generation"] == 2
    assert plan["candidate"]["candidate_index"] == 252
    assert plan["candidate"]["candidate_genome_sha256"] == CANDIDATE_GENOME_SHA256
    assert CANDIDATE_GENOME_SHA256 == "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
    assert EXPECTED_MUTATIONS == (
        {"doctrine": "FEINTER", "key": "group", "old": 4, "new": 3},
        {"doctrine": "FEINTER", "key": "scout_history_min", "old": 16, "new": 20},
    )
    assert EXPECTED_SEEDS == (
        1990061685,
        208354846,
        1496195137,
        331379205,
        905645055,
        411746275,
    )
    assert set(EXPECTED_SEEDS).isdisjoint(set(gen1["seed_derivation"]["seeds"]))

    assert plan["summary"] == gen1["summary"]
    assert plan["summary"]["pair_slot_count"] == 18
    assert plan["summary"]["held_out_pair_slot_count"] == 6
    assert plan["summary"]["total_eventual_game_executions"] == 36
    assert Counter(row["opponent_snapshot_id"] for row in plan["pair_slots"]) == {
        "apollyon-v13-v14-promoted": 6,
        "apollyon-v13-v10-promoted": 6,
        "apollyon-v2r13-qualified-predecessor": 3,
        "apollyon-v3-v8-accepted-model-control": 3,
    }
    assert [row["pair_slot"] for row in plan["pair_slots"] if row["held_out"]] == [13, 14, 15, 16, 17, 18]

    for row in plan["pair_slots"]:
        assert row["baseline_arm"]["abaddon_genome_sha256"] == "3c4346e0c92ea7225425d9ff4fd7ae12daa44162b06d471530179325b7d38a26"
        assert row["candidate_arm"]["abaddon_genome_sha256"] == CANDIDATE_GENOME_SHA256
        assert row["execution_state"] == "NOT_EXECUTED"
        assert all(row["pair_binding"].values())

    assert plan["pre_execution_gates"]["runtime_execution_authorized"] is False
    assert plan["execution_eligible"] is False
    assert plan["reasons"] == ["RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"]
    assert plan["authority"] == gen1["authority"]
