"""Pure coherent implementation of the reviewed pair-06 V9 strict-contact envelope.

This module implements one deterministic pre-inference transform. It derives
combat/contact counts from the current compact state, calls the reviewed V9
proposal, filters copies of the currently offered typed tools, and keeps the
typed production contract coherent with that filtered surface.

RECOVERY remains recovery-only production. NORMAL remains exact identity.
STRICT_VISIBLE_CONTACT retains only currently offered engagement and tactical-
control functions. In filtered modes, production_functions is pruned to offered
functions and legal_units/legal_buildings are reconstructed from the remaining
typed production mappings.

This incorporates the translator invariants learned during the reviewed V8 V1/V2
coherence repairs instead of recreating the old incoherent intermediate state.

No model, host validator, game runtime, service, process, network, training,
deployment, VOID-chain, wallet, signer, transaction, or funds backend is called.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Mapping, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_proposal_generation2
    as proposal,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_proposal_source_binding_review_generation2
    as proposal_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-policy-contract.v1"
)

PROPOSAL_REVIEW_GIT_BLOB = "b13b8dd67062f75a1b324106366f11ac01b7ac8a"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
BASELINE_POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_policy_implementation_review"
)


class Pair06V9StrictVisibleContactPolicyHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactPolicyHold(message)


@lru_cache(maxsize=1)
def _validated_proposal_review() -> dict[str, Any]:
    out = (
        proposal_review
        .pair06_v9_strict_visible_contact_policy_proposal_review_contract()
    )
    _require(
        out.get("pair06_v9_strict_visible_contact_policy_proposal_reviewed")
        is True,
        "V9 strict-contact proposal review missing",
    )
    _require(out.get("policy_id") == POLICY_ID, "V9 policy id drift")
    _require(
        out.get("baseline_policy_id") == BASELINE_POLICY_ID,
        "V9 baseline policy id drift",
    )
    _require(
        out.get("recovery_mode_changed") is False
        and out.get("normal_mode_changed") is False
        and out.get("visible_contact_mode_changed") is True,
        "V9 intervention boundary drift",
    )
    _require(
        out.get("reinforcement_tools_allowed_during_strict_visible_contact")
        is False,
        "V9 proposal still permits visible-contact reinforcement choices",
    )
    _require(
        out.get("causal_claim_made") is False
        and out.get("action_level_causal_attribution_available") is False,
        "V9 proposal review overclaims causal evidence",
    )
    _require(
        out.get("implementation_present") is False
        and out.get("runtime_integration_present") is False
        and out.get("new_execution_request_opened") is False,
        "V9 proposal review crossed implementation boundary",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_REQUIRED",
        "V9 implementation frontier drift",
    )
    return deepcopy(out)


def _tool_name(tool: Mapping[str, Any]) -> str:
    function = tool.get("function")
    _require(isinstance(function, Mapping), "typed tool function missing")
    name = function.get("name")
    _require(
        isinstance(name, str) and bool(name),
        "typed tool function name invalid",
    )
    return name


def _combat_count(state: Mapping[str, Any]) -> int:
    units = state.get("units_summary")
    _require(isinstance(units, list), "compact state units_summary missing")
    count = 0
    for row in units:
        _require(isinstance(row, Mapping), "compact state unit row invalid")
        if row.get("can_attack") is True:
            count += 1
    return count


def _visible_enemy_count(state: Mapping[str, Any]) -> int:
    enemies = state.get("enemy_summary")
    buildings = state.get("enemy_buildings_summary")
    _require(isinstance(enemies, list), "compact state enemy_summary missing")
    _require(
        isinstance(buildings, list),
        "compact state enemy_buildings_summary missing",
    )
    return len(enemies) + len(buildings)


def _typed_legality_sets(
    production_functions: Mapping[str, Any],
) -> tuple[set[str], set[str]]:
    buildings: set[str] = set()
    units: set[str] = set()
    for name, raw_action in production_functions.items():
        _require(
            isinstance(name, str) and bool(name),
            "production function name invalid",
        )
        _require(
            isinstance(raw_action, Mapping),
            "production function action invalid: " + name,
        )
        kind = raw_action.get("kind")
        _require(
            kind in {"build_and_place", "build_unit"},
            "production function kind invalid: " + name,
        )
        if kind == "build_and_place":
            value = raw_action.get("building_type")
            _require(
                isinstance(value, str) and bool(value),
                "production building type invalid: " + name,
            )
            buildings.add(value)
        else:
            value = raw_action.get("unit_type")
            _require(
                isinstance(value, str) and bool(value),
                "production unit type invalid: " + name,
            )
            units.add(value)
    return buildings, units


def apply_pair06_v9_strict_visible_contact_policy(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a coherent filtered copy of the current reviewed tool surface."""
    _validated_proposal_review()
    _require(isinstance(state, Mapping), "compact state must be mapping")
    _require(
        isinstance(typed_tools, Sequence)
        and not isinstance(typed_tools, (str, bytes)),
        "typed tools must be sequence",
    )
    _require(isinstance(tool_contract, Mapping), "tool contract must be mapping")

    original_contract = deepcopy(dict(tool_contract))
    copied_tools = deepcopy(list(typed_tools))
    copied_contract = deepcopy(original_contract)

    tool_names = [_tool_name(tool) for tool in copied_tools]
    _require(bool(tool_names), "typed tool list empty")
    _require(
        len(tool_names) == len(set(tool_names)),
        "typed tool names contain duplicates",
    )

    offered = copied_contract.get("offered_tool_names")
    _require(isinstance(offered, list), "offered_tool_names must be list")
    _require(
        all(isinstance(name, str) and bool(name) for name in offered),
        "offered_tool_names contains invalid entry",
    )
    _require(
        len(offered) == len(set(offered)),
        "offered_tool_names contains duplicates",
    )
    _require(
        tuple(offered) == tuple(tool_names),
        "typed tools and offered_tool_names order or membership disagree",
    )

    production = copied_contract.get("production_functions")
    legal_units = copied_contract.get("legal_units")
    legal_buildings = copied_contract.get("legal_buildings")
    _require(isinstance(production, Mapping), "production_functions missing")
    _require(
        isinstance(legal_units, list)
        and all(isinstance(value, str) and bool(value) for value in legal_units),
        "legal_units invalid",
    )
    _require(
        isinstance(legal_buildings, list)
        and all(
            isinstance(value, str) and bool(value)
            for value in legal_buildings
        ),
        "legal_buildings invalid",
    )
    _require(
        set(production) <= set(offered),
        "input production function escaped offered surface",
    )

    original_production = deepcopy(dict(production))
    original_legal_units = list(legal_units)
    original_legal_buildings = list(legal_buildings)

    original_mapped_buildings, original_mapped_units = _typed_legality_sets(
        original_production
    )
    _require(
        original_mapped_buildings <= set(original_legal_buildings),
        "input production building escaped legal_buildings",
    )
    _require(
        original_mapped_units <= set(original_legal_units),
        "input production unit escaped legal_units",
    )

    combat_count = _combat_count(state)
    visible_enemy_count = _visible_enemy_count(state)
    envelope = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=combat_count,
        visible_enemy_count=visible_enemy_count,
        offered_tool_names=offered,
    )
    mode = envelope["mode"]

    proposed_names = tuple(envelope["proposed_offered_tool_names"])
    proposed_set = set(proposed_names)
    _require(
        proposed_set <= set(offered),
        "V9 strict-contact envelope invented tool name",
    )

    filtered_tools = [
        deepcopy(tool)
        for tool in copied_tools
        if _tool_name(tool) in proposed_set
    ]
    filtered_names = tuple(_tool_name(tool) for tool in filtered_tools)
    _require(
        filtered_names == proposed_names,
        "filtered typed tools do not preserve proposed order",
    )
    _require(bool(filtered_tools), "V9 policy produced empty typed-tool surface")

    copied_contract["offered_tool_names"] = list(proposed_names)

    if mode == "NORMAL":
        _require(
            proposed_names == tuple(offered),
            "NORMAL mode changed offered surface",
        )
        _require(
            copied_contract == original_contract,
            "NORMAL mode changed tool contract",
        )
        filtered_production = original_production
        rebuilt_legal_buildings = original_legal_buildings
        rebuilt_legal_units = original_legal_units
    else:
        filtered_production = {
            name: deepcopy(action)
            for name, action in original_production.items()
            if name in proposed_set
        }
        _require(
            set(filtered_production) <= proposed_set,
            "filtered production function escaped offered surface",
        )
        mapped_buildings, mapped_units = _typed_legality_sets(
            filtered_production
        )
        rebuilt_legal_buildings = [
            value
            for value in original_legal_buildings
            if value in mapped_buildings
        ]
        rebuilt_legal_units = [
            value
            for value in original_legal_units
            if value in mapped_units
        ]
        _require(
            set(rebuilt_legal_buildings) == mapped_buildings,
            "legal building mapping remains incoherent",
        )
        _require(
            set(rebuilt_legal_units) == mapped_units,
            "legal unit mapping remains incoherent",
        )
        copied_contract["production_functions"] = filtered_production
        copied_contract["legal_buildings"] = rebuilt_legal_buildings
        copied_contract["legal_units"] = rebuilt_legal_units

    return {
        "policy_id": POLICY_ID,
        "baseline_policy_id": BASELINE_POLICY_ID,
        "mode": mode,
        "combat_count": combat_count,
        "visible_enemy_count": visible_enemy_count,
        "original_offered_tool_names": tuple(offered),
        "filtered_offered_tool_names": proposed_names,
        "suppressed_tool_names": tuple(
            name for name in offered if name not in proposed_set
        ),
        "reinforcement_tools_suppressed": tuple(
            envelope["reinforcement_tools_suppressed"]
        ),
        "original_production_function_names": tuple(original_production),
        "filtered_production_function_names": tuple(filtered_production),
        "suppressed_production_function_names": tuple(
            name for name in original_production
            if name not in filtered_production
        ),
        "mapped_legal_buildings": tuple(rebuilt_legal_buildings),
        "mapped_legal_units": tuple(rebuilt_legal_units),
        "production_functions_filtered_to_offered_surface": True,
        "translator_legal_building_mapping_coherent": True,
        "translator_legal_unit_mapping_coherent": True,
        "legal_buildings_reconstructed_from_remaining_production": (
            mode != "NORMAL"
        ),
        "legal_units_reconstructed_from_remaining_production": (
            mode != "NORMAL"
        ),
        "normal_mode_contract_identity_preserved": mode != "NORMAL" or (
            copied_contract == original_contract
        ),
        "typed_tools": filtered_tools,
        "tool_contract": copied_contract,
        "host_validation_changed": False,
        "world_state_changed": False,
        "model_called": False,
        "model_weights_changed": False,
    }


def pair06_v9_strict_visible_contact_policy_contract() -> dict[str, Any]:
    reviewed = _validated_proposal_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "proposal_review_git_blob": PROPOSAL_REVIEW_GIT_BLOB,
        "policy_id": POLICY_ID,
        "baseline_policy_id": BASELINE_POLICY_ID,
        "pair06_v9_strict_visible_contact_policy_implemented": True,
        "pair06_v9_strict_visible_contact_policy_reviewed": False,
        "implementation_layer": "pure_pre_inference_coherent_tool_surface_transform",
        "recovery_mode_shape_preserved": True,
        "normal_mode_identity_preserved": True,
        "strict_visible_contact_reinforcement_suppressed": True,
        "strict_visible_contact_engagement_and_controls_only": True,
        "input_state_is_read_only": True,
        "input_typed_tools_are_deep_copied": True,
        "input_tool_contract_is_deep_copied": True,
        "tool_definitions_are_filtered_not_rewritten": True,
        "offered_tool_names_order_and_membership_match_filtered_tools": True,
        "production_functions_filtered_to_offered_surface": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_invariant_required": True,
        "translator_legal_unit_mapping_invariant_required": True,
        "normal_mode_contract_identity_required": True,
        "v8_v1_v2_coherence_invariants_incorporated": True,
        "host_validation_unchanged": True,
        "runtime_integration_implemented": False,
        "model_call_implemented": False,
        "host_command_implemented": False,
        "game_execution_implemented": False,
        "new_execution_request_opened": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_proposal": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactPolicyHold(NEXT_GATE)
