from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_generation2
    as integration,
)


def _tool(name: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": name,
            "parameters": {"type": "object", "properties": {}},
        },
    }


class _Base:
    @staticmethod
    def compact_state(state):
        return deepcopy(state)


class _Legacy:
    def __init__(self, names):
        self.names = list(names)
        self.apollyon_decision_typed = self._original
        self.validation_calls = []

    def _original(self, *args, **kwargs):
        return "original"

    def apollyon_tools_typed(self, base, state, pending):
        contract = {
            "offered_tool_names": list(self.names),
            "legal_units": ["e1", "e3"],
            "legal_buildings": ["powr"],
            "production_functions": {
                "train_unit_e1": {
                    "kind": "build_unit",
                    "unit_type": "e1",
                },
                "train_unit_e3": {
                    "kind": "build_unit",
                    "unit_type": "e3",
                },
                "build_structure_powr": {
                    "kind": "build_and_place",
                    "building_type": "powr",
                },
            },
        }
        return [_tool(name) for name in self.names], contract

    def decision_to_commands_typed(
        self,
        base,
        name,
        args,
        state,
        pending,
        pb2,
        contract,
    ):
        self.validation_calls.append({
            "name": name,
            "args": deepcopy(args),
            "offered": tuple(contract["offered_tool_names"]),
        })
        if name not in set(contract["offered_tool_names"]):
            return False, "not_offered", []
        return True, "accepted", [("command", name)]


def _state(combat: int, visible: int):
    return {
        "units_summary": [
            {"id": index + 1, "type": "e1", "can_attack": True}
            for index in range(combat)
        ],
        "enemy_summary": [
            {"id": 100 + index, "type": "e1"}
            for index in range(visible)
        ],
        "enemy_buildings_summary": [],
    }


def _result(tool: str, arguments=None):
    return {
        "host_mutation_performed": False,
        "campaign_action": {
            "tool": tool,
            "arguments": arguments or {},
        },
    }


def test_contract_pins_reviewed_dependencies_and_remains_nonactivated():
    out = (
        integration
        .pair06_v8_combat_action_priority_runtime_integration_contract()
    )
    assert out["decision_adapter_git_blob"] == (
        "4c8296f6ca642bbaa72b88c1c308e56b8810ce62"
    )
    assert out["decision_review_git_blob"] == (
        "6b9e4efdd7294392deefd5461a0403daaab3b90b"
    )
    assert out["policy_review_main_head"] == (
        "55c599605ec0fbf156b724d7844efa44f52a6695"
    )
    assert out["policy_review_git_blob"] == (
        "6b53ca134325e57d89066894636eb7d574bd3af3"
    )
    assert out["decision_hook_runtime_integration_implemented"] is True
    assert out["proto_game_child_wiring_implemented"] is False
    assert out["runtime_activation_authorized"] is False


def test_recovery_mode_filters_before_decider_and_uses_unchanged_validator():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
    ]
    legacy = _Legacy(names)
    seen = []

    def decider(**kwargs):
        seen.append(deepcopy(kwargs))
        return _result("train_unit_e1", {"count": 2})

    hooks = integration.Pair06V8CombatPriorityDecisionHooks(legacy, decider)
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(0, 0),
            {},
            object(),
            "FEINTER",
            8,
        )
    finally:
        hooks.restore()

    assert result[0] == "train_unit_e1"
    assert result[1] == {"count": 2}
    assert result[2] == [("command", "train_unit_e1")]
    assert result[4]["offered_tool_names"] == [
        "train_unit_e1",
        "train_unit_e3",
    ]
    assert [
        tool["function"]["name"] for tool in seen[0]["typed_tools"]
    ] == ["train_unit_e1", "train_unit_e3"]
    assert tuple(seen[0]["tool_contract"]["offered_tool_names"]) == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert legacy.validation_calls == [{
        "name": "train_unit_e1",
        "args": {"count": 2},
        "offered": ("train_unit_e1", "train_unit_e3"),
    }]
    assert hooks.last_priority_mode == "RECOVERY"


def test_visible_contact_mode_filters_before_decider():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    ]
    legacy = _Legacy(names)
    seen = []

    def decider(**kwargs):
        seen.append(deepcopy(kwargs))
        return _result(
            "attack_target",
            {"unit_ids": "all_combat", "target_actor_id": 100},
        )

    hooks = integration.Pair06V8CombatPriorityDecisionHooks(legacy, decider)
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(3, 2),
            {},
            object(),
            "FEINTER",
            3,
        )
    finally:
        hooks.restore()

    offered = tuple(seen[0]["tool_contract"]["offered_tool_names"])
    assert "advance" not in offered
    assert "build_structure_powr" not in offered
    assert "attack_target" in offered
    assert "attack_move" in offered
    assert "move_units" in offered
    assert "train_unit_e1" in offered
    assert result[0] == "attack_target"
    assert hooks.last_priority_mode == "VISIBLE_CONTACT"


def test_suppressed_action_is_rejected_without_host_validation_then_feedback_retries():
    names = ["advance", "build_structure_powr", "train_unit_e1"]
    legacy = _Legacy(names)
    calls = []

    def decider(**kwargs):
        calls.append(deepcopy(kwargs))
        if len(calls) == 1:
            return _result("advance")
        return _result("train_unit_e1", {"count": 1})

    hooks = integration.Pair06V8CombatPriorityDecisionHooks(legacy, decider)
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(0, 0),
            {},
            object(),
            "FEINTER",
            10,
        )
    finally:
        hooks.restore()

    assert result[0] == "train_unit_e1"
    assert len(result[3]) == 2
    assert result[3][0]["accepted"] is False
    assert result[3][0]["host_reason"] == "function_not_offered:advance"
    assert result[3][0]["world_mutated_before_validation"] is False
    assert calls[0]["feedback"] == ""
    assert calls[1]["feedback"] == "function_not_offered:advance"
    assert len(legacy.validation_calls) == 1
    assert legacy.validation_calls[0]["name"] == "train_unit_e1"
    assert hooks.rejected_attempts == 1


def test_normal_mode_preserves_exact_current_surface():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "move_units",
        "attack_move",
    ]
    legacy = _Legacy(names)
    seen = []

    def decider(**kwargs):
        seen.append(deepcopy(kwargs))
        return _result("advance")

    hooks = integration.Pair06V8CombatPriorityDecisionHooks(legacy, decider)
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(2, 0),
            {},
            object(),
            "FEINTER",
            1,
        )
    finally:
        hooks.restore()

    assert tuple(seen[0]["tool_contract"]["offered_tool_names"]) == tuple(names)
    assert result[4]["offered_tool_names"] == names
    assert hooks.last_priority_mode == "NORMAL"


def test_install_and_restore_touch_only_legacy_decision_hook():
    legacy = _Legacy(["advance"])
    original = legacy.apollyon_decision_typed

    hooks = integration.Pair06V8CombatPriorityDecisionHooks(
        legacy,
        lambda **kwargs: _result("advance"),
    )
    hooks.install()
    assert legacy.apollyon_decision_typed != original
    hooks.restore()
    assert legacy.apollyon_decision_typed == original


def test_contract_grants_no_activation_execution_or_training_authority():
    out = (
        integration
        .pair06_v8_combat_action_priority_runtime_integration_contract()
    )
    for field in (
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_integration_advances_only_to_source_review():
    out = (
        integration
        .pair06_v8_combat_action_priority_runtime_integration_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        integration.Pair06V8CombatActionPriorityRuntimeIntegrationHold,
        match="RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.wire_proto_child_or_execute()
