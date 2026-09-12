from __future__ import annotations

import asyncio
import inspect
from types import SimpleNamespace

from fastmcp import FastMCP

from openra_env.config import OpenRARLConfig
from openra_env.models import ActionType, CommandModel
from openra_env.server.openra_environment import OpenRAEnvironment


def _production(item: str, queue_type: str = "Building") -> dict:
    return {
        "queue_type": queue_type,
        "item": item,
        "progress": 0.5,
        "remaining_ticks": 100,
        "remaining_cost": 100,
        "paused": False,
    }


def _call(value):
    if inspect.isawaitable(value):
        return asyncio.run(value)
    return value


def _direct_env(queue: list[dict]):
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    env._app_config = OpenRARLConfig()
    env._last_obs = {"production": queue}
    env._refresh_obs = lambda: None

    captured: dict[str, object] = {}

    def execute(commands):
        captured["commands"] = commands
        return {"executed": True}

    env._execute_commands = execute

    mcp = FastMCP("cancel-production-test")
    env._register_tools(mcp)
    return env, mcp, captured


def test_direct_cancel_matches_canonical_item_field():
    _, mcp, captured = _direct_env([_production("proc")])
    tool = mcp._tool_manager._tools["cancel_production"]

    result = _call(tool.fn(item_type="proc"))

    assert result["executed"] is True
    commands = captured["commands"]
    assert len(commands) == 1
    assert commands[0].action == ActionType.CANCEL_PRODUCTION
    assert commands[0].item_type == "proc"


def test_direct_cancel_preserves_case_insensitive_lookup_but_uses_canonical_item():
    _, mcp, captured = _direct_env([_production("proc")])
    tool = mcp._tool_manager._tools["cancel_production"]

    result = _call(tool.fn(item_type="PROC"))

    assert result["executed"] is True
    commands = captured["commands"]
    assert commands[0].item_type == "proc"


def test_direct_cancel_missing_item_reports_real_queue_contents():
    _, mcp, captured = _direct_env([
        _production("proc"),
        _production("e1", queue_type="Infantry"),
    ])
    tool = mcp._tool_manager._tools["cancel_production"]

    result = _call(tool.fn(item_type="powr"))

    assert result["error"] == "'powr' is not in the production queue."
    assert result["current_queue"] == ["proc", "e1"]
    assert "commands" not in captured


def test_compound_cancel_matches_canonical_item_field():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = {"production": [_production("proc")]}

    commands = env._action_to_commands(
        {"tool": "cancel_production", "item_type": "PROC"},
        obs,
    )

    assert len(commands) == 1
    assert commands[0].action == ActionType.CANCEL_PRODUCTION
    assert commands[0].item_type == "proc"


def test_compound_cancel_rejects_genuinely_absent_item():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = {"production": [_production("proc")]}

    commands = env._action_to_commands(
        {"tool": "cancel_production", "item_type": "powr"},
        obs,
    )

    assert commands == []


def _execution_obs(production: list[dict]) -> dict:
    return {
        "tick": 10,
        "done": False,
        "result": "",
        "economy": {},
        "units": [],
        "buildings": [],
        "visible_enemies": [],
        "production": production,
    }


def _execution_env(production_after: list[dict]):
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    env._app_config = SimpleNamespace(
        alerts=SimpleNamespace(loss_tracking=False),
    )
    env._pending_placements = {"proc": {"cell_x": 0, "cell_y": 0}}
    env._attempted_placements = {"proc": 1}
    env._last_obs = _execution_obs([_production("proc")])
    env._step_internal = lambda action: _execution_obs(production_after)
    env._process_pending_placements = lambda: None
    return env


def test_successful_cancel_clears_auto_place_metadata_after_observation():
    env = _execution_env([])

    env._execute_commands([
        CommandModel(action=ActionType.CANCEL_PRODUCTION, item_type="proc"),
    ])

    assert "proc" not in env._pending_placements
    assert "proc" not in env._attempted_placements


def test_cancel_does_not_clear_metadata_while_item_remains_in_queue():
    env = _execution_env([_production("proc")])

    env._execute_commands([
        CommandModel(action=ActionType.CANCEL_PRODUCTION, item_type="proc"),
    ])

    assert "proc" in env._pending_placements
    assert "proc" in env._attempted_placements
