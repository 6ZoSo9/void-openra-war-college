"""Source-only proto-child wiring for combat-priority coherence repair V2.

The reviewed V1 coherent proto-child wiring remains unchanged. This module
subclasses that exact hook container and replaces only its uninstalled V1
decision hook with the reviewed V2 legality-coherent hook.

For one delegated child call, the V1 coherent hook class is temporarily
substituted with the V2 subclass and restored in finally. Existing child
execution and combat-priority policy-activation gates remain intact.

The most recent consumed failed attempt remains non-reusable. This source
grants no retry, runtime activation, execution, replay, training, deployment,
chain mutation, or wallet/funds authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_generation2
    as repair_v2,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_source_binding_review_generation2
    as repair_v2_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_generation2
    as v1_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_source_binding_review_generation2
    as v1_wiring_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "proto-child-wiring-contract.v1"
)

REPAIR_V2_REVIEW_MAIN_HEAD = "ea0222f82189c7b55435742d78bb17169630e8f7"
REPAIR_V2_REVIEW_GIT_BLOB = "5e10ca44e614e37ff4f786e3ddff45ae7e0166d7"
REPAIR_V2_REVIEW_SOURCE_SHA256 = (
    "d338be5a16fe809abcf412e06552f94fcb04cecb4ed99d337ae8c40e71f33e3c"
)
REPAIR_V2_REVIEW_TEST_GIT_BLOB = (
    "e482b5d81f8ece9ba30604ef39e09c5db74333b6"
)
REPAIR_V2_REVIEW_TEST_SHA256 = (
    "8f1db10374a4112123115683761c24941e21fb89b0e6293a231e7a66ab398714"
)

V1_COHERENT_PROTO_CHILD_WIRING_GIT_BLOB = (
    "75d4442b2b86a54343dc546b59f58f90e3e9afc4"
)
V1_COHERENT_PROTO_CHILD_WIRING_SOURCE_SHA256 = (
    "e904bd345b07ec25c061da710a625e9aafc51424dba5708408b46c07afed3306"
)
V1_COHERENT_PROTO_CHILD_WIRING_REVIEW_GIT_BLOB = (
    "b8aa17ee161f2b2377ef6d80f1408d04268a2f22"
)

CONSUMED_V2_PRECURSOR_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
CONSUMED_V2_PRECURSOR_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS = (
    v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_v2_proto_child_wiring_review"
)


class Pair06V8CombatPriorityCoherentV2ProtoChildWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2ProtoChildWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    repaired_v2 = (
        repair_v2_review
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract()
    )
    v1_child = (
        v1_wiring_review
        .pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    )

    _require(
        repaired_v2.get(
            "pair06_v8_combat_action_priority_contract_coherence_repair_v2_reviewed"
        )
        is True,
        "V2 contract-coherence repair not reviewed",
    )
    for field in (
        "production_functions_filtered_to_offered_surface_by_v1",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_invariant_required",
        "translator_legal_unit_mapping_invariant_required",
        "normal_mode_identity_required",
    ):
        _require(
            repaired_v2.get(field) is True,
            "V2 contract-coherence invariant drift: " + field,
        )
    _require(
        repaired_v2.get("consumed_v2_precursor_attempt_marker_sha256")
        == CONSUMED_V2_PRECURSOR_ATTEMPT_MARKER_SHA256
        and repaired_v2.get("consumed_v2_precursor_attempt_reusable") is False,
        "V2 precursor consumed-attempt lineage drift",
    )
    _require(
        repaired_v2.get("consumed_v2_precursor_run_id")
        == CONSUMED_V2_PRECURSOR_RUN_ID
        and repaired_v2.get(
            "consumed_v2_precursor_run_reusable_as_authority"
        )
        is False
        and repaired_v2.get("prior_authorization_reusable") is False,
        "V2 precursor run/authorization lineage drift",
    )
    _require(
        repaired_v2.get("attempt_retry_authorized") is False
        and repaired_v2.get("runtime_execution_authorized") is False,
        "V2 repair unexpectedly grants runtime authority",
    )
    _require(
        repaired_v2.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "PROTO_CHILD_WIRING_REQUIRED"
        ),
        "V2 repair proto-child frontier drift",
    )

    _require(
        v1_child.get(
            "pair06_v8_combat_priority_coherent_proto_child_wiring_reviewed"
        )
        is True,
        "V1 coherent proto-child wiring not reviewed",
    )
    _require(
        v1_child.get("repaired_decision_hook_bound") is True
        and v1_child.get("production_functions_filtered_to_offered_surface")
        is True,
        "V1 coherent proto-child invariant drift",
    )
    _require(
        v1_child.get("existing_child_execution_authorization_gate_preserved")
        is True
        and v1_child.get(
            "existing_policy_activation_authorization_gate_preserved"
        )
        is True,
        "V1 coherent proto-child authorization gate drift",
    )
    _require(
        v1_child.get("runtime_execution_authorized") is False
        and v1_child.get("automatic_retry") is False,
        "V1 coherent proto-child unexpectedly grants authority",
    )

    return {
        "repair_v2_review": deepcopy(repaired_v2),
        "v1_coherent_proto_child_wiring_review": deepcopy(v1_child),
    }


class Pair06V8CombatPriorityCoherentV2ProtoChildHooks(
    ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS
):
    """V1 coherent child hooks with only the decision hook advanced to V2."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        super().__init__(legacy, sock, attempt_id)

        v1_decision_hooks = self._decision_hooks
        _require(
            getattr(v1_decision_hooks, "_installed", False) is False,
            "V1 coherent decision hooks unexpectedly installed",
        )

        self._decision_hooks = (
            repair_v2.Pair06V8CombatPriorityContractCoherentV2DecisionHooks(
                legacy,
                self._ipc_decider,
            )
        )
        self.combat_priority_contract_coherence_repair_v2_bound = True


def run_pair06_v8_combat_priority_coherent_v2_proto_game_child(
    *,
    sock: Any,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    execution_authorized: bool,
) -> dict[str, Any]:
    """Delegate one V1-coherent child call with scoped V2 hook substitution."""
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
        v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
        is ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS,
        "V1 coherent proto-child hook class drift before substitution",
    )

    v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks = (
        Pair06V8CombatPriorityCoherentV2ProtoChildHooks
    )
    try:
        result = (
            v1_wiring
            .run_pair06_v8_combat_priority_coherent_proto_game_child(
                sock=sock,
                attempt_id=attempt_id,
                runs_root=runs_root,
                frozen_source_root=frozen_source_root,
                exact_engine_root=exact_engine_root,
                policy_activation_authorized=True,
                execution_authorized=True,
            )
        )
        _require(
            isinstance(result, dict),
            "pair06 coherent V2 proto child result must be object",
        )
        return result
    finally:
        v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks = (
            ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS
        )


def pair06_v8_combat_priority_coherent_v2_proto_child_wiring_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_v2_review_main_head": REPAIR_V2_REVIEW_MAIN_HEAD,
        "repair_v2_review_git_blob": REPAIR_V2_REVIEW_GIT_BLOB,
        "repair_v2_review_source_sha256": REPAIR_V2_REVIEW_SOURCE_SHA256,
        "repair_v2_review_test_git_blob": REPAIR_V2_REVIEW_TEST_GIT_BLOB,
        "repair_v2_review_test_sha256": REPAIR_V2_REVIEW_TEST_SHA256,
        "v1_coherent_proto_child_wiring_git_blob": (
            V1_COHERENT_PROTO_CHILD_WIRING_GIT_BLOB
        ),
        "v1_coherent_proto_child_wiring_source_sha256": (
            V1_COHERENT_PROTO_CHILD_WIRING_SOURCE_SHA256
        ),
        "v1_coherent_proto_child_wiring_review_git_blob": (
            V1_COHERENT_PROTO_CHILD_WIRING_REVIEW_GIT_BLOB
        ),
        "pair06_v8_combat_priority_coherent_v2_proto_child_wiring_implemented": True,
        "v1_coherent_proto_child_wiring_source_modified": False,
        "historical_proto_child_wiring_source_modified": False,
        "historical_proto_child_source_modified": False,
        "v2_repaired_decision_hook_bound": True,
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_coherent": True,
        "translator_legal_unit_mapping_coherent": True,
        "v1_hook_class_substitution_scoped_to_single_call": True,
        "v1_hook_class_restored_in_finally": True,
        "existing_child_execution_authorization_gate_preserved": True,
        "existing_policy_activation_authorization_gate_preserved": True,
        "existing_ipc_decider_reused": True,
        "existing_legacy_runner_reused": True,
        "consumed_v2_precursor_attempt_marker_sha256": (
            CONSUMED_V2_PRECURSOR_ATTEMPT_MARKER_SHA256
        ),
        "consumed_v2_precursor_attempt_reusable": False,
        "consumed_v2_precursor_run_id": CONSUMED_V2_PRECURSOR_RUN_ID,
        "consumed_v2_precursor_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "attempt_retry_authorized": False,
        "parent_supervisor_v2_wiring_implemented": False,
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


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2ProtoChildWiringHold(NEXT_GATE)
