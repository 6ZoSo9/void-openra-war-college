"""Source-only review of the coherent pair-06 combat-priority invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "baseline-attempt-invocation-receipt-bound-no-offload-preclaim-gpu-"
    "review-contract.v1"
)

INVOCATION_MAIN_HEAD = "c16084544dc908707316d84a0fa01a7d48228efa"
INVOCATION_GIT_BLOB = "bdf23aac7e6f51a2c7ca678a1d16c9c351c12ede"
INVOCATION_SOURCE_SHA256 = (
    "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095"
)
INVOCATION_TEST_GIT_BLOB = "056e48c8174c0bc2f3b916209273f7fdd56f3eb2"
INVOCATION_TEST_SHA256 = (
    "6f614411346728a93b7e911a9dd900b05289fd316380c25887f7f3c5772a7839"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
    "EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_repair_"
    "execution_authorization_request"
)


class Pair06V8CombatPriorityCoherentInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_baseline_attempt_invocation_contract()
    )

    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_baseline_attempt_"
            "invocation_implemented"
        )
        is True,
        "coherent invocation missing",
    )
    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_baseline_attempt_"
            "invocation_reviewed"
        )
        is False,
        "coherent invocation unexpectedly self-reviewed",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False,
        "coherent invocation scope drift",
    )
    _require(
        out.get("parent_wiring_review_main_head")
        == "cee72ef93d919022ef2af837627f7c843742cb58"
        and out.get("parent_wiring_review_git_blob")
        == "bb619f70732a5cb476a34b0429ce9041bc3d3598"
        and out.get("parent_wiring_review_source_sha256")
        == "cf85f48f9aac4388de5345043ef51bb0ca210ba76b32150f165744a3b956b591",
        "coherent parent binding drift",
    )

    for field in (
        "fresh_preclaim_gpu_observation_implemented",
        "fresh_preclaim_gpu_admission_required",
        "fresh_preclaim_gpu_observation_precedes_attempt_marker",
        "zero_foreign_cuda0_compute_processes_required",
        "durable_create_only_attempt_marker_implemented",
        "coherent_marker_namespace_distinct_from_spent_combat_priority",
        "coherent_result_namespace_distinct_from_spent_combat_priority",
        "coherent_closeout_namespace_distinct_from_spent_combat_priority",
        "coherent_runs_root_distinct_from_spent_combat_priority",
        "fresh_evidence_namespace_required",
        "fresh_execution_authorization_required",
        "fresh_policy_activation_authorization_required",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "reviewed_combat_priority_coherent_parent_wiring_used",
    ):
        _require(out.get(field) is True, "coherent invocation invariant drift: " + field)

    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10
        and out.get("maximum_attempts") == 1
        and out.get("automatic_retry") is False,
        "coherent invocation bound drift",
    )
    _require(
        out.get("consumed_combat_priority_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_combat_priority_attempt_reusable") is False,
        "consumed attempt lineage drift",
    )
    _require(
        out.get("failed_combat_priority_run_id") == FAILED_RUN_ID
        and out.get("failed_combat_priority_run_reusable_as_authority") is False
        and out.get("prior_authorization_reusable") is False,
        "failed lineage reuse drift",
    )

    for field in (
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
        _require(out.get(field) is False, "coherent invocation authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_"
            "PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "coherent invocation review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_invocation_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_main_head": INVOCATION_MAIN_HEAD,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_invocation_reviewed": True,
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
        "fresh_evidence_namespace_required": True,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
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


def request_authorization_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentInvocationReviewHold(NEXT_GATE)
