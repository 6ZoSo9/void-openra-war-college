from __future__ import annotations

from tests.test_mcp_tools import _make_env_with_tools, _make_spatial


def _obs_with_quadrant_fog() -> dict:
    fog = {}
    for y in range(4):
        for x in range(4):
            # Only the NE quadrant is explored.
            fog[(x, y)] = 1.0 if x >= 2 and y < 2 else 0.0

    return {
        "tick": 1000,
        "done": False,
        "result": "",
        "economy": {
            "cash": 5000,
            "ore": 1000,
            "power_provided": 200,
            "power_drained": 80,
            "resource_capacity": 5000,
            "harvester_count": 1,
        },
        "military": {
            "units_killed": 0,
            "units_lost": 0,
            "buildings_killed": 0,
            "buildings_lost": 0,
            "army_value": 100,
            "active_unit_count": 1,
        },
        "units": [
            {
                "actor_id": 1,
                "type": "e1",
                "cell_x": 1,
                "cell_y": 1,
                "pos_x": 1024,
                "pos_y": 1024,
                "hp_percent": 1.0,
                "is_idle": True,
                "current_activity": "",
                "owner": "Multi1",
                "can_attack": True,
                "facing": 0,
                "experience_level": 0,
                "stance": 3,
                "speed": 56,
                "attack_range": 5120,
                "passenger_count": -1,
                "is_building": False,
            },
        ],
        "buildings": [
            {
                "actor_id": 100,
                "type": "fact",
                "pos_x": 2048,
                "pos_y": 2048,
                "hp_percent": 1.0,
                "owner": "Multi1",
                "is_producing": False,
                "production_progress": 0.0,
                "producing_item": "",
                "is_powered": True,
                "is_repairing": False,
                "sell_value": 500,
                "rally_x": -1,
                "rally_y": -1,
                "power_amount": 0,
                "can_produce": ["powr"],
                "cell_x": 2,
                "cell_y": 2,
            },
        ],
        "production": [],
        "visible_enemies": [],
        "visible_enemy_buildings": [],
        "map_info": {"width": 4, "height": 4, "map_name": "Test"},
        "spatial_map": _make_spatial(4, 4, fog_values=fog),
        "spatial_channels": 9,
        "available_production": ["e1"],
    }


def test_no_scouting_alert_shows_quadrant_exploration_facts():
    obs = _obs_with_quadrant_fog()
    env, mcp = _make_env_with_tools(obs)
    env._app_config.alerts.no_scouting = True

    tool = mcp._tool_manager._tools["get_game_state"]
    result = tool.fn()

    scouting_alerts = [a for a in result["alerts"] if "NO SCOUTING" in a]
    assert len(scouting_alerts) == 1
    alert = scouting_alerts[0]

    assert "quadrant exploration" in alert
    assert "NW=0.0%" in alert
    assert "NE=100.0%" in alert
    assert "SW=0.0%" in alert
    assert "SE=0.0%" in alert

    lower = alert.lower()
    assert "send a unit" not in lower
    assert "target" not in lower
    assert "enemy estimated" not in lower
