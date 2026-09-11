from __future__ import annotations

from pathlib import Path

from openra_env.server.openra_environment import OpenRAEnvironment


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openra_env/server/openra_environment.py"


def _production(*items: str) -> list[dict]:
    return [
        {
            "queue_type": "Infantry",
            "item": item,
            "progress": 0.0,
            "remaining_ticks": 100,
            "remaining_cost": 100,
            "paused": False,
        }
        for item in items
    ]


def _obs(*items: str) -> dict:
    return {
        "available_production": ["e1", "e3"],
        "production": _production(*items),
        "economy": {"cash": 5000, "ore": 0},
        "units": [],
    }


def test_empty_queue_admits_existing_per_call_ceiling():
    assert (
        OpenRAEnvironment._unit_production_queue_hold(
            _obs(),
            "e1",
            10,
            held_tool="build_unit",
        )
        is None
    )


def test_nine_pending_e1_admits_one_more():
    assert (
        OpenRAEnvironment._unit_production_queue_hold(
            _obs(*(["e1"] * 9)),
            "e1",
            1,
            held_tool="build_unit",
        )
        is None
    )


def test_nine_pending_e1_rejects_request_for_two():
    result = OpenRAEnvironment._unit_production_queue_hold(
        _obs(*(["e1"] * 9)),
        "e1",
        2,
        held_tool="build_unit",
    )

    assert result is not None
    assert result["unit_production_queue_hold"] is True
    assert result["executed"] is False
    assert result["held_tool"] == "build_unit"
    assert result["requested_unit_type"] == "e1"
    assert result["requested_count"] == 2
    assert result["pending_same_type"] == 9
    assert result["max_pending_same_type"] == 10
    assert result["available_slots"] == 1
    assert result["pending_after_request"] == 11
    assert "10" in result["reason"]
    assert "1" in result["next_step"]


def test_ten_pending_e1_rejects_another_e1():
    result = OpenRAEnvironment._unit_production_queue_hold(
        _obs(*(["e1"] * 10)),
        "e1",
        1,
        held_tool="build_unit",
    )

    assert result is not None
    assert result["pending_same_type"] == 10
    assert result["available_slots"] == 0


def test_other_unit_types_do_not_consume_e1_slots():
    assert (
        OpenRAEnvironment._unit_production_queue_hold(
            _obs(*(["e3"] * 10)),
            "e1",
            10,
            held_tool="build_unit",
        )
        is None
    )


def test_compound_conversion_cannot_bypass_full_same_unit_queue():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = _obs(*(["e1"] * 10))

    commands = env._action_to_commands(
        {"tool": "build_unit", "unit_type": "e1", "count": 1},
        obs,
    )

    assert commands == []


def test_compound_count_is_clamped_to_existing_direct_ceiling():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = _obs()

    commands = env._action_to_commands(
        {"tool": "build_unit", "unit_type": "e1", "count": 100},
        obs,
    )

    assert len(commands) == 10
    assert all(command.item_type == "e1" for command in commands)


def test_direct_build_unit_guard_precedes_command_construction_and_execution():
    source = SOURCE.read_text(encoding="utf-8")

    start = source.index("def build_unit(")
    end = source.index("def build_structure(", start)
    block = source[start:end]

    normalize_index = block.index("count = max(1, min(count, 10))")
    hold_index = block.index("_unit_production_queue_hold(")
    command_index = block.index("CommandModel(")
    execute_index = block.index("_execute_commands(")

    assert normalize_index < hold_index < command_index < execute_index


def test_compound_build_unit_guard_precedes_command_construction():
    source = SOURCE.read_text(encoding="utf-8")

    start = source.index('if tool == "build_unit":')
    end = source.index('elif tool == "build_structure":', start)
    block = source[start:end]

    assert 'count = max(1, min(action.get("count", 1), 10))' in block
    hold_index = block.index("_unit_production_queue_hold(")
    command_index = block.index("CommandModel(")

    assert hold_index < command_index
