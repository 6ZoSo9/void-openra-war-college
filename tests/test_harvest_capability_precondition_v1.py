from __future__ import annotations

from pathlib import Path

from openra_env.server.openra_environment import OpenRAEnvironment


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openra_env/server/openra_environment.py"


def _unit(actor_id: int, unit_type: str) -> dict:
    return {
        "actor_id": actor_id,
        "type": unit_type,
        "cell_x": 10,
        "cell_y": 10,
        "is_idle": True,
        "can_attack": unit_type != "harv",
    }


def _obs(*units: dict) -> dict:
    return {
        "units": list(units),
        "map_info": {"width": 112, "height": 54, "map_name": "Singles"},
    }


def test_rifle_infantry_is_rejected_as_harvester_with_exact_facts():
    result = OpenRAEnvironment._harvest_precondition_hold(
        _obs(_unit(126, "e1")),
        126,
        held_tool="harvest",
    )

    assert result is not None
    assert result["harvest_precondition_hold"] is True
    assert result["executed"] is False
    assert result["held_tool"] == "harvest"
    assert result["requested_unit"] == {"id": 126, "type": "e1"}
    assert result["required_unit_type"] == "harv"
    assert result["required_unit_name"] == "Ore Truck"
    assert result["required_prerequisites"] == ["proc"]
    assert result["available_harvesters"] == []
    assert "not a harvester" in result["reason"]
    assert "harv" in result["next_step"]


def test_available_harvester_ids_are_returned_on_invalid_request():
    result = OpenRAEnvironment._harvest_precondition_hold(
        _obs(_unit(126, "e1"), _unit(200, "harv")),
        126,
        held_tool="harvest",
    )

    assert result is not None
    assert result["available_harvesters"] == [{"id": 200, "type": "harv"}]


def test_real_harvester_is_admitted():
    assert (
        OpenRAEnvironment._harvest_precondition_hold(
            _obs(_unit(200, "harv")),
            200,
            held_tool="harvest",
        )
        is None
    )


def test_missing_unit_is_left_to_existing_not_found_contract():
    assert (
        OpenRAEnvironment._harvest_precondition_hold(
            _obs(_unit(126, "e1")),
            999,
            held_tool="harvest",
        )
        is None
    )


def test_compound_conversion_rejects_non_harvester():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = _obs(_unit(126, "e1"))

    commands = env._action_to_commands(
        {"tool": "harvest", "unit_id": 126},
        obs,
    )

    assert commands == []


def test_compound_conversion_admits_real_harvester():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = _obs(_unit(200, "harv"))

    commands = env._action_to_commands(
        {"tool": "harvest", "unit_id": 200},
        obs,
    )

    assert len(commands) == 1
    assert commands[0].actor_id == 200
    assert commands[0].target_x == 0
    assert commands[0].target_y == 0


def test_direct_harvest_guard_precedes_command_construction_and_execution():
    source = SOURCE.read_text(encoding="utf-8")

    start = source.index("def harvest(")
    end = source.index("def power_down(", start)
    block = source[start:end]

    hold_index = block.index("_harvest_precondition_hold(")
    command_index = block.index("CommandModel(")
    execute_index = block.index("_execute_commands(")

    assert hold_index < command_index < execute_index


def test_compound_harvest_guard_precedes_command_construction():
    source = SOURCE.read_text(encoding="utf-8")

    start = source.index('elif tool == "harvest":')
    end = source.index('elif tool == "load_transport":', start)
    block = source[start:end]

    hold_index = block.index("_harvest_precondition_hold(")
    command_index = block.index("CommandModel(")

    assert hold_index < command_index
