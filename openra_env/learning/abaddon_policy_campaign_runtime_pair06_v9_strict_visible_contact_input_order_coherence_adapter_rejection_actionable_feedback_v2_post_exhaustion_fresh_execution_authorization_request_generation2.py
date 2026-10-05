"""Proposal-only request for one fresh Pair-06 V9 actionable-feedback V2 run after the consumed V2 failure.

The prior actionable-feedback V2 attempt exhausted six strict-contact decision
attempts, was preservation-closed, and is permanently non-reusable. This record
requests a distinct fresh execution authorization while reusing only the
already-reviewed operator source.

Matching request bytes or digest grant no authority. The consumed execution
authorization and preservation authorization are not reusable. Import and
contract inspection perform no host I/O, attempt claim, runtime load, model
inference, game execution, retry, training, deployment, chain, wallet/funds, or
scheduler mutation.
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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_closeout_source_binding_review_generation2
    as preservation_closeout_review,
)


REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "post-exhaustion-fresh-execution-authorization-request.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "post-exhaustion-fresh-execution-authorization-request-validation.v1"
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
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2"
)

FRESH_OPERATOR_GIT_BLOB = "84132f0ba96cff24dc88ea2ef7259a850162e41a"
FRESH_OPERATOR_REVIEW_GIT_BLOB = "c74c221202e8ec35c96a458e2d9849743b1c0b41"
PRIOR_V2_PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB = (
    "ad975a43e7173d78d34d3dbd9b3102b050b5b35f"
)

PRIOR_V2_ATTEMPT_MARKER_SHA256 = (
    "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
)
PRIOR_V2_WARM_START_SHA256 = (
    "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
)
PRIOR_V2_TRAJECTORY_SHA256 = (
    "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
)
PRIOR_V2_PRESERVATION_RECEIPT_SHA256 = (
    "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
)
PRIOR_V2_ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v8-generation2/generation2/"
    "pair-06/failed-attempts/"
    "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
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
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_FRESH_EXECUTION_"
    "AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_"
    "authorization_request_review"
)


class Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestHold(
            message
        )


def _dependencies() -> dict[str, Any]:
    operator = (
        operator_review
        .pair06_v9_actionable_feedback_v2_fresh_lineage_operator_review_contract()
    )
    closeout = (
        preservation_closeout_review
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_actionable_feedback_v2_fresh_lineage_operator_reviewed"
        )
        is True,
        "reviewed actionable-feedback V2 operator missing",
    )
    _require(
        operator.get("operator_git_blob") == FRESH_OPERATOR_GIT_BLOB,
        "actionable-feedback V2 operator source identity drift",
    )
    _require(
        operator.get("pair_slot") == PAIR_SLOT
        and operator.get("arm") == ARM
        and operator.get("held_out") is HELD_OUT
        and operator.get("policy_id") == POLICY_ID,
        "actionable-feedback V2 operator scope drift",
    )
    _require(
        operator.get("maximum_attempts") == 1
        and operator.get("maximum_automatic_retries") == 0
        and operator.get("fresh_preclaim_gpu_observation_required") is True
        and operator.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and operator.get("zero_foreign_cuda0_compute_processes_required") is True,
        "actionable-feedback V2 operator attempt/GPU boundary drift",
    )
    _require(
        operator.get("five_explicit_authorizations_required") is True
        and operator.get("five_distinct_confirmation_tokens_required") is True
        and operator.get("fresh_execution_authorization_required") is True
        and operator.get(
            "fresh_actionable_feedback_v2_activation_authorization_required"
        )
        is True,
        "actionable-feedback V2 operator authorization shape drift",
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
            "actionable-feedback V2 operator authority drift: " + field,
        )

    _require(
        closeout.get(
            "pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_reviewed"
        )
        is True,
        "actionable-feedback V2 preservation closeout review missing",
    )
    _require(
        closeout.get("attempt_marker_sha256") == PRIOR_V2_ATTEMPT_MARKER_SHA256
        and closeout.get("preservation_receipt_sha256")
        == PRIOR_V2_PRESERVATION_RECEIPT_SHA256,
        "actionable-feedback V2 preservation closeout identity drift",
    )
    _require(
        closeout.get("attempt_consumed") is True
        and closeout.get("attempt_reusable") is False
        and closeout.get("attempt_authorization_reusable") is False
        and closeout.get("preservation_authorization_consumed") is True
        and closeout.get("preservation_authorization_reusable") is False
        and closeout.get("preservation_lineage_closed") is True,
        "actionable-feedback V2 preservation closeout reuse boundary drift",
    )
    _require(
        closeout.get("fresh_execution_authorization_required") is True
        and closeout.get("new_execution_request_opened") is False,
        "actionable-feedback V2 preservation closeout execution frontier drift",
    )

    validated_closeout = closeout["validated_closeout"]
    _require(
        validated_closeout.get("warm_start_sha256") == PRIOR_V2_WARM_START_SHA256
        and validated_closeout.get("trajectory_sha256")
        == PRIOR_V2_TRAJECTORY_SHA256
        and validated_closeout.get("archive_path") == PRIOR_V2_ARCHIVE_PATH,
        "actionable-feedback V2 archived evidence identity drift",
    )

    return {
        "fresh_operator_review": deepcopy(operator),
        "prior_v2_preservation_closeout_review": deepcopy(closeout),
    }


def _request_record() -> dict[str, Any]:
    _dependencies()

    record = {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_binding": {
            "fresh_operator_git_blob": FRESH_OPERATOR_GIT_BLOB,
            "fresh_operator_review_git_blob": FRESH_OPERATOR_REVIEW_GIT_BLOB,
            "prior_v2_preservation_closeout_review_git_blob": (
                PRIOR_V2_PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB
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
            "prior_v2_attempt_marker_sha256": PRIOR_V2_ATTEMPT_MARKER_SHA256,
            "prior_v2_warm_start_sha256": PRIOR_V2_WARM_START_SHA256,
            "prior_v2_trajectory_sha256": PRIOR_V2_TRAJECTORY_SHA256,
            "prior_v2_preservation_receipt_sha256": (
                PRIOR_V2_PRESERVATION_RECEIPT_SHA256
            ),
            "prior_v2_archive_path": PRIOR_V2_ARCHIVE_PATH,
            "prior_v2_failure_class": (
                "strict_contact_actionable_feedback_v2_exhausted"
            ),
            "prior_v2_failure_round": 6,
            "prior_v2_attempt_consumed": True,
            "prior_v2_attempt_reusable": False,
            "prior_v2_execution_authorization_reusable": False,
            "prior_v2_preservation_authorization_reusable": False,
            "prior_v2_preservation_lineage_closed": True,
            "reviewed_operator_source_reuse_requested": True,
            "reviewed_operator_authorization_reuse_requested": False,
            "fresh_active_baseline_namespace_required": True,
            "archived_prior_v2_namespace_must_remain_immutable": True,
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
            "prior_execution_authorization_reusable": False,
            "prior_preservation_authorization_reusable_as_execution_authority": False,
        },
    }

    for field in FALSE_AUTHORITY_FIELDS:
        record[field] = False

    return record


def post_exhaustion_fresh_execution_authorization_request() -> dict[str, Any]:
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

    _require(
        len(raw) <= MAX_REQUEST_BYTES,
        "post-exhaustion fresh execution request too large",
    )

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
    raise Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestHold(
        NEXT_GATE
    )
