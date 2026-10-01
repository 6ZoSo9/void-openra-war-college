"""Source-only operator integration for Pair-06 V9 adapter-rejection handling.

This module composes the reviewed input-order operator with the reviewed scoped
adapter-rejection parent integration without executing either path.

The exact historical operator code object is reused through a call-scoped
FunctionType with a copied globals namespace. Only:
* the operator dependency snapshot; and
* the operator's `order_parent` binding
are substituted in that copied namespace.

The substituted parent binding preserves the historical execution/policy/order
authorization booleans before delegating to the reviewed scoped parent builder.

This integration deliberately does NOT make the consumed input-order evidence
namespace reusable. A fresh attempt namespace, fresh repair-activation
authorization boundary, fresh execution request, and new operator source are
required before any future host execution can be requested.

Import, contract inspection, and operator building perform no host I/O, model
load, inference, child spawn, game execution, attempt claim, replay, training,
deployment, chain, wallet/funds, or scheduler action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType, SimpleNamespace
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_operator_entrypoint_generation2
    as historical_operator,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_operator_entrypoint_source_binding_review_generation2
    as historical_operator_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_generation2
    as repaired_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_source_binding_review_generation2
    as repaired_parent_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-operator-integration-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = "pair06-v9-input-order-coherence-adapter-rejection-retry-v1"

HISTORICAL_OPERATOR_GIT_BLOB = "2a1e9d04b0a877ad4afb4f99f831b7824c5fb59a"
HISTORICAL_OPERATOR_REVIEW_GIT_BLOB = "2538f3c191e7a9826df0415583cac1021783a659"
REPAIRED_PARENT_GIT_BLOB = "381f30278f58ebfd66348807f56251bd16a9ce92"
REPAIRED_PARENT_REVIEW_GIT_BLOB = "81c65183dea163a9cec9bade063d3045045522e0"

ORIGINAL_OPERATOR_EXECUTE = (
    historical_operator.execute_pair06_v9_input_order_coherence_baseline_game
)
ORIGINAL_OPERATOR_DEPENDENCIES = historical_operator._dependency_contracts
ORIGINAL_OPERATOR_ORDER_PARENT = historical_operator.order_parent

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_OPERATOR_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_operator_integration_review"
)


class Pair06V9InputOrderAdapterRejectionOperatorIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionOperatorIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    operator = (
        historical_operator_review
        .pair06_v9_input_order_coherence_operator_review_contract()
    )
    parent = (
        repaired_parent_review
        .pair06_v9_input_order_adapter_rejection_parent_integration_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_input_order_coherence_operator_entrypoint_reviewed"
        )
        is True,
        "historical input-order operator review missing",
    )
    _require(
        operator.get("pair_slot") == PAIR_SLOT
        and operator.get("arm") == ARM
        and operator.get("held_out") is False
        and operator.get("policy_id") == POLICY_ID,
        "historical input-order operator scope drift",
    )
    _require(
        operator.get("maximum_attempts") == 1
        and operator.get("maximum_automatic_retries") == 0
        and operator.get("fresh_preclaim_gpu_observation_required") is True
        and operator.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and operator.get("zero_foreign_cuda0_compute_processes_required")
        is True,
        "historical input-order operator attempt/GPU boundary drift",
    )
    _require(
        operator.get("historical_v9_attempt_reusable") is False
        and operator.get("historical_v9_authorization_reusable") is False
        and operator.get("execution_authorization_accepted") is False
        and operator.get("policy_activation_authorization_accepted") is False
        and operator.get("order_coherence_activation_authorization_accepted")
        is False
        and operator.get("runtime_execution_authorized") is False
        and operator.get("execution_request_created") is False,
        "historical input-order operator authority drift",
    )

    _require(
        parent.get(
            "pair06_v9_input_order_adapter_rejection_parent_integration_reviewed"
        )
        is True,
        "adapter-rejection parent integration review missing",
    )
    _require(
        parent.get("policy_id") == POLICY_ID
        and parent.get("historical_parent_run_code_reused") is True
        and parent.get("call_scoped_child_command_binding_reused") is True
        and parent.get("call_scoped_decision_response_binding_implemented")
        is True,
        "adapter-rejection parent integration invariant drift",
    )
    _require(
        parent.get("malformed_unit_ids_coerced") is False
        and parent.get("malformed_unit_ids_accepted") is False
        and parent.get("consumed_input_order_attempt_retry_authorized")
        is False
        and parent.get("new_execution_request_opened") is False
        and parent.get("attempt_created") is False
        and parent.get("runtime_execution_authorized") is False
        and parent.get("automatic_retry") is False,
        "adapter-rejection parent integration authority drift",
    )

    return {
        "historical_operator_review": deepcopy(operator),
        "adapter_rejection_parent_integration_review": deepcopy(parent),
    }


def _scoped_dependency_contracts() -> dict[str, Any]:
    """Revalidate historical operator plus reviewed repaired-parent dependencies."""
    _dependencies()
    historical = ORIGINAL_OPERATOR_DEPENDENCIES()
    return {
        **deepcopy(historical),
        "adapter_rejection_parent_integration_review": deepcopy(
            _dependencies()["adapter_rejection_parent_integration_review"]
        ),
    }


def _execute_repaired_parent(
    *,
    attempt_id: str,
    attempt_claimed: bool,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    order_coherence_activation_authorized: bool,
    execution_authorized: bool,
    authority_check: Callable[[int, str], bool],
) -> dict[str, Any]:
    """Future-only parent adapter matching the historical operator call shape."""
    _require(
        policy_activation_authorized is True,
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        order_coherence_activation_authorized is True,
        "PAIR06_V9_INPUT_ORDER_COHERENCE_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        execution_authorized is True,
        "PAIR06_V8_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )

    scoped_parent = (
        repaired_parent
        .build_pair06_v9_input_order_adapter_rejection_parent_run()
    )
    return scoped_parent(
        attempt_id=attempt_id,
        attempt_claimed=attempt_claimed,
        runs_root=runs_root,
        frozen_source_root=frozen_source_root,
        exact_engine_root=exact_engine_root,
        execution_authorized=True,
        authority_check=authority_check,
    )


def build_pair06_v9_input_order_adapter_rejection_operator() -> Any:
    """Build but never execute the historical operator with scoped repair bindings."""
    _dependencies()

    _require(
        historical_operator.execute_pair06_v9_input_order_coherence_baseline_game
        is ORIGINAL_OPERATOR_EXECUTE,
        "historical operator execute function drift before scoped build",
    )
    _require(
        historical_operator._dependency_contracts
        is ORIGINAL_OPERATOR_DEPENDENCIES,
        "historical operator dependency function drift before scoped build",
    )
    _require(
        historical_operator.order_parent is ORIGINAL_OPERATOR_ORDER_PARENT,
        "historical operator parent module drift before scoped build",
    )

    scoped_globals = dict(ORIGINAL_OPERATOR_EXECUTE.__globals__)
    scoped_globals["_dependency_contracts"] = _scoped_dependency_contracts
    scoped_globals["order_parent"] = SimpleNamespace(
        execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload=(
            _execute_repaired_parent
        )
    )

    scoped_execute = FunctionType(
        ORIGINAL_OPERATOR_EXECUTE.__code__,
        scoped_globals,
        ORIGINAL_OPERATOR_EXECUTE.__name__,
        ORIGINAL_OPERATOR_EXECUTE.__defaults__,
        ORIGINAL_OPERATOR_EXECUTE.__closure__,
    )
    scoped_execute.__kwdefaults__ = ORIGINAL_OPERATOR_EXECUTE.__kwdefaults__

    _require(
        historical_operator.execute_pair06_v9_input_order_coherence_baseline_game
        is ORIGINAL_OPERATOR_EXECUTE,
        "process-global historical operator execute function mutated",
    )
    _require(
        historical_operator._dependency_contracts
        is ORIGINAL_OPERATOR_DEPENDENCIES,
        "process-global historical operator dependency function mutated",
    )
    _require(
        historical_operator.order_parent is ORIGINAL_OPERATOR_ORDER_PARENT,
        "process-global historical operator parent module mutated",
    )
    return scoped_execute


def pair06_v9_input_order_adapter_rejection_operator_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "historical_operator_git_blob": HISTORICAL_OPERATOR_GIT_BLOB,
        "historical_operator_review_git_blob": (
            HISTORICAL_OPERATOR_REVIEW_GIT_BLOB
        ),
        "repaired_parent_git_blob": REPAIRED_PARENT_GIT_BLOB,
        "repaired_parent_review_git_blob": REPAIRED_PARENT_REVIEW_GIT_BLOB,
        "adapter_rejection_operator_integration_implemented": True,
        "historical_operator_source_modified": False,
        "historical_operator_code_object_reused": True,
        "call_scoped_dependency_binding_implemented": True,
        "call_scoped_parent_binding_implemented": True,
        "reviewed_repaired_parent_used": True,
        "process_global_operator_execute_mutated": False,
        "process_global_operator_dependencies_mutated": False,
        "process_global_operator_parent_binding_mutated": False,
        "builder_executes_operator": False,
        "builder_performs_host_io": False,
        "builder_loads_model": False,
        "builder_runs_inference": False,
        "builder_spawns_child": False,
        "builder_executes_game": False,
        "historical_preclaim_gpu_ordering_preserved": True,
        "historical_one_attempt_cardinality_preserved": True,
        "historical_automatic_retry_remains_false": True,
        "historical_execution_policy_order_authorizations_preserved": True,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "consumed_input_order_namespace_reusable": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "fresh_attempt_namespace_required_before_execution_request": True,
        "fresh_repair_activation_authorization_required_before_execution_request": True,
        "fresh_operator_source_required_before_execution_request": True,
        "new_execution_request_opened": False,
        "repair_activation_authorization_accepted": False,
        "attempt_claim_created": False,
        "attempt_created": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
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


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderAdapterRejectionOperatorIntegrationHold(NEXT_GATE)
