"""Source-only repair for pair-06 combat-priority tool-contract coherence.

The original reviewed priority policy narrows offered_tool_names but keeps
the complete typed production_functions mapping. The V8 campaign translator
requires every production-function key to also be currently offered, so a
priority mode that suppresses structure production can otherwise fail closed
before inference with a production-function-not-offered error.

This repair preserves the historical policy and decision-hook modules
byte-for-byte. It wraps the reviewed pure policy, prunes only stale production
mapping entries from the filtered copy, and provides a decision-hook subclass
that scopes the repaired policy function to one decision call and restores the
historical function in finally.

No runtime activation, execution, retry, training, deployment, chain mutation,
or wallet/funds authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_generation2
    as base_policy,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_generation2
    as base_integration,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair.v1"
)

ORIGINAL_POLICY_APPLY = (
    base_policy.apply_pair06_v8_combat_action_priority_policy
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_repair_review"
)


class Pair06V8CombatPriorityContractCoherenceHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityContractCoherenceHold(message)


def apply_pair06_v8_combat_action_priority_contract_coherence_repair(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply the reviewed policy, then make its filtered contract self-consistent."""
    original_contract = deepcopy(dict(tool_contract))
    out = ORIGINAL_POLICY_APPLY(
        state=state,
        typed_tools=typed_tools,
        tool_contract=tool_contract,
    )
    _require(isinstance(out, Mapping), "priority policy result missing")

    repaired = deepcopy(dict(out))
    filtered_contract = repaired.get("tool_contract")
    _require(
        isinstance(filtered_contract, Mapping),
        "filtered tool contract missing",
    )
    filtered_contract = deepcopy(dict(filtered_contract))

    offered = filtered_contract.get("offered_tool_names")
    _require(
        isinstance(offered, list)
        and all(isinstance(name, str) and name for name in offered),
        "filtered offered tool names invalid",
    )
    offered_set = set(offered)

    production = filtered_contract.get("production_functions")
    _require(
        isinstance(production, Mapping),
        "filtered production_functions missing",
    )
    production = deepcopy(dict(production))

    repaired_production = {
        name: deepcopy(action)
        for name, action in production.items()
        if name in offered_set
    }
    removed = tuple(
        name for name in production
        if name not in offered_set
    )

    _require(
        set(repaired_production) <= offered_set,
        "repaired production function leaked outside offered surface",
    )

    mode = repaired.get("mode")
    _require(
        mode in {"RECOVERY", "VISIBLE_CONTACT", "NORMAL"},
        "priority mode invalid",
    )
    if mode == "NORMAL":
        _require(
            repaired_production == production,
            "NORMAL mode changed production mapping",
        )

    filtered_contract["production_functions"] = repaired_production
    repaired["tool_contract"] = filtered_contract
    repaired["production_functions_filtered_to_offered_surface"] = True
    repaired["suppressed_production_function_names"] = removed
    repaired["original_production_function_names"] = tuple(production)
    repaired["filtered_production_function_names"] = tuple(repaired_production)
    repaired["legal_units_preserved"] = (
        filtered_contract.get("legal_units")
        == original_contract.get("legal_units")
    )
    repaired["legal_buildings_preserved"] = (
        filtered_contract.get("legal_buildings")
        == original_contract.get("legal_buildings")
    )
    repaired["historical_policy_source_modified"] = False
    repaired["historical_runtime_integration_source_modified"] = False

    _require(
        repaired["legal_units_preserved"] is True
        and repaired["legal_buildings_preserved"] is True,
        "typed production legality lists changed",
    )
    return repaired


class Pair06V8CombatPriorityContractCoherentDecisionHooks(
    base_integration.Pair06V8CombatPriorityDecisionHooks
):
    """Use the repaired pure policy only for the scoped decision call."""

    def _adapted_decision(
        self,
        base: Any,
        helper: Any,
        state: Mapping[str, Any],
        pending: Any,
        pb2: Any,
        doctrine: str,
        round_no: int,
    ):
        current = (
            base_integration.priority_policy
            .apply_pair06_v8_combat_action_priority_policy
        )
        _require(
            current is ORIGINAL_POLICY_APPLY,
            "historical priority policy function drift",
        )
        (
            base_integration.priority_policy
            .apply_pair06_v8_combat_action_priority_policy
        ) = apply_pair06_v8_combat_action_priority_contract_coherence_repair
        try:
            return super()._adapted_decision(
                base,
                helper,
                state,
                pending,
                pb2,
                doctrine,
                round_no,
            )
        finally:
            (
                base_integration.priority_policy
                .apply_pair06_v8_combat_action_priority_policy
            ) = ORIGINAL_POLICY_APPLY


def pair06_v8_combat_action_priority_contract_coherence_repair_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_implemented": True,
        "repair_layer": "pure_policy_output_plus_scoped_decision_hook_adapter",
        "historical_policy_source_modified": False,
        "historical_runtime_integration_source_modified": False,
        "production_functions_filtered_to_offered_surface": True,
        "legal_units_preserved": True,
        "legal_buildings_preserved": True,
        "normal_mode_production_mapping_identity_required": True,
        "scoped_policy_function_substitution_implemented": True,
        "policy_function_restored_in_finally": True,
        "translator_production_function_subset_invariant_required": True,
        "attempt_retry_authorized": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityContractCoherenceHold(NEXT_GATE)
