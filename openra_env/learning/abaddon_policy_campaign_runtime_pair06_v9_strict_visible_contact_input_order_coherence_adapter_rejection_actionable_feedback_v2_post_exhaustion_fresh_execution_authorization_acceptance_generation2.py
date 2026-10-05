"""Audit-only acceptance of one fresh post-exhaustion Pair-06 V9 actionable-feedback V2 execution.

This record binds the user's exact explicit authorization text digest/length to
the exact reviewed post-exhaustion execution request and canonical War College
main at authorization time.

It accepts all five reviewed gates for exactly one attempt:
* execution;
* strict-contact policy activation;
* input-order-coherence activation;
* adapter-rejection repair activation; and
* actionable-feedback V2 activation.

The record itself performs no host I/O, GPU observation, attempt claim, runtime
load, inference, game execution, training, deployment, chain, wallet/funds, or
scheduler mutation. Zero automatic retries remains mandatory.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_request_source_binding_review_generation2
    as request_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_acceptance_requirements_source_binding_review_generation2
    as requirements_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "post-exhaustion-fresh-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_MAIN_HEAD = "8aa35cc75c4474061ad591622879a0fd857009ff"
AUTHORIZED_MAIN_TREE = "517dea886ea30467a3c6a4be47e4f2e015743f37"

AUTHORIZATION_TEXT_SHA256 = (
    "ad844941da6c371a04c47bda2f77ad5bcbd46f667b5cb542916efe4d659cd765"
)
AUTHORIZATION_TEXT_BYTES = 760

REQUEST_SHA256 = (
    "ae676de935142a83bbf8374621d5d41dcc81e9aa6910bf12507bcf6589ae8953"
)
REQUEST_BYTES = 3814

REQUEST_REVIEW_GIT_BLOB = "c3ae2c1117ad87851769b3999ae35a475c68b3e8"
REQUIREMENTS_REVIEW_GIT_BLOB = "def228081606c604e785ef057a3ac33fde026a5c"

EXECUTION_CONFIRMATION_TOKEN = "EXECUTION=CONFIRM"
POLICY_CONFIRMATION_TOKEN = "STRICT_CONTACT_POLICY=CONFIRM"
ORDER_COHERENCE_CONFIRMATION_TOKEN = "INPUT_ORDER_COHERENCE=CONFIRM"
REPAIR_CONFIRMATION_TOKEN = "ADAPTER_REJECTION_REPAIR=CONFIRM"
ACTIONABLE_FEEDBACK_V2_CONFIRMATION_TOKEN = "ACTIONABLE_FEEDBACK_V2=CONFIRM"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_"
    "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_post_exhaustion_"
    "authorized_execution_launcher"
)


class Pair06V9ActionableFeedbackV2PostExhaustionAuthorizationAcceptanceHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PostExhaustionAuthorizationAcceptanceHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    request = (
        request_review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
    )
    requirements = (
        requirements_review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_review_contract()
    )

    _require(
        request.get(
            "pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_reviewed"
        )
        is True,
        "post-exhaustion fresh execution request review missing",
    )
    _require(
        requirements.get(
            "pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_reviewed"
        )
        is True,
        "post-exhaustion acceptance requirements review missing",
    )
    _require(
        request.get("request_sha256") == REQUEST_SHA256
        and request.get("request_bytes") == REQUEST_BYTES
        and requirements.get("reviewed_request_sha256") == REQUEST_SHA256
        and requirements.get("reviewed_request_bytes") == REQUEST_BYTES,
        "post-exhaustion fresh execution request identity drift",
    )

    record = request["validated_request"]["request"]
    scope = record["scope"]
    lineage = record["lineage"]
    safety = record["runtime_safety"]

    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("policy_id") == "pair06-v9-strict-visible-contact-envelope-v1"
        and scope.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2",
        "post-exhaustion fresh execution scope drift",
    )
    _require(
        lineage.get("prior_v2_attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and lineage.get("prior_v2_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
        and lineage.get("prior_v2_attempt_reusable") is False
        and lineage.get("prior_v2_execution_authorization_reusable") is False
        and lineage.get("prior_v2_preservation_authorization_reusable") is False
        and lineage.get("reviewed_operator_source_reuse_requested") is True
        and lineage.get("reviewed_operator_authorization_reuse_requested") is False,
        "post-exhaustion lineage boundary drift",
    )
    _require(
        safety.get("maximum_attempts") == 1
        and safety.get("maximum_automatic_retries") == 0
        and safety.get("fresh_preclaim_gpu_observation_required") is True
        and safety.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and safety.get("zero_foreign_cuda0_compute_processes_required") is True
        and safety.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and safety.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "post-exhaustion runtime safety drift",
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
            "post-exhaustion acceptance binding requirement drift: " + field,
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
            "post-exhaustion requirements unexpectedly self-authorize: " + field,
        )

    return {
        "request_review": deepcopy(request),
        "requirements_review": deepcopy(requirements),
        "record": deepcopy(record),
    }


def pair06_v9_actionable_feedback_v2_post_exhaustion_authorization_acceptance_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    record = reviewed["record"]
    scope = record["scope"]
    lineage = record["lineage"]

    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "actionable_feedback_v2_activation_authorization_accepted": True,
        "authorized_request_sha256": REQUEST_SHA256,
        "authorized_request_bytes": REQUEST_BYTES,
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
        "pair_slot": scope["pair_slot"],
        "arm": scope["arm"],
        "held_out": scope["held_out"],
        "policy_id": scope["policy_id"],
        "intervention_id": scope["intervention_id"],
        "prior_v2_attempt_marker_sha256": lineage[
            "prior_v2_attempt_marker_sha256"
        ],
        "prior_v2_preservation_receipt_sha256": lineage[
            "prior_v2_preservation_receipt_sha256"
        ],
        "reviewed_operator_source_reuse_only": True,
        "prior_execution_authorization_reusable": False,
        "prior_preservation_authorization_reusable": False,
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
    raise Pair06V9ActionableFeedbackV2PostExhaustionAuthorizationAcceptanceHold(
        NEXT_GATE
    )
