"""Proposal-only request for one combat-priority pair-06 V8 baseline run.

This request binds the reviewed combat-priority receipt-bound/no-offload/fresh
preclaim-GPU invocation. It is a proposal only: matching request bytes or a
matching request digest grant no authority.

The prior successful GPU-gated pair-06 request, its explicit authorization, its
consumed attempt marker, result, and closeout are carried forward as spent and
non-reusable lineage. The earlier OOM attempt marker is also non-reusable.

This source performs no host observation, process action, attempt claim, model
load, inference, game execution, training, deployment, VOID-chain mutation, or
wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as invocation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_authorization_acceptance_generation2
    as prior_authorization,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_result_source_binding_review_generation2
    as prior_result_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request-validation.v1"
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

INVOCATION_REVIEW_MAIN_HEAD = "3bdc27aca30e0926626410bbedc7d445f4a3dd77"
INVOCATION_REVIEW_GIT_BLOB = "222db31907543f2b776d811f309488e8dc95706a"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "297b53a9f934722c0f1f355e52776c40bd9923e0cd5fbb30cca9c427f2a5f7f2"
)
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
PRIOR_EXECUTION_RESULT_REVIEW_GIT_BLOB = (
    "2ca3aa48919193ed57703a6446372cb4ae6414c7"
)
PRIOR_EXECUTION_RESULT_REVIEW_SOURCE_SHA256 = (
    "3d660037674b0ab39d5cc37dd8db3b3eb1e92dc08a54845fd88ced7f0b8aea3d"
)

EARLIER_RECEIPT_BOUND_REQUEST_SHA256 = (
    "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
)
SPENT_OOM_ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "combat_priority_execution_authorization_accepted",
    "combat_priority_policy_activation_authorization_accepted",
    "combat_priority_execution_authorized",
    "combat_priority_policy_activation_authorized",
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
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
    "BASELINE_EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_no_offload_"
    "receipt_bound_preclaim_gpu_baseline_execution_authorization_request_review"
)


class Pair06V8CombatPriorityExecutionAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityExecutionAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    invocation = (
        invocation_review
        .pair06_v8_combat_priority_baseline_attempt_invocation_review_contract()
    )
    previous_result = (
        prior_result_review
        .pair06_v8_preclaim_gpu_execution_result_review_contract()
    )
    previous_authorization = (
        prior_authorization
        .pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    )

    _require(
        invocation.get(
            "pair06_v8_combat_priority_baseline_attempt_invocation_reviewed"
        )
        is True,
        "combat-priority invocation review missing",
    )
    _require(
        invocation.get("invocation_source_sha256") == INVOCATION_SOURCE_SHA256,
        "combat-priority invocation source drift",
    )
    _require(
        invocation.get("pair_slot") == PAIR_SLOT
        and invocation.get("arm") == ARM
        and invocation.get("held_out") is HELD_OUT,
        "combat-priority invocation scope drift",
    )
    _require(
        invocation.get("maximum_attempts") == 1
        and invocation.get("maximum_automatic_retries") == 0,
        "combat-priority invocation cardinality drift",
    )
    _require(
        invocation.get("fresh_preclaim_gpu_observation_required") is True
        and invocation.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True,
        "combat-priority fresh GPU observation policy drift",
    )
    _require(
        invocation.get("zero_foreign_cuda0_compute_processes_required") is True
        and invocation.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and invocation.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "combat-priority GPU admission policy drift",
    )
    _require(
        invocation.get(
            "combat_priority_evidence_namespace_distinct_from_spent_baseline"
        )
        is True,
        "combat-priority evidence namespace drift",
    )
    _require(
        invocation.get("explicit_execution_authorization_required") is True
        and invocation.get("explicit_policy_activation_authorization_required")
        is True
        and invocation.get(
            "distinct_execution_and_policy_confirmations_required"
        )
        is True,
        "combat-priority dual authorization boundary drift",
    )
    _require(
        invocation.get("attempt_marker_creation_authorized") is False
        and invocation.get("runtime_load_authorized") is False
        and invocation.get("model_inference_authorized") is False
        and invocation.get("game_execution_authorized") is False,
        "combat-priority invocation unexpectedly grants authority",
    )
    _require(
        invocation.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
            "BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
        ),
        "combat-priority request frontier drift",
    )

    _require(
        previous_result.get("pair06_v8_preclaim_gpu_execution_result_reviewed")
        is True,
        "prior successful execution result review missing",
    )
    _require(
        previous_result.get("authorized_request_sha256")
        == PRIOR_SPENT_REQUEST_SHA256,
        "prior spent request drift",
    )
    _require(
        previous_result.get("attempt_marker_sha256")
        == PRIOR_ATTEMPT_MARKER_SHA256
        and previous_result.get("result_file_sha256")
        == PRIOR_RESULT_FILE_SHA256
        and previous_result.get("closeout_file_sha256")
        == PRIOR_CLOSEOUT_FILE_SHA256,
        "prior successful evidence drift",
    )
    _require(
        previous_result.get("attempt_consumed") is True
        and previous_result.get("authorization_reusable") is False
        and previous_result.get("automatic_retry_performed") is False,
        "prior successful attempt reuse state drift",
    )

    _require(
        previous_authorization.get("authorization_accepted") is True
        and previous_authorization.get("authorized_request_sha256")
        == PRIOR_SPENT_REQUEST_SHA256
        and previous_authorization.get("authorization_text_sha256")
        == PRIOR_AUTHORIZATION_TEXT_SHA256,
        "prior explicit authorization drift",
    )
    _require(
        previous_authorization.get("authorization_reusable_after_attempt_claim")
        is False,
        "prior explicit authorization unexpectedly reusable",
    )

    return {
        "combat_priority_invocation_review": deepcopy(invocation),
        "prior_successful_execution_result_review": deepcopy(previous_result),
        "prior_successful_authorization": deepcopy(previous_authorization),
    }


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "lineage": {
            "prior_spent_gpu_gated_request_sha256": (
                PRIOR_SPENT_REQUEST_SHA256
            ),
            "prior_spent_authorization_text_sha256": (
                PRIOR_AUTHORIZATION_TEXT_SHA256
            ),
            "prior_spent_attempt_marker_sha256": (
                PRIOR_ATTEMPT_MARKER_SHA256
            ),
            "prior_result_file_sha256": PRIOR_RESULT_FILE_SHA256,
            "prior_closeout_file_sha256": PRIOR_CLOSEOUT_FILE_SHA256,
            "earlier_receipt_bound_request_sha256": (
                EARLIER_RECEIPT_BOUND_REQUEST_SHA256
            ),
            "spent_oom_attempt_marker_sha256": (
                SPENT_OOM_ATTEMPT_MARKER_SHA256
            ),
            "prior_spent_gpu_gated_request_reusable": False,
            "prior_spent_authorization_reusable": False,
            "prior_spent_attempt_reusable": False,
            "prior_result_reusable_as_authority": False,
            "prior_closeout_reusable_as_authority": False,
            "earlier_receipt_bound_request_reusable": False,
            "spent_oom_attempt_reusable": False,
            "prior_successful_attempt_consumed": True,
            "prior_successful_execution_result_review_git_blob": (
                PRIOR_EXECUTION_RESULT_REVIEW_GIT_BLOB
            ),
            "prior_successful_execution_result_review_source_sha256": (
                PRIOR_EXECUTION_RESULT_REVIEW_SOURCE_SHA256
            ),
            "replacement_reason": (
                "reviewed_combat_action_priority_policy_requires_fresh_request_"
                "fresh_claim_and_distinct_evidence_namespace"
            ),
        },
        "source_binding": {
            "invocation_review_main_head": INVOCATION_REVIEW_MAIN_HEAD,
            "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
            "invocation_review_source_sha256": (
                INVOCATION_REVIEW_SOURCE_SHA256
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
            "policy_id": "pair06-v8-combat-action-priority-envelope-v1",
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
            "exact_combat_priority_request_source_reviewed",
            "explicit_combat_priority_execution_authorization_accepted",
            "explicit_combat_priority_policy_activation_authorization_accepted",
            "exact_combat_priority_invocation_source_reviewed_and_canonical",
            "exact_current_main_required",
            "fresh_combat_priority_evidence_namespace",
            "fresh_v8_environment_and_17_assets",
            "preclaim_exact_frozen_worktree_materialization",
            "fresh_cuda0_readonly_observation",
            "zero_foreign_cuda0_compute_processes",
            "minimum_90_percent_cuda0_memory_free",
            "fresh_gpu_admission_before_attempt_marker",
            "gpu_admission_hold_cleanup_without_attempt_consumption",
            "create_only_single_use_combat_priority_attempt_marker",
            "marker_sha256_bound_as_attempt_id",
            "authority_rechecked_after_claim",
            "authority_rechecked_before_each_inference",
            "separate_execution_and_policy_confirmation_tokens",
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


def build_pair06_v8_combat_priority_execution_authorization_request() -> bytes:
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


def validate_pair06_v8_combat_priority_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v8_combat_priority_execution_authorization_request()
    _require(
        payload == expected,
        "request bytes differ from fixed combat-priority proposal",
    )
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair06_v8_combat_priority_execution_authorization_request_contract() -> dict[str, Any]:
    payload = build_pair06_v8_combat_priority_execution_authorization_request()
    result = validate_pair06_v8_combat_priority_execution_authorization_request(
        payload
    )
    return {
        **result,
        "pair06_v8_combat_priority_execution_authorization_request_implemented": True,
        "combat_priority_execution_authorization_accepted": False,
        "combat_priority_policy_activation_authorization_accepted": False,
        "combat_priority_execution_authorized": False,
        "combat_priority_policy_activation_authorized": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "prior_spent_request_reusable": False,
        "prior_spent_authorization_reusable": False,
        "prior_spent_attempt_reusable": False,
        "fresh_preclaim_gpu_observation_required": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "matching_request_digest_grants_authority": False,
        "request": _request_record(),
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityExecutionAuthorizationRequestHold(NEXT_GATE)
