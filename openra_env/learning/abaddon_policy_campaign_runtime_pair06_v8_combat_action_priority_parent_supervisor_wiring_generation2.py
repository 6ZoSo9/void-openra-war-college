"""Source-only combat-priority wiring for the pair-06 no-offload parent.

The reviewed inference-safe no-offload parent supervisor remains byte-for-byte
unchanged. This module wraps exactly one call and temporarily substitutes only
its child-command builder so the spawned proto child uses the separately
reviewed combat-priority entrypoint.

The existing parent still owns model load/inference, CUDA:0 placement checks,
socketpair creation, child process-group supervision, authority checks, receipt
construction, retirement, and V8 reference release.

Both explicit execution authorization and separate combat-priority policy
activation authorization are required before delegation. The child-command
builder is restored in a finally block.

This source does not create attempt claims, materialize worktrees, activate an
operator entrypoint, or authorize an actual run by contract inspection.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_game_child_entrypoint_generation2
    as combat_child_entry,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_source_binding_review_generation2
    as child_wiring_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2
    as legacy_child_entry,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-parent-supervisor-wiring-contract.v1"
)

CHILD_WIRING_REVIEW_MAIN_HEAD = (
    "83b852117c51bda876b1f4bc18ffd804922054b4"
)
CHILD_WIRING_REVIEW_GIT_BLOB = (
    "e0247e50ead91356f60e57b454331fba8e2ae69c"
)
NO_OFFLOAD_PARENT_GIT_BLOB = (
    "231758aeced0a57949dc39165df0f994e8473ebc"
)
NO_OFFLOAD_PARENT_SOURCE_SHA256 = (
    "1333cac233d6e9235a2d64c36b8398bb4773150cf2fe5025f28fed5457fe7d7f"
)
NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB = (
    "6a65984b81e563def012c6da1405ad47747bb465"
)

PAIR_SLOT = 6
ARM = "baseline"

COMBAT_PRIORITY_CHILD_MODULE = (
    "openra_env.learning."
    "abaddon_policy_campaign_runtime_pair06_v8_"
    "combat_action_priority_proto_game_child_entrypoint_generation2"
)

ORIGINAL_CHILD_COMMAND = parent._child_command

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_parent_supervisor_wiring_review"
)


class Pair06V8CombatPriorityParentWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityParentWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    child = (
        child_wiring_review
        .pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    )
    reviewed_parent = (
        parent_review
        .pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    )
    child_entry = (
        combat_child_entry
        .pair06_v8_combat_priority_proto_child_entrypoint_contract()
    )

    _require(
        child.get(
            "pair06_v8_combat_action_priority_proto_child_wiring_reviewed"
        )
        is True,
        "pair06 combat-priority proto-child wiring not reviewed",
    )
    _require(
        child.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED",
        "pair06 parent wiring frontier drift",
    )

    _require(
        reviewed_parent.get(
            "pair06_v8_parent_launcher_supervisor_no_offload_reviewed"
        )
        is True,
        "pair06 no-offload parent supervisor not reviewed",
    )
    _require(
        reviewed_parent.get("pair_slot") == PAIR_SLOT,
        "pair06 no-offload parent slot drift",
    )
    _require(
        reviewed_parent.get("arm") == ARM,
        "pair06 no-offload parent arm drift",
    )
    _require(
        reviewed_parent.get("inference_safe_no_offload_loader_reviewed")
        is True,
        "pair06 no-offload loader review missing",
    )
    _require(
        reviewed_parent.get("cpu_disk_meta_parameter_offload_forbidden")
        is True
        and reviewed_parent.get("all_parameters_cuda0_required_before_child_spawn")
        is True,
        "pair06 no-offload CUDA placement invariant drift",
    )
    _require(
        reviewed_parent.get("automatic_retry") is False,
        "pair06 no-offload parent automatic retry enabled",
    )
    _require(
        reviewed_parent.get("execution_authorized") is False,
        "pair06 no-offload parent review unexpectedly authorizes execution",
    )

    _require(
        child_entry.get(
            "pair06_v8_combat_priority_proto_child_entrypoint_implemented"
        )
        is True,
        "pair06 combat-priority child entrypoint missing",
    )
    _require(
        child_entry.get("separate_policy_activation_token_required") is True,
        "pair06 separate policy activation token missing",
    )

    return {
        "child_wiring_review": deepcopy(child),
        "no_offload_parent_review": deepcopy(reviewed_parent),
        "combat_priority_child_entrypoint": deepcopy(child_entry),
    }


def _combat_priority_child_command(
    *,
    child_fd: int,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
) -> list[str]:
    return [
        str(parent.PROTO_PYTHON),
        "-B",
        "-m",
        COMBAT_PRIORITY_CHILD_MODULE,
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
        legacy_child_entry.CONFIRM_TOKEN,
        "--policy-confirm",
        combat_child_entry.POLICY_CONFIRM_TOKEN,
    ]


def execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
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
    """Delegate one no-offload parent call with scoped child-command wiring."""
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
        parent._child_command is ORIGINAL_CHILD_COMMAND,
        "pair06 no-offload parent child-command factory drift",
    )

    parent._child_command = _combat_priority_child_command
    try:
        result = parent.execute_pair06_v8_parent_supervisor_no_offload(
            attempt_id=attempt_id,
            attempt_claimed=attempt_claimed,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
            execution_authorized=True,
            authority_check=authority_check,
        )
        _require(
            isinstance(result, dict),
            "pair06 no-offload parent receipt must be object",
        )
        return result
    finally:
        parent._child_command = ORIGINAL_CHILD_COMMAND


def pair06_v8_combat_priority_parent_supervisor_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "child_wiring_review_main_head": CHILD_WIRING_REVIEW_MAIN_HEAD,
        "child_wiring_review_git_blob": CHILD_WIRING_REVIEW_GIT_BLOB,
        "no_offload_parent_git_blob": NO_OFFLOAD_PARENT_GIT_BLOB,
        "no_offload_parent_source_sha256": NO_OFFLOAD_PARENT_SOURCE_SHA256,
        "no_offload_parent_review_git_blob": NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "combat_priority_child_entrypoint_implemented": True,
        "existing_no_offload_parent_source_modified": False,
        "child_command_builder_substitution_implemented": True,
        "child_command_builder_substitution_scoped_to_single_call": True,
        "child_command_builder_restored_in_finally": True,
        "existing_execution_confirmation_token_preserved": True,
        "separate_policy_activation_token_added": True,
        "existing_no_offload_model_loader_reused": True,
        "existing_cuda0_placement_checks_reused": True,
        "existing_parent_decision_service_loop_reused": True,
        "existing_child_retirement_reused": True,
        "existing_parent_receipt_returned_unchanged": True,
        "existing_parent_automatic_retry": False,
        "attempt_claim_required": True,
        "operator_entrypoint_wiring_implemented": False,
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
    raise Pair06V8CombatPriorityParentWiringHold(NEXT_GATE)
