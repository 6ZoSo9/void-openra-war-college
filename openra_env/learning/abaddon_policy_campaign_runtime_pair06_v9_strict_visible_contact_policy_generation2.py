"""Pure implementation of the reviewed pair-06 V9 strict-contact envelope.

This module implements only a deterministic transform of the current
pre-inference typed-tool surface. It derives combat/contact counts from the
current compact state, calls the reviewed V9 proposal transform, filters copies
of the currently offered typed tools, and updates only offered_tool_names in a
copied tool contract.

RECOVERY remains recovery-only production. NORMAL remains the exact current
surface. STRICT_VISIBLE_CONTACT removes train_unit_*, advance, and structure
growth choices, retaining only currently offered engagement and tactical-control
functions.

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


def apply_pair06_v9_strict_visible_contact_policy(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a filtered copy of the current reviewed typed-tool surface."""
    _validated_proposal_review()
    _require(isinstance(state, Mapping), "compact state must be mapping")
    _require(
        isinstance(typed_tools, Sequence)
        and not isinstance(typed_tools, (str, bytes)),
        "typed tools must be sequence",
    )
    _require(
        isinstance(tool_contract, Mapping),
        "tool contract must be mapping",
    )

    copied_tools = deepcopy(list(typed_tools))
    copied_contract = deepcopy(dict(tool_contract))

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

    combat_count = _combat_count(state)
    visible_enemy_count = _visible_enemy_count(state)
    envelope = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=combat_count,
        visible_enemy_count=visible_enemy_count,
        offered_tool_names=offered,
    )

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

    for field in ("production_functions", "legal_units", "legal_buildings"):
        _require(
            copied_contract.get(field) == tool_contract.get(field),
            "V9 policy changed typed legality field: " + field,
        )

    return {
        "policy_id": POLICY_ID,
        "baseline_policy_id": BASELINE_POLICY_ID,
        "mode": envelope["mode"],
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
        "implementation_layer": "pure_pre_inference_tool_surface_transform",
        "recovery_mode_shape_preserved": True,
        "normal_mode_identity_preserved": True,
        "strict_visible_contact_reinforcement_suppressed": True,
        "strict_visible_contact_engagement_and_controls_only": True,
        "input_state_is_read_only": True,
        "input_typed_tools_are_deep_copied": True,
        "input_tool_contract_is_deep_copied": True,
        "tool_definitions_are_filtered_not_rewritten": True,
        "offered_tool_names_order_and_membership_match_filtered_tools": True,
        "production_function_mapping_preserved": True,
        "legal_units_preserved": True,
        "legal_buildings_preserved": True,
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
