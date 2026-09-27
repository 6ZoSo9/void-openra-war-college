"""Source-only no-offload parent wiring for the V2 coherent pair-06 child.

The reviewed V1 coherent parent wrapper remains unchanged. This module
temporarily replaces only that wrapper's coherent child-command builder so its
delegated historical no-offload parent launches the V2 coherent child
entrypoint.

All existing no-offload model loading, CUDA:0 placement checks, parent IPC
decision service, child retirement, authority checks, and receipt construction
remain unchanged.

The latest consumed failed attempt remains non-reusable. No retry or execution
authority is granted by contract inspection.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_child_wiring_source_binding_review_generation2
    as v2_child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_game_child_entrypoint_generation2
    as v2_entry,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_parent_supervisor_wiring_generation2
    as v1_parent,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "parent-supervisor-wiring-contract.v1"
)

V2_CHILD_REVIEW_MAIN_HEAD = "c06de6b1a3b52e689064cd007e8d780dbcfcc9ce"
V2_CHILD_REVIEW_GIT_BLOB = "028565625eca8672e90126ec335d07279ae5d6d3"
V2_CHILD_REVIEW_SOURCE_SHA256 = (
    "d4d94d94df6cf123c0a9c102f57c84f1d5dacce710094057509fe8311c6592a5"
)
V2_CHILD_REVIEW_TEST_GIT_BLOB = (
    "2956f1c660a6b7cc4a7e20c1d473b8292f0624cb"
)
V2_CHILD_REVIEW_TEST_SHA256 = (
    "66421b6cc10eac2adc3afa5a81cb4428c615e50a54efca77425109e2c41316c5"
)

V1_COHERENT_PARENT_WIRING_GIT_BLOB = (
    "fa3dcc13b9150a88e12c8fee005f7bf16670a236"
)
V1_COHERENT_PARENT_WIRING_SOURCE_SHA256 = (
    "114b4ce77abddb3ba9c856c78f1331ba22d807d4ecdf6a0fe0dc944773ff32c0"
)

PAIR_SLOT = 6
ARM = "baseline"

V2_CHILD_MODULE = (
    "openra_env.learning."
    "abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_"
    "contract_coherence_repair_v2_proto_game_child_entrypoint_generation2"
)

ORIGINAL_V1_COHERENT_CHILD_COMMAND = v1_parent._coherent_child_command

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_v2_parent_supervisor_wiring_review"
)


class Pair06V8CombatPriorityCoherentV2ParentWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2ParentWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    child = (
        v2_child_review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    parent = v1_parent.pair06_v8_combat_priority_coherent_parent_wiring_contract()
    child_entry = (
        v2_entry
        .pair06_v8_combat_priority_coherent_v2_child_entrypoint_contract()
    )

    _require(
        child.get(
            "pair06_v8_combat_priority_coherent_v2_proto_child_wiring_reviewed"
        )
        is True,
        "V2 coherent proto-child review missing",
    )
    for field in (
        "v2_repaired_decision_hook_bound",
        "translator_legal_building_mapping_coherent",
        "translator_legal_unit_mapping_coherent",
        "existing_child_execution_authorization_gate_preserved",
        "existing_policy_activation_authorization_gate_preserved",
    ):
        _require(child.get(field) is True, "V2 child invariant drift: " + field)

    _require(
        child.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and child.get("consumed_attempt_reusable") is False,
        "latest consumed attempt lineage drift",
    )
    _require(
        child.get("failed_run_id") == FAILED_RUN_ID
        and child.get("failed_run_reusable_as_authority") is False
        and child.get("prior_authorization_reusable") is False,
        "latest failed run/authorization lineage drift",
    )
    _require(
        child.get("attempt_retry_authorized") is False
        and child.get("runtime_execution_authorized") is False,
        "V2 child review unexpectedly grants execution",
    )
    _require(
        child.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "V2 parent frontier drift",
    )

    _require(
        parent.get("pair_slot") == PAIR_SLOT
        and parent.get("arm") == ARM,
        "V1 coherent parent scope drift",
    )
    for field in (
        "coherent_child_command_substitution_implemented",
        "coherent_child_command_substitution_scoped_to_single_call",
        "historical_child_command_restored_in_finally",
        "existing_no_offload_model_loader_reused",
        "existing_cuda0_placement_checks_reused",
        "existing_parent_decision_service_loop_reused",
        "existing_child_retirement_reused",
        "existing_parent_receipt_returned_unchanged",
    ):
        _require(parent.get(field) is True, "V1 coherent parent invariant drift: " + field)
    _require(
        parent.get("runtime_execution_authorized") is False
        and parent.get("automatic_retry") is False,
        "V1 coherent parent unexpectedly grants authority",
    )

    _require(
        child_entry.get(
            "pair06_v8_combat_priority_coherent_v2_child_entrypoint_implemented"
        )
        is True,
        "V2 child entrypoint missing",
    )
    _require(
        child_entry.get("attempt_retry_authorized") is False
        and child_entry.get("consumed_attempt_reusable") is False
        and child_entry.get("prior_authorization_reusable") is False,
        "V2 child entrypoint retry/lineage boundary drift",
    )

    return {
        "v2_child_review": deepcopy(child),
        "v1_coherent_parent_wiring": deepcopy(parent),
        "v2_child_entrypoint": deepcopy(child_entry),
    }


def _v2_child_command(
    *,
    child_fd: int,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
) -> list[str]:
    return [
        str(v2_entry.PROTO_PYTHON),
        "-B",
        "-m",
        V2_CHILD_MODULE,
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
        v2_entry.CONFIRM_TOKEN,
        "--policy-confirm",
        v2_entry.POLICY_CONFIRM_TOKEN,
    ]


def execute_pair06_v8_combat_priority_coherent_v2_parent_supervisor_no_offload(
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
    """Delegate one V1 coherent parent call with a scoped V2 child command."""
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
        v1_parent._coherent_child_command is ORIGINAL_V1_COHERENT_CHILD_COMMAND,
        "V1 coherent child-command builder drift",
    )

    v1_parent._coherent_child_command = _v2_child_command
    try:
        result = (
            v1_parent
            .execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload(
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
            "pair06 V1 coherent parent receipt must be object",
        )
        return result
    finally:
        v1_parent._coherent_child_command = ORIGINAL_V1_COHERENT_CHILD_COMMAND


def pair06_v8_combat_priority_coherent_v2_parent_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "v2_child_review_main_head": V2_CHILD_REVIEW_MAIN_HEAD,
        "v2_child_review_git_blob": V2_CHILD_REVIEW_GIT_BLOB,
        "v2_child_review_source_sha256": V2_CHILD_REVIEW_SOURCE_SHA256,
        "v2_child_review_test_git_blob": V2_CHILD_REVIEW_TEST_GIT_BLOB,
        "v2_child_review_test_sha256": V2_CHILD_REVIEW_TEST_SHA256,
        "v1_coherent_parent_wiring_git_blob": (
            V1_COHERENT_PARENT_WIRING_GIT_BLOB
        ),
        "v1_coherent_parent_wiring_source_sha256": (
            V1_COHERENT_PARENT_WIRING_SOURCE_SHA256
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "v2_child_entrypoint_implemented": True,
        "v1_coherent_parent_wiring_source_modified": False,
        "historical_parent_wiring_source_modified": False,
        "historical_no_offload_parent_source_modified": False,
        "v2_child_command_substitution_implemented": True,
        "v2_child_command_substitution_scoped_to_single_call": True,
        "v1_coherent_child_command_restored_in_finally": True,
        "existing_execution_confirmation_token_preserved": True,
        "existing_policy_activation_confirmation_token_preserved": True,
        "existing_no_offload_model_loader_reused": True,
        "existing_cuda0_placement_checks_reused": True,
        "existing_parent_decision_service_loop_reused": True,
        "existing_child_retirement_reused": True,
        "existing_parent_receipt_returned_unchanged": True,
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_coherent": True,
        "translator_legal_unit_mapping_coherent": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "attempt_retry_authorized": False,
        "operator_invocation_v2_wiring_implemented": False,
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
    raise Pair06V8CombatPriorityCoherentV2ParentWiringHold(NEXT_GATE)
