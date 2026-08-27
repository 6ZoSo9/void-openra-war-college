from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.coaching import ConditionalEngagementSessionV2
from tools.conditional_engagement_v2_duel_wrapper import (
    ConditionalV2Hooks,
    V2_CANDIDATE_SHA256,
    WrapperError,
    parse_wrapper_args,
)


def candidate() -> dict:
    path = (
        Path(__file__).parents[1]
        / "fixtures"
        / "training"
        / "conditional_engagement_candidate_v2.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def state(*, combat=4, visible=0, kills=0, deaths=0) -> dict:
    return {
        "units_summary": [
            {"actor_id": index + 1, "can_attack": True}
            for index in range(combat)
        ],
        "enemy_summary": [
            {"actor_id": 100 + index}
            for index in range(visible)
        ],
        "enemy_buildings_summary": [],
        "military": {
            "kills_cost": kills,
            "deaths_cost": deaths,
        },
    }


class FakeHelper:
    def __init__(self, answer="attack_move"):
        self.answer = answer
        self.users: list[str] = []

    def ollama_tool_call(self, system, user, tools):
        self.users.append(user)
        return self.answer, {}


class FakeLegacy:
    def __init__(self):
        self.rows: list[dict] = []
        self.apollyon_decision_typed = self._decision
        self.append_jsonl = self._append
        self.surface_calls = 0
        self.drift_surface = False

    def apollyon_tools_typed(self, base, current_state, pending):
        self.surface_calls += 1
        names = ["advance", "attack_move"]
        if self.drift_surface and self.surface_calls >= 2:
            names = ["advance"]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "parameters": {"type": "object", "properties": {}},
                },
            }
            for name in names
        ]
        return tools, {"offered_tool_names": names}

    def _decision(self, base, helper, current_state, pending, pb2, doctrine, round_no):
        tools, contract = self.apollyon_tools_typed(base, current_state, pending)
        name, args = helper.ollama_tool_call("system", "BASE_USER_PROMPT", tools)
        if name not in set(contract["offered_tool_names"]):
            raise RuntimeError("fake host rejected tool")
        return (
            name,
            args,
            [],
            [
                {
                    "attempt": 1,
                    "tool": name,
                    "accepted": True,
                    "function_was_offered": True,
                    "world_mutated_before_validation": False,
                }
            ],
            contract,
        )

    def _append(self, path, row):
        self.rows.append(row)


def provenance() -> dict[str, str]:
    return {
        "source_commit": "1" * 40,
        "candidate_sha256": V2_CANDIDATE_SHA256,
        "policy_sha256": "2" * 64,
        "session_sha256": "3" * 64,
    }


def hooks(legacy: FakeLegacy):
    session = ConditionalEngagementSessionV2(candidate())
    return ConditionalV2Hooks(legacy, session, provenance(), "4" * 64), session


def test_wrapper_injects_coaching_and_commits_only_host_accepted_tool() -> None:
    legacy = FakeLegacy()
    wrapper, session = hooks(legacy)
    helper = FakeHelper("attack_move")
    wrapper.install()
    try:
        result = legacy.apollyon_decision_typed(
            SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1
        )
    finally:
        wrapper.restore()

    assert result[0] == "attack_move"
    assert len(helper.users) == 1
    assert "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2" in helper.users[0]
    assert "CURRENT_ALLOWED_TOOL_NAMES" in helper.users[0]
    assert session.history[0]["selected_tool"] == "attack_move"


def test_joint_decision_and_run_header_receive_cryptographic_v2_binding() -> None:
    legacy = FakeLegacy()
    wrapper, _ = hooks(legacy)
    helper = FakeHelper("advance")
    wrapper.install()
    try:
        legacy.append_jsonl(Path("unused"), {"event": "run_header", "run_id": "r"})
        legacy.apollyon_decision_typed(
            SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1
        )
        legacy.append_jsonl(
            Path("unused"),
            {"event": "joint_decision", "run_id": "r", "round": 1},
        )
    finally:
        wrapper.restore()

    header = legacy.rows[0]["conditional_engagement_v2"]
    decision = legacy.rows[1]["conditional_engagement_v2"]
    assert header["candidate_sha256"] == V2_CANDIDATE_SHA256
    assert header["source_commit"] == "1" * 40
    assert header["wrapper_sha256"] == "4" * 64
    assert header["automatic_corpus_admission"] is False
    assert decision["prepared"]["round"] == 1
    assert decision["prepared"]["history_committed"] is False
    assert decision["accepted"]["selected_tool"] == "advance"
    assert decision["accepted"]["function_was_offered"] is True


def test_missing_round_evidence_fails_closed_before_trajectory_write() -> None:
    legacy = FakeLegacy()
    wrapper, _ = hooks(legacy)
    wrapper.install()
    try:
        with pytest.raises(WrapperError, match="missing V2 evidence"):
            legacy.append_jsonl(
                Path("unused"),
                {"event": "joint_decision", "run_id": "r", "round": 1},
            )
    finally:
        wrapper.restore()
    assert legacy.rows == []


def test_tool_surface_drift_aborts_without_committing_session_history() -> None:
    legacy = FakeLegacy()
    legacy.drift_surface = True
    wrapper, session = hooks(legacy)
    helper = FakeHelper("advance")
    wrapper.install()
    try:
        with pytest.raises(WrapperError, match="tool surface changed"):
            legacy.apollyon_decision_typed(
                SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1
            )
    finally:
        wrapper.restore()

    assert session.history == []
    assert session.pending_round == 1


def test_helper_tool_call_is_restored_when_legacy_decision_raises() -> None:
    legacy = FakeLegacy()
    wrapper, session = hooks(legacy)
    helper = FakeHelper("not_offered")
    original = helper.ollama_tool_call
    wrapper.install()
    try:
        with pytest.raises(RuntimeError, match="fake host rejected"):
            legacy.apollyon_decision_typed(
                SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1
            )
    finally:
        wrapper.restore()

    assert helper.ollama_tool_call == original
    assert session.history == []
    assert session.pending_round == 1


def test_restore_returns_legacy_functions_and_wrapper_args_do_not_consume_duel_flags() -> None:
    legacy = FakeLegacy()
    wrapper, _ = hooks(legacy)
    original_decision = legacy.apollyon_decision_typed
    original_append = legacy.append_jsonl
    wrapper.install()
    assert legacy.apollyon_decision_typed != original_decision
    assert legacy.append_jsonl != original_append
    wrapper.restore()
    assert legacy.apollyon_decision_typed == original_decision
    assert legacy.append_jsonl == original_append

    namespace, remaining = parse_wrapper_args(
        [
            "--v2-source-dir",
            "/tmp/reviewed-v2",
            "--seed",
            "2060",
            "--doctrine",
            "RUSHER",
            "--rounds",
            "72",
        ]
    )
    assert namespace.v2_source_dir == "/tmp/reviewed-v2"
    assert remaining == ["--seed", "2060", "--doctrine", "RUSHER", "--rounds", "72"]
