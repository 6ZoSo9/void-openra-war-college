"""Second source-only coherence repair for pair-06 combat-priority tools.

The reviewed V1 coherence repair correctly prunes typed production functions
whose tool names were removed from the offered surface. Runtime evidence then
proved a second translator invariant: legal_buildings and legal_units must be
exactly the sets mapped by the remaining typed production functions.

This V2 layer leaves all historical sources unchanged. It calls the reviewed
V1 repair first, then reconstructs only the typed legality lists for filtered
RECOVERY/VISIBLE_CONTACT modes. NORMAL mode must remain exactly unchanged.

No retry, runtime activation, execution, replay, training, promotion,
deployment, chain mutation, or wallet/funds authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_generation2
    as repair_v1,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2.v1"
)

ORIGINAL_V1_REPAIR_APPLY = (
    repair_v1.apply_pair06_v8_combat_action_priority_contract_coherence_repair
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_v2_review"
)


class Pair06V8CombatPriorityContractCoherenceV2Hold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityContractCoherenceV2Hold(message)


def _typed_legality_sets(
    production_functions: Mapping[str, Any],
) -> tuple[set[str], set[str]]:
    buildings: set[str] = set()
    units: set[str] = set()

    for name, raw_action in production_functions.items():
        _require(isinstance(name, str) and name, "production function name invalid")
        _require(
            isinstance(raw_action, Mapping),
            f"production action invalid: {name}",
        )
        kind = raw_action.get("kind")
        _require(
            kind in {"build_and_place", "build_unit"},
            f"production kind invalid: {name}",
        )
        if kind == "build_and_place":
            value = raw_action.get("building_type")
            _require(
                isinstance(value, str) and value,
                f"building type invalid: {name}",
            )
            buildings.add(value)
        else:
            value = raw_action.get("unit_type")
            _require(
                isinstance(value, str) and value,
                f"unit type invalid: {name}",
            )
            units.add(value)

    return buildings, units


def apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply V1 repair, then align legality lists to remaining production maps."""
    original_contract = deepcopy(dict(tool_contract))

    out = ORIGINAL_V1_REPAIR_APPLY(
        state=state,
        typed_tools=typed_tools,
        tool_contract=tool_contract,
    )
    _require(isinstance(out, Mapping), "V1 repair result missing")

    repaired = deepcopy(dict(out))
    contract = repaired.get("tool_contract")
    _require(isinstance(contract, Mapping), "repaired tool contract missing")
    contract = deepcopy(dict(contract))

    production = contract.get("production_functions")
    _require(
        isinstance(production, Mapping),
        "repaired production_functions missing",
    )
    production = deepcopy(dict(production))

    legal_buildings = contract.get("legal_buildings")
    legal_units = contract.get("legal_units")
    _require(
        isinstance(legal_buildings, list)
        and all(isinstance(value, str) and value for value in legal_buildings),
        "legal_buildings invalid",
    )
    _require(
        isinstance(legal_units, list)
        and all(isinstance(value, str) and value for value in legal_units),
        "legal_units invalid",
    )

    mapped_buildings, mapped_units = _typed_legality_sets(production)

    _require(
        mapped_buildings <= set(legal_buildings),
        "mapped building escaped reviewed legal_buildings",
    )
    _require(
        mapped_units <= set(legal_units),
        "mapped unit escaped reviewed legal_units",
    )

    mode = repaired.get("mode")
    _require(
        mode in {"RECOVERY", "VISIBLE_CONTACT", "NORMAL"},
        "priority mode invalid",
    )

    if mode == "NORMAL":
        _require(
            contract.get("production_functions")
            == original_contract.get("production_functions"),
            "NORMAL mode changed production mapping",
        )
        _require(
            legal_buildings == original_contract.get("legal_buildings"),
            "NORMAL mode changed legal_buildings",
        )
        _require(
            legal_units == original_contract.get("legal_units"),
            "NORMAL mode changed legal_units",
        )
        repaired_legal_buildings = list(legal_buildings)
        repaired_legal_units = list(legal_units)
    else:
        repaired_legal_buildings = [
            value for value in legal_buildings
            if value in mapped_buildings
        ]
        repaired_legal_units = [
            value for value in legal_units
            if value in mapped_units
        ]

    _require(
        set(repaired_legal_buildings) == mapped_buildings,
        "legal building mapping remains incoherent",
    )
    _require(
        set(repaired_legal_units) == mapped_units,
        "legal unit mapping remains incoherent",
    )

    contract["legal_buildings"] = repaired_legal_buildings
    contract["legal_units"] = repaired_legal_units
    repaired["tool_contract"] = contract

    repaired["translator_legal_building_mapping_coherent"] = True
    repaired["translator_legal_unit_mapping_coherent"] = True
    repaired["legal_buildings_reconstructed_from_remaining_production"] = (
        mode != "NORMAL"
    )
    repaired["legal_units_reconstructed_from_remaining_production"] = (
        mode != "NORMAL"
    )
    repaired["mapped_legal_buildings"] = tuple(
        value for value in repaired_legal_buildings
    )
    repaired["mapped_legal_units"] = tuple(
        value for value in repaired_legal_units
    )
    repaired["historical_v1_repair_source_modified"] = False
    repaired["historical_priority_policy_source_modified"] = False
    repaired["historical_runtime_integration_source_modified"] = False

    return repaired


class Pair06V8CombatPriorityContractCoherentV2DecisionHooks(
    repair_v1.Pair06V8CombatPriorityContractCoherentDecisionHooks
):
    """Use V2 legality reconstruction inside the already-scoped V1 hook."""

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
            repair_v1
            .apply_pair06_v8_combat_action_priority_contract_coherence_repair
        )
        _require(
            current is ORIGINAL_V1_REPAIR_APPLY,
            "historical V1 repair function drift",
        )

        (
            repair_v1
            .apply_pair06_v8_combat_action_priority_contract_coherence_repair
        ) = apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2
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
                repair_v1
                .apply_pair06_v8_combat_action_priority_contract_coherence_repair
            ) = ORIGINAL_V1_REPAIR_APPLY


def pair06_v8_combat_action_priority_contract_coherence_repair_v2_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_v2_implemented": True,
        "repair_layer": (
            "reviewed_v1_output_plus_typed_legality_reconstruction"
        ),
        "historical_v1_repair_source_modified": False,
        "historical_priority_policy_source_modified": False,
        "historical_runtime_integration_source_modified": False,
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_invariant_required": True,
        "translator_legal_unit_mapping_invariant_required": True,
        "normal_mode_identity_required": True,
        "scoped_v1_function_substitution_implemented": True,
        "v1_function_restored_in_finally": True,
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
    raise Pair06V8CombatPriorityContractCoherenceV2Hold(NEXT_GATE)
