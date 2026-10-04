"""Proposal-only request for one fresh Pair-06 V9 actionable-feedback V2 run.

This request opens a new proposal frontier only after the failed V1
adapter-rejection attempt has been preserved and closed, and after the reviewed
actionable-feedback V2 fresh-lineage operator exists.

The request binds:
* the exact reviewed actionable-feedback V2 fresh-lineage operator;
* the exact reviewed preservation closeout;
* a distinct actionable-feedback V2 evidence namespace;
* one-attempt / zero-automatic-retry cardinality; and
* five fresh, distinct authorization gates: execution, strict-contact policy
  activation, input-order-coherence activation, adapter-rejection repair
  activation, and actionable-feedback V2 activation.

Matching request bytes or digest grant no authority. General source-work
authorization is explicitly not execution authorization.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_source_binding_review_generation2
    as operator_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_closeout_source_binding_review_generation2
    as preservation_closeout_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-fresh-lineage-"
    "execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-fresh-lineage-"
    "execution-authorization-request-validation.v1"
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
INTERVENTION_ID = "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2"

FRESH_OPERATOR_GIT_BLOB = "84132f0ba96cff24dc88ea2ef7259a850162e41a"
FRESH_OPERATOR_REVIEW_GIT_BLOB = "c74c221202e8ec35c96a458e2d9849743b1c0b41"
PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB = "49624268f93e5ff9257ce7dbf78a14e005a77cfe"

PRIOR_ATTEMPT_MARKER_SHA256 = (
    "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
)
PRESERVATION_RECEIPT_SHA256 = (
    "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
)

MAX_REQUEST_BYTES = 32768

FALSE_AUTHORITY_FIELDS = (
    "execution_authorization_accepted",
    "policy_activation_authorization_accepted",
    "order_coherence_activation_authorization_accepted",
    "repair_activation_authorization_accepted",
    "actionable_feedback_v2_activation_authorization_accepted",
    "attempt_marker_creation_authorized",
    "runtime_load_authorized",
    "model_inference_authorized",
    "game_execution_authorized",
    "attempt_created",
    "runtime_execution_authorized",
    "replay_authorized",
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
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_EXECUTION_AUTHORIZATION_REQUEST_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_request_review"
)


class Pair06V9ActionableFeedbackV2FreshExecutionRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2FreshExecutionRequestHold(message)


def _dependencies() -> dict[str, Any]:
    operator = (
        operator_review
        .pair06_v9_actionable_feedback_v2_fresh_lineage_operator_review_contract()
    )
    closeout = (
        preservation_closeout_review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_actionable_feedback_v2_fresh_lineage_operator_reviewed"
        )
        is True,
        "fresh actionable-feedback V2 operator review missing",
    )
    _require(
        operator.get("operator_git_blob") == FRESH_OPERATOR_GIT_BLOB,
        "fresh actionable-feedback V2 operator source drift",
    )
    _require(
        operator.get("pair_slot") == PAIR_SLOT
        and operator.get("arm") == ARM
        and operator.get("held_out") is HELD_OUT
        and operator.get("policy_id") == POLICY_ID,
        "fresh actionable-feedback V2 operator scope drift",
    )
    _require(
        operator.get("maximum_attempts") == 1
        and operator.get("maximum_automatic_retries") == 0
        and operator.get("fresh_preclaim_gpu_observation_required") is True
        and operator.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and operator.get("zero_foreign_cuda0_compute_processes_required")
        is True,
        "fresh actionable-feedback V2 attempt/GPU boundary drift",
    )
    _require(
        operator.get("fresh_actionable_feedback_v2_evidence_namespace_required")
        is True
        and operator.get("prior_adapter_rejection_attempt_marker_sha256")
        == PRIOR_ATTEMPT_MARKER_SHA256
        and operator.get("prior_adapter_rejection_attempt_reusable") is False
        and operator.get("prior_adapter_rejection_authorization_reusable") is False
        and operator.get("prior_failed_attempt_preservation_reviewed") is True
        and operator.get("prior_failed_attempt_preservation_lineage_closed") is True,
        "fresh actionable-feedback V2 lineage boundary drift",
    )
    _require(
        operator.get("five_explicit_authorizations_required") is True
        and operator.get("five_distinct_confirmation_tokens_required") is True
        and operator.get("fresh_execution_authorization_required") is True
        and operator.get(
            "fresh_actionable_feedback_v2_activation_authorization_required"
        )
        is True,
        "fresh actionable-feedback V2 authorization shape drift",
    )
    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "execution_request_created",
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
            operator.get(field) is False,
            "fresh actionable-feedback V2 operator authority drift: " + field,
        )

    _require(
        closeout.get(
            "pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_reviewed"
        )
        is True,
        "preservation closeout review missing",
    )
    _require(
        closeout.get("preservation_receipt_sha256")
        == PRESERVATION_RECEIPT_SHA256
        and closeout.get("attempt_marker_sha256")
        == PRIOR_ATTEMPT_MARKER_SHA256,
        "preservation closeout identity drift",
    )
    _require(
        closeout.get("attempt_reusable") is False
        and closeout.get("attempt_authorization_reusable") is False
        and closeout.get("preservation_authorization_reusable") is False
        and closeout.get("preservation_lineage_closed") is True,
        "preservation closeout reuse boundary drift",
    )
    _require(
        closeout.get("fresh_execution_authorization_required") is True
        and closeout.get("new_execution_request_opened") is False,
        "preservation closeout execution frontier drift",
    )

    return {
        "fresh_operator_review": deepcopy(operator),
        "preservation_closeout_review": deepcopy(closeout),
    }


def _request_record() -> dict[str, Any]:
    _dependencies()

    record = {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_binding": {
            "fresh_operator_git_blob": FRESH_OPERATOR_GIT_BLOB,
            "fresh_operator_review_git_blob": FRESH_OPERATOR_REVIEW_GIT_BLOB,
            "preservation_closeout_review_git_blob": (
                PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB
            ),
            "canonical_main_must_be_bound_by_later_authorization": True,
        },
        "scope": {
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
            "policy_id": POLICY_ID,
            "intervention_id": INTERVENTION_ID,
        },
        "lineage": {
            "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
            "prior_attempt_consumed": True,
            "prior_attempt_reusable": False,
            "prior_attempt_authorization_reusable": False,
            "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
            "preservation_lineage_closed": True,
            "preservation_authorization_reusable": False,
            "fresh_actionable_feedback_v2_evidence_namespace_required": True,
        },
        "runtime_safety": {
            "maximum_attempts": 1,
            "maximum_automatic_retries": 0,
            "fresh_preclaim_gpu_observation_required": True,
            "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
            "zero_foreign_cuda0_compute_processes_required": True,
            "minimum_cuda0_free_memory_fraction_numerator": 9,
            "minimum_cuda0_free_memory_fraction_denominator": 10,
        },
        "authorization_boundary": {
            "fresh_execution_authorization_requested": True,
            "fresh_policy_activation_authorization_requested": True,
            "fresh_order_coherence_activation_authorization_requested": True,
            "fresh_repair_activation_authorization_requested": True,
            "fresh_actionable_feedback_v2_activation_authorization_requested": True,
            "five_distinct_confirmation_tokens_required": True,
            "fresh_user_authorization_text_required": True,
            "general_source_work_authorization_is_execution_authorization": False,
            "matching_request_digest_grants_authority": False,
            "matching_request_bytes_grant_authority": False,
            "prior_authorization_text_reusable": False,
            "preservation_authorization_reusable_as_execution_authority": False,
        },
    }

    for field in FALSE_AUTHORITY_FIELDS:
        record[field] = False

    return record


def fresh_execution_authorization_request() -> dict[str, Any]:
    request = _request_record()
    raw = (
        json.dumps(
            request,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")

    _require(len(raw) <= MAX_REQUEST_BYTES, "fresh execution request too large")

    return {
        "schema": VALIDATION_SCHEMA,
        "request": deepcopy(request),
        "request_sha256": hashlib.sha256(raw).hexdigest(),
        "request_bytes": len(raw),
        "fresh_execution_authorization_requested": True,
        "fresh_policy_activation_authorization_requested": True,
        "fresh_order_coherence_activation_authorization_requested": True,
        "fresh_repair_activation_authorization_requested": True,
        "fresh_actionable_feedback_v2_activation_authorization_requested": True,
        "request_grants_authority": False,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "repair_activation_authorization_accepted": False,
        "actionable_feedback_v2_activation_authorization_accepted": False,
        "host_io_performed": False,
        "attempt_marker_created": False,
        "runtime_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "scheduler_mutation_performed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2FreshExecutionRequestHold(NEXT_GATE)
