"""Exact-blob review of the post-exhaustion actionable-feedback V2 fresh execution request.

Pins the proposal-only request source and focused tests. The review confirms the
latest V2 failed attempt is preservation-closed and non-reusable, the reviewed
operator source may be reused, and all execution/activation authority must be
fresh.

No execution authority is accepted here. A later acceptance must bind fresh
explicit user authorization text and canonical main at authorization time.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "post-exhaustion-fresh-execution-authorization-request-review.v1"
)

ACCEPTED_BASE_HEAD = "eed5ee6e66f3d497a25ce3833252773d19ed6bbd"

REQUEST_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_post_exhaustion_fresh_execution_"
    "authorization_request_generation2.py"
)
REQUEST_GIT_BLOB = "93d03636812746a50649f02bab7770fa0676fac5"

REQUEST_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_post_exhaustion_fresh_execution_"
    "authorization_request_generation2.py"
)
REQUEST_TEST_GIT_BLOB = "e6266ad9ff6fb1dc3fddb5d7c1f4d9d53f989a77"

FRESH_OPERATOR_GIT_BLOB = "84132f0ba96cff24dc88ea2ef7259a850162e41a"
FRESH_OPERATOR_REVIEW_GIT_BLOB = "c74c221202e8ec35c96a458e2d9849743b1c0b41"
PRIOR_V2_PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB = (
    "ad975a43e7173d78d34d3dbd9b3102b050b5b35f"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_FRESH_EXECUTION_"
    "AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_"
    "authorization_acceptance"
)


class Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.post_exhaustion_fresh_execution_authorization_request()
    record = out["request"]
    source = record["source_binding"]
    lineage = record["lineage"]
    safety = record["runtime_safety"]
    boundary = record["authorization_boundary"]

    _require(
        record.get("record_kind") == "proposal_only_not_authorization",
        "post-exhaustion execution request record kind drift",
    )
    _require(
        source.get("fresh_operator_git_blob") == FRESH_OPERATOR_GIT_BLOB
        and source.get("fresh_operator_review_git_blob")
        == FRESH_OPERATOR_REVIEW_GIT_BLOB
        and source.get("prior_v2_preservation_closeout_review_git_blob")
        == PRIOR_V2_PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB
        and source.get("canonical_main_must_be_bound_by_later_authorization")
        is True,
        "post-exhaustion request source binding drift",
    )
    _require(
        lineage.get("prior_v2_attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and lineage.get("prior_v2_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
        and lineage.get("prior_v2_failure_class")
        == "strict_contact_actionable_feedback_v2_exhausted"
        and lineage.get("prior_v2_failure_round") == 6,
        "post-exhaustion request prior V2 identity drift",
    )
    _require(
        lineage.get("prior_v2_attempt_consumed") is True
        and lineage.get("prior_v2_attempt_reusable") is False
        and lineage.get("prior_v2_execution_authorization_reusable") is False
        and lineage.get("prior_v2_preservation_authorization_reusable") is False
        and lineage.get("prior_v2_preservation_lineage_closed") is True
        and lineage.get("reviewed_operator_source_reuse_requested") is True
        and lineage.get("reviewed_operator_authorization_reuse_requested") is False
        and lineage.get("fresh_active_baseline_namespace_required") is True
        and lineage.get("archived_prior_v2_namespace_must_remain_immutable")
        is True,
        "post-exhaustion request lineage boundary drift",
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
        "post-exhaustion request fresh authorization shape drift",
    )
    _require(
        boundary.get(
            "general_source_work_authorization_is_execution_authorization"
        )
        is False
        and boundary.get("matching_request_digest_grants_authority") is False
        and boundary.get("matching_request_bytes_grant_authority") is False
        and boundary.get("prior_execution_authorization_reusable") is False
        and boundary.get(
            "prior_preservation_authorization_reusable_as_execution_authority"
        )
        is False,
        "post-exhaustion request authorization reuse boundary drift",
    )

    for field in request.FALSE_AUTHORITY_FIELDS:
        _require(
            record.get(field) is False,
            "post-exhaustion request authority drift: " + field,
        )

    for field in (
        "request_grants_authority",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "host_io_performed",
        "attempt_marker_created",
        "runtime_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "scheduler_mutation_performed",
    ):
        _require(
            out.get(field) is False,
            "post-exhaustion request effect drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (REQUEST_PATH, REQUEST_GIT_BLOB),
        (REQUEST_TEST_PATH, REQUEST_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    record = deepcopy(validated["request"])
    lineage = record["lineage"]

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "request_path": REQUEST_PATH,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_test_path": REQUEST_TEST_PATH,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_post_exhaustion_fresh_execution_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "request_bytes": validated["request_bytes"],
        "prior_v2_attempt_marker_sha256": (
            lineage["prior_v2_attempt_marker_sha256"]
        ),
        "prior_v2_preservation_receipt_sha256": (
            lineage["prior_v2_preservation_receipt_sha256"]
        ),
        "prior_v2_attempt_consumed": True,
        "prior_v2_attempt_reusable": False,
        "prior_v2_execution_authorization_reusable": False,
        "prior_v2_preservation_authorization_reusable": False,
        "prior_v2_preservation_lineage_closed": True,
        "reviewed_operator_source_reuse_requested": True,
        "reviewed_operator_authorization_reuse_requested": False,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "five_fresh_authorization_gates_required": True,
        "fresh_user_authorization_text_required": True,
        "canonical_main_binding_required_at_authorization_time": True,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "repair_activation_authorization_accepted": False,
        "actionable_feedback_v2_activation_authorization_accepted": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestReviewHold(
        NEXT_GATE
    )
