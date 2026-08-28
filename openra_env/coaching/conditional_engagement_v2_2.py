"""Candidate-only action-compliance refinement for Conditional Engagement V2.2."""
from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

from . import conditional_engagement_v2_1 as parent

CANDIDATE_SCHEMA = "void.apollyon.conditional-engagement-candidate.v2.2"
DECISION_SCHEMA = "void.apollyon.conditional-engagement-decision.v2.2"
EXPECTED_CANDIDATE_SHA256 = "92f10e87f01a388882f621a09989783d561302cc46583a5344e8108c81d864ab"
PARENT_V21_CANDIDATE_SHA256 = "a0b08f7a7ea807de53416f589790059e2540404f680d6b470395bdbdc067f460"
SEED_2060_PAIR_REPORT_SHA256 = "4b6941abf758cb5b898dddd2fd1ddf6cbf4276e934614233b33c0d4404d13202"
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class PolicyError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
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
    for key in ("parent_v2_1_candidate_sha256", "seed_2060_pair_report_sha256", "normalized_warm_start_sha256", "baseline_analysis_sha256", "v2_1_analysis_sha256"):
        _sha(source.get(key), key)
    _require(source["parent_v2_1_candidate_sha256"] == PARENT_V21_CANDIDATE_SHA256, "parent V2.1 candidate drift")
    _require(source["seed_2060_pair_report_sha256"] == SEED_2060_PAIR_REPORT_SHA256, "seed-2060 V2.1 pair evidence drift")
    _require(source.get("reviewed_pair_verdict") == "TIE", "reviewed V2.1 pair verdict drift")
    _require(source.get("seed_2060_net_kill_cost_delta") == 0, "reviewed V2.1 net-kill delta drift")
    _require(source.get("seed_2060_final_combat_delta") == 4, "reviewed V2.1 force delta drift")
    _require(source.get("seed_2060_force_conversion_rounds") == 64, "reviewed V2.1 force-conversion count drift")
    _require(source.get("seed_2060_attack_move_fraction") == 0.9583333333333334, "reviewed V2.1 attack-move fraction drift")
    _require(source.get("seed_2060_minimum_gate_pass") is True, "reviewed V2.1 minimum gate did not pass")
    _require(source.get("protocol_clean") is True, "source V2.1 pair is not protocol-clean")
    _require(source.get("reviewed_identity_verified") is True, "source V2.1 reviewed identity not verified")
    _require(source.get("warm_start_semantic_match") is True, "source V2.1 warm-start match not verified")

    boundaries = _obj(candidate.get("policy_boundaries"), "policy_boundaries")
    expected = {
        "runtime_seed_branching": False,
        "unit_type_specific_rule": False,
        "typed_tool_surface_required": True,
        "current_observation_only": True,
        "bounded_recent_history_only": True,
        "hidden_state_use": False,
        "automatic_tool_filtering": False,
        "offered_tool_hinting_only": True,
    }
    _require(all(boundaries.get(key) is value for key, value in expected.items()), "policy boundary drift")

    thresholds = _obj(candidate.get("thresholds"), "thresholds")
    _require(thresholds.get("history_window_rounds") == 6, "V2.2 history window must remain six")
    _require(thresholds.get("force_conversion_floor") == 4, "V2.2 force-conversion floor drift")
    _require(thresholds.get("blind_attack_move_streak_rounds") == 2, "V2.2 blind-attack streak drift")

    modes = _obj(candidate.get("modes"), "modes")
    precedence = candidate.get("mode_precedence")
    _require(isinstance(precedence, list) and len(precedence) == len(set(precedence)), "mode precedence malformed")
    _require(set(precedence) == set(modes), "mode/precedence drift")
    _require("FORCE_CONVERSION" in modes, "force conversion mode absent")

    gate = _obj(candidate.get("acceptance_gate"), "acceptance_gate")
    _require(gate.get("productive_contact_rounds_minimum") == 1, "productive-contact gate drift")
    _require(gate.get("seed_2060_attack_move_fraction_maximum") == 0.75, "attack-move reduction gate drift")
    _require(gate.get("seed_2060_net_kill_cost_delta_minimum") == 0, "net-kill gate drift")
    _require(gate.get("seed_2060_final_combat_delta_minimum") == 0, "force-preservation gate drift")
    _require(gate.get("all_trials_protocol_clean") is True, "protocol-clean gate drift")


def _parent_candidate_view(candidate: Mapping[str, Any]) -> dict[str, Any]:
    """Build the exact V2.1 semantic view used only for unchanged mode selection."""
    validate_candidate(candidate)
    value = copy.deepcopy(dict(candidate))
    value["schema"] = parent.CANDIDATE_SCHEMA
    value["policy_boundaries"].pop("offered_tool_hinting_only", None)
    value["source_evidence"] = {
        "apollyon_final_combat_delta": 12,
        "apollyon_net_kill_cost_delta": -200,
        "baseline_analysis_sha256": "04f30f0c9ef457e19cbaf1acbd5fc2a0805df0d36ba870d6eb3795751434df1a",
        "normalized_warm_start_sha256": "283bf90cc0a2a7c430c3b4179844a8aeb88f510ff0d0079c2643c48bb78fc482",
        "parent_v2_candidate_sha256": parent.PARENT_V2_CANDIDATE_SHA256,
        "protocol_clean": True,
        "reviewed_identity_verified": True,
        "reviewed_pair_verdict": "WORSE",
        "seed_2060_matrix_report_sha256": "b30ea0fe84e5911eb0079c2643c48bb78fc482",
        "seed_2060_pair_report_sha256": parent.SEED_2060_PAIR_REPORT_SHA256,
        "v2_analysis_sha256": "74ad937d7a4ce8886011c50142904c73e25c85d986cd3e49a9ade0d09daf1e22",
        "warm_start_semantic_match": True,
    }
    value["source_evidence"]["seed_2060_matrix_report_sha256"] = "b30ea0fe84e5911eb007fbe7e55f24bb314aadf176c06e608af83076fc4c7591"
    value["modes"]["FORCE_CONVERSION"]["instruction"] = (
        "A rebuilt force is available, but repeated blind attack-move has produced no observed contact or military progress. "
        "Do not repeat the same blind attack-move this round unless new observed evidence justifies it. Use a currently offered "
        "non-hidden-state movement, formation, scouting, or repositioning action to reacquire productive contact while preserving "
        "cohesion; once contact is visible, transition to focused engagement."
    )
    parent.validate_candidate(value)
    return value


def snapshot_from_state(state: Mapping[str, Any], *, round_no: int, selected_tool: str | None = None) -> dict[str, Any]:
    return parent.snapshot_from_state(state, round_no=round_no, selected_tool=selected_tool)


def select_mode(candidate: Mapping[str, Any], current: Mapping[str, Any], history: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validate_candidate(candidate)
    parent_decision = parent.select_mode(_parent_candidate_view(candidate), current, history)
    mode = parent_decision["mode"]
    return {
        **parent_decision,
        "schema": DECISION_SCHEMA,
        "instruction": candidate["modes"][mode]["instruction"],
        "candidate_sha256": candidate_sha256(candidate),
        "runtime_seed_branching": False,
    }


def format_coaching(decision: Mapping[str, Any], allowed_tool_names: Sequence[str]) -> str:
    decision = _obj(decision, "decision")
    _require(decision.get("schema") == DECISION_SCHEMA, "decision schema drift")
    _require(isinstance(decision.get("reasons"), list) and decision["reasons"], "decision reasons malformed")
    _require(isinstance(allowed_tool_names, Sequence) and not isinstance(allowed_tool_names, (str, bytes)), "allowed tools malformed")
    names = tuple(allowed_tool_names)
    _require(bool(names) and all(isinstance(name, str) and name for name in names), "allowed tools must be nonempty text")
    _require(len(names) == len(set(names)), "allowed tools contain duplicates")

    lines = [
        "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_2",
        f"MODE={decision['mode']}",
        f"OBSERVED_REASONS={','.join(decision['reasons'])}",
        "CURRENT_ALLOWED_TOOL_NAMES=" + ",".join(names),
        "BOUNDARY=Use exactly one function from CURRENT_ALLOWED_TOOL_NAMES; do not infer hidden state or invent actor IDs.",
        "TOOL_SURFACE_UNCHANGED=true",
    ]
    if decision["mode"] == "FORCE_CONVERSION":
        alternatives = [name for name in names if name != "attack_move"]
        if alternatives:
            lines.append("FORCE_CONVERSION_ACTION_RULE=Do not choose attack_move this round; choose a currently offered alternative with a deliberate observable objective.")
        if "move_units" in names:
            lines.append("PREFERRED_OFFERED_ALTERNATIVE=move_units")
            lines.append('PREFERRED_MOVE_UNITS_SELECTOR=unit_ids="all_combat"')
            lines.append('SELECTOR_INTEGRITY_RULE=When choosing move_units for FORCE_CONVERSION, use unit_ids="all_combat" exactly; do not enumerate, remember, or invent actor IDs.')
        lines.append("NON_ATTACK_MOVE_OFFERED_NAMES=" + ",".join(alternatives))
    lines.append(f"COACHING={decision['instruction']}")
    return "\n".join(lines)
