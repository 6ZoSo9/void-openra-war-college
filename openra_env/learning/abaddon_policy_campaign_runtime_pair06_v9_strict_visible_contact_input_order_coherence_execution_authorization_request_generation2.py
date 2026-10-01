"""Proposal-only request for one fresh Pair-06 V9 input-order-coherence run.

This request binds the exact reviewed input-order-coherence one-shot operator to
one controlled baseline scope. It is a proposal only: matching request bytes or
a matching digest grant no execution, strict-contact policy activation, or
input-order-coherence activation authority.

The reviewed V8 V2 run is carried only as a non-causal comparator with spent,
non-reusable lineage. The historical V9 lane is also explicitly non-reusable.
A later execution would require fresh explicit authorization text, fresh CUDA:0
preclaim admission, a fresh create-only attempt marker, and the fresh
order-coherence evidence namespace.

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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_operator_entrypoint_source_binding_review_generation2
    as operator_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-no-offload-"
    "receipt-bound-preclaim-gpu-baseline-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-no-offload-"
    "receipt-bound-preclaim-gpu-baseline-execution-authorization-request-"
    "validation.v1"
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
INTERVENTION_ID = "pair06-v9-input-order-coherence-repair-v1"

REVIEWED_OPERATOR_STACK_HEAD = "23dabde76ef494e741294bf7c4ed210af5ce45a9"
OPERATOR_GIT_BLOB = "2a1e9d04b0a877ad4afb4f99f831b7824c5fb59a"
OPERATOR_REVIEW_GIT_BLOB = "2538f3c191e7a9826df0415583cac1021783a659"
OPERATOR_TEST_GIT_BLOB = "eb46654b9f96895c7ef553c5fe13d59e21f5b3cb"
OPERATOR_REVIEW_TEST_GIT_BLOB = "4b90e4d542401eedad0e33369ed6f370bca5917f"
PRIOR_V8_SUCCESS_REVIEW_GIT_BLOB = (
    "149b04e687d16d797603701089846804a384b7ae"
)

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "v9_execution_authorization_accepted",
    "v9_policy_activation_authorization_accepted",
    "v9_order_coherence_activation_authorization_accepted",
    "v9_execution_authorized",
    "v9_policy_activation_authorized",
    "v9_order_coherence_activation_authorized",
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
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "execution_authorization_request_review"
)


class Pair06V9InputOrderCoherenceAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceAuthorizationRequestHold(message)


def _dependencies() -> dict[str, Any]:
    operator = (
        operator_review
        .pair06_v9_input_order_coherence_operator_review_contract()
    )
    prior = (
        prior_success_review
        .pair06_v8_combat_priority_coherent_v2_success_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_input_order_coherence_operator_entrypoint_reviewed"
        )
        is True,
        "V9 input-order operator review missing",
    )
    _require(
        operator.get("operator_git_blob") == OPERATOR_GIT_BLOB
        and operator.get("operator_test_git_blob") == OPERATOR_TEST_GIT_BLOB,
        "V9 input-order operator source identity drift",
    )
    _require(
        operator.get("accepted_base_head")
        == "51a6ba125db8d3c7c5209aa4b37062389ea8b979",
        "V9 input-order operator review predecessor drift",
    )
    _require(
        operator.get("pair_slot") == PAIR_SLOT
        and operator.get("arm") == ARM
        and operator.get("held_out") is HELD_OUT
        and operator.get("policy_id") == POLICY_ID,
        "V9 input-order operator scope drift",
    )
    _require(
        operator.get("maximum_attempts") == 1
        and operator.get("maximum_automatic_retries") == 0,
        "V9 input-order operator attempt cardinality drift",
    )
    _require(
        operator.get("fresh_preclaim_gpu_observation_required") is True
        and operator.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and operator.get("zero_foreign_cuda0_compute_processes_required")
        is True,
        "V9 input-order fresh GPU policy drift",
    )
    _require(
        operator.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and operator.get("minimum_cuda0_free_memory_fraction_denominator")
        == 10,
        "V9 input-order GPU threshold drift",
    )
    _require(
        operator.get("fresh_order_evidence_namespace_required") is True
        and operator.get("historical_v9_attempt_reusable") is False
        and operator.get("historical_v9_authorization_reusable") is False,
        "V9 input-order evidence/historical-lineage boundary drift",
    )
    _require(
        operator.get("triple_explicit_authorizations_required") is True
        and operator.get("triple_distinct_confirmation_tokens_required")
        is True,
        "V9 input-order triple authorization boundary drift",
    )
    _require(
        operator.get("execution_authorization_accepted") is False
        and operator.get("policy_activation_authorization_accepted") is False
        and operator.get("order_coherence_activation_authorization_accepted")
        is False
        and operator.get("attempt_marker_creation_authorized") is False
        and operator.get("runtime_load_authorized") is False
        and operator.get("model_inference_authorized") is False
        and operator.get("game_execution_authorized") is False,
        "V9 input-order operator review unexpectedly grants authority",
    )
    _require(
        operator.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
        ),
        "V9 input-order request frontier drift",
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
        "input_order_operator_review": deepcopy(operator),
        "prior_v8_v2_success_review": deepcopy(prior),
    }


def _request_record() -> dict[str, Any]:
    dependencies = _dependencies()
    prior = dependencies["prior_v8_v2_success_review"]

    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_binding": {
            "reviewed_operator_stack_head": REVIEWED_OPERATOR_STACK_HEAD,
            "operator_git_blob": OPERATOR_GIT_BLOB,
            "operator_review_git_blob": OPERATOR_REVIEW_GIT_BLOB,
            "operator_test_git_blob": OPERATOR_TEST_GIT_BLOB,
            "operator_review_test_git_blob": OPERATOR_REVIEW_TEST_GIT_BLOB,
            "canonical_main_must_be_bound_by_later_authorization": True,
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
            "historical_v9_attempt_reusable": False,
            "historical_v9_authorization_reusable": False,
            "replacement_reason": (
                "input_order_coherence_repair_requires_fresh_request_fresh_"
                "authorization_fresh_claim_and_fresh_evidence_namespace"
            ),
        },
        "controlled_comparison": {
            "comparator_policy_id": (
                "pair06-v8-combat-action-priority-envelope-v1"
            ),
            "candidate_policy_id": POLICY_ID,
            "candidate_intervention_id": INTERVENTION_ID,
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
                "measure_reviewed_input_order_coherence_repair_under_matched_"
                "pair06_baseline_scope"
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
        "activation": {
            "policy_id": POLICY_ID,
            "intervention_id": INTERVENTION_ID,
            "strict_contact_policy_activation_requested": True,
            "order_coherence_activation_requested": True,
            "separate_policy_activation_authorization_required": True,
            "separate_order_coherence_activation_authorization_required": True,
            "separate_policy_confirmation_required": True,
            "separate_order_coherence_confirmation_required": True,
            "request_digest_grants_any_activation": False,
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
            "exact_input_order_request_source_reviewed",
            "fresh_explicit_execution_authorization_accepted",
            "fresh_explicit_v9_policy_activation_authorization_accepted",
            "fresh_explicit_order_coherence_activation_authorization_accepted",
            "exact_input_order_operator_source_reviewed",
            "later_authorization_binds_exact_canonical_main",
            "prior_v8_v2_success_lineage_exact_and_nonreusable",
            "historical_v9_lineage_nonreusable",
            "fresh_order_coherence_evidence_namespace",
            "fresh_v8_environment_and_17_assets",
            "preclaim_exact_frozen_worktree_materialization",
            "fresh_cuda0_readonly_observation",
            "zero_foreign_cuda0_compute_processes",
            "minimum_90_percent_cuda0_memory_free",
            "fresh_gpu_admission_before_attempt_marker",
            "gpu_admission_hold_cleanup_without_attempt_consumption",
            "create_only_single_use_order_coherence_attempt_marker",
            "marker_sha256_bound_as_attempt_id",
            "authority_rechecked_after_claim",
            "authority_rechecked_before_each_inference",
            "three_distinct_fresh_confirmation_tokens",
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
        "general_source_work_authorization_is_execution_authorization": False,
        "request_validation_performs_host_io": False,
        "next_gate": NEXT_GATE,
    }


def build_pair06_v9_input_order_execution_authorization_request() -> bytes:
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


def validate_pair06_v9_input_order_execution_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "request must be exact bytes")
    _require(0 < len(payload) <= MAX_REQUEST_BYTES, "request byte limit")
    expected = build_pair06_v9_input_order_execution_authorization_request()
    _require(
        payload == expected,
        "request bytes differ from fixed input-order proposal",
    )
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "fresh_user_authorization_text_required": True,
        "general_source_work_authorization_is_execution_authorization": False,
        "next_gate": NEXT_GATE,
    }


def pair06_v9_input_order_execution_authorization_request_contract() -> dict[str, Any]:
    payload = build_pair06_v9_input_order_execution_authorization_request()
    result = validate_pair06_v9_input_order_execution_authorization_request(payload)

    return {
        **result,
        "pair06_v9_input_order_execution_authorization_request_implemented": True,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
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
        "reviewed_operator_stack_head": REVIEWED_OPERATOR_STACK_HEAD,
        "canonical_main_must_be_bound_by_later_authorization": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_order_evidence_namespace_required": True,
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "historical_v9_attempt_reusable": False,
        "historical_v9_authorization_reusable": False,
        "controlled_comparison_causal_claim_made": False,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "fresh_order_coherence_activation_authorization_required": True,
        "fresh_user_authorization_text_required": True,
        "matching_request_digest_grants_authority": False,
        "request_digest_reusable_as_authorization": False,
        "general_source_work_authorization_is_execution_authorization": False,
        "v9_execution_authorization_accepted": False,
        "v9_policy_activation_authorization_accepted": False,
        "v9_order_coherence_activation_authorization_accepted": False,
        "v9_execution_authorized": False,
        "v9_policy_activation_authorized": False,
        "v9_order_coherence_activation_authorized": False,
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
    raise Pair06V9InputOrderCoherenceAuthorizationRequestHold(NEXT_GATE)
