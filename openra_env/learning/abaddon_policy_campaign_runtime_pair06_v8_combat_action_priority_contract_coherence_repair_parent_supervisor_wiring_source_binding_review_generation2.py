"""Source-only review of coherent pair-06 combat-priority parent wiring.

Pins the exact merged coherent child entrypoint, parent wiring, and their tests
from #306. The historical combat-priority parent and no-offload parent remain
unchanged.

The failed attempt marker is permanently consumed. This review advances only to
a fresh repaired one-shot invocation source with a distinct evidence namespace.
It grants no retry, attempt claim, runtime activation, execution, replay,
training, deployment, chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_parent_supervisor_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "parent-supervisor-wiring-review-contract.v1"
)

MERGED_MAIN_HEAD = "fc29628d67bc51e17022a7b8a4e5e1cc4dc71ff4"

CHILD_ENTRY_GIT_BLOB = "8a0161b4b6b80c74adc6d68e1fadf2e6c044c601"
CHILD_ENTRY_SOURCE_SHA256 = (
    "9b3fde2af21e01dc2cc13d01a2729c0565f663fbe6b39280c804186f8d1f2102"
)
CHILD_ENTRY_TEST_GIT_BLOB = "339567f12c3b7f95d7280d333d97404b543c7872"
CHILD_ENTRY_TEST_SHA256 = (
    "13b56618c77b7b162b1f61d77296607ad91f4f9b28b91e0d0a4c1445ae8701bb"
)

PARENT_WIRING_GIT_BLOB = "fa3dcc13b9150a88e12c8fee005f7bf16670a236"
PARENT_WIRING_SOURCE_SHA256 = (
    "114b4ce77abddb3ba9c856c78f1331ba22d807d4ecdf6a0fe0dc944773ff32c0"
)
PARENT_WIRING_TEST_GIT_BLOB = "24de93c5543319f063f51aae81a4f6e4ddd946af"
PARENT_WIRING_TEST_SHA256 = (
    "3da302f685e0cd427e6375cf72e25cf3007d93e7d36080363346f2ebe40f718a"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_repair_"
    "baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu"
)


class Pair06V8CombatPriorityCoherentParentWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentParentWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    parent = wiring.pair06_v8_combat_priority_coherent_parent_wiring_contract()
    child = child_entry.pair06_v8_combat_priority_coherent_child_entrypoint_contract()

    _require(parent.get("pair_slot") == 6, "coherent parent slot drift")
    _require(parent.get("arm") == "baseline", "coherent parent arm drift")
    _require(
        parent.get("coherent_child_entrypoint_implemented") is True,
        "coherent child entrypoint missing",
    )
    _require(
        parent.get("historical_parent_wiring_source_modified") is False
        and parent.get("historical_no_offload_parent_source_modified") is False,
        "historical parent source unexpectedly modified",
    )

    for field in (
        "historical_child_command_builder_reused",
        "coherent_child_command_substitution_implemented",
        "coherent_child_command_substitution_scoped_to_single_call",
        "historical_child_command_restored_in_finally",
        "existing_execution_confirmation_token_preserved",
        "existing_policy_activation_confirmation_token_preserved",
        "existing_no_offload_model_loader_reused",
        "existing_cuda0_placement_checks_reused",
        "existing_parent_decision_service_loop_reused",
        "existing_child_retirement_reused",
        "existing_parent_receipt_returned_unchanged",
        "production_functions_filtered_to_offered_surface",
    ):
        _require(parent.get(field) is True, "coherent parent invariant drift: " + field)

    _require(
        parent.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and parent.get("consumed_attempt_reusable") is False,
        "consumed attempt lineage drift",
    )

    for field in (
        "attempt_retry_authorized",
        "operator_invocation_repair_implemented",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(parent.get(field) is False, "coherent parent authority drift: " + field)

    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "coherent parent review frontier drift",
    )

    _require(
        child.get(
            "pair06_v8_combat_priority_coherent_child_entrypoint_implemented"
        )
        is True,
        "coherent child entrypoint contract missing",
    )
    _require(
        child.get("production_functions_filtered_to_offered_surface") is True,
        "coherent child repair missing",
    )
    _require(
        child.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and child.get("consumed_attempt_reusable") is False
        and child.get("attempt_retry_authorized") is False,
        "coherent child consumed-attempt boundary drift",
    )
    _require(
        child.get("execution_performed_by_contract_inspection") is False
        and child.get("runtime_activation_authorized_by_contract_inspection")
        is False,
        "coherent child inspection unexpectedly executes",
    )

    return {
        "parent_wiring": deepcopy(parent),
        "child_entrypoint": deepcopy(child),
    }


def pair06_v8_combat_priority_coherent_parent_wiring_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "merged_main_head": MERGED_MAIN_HEAD,
        "child_entry_git_blob": CHILD_ENTRY_GIT_BLOB,
        "child_entry_source_sha256": CHILD_ENTRY_SOURCE_SHA256,
        "child_entry_test_git_blob": CHILD_ENTRY_TEST_GIT_BLOB,
        "child_entry_test_sha256": CHILD_ENTRY_TEST_SHA256,
        "parent_wiring_git_blob": PARENT_WIRING_GIT_BLOB,
        "parent_wiring_source_sha256": PARENT_WIRING_SOURCE_SHA256,
        "parent_wiring_test_git_blob": PARENT_WIRING_TEST_GIT_BLOB,
        "parent_wiring_test_sha256": PARENT_WIRING_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_parent_wiring_reviewed": True,
        "canonical_invocation_lane": (
            "receipt_bound_no_offload_fresh_preclaim_gpu"
        ),
        "production_functions_filtered_to_offered_surface": True,
        "maximum_attempts_per_fresh_authorization": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_must_precede_attempt_marker": True,
        "durable_create_only_attempt_marker_required": True,
        "attempt_marker_must_precede_model_load_and_child_spawn": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "fresh_evidence_namespace_required": True,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "attempt_retry_authorized": False,
        "attempt_marker_creation_authorized": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def implement_invocation_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentParentWiringReviewHold(NEXT_GATE)
