from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from openra_env.coaching import (
    COMMIT_SCHEMA,
    PREPARED_SCHEMA,
    ConditionalEngagementSessionV2,
    SessionError,
)


def load_candidate() -> dict:
    path = (
        Path(__file__).parents[1]
        / "fixtures"
        / "training"
        / "conditional_engagement_candidate_v2.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def state(
    *,
    combat: int = 4,
    idle: int = 0,
    visible: int = 0,
    kills: int = 0,
    deaths: int = 0,
    seed: int | None = None,
) -> dict:
    units = [
        {
            "actor_id": index + 1,
            "can_attack": True,
            "idle": index < idle,
        }
        for index in range(combat)
    ]
    result = {
        "units_summary": units,
        "enemy_summary": [{"actor_id": 100 + index} for index in range(visible)],
        "enemy_buildings_summary": [],
        "military": {
            "kills_cost": kills,
            "deaths_cost": deaths,
        },
    }
    if seed is not None:
        result["seed"] = seed
    return result


def test_prepare_is_noncommitting_and_commit_records_only_offered_tool() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())
    prepared = session.prepare_round(
        state(),
        round_no=1,
        allowed_tool_names=["advance", "attack_move"],
    )

    assert prepared["schema"] == PREPARED_SCHEMA
    assert prepared["decision"]["mode"] == "BALANCED_SEARCH"
    assert prepared["history_committed"] is False
    assert "MODE=BALANCED_SEARCH" in prepared["coaching"]
    assert session.history == []
    assert session.pending_round == 1

    receipt = session.commit_accepted_tool("advance")
    assert receipt["schema"] == COMMIT_SCHEMA
    assert receipt["selected_tool"] == "advance"
    assert receipt["function_was_offered"] is True
    assert session.pending_round is None
    assert session.history == [
        {
            "round": 1,
            "combat_units": 4,
            "idle_combat_units": 0,
            "visible_enemies": 0,
            "kills_cost": 0,
            "deaths_cost": 0,
            "selected_tool": "advance",
        }
    ]


def test_unoffered_rejected_tool_cannot_contaminate_history() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())
    session.prepare_round(state(), round_no=1, allowed_tool_names=["advance"])

    with pytest.raises(SessionError, match="not offered"):
        session.commit_accepted_tool("attack_move")

    assert session.history == []
    assert session.pending_round == 1
    session.commit_accepted_tool("advance")
    assert session.history[0]["selected_tool"] == "advance"


def test_round_sequence_and_single_pending_decision_are_fail_closed() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())

    with pytest.raises(SessionError, match="expected round 1"):
        session.prepare_round(state(), round_no=2, allowed_tool_names=["advance"])

    session.prepare_round(state(), round_no=1, allowed_tool_names=["advance"])
    with pytest.raises(SessionError, match="still pending"):
        session.prepare_round(state(), round_no=1, allowed_tool_names=["advance"])

    session.commit_accepted_tool("advance")
    with pytest.raises(SessionError, match="expected round 2"):
        session.prepare_round(state(), round_no=3, allowed_tool_names=["advance"])


def test_candidate_is_frozen_against_external_mutation() -> None:
    candidate = load_candidate()
    session = ConditionalEngagementSessionV2(candidate)
    expected_sha = session.candidate_sha256

    candidate["thresholds"]["minimum_engagement_force"] = 999
    candidate["automatic_corpus_admission"] = True

    prepared = session.prepare_round(
        state(combat=4),
        round_no=1,
        allowed_tool_names=["advance"],
    )
    assert prepared["candidate_sha256"] == expected_sha
    assert prepared["decision"]["mode"] == "BALANCED_SEARCH"


def test_bounded_passive_history_reaches_engagement_deficit() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())

    first = session.prepare_round(state(), round_no=1, allowed_tool_names=["advance"])
    assert first["decision"]["mode"] == "BALANCED_SEARCH"
    session.commit_accepted_tool("advance")

    second = session.prepare_round(state(), round_no=2, allowed_tool_names=["advance"])
    assert second["decision"]["mode"] == "BALANCED_SEARCH"
    session.commit_accepted_tool("advance")

    third = session.prepare_round(state(), round_no=3, allowed_tool_names=["advance"])
    assert third["decision"]["mode"] == "ENGAGEMENT_DEFICIT"


def test_observed_attrition_triggers_brake_after_accepted_attack() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())
    session.prepare_round(
        state(combat=4),
        round_no=1,
        allowed_tool_names=["attack_move", "advance"],
    )
    session.commit_accepted_tool("attack_move")

    prepared = session.prepare_round(
        state(combat=2, visible=2, kills=100, deaths=300),
        round_no=2,
        allowed_tool_names=["attack_move", "attack_target", "advance"],
    )
    assert prepared["decision"]["mode"] == "ATTRITION_BRAKE"
    assert "severe_recent_force_drop" in prepared["decision"]["reasons"]


def test_visible_contact_moves_from_response_to_measured_contact() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())
    first = session.prepare_round(
        state(visible=2),
        round_no=1,
        allowed_tool_names=["attack_target", "advance"],
    )
    assert first["decision"]["mode"] == "CONTACT_RESPONSE"
    session.commit_accepted_tool("attack_target")

    second = session.prepare_round(
        state(visible=2, kills=200),
        round_no=2,
        allowed_tool_names=["attack_target", "attack_move", "advance"],
    )
    assert second["decision"]["mode"] == "MEASURED_CONTACT"


def test_history_is_bounded_to_candidate_window() -> None:
    session = ConditionalEngagementSessionV2(load_candidate())
    for round_no in range(1, 8):
        session.prepare_round(
            state(),
            round_no=round_no,
            allowed_tool_names=["advance"],
        )
        session.commit_accepted_tool("advance")

    history = session.history
    assert len(history) == 5
    assert [row["round"] for row in history] == [3, 4, 5, 6, 7]


def test_runtime_seed_metadata_is_not_part_of_session_decision() -> None:
    left = ConditionalEngagementSessionV2(load_candidate())
    right = ConditionalEngagementSessionV2(load_candidate())

    a = left.prepare_round(
        state(seed=2051),
        round_no=1,
        allowed_tool_names=["advance", "attack_move"],
    )
    b = right.prepare_round(
        state(seed=9999),
        round_no=1,
        allowed_tool_names=["advance", "attack_move"],
    )

    assert a["decision"] == b["decision"]
    assert a["coaching"] == b["coaching"]
