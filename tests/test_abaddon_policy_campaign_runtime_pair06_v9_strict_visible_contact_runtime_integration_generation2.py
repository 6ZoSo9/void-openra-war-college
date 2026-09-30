from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_generation2
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
        production_all = {
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
        }
        contract = {
            "offered_tool_names": list(self.names),
            "legal_units": ["e1", "e3"],
            "legal_buildings": ["powr"],
            "production_functions": {
                name: deepcopy(action)
                for name, action in production_all.items()
                if name in self.names
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
            "production": tuple(contract["production_functions"]),
            "legal_units": tuple(contract["legal_units"]),
            "legal_buildings": tuple(contract["legal_buildings"]),
        })
        if name not in set(contract["offered_tool_names"]):
            return False, "not_offered", []
        return True, "accepted", [("command", name)]


def _state(combat: int, visible: int, buildings: int = 0):
    return {
        "units_summary": [
            {"id": index + 1, "type": "e1", "can_attack": True}
            for index in range(combat)
        ],
        "enemy_summary": [
            {"id": 100 + index, "type": "e1"}
            for index in range(visible)
        ],
        "enemy_buildings_summary": [
            {"id": 200 + index, "type": "fact"}
            for index in range(buildings)
        ],
    }


def _result(tool: str, arguments=None):
    return {
        "host_mutation_performed": False,
        "campaign_action": {
            "tool": tool,
            "arguments": arguments or {},
        },
    }


def test_contract_pins_reviewed_v9_policy_and_remains_nonactivated():
    out = (
        integration
        .pair06_v9_strict_visible_contact_runtime_integration_contract()
    )
    assert out["decision_review_git_blob"] == (
        "6b9e4efdd7294392deefd5461a0403daaab3b90b"
    )
    assert out["policy_git_blob"] == (
        "e3930101947430deecc03013088ad9ccfd1d901e"
    )
    assert out["policy_review_git_blob"] == (
        "94eb0bf58ca5d4265ab8f45e8b0f067d3df53e58"
    )
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["decision_hook_runtime_integration_implemented"] is True
    assert out["proto_game_child_wiring_implemented"] is False
    assert out["runtime_activation_authorized"] is False
    assert out["new_execution_request_opened"] is False


def test_recovery_mode_filters_and_sends_coherent_contract_to_validator():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
        "attack_move",
    ]
    legacy = _Legacy(names)
    seen = []

    def decider(**kwargs):
        seen.append(deepcopy(kwargs))
        return _result("train_unit_e1", {"count": 2})

    hooks = integration.Pair06V9StrictVisibleContactDecisionHooks(
        legacy,
        decider,
    )
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
    assert result[4]["offered_tool_names"] == [
        "train_unit_e1",
        "train_unit_e3",
    ]
    assert tuple(result[4]["production_functions"]) == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert result[4]["legal_units"] == ["e1", "e3"]
    assert result[4]["legal_buildings"] == []
    assert [
        tool["function"]["name"] for tool in seen[0]["typed_tools"]
    ] == ["train_unit_e1", "train_unit_e3"]
    assert legacy.validation_calls == [{
        "name": "train_unit_e1",
        "args": {"count": 2},
        "offered": ("train_unit_e1", "train_unit_e3"),
        "production": ("train_unit_e1", "train_unit_e3"),
        "legal_units": ("e1", "e3"),
        "legal_buildings": (),
    }]
    assert hooks.last_policy_mode == "RECOVERY"


def test_strict_visible_contact_removes_reinforcement_before_decider():
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

    hooks = integration.Pair06V9StrictVisibleContactDecisionHooks(
        legacy,
        decider,
    )
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
    assert offered == (
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    )
    assert "train_unit_e1" not in offered
    assert seen[0]["tool_contract"]["production_functions"] == {}
    assert seen[0]["tool_contract"]["legal_units"] == []
    assert seen[0]["tool_contract"]["legal_buildings"] == []
    assert result[0] == "attack_target"
    assert hooks.last_policy_mode == "STRICT_VISIBLE_CONTACT"


def test_suppressed_reinforcement_rejected_before_host_validation_then_feedback_retries():
    names = [
        "train_unit_e1",
        "attack_target",
        "set_stance",
    ]
    legacy = _Legacy(names)
    calls = []

    def decider(**kwargs):
        calls.append(deepcopy(kwargs))
        if len(calls) == 1:
            return _result("train_unit_e1", {"count": 1})
        return _result(
            "attack_target",
            {"unit_ids": "all_combat", "target_actor_id": 100},
        )

    hooks = integration.Pair06V9StrictVisibleContactDecisionHooks(
        legacy,
        decider,
    )
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(2, 1),
            {},
            object(),
            "FEINTER",
            10,
        )
    finally:
        hooks.restore()

    assert result[0] == "attack_target"
    assert len(result[3]) == 2
    assert result[3][0]["tool"] == "train_unit_e1"
    assert result[3][0]["accepted"] is False
    assert (
        result[3][0]["host_reason"]
        == "function_not_offered:train_unit_e1"
    )
    assert result[3][0]["world_mutated_before_validation"] is False
    assert calls[0]["feedback"] == ""
    assert (
        calls[1]["feedback"]
        == "function_not_offered:train_unit_e1"
    )
    assert len(legacy.validation_calls) == 1
    assert legacy.validation_calls[0]["name"] == "attack_target"
    assert hooks.rejected_attempts == 1


def test_compact_state_is_frozen_across_rejected_attempts():
    names = ["attack_target", "set_stance"]
    legacy = _Legacy(names)
    seen_states = []

    def decider(**kwargs):
        seen_states.append(deepcopy(kwargs["state"]))
        kwargs["state"]["enemy_summary"].clear()
        if len(seen_states) == 1:
            return _result("not_offered")
        return _result(
            "attack_target",
            {"unit_ids": "all_combat", "target_actor_id": 100},
        )

    hooks = integration.Pair06V9StrictVisibleContactDecisionHooks(
        legacy,
        decider,
    )
    hooks.install()
    try:
        legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(2, 1),
            {},
            object(),
            "FEINTER",
            11,
        )
    finally:
        hooks.restore()

    assert seen_states[0] == seen_states[1]
    assert len(seen_states[1]["enemy_summary"]) == 1


def test_normal_mode_preserves_exact_current_contract():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
        "move_units",
        "attack_move",
    ]
    legacy = _Legacy(names)
    initial_contract = legacy.apollyon_tools_typed(None, None, None)[1]
    seen = []

    def decider(**kwargs):
        seen.append(deepcopy(kwargs))
        return _result("advance")

    hooks = integration.Pair06V9StrictVisibleContactDecisionHooks(
        legacy,
        decider,
    )
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

    assert seen[0]["tool_contract"] == initial_contract
    assert result[4] == initial_contract
    assert hooks.last_policy_mode == "NORMAL"


def test_install_and_restore_touch_only_legacy_decision_hook():
    legacy = _Legacy(["advance"])
    original = legacy.apollyon_decision_typed

    hooks = integration.Pair06V9StrictVisibleContactDecisionHooks(
        legacy,
        lambda **kwargs: _result("advance"),
    )
    hooks.install()
    assert legacy.apollyon_decision_typed != original
    hooks.restore()
    assert legacy.apollyon_decision_typed == original


@pytest.mark.parametrize(
    "field",
    (
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
    ),
)
def test_contract_grants_no_effect_authority(field):
    out = (
        integration
        .pair06_v9_strict_visible_contact_runtime_integration_contract()
    )
    assert out[field] is False


def test_integration_advances_only_to_source_review():
    out = (
        integration
        .pair06_v9_strict_visible_contact_runtime_integration_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_RUNTIME_INTEGRATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_RUNTIME_INTEGRATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        integration.Pair06V9StrictVisibleContactRuntimeIntegrationHold,
        match="RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.wire_proto_child_or_execute()
