"""Source-only review of the V2-coherent pair-06 combat-priority invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "baseline-attempt-invocation-receipt-bound-no-offload-preclaim-gpu-"
    "review-contract.v1"
)

INVOCATION_MAIN_HEAD = "6f21cb30d46016f8e6bd362f6bb8d996ff0215cc"
INVOCATION_GIT_BLOB = "9b5db375d5ae8e133de73603ffd3745352789018"
INVOCATION_SOURCE_SHA256 = (
    "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
)
INVOCATION_TEST_GIT_BLOB = "bb32d3e436ea40c2c36f46d369533a3e5e9c7d52"
INVOCATION_TEST_SHA256 = (
    "4a9f369155c7808d8df67ecdbbd6271e39fe404e24260e998ebd8d273584c0bf"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
    "EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_repair_v2_"
    "execution_authorization_request"
)


class Pair06V8CombatPriorityCoherentV2InvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2InvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )

    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_v2_baseline_attempt_"
            "invocation_implemented"
        )
        is True,
        "V2 coherent invocation missing",
    )
    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_v2_baseline_attempt_"
            "invocation_reviewed"
        )
        is False,
        "V2 coherent invocation unexpectedly self-reviewed",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False,
        "V2 coherent invocation scope drift",
    )
    _require(
        out.get("parent_wiring_review_main_head")
        == "71afc3c5ca6887d376088bba8d687fd116b4b96b"
        and out.get("parent_wiring_review_git_blob")
        == "bc22e83cb56db2479f77147c84963c8420050899"
        and out.get("parent_wiring_review_source_sha256")
        == "51acdb78f7acca71b0bbdf14adbb558bae422eece6ea175433ab30569d62831d",
        "V2 coherent parent binding drift",
    )

    for field in (
        "fresh_preclaim_gpu_observation_implemented",
        "fresh_preclaim_gpu_admission_required",
        "fresh_preclaim_gpu_observation_precedes_attempt_marker",
        "zero_foreign_cuda0_compute_processes_required",
        "durable_create_only_attempt_marker_implemented",
        "coherent_v2_marker_namespace_distinct_from_spent_coherent_v1",
        "coherent_v2_result_namespace_distinct_from_spent_coherent_v1",
        "coherent_v2_closeout_namespace_distinct_from_spent_coherent_v1",
        "coherent_v2_runs_root_distinct_from_spent_coherent_v1",
        "fresh_evidence_namespace_required",
        "fresh_execution_authorization_required",
        "fresh_policy_activation_authorization_required",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "reviewed_combat_priority_coherent_v2_parent_wiring_used",
        "failed_coherent_v1_run_preserved",
    ):
        _require(
            out.get(field) is True,
            "V2 coherent invocation invariant drift: " + field,
        )

    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10
        and out.get("maximum_attempts") == 1
        and out.get("automatic_retry") is False,
        "V2 coherent invocation bound drift",
    )
    _require(
        out.get("consumed_coherent_v1_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_coherent_v1_attempt_reusable") is False,
        "consumed V1 coherent attempt lineage drift",
    )
    _require(
        out.get("failed_coherent_v1_run_id") == FAILED_RUN_ID
        and out.get("failed_coherent_v1_run_reusable_as_authority") is False
        and out.get("failed_coherent_v1_run_preserved") is True
        and out.get("prior_authorization_reusable") is False,
        "failed V1 coherent lineage reuse drift",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        _require(
            out.get(field) is False,
            "V2 coherent invocation authority drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_"
            "PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V2 coherent invocation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_v2_invocation_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_main_head": INVOCATION_MAIN_HEAD,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_v2_invocation_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_evidence_namespace_required": True,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "v1_production_function_pruning_required": True,
        "v2_legal_building_reconstruction_required": True,
        "v2_legal_unit_reconstruction_required": True,
        "translator_legal_building_mapping_coherence_required": True,
        "translator_legal_unit_mapping_coherence_required": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "failed_run_preserved": True,
        "prior_authorization_reusable": False,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_invocation": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def request_authorization_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2InvocationReviewHold(NEXT_GATE)
