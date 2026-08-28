from __future__ import annotations

from pathlib import Path

from openra_env.learning.general_brain_runtime import BRAIN_RUN_SCHEMA, tactical_overlay
from tools.conditional_engagement_v2_2_g1_duel_wrapper import GeneralBrainOverlayHooks


ADAPTER_SHA = "a" * 64
MANIFEST_SHA = "b" * 64


def binding():
    return {
        "schema": BRAIN_RUN_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "adapter_sha256": ADAPTER_SHA,
        "challenger_manifest_sha256": MANIFEST_SHA,
        "adapter": {
            "weights": {"FORCE_CONVERSION": {"move_units": 4.5}},
        },
    }


def test_unlearned_mode_is_prompt_silent():
    overlay = tactical_overlay(
        binding(),
        mode="BALANCED_SEARCH",
        offered_tool_names=["attack_move", "move_units", "train_unit_e1"],
    )
    assert overlay["preferred_tool"] is None
    assert overlay["preference_applied"] is False
    assert overlay["prompt_injected"] is False
    assert overlay["coaching"] == ""
    assert overlay["offered_weights"] == {}


def test_learned_mode_injects_only_positive_reviewed_preference():
    overlay = tactical_overlay(
        binding(),
        mode="FORCE_CONVERSION",
        offered_tool_names=["attack_move", "move_units", "train_unit_e1"],
    )
    assert overlay["preferred_tool"] == "move_units"
    assert overlay["preferred_arguments"] == {"unit_ids": "all_combat"}
    assert overlay["preference_applied"] is True
    assert overlay["prompt_injected"] is True
    assert "GENERAL_BRAIN_COMPETENCE_ADAPTER_V1" in overlay["coaching"]
    assert "LEARNED_PREFERRED_TOOL=move_units" in overlay["coaching"]


class FakeHelper:
    def __init__(self):
        self.users = []

    def ollama_tool_call(self, system, user, tools):
        self.users.append(user)
        return {"ok": True}


class FakeSession:
    def __init__(self, mode: str):
        self.mode = mode

    def prepare_round(self, state, *, round_no, allowed_tool_names):
        return {"decision": {"mode": self.mode}}

    def commit_accepted_tool(self, selected_tool):
        return {"mode": self.mode, "selected_tool": selected_tool}


class FakeLegacy:
    def __init__(self):
        self.rows = []
        self.apollyon_decision_typed = self._decision
        self.append_jsonl = self._append

    def apollyon_tools_typed(self, base, state, pending):
        return None, {"offered_tool_names": ["attack_move", "move_units"]}

    def _decision(self, base, helper, state, pending, pb2, doctrine, round_no):
        helper.ollama_tool_call("system", "BASE_USER_EXACT", [])
        return (
            "attack_move",
            {},
            [],
            [
                {
                    "tool": "attack_move",
                    "accepted": True,
                    "world_mutated_before_validation": False,
                }
            ],
            {"offered_tool_names": ["attack_move", "move_units"]},
        )

    def _append(self, path: Path, row):
        self.rows.append(row)


def test_hook_does_not_wrap_tool_call_when_mode_has_no_learned_weight():
    legacy = FakeLegacy()
    helper = FakeHelper()
    hooks = GeneralBrainOverlayHooks(legacy, FakeSession("BALANCED_SEARCH"), binding())
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            None, helper, {}, None, None, "RUSHER", 1
        )
    finally:
        hooks.restore()

    assert result[0] == "attack_move"
    assert helper.users == ["BASE_USER_EXACT"]
    evidence = hooks._round_evidence[1]
    assert evidence["preference_applied"] is False
    assert evidence["prompt_injected"] is False
    assert evidence["preferred_tool"] is None


def test_hook_wraps_tool_call_when_reviewed_weight_applies():
    legacy = FakeLegacy()
    helper = FakeHelper()
    hooks = GeneralBrainOverlayHooks(legacy, FakeSession("FORCE_CONVERSION"), binding())
    hooks.install()
    try:
        legacy.apollyon_decision_typed(None, helper, {}, None, None, "RUSHER", 1)
    finally:
        hooks.restore()

    assert len(helper.users) == 1
    assert helper.users[0].startswith("BASE_USER_EXACT\nGENERAL_BRAIN_COMPETENCE_ADAPTER_V1")
    evidence = hooks._round_evidence[1]
    assert evidence["preference_applied"] is True
    assert evidence["prompt_injected"] is True
