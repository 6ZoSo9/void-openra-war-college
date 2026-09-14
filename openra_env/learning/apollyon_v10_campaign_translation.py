"""Reviewed source-only translation for the promoted Apollyon V10 campaign runtime.

The frozen warm-start campaign supplies a current typed tool list plus a compact
state object. Promoted V10 accepts a current turn briefing plus recent tool
results. This module performs only deterministic representation translation in
both directions. It does not contact a runtime, choose an action, mutate a game,
train a model, or grant campaign execution authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any

TRANSLATION_SCHEMA = "void.apollyon.v10-campaign-translation.v1"
TRANSLATION_CONTRACT_SCHEMA = "void.apollyon.v10-campaign-translation-contract.v1"

CAMPAIGN_INPUT_KIND = "legacy_current_tool_list_plus_compact_state_json"
V10_ACCEPTED_INPUT_KIND = "turn_briefing_plus_recent_tool_results"

LEGACY_WARM_START_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)
BASE_JOINT_RUNNER_SHA256 = (
    "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615"
)
V10_CANDIDATE_SHA256 = (
    "c351d98912dfe18ff8552da5e620b0e3ba6d9877dbc185c45be0dda0fd7d4025"
)
V10_LIVE_INPUT_ADAPTER_SHA256 = (
    "9ba6cfa75bea5ac708f7dd690f67640d3f84e03335de09c8a4514eb5c3437686"
)
V10_LIVE_INPUT_CONTRACT_SHA256 = (
    "fe62a8488454e0974179519a53f79a2c823182daa5225b2ea455518a3489fcfe"
)
V10_OPENAI_BRIDGE_SHA256 = (
    "c197f3b75016dd7c4c25346f98aafdb1f631e2ee6e8b3514f9ebb650490b4510"
)

_TYPED_PRODUCTION_KINDS = {"build_and_place", "build_unit"}
_CANONICAL_PRODUCTION_TOOLS = {"build_and_place", "build_unit"}


class TranslationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TranslationError(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _tool_name(tool: Mapping[str, Any]) -> str:
    _require(tool.get("type") == "function", "only function tools are supported")
    function = tool.get("function")
    _require(isinstance(function, Mapping), "tool.function missing")
    name = function.get("name")
    _require(isinstance(name, str) and bool(name), "tool function name missing")
    return name


def _require_string_list(value: Any, label: str) -> list[str]:
    _require(isinstance(value, list), f"{label} must be list")
    _require(
        all(isinstance(item, str) and item for item in value),
        f"{label} entries invalid",
    )
    _require(len(value) == len(set(value)), f"{label} contains duplicates")
    return list(value)


def _validate_state(state: Mapping[str, Any]) -> None:
    _require(isinstance(state, Mapping), "state must be object")
    _require(type(state.get("tick")) is int and state["tick"] >= 0, "state.tick invalid")

    economy = state.get("economy")
    _require(isinstance(economy, Mapping), "state.economy missing")
    for key in ("cash", "ore", "harvester_count"):
        _require(type(economy.get(key)) is int, f"economy.{key} invalid")
    _require(type(state.get("power_balance")) is int, "state.power_balance invalid")

    for list_key in (
        "units_summary",
        "buildings_summary",
        "enemy_summary",
        "enemy_buildings_summary",
    ):
        _require(isinstance(state.get(list_key), list), f"state.{list_key} missing")
        _require(
            all(isinstance(row, Mapping) for row in state[list_key]),
            f"state.{list_key} entries invalid",
        )

    for row in state["units_summary"]:
        _require(type(row.get("id")) is int and row["id"] > 0, "unit id invalid")
        _require(isinstance(row.get("type"), str) and row["type"], "unit type invalid")
        _require(type(row.get("cell_x")) is int, "unit cell_x invalid")
        _require(type(row.get("cell_y")) is int, "unit cell_y invalid")
        _require(type(row.get("can_attack")) is bool, "unit can_attack invalid")
        idle = row.get("idle", row.get("is_idle"))
        _require(type(idle) is bool, "unit idle flag invalid")

    for row in state["buildings_summary"]:
        _require(type(row.get("id")) is int and row["id"] > 0, "building id invalid")
        _require(
            isinstance(row.get("type"), str) and row["type"],
            "building type invalid",
        )
        _require(type(row.get("cell_x")) is int, "building cell_x invalid")
        _require(type(row.get("cell_y")) is int, "building cell_y invalid")

    for key in ("enemy_summary", "enemy_buildings_summary"):
        for row in state[key]:
            _require(type(row.get("id")) is int and row["id"] > 0, f"{key} id invalid")
            _require(
                isinstance(row.get("type"), str) and row["type"],
                f"{key} type invalid",
            )
            _require(type(row.get("cell_x")) is int, f"{key} cell_x invalid")
            _require(type(row.get("cell_y")) is int, f"{key} cell_y invalid")

    production_items = state.get("production_items")
    _require(isinstance(production_items, list), "state.production_items missing")
    _require(
        all(isinstance(item, str) and item for item in production_items),
        "state.production_items entries invalid",
    )

    available = state.get("available_production")
    _require(isinstance(available, list), "state.available_production missing")
    _require(
        all(isinstance(item, str) and item for item in available),
        "state.available_production entries invalid",
    )

    map_info = state.get("map")
    _require(isinstance(map_info, Mapping), "state.map missing")
    _require(
        type(map_info.get("width")) is int and map_info["width"] > 1,
        "map width invalid",
    )
    _require(
        type(map_info.get("height")) is int and map_info["height"] > 1,
        "map height invalid",
    )

    explored = state.get("explored_percent")
    _require(
        isinstance(explored, (int, float)) and not isinstance(explored, bool),
        "state.explored_percent invalid",
    )


def _validate_tool_contract(contract: Mapping[str, Any]) -> None:
    _require(isinstance(contract, Mapping), "tool contract must be object")
    _require(
        contract.get("production_contract_version") == "typed-production-functions-v1",
        "unsupported production contract",
    )

    legal_buildings = _require_string_list(
        contract.get("legal_buildings"),
        "legal_buildings",
    )
    legal_units = _require_string_list(contract.get("legal_units"), "legal_units")
    offered = _require_string_list(
        contract.get("offered_tool_names"),
        "offered_tool_names",
    )
    _require(
        "build_and_place" not in offered and "build_unit" not in offered,
        "generic production tool leaked into typed campaign surface",
    )

    functions = contract.get("production_functions")
    _require(isinstance(functions, Mapping), "production_functions missing")
    mapped_buildings: set[str] = set()
    mapped_units: set[str] = set()

    for name, raw_action in functions.items():
        _require(isinstance(name, str) and name, "production function name invalid")
        _require(name in offered, f"production function not offered: {name}")
        _require(isinstance(raw_action, Mapping), f"production action invalid: {name}")
        kind = raw_action.get("kind")
        _require(kind in _TYPED_PRODUCTION_KINDS, f"production kind invalid: {name}")
        if kind == "build_and_place":
            value = raw_action.get("building_type")
            _require(isinstance(value, str) and value, f"building type invalid: {name}")
            mapped_buildings.add(value)
        else:
            value = raw_action.get("unit_type")
            _require(isinstance(value, str) and value, f"unit type invalid: {name}")
            mapped_units.add(value)

    _require(mapped_buildings == set(legal_buildings), "legal building mapping drift")
    _require(mapped_units == set(legal_units), "legal unit mapping drift")


def _validate_current_tools(
    typed_tools: Sequence[Mapping[str, Any]],
    contract: Mapping[str, Any],
) -> list[str]:
    _require(
        isinstance(typed_tools, Sequence)
        and not isinstance(typed_tools, (str, bytes, bytearray)),
        "typed tools must be sequence",
    )
    names = [_tool_name(tool) for tool in typed_tools]
    _require(len(names) == len(set(names)), "typed tool names contain duplicates")
    offered = list(contract["offered_tool_names"])
    _require(set(names) == set(offered), "typed tool list disagrees with contract")
    return names


def _group_units(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "0"
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in sorted(rows, key=lambda item: (str(item["type"]), int(item["id"]))):
        grouped.setdefault(str(row["type"]), []).append(row)
    parts = []
    for unit_type, group in grouped.items():
        actors = ",".join(
            f"{int(row['id'])}@({int(row['cell_x'])},{int(row['cell_y'])})"
            for row in group
        )
        parts.append(f"{len(group)}x{unit_type}[{actors}]")
    return " ".join(parts)


def _format_buildings(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "0 ()"
    return " ".join(
        (
            f"{row['type']}({int(row['id'])})@"
            f"({int(row['cell_x'])},{int(row['cell_y'])})"
        )
        for row in sorted(rows, key=lambda item: (str(item["type"]), int(item["id"])))
    )


def _format_visible(rows: Sequence[Mapping[str, Any]]) -> str:
    if not rows:
        return "none"
    return ", ".join(
        (
            f"{row['type']}#{int(row['id'])}@"
            f"({int(row['cell_x'])},{int(row['cell_y'])})"
        )
        for row in sorted(rows, key=lambda item: (str(item["type"]), int(item["id"])))
    )


def _legal_production(contract: Mapping[str, Any]) -> list[str]:
    return [
        *list(contract["legal_buildings"]),
        *list(contract["legal_units"]),
    ]


def _turn_briefing(
    *,
    state: Mapping[str, Any],
    contract: Mapping[str, Any],
    doctrine: str,
    round_no: int,
    feedback: str,
) -> str:
    economy = state["economy"]
    cash = int(economy["cash"])
    ore = int(economy["ore"])
    funds = cash + ore
    power_balance = int(state["power_balance"])
    harvesters = int(economy["harvester_count"])
    explored = float(state["explored_percent"])

    idle_combat = sorted(
        int(row["id"])
        for row in state["units_summary"]
        if row["can_attack"] and bool(row.get("idle", row.get("is_idle")))
    )
    production = (
        ", ".join(str(item) for item in state["production_items"])
        if state["production_items"]
        else "IDLE"
    )
    legal = _legal_production(contract)

    lines = [
        f"--- TURN BRIEFING (tick {int(state['tick'])}) ---",
        f"ROUND={round_no}",
        f"ABADDON_DOCTRINE_PUBLIC_TRAINING_LABEL={doctrine}",
        "SHARED_TICKS_PER_ROUND_FIXED=true",
        (
            f"Funds: ${funds} (credits=${cash} + ore=${ore}) | "
            f"Power: {power_balance:+d} | Harvesters: {harvesters} | "
            f"Explored: {explored:.6g}%"
        ),
        "Units: " + _group_units(state["units_summary"]),
    ]
    if idle_combat:
        lines.append(
            "Idle: [" + ",".join(str(actor_id) for actor_id in idle_combat) + "]"
        )
    lines.extend(
        [
            "Buildings: " + _format_buildings(state["buildings_summary"]),
            "Production: " + production,
        ]
    )
    if legal:
        lines.append("Can build: " + ", ".join(legal))
    lines.extend(
        [
            (
                f"Map: width={int(state['map']['width'])}; "
                f"height={int(state['map']['height'])}"
            ),
            "Visible enemy units: " + _format_visible(state["enemy_summary"]),
            (
                "Visible enemy buildings: "
                + _format_visible(state["enemy_buildings_summary"])
            ),
        ]
    )
    if feedback:
        lines.extend(
            [
                "PREVIOUS_OUTPUT_REJECTED_BEFORE_WORLD_MUTATION=" + feedback,
                (
                    "The world state is unchanged; choose only from the current "
                    "provided tools."
                ),
            ]
        )
    lines.append("---")
    return "\n".join(lines)


def _canonical_runtime_tools(
    typed_tools: Sequence[Mapping[str, Any]],
    contract: Mapping[str, Any],
) -> list[dict[str, Any]]:
    production_names = set(contract["production_functions"])
    output: list[dict[str, Any]] = []

    for tool in typed_tools:
        name = _tool_name(tool)
        if name not in production_names:
            output.append(deepcopy(dict(tool)))

    legal_buildings = list(contract["legal_buildings"])
    if legal_buildings:
        output.append(
            {
                "type": "function",
                "function": {
                    "name": "build_and_place",
                    "description": (
                        "Queue one currently legal structure. The campaign host "
                        "performs deterministic placement after construction."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "building_type": {
                                "type": "string",
                                "enum": legal_buildings,
                            }
                        },
                        "required": ["building_type"],
                        "additionalProperties": False,
                    },
                },
            }
        )

    legal_units = list(contract["legal_units"])
    if legal_units:
        output.append(
            {
                "type": "function",
                "function": {
                    "name": "build_unit",
                    "description": "Queue one to three currently legal units.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "unit_type": {
                                "type": "string",
                                "enum": legal_units,
                            },
                            "count": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 3,
                            },
                        },
                        "required": ["unit_type"],
                        "additionalProperties": False,
                    },
                },
            }
        )

    names = [_tool_name(tool) for tool in output]
    _require(len(names) == len(set(names)), "translated runtime tool names collide")
    return output


def translate_campaign_turn(
    *,
    system: str,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
    doctrine: str,
    round_no: int,
    feedback: str = "",
) -> dict[str, Any]:
    _require(isinstance(system, str) and bool(system), "system prompt required")
    _require(isinstance(doctrine, str) and bool(doctrine), "doctrine required")
    _require(type(round_no) is int and round_no >= 1, "round number invalid")
    _require(isinstance(feedback, str), "feedback must be string")
    _require("\x00" not in feedback and len(feedback) <= 512, "feedback invalid")

    _validate_state(state)
    _validate_tool_contract(tool_contract)
    typed_names = _validate_current_tools(typed_tools, tool_contract)

    briefing = _turn_briefing(
        state=state,
        contract=tool_contract,
        doctrine=doctrine,
        round_no=round_no,
        feedback=feedback.strip(),
    )
    runtime_tools = _canonical_runtime_tools(typed_tools, tool_contract)
    runtime_names = [_tool_name(tool) for tool in runtime_tools]

    body = {
        "schema": TRANSLATION_SCHEMA,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": briefing},
        ],
        "tools": runtime_tools,
        "binding": {
            "campaign_input_kind": CAMPAIGN_INPUT_KIND,
            "accepted_input_kind": V10_ACCEPTED_INPUT_KIND,
            "round": round_no,
            "doctrine": doctrine,
            "source_state_sha256": _sha256(state),
            "source_tool_contract_sha256": _sha256(tool_contract),
            "typed_tool_names": typed_names,
            "runtime_tool_names": runtime_names,
            "recent_tool_result_count": 0,
            "crosses_prior_round": False,
            "uses_current_state_only": True,
            "uses_current_tool_list_only": True,
            "fabricated_information": False,
            "runtime_execution_performed": False,
            "model_execution_performed": False,
            "game_mutation_performed": False,
        },
    }
    return {
        **body,
        "translation_sha256": _sha256(body),
    }


def _typed_name_for(
    contract: Mapping[str, Any],
    *,
    kind: str,
    value_key: str,
    value: str,
) -> str:
    matches = [
        name
        for name, action in contract["production_functions"].items()
        if action.get("kind") == kind and action.get(value_key) == value
    ]
    _require(
        len(matches) == 1,
        f"no unique typed production mapping for {kind}:{value}",
    )
    name = matches[0]
    _require(
        name in contract["offered_tool_names"],
        f"typed production mapping not offered: {name}",
    )
    return name


def translate_runtime_tool_call(
    *,
    tool: str,
    arguments: Mapping[str, Any],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    _require(isinstance(tool, str) and bool(tool), "runtime tool name required")
    _require(isinstance(arguments, Mapping), "runtime tool arguments must be object")
    _validate_tool_contract(tool_contract)
    args = dict(arguments)

    if tool == "build_and_place":
        _require(set(args) == {"building_type"}, "build_and_place arguments invalid")
        building_type = args.get("building_type")
        _require(
            isinstance(building_type, str)
            and building_type in tool_contract["legal_buildings"],
            "runtime selected illegal building",
        )
        typed = _typed_name_for(
            tool_contract,
            kind="build_and_place",
            value_key="building_type",
            value=building_type,
        )
        return {
            "tool": typed,
            "arguments": {},
            "source_runtime_tool": tool,
            "translation_kind": "canonical_structure_to_typed_identity",
        }

    if tool == "build_unit":
        _require(
            set(args).issubset({"unit_type", "count"}),
            "build_unit arguments invalid",
        )
        _require("unit_type" in args, "build_unit unit_type missing")
        unit_type = args.get("unit_type")
        _require(
            isinstance(unit_type, str) and unit_type in tool_contract["legal_units"],
            "runtime selected illegal unit",
        )
        count = args.get("count", 1)
        _require(type(count) is int and 1 <= count <= 3, "runtime unit count invalid")
        typed = _typed_name_for(
            tool_contract,
            kind="build_unit",
            value_key="unit_type",
            value=unit_type,
        )
        return {
            "tool": typed,
            "arguments": {"count": count},
            "source_runtime_tool": tool,
            "translation_kind": "canonical_unit_to_typed_identity",
        }

    if tool == "advance":
        _require(
            args == {} or args == {"ticks": 50},
            "advance arguments are neither campaign-empty nor V10 bounded ticks",
        )
        _require("advance" in tool_contract["offered_tool_names"], "advance not offered")
        return {
            "tool": "advance",
            "arguments": {},
            "source_runtime_tool": tool,
            "translation_kind": "bounded_v10_advance_to_campaign_noop",
        }

    _require(
        tool not in _CANONICAL_PRODUCTION_TOOLS,
        "unexpected production tool",
    )
    _require(
        tool in tool_contract["offered_tool_names"],
        f"runtime tool not offered: {tool}",
    )
    _require(
        tool not in tool_contract["production_functions"],
        "typed production tool leaked from runtime",
    )
    return {
        "tool": tool,
        "arguments": args,
        "source_runtime_tool": tool,
        "translation_kind": "identity_nonproduction",
    }


def translation_contract() -> dict[str, Any]:
    body = {
        "schema": TRANSLATION_CONTRACT_SCHEMA,
        "campaign_input_kind": CAMPAIGN_INPUT_KIND,
        "accepted_input_kind": V10_ACCEPTED_INPUT_KIND,
        "legacy_warm_start_runner_sha256": LEGACY_WARM_START_RUNNER_SHA256,
        "base_joint_runner_sha256": BASE_JOINT_RUNNER_SHA256,
        "v10_candidate_sha256": V10_CANDIDATE_SHA256,
        "v10_live_input_adapter_sha256": V10_LIVE_INPUT_ADAPTER_SHA256,
        "v10_live_input_contract_sha256": V10_LIVE_INPUT_CONTRACT_SHA256,
        "v10_openai_bridge_sha256": V10_OPENAI_BRIDGE_SHA256,
        "input_translation_reviewed": True,
        "output_translation_reviewed": True,
        "current_state_only": True,
        "current_tool_list_authoritative": True,
        "crosses_prior_round": False,
        "recent_tool_results_may_be_empty": True,
        "canonical_production_tools_derived_only_from_current_typed_contract": True,
        "canonical_production_output_must_map_back_to_current_typed_identity": True,
        "host_validation_unchanged": True,
        "fabricated_information_allowed": False,
        "fabricated_actor_ids_allowed": False,
        "fabricated_enemy_locations_allowed": False,
        "fabricated_movement_coordinates_allowed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
        "game_mutation_performed": False,
        "training": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
    }
    return {
        **body,
        "translation_contract_sha256": _sha256(body),
    }
