"""Audit-only acceptance of one fresh coherent pair-06 V8 execution.

This record binds the user's exact fresh authorization text to the exact
reviewed contract-coherent execution request and canonical War College main at
authorization time.

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
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "preclaim-gpu-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
)
AUTHORIZED_REQUEST_BYTES = 4998
AUTHORIZED_MAIN_HEAD = "3ca55f3d6327d5e12c1f1e6b3d3ae4adf09ea009"

AUTHORIZATION_TEXT_SHA256 = (
    "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
)
AUTHORIZATION_TEXT_BYTES = 457

REQUEST_REVIEW_GIT_BLOB = "8c9f55231e2d62194f0ecba2469e9fb83784af37"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "8dd65c5c4f19fecebe0d4e320f6cde5895ee51a90f55c1e45f961deb97123258"
)
REQUEST_REVIEW_TEST_GIT_BLOB = "33111ba3ba4219fc7ed10d9ccbef37fd0d855c16"
REQUEST_REVIEW_TEST_SHA256 = (
    "7e7def0cb44a75de0227e1bfec423023e05764325922fea1a98c9d6f7c7cbf84"
)

INVOCATION_SOURCE_SHA256 = (
    "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095"
)

PRIOR_FAILED_REQUEST_SHA256 = (
    "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
)
PRIOR_FAILED_AUTHORIZATION_TEXT_SHA256 = (
    "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
)
PRIOR_FAILED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
PRIOR_FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED"
)


class Pair06V8CombatPriorityCoherentAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = request_review.pair06_v8_combat_priority_coherent_request_review_contract()

    _require(
        out.get("pair06_v8_combat_priority_coherent_request_reviewed") is True,
        "coherent request review missing",
    )
    _require(
        out.get("request_bytes_sha256") == AUTHORIZED_REQUEST_SHA256
        and out.get("request_byte_length") == AUTHORIZED_REQUEST_BYTES,
        "coherent authorized request identity drift",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False,
        "coherent authorized request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "coherent authorized request cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "coherent GPU admission policy drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "coherent GPU admission threshold drift",
    )
    _require(
        out.get("fresh_execution_authorization_required") is True
        and out.get("fresh_policy_activation_authorization_required") is True,
        "coherent fresh dual authorization boundary drift",
    )
    _require(
        out.get("consumed_attempt_marker_sha256")
        == PRIOR_FAILED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_attempt_reusable") is False,
        "prior failed attempt lineage drift",
    )
    _require(
        out.get("failed_run_id") == PRIOR_FAILED_RUN_ID
        and out.get("failed_run_reusable_as_authority") is False
        and out.get("prior_authorization_reusable") is False,
        "prior failed run/authorization reuse drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly grants authority",
    )
    _require(
        out.get("coherent_execution_authorization_accepted") is False
        and out.get("coherent_policy_activation_authorization_accepted") is False
        and out.get("attempt_marker_creation_authorized") is False
        and out.get("runtime_load_authorized") is False
        and out.get("model_inference_authorized") is False
        and out.get("game_execution_authorized") is False,
        "request review unexpectedly self-authorizes execution",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
            "EXECUTION_AUTHORIZATION_REQUIRED"
        ),
        "coherent authorization frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract() -> dict[str, Any]:
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
        "maximum_attempts": 1,
        "automatic_retry": False,
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
        "prior_failed_request_sha256": PRIOR_FAILED_REQUEST_SHA256,
        "prior_failed_request_reusable": False,
        "prior_failed_authorization_text_sha256": (
            PRIOR_FAILED_AUTHORIZATION_TEXT_SHA256
        ),
        "prior_failed_authorization_reusable": False,
        "prior_failed_attempt_marker_sha256": PRIOR_FAILED_ATTEMPT_MARKER_SHA256,
        "prior_failed_attempt_reusable": False,
        "prior_failed_run_id": PRIOR_FAILED_RUN_ID,
        "prior_failed_run_reusable_as_authority": False,
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
    raise Pair06V8CombatPriorityCoherentAuthorizationAcceptanceHold(NEXT_GATE)
