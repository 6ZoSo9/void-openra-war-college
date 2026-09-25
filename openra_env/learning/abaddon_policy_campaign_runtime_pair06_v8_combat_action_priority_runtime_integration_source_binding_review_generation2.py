"""Source-only review of the pair-06 V8 combat-priority runtime integration.

Pins the exact non-activated decision-hook integration merged by #290.
This review confirms that integration exists only at the decision-hook layer and
is not yet wired into the proto game child or parent supervisor.

No runtime activation, game execution, replay, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action is authorized.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-runtime-integration-review-contract.v1"
)

INTEGRATION_MAIN_HEAD = "c70de88f564062fee6d5eb1d6cd575afffa2957b"
INTEGRATION_GIT_BLOB = "5f33527e1b6b7c1bf8912436d70ab406748c66bd"
INTEGRATION_SOURCE_SHA256 = (
    "558be4263016a6e2e74df49ae0d0dbed27ef508389a83a428b09bf5d3387b36d"
)
INTEGRATION_TEST_GIT_BLOB = (
    "5302aad6f50bcc2237e0b452f0d0a35ec189210d"
)
INTEGRATION_TEST_SHA256 = (
    "d7b3ded580bb598ecba5d708db8781b7b87d1a90bf82649e6fe0a5e332e598d7"
)

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_combat_action_priority_proto_child_wiring"


class Pair06V8CombatActionPriorityRuntimeIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionPriorityRuntimeIntegrationReviewHold(message)


@lru_cache(maxsize=1)
def _validated_integration() -> dict[str, Any]:
    out = (
        integration
        .pair06_v8_combat_action_priority_runtime_integration_contract()
    )

    _require(
        out.get("decision_hook_runtime_integration_implemented") is True,
        "pair06 combat-priority integration missing",
    )
    _require(
        out.get("priority_policy_applied_after_tool_build_before_decider")
        is True,
        "pair06 priority application point drift",
    )
    _require(
        out.get("filtered_tools_and_contract_sent_to_decider") is True
        and out.get("accepted_action_validated_against_filtered_surface")
        is True,
        "pair06 filtered decision surface drift",
    )
    _require(
        out.get("unchanged_legacy_host_validator_used") is True
        and out.get("legacy_five_value_return_shape_preserved") is True,
        "pair06 host boundary/return-shape drift",
    )
    _require(
        out.get("max_attempts") == 6
        and out.get("host_rejection_feedback_forwarded") is True
        and out.get("world_mutation_before_host_validation") is False
        and out.get("frozen_compact_state_reused_across_rejected_attempts")
        is True,
        "pair06 fail-closed decision semantics drift",
    )

    for field in (
        "proto_game_child_wiring_implemented",
        "parent_supervisor_wiring_implemented",
        "operator_invocation_implemented",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(
            out.get(field) is False,
            "pair06 integration boundary drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_RUNTIME_INTEGRATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "pair06 integration review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_action_priority_runtime_integration_review_contract() -> dict[str, Any]:
    validated = _validated_integration()
    return {
        "schema": CONTRACT_SCHEMA,
        "integration_main_head": INTEGRATION_MAIN_HEAD,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_source_sha256": INTEGRATION_SOURCE_SHA256,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "integration_test_sha256": INTEGRATION_TEST_SHA256,
        "pair06_v8_combat_action_priority_runtime_integration_reviewed": True,
        "decision_hook_runtime_integration_implemented": True,
        "proto_game_child_wiring_implemented": False,
        "parent_supervisor_wiring_implemented": False,
        "operator_invocation_implemented": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_integration": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionPriorityRuntimeIntegrationReviewHold(NEXT_GATE)
