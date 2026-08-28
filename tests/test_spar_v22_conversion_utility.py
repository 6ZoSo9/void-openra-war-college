from __future__ import annotations

import pytest

from openra_env.analysis._spar_contract import ContractError
from openra_env.analysis.spar_v22_conversion_utility import derive_conversion_productivity


def military(*, kills=0, deaths=0, units_killed=0, units_lost=0, buildings_killed=0, buildings_lost=0):
    return {
        "units_killed": units_killed,
        "units_lost": units_lost,
        "buildings_killed": buildings_killed,
        "buildings_lost": buildings_lost,
        "kills_cost": kills,
        "deaths_cost": deaths,
    }


def state(*, visible=0, stats=None):
    return {
        "enemy_summary": [{"actor_id": 100 + i} for i in range(visible)],
        "enemy_buildings_summary": [],
        "military": military() if stats is None else stats,
    }


def pair(*, mode, tool="attack_move", before=None, after=None):
    before = state() if before is None else before
    after = state() if after is None else after
    return (
        {
            "conditional_engagement_v2_2": {
                "prepared": {"decision": {"mode": mode}},
            },
            "apollyon": {"tool": tool},
            "apollyon_state": before,
        },
        {"apollyon_after": after},
    )


def test_no_force_conversion_is_not_applicable_and_does_not_fail_gate():
    out = derive_conversion_productivity([
        pair(mode="BALANCED_SEARCH"),
        pair(mode="MEASURED_CONTACT", after=state(visible=1)),
    ])
    assert out["conversion_productivity_applicable"] is False
    assert out["post_conversion_productivity_pass"] is True
    assert out["first_conversion_round"] is None
    assert out["post_conversion_round_count"] == 0


def test_early_contact_and_damage_do_not_rescue_unproductive_conversion():
    early_before = state(stats=military())
    early_after = state(visible=1, stats=military(kills=100, units_killed=1))
    out = derive_conversion_productivity([
        pair(mode="MEASURED_CONTACT", tool="attack_target", before=early_before, after=early_after),
        pair(
            mode="FORCE_CONVERSION",
            tool="move_units",
            before=state(stats=military(kills=100, units_killed=1)),
            after=state(stats=military(kills=100, units_killed=1)),
        ),
        pair(
            mode="BALANCED_SEARCH",
            before=state(stats=military(kills=100, units_killed=1)),
            after=state(stats=military(kills=100, units_killed=1)),
        ),
    ])
    assert out["first_conversion_round"] == 2
    assert out["post_conversion_contact_rounds"] == []
    assert out["post_conversion_damage_rounds"] == []
    assert out["post_conversion_productivity_pass"] is False


def test_contact_and_damage_after_first_conversion_pass_productivity_gate():
    baseline = military()
    damaged = military(kills=100, units_killed=1)
    out = derive_conversion_productivity([
        pair(mode="FORCE_CONVERSION", tool="move_units"),
        pair(mode="BALANCED_SEARCH", after=state(visible=2)),
        pair(
            mode="MEASURED_CONTACT",
            tool="attack_target",
            before=state(visible=2, stats=baseline),
            after=state(visible=1, stats=damaged),
        ),
    ])
    assert out["conversion_productivity_applicable"] is True
    assert out["post_conversion_contact_rounds"] == [2, 3]
    assert out["post_conversion_damage_rounds"] == [3]
    assert out["first_contact_round_after_conversion"] == 2
    assert out["first_damage_round_after_conversion"] == 3
    assert out["post_conversion_productivity_pass"] is True


def test_immediate_conversion_contact_and_damage_are_recorded():
    out = derive_conversion_productivity([
        pair(
            mode="FORCE_CONVERSION",
            tool="move_units",
            before=state(stats=military()),
            after=state(visible=1, stats=military(kills=100, units_killed=1)),
        )
    ])
    assert out["conversion_rounds_with_immediate_contact"] == [1]
    assert out["conversion_rounds_with_immediate_damage"] == [1]
    assert out["post_conversion_productivity_pass"] is True


def test_post_conversion_tool_mix_is_measured_separately_from_conversion_rounds():
    out = derive_conversion_productivity([
        pair(mode="BALANCED_SEARCH", tool="attack_move"),
        pair(mode="FORCE_CONVERSION", tool="move_units"),
        pair(mode="BALANCED_SEARCH", tool="attack_move"),
        pair(mode="BALANCED_SEARCH", tool="attack_move"),
        pair(mode="FORCE_CONVERSION", tool="move_units"),
    ])
    assert out["conversion_selected_tools"] == {"move_units": 2}
    assert out["post_conversion_selected_tools"] == {"attack_move": 2, "move_units": 2}
    assert out["post_conversion_attack_move_fraction"] == 0.5


def test_military_counter_regression_fails_closed():
    with pytest.raises(ContractError, match="military counters regressed"):
        derive_conversion_productivity([
            pair(
                mode="FORCE_CONVERSION",
                before=state(stats=military(kills=100, units_killed=1)),
                after=state(stats=military()),
            )
        ])
