"""Proposal-only request for one fresh coherent pair-06 V8 baseline run.

This request binds the reviewed contract-coherent combat-priority
receipt-bound/no-offload/fresh-preclaim-GPU invocation.

It is proposal-only. Matching bytes or digest grant no execution or policy
activation authority.

The prior combat-priority request, its explicit authorization, consumed failed
attempt marker, and failed run are carried forward as spent and non-reusable.
The prior failed run produced no durable result or closeout.

This source performs no host observation, process action, attempt claim, model
load, inference, game execution, replay, training, deployment, VOID-chain
mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as invocation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_preclaim_gpu_execution_authorization_acceptance_generation2
    as prior_authorization,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "no-offload-receipt-bound-preclaim-gpu-baseline-"
    "execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "no-offload-receipt-bound-preclaim-gpu-baseline-"
    "execution-authorization-request-validation.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
DOCTRINE = "FEINTER"
SEED = 208354846
ROUNDS = 36
TICKS_PER_ROUND = 25
STARTER_INFANTRY = 4
STAGING_MAX_TICKS = 800
RUNTIME_SELECTION_KEY = "apollyon-v3-qwen35-4b-lora-v1"

INVOCATION_REVIEW_MAIN_HEAD = "c941b437d63d82174af2849013d33e8d7ae29a86"
INVOCATION_REVIEW_GIT_BLOB = "92ac3f8b09aa22be4ed2acf72834da7bc9db08b4"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "05bdcf091a19c0acdc2b40d19617d1c6e15b5788bed8a4e074554795a9d27100"
)
INVOCATION_REVIEW_TEST_GIT_BLOB = (
    "410a6106bda81df7dea8a893739a66d5a23f47ec"
)
INVOCATION_REVIEW_TEST_SHA256 = (
    "41216c34669efe7030b2e92c8292ba1777ee22091d7b152ab368d4aa5d0b9f79"
)
INVOCATION_SOURCE_SHA256 = (
    "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095"
)

PRIOR_FAILED_REQUEST_SHA256 = (
    "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
)
PRIOR_FAILED_REQUEST_BYTES = 5098
PRIOR_FAILED_AUTHORIZATION_TEXT_SHA256 = (
    "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
)
PRIOR_FAILED_AUTHORIZATION_TEXT_BYTES = 11
PRIOR_FAILED_AUTHORIZED_MAIN_HEAD = (
    "564fb5b4aa404cfc18e3e90b8df4a1a49109e858"
)
PRIOR_FAILED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
PRIOR_FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "coherent_execution_authorization_accepted",
    "coherent_policy_activation_authorization_accepted",
    "coherent_execution_authorized",
    "coherent_policy_activation_authorized",
    "attempt_consumed",
    "attempt_marker_creation_authorized",
    "runtime_load_authorized",
    "model_inference_authorized",
    "game_execution_authorized",
    "candidate_execution_authorized",
    "pair15_execution_authorized",
    "pair03_replay_authorized",
    "pair09_replay_authorized",
    "training_authorized",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
    "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_repair_"
    "execution_authorization_request_review"
)


class Pair06V8CombatPriorityCoherentAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    invocation = (
        invocation_review
        .pair06_v8_combat_priority_coherent_invocation_review_contract()
    )
    previous_authorization = (
        prior_authorization
        .pair06_v8_combat_priority_execution_authorization_acceptance_contract()
    )

    _require(
        invocation.get("pair06_v8_combat_priority_coherent_invocation_reviewed")
        is True,
        "coherent invocation review missing",
    )
    _require(
        invocation.get("invocation_source_sha256") == INVOCATION_SOURCE_SHA256,
        "coherent invocation source drift",
    )
    _require(
        invocation.get("pair_slot") == PAIR_SLOT
        and invocation.get("arm") == ARM
        and invocation.get("held_out") is HELD_OUT,
        "coherent invocation scope drift",
    )
    _require(
        invocation.get("maximum_attempts") == 1
        and invocation.get("maximum_automatic_retries") == 0,
        "coherent invocation cardinality drift",
    )
    _require(
        invocation.get("fresh_preclaim_gpu_observation_required") is True
        and invocation.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and invocation.get("zero_foreign_cuda0_compute_processes_required")
        is True,
        "coherent fresh GPU policy drift",
    )
    _require(
        invocation.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and invocation.get("minimum_cuda0_free_memory_fraction_denominator")
        == 10,
        "coherent GPU threshold drift",
    )
    _require(
        invocation.get("fresh_evidence_namespace_required") is True
        and invocation.get("fresh_execution_authorization_required") is True
        and invocation.get("fresh_policy_activation_authorization_required")
        is True,
        "coherent fresh authority boundary drift",
    )
    _require(
        invocation.get("consumed_attempt_marker_sha256")
        == PRIOR_FAILED_ATTEMPT_MARKER_SHA256
        and invocation.get("consumed_attempt_reusable") is False
        and invocation.get("failed_run_id") == PRIOR_FAILED_RUN_ID
        and invocation.get("failed_run_reusable_as_authority") is False
        and invocation.get("prior_authorization_reusable") is False,
        "coherent consumed lineage drift",
    )
    _require(
        invocation.get("execution_authorization_accepted") is False
        and invocation.get("policy_activation_authorization_accepted") is False
        and invocation.get("attempt_marker_creation_authorized") is False
        and invocation.get("runtime_load_authorized") is False
        and invocation.get("model_inference_authorized") is False
        and invocation.get("game_execution_authorized") is False,
        "coherent invocation unexpectedly grants authority",
    )
    _require(
        invocation.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
            "EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
        ),
        "coherent request frontier drift",
    )

    _require(
        previous_authorization.get("authorization_accepted") is True
        and previous_authorization.get("execution_authorization_accepted")
        is True
        and previous_authorization.get(
            "policy_activation_authorization_accepted"
        )
        is True,
        "prior failed authorization acceptance missing",
    )
    _require(
        previous_authorization.get("authorized_request_sha256")
        == PRIOR_FAILED_REQUEST_SHA256
        and previous_authorization.get("authorized_request_bytes")
        == PRIOR_FAILED_REQUEST_BYTES
        and previous_authorization.get("authorization_text_sha256")
        == PRIOR_FAILED_AUTHORIZATION_TEXT_SHA256
        and previous_authorization.get("authorization_text_bytes")
        == PRIOR_FAILED_AUTHORIZATION_TEXT_BYTES
        and previous_authorization.get("authorized_main_head")
        == PRIOR_FAILED_AUTHORIZED_MAIN_HEAD,
        "prior failed authorization identity drift",
    )
    _require(
        previous_authorization.get(
            "execution_authorization_reusable_after_attempt_claim"
        )
        is False
        and previous_authorization.get(
            "policy_activation_authorization_reusable_after_attempt_claim"
        )
        is False,
        "prior failed authorization unexpectedly reusable",
    )

    return {
        "coherent_invocation_review": deepcopy(invocation),
        "prior_failed_authorization": deepcopy(previous_authorization),
    }


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "lineage": {
            "prior_failed_request_sha256": PRIOR_FAILED_REQUEST_SHA256,
            "prior_failed_request_bytes": PRIOR_FAILED_REQUEST_BYTES,
            "prior_failed_request_reusable": False,
            "prior_failed_authorization_text_sha256": (
                PRIOR_FAILED_AUTHORIZATION_TEXT_SHA256
            ),
            "prior_failed_authorization_text_bytes": (
                PRIOR_FAILED_AUTHORIZATION_TEXT_BYTES
            ),
            "prior_failed_authorization_reusable": False,
            "prior_failed_authorized_main_head": (
                PRIOR_FAILED_AUTHORIZED_MAIN_HEAD
            ),
            "prior_failed_attempt_marker_sha256": (
                PRIOR_FAILED_ATTEMPT_MARKER_SHA256
            ),
            "prior_failed_attempt_reusable": False,
            "prior_failed_run_id": PRIOR_FAILED_RUN_ID,
            "prior_failed_run_reusable_as_authority": False,
            "prior_failed_result_present": False,
            "prior_failed_closeout_present": False,
            "prior_failed_result_reusable_as_authority": False,
            "prior_failed_closeout_reusable_as_authority": False,
            "replacement_reason": (
                "contract_coherence_repair_requires_fresh_request_"
                "fresh_authorization_fresh_claim_and_fresh_evidence_namespace"
            ),
        },
        "source_binding": {
            "invocation_review_main_head": INVOCATION_REVIEW_MAIN_HEAD,
            "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
            "invocation_review_source_sha256": (
                INVOCATION_REVIEW_SOURCE_SHA256
            ),
            "invocation_review_test_git_blob": (
                INVOCATION_REVIEW_TEST_GIT_BLOB
            ),
            "invocation_review_test_sha256": (
                INVOCATION_REVIEW_TEST_SHA256
            ),
            "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        },
        "gpu_admission_policy": {
            "gpu_index": 0,
            "fresh_observation_required": True,
            "fresh_observation_precedes_attempt_marker": True,
            "zero_foreign_compute_processes_required": True,
            "minimum_free_memory_fraction": {
                "numerator": 9,
                "denominator": 10,
            },
            "historical_gpu_observation_reusable": False,
            "gpu_admission_hold_must_not_consume_attempt": True,
        },
        "policy_activation": {
            "policy_id": POLICY_ID,
            "policy_activation_requested": True,
            "separate_policy_activation_authorization_required": True,
            "separate_policy_confirmation_required": True,
            "request_digest_grants_policy_activation": False,
        },
        "proposed_scope": {
            "pair_slot": PAIR_SLOT,
            "arm": ARM,
            "held_out": HELD_OUT,
            "doctrine": DOCTRINE,
            "seed": SEED,
            "rounds": ROUNDS,
            "ticks_per_round": TICKS_PER_ROUND,
            "starter_infantry": STARTER_INFANTRY,
            "staging_max_ticks": STAGING_MAX_TICKS,
            "runtime_selection_key": RUNTIME_SELECTION_KEY,
            "maximum_attempts": 1,
            "maximum_automatic_retries": 0,
            "candidate_arm_included": False,
            "held_out_pair15_included": False,
            "pair03_replay_included": False,
            "pair09_replay_included": False,
        },
        "required_runtime_gates": [
            "exact_coherent_request_source_reviewed",
            "explicit_fresh_execution_authorization_accepted",
            "explicit_fresh_policy_activation_authorization_accepted",
            "exact_coherent_invocation_source_reviewed_and_canonical",
            "exact_current_main_required",
            "prior_consumed_attempt_marker_exact_and_nonreusable",
            "prior_failed_result_and_closeout_remain_absent",
            "fresh_coherent_evidence_namespace",
            "fresh_v8_environment_and_17_assets",
            "preclaim_exact_frozen_worktree_materialization",
            "fresh_cuda0_readonly_observation",
            "zero_foreign_cuda0_compute_processes",
            "minimum_90_percent_cuda0_memory_free",
            "fresh_gpu_admission_before_attempt_marker",
            "gpu_admission_hold_cleanup_without_attempt_consumption",
            "create_only_single_use_coherent_attempt_marker",
            "marker_sha256_bound_as_attempt_id",
            "authority_rechecked_after_claim",
            "authority_rechecked_before_each_inference",
            "distinct_fresh_execution_and_policy_confirmation_tokens",
            "private_child_process_group",
            "legacy_ollama_not_started_or_contacted",
            "inference_safe_no_offload_cuda0_placement_receipt_required",
            "durable_execution_result_before_worktree_cleanup",
            "success_only_owned_worktree_cleanup",
            "durable_cleanup_closeout",
        ],
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "request_validation_performs_host_io": False,
        "next_gate": NEXT_GATE,
    }


def build_pair06_v8_combat_priority_coherent_execution_authorization_request() -> bytes:
    _dependencies()
    return (
        json.dumps(
            _request_record(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def validate_pair06_v8_combat_priority_coherent_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = (
        build_pair06_v8_combat_priority_coherent_execution_authorization_request()
    )
    _require(
        payload == expected,
        "request bytes differ from fixed coherent proposal",
    )
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair06_v8_combat_priority_coherent_execution_authorization_request_contract() -> dict[str, Any]:
    payload = (
        build_pair06_v8_combat_priority_coherent_execution_authorization_request()
    )
    result = (
        validate_pair06_v8_combat_priority_coherent_execution_authorization_request(
            payload
        )
    )
    return {
        **result,
        "pair06_v8_combat_priority_coherent_execution_authorization_request_implemented": True,
        "coherent_execution_authorization_accepted": False,
        "coherent_policy_activation_authorization_accepted": False,
        "coherent_execution_authorized": False,
        "coherent_policy_activation_authorized": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "fresh_preclaim_gpu_observation_required": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_evidence_namespace_required": True,
        "prior_failed_request_reusable": False,
        "prior_failed_authorization_reusable": False,
        "prior_failed_attempt_reusable": False,
        "prior_failed_run_reusable_as_authority": False,
        "matching_request_digest_grants_authority": False,
        "request": _request_record(),
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentAuthorizationRequestHold(NEXT_GATE)
