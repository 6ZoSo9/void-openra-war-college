"""Source-only review of pair-06 combat-priority V2 proto-child wiring.

Pins the exact merged V2 proto-child wiring source/tests from #315. The review
confirms that only the decision-hook selection advanced from the reviewed V1
coherent child to the V2 legality-coherent hook while execution, policy
activation, IPC, legacy runner, and restoration boundaries remain unchanged.

The latest consumed attempt and its authorization remain non-reusable.
No retry or runtime authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_child_wiring_generation2
    as wiring,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "proto-child-wiring-review.v1"
)

WIRING_MAIN_HEAD = "b7815dee5408e860ef71784b8617f9a2b89f4e80"
WIRING_GIT_BLOB = "7d55059d17d8679c9e2883c0ee2e6d7951883a22"
WIRING_SOURCE_SHA256 = (
    "3e0c8d7f15b997786b0436dc5a3165b8028b29adca84e41bdd668c32d49b6e3e"
)
WIRING_TEST_GIT_BLOB = "63e543b7ff9d37f6d6b1cd160360dd69bc981dd0"
WIRING_TEST_SHA256 = (
    "c2ec27056ce25192504b1d7af42b3d1b562171d4f7b8e2a29e326131569ed182"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_v2_parent_supervisor_wiring"
)


class Pair06V8CombatPriorityCoherentV2ProtoChildWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2ProtoChildWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = wiring.pair06_v8_combat_priority_coherent_v2_proto_child_wiring_contract()

    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_v2_proto_child_wiring_implemented"
        )
        is True,
        "V2 proto-child wiring missing",
    )

    for field in (
        "v2_repaired_decision_hook_bound",
        "production_functions_filtered_to_offered_surface_by_v1",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_coherent",
        "translator_legal_unit_mapping_coherent",
        "v1_hook_class_substitution_scoped_to_single_call",
        "v1_hook_class_restored_in_finally",
        "existing_child_execution_authorization_gate_preserved",
        "existing_policy_activation_authorization_gate_preserved",
        "existing_ipc_decider_reused",
        "existing_legacy_runner_reused",
    ):
        _require(out.get(field) is True, "V2 proto-child invariant drift: " + field)

    _require(
        out.get("v1_coherent_proto_child_wiring_source_modified") is False
        and out.get("historical_proto_child_wiring_source_modified") is False
        and out.get("historical_proto_child_source_modified") is False,
        "historical reviewed child source unexpectedly modified",
    )

    _require(
        out.get("consumed_v2_precursor_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_v2_precursor_attempt_reusable") is False,
        "consumed attempt lineage drift",
    )
    _require(
        out.get("consumed_v2_precursor_run_id") == FAILED_RUN_ID
        and out.get("consumed_v2_precursor_run_reusable_as_authority") is False
        and out.get("prior_authorization_reusable") is False,
        "failed run/authorization lineage drift",
    )

    for field in (
        "attempt_retry_authorized",
        "parent_supervisor_v2_wiring_implemented",
        "operator_invocation_v2_wiring_implemented",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(out.get(field) is False, "V2 proto-child authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V2 proto-child review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "wiring_main_head": WIRING_MAIN_HEAD,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_source_sha256": WIRING_SOURCE_SHA256,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "wiring_test_sha256": WIRING_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_v2_proto_child_wiring_reviewed": True,
        "v2_repaired_decision_hook_bound": True,
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_coherent": True,
        "translator_legal_unit_mapping_coherent": True,
        "existing_child_execution_authorization_gate_preserved": True,
        "existing_policy_activation_authorization_gate_preserved": True,
        "existing_ipc_decider_reused": True,
        "existing_legacy_runner_reused": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "attempt_retry_authorized": False,
        "parent_supervisor_v2_wiring_implemented": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_wiring": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2ProtoChildWiringReviewHold(NEXT_GATE)
