"""Exact-blob review of the pair-06 V9 authorization acceptance record.

Pins the audit-only authorization acceptance source and tests to exact
repository bytes. The review confirms that the fresh user authorization is
bound by digest/length to the exact reviewed V9 request and canonical main at
authorization time.

The record itself performs no GPU observation, attempt claim, policy activation,
model load, inference, game execution, replay, training, promotion, deployment,
VOID-chain mutation, wallet/funds action, or scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_execution_authorization_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-execution-authorization-"
    "acceptance-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "bfe8f06245ed2951d247973df927a756a37cfbfd"
ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_GIT_BLOB = "0b72636735120e8ebf7df101b05c46d41c4ba2f0"
ACCEPTANCE_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_TEST_GIT_BLOB = "d381a1a5ac56361b6c2a4e33d54c7644c2710be6"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_RECEIPT_BOUND_PRECLAIM_GPU_"
    "EXECUTION_AUTHORIZED"
)
NEXT_CHANGE_CLASS = (
    "runtime_pair06_v9_strict_visible_contact_receipt_bound_preclaim_gpu_"
    "execution"
)


class Pair06V9StrictVisibleContactAuthorizationAcceptanceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactAuthorizationAcceptanceReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

    _require(
        out.get("authorization_record_kind") == "explicit_user_authorization"
        and out.get("authorization_accepted") is True
        and out.get("execution_authorization_accepted") is True
        and out.get("policy_activation_authorization_accepted") is True,
        "V9 authorization acceptance missing",
    )
    _require(
        out.get("authorized_main_head")
        == "bfe8f06245ed2951d247973df927a756a37cfbfd",
        "V9 authorized main drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "d41fd580d15b4d59491fbb7a2b635946656bbb6c6ae61bcc9222085e23a45bd6"
        and out.get("authorization_text_bytes") == 362,
        "V9 authorization text binding drift",
    )
    _require(
        out.get("request_review_git_blob")
        == "8565d587e57335a2a30940effa40713ae6a7315a"
        and out.get("request_source_git_blob")
        == "1fcc9968ae6032613096fdbcd9550ca718cd257f"
        and out.get("request_test_git_blob")
        == "b8737c0040de2e2f0e3437f9b9496c18ba17408a"
        and out.get("request_review_test_git_blob")
        == "9a5f805ca434411f40f9a222e36426a62705f6bf",
        "V9 reviewed request source binding drift",
    )
    _require(
        out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("pair_slot") == 6
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
        "V9 accepted scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("automatic_retry") is False,
        "V9 accepted attempt cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True
        and out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 accepted GPU admission policy drift",
    )
    for field in (
        "gpu_admission_failure_must_not_create_attempt_marker",
        "gpu_admission_failure_must_not_activate_policy",
        "gpu_admission_failure_must_not_load_model",
        "gpu_admission_failure_must_not_execute_inference",
        "gpu_admission_failure_must_not_execute_game",
        "fresh_v9_evidence_namespace_required",
        "receipt_bound_preclaim_gpu_execution_authorized",
        "v9_policy_activation_authorized",
        "attempt_marker_creation_authorized_after_fresh_gpu_admission",
        "policy_activation_authorized_after_fresh_gpu_admission",
        "runtime_load_authorized_after_fresh_gpu_admission",
        "model_inference_authorized_after_fresh_gpu_admission",
        "game_execution_authorized_after_fresh_gpu_admission",
    ):
        _require(
            out.get(field) is True,
            "V9 acceptance invariant drift: " + field,
        )
    _require(
        out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False
        and out.get("controlled_comparison_causal_claim_made") is False,
        "V9 predecessor/comparison boundary drift",
    )
    for field in (
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
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
    ):
        _require(
            out.get(field) is False,
            "V9 acceptance effect boundary drift: " + field,
        )
    _require(
        out.get("execution_authorization_reusable_after_attempt_claim") is False
        and out.get("policy_activation_authorization_reusable_after_attempt_claim")
        is False,
        "V9 authorization reuse boundary drift",
    )
    _require(
        out.get("next_gate") == NEXT_GATE,
        "V9 acceptance next gate drift",
    )

    return deepcopy(out)


def pair06_v9_execution_authorization_acceptance_review_contract() -> dict[str, Any]:
    validated = _validated()

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "acceptance_path": ACCEPTANCE_PATH,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_test_path": ACCEPTANCE_TEST_PATH,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "pair06_v9_execution_authorization_acceptance_reviewed": True,
        "authorization_text_sha256": validated["authorization_text_sha256"],
        "authorization_text_bytes": validated["authorization_text_bytes"],
        "authorized_request_sha256": validated["authorized_request_sha256"],
        "authorized_request_bytes": validated["authorized_request_bytes"],
        "authorized_main_head": validated["authorized_main_head"],
        "policy_id": validated["policy_id"],
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_v9_evidence_namespace_required": True,
        "receipt_bound_preclaim_gpu_execution_authorized": True,
        "v9_policy_activation_authorized": True,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
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
        "validated_acceptance": validated,
        "source_frontier_closed": True,
        "execution_blockers": (
            "fresh_preclaim_gpu_admission",
            "exact_current_main",
            "exact_operator_source",
            "fresh_create_only_v9_attempt_marker",
        ),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactAuthorizationAcceptanceReviewHold(NEXT_GATE)
