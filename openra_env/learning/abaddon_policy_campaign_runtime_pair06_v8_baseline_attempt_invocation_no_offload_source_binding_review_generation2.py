"""Source-only review of the no-offload pair-06 V8 baseline one-shot invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_no_offload_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-attempt-invocation-no-offload-review-contract.v1"
)

INVOCATION_GIT_BLOB = "b93255245f4d622dfb2cf0ddd6f97c3592f87cdc"
INVOCATION_SOURCE_SHA256 = (
    "4be25b850afc45cd34b977308add5cd288ce95411c683ca6545e0fb2fd6a0529"
)
INVOCATION_TEST_GIT_BLOB = "e29e25afe7bb24c9fd7bb4eda809bbe5951058af"
INVOCATION_TEST_SHA256 = (
    "f4865ded3550fcf51adc3dd9dc22ae26627879a2ac5bb8e7bdddd3a5bb33de3d"
)

NEXT_GATE = "PAIR06_V8_NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_no_offload_baseline_execution_authorization_request"


class Pair06V8BaselineInvocationNoOffloadReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineInvocationNoOffloadReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = invocation.pair06_v8_baseline_attempt_invocation_no_offload_contract()
    _require(
        out.get("pair06_v8_baseline_attempt_invocation_no_offload_implemented") is True,
        "no-offload pair06 invocation missing",
    )
    _require(
        out.get("pair06_v8_baseline_attempt_invocation_no_offload_reviewed") is False,
        "no-offload pair06 invocation unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "no-offload pair06 invocation slot drift")
    _require(out.get("arm") == "baseline", "no-offload pair06 invocation arm drift")
    _require(out.get("held_out") is False, "no-offload pair06 invocation held-out drift")
    _require(
        out.get("no_offload_parent_generation_required") is True,
        "no-offload parent generation requirement missing",
    )
    _require(
        out.get("second_preservation_result_review_required") is True,
        "second preservation result review requirement missing",
    )
    for field in (
        "preclaim_worktree_materialization_implemented",
        "preclaim_materialization_cleanup_on_hold_implemented",
        "durable_create_only_attempt_marker_implemented",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "marker_sha256_is_attempt_id",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
    ):
        _require(out.get(field) is True, f"no-offload invocation invariant drift: {field}")

    _require(out.get("maximum_attempts") == 1, "no-offload invocation attempt cardinality drift")
    _require(out.get("automatic_retry") is False, "no-offload invocation automatic retry enabled")
    for field in (
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
        _require(out.get(field) is False, f"no-offload invocation authority drift: {field}")

    _require(
        out.get("next_gate")
        == "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
        "no-offload invocation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_baseline_attempt_invocation_no_offload_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_baseline_attempt_invocation_no_offload_source_binding_present": True,
        "pair06_v8_baseline_attempt_invocation_no_offload_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "no_offload_parent_generation_required": True,
        "second_preservation_result_review_required": True,
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
    raise Pair06V8BaselineInvocationNoOffloadReviewHold(NEXT_GATE)
