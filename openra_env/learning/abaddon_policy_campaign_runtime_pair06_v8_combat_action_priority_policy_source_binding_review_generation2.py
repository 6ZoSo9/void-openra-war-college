"""Source-only review of the pure pair-06 V8 combat-priority policy implementation.

Pins the exact implementation source/tests and validates that the module remains
pure and non-integrated. This review grants no runtime execution, replay,
training, promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_generation2
    as policy,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-policy-review-contract.v1"
)

IMPLEMENTATION_MAIN_HEAD = "e8961c6096e4e0971582ca7c576182a5339156d1"
IMPLEMENTATION_GIT_BLOB = "15cef31b57c4402e151053086e38c76c3226bd1d"
IMPLEMENTATION_SOURCE_SHA256 = (
    "856f3391eb705998bcfeacb738ab7355c1a42581e64232c07be42ff2cc60f8b0"
)
IMPLEMENTATION_TEST_GIT_BLOB = (
    "4a7b778bf9cd95604afa321dfafaabbda6269c70"
)
IMPLEMENTATION_TEST_SHA256 = (
    "1025ca0ab48cac27504f769fceb3a2b6b3bfd6338d78af0df5404b94912e2e63"
)

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_combat_action_priority_runtime_integration"


class Pair06V8CombatActionPriorityPolicyReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityPolicyReviewHold(message)


@lru_cache(maxsize=1)
def _validated_policy() -> dict[str, Any]:
    out = policy.pair06_v8_combat_action_priority_policy_contract()

    _require(
        out.get("pair06_v8_combat_action_priority_policy_implemented") is True,
        "pair06 combat-priority policy implementation missing",
    )
    _require(
        out.get("pair06_v8_combat_action_priority_policy_reviewed") is False,
        "pair06 combat-priority implementation unexpectedly self-reviewed",
    )
    _require(
        out.get("implementation_layer")
        == "pure_pre_inference_tool_surface_transform",
        "pair06 policy implementation layer drift",
    )

    for field in (
        "input_state_is_read_only",
        "input_typed_tools_are_deep_copied",
        "input_tool_contract_is_deep_copied",
        "tool_definitions_are_filtered_not_rewritten",
        "offered_tool_names_matches_filtered_tools_required",
        "production_function_mapping_preserved",
        "host_validation_unchanged",
        "six_attempt_fail_closed_retry_unchanged",
        "frozen_world_state_across_rejected_attempts_unchanged",
        "typed_production_legality_unchanged",
        "normal_mode_surface_identity_required",
    ):
        _require(out.get(field) is True, "pair06 implementation invariant drift: " + field)

    for field in (
        "runtime_integration_implemented",
        "model_call_implemented",
        "host_command_implemented",
        "game_execution_implemented",
        "policy_activation_authorized",
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
        _require(out.get(field) is False, "pair06 implementation boundary drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_IMPLEMENTATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "pair06 implementation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_policy_review_contract() -> dict[str, Any]:
    validated = _validated_policy()
    return {
        "schema": CONTRACT_SCHEMA,
        "implementation_main_head": IMPLEMENTATION_MAIN_HEAD,
        "implementation_git_blob": IMPLEMENTATION_GIT_BLOB,
        "implementation_source_sha256": IMPLEMENTATION_SOURCE_SHA256,
        "implementation_test_git_blob": IMPLEMENTATION_TEST_GIT_BLOB,
        "implementation_test_sha256": IMPLEMENTATION_TEST_SHA256,
        "pair06_v8_combat_action_priority_policy_reviewed": True,
        "policy_id": validated["policy_id"],
        "implementation_layer": validated["implementation_layer"],
        "runtime_integration_implemented": False,
        "model_call_implemented": False,
        "host_command_implemented": False,
        "game_execution_implemented": False,
        "policy_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_policy": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityPolicyReviewHold(NEXT_GATE)
