from __future__ import annotations

import json
from pathlib import Path

import pytest

from openra_env.coaching.conditional_engagement_v2_1 import (
    EXPECTED_CANDIDATE_SHA256,
    PolicyError,
    candidate_sha256,
    format_coaching,
    select_mode,
    snapshot_from_state,
    validate_candidate,
)
from openra_env.coaching.conditional_engagement_session_v2_1 import (
    ConditionalEngagementSessionV21,
    SessionError,
)

FIXTURE = Path(__file__).parents[1] / "fixtures/training/conditional_engagement_candidate_v2_1.json"


def candidate():
    return json.loads(FIXTURE.read_text())


def snap(round_no, combat, *, visible=0, kills=0, deaths=0, tool=None):
    return {
        "round": round_no,
        "combat_units": combat,
        "idle_combat_units": 0,
        "visible_enemies": visible,
        "kills_cost": kills,
        "deaths_cost": deaths,
        "selected_tool": tool,
    }


def state(combat=4, *, visible=0, kills=0, deaths=0):
    return {
        "units_summary": [{"actor_id": i + 1, "can_attack": True} for i in range(combat)],
        "enemy_summary": [{"actor_id": 100 + i} for i in range(visible)],
        "enemy_buildings_summary": [],
        "military": {"kills_cost": kills, "deaths_cost": deaths},
    }


def test_candidate_exact_identity_and_authority():
    c = candidate()
    validate_candidate(c)
    assert candidate_sha256(c) == EXPECTED_CANDIDATE_SHA256 == "a0b08f7a7ea807de53416f589790059e2540404f680d6b470395bdbdc067f460"
    assert c["policy_boundaries"]["runtime_seed_branching"] is False
    assert c["policy_boundaries"]["unit_type_specific_rule"] is False
    assert c["automatic_corpus_admission"] is False


def test_source_evidence_binds_worse_primary_metric_and_force_gain():
    src = candidate()["source_evidence"]
    assert src["reviewed_pair_verdict"] == "WORSE"
    assert src["apollyon_net_kill_cost_delta"] == -200
    assert src["apollyon_final_combat_delta"] == 12
    assert src["protocol_clean"] is True
    assert src["warm_start_semantic_match"] is True


def test_rebuild_force_keeps_highest_precedence():
    d = select_mode(candidate(), snap(3, 1), [snap(1, 4, tool="attack_move"), snap(2, 1, tool="attack_move")])
    assert d["mode"] == "REBUILD_FORCE"


def test_attrition_brake_beats_force_conversion():
    history = [snap(1, 6, tool="attack_move"), snap(2, 6, tool="attack_move")]
    d = select_mode(candidate(), snap(3, 4, deaths=200), history)
    assert d["mode"] == "ATTRITION_BRAKE"


def test_force_conversion_fires_on_rebuilt_force_repeating_blind_attack_move_without_progress():
    history = [snap(1, 4, tool="attack_move"), snap(2, 5, tool="attack_move")]
    d = select_mode(candidate(), snap(3, 6), history)
    assert d["mode"] == "FORCE_CONVERSION"
    assert "repeated_blind_attack_move_without_military_progress" in d["reasons"]
    assert d["evidence"]["blind_attack_move_streak"] == 2


def test_force_conversion_requires_force_floor():
    history = [snap(1, 2, tool="attack_move"), snap(2, 3, tool="attack_move")]
    d = select_mode(candidate(), snap(3, 3), history)
    assert d["mode"] != "FORCE_CONVERSION"


def test_visible_contact_preempts_force_conversion():
    history = [snap(1, 5, tool="attack_move"), snap(2, 5, tool="attack_move")]
    d = select_mode(candidate(), snap(3, 5, visible=1), history)
    assert d["mode"] == "MEASURED_CONTACT"


def test_new_military_progress_cancels_force_conversion():
    history = [snap(1, 5, kills=0, tool="attack_move"), snap(2, 5, kills=0, tool="attack_move")]
    d = select_mode(candidate(), snap(3, 5, kills=100), history)
    assert d["mode"] != "FORCE_CONVERSION"


def test_one_blind_attack_move_is_not_enough():
    history = [snap(1, 5, tool="advance"), snap(2, 5, tool="attack_move")]
    d = select_mode(candidate(), snap(3, 5), history)
    assert d["mode"] != "FORCE_CONVERSION"


def test_passive_force_uses_engagement_deficit():
    history = [snap(1, 4, tool="train_unit_e1"), snap(2, 5, tool="build_structure_powr")]
    d = select_mode(candidate(), snap(3, 5), history)
    assert d["mode"] == "ENGAGEMENT_DEFICIT"


def test_default_is_balanced_search():
    d = select_mode(candidate(), snap(1, 4), [])
    assert d["mode"] == "BALANCED_SEARCH"


def test_history_regression_fails_closed():
    with pytest.raises(PolicyError, match="kills_cost regressed"):
        select_mode(candidate(), snap(3, 4, kills=50), [snap(1, 4, kills=100), snap(2, 4, kills=100)])


def test_snapshot_uses_capability_not_unit_type():
    s = snapshot_from_state(
        {
            "units_summary": [{"actor_id": 1, "can_attack": True}, {"actor_id": 2, "can_attack": False}],
            "enemy_summary": [],
            "enemy_buildings_summary": [],
            "military": {"kills_cost": 0, "deaths_cost": 0},
        },
        round_no=1,
    )
    assert s["combat_units"] == 1


def test_coaching_names_force_conversion_and_preserves_boundary():
    d = select_mode(candidate(), snap(3, 6), [snap(1, 4, tool="attack_move"), snap(2, 5, tool="attack_move")])
    text = format_coaching(d)
    assert "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_1" in text
    assert "MODE=FORCE_CONVERSION" in text
    assert "CURRENT_ALLOWED_TOOL_NAMES" in text
    assert "do not infer hidden state" in text


def test_session_commits_only_offered_tool():
    s = ConditionalEngagementSessionV21(candidate())
    prepared = s.prepare_round(state(4), round_no=1, allowed_tool_names=["advance", "attack_move"])
    assert prepared["history_committed"] is False
    with pytest.raises(SessionError, match="not offered"):
        s.commit_accepted_tool("move_units")
    receipt = s.commit_accepted_tool("advance")
    assert receipt["selected_tool"] == "advance"
    assert s.history[0]["selected_tool"] == "advance"


def test_session_rejected_attempt_does_not_commit_history():
    s = ConditionalEngagementSessionV21(candidate())
    s.prepare_round(state(4), round_no=1, allowed_tool_names=["advance"])
    assert s.history == []
    assert s.pending_round == 1


def test_candidate_mutation_after_session_creation_does_not_change_session():
    c = candidate()
    s = ConditionalEngagementSessionV21(c)
    original = s.candidate_sha256
    c["thresholds"]["force_conversion_floor"] = 99
    assert s.candidate_sha256 == original
