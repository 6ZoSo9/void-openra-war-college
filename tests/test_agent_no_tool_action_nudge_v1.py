from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "openra_env/agent.py"


def _helper():
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    nodes = [
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "_no_tool_action_nudge"
    ]
    assert len(nodes) == 1
    ns = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(AGENT), "exec"), ns)
    return ns["_no_tool_action_nudge"]


def test_no_tool_nudge_surfaces_exact_current_action_state():
    nudge = _helper()
    state = {
        "tick": 840,
        "available_production": ["syrd", "proc", "powr", "tent", "e1", "e3", "medi"],
        "units_summary": [
            {"id": 126, "type": "e1", "idle": True},
            {"id": 127, "type": "e1", "idle": False},
            {"id": 128, "type": "e1", "idle": True},
        ],
    }
    result = nudge("No tool was called. A tool call is required each turn.", state)
    assert "Current tick: 840." in result
    assert "Current available_production: syrd, proc, powr, tent, e1, e3, medi." in result
    assert "Current idle unit IDs: 126, 128." in result
    assert "Issue one concrete valid tool call now" in result
    assert "If a desired production item is absent, do not retry it" in result


def test_no_tool_nudge_preserves_custom_base_text():
    nudge = _helper()
    result = nudge("Custom operator nudge.", {"tick": 5})
    assert result.startswith("Custom operator nudge.")
    assert "Current tick: 5." in result


def test_no_tool_nudge_reports_empty_available_production_truthfully():
    nudge = _helper()
    result = nudge("Act now.", {"tick": 4, "available_production": [], "units_summary": []})
    assert "Current available_production is empty." in result
    assert "Current idle unit IDs:" not in result


def test_no_tool_nudge_ignores_malformed_state_members():
    nudge = _helper()
    result = nudge("Act now.", {
        "tick": True,
        "available_production": ["powr", "", None, 7],
        "units_summary": [
            {"id": True, "idle": True},
            {"id": None, "idle": True},
            {"id": 12, "idle": False},
            "bad",
        ],
    })
    assert "Current tick:" not in result
    assert "Current available_production: powr." in result
    assert "Current idle unit IDs:" not in result


def test_no_tool_nudge_falls_back_for_non_mapping_state():
    nudge = _helper()
    assert nudge("No tool was called. A tool call is required each turn.", None) == (
        "No tool was called. A tool call is required each turn."
    )


def test_agent_uses_state_aware_nudge_at_exact_gameplay_no_tool_branch():
    source = AGENT.read_text(encoding="utf-8")
    handle_tool_calls = source.index("# Handle tool calls")
    start = source.index("if not tool_calls:", handle_tool_calls)
    end = source.index("continue", start)
    block = source[start:end]

    assert block.count("_no_tool_action_nudge(") == 1
    assert "config.prompts.no_tool_nudge" in block
    assert "latest_game_state" in block
    assert block.count("_append_traced_message(") == 1

    planning_start = source.index("# ─── Pre-Game Planning Phase")
    planning_end = source.index("# ─── Game Start", planning_start, handle_tool_calls)
    planning_block = source[planning_start:planning_end]
    assert '"content": prompts.planning_nudge' in planning_block
    assert "_no_tool_action_nudge(" not in planning_block
