"""Source-only combat-action-priority hypothesis for pair-06 V8.

This module converts the accepted post-run diagnostic into a falsifiable
hypothesis, not a policy change.

Observed facts from the reviewed run:
- no Apollyon controller round required a rejected-tool retry;
- Apollyon selected 11 structure-build actions and 25 advance actions;
- no accepted Apollyon attack_target, move_units, or explicit unit-build action
  was observed;
- Apollyon's combat count fell from four to zero by round seven and remained
  zero through round 36.

Hypothesis:
If legal combat-recovery / engagement actions were actually available at the
decision points where Apollyon lost or lacked combat capacity, then the
controller's action-priority/ranking behavior underweighted combat utility
relative to infrastructure and bare advance.

This source does not assume those combat actions were available. A separate
availability audit is required before any policy proposal can treat ranking as
the supported causal mechanism.

No policy change, runtime execution, replay, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action is authorized.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_post_run_combat_utility_rejection_diagnostic_generation2
    as diagnostic,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-hypothesis-contract.v1"
)

DIAGNOSTIC_MAIN_HEAD = "f7d76da01e8bdd40f43aad91104252ecda4e97a7"
DIAGNOSTIC_GIT_BLOB = "1abb7add92d82a118f4357ce26e8af9bbfa20b1d"
DIAGNOSTIC_SOURCE_SHA256 = (
    "5ea3d91f538ca7826d8a8c1765211d5d8488b20507326f53028fbce394b77603"
)

HYPOTHESIS_ID = "pair06-v8-combat-action-priority-v1"

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_AUDIT_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_combat_action_availability_audit"


class Pair06V8CombatActionPriorityHypothesisHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityHypothesisHold(message)


@lru_cache(maxsize=1)
def _validated_diagnostic() -> dict[str, Any]:
    out = (
        diagnostic
        .pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    )

    _require(
        out.get("diagnostic_classification")
        == "combat_utility_action_mix_not_tool_rejection",
        "pair06 diagnostic classification drift",
    )
    _require(
        out.get("controller_rounds") == 36
        and out.get("apollyon_tool_contract_accepted_rounds") == 36
        and out.get("apollyon_total_tool_attempts") == 36
        and out.get("apollyon_rounds_requiring_tool_retry") == 0,
        "pair06 rejection diagnostic drift",
    )
    _require(
        out.get("tool_rejection_or_retry_failure_observed") is False
        and out.get("trace_supports_protocol_rejection_failure") is False,
        "pair06 rejection evidence drift",
    )
    _require(
        out.get("apollyon_structure_build_actions") == 11
        and out.get("apollyon_advance_actions") == 25
        and out.get("apollyon_explicit_attack_target_actions") == 0
        and out.get("apollyon_explicit_move_units_actions") == 0
        and out.get("apollyon_explicit_unit_build_actions") == 0,
        "pair06 action-mix diagnostic drift",
    )
    _require(
        out.get("apollyon_combat_count_at_controller_start") == 4
        and out.get("apollyon_combat_count_zero_round") == 7
        and out.get("apollyon_zero_combat_rounds_7_through_36") == 30
        and out.get("combat_counts_at_round_36") == (0, 6),
        "pair06 combat-collapse diagnostic drift",
    )
    _require(
        out.get("causal_root_cause_proven") is False
        and out.get("tool_availability_root_cause_proven") is False
        and out.get("policy_ranking_root_cause_proven") is False,
        "pair06 diagnostic unexpectedly proves cause",
    )
    _require(
        out.get("policy_change_authorized") is False
        and out.get("new_runtime_execution_authorized") is False
        and out.get("training_authorized") is False,
        "pair06 diagnostic unexpectedly grants authority",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_PRIORITY_HYPOTHESIS_REQUIRED",
        "pair06 hypothesis frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_hypothesis_contract() -> dict[str, Any]:
    observed = _validated_diagnostic()
    return {
        "schema": CONTRACT_SCHEMA,
        "hypothesis_id": HYPOTHESIS_ID,
        "diagnostic_main_head": DIAGNOSTIC_MAIN_HEAD,
        "diagnostic_git_blob": DIAGNOSTIC_GIT_BLOB,
        "diagnostic_source_sha256": DIAGNOSTIC_SOURCE_SHA256,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "observed_tool_rejection_or_retry_failure": False,
        "observed_controller_rounds": 36,
        "observed_apollyon_structure_build_actions": 11,
        "observed_apollyon_advance_actions": 25,
        "observed_apollyon_explicit_attack_target_actions": 0,
        "observed_apollyon_explicit_move_units_actions": 0,
        "observed_apollyon_explicit_unit_build_actions": 0,
        "observed_apollyon_combat_count_start": 4,
        "observed_apollyon_combat_count_zero_round": 7,
        "observed_apollyon_zero_combat_round_count": 30,
        "hypothesis_kind": "conditional_action_priority_ranking",
        "hypothesis_statement": (
            "if legal combat-recovery or engagement actions were available "
            "at the relevant decision points, Apollyon underweighted combat "
            "utility relative to infrastructure and bare advance"
        ),
        "combat_recovery_condition": (
            "own_combat_count_zero_or_depleted_and_legal_recovery_action_available"
        ),
        "combat_recovery_priority_hypothesis": (
            "prefer_legal_combat_capacity_recovery_over_nonessential_structure_or_bare_advance"
        ),
        "engagement_condition": (
            "own_combat_count_positive_and_enemy_visible_and_legal_engagement_action_available"
        ),
        "engagement_priority_hypothesis": (
            "prefer_legal_attack_or_contact_movement_over_nonessential_structure_or_bare_advance"
        ),
        "nonessential_structure_suppression_hypothesis": (
            "during_active_contact_or_combat_depletion_do_not_prioritize_nonessential_structure_growth"
        ),
        "availability_must_be_proven_before_ranking_cause": True,
        "tool_availability_currently_proven": False,
        "policy_ranking_cause_currently_proven": False,
        "reward_shaping_cause_currently_proven": False,
        "state_interpretation_cause_currently_proven": False,
        "falsification_if_relevant_combat_actions_unavailable": True,
        "falsification_if_availability_present_but_priority_change_does_not_improve_bounded_metrics": True,
        "availability_audit_required_before_policy_proposal": True,
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
        "validated_diagnostic": observed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def audit_or_change_policy(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityHypothesisHold(NEXT_GATE)
