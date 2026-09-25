"""Source-only review of pair-06 V8 combat-priority parent wiring.

Pins the exact merged child entrypoint, parent wiring, and their tests from
#295. The reviewed no-offload parent remains unchanged. No attempt claim,
runtime activation, game execution, replay, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action is authorized.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-parent-supervisor-wiring-review-contract.v1"
)

MERGED_MAIN_HEAD = "af870046fc4d3f3a791c6cd7fbe801dca3fbd39c"

CHILD_ENTRY_GIT_BLOB = "ccc2591e018875c236207343e3d8e7a04c5873b7"
CHILD_ENTRY_SOURCE_SHA256 = (
    "bf21b64e71e7e7ad62087950366c24035ab15097b6f36b1187f77eafb24c66bf"
)
CHILD_ENTRY_TEST_GIT_BLOB = "26618c99a84944e0223808bdf93ed06c7ef5ffa2"
CHILD_ENTRY_TEST_SHA256 = (
    "4566be9712cb6062c48ea5a09459302cfda78a1b5e52598608d29d4dad949a72"
)

PARENT_WIRING_GIT_BLOB = "c30cf75b26d5e0cecee08286717d8a856e2233bd"
PARENT_WIRING_SOURCE_SHA256 = (
    "9af96b7e3923eeb221fdba2c34e946b0776124549af7ba22a62e83c5306d72b0"
)
PARENT_WIRING_TEST_GIT_BLOB = "98c83f63b8e72d8359913ec0f012545473a69a36"
PARENT_WIRING_TEST_SHA256 = (
    "fbd547e71e2c8783b921783d9b419dc4f7845efa1f6b16c9aa76f8e985ffcd74"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_"
    "RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_baseline_attempt_invocation_"
    "receipt_bound_no_offload_preclaim_gpu"
)


class Pair06V8CombatPriorityParentWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityParentWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    parent = wiring.pair06_v8_combat_priority_parent_supervisor_wiring_contract()
    child = child_entry.pair06_v8_combat_priority_proto_child_entrypoint_contract()

    _require(parent.get("pair_slot") == 6, "pair06 parent slot drift")
    _require(parent.get("arm") == "baseline", "pair06 parent arm drift")
    _require(
        parent.get("combat_priority_child_entrypoint_implemented") is True,
        "combat-priority child entrypoint missing",
    )
    _require(
        parent.get("existing_no_offload_parent_source_modified") is False,
        "reviewed no-offload parent source unexpectedly modified",
    )
    for field in (
        "child_command_builder_substitution_implemented",
        "child_command_builder_substitution_scoped_to_single_call",
        "child_command_builder_restored_in_finally",
        "existing_execution_confirmation_token_preserved",
        "separate_policy_activation_token_added",
        "existing_no_offload_model_loader_reused",
        "existing_cuda0_placement_checks_reused",
        "existing_parent_decision_service_loop_reused",
        "existing_child_retirement_reused",
        "existing_parent_receipt_returned_unchanged",
        "attempt_claim_required",
    ):
        _require(parent.get(field) is True, "parent wiring invariant drift: " + field)

    _require(
        parent.get("existing_parent_automatic_retry") is False,
        "existing parent retry behavior drift",
    )
    for field in (
        "operator_entrypoint_wiring_implemented",
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
        _require(parent.get(field) is False, "parent wiring boundary drift: " + field)

    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "parent wiring review frontier drift",
    )

    _require(
        child.get("pair06_v8_combat_priority_proto_child_entrypoint_implemented")
        is True,
        "combat-priority child entrypoint contract missing",
    )
    _require(
        child.get("existing_execution_confirmation_token_required") is True
        and child.get("separate_policy_activation_token_required") is True
        and child.get("policy_activation_token_distinct_from_execution_token")
        is True,
        "child entrypoint dual-token boundary drift",
    )
    _require(
        child.get("execution_performed_by_contract_inspection") is False
        and child.get("runtime_activation_authorized_by_contract_inspection")
        is False,
        "child entrypoint inspection unexpectedly activates runtime",
    )

    return {
        "parent_wiring": deepcopy(parent),
        "child_entrypoint": deepcopy(child),
    }


def pair06_v8_combat_priority_parent_supervisor_wiring_review_contract() -> dict[str, Any]:
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
        "pair06_v8_combat_priority_parent_supervisor_wiring_reviewed": True,
        "canonical_invocation_lane": (
            "receipt_bound_no_offload_fresh_preclaim_gpu"
        ),
        "maximum_attempts_required": 1,
        "automatic_retry_required": False,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_must_precede_attempt_marker": True,
        "durable_create_only_attempt_marker_required": True,
        "attempt_marker_must_precede_model_load_and_child_spawn": True,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "attempt_marker_creation_authorized": False,
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
    raise Pair06V8CombatPriorityParentWiringReviewHold(NEXT_GATE)
