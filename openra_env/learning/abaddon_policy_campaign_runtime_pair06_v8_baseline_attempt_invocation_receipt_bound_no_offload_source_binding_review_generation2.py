"""Source-only review of receipt-bound no-offload pair-06 invocation generation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-attempt-invocation-receipt-bound-no-offload-review-contract.v1"
)

INVOCATION_GIT_BLOB = "f22313cc3481b806a30dee5a7009b62c25293f17"
INVOCATION_SOURCE_SHA256 = (
    "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
)
INVOCATION_TEST_GIT_BLOB = "1f106f83502e6d802fd6cbffacf175985ee59ab6"
INVOCATION_TEST_SHA256 = (
    "d62591daee8896648686ee865587a945ba1c63471b464a3f45b6b5ec5bbe21af"
)

NEXT_GATE = (
    "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_no_offload_receipt_bound_execution_authorization_request"
)


class Pair06V8ReceiptBoundInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ReceiptBoundInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()
    _require(
        out.get("pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_implemented")
        is True,
        "receipt-bound pair06 invocation missing",
    )
    _require(
        out.get("pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed")
        is False,
        "receipt-bound pair06 invocation unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "receipt-bound invocation slot drift")
    _require(out.get("arm") == "baseline", "receipt-bound invocation arm drift")
    _require(out.get("held_out") is False, "receipt-bound invocation held-out drift")

    for field in (
        "no_offload_parent_generation_required",
        "second_preservation_result_review_required",
        "preclaim_worktree_materialization_implemented",
        "preclaim_materialization_cleanup_on_hold_implemented",
        "durable_create_only_attempt_marker_implemented",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "marker_sha256_is_attempt_id",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "no_offload_parent_receipt_schema_required",
        "inference_safe_placement_receipt_required",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
    ):
        _require(out.get(field) is True, f"receipt-bound invocation invariant drift: {field}")

    _require(out.get("maximum_attempts") == 1, "receipt-bound attempt cardinality drift")
    for field in (
        "automatic_retry",
        "pair06_baseline_specific_authorization_accepted",
        "attempt_consumed",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        _require(out.get(field) is False, f"receipt-bound invocation authority drift: {field}")

    _require(
        out.get("next_gate")
        == "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
        "receipt-bound invocation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "no_offload_parent_generation_required": True,
        "second_preservation_result_review_required": True,
        "no_offload_parent_receipt_schema_required": True,
        "inference_safe_placement_receipt_required": True,
        "explicit_authorization_required": True,
        "pair06_baseline_specific_authorization_accepted": False,
        "attempt_marker_create_only": True,
        "attempt_marker_precedes_model_load_and_child_spawn": True,
        "postclaim_reset_or_resume_available": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_invocation": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_authorize(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ReceiptBoundInvocationReviewHold(NEXT_GATE)
