"""Source-only acceptance requirements for the post-exhaustion actionable-feedback V2 execution request.

Consumes the reviewed proposal-only request and defines the exact bindings a
later explicit user authorization acceptance must capture. No execution or
activation authority is accepted here and no host/runtime action is performed.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_request_source_binding_review_generation2
    as request_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "post-exhaustion-fresh-execution-authorization-acceptance-requirements.v1"
)

REQUEST_REVIEW_GIT_BLOB = "c3ae2c1117ad87851769b3999ae35a475c68b3e8"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_FRESH_EXECUTION_"
    "EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_"
    "authorization_acceptance"
)


class Pair06V9ActionableFeedbackV2PostExhaustionAcceptanceRequirementsHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PostExhaustionAcceptanceRequirementsHold(
            message
        )


@lru_cache(maxsize=1)
def _reviewed_request() -> dict[str, Any]:
    out = (
        request_review
        .pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract()
    )
    _require(
        out.get(
            "pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_reviewed"
        )
        is True,
        "post-exhaustion fresh execution request review missing",
    )

    validated = out["validated_request"]
    record = validated["request"]
    scope = record["scope"]
    lineage = record["lineage"]
    safety = record["runtime_safety"]
    boundary = record["authorization_boundary"]

    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("policy_id") == "pair06-v9-strict-visible-contact-envelope-v1"
        and scope.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2",
        "post-exhaustion request scope drift",
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
        "post-exhaustion request lineage drift",
    )
    _require(
        safety.get("maximum_attempts") == 1
        and safety.get("maximum_automatic_retries") == 0
        and safety.get("fresh_preclaim_gpu_observation_required") is True
        and safety.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and safety.get("zero_foreign_cuda0_compute_processes_required") is True,
        "post-exhaustion request runtime safety drift",
    )
    _require(
        boundary.get("fresh_execution_authorization_requested") is True
        and boundary.get("fresh_policy_activation_authorization_requested") is True
        and boundary.get("fresh_order_coherence_activation_authorization_requested")
        is True
        and boundary.get("fresh_repair_activation_authorization_requested") is True
        and boundary.get(
            "fresh_actionable_feedback_v2_activation_authorization_requested"
        )
        is True
        and boundary.get("five_distinct_confirmation_tokens_required") is True
        and boundary.get("fresh_user_authorization_text_required") is True,
        "post-exhaustion request authorization shape drift",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "runtime_retry_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "post-exhaustion request unexpectedly grants authority: " + field,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_post_exhaustion_acceptance_requirements_contract() -> dict[str, Any]:
    reviewed = _reviewed_request()
    record = reviewed["validated_request"]["request"]
    scope = record["scope"]
    lineage = record["lineage"]

    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "acceptance_requirements_implemented": True,
        "reviewed_request_sha256": reviewed["request_sha256"],
        "reviewed_request_bytes": reviewed["request_bytes"],
        "pair_slot": scope["pair_slot"],
        "arm": scope["arm"],
        "held_out": scope["held_out"],
        "policy_id": scope["policy_id"],
        "intervention_id": scope["intervention_id"],
        "prior_v2_attempt_marker_sha256": lineage["prior_v2_attempt_marker_sha256"],
        "prior_v2_preservation_receipt_sha256": (
            lineage["prior_v2_preservation_receipt_sha256"]
        ),
        "reviewed_operator_source_reuse_only": True,
        "prior_execution_authorization_reusable": False,
        "prior_preservation_authorization_reusable": False,
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
    raise Pair06V9ActionableFeedbackV2PostExhaustionAcceptanceRequirementsHold(
        NEXT_GATE
    )
