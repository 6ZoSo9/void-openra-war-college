from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_PATH = ROOT / "openra_env/agent.py"

EXPECTED_PLANNING_TOOLS = {
    "get_faction_briefing",
    "get_map_analysis",
    "get_opponent_intel",
    "batch_lookup",
    "end_planning_phase",
}
EXPECTED_GAMEPLAY_HIDDEN_TOOLS = {
    "start_planning_phase",
    "end_planning_phase",
    "get_planning_status",
}


def _agent_tree() -> ast.Module:
    return ast.parse(AGENT_PATH.read_text(encoding="utf-8"))


def _phase_scope_namespace() -> dict:
    tree = _agent_tree()
    wanted_assignments = {
        "PLANNING_LLM_TOOL_NAMES",
        "GAMEPLAY_HIDDEN_TOOL_NAMES",
    }
    wanted_functions = {
        "_openai_tool_name",
        "_phase_scoped_tool_surfaces",
    }
    body: list[ast.stmt] = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = {
                target.id
                for target in node.targets
                if isinstance(target, ast.Name)
            }
            if names & wanted_assignments:
                body.append(node)
        elif (
            isinstance(node, ast.FunctionDef)
            and node.name in wanted_functions
        ):
            body.append(node)

    module = ast.Module(body=body, type_ignores=[])
    ast.fix_missing_locations(module)

    namespace: dict = {}
    exec(
        compile(module, str(AGENT_PATH), "exec"),
        namespace,
        namespace,
    )
    return namespace


def _tool(name: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": name,
            "parameters": {"type": "object", "properties": {}},
        },
    }


def _names(tools: list[dict]) -> list[str]:
    return [item["function"]["name"] for item in tools]


def test_phase_scope_constants_and_runtime_filter_are_exact():
    namespace = _phase_scope_namespace()

    assert set(namespace["PLANNING_LLM_TOOL_NAMES"]) == EXPECTED_PLANNING_TOOLS
    assert (
        set(namespace["GAMEPLAY_HIDDEN_TOOL_NAMES"])
        == EXPECTED_GAMEPLAY_HIDDEN_TOOLS
    )

    split = namespace["_phase_scoped_tool_surfaces"]
    discovered = [
        _tool("start_planning_phase"),
        _tool("get_faction_briefing"),
        _tool("get_map_analysis"),
        _tool("get_opponent_intel"),
        _tool("batch_lookup"),
        _tool("end_planning_phase"),
        _tool("get_planning_status"),
        _tool("get_game_state"),
        _tool("deploy_unit"),
        _tool("build_structure"),
        _tool("move_units"),
        _tool("attack_target"),
        _tool("advance"),
    ]

    planning, gameplay = split(discovered)

    assert _names(planning) == [
        "get_faction_briefing",
        "get_map_analysis",
        "get_opponent_intel",
        "batch_lookup",
        "end_planning_phase",
    ]
    assert _names(gameplay) == [
        "get_faction_briefing",
        "get_map_analysis",
        "get_opponent_intel",
        "batch_lookup",
        "get_game_state",
        "deploy_unit",
        "build_structure",
        "move_units",
        "attack_target",
        "advance",
    ]


def test_planning_hides_host_phase_entry_and_gameplay_mutations():
    namespace = _phase_scope_namespace()
    split = namespace["_phase_scoped_tool_surfaces"]

    discovered = [
        _tool("start_planning_phase"),
        _tool("end_planning_phase"),
        _tool("get_planning_status"),
        _tool("deploy_unit"),
        _tool("build_structure"),
        _tool("advance"),
    ]
    planning, _ = split(discovered)

    assert _names(planning) == ["end_planning_phase"]


def test_gameplay_hides_all_planning_controls_but_keeps_normal_actions():
    namespace = _phase_scope_namespace()
    split = namespace["_phase_scoped_tool_surfaces"]

    discovered = [
        _tool("start_planning_phase"),
        _tool("end_planning_phase"),
        _tool("get_planning_status"),
        _tool("get_game_state"),
        _tool("deploy_unit"),
        _tool("build_structure"),
        _tool("move_units"),
        _tool("attack_target"),
        _tool("advance"),
    ]
    _, gameplay = split(discovered)

    assert _names(gameplay) == [
        "get_game_state",
        "deploy_unit",
        "build_structure",
        "move_units",
        "attack_target",
        "advance",
    ]


def test_run_agent_wires_phase_surfaces_and_tool_free_reflection():
    tree = _agent_tree()
    run_agent = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef)
        and node.name == "run_agent"
    )

    calls: list[ast.Call] = []
    for node in ast.walk(run_agent):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "chat_completion":
            calls.append(node)

    calls.sort(key=lambda node: (node.lineno, node.col_offset))
    assert len(calls) == 3

    phase_calls: list[ast.Call] = []
    phase_tool_arguments: list[str] = []
    reflection_calls: list[ast.Call] = []

    for call in calls:
        if len(call.args) >= 2 and isinstance(call.args[1], ast.Name):
            phase_calls.append(call)
            phase_tool_arguments.append(call.args[1].id)

        for keyword in call.keywords:
            if (
                keyword.arg == "tools"
                and isinstance(keyword.value, ast.List)
                and keyword.value.elts == []
            ):
                reflection_calls.append(call)

    assert phase_tool_arguments == [
        "planning_openai_tools",
        "gameplay_openai_tools",
    ]
    assert len(phase_calls) == 2
    assert len(reflection_calls) == 1
    assert reflection_calls[0] not in phase_calls
