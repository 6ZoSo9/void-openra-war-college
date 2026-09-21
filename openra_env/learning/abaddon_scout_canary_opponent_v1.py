"""Pure deterministic pressure opponent for scout-repair causal canaries.

This module proposes one action from a caller-supplied CURRENT tool contract. It
never dispatches, validates, loads a model, reads files, opens a socket, or grants
execution authority. A future canary runner must pass the proposal through the
unchanged host validator and record the exact source identity.

The policy is intentionally simple and non-learning: attack visible contact;
otherwise replenish a critically small infantry force when the exact typed tool
is offered; otherwise pressure the opposite half of the map with attack_move;
otherwise advance. It is an isolation instrument, not an Apollyon performance
claim or training target.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

SCHEMA = "void.abaddon.scout-canary.deterministic-pressure-opponent.v1"
MAX_ACTORS = 4096
MAX_TOOL_NAMES = 512


class DeterministicOpponentHold(ValueError):
    pass


def _require(value: bool, reason: str) -> None:
    if not value:
        raise DeterministicOpponentHold(reason)


def _owned_combat(state: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = state.get("units_summary")
    _require(type(rows) is list and len(rows) <= MAX_ACTORS, "owned_units_required")
    out = []
    for row in rows:
        _require(isinstance(row, Mapping), "owned_unit_object_required")
        uid = row.get("id")
        _require(type(uid) is int and uid > 0, "owned_unit_id_invalid")
        if row.get("can_attack") is True:
            out.append(row)
    return out


def _visible_targets(state: Mapping[str, Any]) -> list[int]:
    targets = []
    for key in ("enemy_summary", "enemy_buildings_summary"):
        rows = state.get(key)
        _require(type(rows) is list and len(rows) <= MAX_ACTORS, "visible_enemy_census_required")
        for row in rows:
            _require(isinstance(row, Mapping), "visible_enemy_object_required")
            uid = row.get("id")
            _require(type(uid) is int and uid > 0, "visible_enemy_id_invalid")
            targets.append(uid)
    return sorted(set(targets))


def _pressure_target(state: Mapping[str, Any]) -> tuple[int, int]:
    map_state = state.get("map")
    _require(isinstance(map_state, Mapping), "map_required")
    width, height = map_state.get("width"), map_state.get("height")
    _require(type(width) is int and 22 <= width <= 4096, "map_width_invalid")
    _require(type(height) is int and 22 <= height <= 4096, "map_height_invalid")
    buildings = state.get("buildings_summary")
    _require(type(buildings) is list and len(buildings) <= MAX_ACTORS, "building_census_required")
    positions = []
    for row in buildings:
        _require(isinstance(row, Mapping), "building_object_required")
        x, y = row.get("cell_x"), row.get("cell_y")
        if type(x) is int and type(y) is int and 0 <= x < width and 0 <= y < height:
            if str(row.get("type")) in {"fact", "proc", "barr", "tent", "powr"}:
                positions.append((x, y))
    _require(bool(positions), "base_position_required")
    bx = positions[0][0]
    target_x = width - 11 if bx < width // 2 else 10
    target_y = height // 2
    return target_x, target_y


def propose_deterministic_pressure_action(
    state: Mapping[str, Any], *, offered_tool_names: Sequence[str],
) -> dict[str, Any]:
    """Return a deterministic proposal that still requires unchanged host validation."""
    _require(isinstance(state, Mapping), "state_object_required")
    names = tuple(offered_tool_names)
    _require(0 < len(names) <= MAX_TOOL_NAMES and all(type(name) is str and name for name in names),
             "offered_tool_names_invalid")
    _require(len(names) == len(set(names)), "offered_tool_names_duplicate")
    offered = set(names)
    combat = _owned_combat(state)
    visible = _visible_targets(state)

    if visible and combat and "attack_target" in offered:
        tool = "attack_target"
        args = {"unit_ids": "all_combat", "target_actor_id": visible[0]}
        reason = "VISIBLE_CONTACT_LOWEST_ID_TARGET"
    elif len(combat) < 2 and "train_unit_e1" in offered:
        tool = "train_unit_e1"
        args = {"count": 1}
        reason = "REPLENISH_CRITICAL_INFANTRY_FORCE"
    elif combat and "attack_move" in offered:
        x, y = _pressure_target(state)
        tool = "attack_move"
        args = {"unit_ids": "all_combat", "target_x": x, "target_y": y, "queued": False}
        reason = "DETERMINISTIC_OPPOSITE_HALF_PRESSURE"
    elif "train_unit_e1" in offered:
        tool = "train_unit_e1"
        args = {"count": 1}
        reason = "REBUILD_INFANTRY_FORCE"
    elif "advance" in offered:
        tool = "advance"
        args = {}
        reason = "NO_REVIEWED_PRESSURE_ACTION_AVAILABLE"
    else:
        raise DeterministicOpponentHold("no_supported_offered_action")

    _require(tool in offered, "selected_tool_not_offered")
    return {
        "schema": SCHEMA,
        "tool": tool,
        "arguments": deepcopy(args),
        "reason": reason,
        "decision_source": "deterministic_pressure_opponent_v1",
        "deterministic": True,
        "model_backed": False,
        "learning_performed": False,
        "host_validation_required": True,
        "world_mutated_before_validation": False,
        "execution_authority": False,
        "training_use_approved": False,
        "automatic_promotion": False,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise DeterministicOpponentHold("HOST_VALIDATION_AND_SEPARATE_CANARY_AUTHORITY_REQUIRED")
