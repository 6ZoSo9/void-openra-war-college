"""Source-only acceptance requirements for actionable-feedback V2 execution.

This module consumes the reviewed proposal-only actionable-feedback V2 request
and publishes the exact bindings a later explicit user authorization acceptance
must capture.

A later acceptance must bind:
* exact reviewed request digest and byte length;
* exact user authorization text digest and byte length;
* canonical main head and tree at authorization time;
* explicit coverage of all five fresh authorization gates:
  execution, strict-contact policy activation, input-order coherence
  activation, adapter-rejection repair activation, and actionable-feedback V2
  activation.

This module accepts no authorization and performs no host or runtime action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "fresh-execution-authorization-acceptance-requirements-contract.v1"
)

REQUEST_REVIEW_GIT_BLOB = "5b550b6378e54d8b8b8efe581f34eb7df0a05ceb"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_EXECUTION_"
    "EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_acceptance"
)


class Pair06V9ActionableFeedbackV2FreshExecutionAcceptanceRequirementsHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2FreshExecutionAcceptanceRequirementsHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v9_actionable_feedback_v2_fresh_execution_request_review_contract()
    )

    _require(
        out.get("pair06_v9_actionable_feedback_v2_fresh_execution_request_reviewed")
        is True,
        "actionable-feedback V2 fresh execution request review missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("policy_id") == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2",
        "actionable-feedback V2 fresh execution request scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker") is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "actionable-feedback V2 fresh execution request runtime-safety drift",
    )
    _require(
        out.get("fresh_actionable_feedback_v2_evidence_namespace_required") is True
        and out.get("five_explicit_authorizations_required") is True
        and out.get("five_distinct_confirmation_tokens_required") is True
        and out.get("fresh_user_authorization_text_required") is True,
        "actionable-feedback V2 fresh execution request authorization-shape drift",
    )
    _require(
        out.get("general_source_work_authorization_is_execution_authorization")
        is False
        and out.get("prior_authorization_text_reusable") is False
        and out.get("preservation_authorization_reusable_as_execution_authority")
        is False,
        "actionable-feedback V2 fresh execution request authority-reuse drift",
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
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "actionable-feedback V2 fresh execution request unexpectedly grants authority: "
            + field,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_fresh_execution_acceptance_requirements_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()

    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "acceptance_requirements_implemented": True,
        "reviewed_request_sha256": reviewed["request_sha256"],
        "reviewed_request_bytes": reviewed["request_bytes"],
        "pair_slot": reviewed["pair_slot"],
        "arm": reviewed["arm"],
        "held_out": reviewed["held_out"],
        "policy_id": reviewed["policy_id"],
        "intervention_id": reviewed["intervention_id"],
        "prior_attempt_marker_sha256": reviewed["prior_attempt_marker_sha256"],
        "preservation_receipt_sha256": reviewed["preservation_receipt_sha256"],
        "fresh_actionable_feedback_v2_evidence_namespace_required": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "exact_user_authorization_text_required": True,
        "authorization_text_sha256_binding_required": True,
        "authorization_text_byte_length_binding_required": True,
        "canonical_main_head_binding_required": True,
        "canonical_main_tree_binding_required": True,
        "canonical_main_must_be_bound_at_authorization_time": True,
        "authorization_must_reference_exact_reviewed_request": True,
        "authorization_must_explicitly_cover_execution": True,
        "authorization_must_explicitly_cover_policy_activation": True,
        "authorization_must_explicitly_cover_order_coherence_activation": True,
        "authorization_must_explicitly_cover_repair_activation": True,
        "authorization_must_explicitly_cover_actionable_feedback_v2_activation": True,
        "five_distinct_confirmation_tokens_required": True,
        "general_source_work_authorization_is_execution_authorization": False,
        "prior_authorization_text_reusable": False,
        "preservation_authorization_reusable_as_execution_authority": False,
        "matching_request_digest_grants_authority": False,
        "matching_request_bytes_grant_authority": False,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "repair_activation_authorization_accepted": False,
        "actionable_feedback_v2_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "attempt_created": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "reviewed_request": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2FreshExecutionAcceptanceRequirementsHold(
        NEXT_GATE
    )
