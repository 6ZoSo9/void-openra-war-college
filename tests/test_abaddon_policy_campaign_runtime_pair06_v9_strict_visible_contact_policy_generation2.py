from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_generation2
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


def _state(combat: int, visible_units: int, visible_buildings: int = 0) -> dict:
    return {
        "units_summary": [
            {"id": index + 1, "type": "e1", "can_attack": True}
            for index in range(combat)
        ],
        "enemy_summary": [
            {"id": 100 + index, "type": "e1"}
            for index in range(visible_units)
        ],
        "enemy_buildings_summary": [
            {"id": 200 + index, "type": "fact"}
            for index in range(visible_buildings)
        ],
    }


def _contract(names: list[str]) -> dict:
    return {
        "offered_tool_names": list(names),
        "legal_units": ["e1", "e3"],
        "legal_buildings": ["powr"],
        "production_functions": {
            "train_unit_e1": {"kind": "build_unit", "unit_type": "e1"},
            "train_unit_e3": {"kind": "build_unit", "unit_type": "e3"},
            "build_structure_powr": {
                "kind": "build_and_place",
                "building_type": "powr",
            },
        },
    }


def test_contract_is_pure_source_only_implementation():
    out = policy.pair06_v9_strict_visible_contact_policy_contract()

    assert out["proposal_review_git_blob"] == (
        "b13b8dd67062f75a1b324106366f11ac01b7ac8a"
    )
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["baseline_policy_id"] == (
        "pair06-v8-combat-action-priority-envelope-v1"
    )
    assert out["pair06_v9_strict_visible_contact_policy_implemented"] is True
    assert out["pair06_v9_strict_visible_contact_policy_reviewed"] is False
    assert out["implementation_layer"] == (
        "pure_pre_inference_tool_surface_transform"
    )
    assert out["runtime_integration_implemented"] is False
    assert out["model_call_implemented"] is False
    assert out["host_command_implemented"] is False
    assert out["game_execution_implemented"] is False
    assert out["new_execution_request_opened"] is False


def test_recovery_mode_keeps_only_current_recovery_tools():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
        "attack_move",
    ]
    out = policy.apply_pair06_v9_strict_visible_contact_policy(
        state=_state(0, 0),
        typed_tools=[_tool(name) for name in names],
        tool_contract=_contract(names),
    )

    assert out["mode"] == "RECOVERY"
    assert out["filtered_offered_tool_names"] == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert [tool["function"]["name"] for tool in out["typed_tools"]] == [
        "train_unit_e1",
        "train_unit_e3",
    ]
    assert out["reinforcement_tools_suppressed"] == ()


def test_strict_contact_keeps_only_engagement_and_tactical_controls():
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
    out = policy.apply_pair06_v9_strict_visible_contact_policy(
        state=_state(4, 1, 1),
        typed_tools=[_tool(name) for name in names],
        tool_contract=_contract(names),
    )

    expected = (
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    )
    assert out["mode"] == "STRICT_VISIBLE_CONTACT"
    assert out["filtered_offered_tool_names"] == expected
    assert tuple(
        tool["function"]["name"] for tool in out["typed_tools"]
    ) == expected
    assert out["tool_contract"]["offered_tool_names"] == list(expected)
    assert out["reinforcement_tools_suppressed"] == ("train_unit_e1",)
    assert out["suppressed_tool_names"] == (
        "advance",
        "build_structure_powr",
        "train_unit_e1",
    )


def test_normal_mode_preserves_exact_tool_order_and_membership():
    names = [
        "advance",
        "train_unit_e1",
        "move_units",
        "attack_move",
    ]
    out = policy.apply_pair06_v9_strict_visible_contact_policy(
        state=_state(3, 0),
        typed_tools=[_tool(name) for name in names],
        tool_contract=_contract(names),
    )

    assert out["mode"] == "NORMAL"
    assert out["filtered_offered_tool_names"] == tuple(names)
    assert tuple(
        tool["function"]["name"] for tool in out["typed_tools"]
    ) == tuple(names)
    assert out["suppressed_tool_names"] == ()


def test_input_state_tools_and_contract_are_not_mutated():
    names = [
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "attack_target",
        "set_stance",
    ]
    state = _state(2, 1)
    tools = [_tool(name) for name in names]
    contract = _contract(names)
    before_state = deepcopy(state)
    before_tools = deepcopy(tools)
    before_contract = deepcopy(contract)

    out = policy.apply_pair06_v9_strict_visible_contact_policy(
        state=state,
        typed_tools=tools,
        tool_contract=contract,
    )

    assert state == before_state
    assert tools == before_tools
    assert contract == before_contract
    assert out["tool_contract"] is not contract
    assert out["typed_tools"] is not tools


def test_typed_legality_and_production_mappings_are_preserved_verbatim():
    names = [
        "build_structure_powr",
        "train_unit_e1",
        "attack_target",
        "set_stance",
    ]
    contract = _contract(names)
    out = policy.apply_pair06_v9_strict_visible_contact_policy(
        state=_state(1, 1),
        typed_tools=[_tool(name) for name in names],
        tool_contract=contract,
    )

    assert out["tool_contract"]["production_functions"] == (
        contract["production_functions"]
    )
    assert out["tool_contract"]["legal_units"] == contract["legal_units"]
    assert out["tool_contract"]["legal_buildings"] == contract["legal_buildings"]


def test_order_or_membership_mismatch_fails_closed():
    names = ["attack_target", "set_stance", "train_unit_e1"]
    with pytest.raises(
        policy.Pair06V9StrictVisibleContactPolicyHold,
        match="order or membership disagree",
    ):
        policy.apply_pair06_v9_strict_visible_contact_policy(
            state=_state(1, 1),
            typed_tools=[_tool(name) for name in names],
            tool_contract=_contract(
                ["set_stance", "attack_target", "train_unit_e1"]
            ),
        )


def test_duplicate_tool_name_fails_closed():
    with pytest.raises(
        policy.Pair06V9StrictVisibleContactPolicyHold,
        match="typed tool names contain duplicates",
    ):
        policy.apply_pair06_v9_strict_visible_contact_policy(
            state=_state(1, 1),
            typed_tools=[_tool("attack_target"), _tool("attack_target")],
            tool_contract=_contract(["attack_target"]),
        )


def test_missing_or_invalid_compact_state_fails_closed():
    names = ["attack_target"]
    with pytest.raises(
        policy.Pair06V9StrictVisibleContactPolicyHold,
        match="units_summary missing",
    ):
        policy.apply_pair06_v9_strict_visible_contact_policy(
            state={
                "enemy_summary": [],
                "enemy_buildings_summary": [],
            },
            typed_tools=[_tool(name) for name in names],
            tool_contract=_contract(names),
        )


@pytest.mark.parametrize(
    "field",
    (
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
def test_implementation_grants_no_effect_authority(field):
    out = policy.pair06_v9_strict_visible_contact_policy_contract()
    assert out[field] is False


def test_implementation_advances_only_to_source_review():
    out = policy.pair06_v9_strict_visible_contact_policy_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_integrate_or_execute_holds():
    with pytest.raises(
        policy.Pair06V9StrictVisibleContactPolicyHold,
        match="IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        policy.integrate_or_execute()
