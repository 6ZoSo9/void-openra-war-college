"""Source-only review of coherent pair-06 combat-priority proto-child wiring.

Pins the exact merged wiring source/tests from #304 and validates that the
reviewed contract-coherence repair is bound only at the proto-child decision
hook seam. The consumed failed attempt remains sealed and non-reusable.

This review grants no retry, runtime activation, execution, replay, training,
promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_generation2
    as wiring,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "proto-child-wiring-review-contract.v1"
)

WIRING_MAIN_HEAD = "721bb382cc07abbd26111bfdc605504d5961886c"
WIRING_GIT_BLOB = "75d4442b2b86a54343dc546b59f58f90e3e9afc4"
WIRING_SOURCE_SHA256 = (
    "e904bd345b07ec25c061da710a625e9aafc51424dba5708408b46c07afed3306"
)
WIRING_TEST_GIT_BLOB = "e41123b2f46091359a3099766d152ce4418666b5"
WIRING_TEST_SHA256 = (
    "d2559b04b0b854dd24477bb96a1dbc2ef4743b22d20d70d66c9a9d38a136e86f"
)

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_parent_supervisor_wiring"
)


class Pair06V8CombatPriorityCoherentProtoChildWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentProtoChildWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = wiring.pair06_v8_combat_priority_coherent_proto_child_wiring_contract()

    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_proto_child_wiring_implemented"
        )
        is True,
        "coherent proto-child wiring missing",
    )
    _require(
        out.get("historical_proto_child_wiring_source_modified") is False
        and out.get("historical_proto_child_source_modified") is False,
        "historical child source unexpectedly modified",
    )

    for field in (
        "repaired_decision_hook_bound",
        "production_functions_filtered_to_offered_surface",
        "historical_hook_class_substitution_scoped_to_single_call",
        "historical_hook_class_restored_in_finally",
        "existing_child_execution_authorization_gate_preserved",
        "existing_policy_activation_authorization_gate_preserved",
        "existing_ipc_decider_reused",
        "existing_legacy_runner_reused",
    ):
        _require(out.get(field) is True, "coherent child invariant drift: " + field)

    _require(
        out.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_attempt_reusable") is False,
        "consumed attempt lineage drift",
    )
    _require(
        out.get("failed_run_id") == FAILED_RUN_ID
        and out.get("failed_run_reusable_as_authority") is False,
        "failed run lineage drift",
    )

    for field in (
        "attempt_retry_authorized",
        "parent_supervisor_repair_wiring_implemented",
        "operator_invocation_repair_implemented",
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
        _require(out.get(field) is False, "coherent child authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "coherent child review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "wiring_main_head": WIRING_MAIN_HEAD,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_source_sha256": WIRING_SOURCE_SHA256,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "wiring_test_sha256": WIRING_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_proto_child_wiring_reviewed": True,
        "repaired_decision_hook_bound": True,
        "production_functions_filtered_to_offered_surface": True,
        "existing_child_execution_authorization_gate_preserved": True,
        "existing_policy_activation_authorization_gate_preserved": True,
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
    raise Pair06V8CombatPriorityCoherentProtoChildWiringReviewHold(NEXT_GATE)
