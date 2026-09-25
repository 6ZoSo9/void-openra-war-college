"""Pure implementation of the reviewed pair-06 V8 combat-priority envelope.

This module implements only a deterministic transformation of the current
pre-inference typed-tool surface. It does not call the model, host validator,
game runtime, services, network, training, deployment, chain, wallet, or funds.

Inputs:
- current compact Apollyon state;
- current reviewed typed tool definitions;
- current reviewed tool contract.

Output:
- a deep-copied filtered typed-tool list;
- a deep-copied tool contract whose offered_tool_names matches that list;
- an audit record describing the selected priority mode.

The underlying production_functions, legal_units, legal_buildings, and all
host-validation semantics remain unchanged. Suppressed functions remain
unavailable to model selection because offered_tool_names is narrowed to the
same exact names as the filtered tool definitions.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Mapping, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_proposal_generation2
    as proposal,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_proposal_source_binding_review_generation2
    as proposal_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-policy-contract.v1"
)

PROPOSAL_REVIEW_MAIN_HEAD = "f58ecb5d06cfa92f2b179cfabae54731f6b18d68"
PROPOSAL_REVIEW_GIT_BLOB = "1f1de1d167efd116b3f3dbce40ea51793cf41d03"
PROPOSAL_REVIEW_SOURCE_SHA256 = (
    "719265a4be84a25d5552179b89b2c0c2fcbe10c8912e7c11d193afedffae29fc"
)
PROPOSAL_REVIEW_TEST_GIT_BLOB = (
    "6c15a27f7fcedb6cd113b4adb137f1234981e0a7"
)
PROPOSAL_REVIEW_TEST_SHA256 = (
    "73631539ea096b80b30d5637c6c686dff2d531e5b54409184ddeef4a9fb2ab7d"
)

POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_policy_implementation_review"
)


class Pair06V8CombatActionPriorityPolicyHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityPolicyHold(message)


@lru_cache(maxsize=1)
def _validated_proposal_review() -> dict[str, Any]:
    out = (
        proposal_review
        .pair06_v8_combat_action_priority_policy_proposal_review_contract()
    )
    _require(
        out.get("pair06_v8_combat_action_priority_policy_proposal_reviewed")
        is True,
        "pair06 combat-priority proposal not reviewed",
    )
    _require(out.get("policy_id") == POLICY_ID, "pair06 policy id drift")
    _require(
        out.get("intervention_layer")
        == "pre_inference_current_tool_surface",
        "pair06 intervention layer drift",
    )
    for field in (
        "host_validation_must_remain_unchanged",
        "six_attempt_fail_closed_retry_must_remain_unchanged",
        "frozen_world_state_across_rejected_attempts_must_remain_unchanged",
        "typed_production_legality_must_remain_unchanged",
        "normal_mode_surface_must_remain_unchanged",
    ):
        _require(
            out.get(field) is True,
            "pair06 proposal-review invariant drift: " + field,
        )
    _require(
        out.get("implementation_present") is False,
        "pair06 proposal review unexpectedly includes implementation",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_REQUIRED",
        "pair06 implementation frontier drift",
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


def apply_pair06_v8_combat_action_priority_policy(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a filtered copy of the current typed-tool surface."""
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
        set(offered) == set(tool_names),
        "typed tools and offered_tool_names disagree",
    )

    combat_count = _combat_count(state)
    visible_enemy_count = _visible_enemy_count(state)
    envelope = proposal.proposed_priority_envelope(
        combat_count=combat_count,
        visible_enemy_count=visible_enemy_count,
        offered_tool_names=offered,
    )

    proposed_names = tuple(envelope["proposed_offered_tool_names"])
    proposed_set = set(proposed_names)
    _require(
        proposed_set <= set(offered),
        "priority envelope invented tool name",
    )

    filtered_tools = [
        deepcopy(tool)
        for tool in copied_tools
        if _tool_name(tool) in proposed_set
    ]
    filtered_names = [_tool_name(tool) for tool in filtered_tools]

    _require(bool(filtered_tools), "priority envelope produced empty tool list")
    _require(
        set(filtered_names) == proposed_set,
        "filtered typed tools do not match proposed names",
    )

    copied_contract["offered_tool_names"] = list(proposed_names)

    production_functions = copied_contract.get("production_functions")
    if production_functions is not None:
        _require(
            isinstance(production_functions, Mapping),
            "production_functions must be mapping",
        )

    return {
        "policy_id": POLICY_ID,
        "mode": envelope["mode"],
        "combat_count": combat_count,
        "visible_enemy_count": visible_enemy_count,
        "original_offered_tool_names": tuple(offered),
        "filtered_offered_tool_names": proposed_names,
        "suppressed_tool_names": tuple(
            name for name in offered if name not in proposed_set
        ),
        "typed_tools": filtered_tools,
        "tool_contract": copied_contract,
        "host_validation_changed": False,
        "world_state_changed": False,
        "model_called": False,
        "model_weights_changed": False,
    }


def pair06_v8_combat_action_priority_policy_contract() -> dict[str, Any]:
    reviewed = _validated_proposal_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "proposal_review_main_head": PROPOSAL_REVIEW_MAIN_HEAD,
        "proposal_review_git_blob": PROPOSAL_REVIEW_GIT_BLOB,
        "proposal_review_source_sha256": PROPOSAL_REVIEW_SOURCE_SHA256,
        "proposal_review_test_git_blob": PROPOSAL_REVIEW_TEST_GIT_BLOB,
        "proposal_review_test_sha256": PROPOSAL_REVIEW_TEST_SHA256,
        "policy_id": POLICY_ID,
        "pair06_v8_combat_action_priority_policy_implemented": True,
        "pair06_v8_combat_action_priority_policy_reviewed": False,
        "implementation_layer": "pure_pre_inference_tool_surface_transform",
        "input_state_is_read_only": True,
        "input_typed_tools_are_deep_copied": True,
        "input_tool_contract_is_deep_copied": True,
        "tool_definitions_are_filtered_not_rewritten": True,
        "offered_tool_names_matches_filtered_tools_required": True,
        "production_function_mapping_preserved": True,
        "host_validation_unchanged": True,
        "six_attempt_fail_closed_retry_unchanged": True,
        "frozen_world_state_across_rejected_attempts_unchanged": True,
        "typed_production_legality_unchanged": True,
        "normal_mode_surface_identity_required": True,
        "runtime_integration_implemented": False,
        "model_call_implemented": False,
        "host_command_implemented": False,
        "game_execution_implemented": False,
        "policy_activation_authorized": False,
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
    raise Pair06V8CombatActionPriorityPolicyHold(NEXT_GATE)
