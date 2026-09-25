"""Source-only proto-child wiring for the pair-06 V8 combat-priority hook.

The existing reviewed proto child remains byte-for-byte unchanged. This module
provides an isolated wrapper that, for one explicitly authorized child call,
temporarily substitutes only the proto child's hook factory with a subclass
whose decision hook is the reviewed combat-priority runtime integration.

The substitution is process-local, scoped to one call, and restored in a
finally block. The existing child execution authorization gate remains intact,
and an additional explicit policy-activation gate is required here.

This module does not wire the parent supervisor or operator entrypoint and
grants no runtime activation, game execution, replay, training, promotion,
deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_generation2
    as combat_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_source_binding_review_generation2
    as integration_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as proto_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_source_binding_review_generation2
    as proto_child_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-proto-child-wiring-contract.v1"
)

INTEGRATION_REVIEW_MAIN_HEAD = (
    "9b03426a30a4855a01f4666d0354775afa70fdaf"
)
INTEGRATION_REVIEW_GIT_BLOB = (
    "4849fe2fd54846144dc72b1cca00dee5f392de7c"
)
INTEGRATION_REVIEW_SOURCE_SHA256 = (
    "2fab6841e92866199b9cc3cb55ee99a4b586a7aa96b53b7b6c793bd49b7f545f"
)
INTEGRATION_REVIEW_TEST_GIT_BLOB = (
    "a364642a47e46e0ac69185adeb9d1df9446b02bc"
)
INTEGRATION_REVIEW_TEST_SHA256 = (
    "a6c4979734e5fa9d5af1cdca140ce748f63be821a93bfec2451279735955f605"
)

PROTO_CHILD_GIT_BLOB = "7ea5d27c2d2bb499dfec4c00d2812d7ed043f8bc"
PROTO_CHILD_SOURCE_SHA256 = (
    "d621ecd7a20c824ead5247d84fef5fb817df337063cd5ab558c68d42f346601a"
)
PROTO_CHILD_REVIEW_GIT_BLOB = (
    "bd2d7d97a9ed9c04be3bddae5f64977265686fa5"
)
PROTO_CHILD_REVIEW_SOURCE_SHA256 = (
    "8a6d62ca43f3475fab51481e75670a0a5e79ddc7cbc3865ad4ad34db50d8536c"
)

PAIR_SLOT = 6
ARM = "baseline"

ORIGINAL_PROTO_CHILD_HOOKS = proto_child.Pair06V8ProtoChildHooks

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_proto_child_wiring_review"
)


class Pair06V8CombatActionPriorityProtoChildWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityProtoChildWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    integration = (
        integration_review
        .pair06_v8_combat_action_priority_runtime_integration_review_contract()
    )
    child = proto_child_review.pair06_v8_proto_game_child_review_contract()

    _require(
        integration.get(
            "pair06_v8_combat_action_priority_runtime_integration_reviewed"
        )
        is True,
        "pair06 combat-priority runtime integration not reviewed",
    )
    _require(
        integration.get("decision_hook_runtime_integration_implemented")
        is True,
        "pair06 combat-priority decision hook integration missing",
    )
    _require(
        integration.get("proto_game_child_wiring_implemented") is False,
        "pair06 combat-priority proto-child wiring already present",
    )
    _require(
        integration.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_REQUIRED",
        "pair06 proto-child wiring frontier drift",
    )

    _require(
        child.get("pair06_v8_proto_game_child_reviewed") is True,
        "pair06 existing proto child not reviewed",
    )
    _require(child.get("pair_slot") == PAIR_SLOT, "pair06 child slot drift")
    _require(child.get("arm") == ARM, "pair06 child arm drift")
    _require(
        child.get("child_git_blob") == PROTO_CHILD_GIT_BLOB,
        "pair06 proto child source identity drift",
    )
    _require(
        child.get("game_execution_authorized") is False,
        "pair06 existing proto child unexpectedly authorizes execution",
    )
    _require(
        child.get("automatic_retry") is False,
        "pair06 existing proto child automatic retry enabled",
    )

    return {
        "integration_review": integration,
        "proto_child_review": child,
    }


class Pair06V8CombatPriorityProtoChildHooks(ORIGINAL_PROTO_CHILD_HOOKS):
    """Existing proto-child hooks with only the decision hook replaced."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        super().__init__(legacy, sock, attempt_id)

        original_decision_hooks = self._decision_hooks
        _require(
            getattr(original_decision_hooks, "_installed", False) is False,
            "legacy decision hooks unexpectedly installed during construction",
        )

        self._decision_hooks = (
            combat_integration.Pair06V8CombatPriorityDecisionHooks(
                legacy,
                self._ipc_decider,
            )
        )
        self.combat_priority_decision_hook_bound = True


def run_pair06_v8_combat_priority_proto_game_child(
    *,
    sock: Any,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    execution_authorized: bool,
) -> dict[str, Any]:
    """Delegate one child call with scoped combat-priority hook substitution."""
    _dependencies()

    _require(
        policy_activation_authorized is True,
        "PAIR06_V8_COMBAT_PRIORITY_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
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
        Pair06V8CombatPriorityProtoChildHooks
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
            "pair06 proto child result must be object",
        )
        return result
    finally:
        proto_child.Pair06V8ProtoChildHooks = ORIGINAL_PROTO_CHILD_HOOKS


def pair06_v8_combat_action_priority_proto_child_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "integration_review_main_head": INTEGRATION_REVIEW_MAIN_HEAD,
        "integration_review_git_blob": INTEGRATION_REVIEW_GIT_BLOB,
        "integration_review_source_sha256": (
            INTEGRATION_REVIEW_SOURCE_SHA256
        ),
        "integration_review_test_git_blob": (
            INTEGRATION_REVIEW_TEST_GIT_BLOB
        ),
        "integration_review_test_sha256": (
            INTEGRATION_REVIEW_TEST_SHA256
        ),
        "proto_child_git_blob": PROTO_CHILD_GIT_BLOB,
        "proto_child_source_sha256": PROTO_CHILD_SOURCE_SHA256,
        "proto_child_review_git_blob": PROTO_CHILD_REVIEW_GIT_BLOB,
        "proto_child_review_source_sha256": (
            PROTO_CHILD_REVIEW_SOURCE_SHA256
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "existing_proto_child_source_modified": False,
        "combat_priority_proto_child_hook_subclass_implemented": True,
        "existing_proto_child_hook_factory_reused": True,
        "hook_factory_substitution_scoped_to_single_call": True,
        "hook_factory_restored_in_finally": True,
        "original_child_execution_authorization_gate_preserved": True,
        "additional_policy_activation_gate_required": True,
        "reviewed_combat_priority_decision_hook_used": True,
        "existing_ipc_decider_reused": True,
        "existing_legacy_runner_reused": True,
        "existing_portable_worktree_binding_reused": True,
        "parent_supervisor_wiring_implemented": False,
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


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityProtoChildWiringHold(NEXT_GATE)
