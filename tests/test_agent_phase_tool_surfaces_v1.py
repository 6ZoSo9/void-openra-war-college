from __future__ import annotations

import inspect

from openra_env.agent import (
    GAMEPLAY_HIDDEN_TOOL_NAMES,
    PLANNING_LLM_TOOL_NAMES,
    _phase_scoped_tool_surfaces,
    run_agent,
)


def tool(name: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": name,
            "parameters": {"type": "object", "properties": {}},
        },
    }


def names(tools: list[dict]) -> list[str]:
    return [item["function"]["name"] for item in tools]


def test_planning_surface_is_narrow_and_host_phase_entry_is_hidden():
    discovered = [
        tool("start_planning_phase"),
        tool("get_faction_briefing"),
        tool("get_map_analysis"),
        tool("get_opponent_intel"),
        tool("batch_lookup"),
        tool("end_planning_phase"),
        tool("get_planning_status"),
        tool("deploy_unit"),
        tool("build_structure"),
        tool("advance"),
    ]
    planning, gameplay = _phase_scoped_tool_surfaces(discovered)
    assert set(names(planning)) == set(PLANNING_LLM_TOOL_NAMES)
    assert "start_planning_phase" not in names(planning)
    assert "get_planning_status" not in names(planning)
    assert "deploy_unit" not in names(planning)
    assert "build_structure" not in names(planning)
    assert "advance" not in names(planning)
    assert GAMEPLAY_HIDDEN_TOOL_NAMES.isdisjoint(names(gameplay))


def test_gameplay_retains_normal_actions_but_hides_planning_controls():
    discovered = [
        tool("start_planning_phase"),
        tool("end_planning_phase"),
        tool("get_planning_status"),
        tool("get_game_state"),
        tool("deploy_unit"),
        tool("build_structure"),
        tool("move_units"),
        tool("attack_target"),
        tool("advance"),
    ]
    _, gameplay = _phase_scoped_tool_surfaces(discovered)
    assert names(gameplay) == [
        "get_game_state",
        "deploy_unit",
        "build_structure",
        "move_units",
        "attack_target",
        "advance",
    ]


def test_phase_filter_preserves_discovery_order():
    discovered = [
        tool("batch_lookup"),
        tool("get_opponent_intel"),
        tool("end_planning_phase"),
        tool("get_map_analysis"),
        tool("get_faction_briefing"),
    ]
    planning, gameplay = _phase_scoped_tool_surfaces(discovered)
    assert names(planning) == names(discovered)
    assert names(gameplay) == [
        "batch_lookup",
        "get_opponent_intel",
        "get_map_analysis",
        "get_faction_briefing",
    ]


def test_run_agent_wires_distinct_phase_surfaces_into_provider_calls():
    source = "".join(inspect.getsource(run_agent).split())
    assert (
        "chat_completion(messages,planning_openai_tools,llm_config,"
        "verbose,prompts=config.prompts)" in source
    )
    assert (
        "chat_completion(messages,gameplay_openai_tools,llm_config,"
        "verbose,prompts=config.prompts)" in source
    )
    assert (
        "chat_completion(messages,openai_tools,llm_config,"
        "verbose,prompts=config.prompts)" not in source
    )
