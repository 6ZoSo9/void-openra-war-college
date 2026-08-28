"""Candidate-only force-conversion refinement for Conditional Engagement V2.1."""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

CANDIDATE_SCHEMA = "void.apollyon.conditional-engagement-candidate.v2.1"
DECISION_SCHEMA = "void.apollyon.conditional-engagement-decision.v2.1"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
HOSTILE = {"attack_move", "attack_target"}
PARENT_V2_CANDIDATE_SHA256 = "27f28a6a46f63a055f8f35c021bafae1035084c444ba7e2009161109ec3efdd6"
SEED_2060_PAIR_REPORT_SHA256 = "aeb39e266cd2e9b0850b777caf7225d0a8026f56839de9c05910bca22fced880"
EXPECTED_CANDIDATE_SHA256 = "a0b08f7a7ea807de53416f589790059e2540404f680d6b470395bdbdc067f460"


class PolicyError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _int(value: Any, label: str, minimum: int = 0) -> int:
    _require(type(value) is int and value >= minimum, f"{label} must be integer >= {minimum}")
    return value


def _sha(value: Any, label: str) -> str:
    _require(isinstance(value, str) and SHA256.fullmatch(value) is not None, f"{label} must be lowercase SHA-256")
    return value


def canonical_json_bytes(candidate: Mapping[str, Any]) -> bytes:
    return (json.dumps(candidate, indent=2, sort_keys=True) + "\n").encode("utf-8")


def candidate_sha256(candidate: Mapping[str, Any]) -> str:
    validate_candidate(candidate)
    return hashlib.sha256(canonical_json_bytes(candidate)).hexdigest()


def validate_candidate(candidate: Mapping[str, Any]) -> None:
    candidate = _obj(candidate, "candidate")
    _require(candidate.get("schema") == CANDIDATE_SCHEMA, "candidate schema drift")
    _require(candidate.get("candidate_only") is True, "candidate_only must be true")
    for key in ("automatic_apollyon_weight_mutation", "automatic_abaddon_policy_promotion", "automatic_corpus_admission"):
        _require(candidate.get(key) is False, f"candidate authority drift: {key}")

    source = _obj(candidate.get("source_evidence"), "source_evidence")
    for key in (
        "parent_v2_candidate_sha256",
        "seed_2060_pair_report_sha256",
        "seed_2060_matrix_report_sha256",
        "normalized_warm_start_sha256",
        "baseline_analysis_sha256",
        "v2_analysis_sha256",
    ):
        _sha(source.get(key), key)
    _require(source["parent_v2_candidate_sha256"] == PARENT_V2_CANDIDATE_SHA256, "parent V2 candidate drift")
    _require(source["seed_2060_pair_report_sha256"] == SEED_2060_PAIR_REPORT_SHA256, "seed-2060 pair evidence drift")
    _require(source.get("reviewed_pair_verdict") == "WORSE", "reviewed pair verdict drift")
    _require(source.get("apollyon_net_kill_cost_delta") == -200, "reviewed net-kill delta drift")
    _require(source.get("apollyon_final_combat_delta") == 12, "reviewed force-survival delta drift")
    _require(source.get("protocol_clean") is True, "source pair is not protocol-clean")
    _require(source.get("reviewed_identity_verified") is True, "source reviewed identity not verified")
    _require(source.get("warm_start_semantic_match") is True, "source warm-start semantic match not verified")

    boundaries = _obj(candidate.get("policy_boundaries"), "policy_boundaries")
    expected = {
        "runtime_seed_branching": False,
        "unit_type_specific_rule": False,
        "typed_tool_surface_required": True,
        "current_observation_only": True,
        "bounded_recent_history_only": True,
        "hidden_state_use": False,
        "automatic_tool_filtering": False,
    }
    _require(all(boundaries.get(key) is value for key, value in expected.items()), "policy boundary drift")

    thresholds = _obj(candidate.get("thresholds"), "thresholds")
    for key in (
        "history_window_rounds",
        "minimum_engagement_force",
        "force_conversion_floor",
        "severe_force_drop_units",
        "no_military_progress_rounds",
        "blind_attack_move_streak_rounds",
        "passive_streak_rounds",
    ):
        _int(thresholds.get(key), key, 1)
    _require(thresholds["force_conversion_floor"] >= thresholds["minimum_engagement_force"], "force conversion floor below engagement floor")

    modes = _obj(candidate.get("modes"), "modes")
    precedence = candidate.get("mode_precedence")
    _require(isinstance(precedence, list) and len(precedence) == len(set(precedence)), "mode precedence malformed")
    _require(set(precedence) == set(modes), "mode/precedence drift")
    _require("FORCE_CONVERSION" in modes, "force conversion mode absent")


def snapshot_from_state(state: Mapping[str, Any], *, round_no: int, selected_tool: str | None = None) -> dict[str, Any]:
    state = _obj(state, "state")
    units = state.get("units_summary")
    enemies = state.get("enemy_summary")
    buildings = state.get("enemy_buildings_summary")
    _require(all(isinstance(value, list) for value in (units, enemies, buildings)), "state summary arrays malformed")
    military = _obj(state.get("military"), "state.military")
    combat = sum(1 for unit in units if isinstance(unit, Mapping) and unit.get("can_attack") is True)
    idle = sum(1 for unit in units if isinstance(unit, Mapping) and unit.get("can_attack") is True and unit.get("idle") is True)
    _require(selected_tool is None or isinstance(selected_tool, str), "selected_tool malformed")
    return {
        "round": _int(round_no, "round", 1),
        "combat_units": combat,
        "idle_combat_units": idle,
        "visible_enemies": len(enemies) + len(buildings),
        "kills_cost": _int(military.get("kills_cost", 0), "kills_cost"),
        "deaths_cost": _int(military.get("deaths_cost", 0), "deaths_cost"),
        "selected_tool": selected_tool,
    }


def _snapshot(row: Mapping[str, Any], label: str) -> dict[str, Any]:
    row = _obj(row, label)
    result = {
        key: _int(row.get(key), f"{label}.{key}", 1 if key == "round" else 0)
        for key in ("round", "combat_units", "idle_combat_units", "visible_enemies", "kills_cost", "deaths_cost")
    }
    _require(result["idle_combat_units"] <= result["combat_units"], f"{label} idle force exceeds combat force")
    tool = row.get("selected_tool")
    _require(tool is None or isinstance(tool, str), f"{label} selected_tool malformed")
    result["selected_tool"] = tool
    return result


def _consecutive_blind_attack_moves(window: Sequence[Mapping[str, Any]]) -> int:
    count = 0
    for row in reversed(window):
        if row["selected_tool"] == "attack_move" and row["visible_enemies"] == 0:
            count += 1
        else:
            break
    return count


def select_mode(candidate: Mapping[str, Any], current: Mapping[str, Any], history: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validate_candidate(candidate)
    _require(isinstance(history, Sequence) and not isinstance(history, (str, bytes)), "history must be a sequence")
    current = _snapshot(current, "current")
    rows = [_snapshot(row, f"history[{index}]") for index, row in enumerate(history)]
    points = [*rows, current]
    for earlier, later in zip(points, points[1:]):
        _require(later["round"] > earlier["round"], "history rounds regressed")
        _require(later["kills_cost"] >= earlier["kills_cost"], "kills_cost regressed")
        _require(later["deaths_cost"] >= earlier["deaths_cost"], "deaths_cost regressed")

    t = candidate["thresholds"]
    window = rows[-t["history_window_rounds"]:]
    previous = window[-1] if window else None
    drop = max(0, previous["combat_units"] - current["combat_units"]) if previous else 0
    kills_delta = current["kills_cost"] - previous["kills_cost"] if previous else 0
    deaths_delta = current["deaths_cost"] - previous["deaths_cost"] if previous else 0

    stagnant = 0
    for earlier, later in zip(reversed(points[:-1]), reversed(points[1:])):
        if earlier["kills_cost"] == later["kills_cost"] and earlier["deaths_cost"] == later["deaths_cost"]:
            stagnant += 1
        else:
            break

    passive = 0
    for row in reversed(window):
        if row["selected_tool"] is None or row["selected_tool"] in HOSTILE:
            break
        passive += 1

    recent_hostile = sum(row["selected_tool"] in HOSTILE for row in window if row["selected_tool"] is not None)
    blind_attack_move_streak = _consecutive_blind_attack_moves(window)
    reasons: list[str]

    if current["combat_units"] < t["minimum_engagement_force"]:
        mode, reasons = "REBUILD_FORCE", ["combat_force_below_engagement_floor"]
    elif drop >= t["severe_force_drop_units"] or (deaths_delta > kills_delta and deaths_delta > 0):
        mode, reasons = "ATTRITION_BRAKE", []
        if drop >= t["severe_force_drop_units"]:
            reasons.append("severe_recent_force_drop")
        if deaths_delta > kills_delta and deaths_delta > 0:
            reasons.append("recent_deaths_cost_exceeds_kills_cost")
    elif current["visible_enemies"] > 0 and recent_hostile == 0:
        mode, reasons = "CONTACT_RESPONSE", ["visible_enemy_with_underused_combat_force"]
    elif current["visible_enemies"] > 0:
        mode, reasons = "MEASURED_CONTACT", ["active_visible_contact"]
    elif (
        current["combat_units"] >= t["force_conversion_floor"]
        and stagnant >= t["no_military_progress_rounds"]
        and blind_attack_move_streak >= t["blind_attack_move_streak_rounds"]
    ):
        mode, reasons = "FORCE_CONVERSION", [
            "rebuilt_force_without_contact",
            "repeated_blind_attack_move_without_military_progress",
        ]
    elif (
        current["combat_units"] >= t["minimum_engagement_force"]
        and stagnant >= t["no_military_progress_rounds"]
        and passive >= t["passive_streak_rounds"]
    ):
        mode, reasons = "ENGAGEMENT_DEFICIT", ["usable_force_passive_without_military_progress"]
    else:
        mode, reasons = "BALANCED_SEARCH", ["no_emergency_condition_proven"]

    return {
        "schema": DECISION_SCHEMA,
        "mode": mode,
        "reasons": reasons,
        "evidence": {
            "round": current["round"],
            "history_window_size": len(window),
            "combat_units": current["combat_units"],
            "idle_combat_units": current["idle_combat_units"],
            "visible_enemies": current["visible_enemies"],
            "kills_cost": current["kills_cost"],
            "deaths_cost": current["deaths_cost"],
            "recent_force_drop": drop,
            "recent_kills_cost_delta": kills_delta,
            "recent_deaths_cost_delta": deaths_delta,
            "stagnant_military_intervals": stagnant,
            "passive_streak_rounds": passive,
            "recent_hostile_count": recent_hostile,
            "blind_attack_move_streak": blind_attack_move_streak,
        },
        "instruction": candidate["modes"][mode]["instruction"],
        "candidate_sha256": candidate_sha256(candidate),
        "runtime_seed_branching": False,
    }


def format_coaching(decision: Mapping[str, Any]) -> str:
    decision = _obj(decision, "decision")
    _require(decision.get("schema") == DECISION_SCHEMA, "decision schema drift")
    _require(isinstance(decision.get("reasons"), list) and decision["reasons"], "decision reasons malformed")
    return (
        "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_1\n"
        f"MODE={decision['mode']}\n"
        f"OBSERVED_REASONS={','.join(decision['reasons'])}\n"
        "BOUNDARY=Use exactly one function from CURRENT_ALLOWED_TOOL_NAMES; do not infer hidden state or invent actor IDs.\n"
        f"COACHING={decision['instruction']}"
    )