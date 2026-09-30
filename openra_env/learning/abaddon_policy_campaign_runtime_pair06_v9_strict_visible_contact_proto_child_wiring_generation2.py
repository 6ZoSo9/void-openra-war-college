"""Source-only proto-child wiring for pair-06 V9 strict visible contact.

The reviewed pair-06 V8 proto-game child remains unchanged. This module
provides an isolated wrapper that temporarily substitutes only the proto-child
hook factory with a subclass whose decision hook is the reviewed V9 strict-
visible-contact runtime integration.

The substitution is process-local, scoped to one delegated child call, and
restored in a finally block. The existing child execution authorization gate is
preserved and a separate explicit V9 policy-activation gate is required.

This source does not wire the parent supervisor or operator entrypoint, does not
create an execution request or attempt, and grants no runtime activation,
execution, replay, training, promotion, deployment, VOID-chain, wallet,
transaction, funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as proto_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_source_binding_review_generation2
    as proto_child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_generation2
    as v9_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_source_binding_review_generation2
    as v9_integration_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-proto-child-wiring-contract.v1"
)

V9_INTEGRATION_GIT_BLOB = "8aa8a3bae62a914dfa1c1b7daf2fca6b13ecf2ef"
V9_INTEGRATION_REVIEW_GIT_BLOB = "9e92605527aeea59f9d99cfcb798adea569f7309"
PROTO_CHILD_GIT_BLOB = "7ea5d27c2d2bb499dfec4c00d2812d7ed043f8bc"
PROTO_CHILD_REVIEW_GIT_BLOB = "bd2d7d97a9ed9c04be3bddae5f64977265686fa5"

PAIR_SLOT = 6
ARM = "baseline"

ORIGINAL_PROTO_CHILD_HOOKS = proto_child.Pair06V8ProtoChildHooks

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_proto_child_wiring_review"
)


class Pair06V9StrictVisibleContactProtoChildWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactProtoChildWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    integration = (
        v9_integration_review
        .pair06_v9_strict_visible_contact_runtime_integration_review_contract()
    )
    child = proto_child_review.pair06_v8_proto_game_child_review_contract()

    _require(
        integration.get(
            "pair06_v9_strict_visible_contact_runtime_integration_reviewed"
        )
        is True,
        "V9 strict-contact runtime integration not reviewed",
    )
    _require(
        integration.get("decision_hook_runtime_integration_implemented")
        is True,
        "V9 decision-hook integration missing",
    )
    _require(
        integration.get("coherent_filtered_surface_reviewed") is True
        and integration.get("unchanged_legacy_host_validator_reviewed")
        is True
        and integration.get("six_attempt_fail_closed_retry_reviewed")
        is True
        and integration.get("frozen_compact_state_reuse_reviewed")
        is True,
        "V9 reviewed decision boundary drift",
    )
    _require(
        integration.get("proto_game_child_wiring_implemented") is False
        and integration.get("parent_supervisor_wiring_implemented") is False
        and integration.get("new_execution_request_opened") is False,
        "V9 integration unexpectedly crossed child/runtime boundary",
    )
    _require(
        integration.get("runtime_activation_authorized") is False
        and integration.get("runtime_execution_authorized") is False,
        "V9 integration unexpectedly grants runtime authority",
    )
    _require(
        integration.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_REQUIRED",
        "V9 proto-child wiring frontier drift",
    )

    _require(
        child.get("pair06_v8_proto_game_child_reviewed") is True,
        "existing pair06 proto child not reviewed",
    )
    _require(child.get("pair_slot") == PAIR_SLOT, "pair06 child slot drift")
    _require(child.get("arm") == ARM, "pair06 child arm drift")
    _require(
        child.get("child_git_blob") == PROTO_CHILD_GIT_BLOB,
        "pair06 proto-child source identity drift",
    )
    _require(
        child.get("game_execution_authorized") is False,
        "existing proto child unexpectedly authorizes execution",
    )
    _require(
        child.get("automatic_retry") is False,
        "existing proto child automatic retry enabled",
    )

    return {
        "v9_runtime_integration_review": deepcopy(integration),
        "proto_child_review": deepcopy(child),
    }


class Pair06V9StrictVisibleContactProtoChildHooks(ORIGINAL_PROTO_CHILD_HOOKS):
    """Existing proto-child hooks with only the decision hook advanced to V9."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        super().__init__(legacy, sock, attempt_id)

        original_decision_hooks = self._decision_hooks
        _require(
            getattr(original_decision_hooks, "_installed", False) is False,
            "existing decision hooks unexpectedly installed during construction",
        )

        self._decision_hooks = (
            v9_integration.Pair06V9StrictVisibleContactDecisionHooks(
                legacy,
                self._ipc_decider,
            )
        )
        self.v9_strict_visible_contact_decision_hook_bound = True


def run_pair06_v9_strict_visible_contact_proto_game_child(
    *,
    sock: Any,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    execution_authorized: bool,
) -> dict[str, Any]:
    """Delegate one child call with scoped V9 hook-factory substitution."""
    _dependencies()

    _require(
        policy_activation_authorized is True,
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        execution_authorized is True,
        "PAIR06_V8_CHILD_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    _require(
        proto_child.Pair06V8ProtoChildHooks is ORIGINAL_PROTO_CHILD_HOOKS,
        "pair06 proto-child hook factory drift before scoped substitution",
    )

    proto_child.Pair06V8ProtoChildHooks = (
        Pair06V9StrictVisibleContactProtoChildHooks
    )
    try:
        result = proto_child.run_pair06_v8_proto_game_child(
            sock=sock,
            attempt_id=attempt_id,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
            execution_authorized=True,
        )
        _require(
            isinstance(result, dict),
            "pair06 V9 proto-child result must be object",
        )
        return result
    finally:
        proto_child.Pair06V8ProtoChildHooks = ORIGINAL_PROTO_CHILD_HOOKS


def pair06_v9_strict_visible_contact_proto_child_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "v9_integration_git_blob": V9_INTEGRATION_GIT_BLOB,
        "v9_integration_review_git_blob": V9_INTEGRATION_REVIEW_GIT_BLOB,
        "proto_child_git_blob": PROTO_CHILD_GIT_BLOB,
        "proto_child_review_git_blob": PROTO_CHILD_REVIEW_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "existing_proto_child_source_modified": False,
        "v9_proto_child_hook_subclass_implemented": True,
        "existing_proto_child_hook_factory_reused": True,
        "hook_factory_substitution_scoped_to_single_call": True,
        "hook_factory_restored_in_finally": True,
        "original_child_execution_authorization_gate_preserved": True,
        "additional_v9_policy_activation_gate_required": True,
        "reviewed_v9_decision_hook_used": True,
        "coherent_v9_tool_contract_path_preserved": True,
        "existing_ipc_decider_reused": True,
        "existing_legacy_runner_reused": True,
        "existing_portable_worktree_binding_reused": True,
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
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactProtoChildWiringHold(NEXT_GATE)
