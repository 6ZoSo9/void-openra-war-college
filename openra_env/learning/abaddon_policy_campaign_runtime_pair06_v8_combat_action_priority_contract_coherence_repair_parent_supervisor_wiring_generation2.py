"""Source-only no-offload parent wiring for the coherent pair-06 child.

The historical combat-priority parent wrapper remains byte-for-byte unchanged.
This module temporarily replaces only that wrapper's child-command builder so
its delegated no-offload parent launches the reviewed coherent child entrypoint.

All historical no-offload model loading, CUDA:0 placement checks, parent IPC
decision service, child retirement, authority checks, and receipt construction
remain unchanged.

The consumed failed attempt is non-reusable. No retry or execution authority is
granted by contract inspection.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_source_binding_review_generation2
    as coherent_child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_game_child_entrypoint_generation2
    as coherent_entry,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_generation2
    as historical_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_source_binding_review_generation2
    as historical_parent_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "parent-supervisor-wiring-contract.v1"
)

COHERENT_CHILD_REVIEW_MAIN_HEAD = (
    "b3293e69790ad90b02ae7e38fc4b078c1c15c707"
)
COHERENT_CHILD_REVIEW_GIT_BLOB = (
    "b8aa17ee161f2b2377ef6d80f1408d04268a2f22"
)
COHERENT_CHILD_REVIEW_SOURCE_SHA256 = (
    "74520b1cf16a6f2086a99b3f5d6f08a15bc276a9be8d368b82592455a05e28f7"
)
COHERENT_CHILD_REVIEW_TEST_GIT_BLOB = (
    "0036a60a122a38f758b3b8ac0986744437d05059"
)
COHERENT_CHILD_REVIEW_TEST_SHA256 = (
    "b1d77131a06b0a71e5feb93d2fbdf890acc71ea581a5a925719c30d308e7ef6f"
)

HISTORICAL_PARENT_WIRING_GIT_BLOB = (
    "c30cf75b26d5e0cecee08286717d8a856e2233bd"
)
HISTORICAL_PARENT_WIRING_SOURCE_SHA256 = (
    "9af96b7e3923eeb221fdba2c34e946b0776124549af7ba22a62e83c5306d72b0"
)

PAIR_SLOT = 6
ARM = "baseline"

COHERENT_CHILD_MODULE = (
    "openra_env.learning."
    "abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_"
    "contract_coherence_repair_proto_game_child_entrypoint_generation2"
)

ORIGINAL_HISTORICAL_CHILD_COMMAND = (
    historical_parent._combat_priority_child_command
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_parent_supervisor_wiring_review"
)


class Pair06V8CombatPriorityCoherentParentWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentParentWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    child = (
        coherent_child_review
        .pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    )
    parent = (
        historical_parent_review
        .pair06_v8_combat_priority_parent_supervisor_wiring_review_contract()
    )
    child_entry = (
        coherent_entry
        .pair06_v8_combat_priority_coherent_child_entrypoint_contract()
    )

    _require(
        child.get("pair06_v8_combat_priority_coherent_proto_child_wiring_reviewed")
        is True,
        "coherent proto-child review missing",
    )
    _require(
        child.get("production_functions_filtered_to_offered_surface") is True,
        "coherent contract repair missing",
    )
    _require(
        child.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and child.get("consumed_attempt_reusable") is False,
        "consumed attempt lineage drift",
    )
    _require(
        child.get("attempt_retry_authorized") is False
        and child.get("runtime_execution_authorized") is False,
        "coherent child review unexpectedly grants execution",
    )
    _require(
        child.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "coherent parent frontier drift",
    )

    _require(
        parent.get("pair06_v8_combat_priority_parent_supervisor_wiring_reviewed")
        is True,
        "historical combat-priority parent review missing",
    )
    _require(
        parent.get("canonical_invocation_lane")
        == "receipt_bound_no_offload_fresh_preclaim_gpu",
        "historical parent invocation lane drift",
    )
    _require(
        parent.get("maximum_attempts_required") == 1
        and parent.get("automatic_retry_required") is False,
        "historical parent attempt boundary drift",
    )
    _require(
        parent.get("runtime_execution_authorized") is False,
        "historical parent review unexpectedly grants execution",
    )

    _require(
        child_entry.get(
            "pair06_v8_combat_priority_coherent_child_entrypoint_implemented"
        )
        is True,
        "coherent child entrypoint missing",
    )
    _require(
        child_entry.get("attempt_retry_authorized") is False
        and child_entry.get("consumed_attempt_reusable") is False,
        "coherent child entrypoint retry boundary drift",
    )

    return {
        "coherent_child_review": deepcopy(child),
        "historical_parent_review": deepcopy(parent),
        "coherent_child_entrypoint": deepcopy(child_entry),
    }


def _coherent_child_command(
    *,
    child_fd: int,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
) -> list[str]:
    return [
        str(coherent_entry.PROTO_PYTHON),
        "-B",
        "-m",
        COHERENT_CHILD_MODULE,
        "--fd",
        str(child_fd),
        "--attempt-id",
        attempt_id,
        "--runs-root",
        runs_root,
        "--frozen-source-root",
        frozen_source_root,
        "--exact-engine-root",
        exact_engine_root,
        "--confirm",
        coherent_entry.CONFIRM_TOKEN,
        "--policy-confirm",
        coherent_entry.POLICY_CONFIRM_TOKEN,
    ]


def execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload(
    *,
    attempt_id: str,
    attempt_claimed: bool,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    execution_authorized: bool,
    authority_check: Callable[[int, str], bool],
) -> dict[str, Any]:
    """Delegate one historical parent call with a scoped coherent child command."""
    _dependencies()

    _require(
        policy_activation_authorized is True,
        "PAIR06_V8_COMBAT_PRIORITY_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        execution_authorized is True,
        "PAIR06_V8_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    _require(
        historical_parent._combat_priority_child_command
        is ORIGINAL_HISTORICAL_CHILD_COMMAND,
        "historical combat-priority child-command builder drift",
    )

    historical_parent._combat_priority_child_command = _coherent_child_command
    try:
        result = (
            historical_parent
            .execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
                attempt_id=attempt_id,
                attempt_claimed=attempt_claimed,
                runs_root=runs_root,
                frozen_source_root=frozen_source_root,
                exact_engine_root=exact_engine_root,
                policy_activation_authorized=True,
                execution_authorized=True,
                authority_check=authority_check,
            )
        )
        _require(
            isinstance(result, dict),
            "pair06 historical parent receipt must be object",
        )
        return result
    finally:
        historical_parent._combat_priority_child_command = (
            ORIGINAL_HISTORICAL_CHILD_COMMAND
        )


def pair06_v8_combat_priority_coherent_parent_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "coherent_child_review_main_head": COHERENT_CHILD_REVIEW_MAIN_HEAD,
        "coherent_child_review_git_blob": COHERENT_CHILD_REVIEW_GIT_BLOB,
        "coherent_child_review_source_sha256": (
            COHERENT_CHILD_REVIEW_SOURCE_SHA256
        ),
        "coherent_child_review_test_git_blob": (
            COHERENT_CHILD_REVIEW_TEST_GIT_BLOB
        ),
        "coherent_child_review_test_sha256": (
            COHERENT_CHILD_REVIEW_TEST_SHA256
        ),
        "historical_parent_wiring_git_blob": HISTORICAL_PARENT_WIRING_GIT_BLOB,
        "historical_parent_wiring_source_sha256": (
            HISTORICAL_PARENT_WIRING_SOURCE_SHA256
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "coherent_child_entrypoint_implemented": True,
        "historical_parent_wiring_source_modified": False,
        "historical_no_offload_parent_source_modified": False,
        "historical_child_command_builder_reused": True,
        "coherent_child_command_substitution_implemented": True,
        "coherent_child_command_substitution_scoped_to_single_call": True,
        "historical_child_command_restored_in_finally": True,
        "existing_execution_confirmation_token_preserved": True,
        "existing_policy_activation_confirmation_token_preserved": True,
        "existing_no_offload_model_loader_reused": True,
        "existing_cuda0_placement_checks_reused": True,
        "existing_parent_decision_service_loop_reused": True,
        "existing_child_retirement_reused": True,
        "existing_parent_receipt_returned_unchanged": True,
        "production_functions_filtered_to_offered_surface": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "attempt_retry_authorized": False,
        "operator_invocation_repair_implemented": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_operator_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentParentWiringHold(NEXT_GATE)
