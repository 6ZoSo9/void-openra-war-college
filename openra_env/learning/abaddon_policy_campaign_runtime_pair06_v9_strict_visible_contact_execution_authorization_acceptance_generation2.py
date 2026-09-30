"""Audit-only acceptance of one fresh pair-06 V9 execution authorization.

This record binds the user's fresh authorization text digest and byte length to
the exact reviewed V9 execution-authorization request merged by PR #335 and to
War College main at authorization time.

It performs no host I/O, GPU observation, attempt claim, policy activation,
model load, inference, game execution, replay, training, promotion, deployment,
VOID-chain mutation, wallet/funds action, or scheduler mutation.

Execution and V9 policy activation remain single-use and become non-reusable
after the fresh create-only attempt claim. Fresh CUDA:0 preclaim admission must
still pass before the attempt marker can be created or runtime effects can occur.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-execution-authorization-"
    "acceptance-contract.v1"
)

AUTHORIZED_MAIN_HEAD = "bfe8f06245ed2951d247973df927a756a37cfbfd"

AUTHORIZATION_TEXT_SHA256 = (
    "d41fd580d15b4d59491fbb7a2b635946656bbb6c6ae61bcc9222085e23a45bd6"
)
AUTHORIZATION_TEXT_BYTES = 362

REQUEST_REVIEW_GIT_BLOB = "8565d587e57335a2a30940effa40713ae6a7315a"
REQUEST_SOURCE_GIT_BLOB = "1fcc9968ae6032613096fdbcd9550ca718cd257f"
REQUEST_TEST_GIT_BLOB = "b8737c0040de2e2f0e3437f9b9496c18ba17408a"
REQUEST_REVIEW_TEST_GIT_BLOB = (
    "9a5f805ca434411f40f9a222e36426a62705f6bf"
)

POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_RECEIPT_BOUND_PRECLAIM_GPU_"
    "EXECUTION_AUTHORIZED"
)


class Pair06V9StrictVisibleContactAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactAuthorizationAcceptanceHold(message)


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = request_review.pair06_v9_execution_authorization_request_review_contract()

    _require(
        out.get("pair06_v9_execution_authorization_request_reviewed") is True,
        "V9 execution request review missing",
    )
    _require(
        out.get("request_git_blob") == REQUEST_SOURCE_GIT_BLOB
        and out.get("request_test_git_blob") == REQUEST_TEST_GIT_BLOB,
        "V9 request exact source identity drift",
    )
    _require(
        out.get("policy_id") == POLICY_ID,
        "V9 authorized request policy drift",
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
        "V9 authorized request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V9 authorized request cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "V9 authorized request GPU policy drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 authorized request GPU threshold drift",
    )
    _require(
        out.get("fresh_v9_evidence_namespace_required") is True
        and out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False,
        "V9 authorized request lineage drift",
    )
    _require(
        out.get("controlled_comparison_causal_claim_made") is False,
        "V9 request unexpectedly makes causal claim",
    )
    _require(
        out.get("fresh_user_authorization_text_required") is True
        and out.get("matching_request_digest_grants_authority") is False
        and out.get("request_digest_reusable_as_authorization") is False,
        "V9 request authorization boundary drift",
    )
    _require(
        out.get("v9_execution_authorization_accepted") is False
        and out.get("v9_policy_activation_authorization_accepted") is False
        and out.get("attempt_marker_creation_authorized") is False
        and out.get("runtime_load_authorized") is False
        and out.get("model_inference_authorized") is False
        and out.get("game_execution_authorized") is False,
        "V9 request review unexpectedly self-authorizes execution",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUIRED",
        "V9 authorization frontier drift",
    )

    return deepcopy(out)


def pair06_v9_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()

    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "authorized_request_sha256": reviewed["request_bytes_sha256"],
        "authorized_request_bytes": reviewed["request_byte_length"],
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_source_git_blob": REQUEST_SOURCE_GIT_BLOB,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_review_test_git_blob": REQUEST_REVIEW_TEST_GIT_BLOB,
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
        "fresh_v9_evidence_namespace_required": True,
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "controlled_comparison_causal_claim_made": False,
        "receipt_bound_preclaim_gpu_execution_authorized": True,
        "v9_policy_activation_authorized": True,
        "attempt_marker_creation_authorized_after_fresh_gpu_admission": True,
        "policy_activation_authorized_after_fresh_gpu_admission": True,
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
        "runtime_load_performed_by_this_record": False,
        "model_inference_performed_by_this_record": False,
        "game_execution_performed_by_this_record": False,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
        "reviewed_request": reviewed,
        "next_gate": NEXT_GATE,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactAuthorizationAcceptanceHold(NEXT_GATE)
