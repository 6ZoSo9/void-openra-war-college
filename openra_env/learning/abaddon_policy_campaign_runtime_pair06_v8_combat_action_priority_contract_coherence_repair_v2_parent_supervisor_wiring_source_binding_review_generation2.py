"""Source-only review of pair-06 combat-priority V2 parent wiring.

Pins the exact merged V2 child entrypoint, V2 parent wiring, and their tests
from #317. The reviewed V1 coherent parent wrapper, historical combat-priority
parent, and historical no-offload parent remain unchanged.

The latest consumed attempt marker and failed run are permanently non-reusable.
This review advances only to a fresh V2 one-shot invocation source with a
distinct evidence namespace. It grants no retry, attempt claim, runtime
activation, execution, replay, training, deployment, chain mutation, or
wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_parent_supervisor_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "parent-supervisor-wiring-review-contract.v1"
)

MERGED_MAIN_HEAD = "3865459c9829a18593b6e3eea431abd0877941a8"

CHILD_ENTRY_GIT_BLOB = "0078db895accd35a0f7f64e5cb16bab31998bd71"
CHILD_ENTRY_SOURCE_SHA256 = (
    "14d5b4cbe52aa493d07ac8f9d8e3b7d0a00cbead9f4147ecdefa55e868767d35"
)
CHILD_ENTRY_TEST_GIT_BLOB = "d5c0f68c1a883124b640f2f0c15a361cfafcdb22"
CHILD_ENTRY_TEST_SHA256 = (
    "6fb942a43d6271b16c856dfaaafc49c002ba6f2306c02283bbf302da9ab5959b"
)

PARENT_WIRING_GIT_BLOB = "2541ea0de84ede2bb3a0effcca19cca61204d3a7"
PARENT_WIRING_SOURCE_SHA256 = (
    "9aea4ce2abac908cee658fda4f2f2e2d8cf22bf05d73299d741b2dbf8d52ce9e"
)
PARENT_WIRING_TEST_GIT_BLOB = "6d2dc05122bc59c3a079d68ec715d4db13319ddf"
PARENT_WIRING_TEST_SHA256 = (
    "7af07fb2031b9d8edf90b6e62efc6042aafb9d2e3510e40e99c376dfa6764049"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_repair_v2_"
    "baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu"
)


class Pair06V8CombatPriorityCoherentV2ParentWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2ParentWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    parent = wiring.pair06_v8_combat_priority_coherent_v2_parent_wiring_contract()
    child = (
        child_entry
        .pair06_v8_combat_priority_coherent_v2_child_entrypoint_contract()
    )

    _require(parent.get("pair_slot") == 6, "V2 coherent parent slot drift")
    _require(parent.get("arm") == "baseline", "V2 coherent parent arm drift")
    _require(
        parent.get("v2_child_entrypoint_implemented") is True,
        "V2 coherent child entrypoint missing",
    )
    _require(
        parent.get("v1_coherent_parent_wiring_source_modified") is False
        and parent.get("historical_parent_wiring_source_modified") is False
        and parent.get("historical_no_offload_parent_source_modified") is False,
        "reviewed parent source unexpectedly modified",
    )

    for field in (
        "v2_child_command_substitution_implemented",
        "v2_child_command_substitution_scoped_to_single_call",
        "v1_coherent_child_command_restored_in_finally",
        "existing_execution_confirmation_token_preserved",
        "existing_policy_activation_confirmation_token_preserved",
        "existing_no_offload_model_loader_reused",
        "existing_cuda0_placement_checks_reused",
        "existing_parent_decision_service_loop_reused",
        "existing_child_retirement_reused",
        "existing_parent_receipt_returned_unchanged",
        "production_functions_filtered_to_offered_surface_by_v1",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_coherent",
        "translator_legal_unit_mapping_coherent",
    ):
        _require(parent.get(field) is True, "V2 coherent parent invariant drift: " + field)

    _require(
        parent.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and parent.get("consumed_attempt_reusable") is False,
        "consumed V2 attempt lineage drift",
    )
    _require(
        parent.get("failed_run_id") == FAILED_RUN_ID
        and parent.get("failed_run_reusable_as_authority") is False
        and parent.get("prior_authorization_reusable") is False,
        "failed V2 run/authorization lineage drift",
    )

    for field in (
        "attempt_retry_authorized",
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
        _require(parent.get(field) is False, "V2 coherent parent authority drift: " + field)

    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V2 coherent parent review frontier drift",
    )

    _require(
        child.get(
            "pair06_v8_combat_priority_coherent_v2_child_entrypoint_implemented"
        )
        is True,
        "V2 coherent child entrypoint contract missing",
    )
    for field in (
        "v2_proto_child_wiring_reviewed",
        "production_functions_filtered_to_offered_surface_by_v1",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_coherent",
        "translator_legal_unit_mapping_coherent",
    ):
        _require(child.get(field) is True, "V2 child invariant drift: " + field)
    _require(
        child.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and child.get("consumed_attempt_reusable") is False
        and child.get("failed_run_id") == FAILED_RUN_ID
        and child.get("failed_run_reusable_as_authority") is False
        and child.get("prior_authorization_reusable") is False
        and child.get("attempt_retry_authorized") is False,
        "V2 child consumed-attempt boundary drift",
    )
    _require(
        child.get("execution_performed_by_contract_inspection") is False
        and child.get("runtime_activation_authorized_by_contract_inspection")
        is False,
        "V2 child inspection unexpectedly executes",
    )

    return {
        "parent_wiring": deepcopy(parent),
        "child_entrypoint": deepcopy(child),
    }


def pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "merged_main_head": MERGED_MAIN_HEAD,
        "child_entry_git_blob": CHILD_ENTRY_GIT_BLOB,
        "child_entry_source_sha256": CHILD_ENTRY_SOURCE_SHA256,
        "child_entry_test_git_blob": CHILD_ENTRY_TEST_GIT_BLOB,
        "child_entry_test_sha256": CHILD_ENTRY_TEST_SHA256,
        "parent_wiring_git_blob": PARENT_WIRING_GIT_BLOB,
        "parent_wiring_source_sha256": PARENT_WIRING_SOURCE_SHA256,
        "parent_wiring_test_git_blob": PARENT_WIRING_TEST_GIT_BLOB,
        "parent_wiring_test_sha256": PARENT_WIRING_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_v2_parent_wiring_reviewed": True,
        "canonical_invocation_lane": (
            "receipt_bound_no_offload_fresh_preclaim_gpu"
        ),
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_coherent": True,
        "translator_legal_unit_mapping_coherent": True,
        "maximum_attempts_per_fresh_authorization": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_must_precede_attempt_marker": True,
        "durable_create_only_attempt_marker_required": True,
        "attempt_marker_must_precede_model_load_and_child_spawn": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "fresh_evidence_namespace_required": True,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "attempt_retry_authorized": False,
        "attempt_marker_creation_authorized": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def implement_invocation_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2ParentWiringReviewHold(NEXT_GATE)
