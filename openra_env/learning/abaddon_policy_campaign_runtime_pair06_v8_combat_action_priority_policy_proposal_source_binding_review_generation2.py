"""Source-only review of the pair-06 V8 combat-action priority policy proposal.

Pins the exact proposal source and tests after the GREEN policy-proposal PR.
This review authorizes no implementation, replay, runtime execution, training,
promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_proposal_generation2
    as proposal,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-policy-proposal-review-contract.v1"
)

PROPOSAL_MAIN_HEAD = "46dd688fca16235a847ab9b9165b800606b6b9d0"
PROPOSAL_GIT_BLOB = "f230f77c5b78e47b5d8872870f5c87a040861c15"
PROPOSAL_SOURCE_SHA256 = (
    "937da96c490e658f5fce7847e27bfb6833c01fff82a92aa222657297eda6d291"
)
PROPOSAL_TEST_GIT_BLOB = "e81a3faf32143425baf9c81c31b931140d40258c"
PROPOSAL_TEST_SHA256 = (
    "cebe7a3f27786d2a6b9fbebf5d5031a1b09d4a51f00e8a51b003baf67ffad42c"
)

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_combat_action_priority_policy_implementation"


class Pair06V8CombatActionPriorityPolicyProposalReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityPolicyProposalReviewHold(message)


@lru_cache(maxsize=1)
def _validated_proposal() -> dict[str, Any]:
    out = proposal.pair06_v8_combat_action_priority_policy_proposal_contract()

    _require(
        out.get("policy_id") == "pair06-v8-combat-action-priority-envelope-v1",
        "pair06 policy id drift",
    )
    _require(
        out.get("evidence_available_but_not_chosen") is True,
        "pair06 proposal evidence drift",
    )
    _require(
        out.get("intervention_layer") == "pre_inference_current_tool_surface",
        "pair06 intervention layer drift",
    )
    _require(
        out.get("recovery_surface")
        == "only_currently_offered_train_unit_functions",
        "pair06 recovery surface drift",
    )
    _require(
        out.get("visible_contact_surface")
        == "current_engagement_plus_tactical_control_plus_train_unit_functions",
        "pair06 visible-contact surface drift",
    )
    _require(
        out.get("normal_surface")
        == "exact_current_reviewed_offered_tool_surface",
        "pair06 normal surface drift",
    )
    for field in (
        "bare_advance_suppressed_in_recovery_mode",
        "bare_advance_suppressed_in_visible_contact_mode",
        "structure_growth_suppressed_in_recovery_mode",
        "structure_growth_suppressed_in_visible_contact_mode",
        "host_validation_must_remain_unchanged",
        "six_attempt_fail_closed_retry_must_remain_unchanged",
        "frozen_world_state_across_rejected_attempts_must_remain_unchanged",
        "typed_production_legality_must_remain_unchanged",
        "normal_mode_surface_must_remain_unchanged",
        "implementation_required_before_effect",
    ):
        _require(out.get(field) is True, "pair06 proposal invariant drift: " + field)

    _require(out.get("implementation_present") is False, "implementation present too early")
    for field in (
        "policy_change_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(out.get(field) is False, "pair06 proposal authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "pair06 proposal review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_policy_proposal_review_contract() -> dict[str, Any]:
    validated = _validated_proposal()
    return {
        "schema": CONTRACT_SCHEMA,
        "proposal_main_head": PROPOSAL_MAIN_HEAD,
        "proposal_git_blob": PROPOSAL_GIT_BLOB,
        "proposal_source_sha256": PROPOSAL_SOURCE_SHA256,
        "proposal_test_git_blob": PROPOSAL_TEST_GIT_BLOB,
        "proposal_test_sha256": PROPOSAL_TEST_SHA256,
        "pair06_v8_combat_action_priority_policy_proposal_reviewed": True,
        "policy_id": validated["policy_id"],
        "intervention_layer": validated["intervention_layer"],
        "recovery_surface": validated["recovery_surface"],
        "visible_contact_surface": validated["visible_contact_surface"],
        "normal_surface": validated["normal_surface"],
        "host_validation_must_remain_unchanged": True,
        "six_attempt_fail_closed_retry_must_remain_unchanged": True,
        "frozen_world_state_across_rejected_attempts_must_remain_unchanged": True,
        "typed_production_legality_must_remain_unchanged": True,
        "normal_mode_surface_must_remain_unchanged": True,
        "implementation_present": False,
        "policy_change_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_proposal": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def implement_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityPolicyProposalReviewHold(NEXT_GATE)
