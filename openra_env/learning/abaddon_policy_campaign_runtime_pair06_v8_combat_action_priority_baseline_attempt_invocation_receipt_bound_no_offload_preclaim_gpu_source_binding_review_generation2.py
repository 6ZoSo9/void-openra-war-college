"""Source-only review of the pair-06 V8 combat-priority one-shot invocation.

Pins the exact merged invocation source/tests from #297 and validates the
receipt-bound, no-offload, fresh-preclaim-GPU, one-attempt, zero-retry envelope.

This review grants no attempt-marker creation, policy activation, runtime/model
load, inference, game execution, replay, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-baseline-attempt-invocation-"
    "receipt-bound-no-offload-preclaim-gpu-review-contract.v1"
)

INVOCATION_MAIN_HEAD = "589c83fbb2b9ef59c99a23e2830a252f78751186"
INVOCATION_GIT_BLOB = "b8a4c21703dad31e0b6b9768e7e4ba6ae1084abb"
INVOCATION_SOURCE_SHA256 = (
    "db383a1a833599d2b444dc4a07d6d1c08ef75e6e5c5dc6fd50cbe173ce5e39dd"
)
INVOCATION_TEST_GIT_BLOB = (
    "568548907f9b434d5d4ca45a2b01e3af9ea17a23"
)
INVOCATION_TEST_SHA256 = (
    "b2be3d7a8da30708e70ae1b5611e04ed1a6ed8e4ffb900549c6ebee55decc9e5"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
    "BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_no_offload_"
    "receipt_bound_preclaim_gpu_baseline_execution_authorization_request"
)


class Pair06V8CombatPriorityInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = invocation.pair06_v8_combat_priority_baseline_attempt_invocation_contract()

    _require(
        out.get("pair06_v8_combat_priority_baseline_attempt_invocation_implemented")
        is True,
        "pair06 combat-priority invocation missing",
    )
    _require(
        out.get("pair06_v8_combat_priority_baseline_attempt_invocation_reviewed")
        is False,
        "pair06 combat-priority invocation unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "pair06 invocation slot drift")
    _require(out.get("arm") == "baseline", "pair06 invocation arm drift")
    _require(out.get("held_out") is False, "pair06 invocation held-out drift")

    for field in (
        "exact_v8_python_required",
        "exact_current_main_required",
        "exact_invocation_source_sha256_required",
        "fresh_v8_environment_and_assets_required",
        "reviewed_base_preclaim_gpu_helpers_reused",
        "reviewed_worktree_materializer_reused",
        "preclaim_worktree_materialization_implemented",
        "preclaim_materialization_cleanup_on_hold_implemented",
        "fresh_preclaim_gpu_observation_implemented",
        "fresh_preclaim_gpu_admission_required",
        "fresh_preclaim_gpu_observation_precedes_attempt_marker",
        "zero_foreign_cuda0_compute_processes_required",
        "durable_create_only_attempt_marker_implemented",
        "combat_priority_marker_namespace_distinct_from_legacy",
        "combat_priority_result_namespace_distinct_from_legacy",
        "combat_priority_closeout_namespace_distinct_from_legacy",
        "combat_priority_runs_root_distinct_from_legacy",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "marker_sha256_is_attempt_id",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "reviewed_combat_priority_parent_wiring_used",
        "no_offload_parent_receipt_schema_required",
        "inference_safe_placement_receipt_required",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
        "explicit_execution_authorization_boolean_required",
        "explicit_policy_activation_authorization_boolean_required",
        "explicit_execution_confirmation_token_required",
        "explicit_policy_confirmation_token_required",
        "execution_and_policy_confirmation_tokens_distinct",
    ):
        _require(out.get(field) is True, "pair06 invocation invariant drift: " + field)

    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "pair06 GPU free-memory threshold drift",
    )
    _require(out.get("maximum_attempts") == 1, "pair06 attempt cardinality drift")
    _require(out.get("automatic_retry") is False, "pair06 automatic retry enabled")

    for field in (
        "marker_deletion_api_implemented",
        "reset_api_implemented",
        "resume_api_implemented",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
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
        _require(out.get(field) is False, "pair06 invocation authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_"
            "RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "pair06 invocation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_baseline_attempt_invocation_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_main_head": INVOCATION_MAIN_HEAD,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_combat_priority_baseline_attempt_invocation_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "combat_priority_evidence_namespace_distinct_from_spent_baseline": True,
        "explicit_execution_authorization_required": True,
        "explicit_policy_activation_authorization_required": True,
        "distinct_execution_and_policy_confirmations_required": True,
        "attempt_marker_creation_authorized": False,
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


def request_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityInvocationReviewHold(NEXT_GATE)
