"""Exact-blob source review for the pair-06 V9 strict-contact implementation.

This review pins the pure implementation and its regression tests to repository
bytes and verifies that the implementation preserves the reviewed V9 proposal
boundary. It grants no runtime activation, execution, replay, training,
promotion, deployment, chain, wallet, transaction, or funds authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_generation2
    as policy,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-policy-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "79ff26904ded459117cd0731744d72396c303a1d"
IMPLEMENTATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_policy_generation2.py"
)
IMPLEMENTATION_GIT_BLOB = "a3ab21dad67471dd2ff69281b549a1f64035af1e"
IMPLEMENTATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_policy_generation2.py"
)
IMPLEMENTATION_TEST_GIT_BLOB = "c94e389216ba2121f9447ec94cd5e7f0dfa0fccb"

NEXT_GATE = "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_RUNTIME_INTEGRATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_runtime_integration"
)


class Pair06V9StrictVisibleContactPolicyReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactPolicyReviewHold(message)


def pair06_v9_strict_visible_contact_policy_review_contract() -> dict[str, Any]:
    candidate = policy.pair06_v9_strict_visible_contact_policy_contract()

    _require(
        candidate.get("pair06_v9_strict_visible_contact_policy_implemented")
        is True,
        "V9 strict-contact implementation missing",
    )
    _require(
        candidate.get("pair06_v9_strict_visible_contact_policy_reviewed")
        is False,
        "V9 implementation unexpectedly self-reviewed",
    )
    _require(
        candidate.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 policy id drift",
    )
    _require(
        candidate.get("baseline_policy_id")
        == "pair06-v8-combat-action-priority-envelope-v1",
        "V9 baseline policy id drift",
    )
    _require(
        candidate.get("implementation_layer")
        == "pure_pre_inference_tool_surface_transform",
        "V9 implementation layer drift",
    )

    for field in (
        "recovery_mode_shape_preserved",
        "normal_mode_identity_preserved",
        "strict_visible_contact_reinforcement_suppressed",
        "strict_visible_contact_engagement_and_controls_only",
        "input_state_is_read_only",
        "input_typed_tools_are_deep_copied",
        "input_tool_contract_is_deep_copied",
        "tool_definitions_are_filtered_not_rewritten",
        "offered_tool_names_order_and_membership_match_filtered_tools",
        "production_function_mapping_preserved",
        "legal_units_preserved",
        "legal_buildings_preserved",
        "host_validation_unchanged",
    ):
        _require(
            candidate.get(field) is True,
            "V9 implementation invariant drift: " + field,
        )

    for field in (
        "runtime_integration_implemented",
        "model_call_implemented",
        "host_command_implemented",
        "game_execution_implemented",
        "new_execution_request_opened",
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
        _require(
            candidate.get(field) is False,
            "V9 implementation boundary drift: " + field,
        )

    _require(
        candidate.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 implementation review frontier drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "implementation_path": IMPLEMENTATION_PATH,
        "implementation_git_blob": IMPLEMENTATION_GIT_BLOB,
        "implementation_test_path": IMPLEMENTATION_TEST_PATH,
        "implementation_test_git_blob": IMPLEMENTATION_TEST_GIT_BLOB,
        "pair06_v9_strict_visible_contact_policy_reviewed": True,
        "policy_id": candidate["policy_id"],
        "baseline_policy_id": candidate["baseline_policy_id"],
        "implementation_layer": candidate["implementation_layer"],
        "recovery_mode_shape_preserved": True,
        "normal_mode_identity_preserved": True,
        "strict_visible_contact_reinforcement_suppressed": True,
        "strict_visible_contact_engagement_and_controls_only": True,
        "host_validation_unchanged": True,
        "runtime_integration_implemented": False,
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
        "validated_policy": deepcopy(candidate),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactPolicyReviewHold(NEXT_GATE)
