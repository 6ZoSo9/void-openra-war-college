"""Source-only acceptance of the read-only Precision pair-06 V8 action-availability audit.

The observation proves, for this exact completed trajectory, that:
* every engagement-relevant decision round had at least one legal engagement
  action in the exact offered tool surface; and
* every zero-combat recovery round had at least one typed train_unit_* recovery
  action in the exact offered tool surface.

This establishes available-but-not-chosen at the action-selection layer for the
observed run. It does not by itself identify whether model preference, prompt
framing, learned policy, reward shaping, or another upstream mechanism caused
that selection behavior.

No policy mutation, replay, runtime execution, training, corpus admission,
weight update, promotion, deployment, VOID-chain mutation, or wallet/funds
action is authorized.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_availability_audit_generation2
    as audit,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-availability-observation-acceptance-contract.v1"
)

AUDIT_MAIN_HEAD = "e6f95851026dfdbca4bfa60572f086bdc9d65ba1"
AUDIT_GIT_BLOB = "4f5a9797e8aea5c4aa960d63d524eac2237603d4"
AUDIT_SOURCE_SHA256 = (
    "a4fa1aff1666bc7d566cad8f31ac24817aee36e7cc2deb8f43ad8ee5b3f03a34"
)
AUDIT_TEST_GIT_BLOB = "feaff472592dbcfc01290242ebe86ca4c2390029"
AUDIT_TEST_SHA256 = (
    "c45d54744c500a0b25de31b19ef62f57d7795c68f4b5c0ea14d8624a02e50c91"
)

TRAJECTORY_SHA256 = (
    "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
)
TRAJECTORY_BYTES = 386881

OBSERVATION_TERMINAL_SHA256 = (
    "79841b3174bab1b8b4a5eccc764c470237736c8c759a04bc362d086b749b3f47"
)
OBSERVATION_TERMINAL_BYTES = 25319

RECOVERY_RELEVANT_ROUNDS = tuple(range(8, 37))
RECOVERY_AVAILABLE_ROUNDS = tuple(range(8, 37))
RECOVERY_UNAVAILABLE_ROUNDS: tuple[int, ...] = ()

ENGAGEMENT_RELEVANT_ROUNDS = (3, 4, 5, 6, 7)
ENGAGEMENT_AVAILABLE_ROUNDS = (3, 4, 5, 6, 7)
ENGAGEMENT_UNAVAILABLE_ROUNDS: tuple[int, ...] = ()

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_combat_action_priority_policy_proposal"


class Pair06V8CombatActionAvailabilityObservationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionAvailabilityObservationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _validated_audit_contract() -> dict[str, Any]:
    out = audit.pair06_v8_combat_action_availability_audit_contract()
    _require(
        out.get("trajectory_sha256") == TRAJECTORY_SHA256,
        "pair06 trajectory identity drift",
    )
    _require(
        out.get("expected_rounds") == 36,
        "pair06 round cardinality drift",
    )
    _require(
        out.get("trajectory_persists_exact_tool_contract") is True
        and out.get("offered_tool_names_audited_per_round") is True
        and out.get("typed_legal_units_audited_per_round") is True,
        "pair06 audit evidence surface drift",
    )
    _require(
        out.get("policy_change_authorized") is False
        and out.get("runtime_execution_authorized") is False
        and out.get("replay_authorized") is False
        and out.get("training_authorized") is False,
        "pair06 audit unexpectedly grants authority",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_PRECISION_OBSERVATION_REQUIRED",
        "pair06 observation frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_availability_observation_acceptance_contract() -> dict[str, Any]:
    validated = _validated_audit_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "audit_main_head": AUDIT_MAIN_HEAD,
        "audit_git_blob": AUDIT_GIT_BLOB,
        "audit_source_sha256": AUDIT_SOURCE_SHA256,
        "audit_test_git_blob": AUDIT_TEST_GIT_BLOB,
        "audit_test_sha256": AUDIT_TEST_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "trajectory_bytes": TRAJECTORY_BYTES,
        "observation_terminal_sha256": OBSERVATION_TERMINAL_SHA256,
        "observation_terminal_bytes": OBSERVATION_TERMINAL_BYTES,
        "availability_audit_result_green": True,
        "round_count": 36,
        "combat_recovery_relevant_rounds": RECOVERY_RELEVANT_ROUNDS,
        "combat_recovery_available_rounds": RECOVERY_AVAILABLE_ROUNDS,
        "combat_recovery_unavailable_rounds": RECOVERY_UNAVAILABLE_ROUNDS,
        "engagement_relevant_rounds": ENGAGEMENT_RELEVANT_ROUNDS,
        "engagement_available_rounds": ENGAGEMENT_AVAILABLE_ROUNDS,
        "engagement_unavailable_rounds": ENGAGEMENT_UNAVAILABLE_ROUNDS,
        "all_recovery_relevant_rounds_had_recovery_tool": True,
        "all_engagement_relevant_rounds_had_engagement_tool": True,
        "ranking_cause_supported_by_availability": True,
        "action_selection_layer_available_but_not_chosen_proven": True,
        "upstream_model_preference_cause_proven": False,
        "prompt_framing_cause_proven": False,
        "learned_policy_cause_proven": False,
        "reward_shaping_cause_proven": False,
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
        "validated_audit_contract": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def change_policy_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionAvailabilityObservationAcceptanceHold(NEXT_GATE)
