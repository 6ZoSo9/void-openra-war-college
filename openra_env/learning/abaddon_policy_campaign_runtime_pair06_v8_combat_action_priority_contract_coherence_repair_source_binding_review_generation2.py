"""Source-only review of the pair-06 combat-priority contract repair.

Pins the exact repair source/tests merged after the consumed failed attempt.
This review grants no retry or runtime authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_generation2
    as repair,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-review.v1"
)

REPAIR_MAIN_HEAD = "72104294537bc8450a1505b643914dc503b83845"
REPAIR_GIT_BLOB = "fee7f07791d01594bf7f31b8cd8e24c8eb6fbed3"
REPAIR_SOURCE_SHA256 = (
    "cd951c4cbfe6014e1dc2412b1f52b5beda552cf89e77846a5af176b2278b81f6"
)
REPAIR_TEST_GIT_BLOB = "d107a944897a461abb479ba47bed88155d3bedae"
REPAIR_TEST_SHA256 = (
    "1d910f6cfd88c72ca362251f47bbb848bb7a159773d1a42874b2e84c5a46f8ac"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "PROTO_CHILD_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_proto_child_wiring"
)


class Pair06V8CombatPriorityContractCoherenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityContractCoherenceReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = repair.pair06_v8_combat_action_priority_contract_coherence_repair_contract()

    _require(out.get("repair_implemented") is True, "coherence repair missing")
    _require(
        out.get("repair_layer")
        == "pure_policy_output_plus_scoped_decision_hook_adapter",
        "coherence repair layer drift",
    )
    for field in (
        "production_functions_filtered_to_offered_surface",
        "legal_units_preserved",
        "legal_buildings_preserved",
        "normal_mode_production_mapping_identity_required",
        "scoped_policy_function_substitution_implemented",
        "policy_function_restored_in_finally",
        "translator_production_function_subset_invariant_required",
    ):
        _require(out.get(field) is True, "coherence repair invariant drift: " + field)

    _require(
        out.get("historical_policy_source_modified") is False
        and out.get("historical_runtime_integration_source_modified") is False,
        "historical reviewed source unexpectedly modified",
    )

    for field in (
        "attempt_retry_authorized",
        "runtime_activation_authorized",
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
        _require(out.get(field) is False, "coherence repair authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "coherence repair review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_contract_coherence_repair_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_main_head": REPAIR_MAIN_HEAD,
        "repair_git_blob": REPAIR_GIT_BLOB,
        "repair_source_sha256": REPAIR_SOURCE_SHA256,
        "repair_test_git_blob": REPAIR_TEST_GIT_BLOB,
        "repair_test_sha256": REPAIR_TEST_SHA256,
        "pair06_v8_combat_action_priority_contract_coherence_repair_reviewed": True,
        "production_functions_filtered_to_offered_surface": True,
        "legal_units_preserved": True,
        "legal_buildings_preserved": True,
        "normal_mode_production_mapping_identity_required": True,
        "attempt_retry_authorized": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_repair": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityContractCoherenceReviewHold(NEXT_GATE)
