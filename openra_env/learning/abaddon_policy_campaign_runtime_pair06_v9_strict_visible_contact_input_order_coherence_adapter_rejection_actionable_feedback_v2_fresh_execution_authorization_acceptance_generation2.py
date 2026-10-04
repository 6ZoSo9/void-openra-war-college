"""Audit-only acceptance of one fresh Pair-06 V9 actionable-feedback V2 execution.

This record binds the user's exact explicit authorization text digest/length to
the exact reviewed fresh execution request and to canonical War College main at
authorization time.

It accepts all five reviewed authorization gates:
* execution;
* strict-contact policy activation;
* input-order-coherence activation;
* adapter-rejection repair activation; and
* actionable-feedback V2 activation.

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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_request_source_binding_review_generation2
    as request_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_acceptance_requirements_source_binding_review_generation2
    as requirements_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "fresh-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_MAIN_HEAD = "c86394ad81f7614dc56f1fcc5b0efddbbff49be2"
AUTHORIZED_MAIN_TREE = "9119ed3447084f5e67ec14d9d0089d0255dc74dc"

AUTHORIZATION_TEXT_SHA256 = (
    "b1dca3c6b54f4156ef0a6acb2bad0030e4fbde56501928839f5d2878f5fd0aeb"
)
AUTHORIZATION_TEXT_BYTES = 435

REQUEST_SHA256 = (
    "1a5c5585ac0c25c3da0808e3d50e495b1a7aaf12d4f3cb0d4d000c794aa84268"
)
REQUEST_BYTES = 3113

REQUEST_REVIEW_GIT_BLOB = "5b550b6378e54d8b8b8efe581f34eb7df0a05ceb"
REQUIREMENTS_REVIEW_GIT_BLOB = "541fbacd4ec6d5acbce0cbd2c945f2b45801cfed"

EXECUTION_CONFIRMATION_TOKEN = "EXECUTION=CONFIRM"
POLICY_CONFIRMATION_TOKEN = "STRICT_CONTACT_POLICY=CONFIRM"
ORDER_COHERENCE_CONFIRMATION_TOKEN = "INPUT_ORDER_COHERENCE=CONFIRM"
REPAIR_CONFIRMATION_TOKEN = "ADAPTER_REJECTION_REPAIR=CONFIRM"
ACTIONABLE_FEEDBACK_V2_CONFIRMATION_TOKEN = "ACTIONABLE_FEEDBACK_V2=CONFIRM"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_authorized_execution_launcher"
)


class Pair06V9ActionableFeedbackV2FreshExecutionAuthorizationAcceptanceHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2FreshExecutionAuthorizationAcceptanceHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    request = (
        request_review
        .pair06_v9_actionable_feedback_v2_fresh_execution_request_review_contract()
    )
    requirements = (
        requirements_review
        .pair06_v9_actionable_feedback_v2_fresh_execution_acceptance_requirements_review_contract()
    )

    _require(
        request.get(
            "pair06_v9_actionable_feedback_v2_fresh_execution_request_reviewed"
        )
        is True,
        "actionable-feedback V2 fresh execution request review missing",
    )
    _require(
        requirements.get(
            "pair06_v9_actionable_feedback_v2_fresh_execution_acceptance_requirements_reviewed"
        )
        is True,
        "actionable-feedback V2 fresh execution acceptance requirements review missing",
    )
    _require(
        request.get("request_sha256") == REQUEST_SHA256
        and request.get("request_bytes") == REQUEST_BYTES
        and requirements.get("reviewed_request_sha256") == REQUEST_SHA256
        and requirements.get("reviewed_request_bytes") == REQUEST_BYTES,
        "actionable-feedback V2 fresh execution request identity drift",
    )
    _require(
        request.get("pair_slot") == 6
        and request.get("arm") == "baseline"
        and request.get("held_out") is False
        and request.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and request.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2",
        "actionable-feedback V2 fresh execution request scope drift",
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
        "actionable-feedback V2 fresh execution runtime-safety drift",
    )
    _require(
        request.get("fresh_actionable_feedback_v2_evidence_namespace_required")
        is True
        and request.get("five_explicit_authorizations_required") is True
        and request.get("five_distinct_confirmation_tokens_required") is True,
        "actionable-feedback V2 fresh execution authorization shape drift",
    )

    for field in (
        "exact_user_authorization_text_required",
        "authorization_text_sha256_binding_required",
        "authorization_text_byte_length_binding_required",
        "canonical_main_head_binding_required",
        "canonical_main_tree_binding_required",
        "canonical_main_must_be_bound_at_authorization_time",
        "authorization_must_reference_exact_reviewed_request",
        "authorization_must_explicitly_cover_execution",
        "authorization_must_explicitly_cover_policy_activation",
        "authorization_must_explicitly_cover_order_coherence_activation",
        "authorization_must_explicitly_cover_repair_activation",
        "authorization_must_explicitly_cover_actionable_feedback_v2_activation",
        "five_distinct_confirmation_tokens_required",
    ):
        _require(
            requirements.get(field) is True,
            "actionable-feedback V2 acceptance binding requirement drift: " + field,
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
        "actionable-feedback V2 acceptance authority-reuse drift",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(
            requirements.get(field) is False,
            "actionable-feedback V2 requirements unexpectedly self-authorize: "
            + field,
        )

    return {
        "request_review": deepcopy(request),
        "requirements_review": deepcopy(requirements),
    }


def pair06_v9_actionable_feedback_v2_fresh_execution_authorization_acceptance_contract() -> dict[str, Any]:
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
        "actionable_feedback_v2_activation_authorization_accepted": True,
        "authorized_request_sha256": request["request_sha256"],
        "authorized_request_bytes": request["request_bytes"],
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorized_main_tree": AUTHORIZED_MAIN_TREE,
        "canonical_main_bound_at_authorization_time": True,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "requirements_review_git_blob": REQUIREMENTS_REVIEW_GIT_BLOB,
        "execution_confirmation_token": EXECUTION_CONFIRMATION_TOKEN,
        "policy_confirmation_token": POLICY_CONFIRMATION_TOKEN,
        "order_coherence_confirmation_token": ORDER_COHERENCE_CONFIRMATION_TOKEN,
        "repair_confirmation_token": REPAIR_CONFIRMATION_TOKEN,
        "actionable_feedback_v2_confirmation_token": (
            ACTIONABLE_FEEDBACK_V2_CONFIRMATION_TOKEN
        ),
        "pair_slot": request["pair_slot"],
        "arm": request["arm"],
        "held_out": request["held_out"],
        "policy_id": request["policy_id"],
        "intervention_id": request["intervention_id"],
        "prior_attempt_marker_sha256": request["prior_attempt_marker_sha256"],
        "preservation_receipt_sha256": request["preservation_receipt_sha256"],
        "fresh_actionable_feedback_v2_evidence_namespace_required": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "five_distinct_confirmation_tokens_required": True,
        "attempt_marker_creation_authorized_after_fresh_gpu_admission": True,
        "policy_activation_authorized_after_fresh_gpu_admission": True,
        "order_coherence_activation_authorized_after_fresh_gpu_admission": True,
        "repair_activation_authorized_after_fresh_gpu_admission": True,
        "actionable_feedback_v2_activation_authorized_after_fresh_gpu_admission": True,
        "runtime_load_authorized_after_fresh_gpu_admission": True,
        "model_inference_authorized_after_fresh_gpu_admission": True,
        "game_execution_authorized_after_fresh_gpu_admission": True,
        "gpu_admission_failure_must_not_create_attempt_marker": True,
        "gpu_admission_failure_must_not_activate_policy": True,
        "gpu_admission_failure_must_not_activate_order_coherence": True,
        "gpu_admission_failure_must_not_activate_repair": True,
        "gpu_admission_failure_must_not_activate_actionable_feedback_v2": True,
        "gpu_admission_failure_must_not_load_model": True,
        "gpu_admission_failure_must_not_execute_inference": True,
        "gpu_admission_failure_must_not_execute_game": True,
        "automatic_retry": False,
        "attempt_marker_created_by_this_record": False,
        "gpu_observation_performed_by_this_record": False,
        "policy_activation_performed_by_this_record": False,
        "order_coherence_activation_performed_by_this_record": False,
        "repair_activation_performed_by_this_record": False,
        "actionable_feedback_v2_activation_performed_by_this_record": False,
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
        "actionable_feedback_v2_activation_authorization_reusable_after_attempt_claim": False,
        "reviewed_request": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2FreshExecutionAuthorizationAcceptanceHold(
        NEXT_GATE
    )
