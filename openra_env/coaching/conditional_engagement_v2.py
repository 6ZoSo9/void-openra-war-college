"""Candidate-only conditional engagement coaching for VOID War College."""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

CANDIDATE_SCHEMA = "void.apollyon.conditional-engagement-candidate.v2"
DECISION_SCHEMA = "void.apollyon.conditional-engagement-decision.v2"
AUDIT_SCHEMA = "void.apollyon.tactical-refinement-variance-audit-review.v1"
EXPECTED_CLASSIFICATION = "SEED_CONDITIONAL_AGGRESSION_EFFECT_CONFIRMED"
EXPECTED_RECOMMENDATION = "REWORK_COACHING_BEFORE_ADMISSION"
EXPECTED_NEXT_STEP = "derive_conditional_engagement_candidate_v2"
SHA = re.compile(r"^[0-9a-f]{64}$")
HOSTILE = {"attack_move", "attack_target"}


class PolicyError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _integer(value: Any, label: str, minimum: int = 0) -> int:
    _require(type(value) is int and value >= minimum, f"{label} must be integer >= {minimum}")
    return value


def _digest(value: Any, label: str) -> str:
    _require(isinstance(value, str) and SHA.fullmatch(value) is not None, f"{label} must be lowercase SHA-256")
    return value


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def candidate_sha256(candidate: Mapping[str, Any]) -> str:
    validate_candidate(candidate)
    return hashlib.sha256(canonical_json_bytes(candidate)).hexdigest()


def _summary(review: Mapping[str, Any], seed: str, better: int, worse: int, sign: int) -> Mapping[str, Any]:
    row = _obj(_obj(review.get("by_seed"), "review.by_seed").get(seed), f"review.by_seed.{seed}")
    _require(row.get("all_protocol_clean") is True, f"seed {seed} is not protocol-clean")
    _require(row.get("pair_count") == 3 and row.get("better") == better and row.get("worse") == worse, f"seed {seed} repeat outcome drift")
    median = row.get("median_net_delta")
    _require(type(median) in (int, float) and (median < 0 if sign < 0 else median > 0), f"seed {seed} median condition drift")
    return row


def derive_candidate(review: Mapping[str, Any], *, manifest_sha256: str, review_sha256: str) -> dict[str, Any]:
    review = _obj(review, "review")
    _require(review.get("schema") == AUDIT_SCHEMA, "unexpected audit schema")
    _require(review.get("classification") == EXPECTED_CLASSIFICATION, "audit classification drift")
    _require(review.get("recommendation") == EXPECTED_RECOMMENDATION, "audit recommendation drift")
    _require(review.get("next_step") == EXPECTED_NEXT_STEP, "audit next-step drift")
    _require(review.get("candidate_only") is True, "audit is not candidate-only")
    for key in ("automatic_apollyon_weight_mutation", "automatic_abaddon_policy_promotion", "automatic_corpus_admission"):
        _require(review.get(key) is False, f"audit authority drift: {key}")
    regression = _summary(review, "2051", 1, 2, -1)
    gain = _summary(review, "2055", 3, 0, 1)

    def compact(row: Mapping[str, Any]) -> dict[str, Any]:
        return {key: row[key] for key in (
            "pair_count", "better", "worse", "median_net_delta",
            "baseline_mean_attack_move_fraction", "refined_mean_attack_move_fraction",
        )}

    modes = {
        "REBUILD_FORCE": "Your observed combat force is below the bounded engagement floor. Preserve surviving units, restore a usable force and economy, and use only currently offered functions. Do not spend the last combat unit on activity that has no measured objective.",
        "ATTRITION_BRAKE": "Recent observed pressure is destroying force faster than it creates military progress, or repeated attack-move has saturated without progress. Do not repeat the same route merely to appear aggressive. Regroup, reinforce, preserve damaged units, or focus a currently visible target using only a currently offered function.",
        "CONTACT_RESPONSE": "An enemy is currently visible while usable combat force exists. Prefer a deliberate currently offered tactical movement or targeting function over unrelated production. Concentrate useful force, protect the economy, and avoid blind pursuit beyond observed evidence.",
        "MEASURED_CONTACT": "Contact is active. Maintain pressure only while observed trades, force survival, or positional progress justify it. Use focused targeting, repositioning, reinforcement, or a deliberate pause as the current offered functions and evidence support.",
        "ENGAGEMENT_DEFICIT": "A usable combat force has produced no observed military progress through a bounded passive streak. Reacquire contact with a currently offered scouting or tactical movement function. Do not repeat irrelevant production indefinitely, and do not invent hidden targets.",
        "BALANCED_SEARCH": "No emergency engagement or attrition condition is proven. Balance scouting, reinforcement, economy and positioning from current observations. Aggression is not a quota; choose exactly one currently offered function that advances a measurable objective.",
    }
    candidate = {
        "schema": CANDIDATE_SCHEMA,
        "candidate_only": True,
        "generation_id": review["generation_id"],
        "curriculum_id": review["curriculum_id"],
        "doctrine": review["doctrine"],
        "source_evidence": {
            "variance_manifest_sha256": _digest(manifest_sha256, "manifest_sha256"),
            "variance_review_sha256": _digest(review_sha256, "review_sha256"),
            "source_candidate_sha256": _digest(review.get("source_candidate_sha256"), "source_candidate_sha256"),
            "source_review_sha256": _digest(review.get("source_review_sha256"), "source_review_sha256"),
            "classification": EXPECTED_CLASSIFICATION,
            "recommendation": EXPECTED_RECOMMENDATION,
            "regression_summary": compact(regression),
            "gain_summary": compact(gain),
        },
        "policy_boundaries": {
            "runtime_seed_branching": False,
            "unit_type_specific_rule": False,
            "typed_tool_surface_required": True,
            "current_observation_only": True,
            "bounded_recent_history_only": True,
            "hidden_state_use": False,
        },
        "thresholds": {
            "history_window_rounds": 5,
            "minimum_engagement_force": 2,
            "severe_force_drop_units": 2,
            "attack_move_saturation_numerator": 4,
            "attack_move_saturation_denominator": 5,
            "no_military_progress_rounds": 2,
            "passive_streak_rounds": 2,
        },
        "mode_precedence": list(modes),
        "modes": {name: {"instruction": instruction} for name, instruction in modes.items()},
        "acceptance_gate": {
            "reviewed_regression_seed": {"median_net_delta_minimum": 0, "maximum_worse_pairs_out_of_three": 1},
            "reviewed_gain_seed": {"median_net_delta_strictly_positive": True, "minimum_better_pairs_out_of_three": 2},
            "held_out_seeds": {"maximum_worse_pairs_out_of_three_per_seed": 1, "minimum_seed_count": 3},
            "all_trials_protocol_clean": True,
            "all_accepted_actions_first_attempt": True,
            "invalid_attempt_count": 0,
        },
        "automatic_apollyon_weight_mutation": False,
        "automatic_abaddon_policy_promotion": False,
        "automatic_corpus_admission": False,
    }
    validate_candidate(candidate)
    return candidate


def validate_candidate(candidate: Mapping[str, Any]) -> None:
    candidate = _obj(candidate, "candidate")
    _require(candidate.get("schema") == CANDIDATE_SCHEMA and candidate.get("candidate_only") is True, "candidate identity drift")
    for key in ("automatic_apollyon_weight_mutation", "automatic_abaddon_policy_promotion", "automatic_corpus_admission"):
        _require(candidate.get(key) is False, f"candidate authority drift: {key}")
    source = _obj(candidate.get("source_evidence"), "source_evidence")
    for key in ("variance_manifest_sha256", "variance_review_sha256", "source_candidate_sha256", "source_review_sha256"):
        _digest(source.get(key), key)
    _require(source.get("classification") == EXPECTED_CLASSIFICATION and source.get("recommendation") == EXPECTED_RECOMMENDATION, "source verdict drift")
    boundaries = _obj(candidate.get("policy_boundaries"), "policy_boundaries")
    expected = {"runtime_seed_branching": False, "unit_type_specific_rule": False, "typed_tool_surface_required": True, "current_observation_only": True, "bounded_recent_history_only": True, "hidden_state_use": False}
    _require(all(boundaries.get(key) is value for key, value in expected.items()), "policy boundary drift")
    thresholds = _obj(candidate.get("thresholds"), "thresholds")
    for key in ("history_window_rounds", "minimum_engagement_force", "severe_force_drop_units", "attack_move_saturation_numerator", "attack_move_saturation_denominator", "no_military_progress_rounds", "passive_streak_rounds"):
        _integer(thresholds.get(key), key, 1)
    _require(thresholds["attack_move_saturation_numerator"] <= thresholds["attack_move_saturation_denominator"], "invalid saturation fraction")
    modes = _obj(candidate.get("modes"), "modes")
    precedence = candidate.get("mode_precedence")
    _require(isinstance(precedence, list) and len(precedence) == len(set(precedence)) and set(precedence) == set(modes), "mode/precedence drift")


def snapshot_from_state(state: Mapping[str, Any], *, round_no: int, selected_tool: str | None = None) -> dict[str, Any]:
    state = _obj(state, "state")
    units, enemies, buildings = state.get("units_summary"), state.get("enemy_summary"), state.get("enemy_buildings_summary")
    _require(all(isinstance(value, list) for value in (units, enemies, buildings)), "state summary arrays malformed")
    military = _obj(state.get("military"), "state.military")
    combat = sum(1 for unit in units if isinstance(unit, Mapping) and unit.get("can_attack") is True)
    idle = sum(1 for unit in units if isinstance(unit, Mapping) and unit.get("can_attack") is True and unit.get("idle") is True)
    return {"round": _integer(round_no, "round", 1), "combat_units": combat, "idle_combat_units": idle, "visible_enemies": len(enemies) + len(buildings), "kills_cost": _integer(military.get("kills_cost", 0), "kills_cost"), "deaths_cost": _integer(military.get("deaths_cost", 0), "deaths_cost"), "selected_tool": selected_tool}


def _snapshot(row: Mapping[str, Any], label: str) -> dict[str, Any]:
    row = _obj(row, label)
    result = {key: _integer(row.get(key), f"{label}.{key}", 1 if key == "round" else 0) for key in ("round", "combat_units", "idle_combat_units", "visible_enemies", "kills_cost", "deaths_cost")}
    _require(result["idle_combat_units"] <= result["combat_units"], f"{label} idle force exceeds combat force")
    result["selected_tool"] = row.get("selected_tool")
    _require(result["selected_tool"] is None or isinstance(result["selected_tool"], str), f"{label} tool malformed")
    return result


def select_mode(candidate: Mapping[str, Any], current: Mapping[str, Any], history: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validate_candidate(candidate)
    _require(isinstance(history, Sequence) and not isinstance(history, (str, bytes)), "history must be a sequence")
    current = _snapshot(current, "current")
    rows = [_snapshot(row, f"history[{index}]") for index, row in enumerate(history)]
    points = [*rows, current]
    for earlier, later in zip(points, points[1:]):
        _require(later["round"] > earlier["round"] and later["kills_cost"] >= earlier["kills_cost"] and later["deaths_cost"] >= earlier["deaths_cost"], "history counters or rounds regressed")
    t = candidate["thresholds"]
    window = rows[-t["history_window_rounds"]:]
    previous = window[-1] if window else None
    tools = [row["selected_tool"] for row in window if row["selected_tool"] is not None]
    attacks = sum(tool == "attack_move" for tool in tools)
    hostile = sum(tool in HOSTILE for tool in tools)
    passive = 0
    for row in reversed(window):
        if row["selected_tool"] is None or row["selected_tool"] in HOSTILE:
            break
        passive += 1
    stagnant = 0
    for earlier, later in zip(reversed(points[:-1]), reversed(points[1:])):
        if earlier["kills_cost"] == later["kills_cost"] and earlier["deaths_cost"] == later["deaths_cost"]:
            stagnant += 1
        else:
            break
    drop = max(0, previous["combat_units"] - current["combat_units"]) if previous else 0
    kills_delta = current["kills_cost"] - previous["kills_cost"] if previous else 0
    deaths_delta = current["deaths_cost"] - previous["deaths_cost"] if previous else 0
    saturated = len(tools) >= t["attack_move_saturation_denominator"] and attacks * t["attack_move_saturation_denominator"] >= len(tools) * t["attack_move_saturation_numerator"]
    reasons: list[str] = []
    if current["combat_units"] < t["minimum_engagement_force"]:
        mode, reasons = "REBUILD_FORCE", ["combat_force_below_engagement_floor"]
    elif drop >= t["severe_force_drop_units"] or (deaths_delta > kills_delta and deaths_delta > 0) or (saturated and stagnant >= t["no_military_progress_rounds"]):
        mode = "ATTRITION_BRAKE"
        if drop >= t["severe_force_drop_units"]: reasons.append("severe_recent_force_drop")
        if deaths_delta > kills_delta and deaths_delta > 0: reasons.append("recent_deaths_cost_exceeds_kills_cost")
        if saturated and stagnant >= t["no_military_progress_rounds"]: reasons.append("attack_move_saturation_without_military_progress")
    elif current["visible_enemies"] > 0 and (passive >= 1 or hostile == 0):
        mode, reasons = "CONTACT_RESPONSE", ["visible_enemy_with_underused_combat_force"]
    elif current["visible_enemies"] > 0:
        mode, reasons = "MEASURED_CONTACT", ["active_visible_contact"]
    elif current["combat_units"] >= t["minimum_engagement_force"] and stagnant >= t["no_military_progress_rounds"] and passive >= t["passive_streak_rounds"]:
        mode, reasons = "ENGAGEMENT_DEFICIT", ["usable_force_passive_without_military_progress"]
    else:
        mode, reasons = "BALANCED_SEARCH", ["no_emergency_condition_proven"]
    return {"schema": DECISION_SCHEMA, "mode": mode, "reasons": reasons, "evidence": {"round": current["round"], "history_window_size": len(window), "combat_units": current["combat_units"], "idle_combat_units": current["idle_combat_units"], "visible_enemies": current["visible_enemies"], "kills_cost": current["kills_cost"], "deaths_cost": current["deaths_cost"], "recent_force_drop": drop, "recent_kills_cost_delta": kills_delta, "recent_deaths_cost_delta": deaths_delta, "recent_attack_move_count": attacks, "recent_hostile_count": hostile, "recent_tool_count": len(tools), "passive_streak_rounds": passive, "stagnant_military_intervals": stagnant, "attack_move_saturated": saturated}, "instruction": candidate["modes"][mode]["instruction"], "candidate_sha256": candidate_sha256(candidate), "runtime_seed_branching": False}


def format_coaching(decision: Mapping[str, Any]) -> str:
    decision = _obj(decision, "decision")
    _require(decision.get("schema") == DECISION_SCHEMA and isinstance(decision.get("reasons"), list), "decision identity drift")
    return "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2\nMODE={}\nOBSERVED_REASONS={}\nBOUNDARY=Use exactly one function from CURRENT_ALLOWED_TOOL_NAMES; do not infer hidden state or invent actor IDs.\nCOACHING={}".format(decision["mode"], ",".join(decision["reasons"]), decision["instruction"])
