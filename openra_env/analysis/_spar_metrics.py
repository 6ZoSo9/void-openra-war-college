"""State, action, and summary contracts for spar analysis."""

from __future__ import annotations

from collections import Counter
from typing import Any

from ._spar_contract import (
    DAMAGE, ContractError, _arr, _bool, _int, _obj, _str,
)

def visible_count(state: dict[str, Any]) -> int:
    if "enemy_summary" in state or "enemy_buildings_summary" in state:
        return len(_arr(state.get("enemy_summary"), "enemy_summary")) + len(
            _arr(state.get("enemy_buildings_summary"), "enemy_buildings_summary")
        )
    return _int(state.get("visible_enemy_units"), "visible_enemy_units") + _int(
        state.get("visible_enemy_buildings"), "visible_enemy_buildings"
    )


def combat_count(state: dict[str, Any]) -> int:
    count = 0
    for index, raw in enumerate(_arr(state.get("units_summary"), "units_summary")):
        unit = _obj(raw, f"units_summary[{index}]")
        count += int(_bool(unit.get("can_attack"), f"units_summary[{index}].can_attack"))
    return count


def military(state: dict[str, Any]) -> dict[str, int]:
    source = _obj(state.get("military"), "military")
    if any(field not in source for field in DAMAGE):
        raise ContractError("military counters are incomplete")
    return {field: _int(source[field], f"military.{field}") for field in DAMAGE}


def _state(state: dict[str, Any], label: str, tick: int) -> None:
    if _int(state.get("tick"), f"{label}.tick") != tick:
        raise ContractError(f"{label} tick does not match world clock")
    visible_count(state)
    combat_count(state)
    military(state)


def _delta(before: dict[str, int], after: dict[str, int]) -> dict[str, int]:
    change = {field: after[field] - before[field] for field in DAMAGE}
    if any(value < 0 for value in change.values()):
        raise ContractError("military counters regressed within a round")
    return change


def _perspectives(apollyon: dict[str, int], abaddon: dict[str, int]) -> None:
    checks = (
        ("units_killed", "units_lost"), ("units_lost", "units_killed"),
        ("buildings_killed", "buildings_lost"),
        ("buildings_lost", "buildings_killed"),
        ("kills_cost", "deaths_cost"), ("deaths_cost", "kills_cost"),
    )
    if any(apollyon[left] != abaddon[right] for left, right in checks):
        raise ContractError("player perspectives disagree on military accounting")


def contact_episodes(rounds: list[int], gap: int = 2) -> list[dict[str, Any]]:
    if rounds != sorted(set(rounds)):
        raise ContractError("contact rounds must be strictly increasing")
    groups: list[list[int]] = []
    for number in rounds:
        if not groups or number - groups[-1][-1] > gap:
            groups.append([number])
        else:
            groups[-1].append(number)
    return [
        {"start_round": group[0], "end_round": group[-1], "rounds": group}
        for group in groups
    ]


def _action(decision: dict[str, Any], side: str, number: int) -> tuple[str, int, int]:
    data = _obj(decision.get(side), f"round {number} {side}")
    if side == "apollyon":
        tool = _str(data.get("tool"), "Apollyon tool")
        attempts = _arr(data.get("attempts"), "Apollyon attempts")
        accepted = []
        for index, raw in enumerate(attempts):
            attempt = _obj(raw, f"Apollyon attempt {index}")
            ok = _bool(attempt.get("accepted"), f"attempt {index}.accepted")
            _bool(
                attempt.get("world_mutated_before_validation"),
                f"attempt {index}.mutation",
                False,
            )
            if ok:
                accepted.append(attempt)
        if len(accepted) != 1 or accepted[0].get("tool") != tool:
            raise ContractError("accepted Apollyon attempt is not exact")
        offered = _arr(
            _obj(data.get("tool_contract"), "tool_contract").get("offered_tool_names"),
            "offered_tool_names",
        )
        if any(not isinstance(name, str) or not name for name in offered):
            raise ContractError("offered tools must be nonempty text")
        if len(offered) != len(set(offered)) or tool not in offered:
            raise ContractError("accepted Apollyon tool was not uniquely offered")
        attempts_count = len(attempts)
    else:
        _bool(data.get("accepted"), "Abaddon accepted", True)
        decision_obj = _obj(data.get("decision"), "Abaddon decision")
        action = _obj(decision_obj.get("action"), "Abaddon action")
        tool, attempts_count = _str(action.get("tool"), "Abaddon tool"), 1
    return tool, _int(data.get("command_count"), f"{side} command_count"), attempts_count


def _production(tool: str) -> bool:
    return tool in {"build_unit", "train_unit"} or tool.startswith(("build_unit_", "train_unit_"))


def _side_metrics() -> dict[str, Any]:
    return {
        "tools": Counter(), "no_command": [], "passive": [], "hostile": [],
        "contact": [], "orders": [], "retried": [], "first_visible": None,
        "first_hostile": None, "first_inflicted": None, "first_received": None,
        "first_growth": None, "first_production": None,
    }


def _ratio(stats: dict[str, int]) -> dict[str, Any]:
    kills, deaths = stats["kills_cost"], stats["deaths_cost"]
    return {
        "kills_cost": kills, "deaths_cost": deaths,
        "value": kills / deaths if deaths else None,
        "infinite": deaths == 0 and kills > 0,
    }


def trade_ratio(stats: dict[str, int]) -> dict[str, Any]:
    """Return a JSON-safe kill-cost/death-cost ratio."""
    return _ratio(stats)


def _summary(
    value: dict[str, Any], header: dict[str, Any], trajectory_sha: str,
    rounds: int, final_tick: int, phase: str, winner: str,
    final: dict[str, dict[str, Any]],
) -> None:
    exact = {
        "run_id": header["run_id"], "curriculum_id": header["curriculum_id"],
        "generation_id": header["generation_id"],
        "runtime_image_id": header["runtime_image_id"],
        "warm_start_sha256": header["warm_start_sha256"],
        "warm_start_handoff": header["warm_start_handoff"],
        "trajectory_sha256": trajectory_sha, "seed": header["seed"],
        "abaddon_doctrine": header["abaddon_doctrine"],
        "rounds_completed": rounds, "ticks_per_round": header["ticks_per_round"],
        "final_tick": final_tick, "winner": winner,
        "apollyon_final": final["apollyon"], "abaddon_final": final["abaddon"],
    }
    for key, expected in exact.items():
        if value.get(key) != expected:
            raise ContractError(f"summary {key} does not match trajectory")
    status = "game_over" if phase == "game_over" else "round_limit"
    outcome = (
        "APOLLYON_WIN" if winner == "Multi0" else
        "ABADDON_WIN" if winner == "Multi1" else "DRAW_OR_UNFINISHED"
    )
    if value.get("status") != status or value.get("outcome") != outcome:
        raise ContractError("summary terminal does not match trajectory")
    _bool(value.get("candidate_only"), "summary.candidate_only", True)
    _bool(value.get("warm_start_rows_training_candidate"), "summary.warm rows", False)
    _bool(value.get("controller_rows_training_candidate"), "summary controller rows", True)
    for key in (
        "automatic_corpus_admission", "automatic_apollyon_weight_mutation",
        "automatic_abaddon_policy_promotion",
    ):
        _bool(value.get(key), f"summary.{key}", False)


