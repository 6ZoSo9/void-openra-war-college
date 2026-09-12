from __future__ import annotations

from tests.test_mcp_tools import _make_env_with_tools, _make_spatial


def _unit(actor_id: int, *, can_attack: bool, is_idle: bool, unit_type: str = "e1") -> dict:
    return {
        "actor_id": actor_id,
        "type": unit_type,
        "pos_x": 1024,
        "pos_y": 1024,
        "cell_x": 1,
        "cell_y": 1,
        "hp_percent": 1.0,
        "is_idle": is_idle,
        "current_activity": "",
        "owner": "Multi0",
        "can_attack": can_attack,
        "facing": 0,
        "experience_level": 0,
        "stance": 3,
        "speed": 56,
        "attack_range": 5120 if can_attack else 0,
        "passenger_count": -1,
        "is_building": False,
    }


def _obs(units: list[dict]) -> dict:
    return {
        "tick": 1000,
        "done": False,
        "result": "",
        "economy": {
            "cash": 2000,
            "ore": 0,
            "power_provided": 100,
            "power_drained": 20,
            "resource_capacity": 2000,
            "harvester_count": 0,
        },
        "military": {
            "units_killed": 0,
            "units_lost": 0,
            "buildings_killed": 0,
            "buildings_lost": 0,
            "army_value": 0,
            "active_unit_count": len(units),
            "kills_cost": 0,
            "deaths_cost": 0,
            "assets_value": 0,
            "experience": 0,
            "order_count": 0,
        },
        "units": units,
        "buildings": [],
        "production": [],
        "visible_enemies": [],
        "visible_enemy_buildings": [],
        "map_info": {"width": 4, "height": 4, "map_name": "Test"},
        "spatial_map": _make_spatial(4, 4),
        "spatial_channels": 9,
        "available_production": [],
    }


def _scouting_alerts(units: list[dict]) -> list[str]:
    env, mcp = _make_env_with_tools(_obs(units))
    env._app_config.alerts.no_scouting = True
    env._enemy_ever_seen = False
    tool = mcp._tool_manager._tools["get_game_state"]
    result = tool.fn()
    return [a for a in result["alerts"] if "NO SCOUTING" in a]


def test_no_scouting_suppressed_with_no_units():
    assert _scouting_alerts([]) == []


def test_no_scouting_suppressed_when_combat_unit_is_busy():
    assert _scouting_alerts([_unit(1, can_attack=True, is_idle=False)]) == []


def test_no_scouting_suppressed_for_idle_noncombat_unit():
    assert _scouting_alerts([
        _unit(2, can_attack=False, is_idle=True, unit_type="harv"),
    ]) == []


def test_no_scouting_emitted_when_idle_combat_unit_exists():
    alerts = _scouting_alerts([_unit(3, can_attack=True, is_idle=True)])
    assert len(alerts) == 1
    assert "1 idle combat units available" in alerts[0]
    assert "quadrant exploration" in alerts[0]


def test_no_scouting_counts_only_idle_combat_units():
    alerts = _scouting_alerts([
        _unit(4, can_attack=True, is_idle=True),
        _unit(5, can_attack=True, is_idle=False),
        _unit(6, can_attack=False, is_idle=True, unit_type="harv"),
    ])
    assert len(alerts) == 1
    assert "1 idle combat units available" in alerts[0]
