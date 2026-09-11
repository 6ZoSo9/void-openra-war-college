from __future__ import annotations

from pathlib import Path

from openra_env.server.openra_environment import OpenRAEnvironment

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openra_env/server/openra_environment.py"


def _obs(width: int = 112, height: int = 54) -> dict:
    return {
        "units": [{"actor_id": 126, "type": "e1", "can_attack": True, "is_idle": True}],
        "map_info": {"width": width, "height": height, "map_name": "Singles"},
    }


def test_valid_target_corners_are_admitted():
    obs = _obs()
    assert OpenRAEnvironment._movement_target_bounds_hold(
        obs, 0, 0, held_tool="move_units"
    ) is None
    assert OpenRAEnvironment._movement_target_bounds_hold(
        obs, 111, 53, held_tool="attack_move"
    ) is None


def test_out_of_bounds_target_fails_closed_with_legal_ranges():
    result = OpenRAEnvironment._movement_target_bounds_hold(
        _obs(), 60, 60, held_tool="attack_move"
    )
    assert result is not None
    assert result["movement_target_bounds_hold"] is True
    assert result["executed"] is False
    assert result["held_tool"] == "attack_move"
    assert result["requested_target"] == {"x": 60, "y": 60}
    assert result["map"] == {"width": 112, "height": 54}
    assert result["valid_target_x"] == [0, 111]
    assert result["valid_target_y"] == [0, 53]
    assert "outside map bounds" in result["reason"]
    assert "0..111" in result["next_step"]
    assert "0..53" in result["next_step"]


def test_negative_target_fails_closed():
    result = OpenRAEnvironment._movement_target_bounds_hold(
        _obs(), -1, 10, held_tool="patrol_units"
    )
    assert result is not None
    assert result["requested_target"] == {"x": -1, "y": 10}


def test_unknown_map_dimensions_do_not_invent_rejection():
    obs = {"units": _obs()["units"], "map_info": {"width": 0, "height": 0}}
    assert OpenRAEnvironment._movement_target_bounds_hold(
        obs, 60, 60, held_tool="move_units"
    ) is None


def test_compound_attack_move_cannot_bypass_bounds():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = _obs()
    invalid = env._action_to_commands(
        {"tool": "attack_move", "unit_ids": [126], "target_x": 60, "target_y": 60},
        obs,
    )
    valid = env._action_to_commands(
        {"tool": "attack_move", "unit_ids": [126], "target_x": 50, "target_y": 50},
        obs,
    )
    assert invalid == []
    assert len(valid) == 1
    assert valid[0].target_x == 50
    assert valid[0].target_y == 50


def test_compound_move_units_cannot_bypass_bounds():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    invalid = env._action_to_commands(
        {"tool": "move_units", "unit_ids": [126], "target_x": 112, "target_y": 53},
        _obs(),
    )
    assert invalid == []


def test_direct_movement_guards_precede_command_execution():
    source = SOURCE.read_text(encoding="utf-8")
    for function_name, next_name in (
        ("move_units", "attack_move"),
        ("attack_move", "attack_target"),
        ("patrol_units", "load_transport"),
    ):
        start = source.index(f"def {function_name}(")
        end = source.index(f"def {next_name}(", start)
        block = source[start:end]
        assert block.index("_movement_target_bounds_hold(") < block.index("CommandModel(")
        assert block.index("_movement_target_bounds_hold(") < block.index("_execute_commands(")


def test_group_guard_precedes_group_command_construction():
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("def command_group(")
    end = source.index("def get_replay_path(", start)
    block = source[start:end]
    assert block.index("_movement_target_bounds_hold(") < block.index(
        'if command == "attack_move":'
    )


def test_compound_source_contract_checks_bounds_before_commands():
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("def _action_to_commands(")
    end = source.index("def _build_initial_obs_from_state(", start)
    block = source[start:end]
    for tool_name in ("attack_move", "move_units"):
        branch = block.index(f'elif tool == "{tool_name}":')
        next_branch = block.find("elif tool ==", branch + 1)
        section = block[branch:] if next_branch < 0 else block[branch:next_branch]
        assert "_movement_target_bounds_hold(" in section
        assert section.index("_movement_target_bounds_hold(") < section.index("CommandModel(")
