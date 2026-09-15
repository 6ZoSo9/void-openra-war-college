from __future__ import annotations

from collections import Counter

from openra_env.learning.abaddon_policy_campaign_plan import (
    PLAN_INTERNAL_SHA256,
    precommitted_campaign_plan,
)


def test_integrated_plan_is_18_pairs_and_still_not_execution_eligible():
    plan = precommitted_campaign_plan()
    assert plan["plan_sha256"] == PLAN_INTERNAL_SHA256 == "2a3f13699b29f1f8fcc4a5d4e31609ada0bc8524f42e0cf9e86642dc1d374e98"
    assert plan["summary"]["pair_slot_count"] == 18
    assert plan["summary"]["total_eventual_game_executions"] == 36
    assert Counter(row["opponent_snapshot_id"] for row in plan["pair_slots"]) == {
        "apollyon-v13-v14-promoted": 6,
        "apollyon-v13-v10-promoted": 6,
        "apollyon-v2r13-qualified-predecessor": 3,
        "apollyon-v3-v8-accepted-model-control": 3,
    }
    assert plan["pre_execution_gates"]["previous_champion_binding_complete"] is True
    assert plan["pre_execution_gates"]["opponent_runtime_realization_complete"] is True
    assert plan["pre_execution_gates"]["runtime_execution_authorized"] is False
    assert plan["execution_eligible"] is False
    assert plan["reasons"] == ["RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"]
