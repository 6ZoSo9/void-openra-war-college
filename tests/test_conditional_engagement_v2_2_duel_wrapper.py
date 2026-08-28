from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.coaching import ConditionalEngagementSessionV22
from tools import conditional_engagement_v2_2_duel_wrapper as wrapper_module
from tools.conditional_engagement_v2_2_duel_wrapper import (
    ConditionalV22Hooks,
    TRAJECTORY_KEY,
    V22_CANDIDATE_SHA256,
    WrapperError,
    parse_wrapper_args,
)


def candidate() -> dict:
    path = Path(__file__).parents[1] / "fixtures/training/conditional_engagement_candidate_v2_2.json"
    return json.loads(path.read_text(encoding="utf-8"))


def state(*, combat=4, visible=0, kills=0, deaths=0) -> dict:
    return {
        "units_summary": [{"actor_id": index + 1, "can_attack": True} for index in range(combat)],
        "enemy_summary": [{"actor_id": 100 + index} for index in range(visible)],
        "enemy_buildings_summary": [],
        "military": {"kills_cost": kills, "deaths_cost": deaths},
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
        names = ["advance", "attack_move", "move_units"]
        if self.drift_surface and self.surface_calls >= 2:
            names = ["advance", "move_units"]
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
            [{
                "attempt": 1,
                "tool": name,
                "accepted": True,
                "function_was_offered": True,
                "world_mutated_before_validation": False,
            }],
            contract,
        )

    def _append(self, path, row):
        self.rows.append(row)


def provenance() -> dict[str, str]:
    return {
        "source_commit": "1" * 40,
        "candidate_sha256": V22_CANDIDATE_SHA256,
        "policy_sha256": "2" * 64,
        "session_sha256": "3" * 64,
        "parent_v2_1_policy_sha256": "4" * 64,
    }


def hooks(legacy: FakeLegacy):
    session = ConditionalEngagementSessionV22(candidate())
    return ConditionalV22Hooks(legacy, session, provenance(), "5" * 64), session


def test_wrapper_injects_v22_coaching_and_commits_only_host_accepted_tool():
    legacy = FakeLegacy()
    wrapper, session = hooks(legacy)
    helper = FakeHelper("move_units")
    wrapper.install()
    try:
        result = legacy.apollyon_decision_typed(
            SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1
        )
    finally:
        wrapper.restore()
    assert result[0] == "move_units"
    assert "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_2" in helper.users[0]
    assert "CURRENT_ALLOWED_TOOL_NAMES=" in helper.users[0]
    assert "TOOL_SURFACE_UNCHANGED=true" in helper.users[0]
    assert session.history[0]["selected_tool"] == "move_units"


def test_force_conversion_prompt_prefers_offered_move_units_without_filtering_surface():
    legacy = FakeLegacy()
    wrapper, session = hooks(legacy)
    wrapper.install()
    try:
        for round_no in (1, 2):
            helper = FakeHelper("attack_move")
            legacy.apollyon_decision_typed(SimpleNamespace(), helper, state(), {}, object(), "RUSHER", round_no)
        helper = FakeHelper("move_units")
        result = legacy.apollyon_decision_typed(SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 3)
    finally:
        wrapper.restore()
    assert result[0] == "move_units"
    assert "MODE=FORCE_CONVERSION" in helper.users[0]
    assert "Do not choose attack_move this round" in helper.users[0]
    assert "PREFERRED_OFFERED_ALTERNATIVE=move_units" in helper.users[0]
    assert "CURRENT_ALLOWED_TOOL_NAMES=advance,attack_move,move_units" in helper.users[0]
    assert session.history[-1]["selected_tool"] == "move_units"


def test_advisory_only_force_conversion_may_still_commit_offered_attack_move():
    legacy = FakeLegacy()
    wrapper, session = hooks(legacy)
    wrapper.install()
    try:
        for round_no in (1, 2, 3):
            helper = FakeHelper("attack_move")
            legacy.apollyon_decision_typed(SimpleNamespace(), helper, state(), {}, object(), "RUSHER", round_no)
    finally:
        wrapper.restore()
    assert session.history[-1]["selected_tool"] == "attack_move"
    assert "Do not choose attack_move this round" in helper.users[0]


def test_run_header_and_joint_decision_use_distinct_v22_namespace_and_compliance_receipt():
    legacy = FakeLegacy()
    wrapper, _ = hooks(legacy)
    helper = FakeHelper("advance")
    wrapper.install()
    try:
        legacy.append_jsonl(Path("unused"), {"event": "run_header", "run_id": "r"})
        legacy.apollyon_decision_typed(SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1)
        legacy.append_jsonl(Path("unused"), {"event": "joint_decision", "round": 1})
    finally:
        wrapper.restore()
    assert "conditional_engagement_v2" not in legacy.rows[0]
    assert "conditional_engagement_v2_1" not in legacy.rows[0]
    header = legacy.rows[0][TRAJECTORY_KEY]
    evidence = legacy.rows[1][TRAJECTORY_KEY]
    assert header["schema"].endswith("v2.2")
    assert header["candidate_sha256"] == V22_CANDIDATE_SHA256
    assert header["parent_v2_1_candidate_sha256"].startswith("a0b08f7a")
    assert evidence["prepared"]["action_compliance"]["tool_surface_unchanged"] is True
    assert evidence["accepted"]["selected_tool"] == "advance"


def test_missing_round_evidence_holds_before_write():
    legacy = FakeLegacy()
    wrapper, _ = hooks(legacy)
    wrapper.install()
    try:
        with pytest.raises(WrapperError, match="missing V2.2 evidence"):
            legacy.append_jsonl(Path("unused"), {"event": "joint_decision", "round": 1})
    finally:
        wrapper.restore()
    assert legacy.rows == []


def test_tool_surface_drift_holds_without_history_commit():
    legacy = FakeLegacy()
    legacy.drift_surface = True
    wrapper, session = hooks(legacy)
    helper = FakeHelper("advance")
    wrapper.install()
    try:
        with pytest.raises(WrapperError, match="tool surface changed"):
            legacy.apollyon_decision_typed(SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1)
    finally:
        wrapper.restore()
    assert session.history == []
    assert session.pending_round == 1


def test_model_rejection_does_not_commit_history_and_tool_call_restores():
    legacy = FakeLegacy()
    wrapper, session = hooks(legacy)
    helper = FakeHelper("not_offered")
    original = helper.ollama_tool_call
    wrapper.install()
    try:
        with pytest.raises(RuntimeError, match="fake host rejected"):
            legacy.apollyon_decision_typed(SimpleNamespace(), helper, state(), {}, object(), "RUSHER", 1)
    finally:
        wrapper.restore()
    assert helper.ollama_tool_call == original
    assert session.history == []
    assert session.pending_round == 1


def test_restore_arg_partition_and_unique_terminal_hold(monkeypatch, capsys):
    legacy = FakeLegacy()
    wrapper, _ = hooks(legacy)
    original_decision = legacy.apollyon_decision_typed
    original_append = legacy.append_jsonl
    wrapper.install()
    wrapper.restore()
    assert legacy.apollyon_decision_typed == original_decision
    assert legacy.append_jsonl == original_append

    namespace, remaining = parse_wrapper_args([
        "--v2-2-source-dir", "/tmp/v22", "--seed", "2060", "--rounds", "72"
    ])
    assert namespace.v2_2_source_dir == "/tmp/v22"
    assert remaining == ["--seed", "2060", "--rounds", "72"]

    def fail(_argv=None):
        raise WrapperError("fixture contract drift")

    monkeypatch.setattr(wrapper_module, "main", fail)
    assert wrapper_module.cli([]) == 2
    captured = capsys.readouterr()
    assert "VOID_CONDITIONAL_ENGAGEMENT_V2_2_WRAPPER_HOLD" in captured.err
    assert "blocker=fixture contract drift" in captured.err
