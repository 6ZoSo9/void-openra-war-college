"""Source-only review of the fresh V2-coherent pair-06 execution request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "execution-authorization-request-review-contract.v1"
)

REQUEST_MAIN_HEAD = "b56bcba2830523c4795c3f2a36241cc2692584f5"
REQUEST_GIT_BLOB = "a51863da1233b54c92818c418d4412cd55d03538"
REQUEST_SOURCE_SHA256 = (
    "7b83e97af67c00394b872bf9aebb55198a38c728ab371f204f7a8cd1c46e45ae"
)
REQUEST_TEST_GIT_BLOB = "160eb92af3d6707c5409d6d6938cda9c7fb60921"
REQUEST_TEST_SHA256 = (
    "286e0b3673262e66d3dd40b9743106e5970d194e0cd54fa9b32334f5859d6cf9"
)
REQUEST_BYTES_SHA256 = (
    "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
)
REQUEST_BYTE_LENGTH = 5670

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)
PRIOR_CONSUMED_REQUEST_SHA256 = (
    "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
)
PRIOR_CONSUMED_AUTHORIZATION_TEXT_SHA256 = (
    "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "explicit_fresh_pair06_v8_combat_action_priority_contract_coherence_repair_v2_"
    "execution_and_policy_activation_authorization"
)


class Pair06V8CombatPriorityCoherentV2RequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2RequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )
    proposal = out.get("request")

    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_v2_execution_authorization_request_implemented"
        )
        is True,
        "V2 coherent request missing",
    )
    _require(
        isinstance(proposal, dict)
        and proposal.get("record_kind") == "proposal_only_not_authorization",
        "V2 coherent request not proposal-only",
    )
    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "V2 coherent request digest drift",
    )
    _require(
        out.get("request_byte_length") == REQUEST_BYTE_LENGTH,
        "V2 coherent request byte-length drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "V2 coherent request digest unexpectedly grants authority",
    )

    source = proposal.get("source_binding")
    _require(isinstance(source, dict), "V2 coherent source binding missing")
    _require(
        source.get("invocation_review_main_head")
        == "bc0b6938323ad9cf31457f1af02d120598445dac"
        and source.get("invocation_review_git_blob")
        == "8e78f768c1a701d4c7b3afec0665faf2bfa256e8"
        and source.get("invocation_review_source_sha256")
        == "74eca7280dfac30cac0fd10ee857f9fc11deb7c7c20d145463f47631137433ad"
        and source.get("invocation_source_sha256")
        == "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c",
        "V2 coherent invocation binding drift",
    )

    mapping = proposal.get("mapping_coherence")
    _require(isinstance(mapping, dict), "V2 mapping coherence missing")
    for field in (
        "v1_production_function_pruning_required",
        "v2_legal_building_reconstruction_required",
        "v2_legal_unit_reconstruction_required",
        "translator_legal_building_mapping_coherence_required",
        "translator_legal_unit_mapping_coherence_required",
        "normal_mode_identity_required",
    ):
        _require(mapping.get(field) is True, "V2 mapping coherence drift: " + field)

    lineage = proposal.get("lineage")
    _require(isinstance(lineage, dict), "V2 coherent lineage missing")
    _require(
        lineage.get("prior_consumed_request_sha256")
        == PRIOR_CONSUMED_REQUEST_SHA256
        and lineage.get("prior_consumed_request_reusable") is False,
        "prior consumed request lineage drift",
    )
    _require(
        lineage.get("prior_consumed_authorization_text_sha256")
        == PRIOR_CONSUMED_AUTHORIZATION_TEXT_SHA256
        and lineage.get("prior_consumed_authorization_reusable") is False,
        "prior consumed authorization lineage drift",
    )
    _require(
        lineage.get("prior_consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and lineage.get("prior_consumed_attempt_reusable") is False,
        "prior consumed attempt lineage drift",
    )
    _require(
        lineage.get("prior_consumed_run_id") == FAILED_RUN_ID
        and lineage.get("prior_consumed_run_preserved") is True
        and lineage.get("prior_consumed_run_reusable_as_authority") is False
        and lineage.get("prior_consumed_result_present") is False
        and lineage.get("prior_consumed_closeout_present") is False,
        "prior consumed run lineage drift",
    )

    scope = proposal.get("proposed_scope")
    _require(isinstance(scope, dict), "V2 coherent proposed scope missing")
    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("doctrine") == "FEINTER"
        and scope.get("seed") == 208354846
        and scope.get("rounds") == 36
        and scope.get("ticks_per_round") == 25
        and scope.get("starter_infantry") == 4
        and scope.get("staging_max_ticks") == 800
        and scope.get("runtime_selection_key")
        == "apollyon-v3-qwen35-4b-lora-v1"
        and scope.get("maximum_attempts") == 1
        and scope.get("maximum_automatic_retries") == 0
        and scope.get("candidate_arm_included") is False
        and scope.get("held_out_pair15_included") is False
        and scope.get("pair03_replay_included") is False
        and scope.get("pair09_replay_included") is False,
        "V2 coherent proposed scope drift",
    )

    gpu = proposal.get("gpu_admission_policy")
    _require(isinstance(gpu, dict), "V2 GPU admission policy missing")
    _require(
        gpu.get("fresh_observation_required") is True
        and gpu.get("fresh_observation_precedes_attempt_marker") is True
        and gpu.get("zero_foreign_compute_processes_required") is True
        and gpu.get("minimum_free_memory_fraction")
        == {"numerator": 9, "denominator": 10}
        and gpu.get("historical_gpu_observation_reusable") is False
        and gpu.get("gpu_admission_hold_must_not_consume_attempt") is True,
        "V2 GPU admission policy drift",
    )

    for field in (
        "v2_coherent_execution_authorization_accepted",
        "v2_coherent_policy_activation_authorization_accepted",
        "v2_coherent_execution_authorized",
        "v2_coherent_policy_activation_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(
            out.get(field) is False,
            "V2 coherent request authority drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
            "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V2 coherent request review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_v2_request_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_main_head": REQUEST_MAIN_HEAD,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "request_bytes_sha256": REQUEST_BYTES_SHA256,
        "request_byte_length": REQUEST_BYTE_LENGTH,
        "pair06_v8_combat_priority_coherent_v2_request_reviewed": True,
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
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "v1_production_function_pruning_required": True,
        "v2_legal_building_reconstruction_required": True,
        "v2_legal_unit_reconstruction_required": True,
        "translator_legal_building_mapping_coherence_required": True,
        "translator_legal_unit_mapping_coherence_required": True,
        "normal_mode_identity_required": True,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_preserved": True,
        "failed_run_reusable_as_authority": False,
        "prior_request_sha256": PRIOR_CONSUMED_REQUEST_SHA256,
        "prior_request_reusable": False,
        "prior_authorization_text_sha256": (
            PRIOR_CONSUMED_AUTHORIZATION_TEXT_SHA256
        ),
        "prior_authorization_reusable": False,
        "matching_request_digest_grants_authority": False,
        "v2_coherent_execution_authorization_accepted": False,
        "v2_coherent_policy_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "automatic_retry": False,
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
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2RequestReviewHold(NEXT_GATE)
