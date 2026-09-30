"""Proposal-only request for one fresh pair-06 V9 baseline run.

This request binds the reviewed V9 strict-visible-contact one-shot operator
entrypoint to one controlled baseline scope. It is a proposal only: matching
request bytes or a matching request digest grant no execution or policy-
activation authority.

The successful V8 V2 coherent run is carried forward only as a comparator and
spent, non-reusable lineage. V9 requires a fresh authorization record, fresh
preclaim CUDA:0 admission, a fresh create-only attempt marker, and a distinct
V9 evidence namespace.

This source performs no host observation, process action, attempt claim, model
load, inference, game execution, replay, training, deployment, VOID-chain
mutation, wallet/funds action, or scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_source_binding_review_generation2
    as prior_success_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_operator_entrypoint_source_binding_review_generation2
    as operator_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-no-offload-receipt-bound-preclaim-gpu-"
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
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"

CANONICAL_OPERATOR_MAIN_HEAD = "9c8bde4fa2d1ce2665b8750714840ab207fcec65"
OPERATOR_GIT_BLOB = "d2e097bfd5b3afb7cd7e0581c2496777c89d43de"
OPERATOR_REVIEW_GIT_BLOB = "7c797d9e3c045d92e64b0f9ff0910563c4662cd3"
OPERATOR_TEST_GIT_BLOB = "0e08b2ebb8c3c66fe3676513073e016304c166d2"
OPERATOR_REVIEW_TEST_GIT_BLOB = (
    "21eb6adcde08831b227c85841aa46522d765054b"
)
PRIOR_V8_SUCCESS_REVIEW_GIT_BLOB = (
    "149b04e687d16d797603701089846804a384b7ae"
)

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "v9_execution_authorization_accepted",
    "v9_policy_activation_authorization_accepted",
    "v9_execution_authorized",
    "v9_policy_activation_authorized",
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
    "scheduler_mutation_authorized",
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUEST_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_execution_authorization_"
    "request_review"
)


class Pair06V9StrictVisibleContactAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    operator = (
        operator_review
        .pair06_v9_strict_visible_contact_operator_review_contract()
    )
    prior = (
        prior_success_review
        .pair06_v8_combat_priority_coherent_v2_success_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_strict_visible_contact_operator_entrypoint_reviewed"
        )
        is True,
        "V9 operator review missing",
    )
    _require(
        operator.get("operator_git_blob") == OPERATOR_GIT_BLOB
        and operator.get("operator_test_git_blob") == OPERATOR_TEST_GIT_BLOB,
        "V9 operator source identity drift",
    )
    _require(
        operator.get("accepted_base_main_head")
        == "a016b2c0111b431e825a61417e6570654d570d96",
        "V9 operator review base drift",
    )
    _require(
        operator.get("pair_slot") == PAIR_SLOT
        and operator.get("arm") == ARM
        and operator.get("held_out") is HELD_OUT
        and operator.get("policy_id") == POLICY_ID,
        "V9 operator scope drift",
    )
    _require(
        operator.get("maximum_attempts") == 1
        and operator.get("maximum_automatic_retries") == 0,
        "V9 operator attempt cardinality drift",
    )
    _require(
        operator.get("fresh_preclaim_gpu_observation_required") is True
        and operator.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and operator.get("zero_foreign_cuda0_compute_processes_required")
        is True,
        "V9 fresh GPU policy drift",
    )
    _require(
        operator.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and operator.get("minimum_cuda0_free_memory_fraction_denominator")
        == 10,
        "V9 GPU threshold drift",
    )
    _require(
        operator.get("fresh_v9_evidence_namespace_required") is True
        and operator.get("prior_v8_v2_attempt_reusable") is False
        and operator.get("prior_v8_v2_authorization_reusable") is False,
        "V9 evidence/lineage boundary drift",
    )
    _require(
        operator.get("dual_explicit_authorizations_required") is True
        and operator.get("dual_distinct_confirmation_tokens_required") is True,
        "V9 dual authorization boundary drift",
    )
    _require(
        operator.get("execution_authorization_accepted") is False
        and operator.get("policy_activation_authorization_accepted") is False
        and operator.get("attempt_marker_creation_authorized") is False
        and operator.get("runtime_load_authorized") is False
        and operator.get("model_inference_authorized") is False
        and operator.get("game_execution_authorized") is False,
        "V9 operator review unexpectedly grants authority",
    )
    _require(
        operator.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
        "V9 request frontier drift",
    )

    _require(
        prior.get(
            "pair06_v8_combat_priority_coherent_v2_success_reviewed"
        )
        is True,
        "prior V8 V2 success review missing",
    )
    _require(
        prior.get("rounds_completed") == ROUNDS
        and prior.get("outcome") == "DRAW_OR_UNFINISHED",
        "prior V8 comparator scope drift",
    )
    _require(
        prior.get("attempt_consumed") is True
        and prior.get("attempt_reusable") is False
        and prior.get("authorization_reusable") is False
        and prior.get("automatic_retry") is False
        and prior.get("lineage_closed") is True,
        "prior V8 success lineage unexpectedly reusable",
    )

    return {
        "v9_operator_review": deepcopy(operator),
        "prior_v8_v2_success_review": deepcopy(prior),
    }


def _request_record() -> dict[str, Any]:
    dependencies = _dependencies()
    prior = dependencies["prior_v8_v2_success_review"]

    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_binding": {
            "canonical_operator_main_head": CANONICAL_OPERATOR_MAIN_HEAD,
            "operator_git_blob": OPERATOR_GIT_BLOB,
            "operator_review_git_blob": OPERATOR_REVIEW_GIT_BLOB,
            "operator_test_git_blob": OPERATOR_TEST_GIT_BLOB,
            "operator_review_test_git_blob": OPERATOR_REVIEW_TEST_GIT_BLOB,
        },
        "lineage": {
            "prior_v8_success_review_git_blob": (
                PRIOR_V8_SUCCESS_REVIEW_GIT_BLOB
            ),
            "prior_v8_v2_run_id": prior["run_id"],
            "prior_v8_v2_attempt_marker_sha256": (
                prior["attempt_marker_sha256"]
            ),
            "prior_v8_v2_result_file_sha256": prior["result_file_sha256"],
            "prior_v8_v2_closeout_file_sha256": prior["closeout_file_sha256"],
            "prior_v8_v2_outcome": prior["outcome"],
            "prior_v8_v2_rounds_completed": prior["rounds_completed"],
            "prior_v8_v2_final_tick": prior["final_tick"],
            "prior_v8_v2_attempt_consumed": True,
            "prior_v8_v2_attempt_reusable": False,
            "prior_v8_v2_authorization_reusable": False,
            "prior_v8_v2_result_reusable_as_authority": False,
            "prior_v8_v2_closeout_reusable_as_authority": False,
            "prior_v8_v2_lineage_closed": True,
            "replacement_reason": (
                "v9_strict_visible_contact_hypothesis_requires_fresh_request_"
                "fresh_authorization_fresh_claim_and_fresh_evidence_namespace"
            ),
        },
        "controlled_comparison": {
            "comparator_policy_id": (
                "pair06-v8-combat-action-priority-envelope-v1"
            ),
            "candidate_policy_id": POLICY_ID,
            "same_pair_slot": True,
            "same_arm": True,
            "same_doctrine": True,
            "same_seed": True,
            "same_round_budget": True,
            "same_tick_budget": True,
            "same_starter_infantry": True,
            "same_runtime_selection": True,
            "causal_claim_made": False,
            "purpose": (
                "measure_v9_strict_visible_contact_behavior_against_reviewed_"
                "v8_v2_comparator_under_matched_scope"
            ),
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
            "exact_v9_request_source_reviewed",
            "fresh_explicit_v9_execution_authorization_accepted",
            "fresh_explicit_v9_policy_activation_authorization_accepted",
            "exact_v9_operator_source_reviewed_and_canonical",
            "exact_current_main_required",
            "prior_v8_v2_success_lineage_exact_and_nonreusable",
            "fresh_v9_evidence_namespace",
            "fresh_v8_environment_and_17_assets",
            "preclaim_exact_frozen_worktree_materialization",
            "fresh_cuda0_readonly_observation",
            "zero_foreign_cuda0_compute_processes",
            "minimum_90_percent_cuda0_memory_free",
            "fresh_gpu_admission_before_attempt_marker",
            "gpu_admission_hold_cleanup_without_attempt_consumption",
            "create_only_single_use_v9_attempt_marker",
            "marker_sha256_bound_as_attempt_id",
            "authority_rechecked_after_claim",
            "authority_rechecked_before_each_inference",
            "distinct_fresh_execution_and_v9_policy_confirmation_tokens",
            "private_child_process_group",
            "legacy_ollama_not_started_or_contacted",
            "inference_safe_no_offload_cuda0_placement_receipt_required",
            "durable_execution_result_before_worktree_cleanup",
            "success_only_owned_worktree_cleanup",
            "durable_cleanup_closeout",
        ],
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "request_digest_reusable_as_authorization": False,
        "fresh_user_authorization_text_required": True,
        "request_validation_performs_host_io": False,
        "next_gate": NEXT_GATE,
    }


def build_pair06_v9_execution_authorization_request() -> bytes:
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


def validate_pair06_v9_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v9_execution_authorization_request()
    _require(
        payload == expected,
        "request bytes differ from fixed V9 proposal",
    )
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "fresh_user_authorization_text_required": True,
        "next_gate": NEXT_GATE,
    }


def pair06_v9_execution_authorization_request_contract() -> dict[str, Any]:
    payload = build_pair06_v9_execution_authorization_request()
    result = validate_pair06_v9_execution_authorization_request(payload)

    return {
        **result,
        "pair06_v9_execution_authorization_request_implemented": True,
        "policy_id": POLICY_ID,
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
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_v9_evidence_namespace_required": True,
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "controlled_comparison_causal_claim_made": False,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "fresh_user_authorization_text_required": True,
        "matching_request_digest_grants_authority": False,
        "request_digest_reusable_as_authorization": False,
        "v9_execution_authorization_accepted": False,
        "v9_policy_activation_authorization_accepted": False,
        "v9_execution_authorized": False,
        "v9_policy_activation_authorized": False,
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
        "scheduler_mutation_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "request": _request_record(),
        "dependencies": _dependencies(),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactAuthorizationRequestHold(NEXT_GATE)
