"""Source-only pair-06 V8 combat-action priority policy proposal.

Evidence from the exact reviewed trajectory establishes that relevant combat
actions were available but not chosen:
* engagement actions were available on every engagement-relevant round 3..7;
* typed train_unit_* recovery actions were available on every zero-combat
  recovery round 8..36.

This proposal defines a bounded pre-inference tool-surface envelope. It does not
implement or execute that envelope.

Proposed behavior:
1. RECOVERY mode:
   If own combat count is zero and at least one legal train_unit_* function is
   currently offered, expose only those recovery functions for that decision.
2. VISIBLE_CONTACT mode:
   If own combat count is positive, at least one enemy is visible, and at least
   one engagement function is currently offered, suppress bare advance and
   build_structure_* choices. Retain engagement functions, legal train_unit_*
   reinforcement functions, and existing tactical control functions.
3. NORMAL mode:
   Otherwise preserve the exact current reviewed offered tool surface.

The proposal changes only the tool surface presented to the model. Existing
host validation, six-attempt fail-closed retry behavior, frozen decision state,
typed production legality, and the game runner remain unchanged.

No implementation, replay, runtime execution, training, corpus admission,
weight update, promotion, deployment, VOID-chain mutation, or wallet/funds
action is authorized.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Iterable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_availability_observation_acceptance_generation2
    as availability,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-policy-proposal-contract.v1"
)

AVAILABILITY_ACCEPTANCE_MAIN_HEAD = (
    "71df31c3369f833bdcc4392cfd6749df3eb35896"
)
AVAILABILITY_ACCEPTANCE_GIT_BLOB = (
    "f4f535d039a7dc5c72c87713e8f78dd360b42fa0"
)
AVAILABILITY_ACCEPTANCE_SOURCE_SHA256 = (
    "55a82e91b327590a3b2300abdcf698c251ea9b3980dc036d828a27a77636b7ab"
)
AVAILABILITY_ACCEPTANCE_TEST_GIT_BLOB = (
    "4bf5a85f85a00fc098a0e6d90012930445d8c482"
)
AVAILABILITY_ACCEPTANCE_TEST_SHA256 = (
    "4a4c0bbc29f9948d82994477d3be8ff32762409ee4fd935d53a97dceaa43734e"
)

POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

RECOVERY_PREFIX = "train_unit_"
STRUCTURE_PREFIX = "build_structure_"

ENGAGEMENT_TOOLS = frozenset({
    "attack_target",
    "move_units",
    "attack_move",
})
TACTICAL_CONTROL_TOOLS = frozenset({
    "set_stance",
    "stop_units",
    "guard_target",
})

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_policy_proposal_review"
)


class Pair06V8CombatActionPriorityPolicyProposalHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityPolicyProposalHold(message)


@lru_cache(maxsize=1)
def _validated_availability() -> dict[str, Any]:
    out = (
        availability
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
    _require(
        out.get("availability_audit_result_green") is True,
        "pair06 availability observation not green",
    )
    _require(
        out.get("ranking_cause_supported_by_availability") is True,
        "pair06 availability does not support action-priority hypothesis",
    )
    _require(
        out.get("action_selection_layer_available_but_not_chosen_proven")
        is True,
        "pair06 available-but-not-chosen evidence missing",
    )
    _require(
        out.get("combat_recovery_unavailable_rounds") == (),
        "pair06 recovery action unavailable on relevant round",
    )
    _require(
        out.get("engagement_unavailable_rounds") == (),
        "pair06 engagement action unavailable on relevant round",
    )
    _require(
        out.get("policy_change_authorized") is False
        and out.get("runtime_execution_authorized") is False
        and out.get("training_authorized") is False,
        "pair06 observation unexpectedly grants authority",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_REQUIRED",
        "pair06 policy-proposal frontier drift",
    )
    return deepcopy(out)


def _names(values: Iterable[str]) -> tuple[str, ...]:
    names = tuple(values)
    _require(
        all(isinstance(name, str) and bool(name) for name in names),
        "tool name invalid",
    )
    _require(len(names) == len(set(names)), "duplicate offered tool name")
    return names


def proposed_priority_envelope(
    *,
    combat_count: int,
    visible_enemy_count: int,
    offered_tool_names: Iterable[str],
) -> dict[str, Any]:
    """Pure proposed surface transform; no host state or model calls."""
    _require(
        type(combat_count) is int and combat_count >= 0,
        "combat_count invalid",
    )
    _require(
        type(visible_enemy_count) is int and visible_enemy_count >= 0,
        "visible_enemy_count invalid",
    )
    offered = _names(offered_tool_names)
    offered_set = set(offered)

    recovery = tuple(
        name for name in offered if name.startswith(RECOVERY_PREFIX)
    )
    engagement = tuple(
        name for name in offered if name in ENGAGEMENT_TOOLS
    )
    tactical_controls = tuple(
        name for name in offered if name in TACTICAL_CONTROL_TOOLS
    )

    if combat_count == 0 and recovery:
        mode = "RECOVERY"
        proposed = recovery
        rationale = (
            "zero combat capacity with legal typed recovery actions available"
        )
    elif combat_count > 0 and visible_enemy_count > 0 and engagement:
        mode = "VISIBLE_CONTACT"
        proposed = tuple(
            name for name in offered
            if (
                name in ENGAGEMENT_TOOLS
                or name in TACTICAL_CONTROL_TOOLS
                or name.startswith(RECOVERY_PREFIX)
            )
        )
        rationale = (
            "visible enemy contact with legal engagement actions available"
        )
    else:
        mode = "NORMAL"
        proposed = offered
        rationale = "priority trigger absent"

    _require(bool(proposed), "proposed priority surface unexpectedly empty")
    _require(set(proposed) <= offered_set, "proposal invented tool name")

    return {
        "policy_id": POLICY_ID,
        "mode": mode,
        "rationale": rationale,
        "original_offered_tool_names": offered,
        "proposed_offered_tool_names": proposed,
        "recovery_tools": recovery,
        "engagement_tools": engagement,
        "tactical_control_tools": tactical_controls,
        "advance_suppressed": (
            "advance" in offered_set and "advance" not in set(proposed)
        ),
        "structure_tools_suppressed": tuple(
            name for name in offered
            if name.startswith(STRUCTURE_PREFIX)
            and name not in set(proposed)
        ),
        "host_validation_changed": False,
        "world_state_changed": False,
        "model_weights_changed": False,
    }


def pair06_v8_combat_action_priority_policy_proposal_contract() -> dict[str, Any]:
    evidence = _validated_availability()
    return {
        "schema": CONTRACT_SCHEMA,
        "policy_id": POLICY_ID,
        "availability_acceptance_main_head": (
            AVAILABILITY_ACCEPTANCE_MAIN_HEAD
        ),
        "availability_acceptance_git_blob": (
            AVAILABILITY_ACCEPTANCE_GIT_BLOB
        ),
        "availability_acceptance_source_sha256": (
            AVAILABILITY_ACCEPTANCE_SOURCE_SHA256
        ),
        "availability_acceptance_test_git_blob": (
            AVAILABILITY_ACCEPTANCE_TEST_GIT_BLOB
        ),
        "availability_acceptance_test_sha256": (
            AVAILABILITY_ACCEPTANCE_TEST_SHA256
        ),
        "evidence_available_but_not_chosen": True,
        "intervention_layer": "pre_inference_current_tool_surface",
        "recovery_trigger": (
            "combat_count==0 and one_or_more_train_unit_functions_offered"
        ),
        "recovery_surface": "only_currently_offered_train_unit_functions",
        "visible_contact_trigger": (
            "combat_count>0 and visible_enemy_count>0 "
            "and one_or_more_engagement_functions_offered"
        ),
        "visible_contact_surface": (
            "current_engagement_plus_tactical_control_plus_train_unit_functions"
        ),
        "normal_surface": "exact_current_reviewed_offered_tool_surface",
        "engagement_tools": tuple(sorted(ENGAGEMENT_TOOLS)),
        "tactical_control_tools": tuple(sorted(TACTICAL_CONTROL_TOOLS)),
        "recovery_tool_prefix": RECOVERY_PREFIX,
        "structure_tool_prefix": STRUCTURE_PREFIX,
        "bare_advance_suppressed_in_recovery_mode": True,
        "bare_advance_suppressed_in_visible_contact_mode": True,
        "structure_growth_suppressed_in_recovery_mode": True,
        "structure_growth_suppressed_in_visible_contact_mode": True,
        "host_validation_must_remain_unchanged": True,
        "six_attempt_fail_closed_retry_must_remain_unchanged": True,
        "frozen_world_state_across_rejected_attempts_must_remain_unchanged": True,
        "typed_production_legality_must_remain_unchanged": True,
        "normal_mode_surface_must_remain_unchanged": True,
        "implementation_required_before_effect": True,
        "implementation_present": False,
        "policy_change_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_availability": evidence,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def implement_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityPolicyProposalHold(NEXT_GATE)
