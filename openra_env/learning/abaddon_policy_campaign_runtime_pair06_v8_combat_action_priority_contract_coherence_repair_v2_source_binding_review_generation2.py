"""Source-only review of pair-06 combat-priority coherence repair V2.

Pins the exact merged V2 repair source/tests from #313 and seals the most
recent consumed failed attempt. The V2 repair reconstructs typed legality lists
from the remaining production mappings after V1 pruning.

No retry, runtime activation, execution, replay, training, promotion,
deployment, chain mutation, or wallet/funds authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_generation2
    as repair_v2,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-review.v1"
)

REPAIR_V2_MAIN_HEAD = "d4d3e57d5025e0a37729440377d1d36be10fce71"
REPAIR_V2_GIT_BLOB = "bf9b5f0e5f8d1c61f1bc8f4ba42aa45b2d3278ae"
REPAIR_V2_SOURCE_SHA256 = (
    "087245a4fea130ff25cec1c052370fa26fa4e31450b91b5277d9e5b63ad2cdab"
)
REPAIR_V2_TEST_GIT_BLOB = "8ec279e12294020876ebb38a9ef6f8f3481046a1"
REPAIR_V2_TEST_SHA256 = (
    "c5c69956dea345dc01f6ef78bdd67df83487853fa1635b423ffbba4a7ad720a4"
)

CONSUMED_V2_PRECURSOR_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
CONSUMED_V2_PRECURSOR_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "PROTO_CHILD_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_v2_proto_child_wiring"
)


class Pair06V8CombatPriorityContractCoherenceV2ReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityContractCoherenceV2ReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        repair_v2
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_contract()
    )

    _require(out.get("repair_v2_implemented") is True, "V2 repair missing")
    _require(
        out.get("repair_layer")
        == "reviewed_v1_output_plus_typed_legality_reconstruction",
        "V2 repair layer drift",
    )

    for field in (
        "production_functions_filtered_to_offered_surface_by_v1",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_invariant_required",
        "translator_legal_unit_mapping_invariant_required",
        "normal_mode_identity_required",
        "scoped_v1_function_substitution_implemented",
        "v1_function_restored_in_finally",
    ):
        _require(out.get(field) is True, "V2 repair invariant drift: " + field)

    _require(
        out.get("historical_v1_repair_source_modified") is False
        and out.get("historical_priority_policy_source_modified") is False
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
        _require(out.get(field) is False, "V2 authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V2 repair review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_v2_main_head": REPAIR_V2_MAIN_HEAD,
        "repair_v2_git_blob": REPAIR_V2_GIT_BLOB,
        "repair_v2_source_sha256": REPAIR_V2_SOURCE_SHA256,
        "repair_v2_test_git_blob": REPAIR_V2_TEST_GIT_BLOB,
        "repair_v2_test_sha256": REPAIR_V2_TEST_SHA256,
        "pair06_v8_combat_action_priority_contract_coherence_repair_v2_reviewed": True,
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_invariant_required": True,
        "translator_legal_unit_mapping_invariant_required": True,
        "normal_mode_identity_required": True,
        "consumed_v2_precursor_attempt_marker_sha256": (
            CONSUMED_V2_PRECURSOR_ATTEMPT_MARKER_SHA256
        ),
        "consumed_v2_precursor_attempt_reusable": False,
        "consumed_v2_precursor_run_id": CONSUMED_V2_PRECURSOR_RUN_ID,
        "consumed_v2_precursor_run_reusable_as_authority": False,
        "consumed_v2_precursor_result_present": False,
        "consumed_v2_precursor_closeout_present": False,
        "prior_authorization_reusable": False,
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
        "validated_repair_v2": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityContractCoherenceV2ReviewHold(NEXT_GATE)
