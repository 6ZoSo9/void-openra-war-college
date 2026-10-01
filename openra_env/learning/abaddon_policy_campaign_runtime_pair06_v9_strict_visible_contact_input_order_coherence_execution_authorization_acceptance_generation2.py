"""Audit-only acceptance of one fresh Pair-06 V9 input-order execution authorization.

This record binds the user's fresh authorization text digest and byte length to
the exact reviewed input-order execution-authorization request and to canonical
War College main at authorization time.

It performs no host I/O, GPU observation, attempt claim, policy activation,
order-coherence activation, model load, inference, game execution, replay,
training, promotion, deployment, VOID-chain mutation, wallet/funds action, or
scheduler mutation.

Execution, strict-contact policy activation, and input-order-coherence
activation remain single-use and become non-reusable after the fresh create-only
attempt claim. Fresh CUDA:0 preclaim admission must still pass before any attempt
marker or runtime effect can occur.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_MAIN_HEAD = "b30533b6f3855845e24eeabc1729e8113358cdbb"
AUTHORIZED_MAIN_TREE = "d78ade6ea0a8a53634417eea424ebb0a3b1e03a5"

AUTHORIZATION_TEXT_SHA256 = (
    "ad1edd0797e2ec6d95d0a4346a09d1a6d02e7f47ba32029cd6d80ec48c532af3"
)
AUTHORIZATION_TEXT_BYTES = 13

REQUEST_REVIEW_GIT_BLOB = "19afaae0a30ddebb22e37ba7b5004d370fb97517"
REQUEST_SOURCE_GIT_BLOB = "1110cd7fc41f390f579e2207ac2fc9d0bfa4adcf"
REQUEST_TEST_GIT_BLOB = "e03d008ff79f2428994b4f877a3c0477868be632"
REQUEST_REVIEW_TEST_GIT_BLOB = "4788c6068b35bc2a71020d58ea03c424c431de85"

POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = "pair06-v9-input-order-coherence-repair-v1"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "authorized_execution_launcher"
)


class Pair06V9InputOrderCoherenceAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v9_input_order_execution_authorization_request_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_input_order_execution_authorization_request_reviewed"
        )
        is True,
        "V9 input-order execution request review missing",
    )
    _require(
        out.get("request_git_blob") == REQUEST_SOURCE_GIT_BLOB
        and out.get("request_test_git_blob") == REQUEST_TEST_GIT_BLOB,
        "V9 input-order request exact source identity drift",
    )
    _require(
        out.get("policy_id") == POLICY_ID
        and out.get("intervention_id") == INTERVENTION_ID,
        "V9 input-order authorized request identity drift",
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
        "V9 input-order authorized request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V9 input-order authorized request cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "V9 input-order authorized request GPU policy drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 input-order authorized request GPU threshold drift",
    )
    _require(
        out.get("fresh_order_evidence_namespace_required") is True
        and out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False
        and out.get("historical_v9_attempt_reusable") is False
        and out.get("historical_v9_authorization_reusable") is False,
        "V9 input-order authorized request lineage drift",
    )
    _require(
        out.get("controlled_comparison_causal_claim_made") is False,
        "V9 input-order request unexpectedly makes causal claim",
    )
    _require(
        out.get("fresh_user_authorization_text_required") is True
        and out.get("matching_request_digest_grants_authority") is False
        and out.get("request_digest_reusable_as_authorization") is False
        and out.get(
            "general_source_work_authorization_is_execution_authorization"
        )
        is False,
        "V9 input-order request authorization boundary drift",
    )
    _require(
        out.get("v9_execution_authorization_accepted") is False
        and out.get("v9_policy_activation_authorization_accepted") is False
        and out.get(
            "v9_order_coherence_activation_authorization_accepted"
        )
        is False
        and out.get("attempt_marker_creation_authorized") is False
        and out.get("runtime_load_authorized") is False
        and out.get("model_inference_authorized") is False
        and out.get("game_execution_authorized") is False,
        "V9 input-order request review unexpectedly self-authorizes execution",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "EXECUTION_AUTHORIZATION_REQUIRED"
        ),
        "V9 input-order authorization frontier drift",
    )

    return deepcopy(out)


def pair06_v9_input_order_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()

    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "authorized_request_sha256": reviewed["request_bytes_sha256"],
        "authorized_request_bytes": reviewed["request_byte_length"],
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_main_tree": AUTHORIZED_MAIN_TREE,
        "canonical_main_bound_at_authorization_time": True,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_source_git_blob": REQUEST_SOURCE_GIT_BLOB,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_review_test_git_blob": REQUEST_REVIEW_TEST_GIT_BLOB,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
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
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "gpu_admission_failure_must_not_create_attempt_marker": True,
        "gpu_admission_failure_must_not_activate_policy": True,
        "gpu_admission_failure_must_not_activate_order_coherence": True,
        "gpu_admission_failure_must_not_load_model": True,
        "gpu_admission_failure_must_not_execute_inference": True,
        "gpu_admission_failure_must_not_execute_game": True,
        "fresh_order_evidence_namespace_required": True,
        "historical_v9_attempt_reusable": False,
        "historical_v9_authorization_reusable": False,
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "controlled_comparison_causal_claim_made": False,
        "receipt_bound_preclaim_gpu_execution_authorized": True,
        "v9_policy_activation_authorized": True,
        "v9_order_coherence_activation_authorized": True,
        "attempt_marker_creation_authorized_after_fresh_gpu_admission": True,
        "policy_activation_authorized_after_fresh_gpu_admission": True,
        "order_coherence_activation_authorized_after_fresh_gpu_admission": True,
        "runtime_load_authorized_after_fresh_gpu_admission": True,
        "model_inference_authorized_after_fresh_gpu_admission": True,
        "game_execution_authorized_after_fresh_gpu_admission": True,
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
        "attempt_marker_created_by_this_record": False,
        "gpu_observation_performed_by_this_record": False,
        "policy_activation_performed_by_this_record": False,
        "order_coherence_activation_performed_by_this_record": False,
        "runtime_load_performed_by_this_record": False,
        "model_inference_performed_by_this_record": False,
        "game_execution_performed_by_this_record": False,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
        "order_coherence_activation_authorization_reusable_after_attempt_claim": False,
        "reviewed_request": reviewed,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceAuthorizationAcceptanceHold(NEXT_GATE)
