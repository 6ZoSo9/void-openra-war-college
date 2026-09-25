"""Source-only review of pair-06 V8 combat-priority proto-child wiring.

Pins the exact scoped proto-child wiring merged by #293 and confirms that the
existing reviewed proto-child source remains unchanged. This review grants no
runtime activation, game execution, replay, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_generation2
    as wiring,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-proto-child-wiring-review-contract.v1"
)

WIRING_MAIN_HEAD = "d213f9805de2a0990c831b59ec8a5b73c8d1539a"
WIRING_GIT_BLOB = "7dd120dce2bc39a780ce40b9d167d39ea5cf9bfc"
WIRING_SOURCE_SHA256 = (
    "3483056aab144c412be96ed8e90f27f07c8c0d0988419be64a844e10d870b2b1"
)
WIRING_TEST_GIT_BLOB = "6c58ab0d3692f6a8fc9feb6755e0a140228b9819"
WIRING_TEST_SHA256 = (
    "a762c71c24ef38a9f1798163fdffcc68b9c7c5c3dcf160dbe92b9cfe354905e8"
)

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_parent_supervisor_wiring"
)


class Pair06V8CombatActionPriorityProtoChildWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityProtoChildWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated_wiring() -> dict[str, Any]:
    out = wiring.pair06_v8_combat_action_priority_proto_child_wiring_contract()

    _require(
        out.get("combat_priority_proto_child_hook_subclass_implemented") is True,
        "pair06 combat-priority proto-child hook missing",
    )
    _require(
        out.get("existing_proto_child_source_modified") is False,
        "existing proto child source unexpectedly modified",
    )
    _require(
        out.get("existing_proto_child_hook_factory_reused") is True
        and out.get("hook_factory_substitution_scoped_to_single_call") is True
        and out.get("hook_factory_restored_in_finally") is True,
        "pair06 scoped hook substitution invariant drift",
    )
    _require(
        out.get("original_child_execution_authorization_gate_preserved") is True
        and out.get("additional_policy_activation_gate_required") is True,
        "pair06 child authorization-gate drift",
    )
    _require(
        out.get("reviewed_combat_priority_decision_hook_used") is True
        and out.get("existing_ipc_decider_reused") is True
        and out.get("existing_legacy_runner_reused") is True
        and out.get("existing_portable_worktree_binding_reused") is True,
        "pair06 reviewed-child reuse invariant drift",
    )

    for field in (
        "parent_supervisor_wiring_implemented",
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
        _require(out.get(field) is False, "pair06 wiring boundary drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "pair06 proto-child wiring review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_proto_child_wiring_review_contract() -> dict[str, Any]:
    validated = _validated_wiring()
    return {
        "schema": CONTRACT_SCHEMA,
        "wiring_main_head": WIRING_MAIN_HEAD,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_source_sha256": WIRING_SOURCE_SHA256,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "wiring_test_sha256": WIRING_TEST_SHA256,
        "pair06_v8_combat_action_priority_proto_child_wiring_reviewed": True,
        "existing_proto_child_source_modified": False,
        "hook_factory_substitution_scoped_to_single_call": True,
        "hook_factory_restored_in_finally": True,
        "additional_policy_activation_gate_required": True,
        "parent_supervisor_wiring_implemented": False,
        "operator_entrypoint_wiring_implemented": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_wiring": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityProtoChildWiringReviewHold(NEXT_GATE)
