from __future__ import annotations

import json
from pathlib import Path

import pytest

from openra_env.coaching import (
    ConditionalEngagementSessionV22,
    V22_CANDIDATE_SCHEMA,
    V22_DECISION_SCHEMA,
    V22_EXPECTED_CANDIDATE_SHA256,
    format_coaching_v22,
    v22_candidate_sha256,
    validate_candidate_v22,
)
from openra_env.coaching.conditional_engagement_v2_2 import PolicyError, select_mode, snapshot_from_state

FIXTURE = Path("fixtures/training/conditional_engagement_candidate_v2_2.json")


def candidate() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def state(*, combat: int = 4, visible: int = 0, kills: int = 0, deaths: int = 0) -> dict:
    return {
        "units_summary": [
            {"can_attack": True, "idle": False}
            for _ in range(combat)
        ],
        "enemy_summary": [{} for _ in range(visible)],
        "enemy_buildings_summary": [],
        "military": {"kills_cost": kills, "deaths_cost": deaths},
    }


def history_row(round_no: int, *, tool: str, combat: int = 4, visible: int = 0, kills: int = 0, deaths: int = 0) -> dict:
    row = snapshot_from_state(state(combat=combat, visible=visible, kills=kills, deaths=deaths), round_no=round_no)
    row["selected_tool"] = tool
    return row


def test_exact_candidate_digest_and_source_evidence_are_frozen():
    value = candidate()
    validate_candidate_v22(value)
    assert value["schema"] == V22_CANDIDATE_SCHEMA
    assert v22_candidate_sha256(value) == V22_EXPECTED_CANDIDATE_SHA256
    assert V22_EXPECTED_CANDIDATE_SHA256 == "92f10e87f01a388882f621a09989783d561302cc46583a5344e8108c81d864ab"
    source = value["source_evidence"]
    assert source["seed_2060_pair_report_sha256"] == "4b6941abf758cb5b898dddd2fd1ddf6cbf4276e934614233b33c0d4404d13202"
    assert source["reviewed_pair_verdict"] == "TIE"
    assert source["seed_2060_force_conversion_rounds"] == 64
    assert source["seed_2060_attack_move_fraction"] == 0.9583333333333334


def test_force_conversion_selection_semantics_remain_parent_equivalent():
    value = candidate()
    current = snapshot_from_state(state(), round_no=3)
    history = [
        history_row(1, tool="attack_move"),
        history_row(2, tool="attack_move"),
    ]
    decision = select_mode(value, current, history)
    assert decision["schema"] == V22_DECISION_SCHEMA
    assert decision["mode"] == "FORCE_CONVERSION"
    assert decision["runtime_seed_branching"] is False
    assert decision["evidence"]["blind_attack_move_streak"] == 2


def test_force_conversion_coaching_names_offered_move_units_and_preserves_surface():
    value = candidate()
    decision = select_mode(
        value,
        snapshot_from_state(state(), round_no=3),
        [history_row(1, tool="attack_move"), history_row(2, tool="attack_move")],
    )
    coaching = format_coaching_v22(decision, ["attack_move", "move_units", "build_unit"])
    assert "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_2" in coaching
    assert "MODE=FORCE_CONVERSION" in coaching
    assert "TOOL_SURFACE_UNCHANGED=true" in coaching
    assert "Do not choose attack_move this round" in coaching
    assert "PREFERRED_OFFERED_ALTERNATIVE=move_units" in coaching
    assert 'PREFERRED_MOVE_UNITS_SELECTOR=unit_ids="all_combat"' in coaching
    assert 'SELECTOR_INTEGRITY_RULE=When choosing move_units for FORCE_CONVERSION, use unit_ids="all_combat" exactly' in coaching
    assert "CURRENT_ALLOWED_TOOL_NAMES=attack_move,move_units,build_unit" in coaching


def test_force_conversion_selector_hint_only_exists_when_move_units_is_offered():
    value = candidate()
    decision = select_mode(
        value,
        snapshot_from_state(state(), round_no=3),
        [history_row(1, tool="attack_move"), history_row(2, tool="attack_move")],
    )
    coaching = format_coaching_v22(decision, ["attack_move", "build_unit"])
    assert "PREFERRED_OFFERED_ALTERNATIVE=move_units" not in coaching
    assert "PREFERRED_MOVE_UNITS_SELECTOR" not in coaching
    assert "SELECTOR_INTEGRITY_RULE" not in coaching


def test_non_force_conversion_never_injects_selector_hint():
    value = candidate()
    decision = select_mode(
        value,
        snapshot_from_state(state(visible=1), round_no=3),
        [history_row(1, tool="attack_move"), history_row(2, tool="attack_move")],
    )
    assert decision["mode"] != "FORCE_CONVERSION"
    coaching = format_coaching_v22(decision, ["attack_move", "move_units"])
    assert "PREFERRED_MOVE_UNITS_SELECTOR" not in coaching
    assert "SELECTOR_INTEGRITY_RULE" not in coaching


def test_session_marks_action_compliance_without_filtering_any_tool():
    session = ConditionalEngagementSessionV22(candidate())
    offered = ["attack_move", "move_units", "build_unit"]
    for round_no in (1, 2):
        prepared = session.prepare_round(state(), round_no=round_no, allowed_tool_names=offered)
        assert prepared["current_allowed_tool_names"] == offered
        session.commit_accepted_tool("attack_move")

    prepared = session.prepare_round(state(), round_no=3, allowed_tool_names=offered)
    compliance = prepared["action_compliance"]
    assert prepared["decision"]["mode"] == "FORCE_CONVERSION"
    assert prepared["current_allowed_tool_names"] == offered
    assert compliance["tool_surface_unchanged"] is True
    assert compliance["attack_move_discouraged"] is True
    assert compliance["preferred_offered_alternative"] == "move_units"
    assert compliance["non_attack_move_offered_names"] == ["move_units", "build_unit"]

    # Advisory-only means the host may still accept attack_move; V2.2 must not manufacture a retry.
    receipt = session.commit_accepted_tool("attack_move")
    assert receipt["selected_tool"] == "attack_move"
    assert receipt["function_was_offered"] is True


def test_force_conversion_does_not_claim_alternative_when_none_is_offered():
    session = ConditionalEngagementSessionV22(candidate())
    for round_no in (1, 2):
        session.prepare_round(state(), round_no=round_no, allowed_tool_names=["attack_move"])
        session.commit_accepted_tool("attack_move")
    prepared = session.prepare_round(state(), round_no=3, allowed_tool_names=["attack_move"])
    compliance = prepared["action_compliance"]
    assert prepared["decision"]["mode"] == "FORCE_CONVERSION"
    assert compliance["attack_move_discouraged"] is False
    assert compliance["preferred_offered_alternative"] is None
    assert compliance["non_attack_move_offered_names"] == []


def test_visible_contact_preempts_force_conversion():
    value = candidate()
    decision = select_mode(
        value,
        snapshot_from_state(state(visible=1), round_no=3),
        [history_row(1, tool="attack_move"), history_row(2, tool="attack_move")],
    )
    assert decision["mode"] in {"CONTACT_RESPONSE", "MEASURED_CONTACT"}


def test_acceptance_gate_adds_productive_contact_and_attack_move_reduction():
    gate = candidate()["acceptance_gate"]
    assert gate == {
        "all_trials_protocol_clean": True,
        "productive_contact_rounds_minimum": 1,
        "seed_2060_attack_move_fraction_maximum": 0.75,
        "seed_2060_final_combat_delta_minimum": 0,
        "seed_2060_net_kill_cost_delta_minimum": 0,
    }


def test_candidate_rejects_authority_or_hinting_boundary_drift():
    value = candidate()
    value["policy_boundaries"]["automatic_tool_filtering"] = True
    with pytest.raises(PolicyError, match="policy boundary drift"):
        validate_candidate_v22(value)

    value = candidate()
    value["policy_boundaries"]["offered_tool_hinting_only"] = False
    with pytest.raises(PolicyError, match="policy boundary drift"):
        validate_candidate_v22(value)
