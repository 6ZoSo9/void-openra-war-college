from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .general_brain_policy_adapter import MILLIS, validate_policy_adapter


class GeneralBrainDirectPolicyError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GeneralBrainDirectPolicyError(message)


def _combat_unit_count(state: Mapping[str, Any]) -> int:
    units = state.get("units_summary")
    if not isinstance(units, list):
        return 0
    return sum(
        1
        for unit in units
        if isinstance(unit, Mapping) and unit.get("can_attack") is True
    )


def _map_dimensions(state: Mapping[str, Any]) -> tuple[int, int] | None:
    raw = state.get("map")
    if not isinstance(raw, Mapping):
        return None
    width, height = raw.get("width"), raw.get("height")
    if type(width) is not int or type(height) is not int or width <= 1 or height <= 1:
        return None
    return width, height


def propose_direct_policy_action(
    adapter: Mapping[str, Any],
    *,
    state: Mapping[str, Any],
    mode: str,
    previous_mode: str | None,
    offered_tool_names: Sequence[str],
) -> dict[str, Any] | None:
    """Return one deterministic candidate proposal or None.

    This function does not authorize or execute anything. The caller must pass
    the proposal through the unchanged host decision_to_commands_typed validator
    before any world mutation. No learned policy means no prompt injection and
    no behavioral change.
    """

    validate_policy_adapter(adapter)
    _require(isinstance(mode, str) and mode, "mode must be nonempty text")
    _require(previous_mode is None or isinstance(previous_mode, str), "previous_mode malformed")
    names = tuple(offered_tool_names)
    _require(all(isinstance(name, str) and name for name in names), "offered tools malformed")
    _require(len(names) == len(set(names)), "offered tools contain duplicates")

    policies = adapter.get("policies")
    _require(isinstance(policies, Mapping), "adapter policies missing")
    raw = policies.get(mode)
    if not isinstance(raw, Mapping):
        return None
    if raw.get("application") == "mode_entry_only" and previous_mode == mode:
        return None

    tool = raw.get("tool")
    if not isinstance(tool, str) or tool not in names:
        return None
    if tool != "move_units":
        return None
    if _combat_unit_count(state) < 1:
        return None
    dimensions = _map_dimensions(state)
    if dimensions is None:
        return None
    width, height = dimensions

    x_millis, y_millis = raw.get("target_x_millis"), raw.get("target_y_millis")
    if type(x_millis) is not int or type(y_millis) is not int:
        return None
    if not (0 <= x_millis <= MILLIS and 0 <= y_millis <= MILLIS):
        return None
    target_x = int(round((x_millis / MILLIS) * (width - 1)))
    target_y = int(round((y_millis / MILLIS) * (height - 1)))
    if not (0 <= target_x < width and 0 <= target_y < height):
        return None

    return {
        "tool": "move_units",
        "arguments": {
            "unit_ids": "all_combat",
            "target_x": target_x,
            "target_y": target_y,
            "queued": False,
        },
        "decision_source": "general_brain_direct_policy",
        "generation": 1,
        "candidate_revision": 2,
        "mode": mode,
        "policy_application": raw.get("application"),
        "target_policy": raw.get("target_policy"),
        "host_validation_required": True,
        "world_mutated_before_validation": False,
        "authority_envelope_trainable": False,
        "tool_authorization_trainable": False,
        "automatic_weight_install": False,
        "automatic_promotion": False,
    }


def validate_host_prevalidated_proposal(
    proposal: Mapping[str, Any],
    *,
    validation_ok: bool,
    validation_reason: str,
) -> dict[str, Any]:
    """Bind the pure host validation result without converting it to authority."""

    _require(isinstance(proposal, Mapping), "proposal must be an object")
    _require(proposal.get("host_validation_required") is True, "proposal bypassed host validation")
    _require(proposal.get("world_mutated_before_validation") is False, "proposal mutated world before validation")
    _require(isinstance(validation_ok, bool), "validation_ok must be boolean")
    _require(isinstance(validation_reason, str), "validation_reason must be text")
    return {
        **dict(proposal),
        "host_prevalidated": validation_ok,
        "host_validation_reason": validation_reason,
        "proposal_eligible_for_execution": validation_ok,
        "execution_authority": False,
    }


__all__ = [
    "GeneralBrainDirectPolicyError",
    "propose_direct_policy_action",
    "validate_host_prevalidated_proposal",
]
