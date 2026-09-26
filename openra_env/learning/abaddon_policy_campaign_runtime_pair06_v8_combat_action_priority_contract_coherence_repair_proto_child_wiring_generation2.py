"""Source-only proto-child wiring for the reviewed contract-coherence repair.

The historical combat-priority proto-child wiring remains unchanged. This
module subclasses its hook container and replaces only the uninstalled
combat-priority decision hook with the reviewed contract-coherent hook.

The historical combat-priority hook class is temporarily substituted for one
delegated child call and restored in finally. Existing execution and policy
activation gates remain intact.

The consumed failed attempt remains non-reusable. This source grants no retry,
runtime activation, execution, replay, training, deployment, chain mutation,
or wallet/funds authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_generation2
    as repair,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_source_binding_review_generation2
    as repair_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_generation2
    as base_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_source_binding_review_generation2
    as base_wiring_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "proto-child-wiring-contract.v1"
)

REPAIR_REVIEW_MAIN_HEAD = "54741af71ff64af9bfacbe0cc126148cfa8ba5b4"
REPAIR_REVIEW_GIT_BLOB = "bc4738d8e3a069c2094e2efd0724f2ab7ad71133"
REPAIR_REVIEW_TEST_GIT_BLOB = "523bbc11e5d694cdf81bf69dcf1a0bc70ece5632"

BASE_PROTO_CHILD_WIRING_GIT_BLOB = (
    "7dd120dce2bc39a780ce40b9d167d39ea5cf9bfc"
)
BASE_PROTO_CHILD_WIRING_REVIEW_GIT_BLOB = (
    "e0247e50ead91356f60e57b454331fba8e2ae69c"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS = (
    base_wiring.Pair06V8CombatPriorityProtoChildHooks
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_proto_child_wiring_review"
)


class Pair06V8CombatPriorityCoherentProtoChildWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentProtoChildWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    repaired = (
        repair_review
        .pair06_v8_combat_action_priority_contract_coherence_repair_review_contract()
    )
    historical_child = (
        base_wiring_review
        .pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    )

    _require(
        repaired.get(
            "pair06_v8_combat_action_priority_contract_coherence_repair_reviewed"
        )
        is True,
        "contract-coherence repair not reviewed",
    )
    _require(
        repaired.get("production_functions_filtered_to_offered_surface") is True
        and repaired.get("legal_units_preserved") is True
        and repaired.get("legal_buildings_preserved") is True,
        "contract-coherence repair invariant drift",
    )
    _require(
        repaired.get("attempt_retry_authorized") is False
        and repaired.get("runtime_execution_authorized") is False,
        "contract-coherence repair unexpectedly grants runtime authority",
    )
    _require(
        repaired.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "PROTO_CHILD_WIRING_REQUIRED"
        ),
        "repair proto-child frontier drift",
    )

    _require(
        historical_child.get(
            "pair06_v8_combat_action_priority_proto_child_wiring_reviewed"
        )
        is True,
        "historical combat-priority proto-child wiring not reviewed",
    )
    _require(
        historical_child.get("existing_proto_child_source_modified") is False,
        "historical proto child unexpectedly modified",
    )
    _require(
        historical_child.get("additional_policy_activation_gate_required")
        is True,
        "historical policy activation gate missing",
    )
    _require(
        historical_child.get("runtime_execution_authorized") is False,
        "historical child review unexpectedly authorizes execution",
    )

    return {
        "repair_review": deepcopy(repaired),
        "historical_proto_child_wiring_review": deepcopy(historical_child),
    }


class Pair06V8CombatPriorityCoherentProtoChildHooks(
    ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS
):
    """Historical combat-priority child hooks with only decision hook repaired."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        super().__init__(legacy, sock, attempt_id)

        historical_decision_hooks = self._decision_hooks
        _require(
            getattr(historical_decision_hooks, "_installed", False) is False,
            "historical combat-priority hooks unexpectedly installed",
        )

        self._decision_hooks = (
            repair.Pair06V8CombatPriorityContractCoherentDecisionHooks(
                legacy,
                self._ipc_decider,
            )
        )
        self.combat_priority_contract_coherence_repair_bound = True


def run_pair06_v8_combat_priority_coherent_proto_game_child(
    *,
    sock: Any,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    execution_authorized: bool,
) -> dict[str, Any]:
    """Delegate one child call with scoped repaired-hook substitution."""
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
        base_wiring.Pair06V8CombatPriorityProtoChildHooks
        is ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS,
        "historical combat-priority child hook class drift before substitution",
    )

    base_wiring.Pair06V8CombatPriorityProtoChildHooks = (
        Pair06V8CombatPriorityCoherentProtoChildHooks
    )
    try:
        result = base_wiring.run_pair06_v8_combat_priority_proto_game_child(
            sock=sock,
            attempt_id=attempt_id,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
            policy_activation_authorized=True,
            execution_authorized=True,
        )
        _require(
            isinstance(result, dict),
            "pair06 coherent proto child result must be object",
        )
        return result
    finally:
        base_wiring.Pair06V8CombatPriorityProtoChildHooks = (
            ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS
        )


def pair06_v8_combat_priority_coherent_proto_child_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_review_main_head": REPAIR_REVIEW_MAIN_HEAD,
        "repair_review_git_blob": REPAIR_REVIEW_GIT_BLOB,
        "repair_review_test_git_blob": REPAIR_REVIEW_TEST_GIT_BLOB,
        "base_proto_child_wiring_git_blob": BASE_PROTO_CHILD_WIRING_GIT_BLOB,
        "base_proto_child_wiring_review_git_blob": (
            BASE_PROTO_CHILD_WIRING_REVIEW_GIT_BLOB
        ),
        "pair06_v8_combat_priority_coherent_proto_child_wiring_implemented": True,
        "historical_proto_child_wiring_source_modified": False,
        "historical_proto_child_source_modified": False,
        "repaired_decision_hook_bound": True,
        "production_functions_filtered_to_offered_surface": True,
        "historical_hook_class_substitution_scoped_to_single_call": True,
        "historical_hook_class_restored_in_finally": True,
        "existing_child_execution_authorization_gate_preserved": True,
        "existing_policy_activation_authorization_gate_preserved": True,
        "existing_ipc_decider_reused": True,
        "existing_legacy_runner_reused": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "attempt_retry_authorized": False,
        "parent_supervisor_repair_wiring_implemented": False,
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


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentProtoChildWiringHold(NEXT_GATE)
