from __future__ import annotations

import pytest

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_unit_ids_canonicalization_generation2
    as repair,
)


def _state() -> dict:
    return {
        "tick": 2701,
        "economy": {"cash": 4000, "ore": 0, "harvester_count": 1},
        "power_balance": 50,
        "military": {},
        "units_summary": [
            {
                "id": 201,
                "type": "e1",
                "idle": True,
                "can_attack": True,
                "cell_x": 20,
                "cell_y": 20,
            },
            {
                "id": 202,
                "type": "e1",
                "idle": True,
                "can_attack": True,
                "cell_x": 21,
                "cell_y": 20,
            },
        ],
        "buildings_summary": [],
        "enemy_summary": [],
        "enemy_buildings_summary": [],
        "production_items": [],
        "available_production": ["barr", "e1"],
        "map": {"width": 112, "height": 54, "name": "Singles"},
        "explored_percent": 10.0,
    }


def _contract() -> dict:
    return {
        "production_contract_version": "typed-production-functions-v1",
        "legal_buildings": ["barr"],
        "legal_units": ["e1"],
        "production_functions": {
            "build_structure_barr": {
                "kind": "build_and_place",
                "building_type": "barr",
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


def _runtime_tools() -> list[dict]:
    typed = [_tool(name) for name in _contract()["offered_tool_names"]]
    return v8_runtime.translate_campaign_turn_for_v8(
        state=_state(),
        typed_tools=typed,
        tool_contract=_contract(),
        doctrine="FEINTER",
        round_no=6,
        feedback="",
    )["tools"]


def _raw(unit_ids: str) -> str:
    return (
        "<tool_call><function=move_units>"
        f"<parameter=unit_ids>{unit_ids}</parameter>"
        "<parameter=target_x>25</parameter>"
        "<parameter=target_y>26</parameter>"
        "<parameter=queued>false</parameter>"
        "</function></tool_call>"
    )


def test_integer_list_is_canonicalized_only_when_all_ids_are_currently_owned():
    out = repair.canonicalize_move_units_unit_ids(
        raw_model_output=_raw("[201,202]"),
        state=_state(),
        runtime_tools=_runtime_tools(),
        tool_contract=_contract(),
    )

    assert out["canonicalization_applied"] is True
    assert out["canonical_unit_ids"] == "201,202"
    assert out["canonicalized_ids"] == [201, 202]
    assert out["owned_ids_checked"] is True
    assert out["frozen_v8_translation_revalidated"] is True
    assert out["host_validation_performed"] is False

    translated = v8_runtime.translate_v8_output_to_campaign(
        text=out["canonical_raw_model_output"],
        runtime_tools=_runtime_tools(),
        tool_contract=_contract(),
    )
    assert translated["tool"] == "move_units"
    assert translated["arguments"]["unit_ids"] == "201,202"


def test_bare_integer_is_canonicalized_to_existing_required_string_wire_type():
    out = repair.canonicalize_move_units_unit_ids(
        raw_model_output=_raw("201"),
        state=_state(),
        runtime_tools=_runtime_tools(),
        tool_contract=_contract(),
    )
    assert out["canonicalization_applied"] is True
    assert out["canonical_unit_ids"] == "201"
    assert out["canonicalized_ids"] == [201]


def test_existing_string_passes_through_byte_for_byte():
    raw = _raw('"201,202"')
    out = repair.canonicalize_move_units_unit_ids(
        raw_model_output=raw,
        state=_state(),
        runtime_tools=_runtime_tools(),
        tool_contract=_contract(),
    )
    assert out["canonicalization_applied"] is False
    assert out["reason"] == "unit_ids_already_string"
    assert out["canonical_raw_model_output"] == raw


def test_non_move_units_passes_through_byte_for_byte():
    raw = (
        "<tool_call><function=advance>"
        "<parameter=ticks>50</parameter>"
        "</function></tool_call>"
    )
    out = repair.canonicalize_move_units_unit_ids(
        raw_model_output=raw,
        state=_state(),
        runtime_tools=_runtime_tools(),
        tool_contract=_contract(),
    )
    assert out["canonicalization_applied"] is False
    assert out["reason"] == "non_move_units_passthrough"
    assert out["canonical_raw_model_output"] == raw


@pytest.mark.parametrize(
    ("unit_ids", "message"),
    (
        ("[201,999]", "absent from current own_units"),
        ("[201,201]", "must not contain duplicates"),
        ("[]", "must be non-empty"),
        ("true", "not V4-canonicalizable"),
        ("1.5", "not V4-canonicalizable"),
        ('{"nested":201}', "not V4-canonicalizable"),
    ),
)
def test_ambiguous_or_unsafe_values_fail_closed(unit_ids, message):
    with pytest.raises(
        repair.Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationHold,
        match=message,
    ):
        repair.canonicalize_move_units_unit_ids(
            raw_model_output=_raw(unit_ids),
            state=_state(),
            runtime_tools=_runtime_tools(),
            tool_contract=_contract(),
        )


def test_current_own_unit_ids_must_themselves_be_well_formed():
    state = _state()
    state["units_summary"][1]["id"] = 201
    with pytest.raises(
        repair.Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationHold,
        match="duplicated",
    ):
        repair.canonicalize_move_units_unit_ids(
            raw_model_output=_raw("[201]"),
            state=state,
            runtime_tools=_runtime_tools(),
            tool_contract=_contract(),
        )


@pytest.mark.parametrize(
    "field",
    (
        "frozen_v8_runtime_source_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "host_validator_bypassed",
        "world_mutation_performed",
        "consumed_v3_attempt_retry_authorized",
        "new_execution_request_opened",
        "attempt_claim_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_contract_opens_no_runtime_or_extra_authority(field):
    out = repair.pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_contract()
    assert out[field] is False


def test_contract_binds_consumed_v3_failure_and_stops_at_review():
    out = repair.pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_contract()
    assert out["consumed_v3_main_head"] == (
        "e983220f85e35c024bcc0da8dec418bcd8342e03"
    )
    assert out["observed_v3_failed_round"] == 6
    assert out["observed_v3_max_attempts"] == 6
    assert out["observed_v3_terminal_feedback"].endswith(
        "not_json_array_or_bare_integer__"
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"].endswith("SOURCE_BINDING_REVIEW_REQUIRED")
