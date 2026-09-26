"""Audit-only acceptance of one combat-priority pair-06 V8 execution.

This record binds the user's exact explicit authorization text to the reviewed
combat-priority request and the canonical War College main at authorization
time. It performs no host I/O, GPU observation, process action, attempt claim,
model load, inference, game execution, replay, training, deployment,
VOID-chain mutation, or wallet/funds action.

Execution and policy activation are authorized only after a fresh reviewed
CUDA:0 observation passes the exact admission policy. The authorization is
single-use and becomes non-reusable after the create-only attempt claim.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-preclaim-gpu-execution-"
    "authorization-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
)
AUTHORIZED_REQUEST_BYTES = 5098
AUTHORIZED_MAIN_HEAD = "564fb5b4aa404cfc18e3e90b8df4a1a49109e858"

AUTHORIZATION_TEXT_SHA256 = (
    "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
)
AUTHORIZATION_TEXT_BYTES = 11

REQUEST_REVIEW_GIT_BLOB = "8ef081192c4859428b3a16a167c2b58345137e73"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "f885004187a10520b6ab8e72a21a7e526db20a3d13a97e5cf73933f677b3e807"
)
REQUEST_REVIEW_TEST_GIT_BLOB = "4feb24d495f16cd709ec61a06b329ed3076cced5"
REQUEST_REVIEW_TEST_SHA256 = (
    "2ca5e9c99fc7b7f1cfd7f49afa4914947095962eb156c64dab9dcf280ef640d9"
)

INVOCATION_REVIEW_GIT_BLOB = "222db31907543f2b776d811f309488e8dc95706a"
INVOCATION_SOURCE_SHA256 = (
    "db383a1a833599d2b444dc4a07d6d1c08ef75e6e5c5dc6fd50cbe173ce5e39dd"
)

PRIOR_SPENT_REQUEST_SHA256 = (
    "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
)
PRIOR_AUTHORIZATION_TEXT_SHA256 = (
    "3cdbfa07fcc1fa14ab0ce01a7e5456b1bf16583ceda5baee16a0191e8a3cf011"
)
PRIOR_ATTEMPT_MARKER_SHA256 = (
    "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
)
PRIOR_RESULT_FILE_SHA256 = (
    "f1a3a1ffec2957b984212e5c11067a477934a1c484020dcb2e6398764a117440"
)
PRIOR_CLOSEOUT_FILE_SHA256 = (
    "f0227597d44ecfc5ae07fdc473a2ca9bda71085fba9970279dedf31d5ac24920"
)
SPENT_OOM_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)

POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_RECEIPT_BOUND_PRECLAIM_GPU_"
    "EXECUTION_AUTHORIZED"
)


class Pair06V8CombatPriorityAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v8_combat_priority_execution_authorization_request_review_contract()
    )

    _require(
        out.get(
            "pair06_v8_combat_priority_execution_authorization_request_reviewed"
        )
        is True,
        "combat-priority request review missing",
    )
    _require(
        out.get("request_sha256") == AUTHORIZED_REQUEST_SHA256
        and out.get("request_byte_length") == AUTHORIZED_REQUEST_BYTES,
        "combat-priority authorized request identity drift",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False,
        "combat-priority authorized request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "combat-priority authorized request cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "combat-priority authorized request GPU observation drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "combat-priority authorized request free-memory threshold drift",
    )
    _require(
        out.get("separate_execution_authorization_required") is True
        and out.get("separate_policy_activation_authorization_required")
        is True,
        "combat-priority dual authorization boundary drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly grants authority without acceptance",
    )

    validated = out.get("validated_request")
    _require(isinstance(validated, dict), "validated request missing")
    proposal = validated.get("request")
    _require(isinstance(proposal, dict), "request proposal missing")

    activation = proposal.get("policy_activation")
    _require(isinstance(activation, dict), "policy activation proposal missing")
    _require(
        activation.get("policy_id") == POLICY_ID
        and activation.get("policy_activation_requested") is True
        and activation.get("separate_policy_activation_authorization_required")
        is True
        and activation.get("separate_policy_confirmation_required") is True,
        "combat-priority policy activation request drift",
    )

    lineage = proposal.get("lineage")
    _require(isinstance(lineage, dict), "combat-priority lineage missing")
    _require(
        lineage.get("prior_spent_gpu_gated_request_sha256")
        == PRIOR_SPENT_REQUEST_SHA256
        and lineage.get("prior_spent_gpu_gated_request_reusable") is False,
        "prior request lineage drift",
    )
    _require(
        lineage.get("prior_spent_authorization_text_sha256")
        == PRIOR_AUTHORIZATION_TEXT_SHA256
        and lineage.get("prior_spent_authorization_reusable") is False,
        "prior authorization lineage drift",
    )
    _require(
        lineage.get("prior_spent_attempt_marker_sha256")
        == PRIOR_ATTEMPT_MARKER_SHA256
        and lineage.get("prior_spent_attempt_reusable") is False
        and lineage.get("prior_successful_attempt_consumed") is True,
        "prior attempt lineage drift",
    )
    _require(
        lineage.get("prior_result_file_sha256") == PRIOR_RESULT_FILE_SHA256
        and lineage.get("prior_result_reusable_as_authority") is False,
        "prior result lineage drift",
    )
    _require(
        lineage.get("prior_closeout_file_sha256")
        == PRIOR_CLOSEOUT_FILE_SHA256
        and lineage.get("prior_closeout_reusable_as_authority") is False,
        "prior closeout lineage drift",
    )
    _require(
        lineage.get("spent_oom_attempt_marker_sha256")
        == SPENT_OOM_ATTEMPT_MARKER_SHA256
        and lineage.get("spent_oom_attempt_reusable") is False,
        "spent OOM attempt lineage drift",
    )

    _require(
        out.get("combat_priority_execution_authorization_accepted") is False
        and out.get(
            "combat_priority_policy_activation_authorization_accepted"
        )
        is False
        and out.get("attempt_marker_creation_authorized") is False
        and out.get("runtime_load_authorized") is False
        and out.get("model_inference_authorized") is False
        and out.get("game_execution_authorized") is False,
        "request review unexpectedly self-authorizes execution",
    )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_"
            "PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
        ),
        "combat-priority authorization frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_execution_authorization_acceptance_contract() -> dict[str, Any]:
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
        "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
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
        "prior_spent_request_sha256": PRIOR_SPENT_REQUEST_SHA256,
        "prior_spent_request_reusable": False,
        "prior_authorization_text_sha256": PRIOR_AUTHORIZATION_TEXT_SHA256,
        "prior_authorization_reusable": False,
        "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
        "prior_attempt_reusable": False,
        "prior_result_file_sha256": PRIOR_RESULT_FILE_SHA256,
        "prior_result_reusable_as_authority": False,
        "prior_closeout_file_sha256": PRIOR_CLOSEOUT_FILE_SHA256,
        "prior_closeout_reusable_as_authority": False,
        "spent_oom_attempt_marker_sha256": SPENT_OOM_ATTEMPT_MARKER_SHA256,
        "spent_oom_attempt_reusable": False,
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
    raise Pair06V8CombatPriorityAuthorizationAcceptanceHold(NEXT_GATE)
