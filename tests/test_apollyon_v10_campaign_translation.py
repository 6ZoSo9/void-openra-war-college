from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning.apollyon_v10_campaign_translation import (
    CAMPAIGN_INPUT_KIND,
    V10_ACCEPTED_INPUT_KIND,
    TranslationError,
    translate_campaign_turn,
    translate_runtime_tool_call,
    translation_contract,
)


def _tool(name: str, parameters: dict | None = None) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": name,
            "parameters": parameters
            or {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    }


def _surface():
    move_parameters = {
        "type": "object",
        "properties": {
            "unit_ids": {"type": "string"},
            "target_x": {"type": "integer"},
            "target_y": {"type": "integer"},
            "queued": {"type": "boolean"},
        },
        "required": ["unit_ids", "target_x", "target_y"],
        "additionalProperties": False,
    }
    count_parameters = {
        "type": "object",
        "properties": {
            "count": {"type": "integer", "minimum": 1, "maximum": 3},
        },
        "additionalProperties": False,
    }
    tools = [
        _tool("advance"),
        _tool("move_units", move_parameters),
        _tool("build_structure_barr"),
        _tool("build_structure_proc"),
        _tool("train_unit_e1", count_parameters),
    ]
    contract = {
        "production_contract_version": "typed-production-functions-v1",
        "pending_buildings": [],
        "queued_structure_buildings": [],
        "unsupported_structures": ["spen", "syrd"],
        "nonunit_blocklist": ["brik", "fenc", "kenn", "sbag"],
        "legal_buildings": ["barr", "proc"],
        "legal_units": ["e1"],
        "production_functions": {
            "build_structure_barr": {
                "kind": "build_and_place",
                "building_type": "barr",
            },
            "build_structure_proc": {
                "kind": "build_and_place",
                "building_type": "proc",
            },
            "train_unit_e1": {
                "kind": "build_unit",
                "unit_type": "e1",
            },
        },
        "offered_tool_names": sorted(
            [
                "advance",
                "move_units",
                "build_structure_barr",
                "build_structure_proc",
                "train_unit_e1",
            ]
        ),
    }
    return tools, contract


def _state(*, with_barracks: bool = False, with_combat: bool = True) -> dict:
    buildings = [
        {
            "id": 120,
            "type": "fact",
            "cell_x": 12,
            "cell_y": 16,
            "hp_percent": 100.0,
            "is_powered": True,
        },
        {
            "id": 121,
            "type": "powr",
            "cell_x": 13,
            "cell_y": 16,
            "hp_percent": 100.0,
            "is_powered": True,
        },
    ]
    if with_barracks:
        buildings.append(
            {
                "id": 122,
                "type": "barr",
                "cell_x": 14,
                "cell_y": 16,
                "hp_percent": 100.0,
                "is_powered": True,
            }
        )
    units = []
    if with_combat:
        units.extend(
            [
                {
                    "id": 126,
                    "type": "e1",
                    "idle": True,
                    "is_idle": True,
                    "can_attack": True,
                    "stance": 0,
                    "cell_x": 12,
                    "cell_y": 14,
                    "activity": "",
                    "current_activity": "",
                    "hp_percent": 100.0,
                },
                {
                    "id": 127,
                    "type": "e1",
                    "idle": False,
                    "is_idle": False,
                    "can_attack": True,
                    "stance": 0,
                    "cell_x": 13,
                    "cell_y": 14,
                    "activity": "Move",
                    "current_activity": "Move",
                    "hp_percent": 100.0,
                },
                {
                    "id": 128,
                    "type": "harv",
                    "idle": True,
                    "is_idle": True,
                    "can_attack": False,
                    "stance": 0,
                    "cell_x": 11,
                    "cell_y": 18,
                    "activity": "",
                    "current_activity": "",
                    "hp_percent": 100.0,
                },
            ]
        )
    return {
        "tick": 390,
        "economy": {
            "cash": 4700,
            "ore": 300,
            "power_provided": 200,
            "power_drained": 100,
            "resource_capacity": 2000,
            "harvester_count": 1,
        },
        "power_balance": 100,
        "military": {
            "units_killed": 0,
            "units_lost": 0,
            "buildings_killed": 0,
            "buildings_lost": 0,
            "army_value": 100,
            "assets_value": 1000,
            "kills_cost": 0,
            "deaths_cost": 0,
        },
        "units_summary": units,
        "buildings_summary": buildings,
        "enemy_summary": [
            {
                "id": 900,
                "type": "e1",
                "cell_x": 96,
                "cell_y": 32,
                "hp_percent": 100.0,
                "can_attack": True,
                "owner": "Multi1",
            }
        ],
        "enemy_buildings_summary": [],
        "production_items": [],
        # Deliberately broader than the current typed production contract.
        "available_production": ["barr", "proc", "e1", "spen", "kenn"],
        "map": {"width": 128, "height": 128, "map_name": "singles.oramap"},
        "explored_percent": 2.7,
    }


def test_translation_contract_is_exactly_nonexecuting_and_facts_only():
    result = translation_contract()
    assert result["campaign_input_kind"] == CAMPAIGN_INPUT_KIND
    assert result["accepted_input_kind"] == V10_ACCEPTED_INPUT_KIND
    assert result["input_translation_reviewed"] is True
    assert result["output_translation_reviewed"] is True
    assert result["current_state_only"] is True
    assert result["current_tool_list_authoritative"] is True
    assert result["crosses_prior_round"] is False
    assert result["recent_tool_results_may_be_empty"] is True
    assert result["fabricated_information_allowed"] is False
    assert result["fabricated_actor_ids_allowed"] is False
    assert result["fabricated_enemy_locations_allowed"] is False
    assert result["fabricated_movement_coordinates_allowed"] is False
    assert result["runtime_execution_performed"] is False
    assert result["model_execution_performed"] is False
    assert result["game_started"] is False
    assert result["training"] is False
    assert result["weights_updated"] is False


def test_current_typed_tool_contract_becomes_bounded_v10_tool_surface():
    tools, contract = _surface()
    result = translate_campaign_turn(
        system="campaign system",
        state=_state(),
        typed_tools=tools,
        tool_contract=contract,
        doctrine="RUSHER",
        round_no=7,
    )
    assert result["schema"] == "void.apollyon.v10-campaign-translation.v1"
    assert result["binding"]["campaign_input_kind"] == CAMPAIGN_INPUT_KIND
    assert result["binding"]["accepted_input_kind"] == V10_ACCEPTED_INPUT_KIND
    assert result["binding"]["recent_tool_result_count"] == 0
    assert result["binding"]["crosses_prior_round"] is False
    assert result["binding"]["fabricated_information"] is False
    names = [tool["function"]["name"] for tool in result["tools"]]
    assert set(names) == {"advance", "move_units", "build_and_place", "build_unit"}
    assert "build_structure_barr" not in names
    assert "train_unit_e1" not in names

    by_name = {tool["function"]["name"]: tool for tool in result["tools"]}
    build_enum = by_name["build_and_place"]["function"]["parameters"]["properties"][
        "building_type"
    ]["enum"]
    unit_enum = by_name["build_unit"]["function"]["parameters"]["properties"][
        "unit_type"
    ]["enum"]
    assert build_enum == ["barr", "proc"]
    assert unit_enum == ["e1"]


def test_briefing_uses_current_tool_authority_not_raw_available_production():
    tools, contract = _surface()
    result = translate_campaign_turn(
        system="campaign system",
        state=_state(),
        typed_tools=tools,
        tool_contract=contract,
        doctrine="RUSHER",
        round_no=7,
    )
    briefing = result["messages"][-1]["content"]
    assert "Can build: barr, proc, e1" in briefing
    assert "cash=" not in briefing
    assert "credits=$4700" in briefing
    assert "spen" not in briefing
    assert "kenn" not in briefing
    assert "Visible enemy units: e1#900@(96,32)" in briefing
    assert "Idle: [126]" in briefing
    assert "127" in briefing
    assert "Idle: [126,127]" not in briefing
    assert "128" in briefing
    assert "Idle: [126,128]" not in briefing
    assert "NO SCOUTING:" not in briefing
    assert "scouting_status:" not in briefing


def test_feedback_is_current_round_host_fact_not_history():
    tools, contract = _surface()
    result = translate_campaign_turn(
        system="campaign system",
        state=_state(),
        typed_tools=tools,
        tool_contract=contract,
        doctrine="RUSHER",
        round_no=7,
        feedback="function_not_offered:bad_tool",
    )
    assert len(result["messages"]) == 2
    assert [message["role"] for message in result["messages"]] == ["system", "user"]
    briefing = result["messages"][1]["content"]
    assert (
        "PREVIOUS_OUTPUT_REJECTED_BEFORE_WORLD_MUTATION="
        "function_not_offered:bad_tool"
    ) in briefing
    assert "The world state is unchanged" in briefing


def test_canonical_production_output_maps_back_to_exact_typed_identity():
    _, contract = _surface()
    build = translate_runtime_tool_call(
        tool="build_and_place",
        arguments={"building_type": "barr"},
        tool_contract=contract,
    )
    assert build == {
        "tool": "build_structure_barr",
        "arguments": {},
        "source_runtime_tool": "build_and_place",
        "translation_kind": "canonical_structure_to_typed_identity",
    }

    unit = translate_runtime_tool_call(
        tool="build_unit",
        arguments={"unit_type": "e1", "count": 2},
        tool_contract=contract,
    )
    assert unit == {
        "tool": "train_unit_e1",
        "arguments": {"count": 2},
        "source_runtime_tool": "build_unit",
        "translation_kind": "canonical_unit_to_typed_identity",
    }


def test_v10_bounded_advance_normalizes_to_campaign_noop():
    _, contract = _surface()
    result = translate_runtime_tool_call(
        tool="advance",
        arguments={"ticks": 50},
        tool_contract=contract,
    )
    assert result["tool"] == "advance"
    assert result["arguments"] == {}
    assert result["translation_kind"] == "bounded_v10_advance_to_campaign_noop"


@pytest.mark.parametrize(
    ("tool", "arguments", "match"),
    [
        ("build_and_place", {"building_type": "spen"}, "illegal building"),
        ("build_unit", {"unit_type": "dog", "count": 1}, "illegal unit"),
        ("build_unit", {"unit_type": "e1", "count": 4}, "unit count invalid"),
        ("get_exploration_status", {}, "not offered"),
        ("build_structure_barr", {}, "typed production tool leaked"),
    ],
)
def test_unoffered_or_invalid_runtime_output_fails_closed(tool, arguments, match):
    _, contract = _surface()
    with pytest.raises(TranslationError, match=match):
        translate_runtime_tool_call(
            tool=tool,
            arguments=arguments,
            tool_contract=contract,
        )


def test_source_hash_is_stable_for_realization_binding():
    path = Path(__file__).parents[1] / (
        "openra_env/learning/apollyon_v10_campaign_translation.py"
    )
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == "2d32351dff8d96a3254436305c2c402ea06c9a344b6b3ea67cb70c512eef2d53"
