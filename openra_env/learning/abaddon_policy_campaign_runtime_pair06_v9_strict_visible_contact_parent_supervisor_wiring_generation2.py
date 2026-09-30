"""Source-only parent-supervisor wiring for pair-06 V9 strict contact.

The reviewed inference-safe no-offload V8 parent remains unchanged. This module
wraps exactly one delegated parent call and temporarily substitutes only its
child-command builder so the spawned proto child uses the separately reviewed
V9 strict-visible-contact child entrypoint.

The existing parent continues to own model loading/inference, CUDA:0 placement
checks, socketpair creation, process-group supervision, authority checks,
receipt construction, child retirement, and model-reference release.

The existing durable attempt-claim prerequisite is preserved. This wrapper does
not create an attempt claim, execution request, or attempt. Both explicit game
execution authorization and separate V9 policy-activation authorization remain
required before delegation.

Import and contract inspection are inert.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_source_binding_review_generation2
    as child_wiring_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-parent-supervisor-wiring-contract.v1"
)

V9_CHILD_WIRING_REVIEW_GIT_BLOB = (
    "747dd644fdff569745854f5a3d35758e150e5d2f"
)
NO_OFFLOAD_PARENT_GIT_BLOB = (
    "231758aeced0a57949dc39165df0f994e8473ebc"
)
NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB = (
    "6a65984b81e563def012c6da1405ad47747bb465"
)

PAIR_SLOT = 6
ARM = "baseline"

V9_CHILD_MODULE = (
    "openra_env.learning."
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_proto_game_child_entrypoint_generation2"
)

ORIGINAL_CHILD_COMMAND = parent._child_command

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_parent_supervisor_wiring_review"
)


class Pair06V9StrictVisibleContactParentWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactParentWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    child = (
        child_wiring_review
        .pair06_v9_strict_visible_contact_proto_child_wiring_review_contract()
    )
    reviewed_parent = (
        parent_review
        .pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    )
    entry = child_entry.pair06_v9_strict_visible_contact_child_entrypoint_contract()

    _require(
        child.get(
            "pair06_v9_strict_visible_contact_proto_child_wiring_reviewed"
        )
        is True,
        "V9 proto-child wiring not reviewed",
    )
    _require(
        child.get("original_child_execution_authorization_gate_preserved")
        is True
        and child.get("additional_v9_policy_activation_gate_required") is True,
        "V9 child authorization boundary drift",
    )
    _require(
        child.get("coherent_v9_tool_contract_path_preserved") is True,
        "V9 coherent child path drift",
    )
    _require(
        child.get("new_execution_request_opened") is False
        and child.get("attempt_created") is False
        and child.get("runtime_execution_authorized") is False,
        "V9 child review unexpectedly grants execution authority",
    )
    _require(
        child.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED",
        "V9 parent-supervisor frontier drift",
    )

    _require(
        reviewed_parent.get(
            "pair06_v8_parent_launcher_supervisor_no_offload_reviewed"
        )
        is True,
        "reviewed no-offload parent missing",
    )
    _require(
        reviewed_parent.get("pair_slot") == PAIR_SLOT
        and reviewed_parent.get("arm") == ARM,
        "no-offload parent scope drift",
    )
    _require(
        reviewed_parent.get("inference_safe_no_offload_loader_reviewed")
        is True,
        "no-offload inference-safe loader review missing",
    )
    _require(
        reviewed_parent.get("cpu_disk_meta_parameter_offload_forbidden")
        is True
        and reviewed_parent.get(
            "all_parameters_cuda0_required_before_child_spawn"
        )
        is True,
        "no-offload CUDA placement invariant drift",
    )
    _require(
        reviewed_parent.get("automatic_retry") is False
        and reviewed_parent.get("execution_authorized") is False,
        "no-offload parent unexpectedly grants execution authority",
    )

    _require(
        entry.get(
            "pair06_v9_strict_visible_contact_child_entrypoint_implemented"
        )
        is True,
        "V9 child entrypoint missing",
    )
    _require(
        entry.get("existing_execution_confirmation_token_required") is True
        and entry.get("separate_v9_policy_activation_token_required") is True
        and entry.get("execution_and_policy_confirmation_tokens_distinct")
        is True,
        "V9 child entrypoint token boundary drift",
    )
    _require(
        entry.get("attempt_claim_created_by_entrypoint") is False
        and entry.get("execution_request_created_by_entrypoint") is False,
        "V9 child entrypoint unexpectedly creates execution lineage",
    )

    return {
        "v9_child_wiring_review": deepcopy(child),
        "no_offload_parent_review": deepcopy(reviewed_parent),
        "v9_child_entrypoint": deepcopy(entry),
    }


def _v9_child_command(
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
        V9_CHILD_MODULE,
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
        child_entry.CONFIRM_TOKEN,
        "--policy-confirm",
        child_entry.POLICY_CONFIRM_TOKEN,
    ]


def execute_pair06_v9_strict_visible_contact_parent_supervisor_no_offload(
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
    """Delegate one no-offload parent call with scoped V9 child-command wiring."""
    _dependencies()

    _require(
        policy_activation_authorized is True,
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        execution_authorized is True,
        "PAIR06_V8_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    _require(
        parent._child_command is ORIGINAL_CHILD_COMMAND,
        "pair06 no-offload parent child-command factory drift",
    )

    parent._child_command = _v9_child_command
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


def pair06_v9_strict_visible_contact_parent_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "v9_child_wiring_review_git_blob": V9_CHILD_WIRING_REVIEW_GIT_BLOB,
        "no_offload_parent_git_blob": NO_OFFLOAD_PARENT_GIT_BLOB,
        "no_offload_parent_review_git_blob": NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "v9_child_entrypoint_implemented": True,
        "existing_no_offload_parent_source_modified": False,
        "child_command_builder_substitution_implemented": True,
        "child_command_builder_substitution_scoped_to_single_call": True,
        "child_command_builder_restored_in_finally": True,
        "existing_execution_confirmation_token_preserved": True,
        "separate_v9_policy_activation_token_added": True,
        "existing_no_offload_model_loader_reused": True,
        "existing_cuda0_placement_checks_reused": True,
        "existing_parent_decision_service_loop_reused": True,
        "existing_child_retirement_reused": True,
        "existing_parent_receipt_returned_unchanged": True,
        "existing_parent_automatic_retry": False,
        "durable_attempt_claim_required_by_existing_parent": True,
        "attempt_claim_created_by_this_wiring": False,
        "execution_request_created_by_this_wiring": False,
        "attempt_created_by_this_wiring": False,
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
        "scheduler_mutation_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_operator_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactParentWiringHold(NEXT_GATE)
