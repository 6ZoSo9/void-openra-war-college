"""Exact-blob review of the actionable-feedback V3 fresh execution request.

Pins the proposal-only request source and focused tests. The review confirms
closed failed-attempt lineage, a distinct actionable-feedback V3 namespace,
one attempt with zero automatic retries, and five fresh authorization gates.

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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_fresh_execution_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "fresh-lineage-execution-authorization-request-review.v1"
)

ACCEPTED_BASE_HEAD = "dca23323c89fd4a92b96c2a325991d2e0a722d55"

REQUEST_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_fresh_execution_authorization_request_generation2.py"
)
REQUEST_GIT_BLOB = "3469917a211ddeff03b5699f8be7c90df1e4fd20"

REQUEST_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_fresh_execution_authorization_request_generation2.py"
)
REQUEST_TEST_GIT_BLOB = "f6ba060d0d2906032fc7936257565e2c30a3f49a"

FRESH_OPERATOR_GIT_BLOB = "deffe1540a75ad8fb1cc0ae0a10e8559ad737a01"
FRESH_OPERATOR_REVIEW_GIT_BLOB = "d6405cf6fd73b244b7ac7096798dcc651ae6c54b"
PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB = "4dadc961e02cd13893bd842bc6ee727c443b55a2"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_FRESH_EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v3_fresh_execution_authorization_acceptance"
)


class Pair06V9ActionableFeedbackV3FreshExecutionRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3FreshExecutionRequestReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.fresh_execution_authorization_request()
    record = out["request"]

    _require(
        record.get("record_kind") == "proposal_only_not_authorization",
        "actionable-feedback V3 execution request record kind drift",
    )

    source = record["source_binding"]
    _require(
        source.get("fresh_operator_git_blob") == FRESH_OPERATOR_GIT_BLOB
        and source.get("fresh_operator_review_git_blob")
        == FRESH_OPERATOR_REVIEW_GIT_BLOB
        and source.get("preservation_closeout_review_git_blob")
        == PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB
        and source.get("canonical_main_must_be_bound_by_later_authorization")
        is True,
        "actionable-feedback V3 request source lineage drift",
    )

    scope = record["scope"]
    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("doctrine") == "FEINTER"
        and scope.get("seed") == 208354846
        and scope.get("rounds") == 36
        and scope.get("ticks_per_round") == 25
        and scope.get("starter_infantry") == 4
        and scope.get("staging_max_ticks") == 800
        and scope.get("runtime_selection_key") == "apollyon-v3-qwen35-4b-lora-v1"
        and scope.get("policy_id") == "pair06-v9-strict-visible-contact-envelope-v1"
        and scope.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v3",
        "actionable-feedback V3 execution request scope drift",
    )

    lineage = record["lineage"]
    _require(
        lineage.get("prior_attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and lineage.get("preservation_receipt_sha256")
        == "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
        and lineage.get("prior_attempt_consumed") is True
        and lineage.get("prior_attempt_reusable") is False
        and lineage.get("prior_attempt_authorization_reusable") is False
        and lineage.get("preservation_lineage_closed") is True
        and lineage.get("preservation_authorization_reusable") is False
        and lineage.get("fresh_actionable_feedback_v3_evidence_namespace_required")
        is True,
        "actionable-feedback V3 execution request lineage drift",
    )

    safety = record["runtime_safety"]
    _require(
        safety.get("maximum_attempts") == 1
        and safety.get("maximum_automatic_retries") == 0
        and safety.get("fresh_preclaim_gpu_observation_required") is True
        and safety.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and safety.get("zero_foreign_cuda0_compute_processes_required") is True
        and safety.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and safety.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "actionable-feedback V3 execution request runtime safety drift",
    )

    boundary = record["authorization_boundary"]
    for field in (
        "fresh_execution_authorization_requested",
        "fresh_policy_activation_authorization_requested",
        "fresh_order_coherence_activation_authorization_requested",
        "fresh_repair_activation_authorization_requested",
        "fresh_actionable_feedback_v3_activation_authorization_requested",
        "five_distinct_confirmation_tokens_required",
        "fresh_user_authorization_text_required",
    ):
        _require(
            boundary.get(field) is True,
            "actionable-feedback V3 request authorization requirement drift: " + field,
        )

    _require(
        boundary.get("general_source_work_authorization_is_execution_authorization")
        is False
        and boundary.get("matching_request_digest_grants_authority") is False
        and boundary.get("matching_request_bytes_grant_authority") is False
        and boundary.get("prior_authorization_text_reusable") is False
        and boundary.get("preservation_authorization_reusable_as_execution_authority")
        is False,
        "actionable-feedback V3 request authority boundary drift",
    )

    for field in request.FALSE_AUTHORITY_FIELDS:
        _require(
            record.get(field) is False,
            "actionable-feedback V3 request record authority drift: " + field,
        )

    for field in (
        "request_grants_authority",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v3_activation_authorization_accepted",
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
            "validated actionable-feedback V3 request authority/effect drift: " + field,
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


def pair06_v9_actionable_feedback_v3_fresh_execution_request_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    record = deepcopy(validated["request"])

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "request_path": REQUEST_PATH,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_test_path": REQUEST_TEST_PATH,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "fresh_operator_git_blob": FRESH_OPERATOR_GIT_BLOB,
        "fresh_operator_review_git_blob": FRESH_OPERATOR_REVIEW_GIT_BLOB,
        "preservation_closeout_review_git_blob": PRESERVATION_CLOSEOUT_REVIEW_GIT_BLOB,
        "pair06_v9_actionable_feedback_v3_fresh_execution_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "request_bytes": validated["request_bytes"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "policy_id": record["scope"]["policy_id"],
        "intervention_id": record["scope"]["intervention_id"],
        "prior_attempt_marker_sha256": record["lineage"]["prior_attempt_marker_sha256"],
        "preservation_receipt_sha256": record["lineage"]["preservation_receipt_sha256"],
        "fresh_actionable_feedback_v3_evidence_namespace_required": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "five_explicit_authorizations_required": True,
        "five_distinct_confirmation_tokens_required": True,
        "fresh_user_authorization_text_required": True,
        "general_source_work_authorization_is_execution_authorization": False,
        "prior_authorization_text_reusable": False,
        "preservation_authorization_reusable_as_execution_authority": False,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "repair_activation_authorization_accepted": False,
        "actionable_feedback_v3_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
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
    raise Pair06V9ActionableFeedbackV3FreshExecutionRequestReviewHold(NEXT_GATE)
