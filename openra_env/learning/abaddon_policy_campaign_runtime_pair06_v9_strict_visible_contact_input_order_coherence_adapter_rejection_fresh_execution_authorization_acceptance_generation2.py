"""Audit-only acceptance of one fresh Pair-06 V9 adapter-rejection execution.

This record binds the user's explicit authorization text to the exact reviewed
fresh execution request and to canonical War College main at authorization time.

It accepts all four reviewed authorization gates:
* execution;
* strict-contact policy activation;
* input-order-coherence activation; and
* adapter-rejection repair activation.

The record itself performs no host I/O, attempt claim, GPU observation, model
load, inference, game execution, training, deployment, chain, wallet/funds, or
scheduler mutation. One-attempt and zero-automatic-retry boundaries remain
unchanged.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_request_source_binding_review_generation2
    as request_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_requirements_source_binding_review_generation2
    as requirements_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-fresh-execution-"
    "authorization-acceptance-contract.v1"
)

AUTHORIZED_MAIN_HEAD = "e61d66b64eccc4f52a6a951e68a3df7cdf75ce0b"
AUTHORIZED_MAIN_TREE = "27f5520c3a4018a66d6cf180f80d35ef655647fe"

AUTHORIZATION_TEXT_SHA256 = (
    "2364e9c7c7e9e11d9dcdacbe68722b202eb0d5790b5d54cac6b92a995fcb94e8"
)
AUTHORIZATION_TEXT_BYTES = 286

REQUEST_REVIEW_GIT_BLOB = "ef9e2b2c638cd358c383235ca1c07845830ca421"
REQUIREMENTS_REVIEW_GIT_BLOB = "7ae9a704aec5a0f2eb39a104385d2fceee3006bb"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_authorized_execution_launcher"
)


class Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    request = (
        request_review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )
    requirements = (
        requirements_review
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_review_contract()
    )

    _require(
        request.get("pair06_v9_adapter_rejection_fresh_execution_request_reviewed")
        is True,
        "fresh execution request review missing",
    )
    _require(
        requirements.get(
            "pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_reviewed"
        )
        is True,
        "fresh execution acceptance requirements review missing",
    )
    _require(
        request.get("request_sha256") == requirements.get("reviewed_request_sha256")
        and request.get("request_bytes") == requirements.get("reviewed_request_bytes"),
        "fresh execution request identity drift",
    )
    _require(
        request.get("pair_slot") == 6
        and request.get("arm") == "baseline"
        and request.get("held_out") is False
        and request.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and request.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-retry-v1",
        "fresh execution request scope drift",
    )
    _require(
        request.get("maximum_attempts") == 1
        and request.get("maximum_automatic_retries") == 0
        and request.get("fresh_preclaim_gpu_observation_required") is True
        and request.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and request.get("zero_foreign_cuda0_compute_processes_required") is True,
        "fresh execution runtime-safety drift",
    )
    _require(
        request.get("fresh_adapter_rejection_evidence_namespace_required")
        is True
        and request.get("quadruple_explicit_authorizations_required") is True
        and request.get("quadruple_distinct_confirmation_tokens_required") is True,
        "fresh execution authorization shape drift",
    )
    _require(
        requirements.get("exact_user_authorization_text_required") is True
        and requirements.get("authorization_text_sha256_binding_required") is True
        and requirements.get("authorization_text_byte_length_binding_required")
        is True
        and requirements.get("canonical_main_head_binding_required") is True
        and requirements.get("canonical_main_tree_binding_required") is True,
        "fresh execution acceptance binding requirements drift",
    )
    for field in (
        "authorization_must_explicitly_cover_execution",
        "authorization_must_explicitly_cover_policy_activation",
        "authorization_must_explicitly_cover_order_coherence_activation",
        "authorization_must_explicitly_cover_repair_activation",
        "four_distinct_confirmation_tokens_required",
    ):
        _require(
            requirements.get(field) is True,
            "fresh execution acceptance coverage drift: " + field,
        )

    _require(
        requirements.get(
            "general_source_work_authorization_is_execution_authorization"
        )
        is False
        and requirements.get("prior_authorization_text_reusable") is False
        and requirements.get(
            "preservation_authorization_reusable_as_execution_authority"
        )
        is False,
        "fresh execution acceptance authority-reuse drift",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(
            requirements.get(field) is False,
            "fresh execution requirements unexpectedly self-authorize: " + field,
        )

    return {
        "request_review": deepcopy(request),
        "requirements_review": deepcopy(requirements),
    }


def pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    request = reviewed["request_review"]

    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "authorized_request_sha256": request["request_sha256"],
        "authorized_request_bytes": request["request_bytes"],
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_main_tree": AUTHORIZED_MAIN_TREE,
        "canonical_main_bound_at_authorization_time": True,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "requirements_review_git_blob": REQUIREMENTS_REVIEW_GIT_BLOB,
        "pair_slot": request["pair_slot"],
        "arm": request["arm"],
        "held_out": request["held_out"],
        "policy_id": request["policy_id"],
        "intervention_id": request["intervention_id"],
        "prior_attempt_marker_sha256": request["prior_attempt_marker_sha256"],
        "preservation_receipt_sha256": request["preservation_receipt_sha256"],
        "fresh_adapter_rejection_evidence_namespace_required": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "four_distinct_confirmation_tokens_required": True,
        "attempt_marker_creation_authorized_after_fresh_gpu_admission": True,
        "policy_activation_authorized_after_fresh_gpu_admission": True,
        "order_coherence_activation_authorized_after_fresh_gpu_admission": True,
        "repair_activation_authorized_after_fresh_gpu_admission": True,
        "runtime_load_authorized_after_fresh_gpu_admission": True,
        "model_inference_authorized_after_fresh_gpu_admission": True,
        "game_execution_authorized_after_fresh_gpu_admission": True,
        "gpu_admission_failure_must_not_create_attempt_marker": True,
        "gpu_admission_failure_must_not_activate_policy": True,
        "gpu_admission_failure_must_not_activate_order_coherence": True,
        "gpu_admission_failure_must_not_activate_repair": True,
        "gpu_admission_failure_must_not_load_model": True,
        "gpu_admission_failure_must_not_execute_inference": True,
        "gpu_admission_failure_must_not_execute_game": True,
        "automatic_retry": False,
        "attempt_marker_created_by_this_record": False,
        "gpu_observation_performed_by_this_record": False,
        "policy_activation_performed_by_this_record": False,
        "order_coherence_activation_performed_by_this_record": False,
        "repair_activation_performed_by_this_record": False,
        "runtime_load_performed_by_this_record": False,
        "model_inference_performed_by_this_record": False,
        "game_execution_performed_by_this_record": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
        "order_coherence_activation_authorization_reusable_after_attempt_claim": False,
        "repair_activation_authorization_reusable_after_attempt_claim": False,
        "reviewed_request": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceHold(
        NEXT_GATE
    )
