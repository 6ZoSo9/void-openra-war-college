"""Closed runtime classification for the Generation-2 frontier adapter.

This module grants no execution authority.  In an active G2 adapter mode every
runtime-discovered tool must have an explicit class; unknown names fail closed.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Iterable

OBSERVATION_CONTROL = "observation_or_control"
MUTATION_CAPABLE = "mutation_capable"

# Explicitly closed against the MCP surface at the reviewed PR #40 generation.
# Lifecycle/planning controls are intentionally not tactical-competence actions.
_TOOL_CLASSIFICATION = {
    # Observation / knowledge / planning / lifecycle controls.
    "get_game_state": OBSERVATION_CONTROL,
    "get_economy": OBSERVATION_CONTROL,
    "get_units": OBSERVATION_CONTROL,
    "get_buildings": OBSERVATION_CONTROL,
    "get_enemies": OBSERVATION_CONTROL,
    "get_production": OBSERVATION_CONTROL,
    "get_map_info": OBSERVATION_CONTROL,
    "get_exploration_status": OBSERVATION_CONTROL,
    "lookup_unit": OBSERVATION_CONTROL,
    "lookup_building": OBSERVATION_CONTROL,
    "lookup_tech_tree": OBSERVATION_CONTROL,
    "lookup_faction": OBSERVATION_CONTROL,
    "get_faction_briefing": OBSERVATION_CONTROL,
    "get_map_analysis": OBSERVATION_CONTROL,
    "batch_lookup": OBSERVATION_CONTROL,
    "get_opponent_intel": OBSERVATION_CONTROL,
    "start_planning_phase": OBSERVATION_CONTROL,
    "end_planning_phase": OBSERVATION_CONTROL,
    "get_planning_status": OBSERVATION_CONTROL,
    "list_transports": OBSERVATION_CONTROL,
    "get_valid_placements": OBSERVATION_CONTROL,
    "get_groups": OBSERVATION_CONTROL,
    "get_replay_path": OBSERVATION_CONTROL,
    "get_terrain_at": OBSERVATION_CONTROL,
    "start_game": OBSERVATION_CONTROL,
    "surrender": OBSERVATION_CONTROL,
    # World- or command-state mutations.
    "advance": MUTATION_CAPABLE,
    "move_units": MUTATION_CAPABLE,
    "attack_move": MUTATION_CAPABLE,
    "attack_target": MUTATION_CAPABLE,
    "stop_units": MUTATION_CAPABLE,
    "build_unit": MUTATION_CAPABLE,
    "build_structure": MUTATION_CAPABLE,
    "build_and_place": MUTATION_CAPABLE,
    "place_building": MUTATION_CAPABLE,
    "cancel_production": MUTATION_CAPABLE,
    "deploy_unit": MUTATION_CAPABLE,
    "sell_building": MUTATION_CAPABLE,
    "repair_building": MUTATION_CAPABLE,
    "set_rally_point": MUTATION_CAPABLE,
    "guard_target": MUTATION_CAPABLE,
    "patrol_units": MUTATION_CAPABLE,
    "load_transport": MUTATION_CAPABLE,
    "unload_transport": MUTATION_CAPABLE,
    "set_stance": MUTATION_CAPABLE,
    "harvest": MUTATION_CAPABLE,
    "power_down": MUTATION_CAPABLE,
    "set_primary": MUTATION_CAPABLE,
    "assign_group": MUTATION_CAPABLE,
    "add_to_group": MUTATION_CAPABLE,
    "command_group": MUTATION_CAPABLE,
    "batch": MUTATION_CAPABLE,
    "plan": MUTATION_CAPABLE,
}
TOOL_CLASSIFICATION = MappingProxyType(_TOOL_CLASSIFICATION)


class ToolClassificationHold(RuntimeError):
    """Fail-closed runtime classification error."""


def _name(value: object) -> str:
    if isinstance(value, str):
        name = value
    elif isinstance(value, dict):
        name = value.get("name")
    else:
        name = getattr(value, "name", None)
    if not isinstance(name, str) or not name:
        raise ToolClassificationHold("invalid_discovered_tool")
    return name


def discovered_tool_names(tools: Iterable[object]) -> tuple[str, ...]:
    names = tuple(_name(tool) for tool in tools)
    if len(names) != len(set(names)):
        raise ToolClassificationHold("duplicate_discovered_tool")
    return names


def validate_discovered_tool_surface(tools: Iterable[object]) -> tuple[str, ...]:
    names = discovered_tool_names(tools)
    unknown = sorted(set(names) - set(TOOL_CLASSIFICATION))
    if unknown:
        raise ToolClassificationHold(
            "unclassified_runtime_tools:" + ",".join(unknown)
        )
    return names


def classify_tool(tool_name: str) -> str:
    if not isinstance(tool_name, str) or not tool_name:
        raise ToolClassificationHold("invalid_tool_name")
    try:
        return TOOL_CLASSIFICATION[tool_name]
    except KeyError as exc:
        raise ToolClassificationHold(
            "unclassified_tool_call:" + tool_name
        ) from exc


def is_mutation_capable(tool_name: str) -> bool:
    return classify_tool(tool_name) == MUTATION_CAPABLE
