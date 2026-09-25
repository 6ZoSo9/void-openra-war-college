from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_generation2
    as policy,
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


def _state(combat: int, visible: int) -> dict:
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


def _contract(names: list[str]) -> dict:
    return {
        "offered_tool_names": list(names),
        "legal_units": ["e1"],
        "legal_buildings": ["powr"],
        "production_functions": {
            "train_unit_e1": {
                "kind": "build_unit",
                "unit_type": "e1",
            },
            "build_structure_powr": {
                "kind": "build_and_place",
                "building_type": "powr",
            },
        },
    }


def test_contract_pins_exact_review_and_is_non_authorizing():
    out = policy.pair06_v8_combat_action_priority_policy_contract()
    assert out["proposal_review_main_head"] == (
        "f58ecb5d06cfa92f2b179cfabae54731f6b18d68"
    )
    assert out["proposal_review_git_blob"] == (
        "1f1de1d167efd116b3f3dbce40ea51793cf41d03"
    )
    assert out["proposal_review_source_sha256"] == (
        "719265a4be84a25d5552179b89b2c0c2fcbe10c8912e7c11d193afedffae29fc"
    )
    assert out["pair06_v8_combat_action_priority_policy_implemented"] is True
    assert out["pair06_v8_combat_action_priority_policy_reviewed"] is False
    assert out["runtime_integration_implemented"] is False
    assert out["model_call_implemented"] is False
    assert out["host_command_implemented"] is False
    assert out["game_execution_implemented"] is False


def test_recovery_mode_filters_to_exact_existing_recovery_tools():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
    ]
    tools = [_tool(name) for name in names]
    contract = _contract(names)
    contract["production_functions"]["train_unit_e3"] = {
        "kind": "build_unit",
        "unit_type": "e3",
    }

    out = policy.apply_pair06_v8_combat_action_priority_policy(
        state=_state(0, 0),
        typed_tools=tools,
        tool_contract=contract,
    )

    assert out["mode"] == "RECOVERY"
    assert out["filtered_offered_tool_names"] == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert [x["function"]["name"] for x in out["typed_tools"]] == [
        "train_unit_e1",
        "train_unit_e3",
    ]
    assert out["tool_contract"]["offered_tool_names"] == [
        "train_unit_e1",
        "train_unit_e3",
    ]
    assert out["suppressed_tool_names"] == (
        "advance",
        "build_structure_powr",
    )


def test_visible_contact_mode_retains_combat_reinforcement_and_controls():
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
    out = policy.apply_pair06_v8_combat_action_priority_policy(
        state=_state(3, 2),
        typed_tools=[_tool(name) for name in names],
        tool_contract=_contract(names),
    )

    assert out["mode"] == "VISIBLE_CONTACT"
    assert out["filtered_offered_tool_names"] == (
        "attack_move",
        "attack_target",
        "guard_target",
        "move_units",
        "set_stance",
        "stop_units",
        "train_unit_e1",
    )
    assert set(x["function"]["name"] for x in out["typed_tools"]) == {
        "train_unit_e1",
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    }
    assert "advance" in out["suppressed_tool_names"]
    assert "build_structure_powr" in out["suppressed_tool_names"]


def test_normal_mode_is_exact_identity_surface():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "move_units",
        "attack_move",
    ]
    out = policy.apply_pair06_v8_combat_action_priority_policy(
        state=_state(2, 0),
        typed_tools=[_tool(name) for name in names],
        tool_contract=_contract(names),
    )

    assert out["mode"] == "NORMAL"
    assert out["filtered_offered_tool_names"] == tuple(names)
    assert [x["function"]["name"] for x in out["typed_tools"]] == names
    assert out["suppressed_tool_names"] == ()


def test_inputs_are_not_mutated_and_nested_contract_is_preserved():
    names = ["advance", "build_structure_powr", "train_unit_e1"]
    state = _state(0, 0)
    tools = [_tool(name) for name in names]
    contract = _contract(names)
    before_state = deepcopy(state)
    before_tools = deepcopy(tools)
    before_contract = deepcopy(contract)

    out = policy.apply_pair06_v8_combat_action_priority_policy(
        state=state,
        typed_tools=tools,
        tool_contract=contract,
    )

    assert state == before_state
    assert tools == before_tools
    assert contract == before_contract
    assert (
        out["tool_contract"]["production_functions"]
        == before_contract["production_functions"]
    )


def test_surface_mismatch_fails_closed():
    with pytest.raises(
        policy.Pair06V8CombatActionPriorityPolicyHold,
        match="typed tools and offered_tool_names disagree",
    ):
        policy.apply_pair06_v8_combat_action_priority_policy(
            state=_state(0, 0),
            typed_tools=[_tool("advance"), _tool("train_unit_e1")],
            tool_contract=_contract(["advance"]),
        )


def test_implementation_grants_no_runtime_or_training_authority():
    out = policy.pair06_v8_combat_action_priority_policy_contract()
    for field in (
        "policy_activation_authorized",
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


def test_implementation_advances_only_to_source_review():
    out = policy.pair06_v8_combat_action_priority_policy_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        policy.Pair06V8CombatActionPriorityPolicyHold,
        match="POLICY_IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        policy.integrate_or_execute()
