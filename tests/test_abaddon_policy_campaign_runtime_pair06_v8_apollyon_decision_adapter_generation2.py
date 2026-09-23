from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_apollyon_decision_adapter_generation2
    as adapter,
)


class Legacy:
    def __init__(self):
        self.apollyon_decision_typed = self.original
        self.validation_calls = []

    def original(self, *args, **kwargs):
        raise AssertionError("original decision path must be replaced")

    @staticmethod
    def apollyon_tools_typed(base, state, pending):
        return (
            [
                {"type": "function", "function": {"name": "advance"}},
                {"type": "function", "function": {"name": "train_unit_e1"}},
            ],
            {
                "offered_tool_names": ["advance", "train_unit_e1"],
                "production_functions": {
                    "train_unit_e1": {
                        "kind": "build_unit",
                        "unit_type": "e1",
                    }
                },
                "legal_units": ["e1"],
                "legal_buildings": [],
            },
        )

    def decision_to_commands_typed(
        self, base, name, args, state, pending, pb2, contract
    ):
        self.validation_calls.append((name, dict(args), state, contract))
        if name == "advance":
            return True, "shared_clock_noop", []
        if name == "train_unit_e1" and args == {"count": 2}:
            return True, "build_unit", ["TRAIN_E1", "TRAIN_E1"]
        return False, "host_rejected", []


BASE = SimpleNamespace(compact_state=lambda state: {"tick": state["tick"]})
STATE = {"tick": 50}
PENDING = {}
PB2 = object()


def test_contract_binds_exact_observed_legacy_boundary_and_stays_inert():
    out = adapter.pair06_v8_apollyon_decision_adapter_contract()
    assert out["pair06_v8_apollyon_decision_adapter_implemented"] is True
    assert out["pair06_v8_apollyon_decision_adapter_reviewed"] is False
    assert out["legacy_hook_symbol"] == "apollyon_decision_typed"
    assert out["legacy_typed_tool_builder_symbol"] == "apollyon_tools_typed"
    assert out["legacy_host_validator_symbol"] == "decision_to_commands_typed"
    assert out["legacy_ollama_tool_call_used"] is False
    assert out["max_attempts"] == 6
    assert out["host_validation_unchanged"] is True
    assert out["world_mutation_before_host_validation"] is False
    assert out["game_execution_authorized"] is False


def test_install_routes_v8_action_through_unchanged_host_validator():
    legacy = Legacy()
    calls = []

    def decider(**kwargs):
        calls.append(kwargs)
        return {
            "host_mutation_performed": False,
            "campaign_action": {
                "tool": "train_unit_e1",
                "arguments": {"count": 2},
            },
        }

    hooks = adapter.Pair06V8ApollyonDecisionHooks(legacy, decider)
    original = legacy.apollyon_decision_typed
    hooks.install()
    try:
        name, args, commands, attempts, contract = legacy.apollyon_decision_typed(
            BASE, object(), STATE, PENDING, PB2, "RUSHER", 1
        )
    finally:
        hooks.restore()

    assert legacy.apollyon_decision_typed == original
    assert name == "train_unit_e1"
    assert args == {"count": 2}
    assert commands == ["TRAIN_E1", "TRAIN_E1"]
    assert len(attempts) == 1
    assert attempts[0]["accepted"] is True
    assert attempts[0]["world_mutated_before_validation"] is False
    assert contract["offered_tool_names"] == ["advance", "train_unit_e1"]
    assert calls[0]["state"] == {"tick": 50}
    assert calls[0]["feedback"] == ""
    assert len(legacy.validation_calls) == 1


def test_host_rejection_feedback_retries_against_unchanged_state():
    legacy = Legacy()
    seen = []

    def decider(**kwargs):
        seen.append((dict(kwargs["state"]), kwargs["feedback"]))
        if len(seen) == 1:
            return {
                "host_mutation_performed": False,
                "campaign_action": {
                    "tool": "train_unit_e1",
                    "arguments": {"count": 3},
                },
            }
        return {
            "host_mutation_performed": False,
            "campaign_action": {"tool": "advance", "arguments": {}},
        }

    hooks = adapter.Pair06V8ApollyonDecisionHooks(legacy, decider)
    hooks.install()
    try:
        name, args, commands, attempts, _ = legacy.apollyon_decision_typed(
            BASE, object(), STATE, PENDING, PB2, "RUSHER", 7
        )
    finally:
        hooks.restore()

    assert name == "advance"
    assert args == {}
    assert commands == []
    assert len(attempts) == 2
    assert attempts[0]["accepted"] is False
    assert attempts[1]["accepted"] is True
    assert seen == [
        ({"tick": 50}, ""),
        ({"tick": 50}, "host_rejected"),
    ]
    assert hooks.rejected_attempts == 1


def test_unoffered_action_is_rejected_before_host_validation():
    legacy = Legacy()
    calls = {"n": 0}

    def decider(**kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return {
                "host_mutation_performed": False,
                "campaign_action": {"tool": "ghost_tool", "arguments": {}},
            }
        return {
            "host_mutation_performed": False,
            "campaign_action": {"tool": "advance", "arguments": {}},
        }

    hooks = adapter.Pair06V8ApollyonDecisionHooks(legacy, decider)
    hooks.install()
    try:
        _, _, _, attempts, _ = legacy.apollyon_decision_typed(
            BASE, object(), STATE, PENDING, PB2, "TURTLE", 2
        )
    finally:
        hooks.restore()

    assert attempts[0]["host_reason"] == "function_not_offered:ghost_tool"
    assert len(legacy.validation_calls) == 1


def test_six_rejections_fail_closed_without_fallback_advance():
    legacy = Legacy()

    def decider(**kwargs):
        return {
            "host_mutation_performed": False,
            "campaign_action": {
                "tool": "train_unit_e1",
                "arguments": {"count": 3},
            },
        }

    hooks = adapter.Pair06V8ApollyonDecisionHooks(legacy, decider)
    hooks.install()
    try:
        with pytest.raises(
            adapter.Pair06V8ApollyonDecisionAdapterHold,
            match="after 6 attempts",
        ):
            legacy.apollyon_decision_typed(
                BASE, object(), STATE, PENDING, PB2, "FLANKER", 3
            )
    finally:
        hooks.restore()

    assert hooks.decision_calls == 6
    assert hooks.host_validation_calls == 6
    assert hooks.rejected_attempts == 6


def test_model_result_cannot_claim_host_mutation_before_validation():
    legacy = Legacy()

    hooks = adapter.Pair06V8ApollyonDecisionHooks(
        legacy,
        lambda **kwargs: {
            "host_mutation_performed": True,
            "campaign_action": {"tool": "advance", "arguments": {}},
        },
    )
    hooks.install()
    try:
        with pytest.raises(
            adapter.Pair06V8ApollyonDecisionAdapterHold,
            match="mutated host before validation",
        ):
            legacy.apollyon_decision_typed(
                BASE, object(), STATE, PENDING, PB2, "ECONOMIST", 4
            )
    finally:
        hooks.restore()

    assert legacy.validation_calls == []


def test_adapter_advances_only_to_separate_source_review():
    out = adapter.pair06_v8_apollyon_decision_adapter_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        adapter.Pair06V8ApollyonDecisionAdapterHold,
        match="PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        adapter.execute_game()
