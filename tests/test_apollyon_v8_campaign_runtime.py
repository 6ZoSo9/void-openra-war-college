from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning.apollyon_v8_campaign_runtime import (
    ACCEPTED_TOOL_NAMES,
    LEGACY_SYSTEM_PROMPT,
    TRANSFER_SYSTEM_PROMPT,
    V8CampaignRuntimeError,
    parse_v8_tool_output,
    translate_campaign_turn_for_v8,
    translate_v8_output_to_campaign,
    v8_tool_runtime_contract,
)


def _state() -> dict:
    return {
        "tick": 390,
        "economy": {"cash": 4700, "ore": 0, "harvester_count": 0},
        "power_balance": 60,
        "military": {},
        "units_summary": [
            {
                "id": 999,
                "type": "mcv",
                "idle": True,
                "can_attack": False,
                "cell_x": 12,
                "cell_y": 16,
            },
            {
                "id": 201,
                "type": "e1",
                "idle": True,
                "can_attack": True,
                "cell_x": 14,
                "cell_y": 16,
            },
        ],
        "buildings_summary": [
            {"id": 120, "type": "fact", "cell_x": 12, "cell_y": 16},
            {"id": 121, "type": "powr", "cell_x": 13, "cell_y": 16},
        ],
        "enemy_summary": [],
        "enemy_buildings_summary": [],
        "production_items": [],
        "available_production": ["barr", "proc", "e1"],
        "map": {"width": 112, "height": 54, "name": "Singles"},
        "explored_percent": 4.25,
    }


def _contract() -> dict:
    return {
        "production_contract_version": "typed-production-functions-v1",
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
            "train_unit_e1": {"kind": "build_unit", "unit_type": "e1"},
        },
        "offered_tool_names": [
            "get_game_state",
            "deploy_unit",
            "advance",
            "move_units",
            "cancel_production",
            "build_structure_barr",
            "build_structure_proc",
            "train_unit_e1",
        ],
    }


def _tool(name: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": name,
            "parameters": {"type": "object", "properties": {}},
        },
    }


def _typed_tools() -> list[dict]:
    return [_tool(name) for name in _contract()["offered_tool_names"]]


def _turn(feedback: str = "") -> dict:
    return translate_campaign_turn_for_v8(
        state=_state(),
        typed_tools=_typed_tools(),
        tool_contract=_contract(),
        doctrine="RUSHER",
        round_no=1,
        feedback=feedback,
    )


def test_contract_binds_accepted_v8_transport_and_stays_nonexecuting():
    result = v8_tool_runtime_contract()
    assert result["v8_adapter_sha256"] == (
        "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6"
    )
    assert result["v8_accepted_evaluator_sha256"] == (
        "8c39267872ba797b30ce2ff7a2174863d7a5d4c8061afc6db8571786a7ea5f27"
    )
    assert result["base_model_resolved_revision"] == (
        "3764fa359b9082ea5a1e4a5e3ac3aaf6e9671636"
    )
    assert result["chat_template_sha256"] == (
        "8452ca85cb1e0ff04304c02f417a53305d5ba17f6eb9d5693343ad8355f985a8"
    )
    assert result["tokenizer_json_sha256"] == (
        "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4"
    )
    assert result["accepted_tool_names"] == list(ACCEPTED_TOOL_NAMES)
    assert result["accepted_user_prompt_prefix"] == "CURRENT STATE:"
    assert result["current_state_fact_renderer_reviewed"] is True
    assert result["parser_exactly_one_tool_call"] is True
    assert result["parser_rejects_duplicate_parameters"] is True
    assert result["parser_rejects_trailing_suffix"] is True
    assert result["tool_schema_narrowing_only"] is True
    assert result["local_runtime_loader_implemented"] is True
    assert result["runtime_assets_hash_verified_before_load"] is True
    assert result["offline_only_model_load"] is True
    assert result["accepted_chat_template_generation_implemented"] is True
    assert result["campaign_decision_adapter_implemented"] is True
    assert result["advance_narrowed_to_shared_50_ticks"] is True
    assert result["host_validation_unchanged"] is True
    assert result["runtime_execution_performed"] is False
    assert result["model_execution_performed"] is False
    assert result["game_started"] is False
    assert result["training"] is False
    assert result["weights_updated"] is False


def test_campaign_translation_uses_exact_accepted_prompt_and_current_two_message_shape():
    result = _turn()
    assert result["messages"][0] == {"role": "system", "content": TRANSFER_SYSTEM_PROMPT}
    assert result["messages"][1]["role"] == "user"
    assert len(result["messages"]) == 2
    user = result["messages"][1]["content"]
    assert user.startswith("CURRENT STATE: ")
    assert "map_bounds=x=0..111,y=0..53" in user
    assert "visible_enemies=[]" in user
    assert "legal_buildings=[\"barr\",\"proc\"]" in user
    assert "NO SCOUTING" not in user
    assert "cash is sufficient" not in user
    assert result["binding"]["system_prompt_family"] == "transfer"
    assert result["binding"]["uses_current_state_only"] is True
    assert result["binding"]["uses_current_tool_list_only"] is True
    assert result["binding"]["fabricated_information"] is False
    assert result["binding"]["runtime_execution_performed"] is False
    assert result["binding"]["model_execution_performed"] is False


def test_rejection_feedback_switches_only_to_exact_accepted_legacy_prompt():
    result = _turn("held_before_world_mutation")
    assert result["messages"][0] == {"role": "system", "content": LEGACY_SYSTEM_PROMPT}
    assert result["binding"]["system_prompt_family"] == "legacy"
    assert 'guard_feedback="held_before_world_mutation"' in result["messages"][1]["content"]


def test_runtime_tool_schema_is_accepted_surface_with_safe_campaign_narrowing():
    result = _turn()
    by_name = {tool["function"]["name"]: tool for tool in result["tools"]}
    assert list(by_name) == list(ACCEPTED_TOOL_NAMES)
    advance = by_name["advance"]["function"]["parameters"]["properties"]["ticks"]
    assert advance["minimum"] == advance["maximum"] == 50
    unit = by_name["build_unit"]["function"]["parameters"]["properties"]
    assert unit["unit_type"]["enum"] == ["e1"]
    assert unit["count"]["maximum"] == 3
    building = by_name["build_and_place"]["function"]["parameters"]["properties"]
    assert building["building_type"]["enum"] == ["barr", "proc"]
    assert building["cell_x"]["minimum"] == building["cell_x"]["maximum"] == 0
    assert building["cell_y"]["minimum"] == building["cell_y"]["maximum"] == 0


def test_parser_matches_accepted_wire_shape_and_allows_reasoning_prefix():
    parsed = parse_v8_tool_output(
        "Choose the legal build.\n"
        "<tool_call><function=build_and_place>"
        "<parameter=building_type>barr</parameter>"
        "</function></tool_call>"
    )
    assert parsed["tool"] == "build_and_place"
    assert parsed["arguments"] == {"building_type": "barr"}
    assert parsed["reasoning_prefix_present"] is True
    assert parsed["suffix_clean"] is True


@pytest.mark.parametrize(
    "text",
    [
        (
            "<tool_call><function=advance><parameter=ticks>50</parameter></function></tool_call>"
            "<tool_call><function=get_game_state></function></tool_call>"
        ),
        (
            "<tool_call><function=advance><parameter=ticks>50</parameter>"
            "<parameter=ticks>50</parameter></function></tool_call>"
        ),
        (
            "<tool_call><function=advance><parameter=ticks>50</parameter></function></tool_call>"
            " trailing"
        ),
    ],
)
def test_parser_fails_closed_on_multiple_duplicate_or_suffix(text):
    with pytest.raises(V8CampaignRuntimeError):
        parse_v8_tool_output(text)


def test_v8_structure_output_maps_to_current_typed_identity():
    turn = _turn()
    result = translate_v8_output_to_campaign(
        text=(
            "<tool_call><function=build_and_place>"
            "<parameter=building_type>barr</parameter>"
            "<parameter=cell_x>0</parameter><parameter=cell_y>0</parameter>"
            "</function></tool_call>"
        ),
        runtime_tools=turn["tools"],
        tool_contract=_contract(),
    )
    assert result["tool"] == "build_structure_barr"
    assert result["arguments"] == {}
    assert result["host_validation_unchanged"] is True


def test_v8_nonzero_structure_coordinates_fail_closed():
    turn = _turn()
    with pytest.raises(V8CampaignRuntimeError, match="nonzero placement"):
        translate_v8_output_to_campaign(
            text=(
                "<tool_call><function=build_and_place>"
                "<parameter=building_type>barr</parameter>"
                "<parameter=cell_x>17</parameter>"
                "</function></tool_call>"
            ),
            runtime_tools=turn["tools"],
            tool_contract=_contract(),
        )


def test_v8_advance_is_narrowed_to_shared_campaign_tick():
    turn = _turn()
    result = translate_v8_output_to_campaign(
        text=(
            "<tool_call><function=advance><parameter=ticks>50</parameter>"
            "</function></tool_call>"
        ),
        runtime_tools=turn["tools"],
        tool_contract=_contract(),
    )
    assert result["tool"] == "advance"
    assert result["arguments"] == {}
    with pytest.raises(V8CampaignRuntimeError, match="exactly 50"):
        translate_v8_output_to_campaign(
            text=(
                "<tool_call><function=advance><parameter=ticks>25</parameter>"
                "</function></tool_call>"
            ),
            runtime_tools=turn["tools"],
            tool_contract=_contract(),
        )


def test_v8_unit_output_maps_to_typed_identity_and_caps_count():
    turn = _turn()
    result = translate_v8_output_to_campaign(
        text=(
            "<tool_call><function=build_unit><parameter=unit_type>e1</parameter>"
            "<parameter=count>3</parameter></function></tool_call>"
        ),
        runtime_tools=turn["tools"],
        tool_contract=_contract(),
    )
    assert result["tool"] == "train_unit_e1"
    assert result["arguments"] == {"count": 3}
    with pytest.raises(V8CampaignRuntimeError, match="count"):
        translate_v8_output_to_campaign(
            text=(
                "<tool_call><function=build_unit><parameter=unit_type>e1</parameter>"
                "<parameter=count>4</parameter></function></tool_call>"
            ),
            runtime_tools=turn["tools"],
            tool_contract=_contract(),
        )


def test_tampered_runtime_tool_schema_is_rejected_before_mapping():
    turn = _turn()
    tampered = [dict(tool) for tool in turn["tools"]]
    for index, tool in enumerate(tampered):
        if tool["function"]["name"] == "advance":
            replacement = {
                **tool,
                "function": {
                    **tool["function"],
                    "parameters": {
                        **tool["function"]["parameters"],
                        "properties": {
                            "ticks": {"type": "integer", "minimum": 1, "maximum": 50}
                        },
                    },
                },
            }
            tampered[index] = replacement
            break
    with pytest.raises(V8CampaignRuntimeError, match="exactly 50"):
        translate_v8_output_to_campaign(
            text=(
                "<tool_call><function=advance><parameter=ticks>50</parameter>"
                "</function></tool_call>"
            ),
            runtime_tools=tampered,
            tool_contract=_contract(),
        )


def test_unavailable_accepted_tool_is_rejected_before_host_mapping():
    turn = _turn()
    limited = [tool for tool in turn["tools"] if tool["function"]["name"] != "move_units"]
    with pytest.raises(V8CampaignRuntimeError, match="unavailable"):
        translate_v8_output_to_campaign(
            text=(
                "<tool_call><function=move_units><parameter=unit_ids>all_idle</parameter>"
                "<parameter=target_x>22</parameter><parameter=target_y>11</parameter>"
                "</function></tool_call>"
            ),
            runtime_tools=limited,
            tool_contract=_contract(),
        )


def test_source_hash_is_stable_for_runtime_realization_binding():
    path = Path(__file__).parents[1] / "openra_env/learning/apollyon_v8_campaign_runtime.py"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "98a37ce59cabead530fb90f696b32081789ae8b5db61a7fd29df7c01137fbe16"
