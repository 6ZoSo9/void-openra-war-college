"""Audit-only acceptance of one fresh V2-coherent pair-06 V8 execution.

This record binds the user's exact fresh authorization text to the exact
reviewed V2 legality-coherent execution request and canonical War College main
at authorization time.

It performs no host I/O, GPU observation, attempt claim, policy activation,
model load, inference, game execution, replay, training, deployment,
VOID-chain mutation, or wallet/funds action.

Execution and policy activation are authorized only after a fresh reviewed
CUDA:0 observation passes the exact admission policy. Both authorizations are
single-use and become non-reusable after the fresh create-only attempt claim.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "preclaim-gpu-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
)
AUTHORIZED_REQUEST_BYTES = 5670
AUTHORIZED_MAIN_HEAD = "d8b16f1c23a74803ac4ace94045fed147c3c69fe"

AUTHORIZATION_TEXT_SHA256 = (
    "6cfe4dd78c02a55c2499163b01de6f5714e0b8573100b7a888177ff1a568d139"
)
AUTHORIZATION_TEXT_BYTES = 533

REQUEST_REVIEW_GIT_BLOB = "18e69f90b4020a775de6bb9f1b7b5346e4e531fd"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "5b97f48b1ad6220bd615194b55f74f17865090c251ae08a257906678e754f862"
)
REQUEST_REVIEW_TEST_GIT_BLOB = "1171d47ea8f9990c6bcb7b0419b8edf8f10779c1"
REQUEST_REVIEW_TEST_SHA256 = (
    "86cceb10e97147bbed2fe3eb900dbc582ad677df56dddaef7e7a2c099cf700ce"
)

INVOCATION_SOURCE_SHA256 = (
    "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
)

PRIOR_CONSUMED_REQUEST_SHA256 = (
    "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
)
PRIOR_CONSUMED_AUTHORIZATION_TEXT_SHA256 = (
    "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
)
PRIOR_CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
PRIOR_CONSUMED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED"
)


class Pair06V8CombatPriorityCoherentV2AuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2AuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v8_combat_priority_coherent_v2_request_review_contract()
    )

    _require(
        out.get("pair06_v8_combat_priority_coherent_v2_request_reviewed")
        is True,
        "V2 coherent request review missing",
    )
    _require(
        out.get("request_bytes_sha256") == AUTHORIZED_REQUEST_SHA256
        and out.get("request_byte_length") == AUTHORIZED_REQUEST_BYTES,
        "V2 coherent authorized request identity drift",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("doctrine") == "FEINTER"
        and out.get("seed") == 208354846
        and out.get("rounds") == 36
        and out.get("ticks_per_round") == 25
        and out.get("starter_infantry") == 4
        and out.get("staging_max_ticks") == 800
        and out.get("runtime_selection_key")
        == "apollyon-v3-qwen35-4b-lora-v1",
        "V2 coherent authorized request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V2 coherent authorized request cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "V2 coherent GPU admission policy drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V2 coherent GPU admission threshold drift",
    )
    for field in (
        "v1_production_function_pruning_required",
        "v2_legal_building_reconstruction_required",
        "v2_legal_unit_reconstruction_required",
        "translator_legal_building_mapping_coherence_required",
        "translator_legal_unit_mapping_coherence_required",
        "normal_mode_identity_required",
        "fresh_execution_authorization_required",
        "fresh_policy_activation_authorization_required",
        "failed_run_preserved",
    ):
        _require(out.get(field) is True, "V2 coherent request invariant drift: " + field)

    _require(
        out.get("consumed_attempt_marker_sha256")
        == PRIOR_CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_attempt_reusable") is False,
        "prior consumed attempt lineage drift",
    )
    _require(
        out.get("failed_run_id") == PRIOR_CONSUMED_RUN_ID
        and out.get("failed_run_reusable_as_authority") is False
        and out.get("prior_request_sha256") == PRIOR_CONSUMED_REQUEST_SHA256
        and out.get("prior_request_reusable") is False
        and out.get("prior_authorization_text_sha256")
        == PRIOR_CONSUMED_AUTHORIZATION_TEXT_SHA256
        and out.get("prior_authorization_reusable") is False,
        "prior consumed request/run/authorization reuse drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "V2 request digest unexpectedly grants authority",
    )
    _require(
        out.get("v2_coherent_execution_authorization_accepted") is False
        and out.get("v2_coherent_policy_activation_authorization_accepted") is False
        and out.get("attempt_marker_creation_authorized") is False
        and out.get("runtime_load_authorized") is False
        and out.get("model_inference_authorized") is False
        and out.get("game_execution_authorized") is False,
        "V2 request review unexpectedly self-authorizes execution",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
            "EXECUTION_AUTHORIZATION_REQUIRED"
        ),
        "V2 coherent authorization frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_v2_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_request_bytes": AUTHORIZED_REQUEST_BYTES,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "request_review_test_git_blob": REQUEST_REVIEW_TEST_GIT_BLOB,
        "request_review_test_sha256": REQUEST_REVIEW_TEST_SHA256,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "policy_id": POLICY_ID,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "runtime_selection_key": "apollyon-v3-qwen35-4b-lora-v1",
        "maximum_attempts": 1,
        "automatic_retry": False,
        "v1_production_function_pruning_required": True,
        "v2_legal_building_reconstruction_required": True,
        "v2_legal_unit_reconstruction_required": True,
        "translator_legal_building_mapping_coherence_required": True,
        "translator_legal_unit_mapping_coherence_required": True,
        "normal_mode_identity_required": True,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "gpu_admission_failure_must_not_create_attempt_marker": True,
        "gpu_admission_failure_must_not_activate_policy": True,
        "gpu_admission_failure_must_not_load_model": True,
        "gpu_admission_failure_must_not_execute_inference": True,
        "gpu_admission_failure_must_not_execute_game": True,
        "receipt_bound_preclaim_gpu_execution_authorized": True,
        "combat_priority_policy_activation_authorized": True,
        "attempt_marker_creation_authorized_after_fresh_gpu_admission": True,
        "policy_activation_authorized_after_fresh_gpu_admission": True,
        "runtime_load_authorized_after_fresh_gpu_admission": True,
        "model_inference_authorized_after_fresh_gpu_admission": True,
        "game_execution_authorized_after_fresh_gpu_admission": True,
        "prior_consumed_request_sha256": PRIOR_CONSUMED_REQUEST_SHA256,
        "prior_consumed_request_reusable": False,
        "prior_consumed_authorization_text_sha256": (
            PRIOR_CONSUMED_AUTHORIZATION_TEXT_SHA256
        ),
        "prior_consumed_authorization_reusable": False,
        "prior_consumed_attempt_marker_sha256": (
            PRIOR_CONSUMED_ATTEMPT_MARKER_SHA256
        ),
        "prior_consumed_attempt_reusable": False,
        "prior_consumed_run_id": PRIOR_CONSUMED_RUN_ID,
        "prior_consumed_run_preserved": True,
        "prior_consumed_run_reusable_as_authority": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "attempt_marker_created_by_this_record": False,
        "gpu_observation_performed_by_this_record": False,
        "policy_activation_performed_by_this_record": False,
        "runtime_load_performed_by_this_record": False,
        "model_inference_performed_by_this_record": False,
        "game_execution_performed_by_this_record": False,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
        "reviewed_request": reviewed,
        "next_gate": NEXT_GATE,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2AuthorizationAcceptanceHold(NEXT_GATE)
