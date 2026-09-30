"""Exact-blob source review of pair-06 V9 proto-child wiring.

Pins the scoped proto-child wrapper and regression suite. The review confirms
that the existing reviewed proto-game child remains unchanged, the V9 decision
hook is bound only through a temporary hook-factory substitution, and both the
existing child execution gate and additional V9 policy-activation gate remain
required.

No parent-supervisor or operator wiring is present. No execution request or
attempt is created, and no runtime activation, execution, replay, training,
promotion, deployment, chain, wallet, transaction, funds, or scheduler
authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_generation2
    as wiring,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-proto-child-wiring-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "18e4466e6996e88c7ce4382166d0cec794c4aad7"
WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_proto_child_wiring_generation2.py"
)
WIRING_GIT_BLOB = "5fc4c66b0c0f23edb8c4932bba1c743fd63b9b12"
WIRING_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_proto_child_wiring_generation2.py"
)
WIRING_TEST_GIT_BLOB = "c5b5277256f3ce06679acbb1bc8df166c548412e"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_parent_supervisor_wiring"
)


class Pair06V9StrictVisibleContactProtoChildWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactProtoChildWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated_wiring() -> dict[str, Any]:
    out = (
        wiring
        .pair06_v9_strict_visible_contact_proto_child_wiring_contract()
    )

    _require(
        out.get("v9_proto_child_hook_subclass_implemented") is True,
        "V9 proto-child hook subclass missing",
    )
    _require(
        out.get("existing_proto_child_source_modified") is False,
        "existing proto-child source unexpectedly modified",
    )
    _require(
        out.get("existing_proto_child_hook_factory_reused") is True
        and out.get("hook_factory_substitution_scoped_to_single_call") is True
        and out.get("hook_factory_restored_in_finally") is True,
        "V9 scoped hook substitution invariant drift",
    )
    _require(
        out.get("original_child_execution_authorization_gate_preserved")
        is True
        and out.get("additional_v9_policy_activation_gate_required") is True,
        "V9 child authorization-gate drift",
    )
    _require(
        out.get("reviewed_v9_decision_hook_used") is True
        and out.get("coherent_v9_tool_contract_path_preserved") is True
        and out.get("existing_ipc_decider_reused") is True
        and out.get("existing_legacy_runner_reused") is True
        and out.get("existing_portable_worktree_binding_reused") is True,
        "V9 reviewed child-reuse invariant drift",
    )
    _require(
        out.get("new_execution_request_opened") is False
        and out.get("attempt_created") is False,
        "V9 proto-child wiring unexpectedly opened execution lineage",
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
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "V9 proto-child wiring boundary drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 proto-child wiring review frontier drift",
    )

    return deepcopy(out)


def pair06_v9_strict_visible_contact_proto_child_wiring_review_contract() -> dict[str, Any]:
    validated = _validated_wiring()
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "wiring_path": WIRING_PATH,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_test_path": WIRING_TEST_PATH,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "pair06_v9_strict_visible_contact_proto_child_wiring_reviewed": True,
        "existing_proto_child_source_modified": False,
        "v9_proto_child_hook_subclass_reviewed": True,
        "hook_factory_substitution_scoped_to_single_call": True,
        "hook_factory_restored_in_finally": True,
        "original_child_execution_authorization_gate_preserved": True,
        "additional_v9_policy_activation_gate_required": True,
        "coherent_v9_tool_contract_path_preserved": True,
        "parent_supervisor_wiring_implemented": False,
        "operator_entrypoint_wiring_implemented": False,
        "new_execution_request_opened": False,
        "attempt_created": False,
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
        "validated_wiring": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactProtoChildWiringReviewHold(NEXT_GATE)
