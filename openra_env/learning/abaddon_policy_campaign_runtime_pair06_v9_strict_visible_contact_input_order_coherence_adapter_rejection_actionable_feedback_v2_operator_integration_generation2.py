"""Source-only V2 operator integration for Pair-06 V9 adapter feedback.

This successor composes the already-reviewed V1 adapter-rejection operator
integration with the already-reviewed actionable-feedback V2 parent
integration. The historical operator code object is reused unchanged.

A call-scoped FunctionType is built from the reviewed V1 operator integration.
Only the copied globals namespace's dependency snapshot and `order_parent`
binding are replaced so the operator delegates through the reviewed V2 parent.

The consumed input-order namespace remains closed. This integration opens no
execution request and accepts no activation authorization. A fresh attempt
namespace, fresh actionable-feedback V2 activation authorization boundary, and
fresh operator source remain required before any future execution request.

Import, contract inspection, dependency inspection, and operator building
perform no host I/O, model load, inference, child spawn, game execution,
attempt claim, replay, retry, training, deployment, chain, wallet/funds, or
scheduler action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType, SimpleNamespace
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_operator_integration_generation2
    as v1_operator,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_operator_integration_source_binding_review_generation2
    as v1_operator_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_parent_integration_generation2
    as v2_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_parent_integration_source_binding_review_generation2
    as v2_parent_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-actionable-feedback-v2-operator-integration-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2"
)

V1_OPERATOR_INTEGRATION_GIT_BLOB = "fcf5cb87ef75f288dbcb5e83f236ea217db1db2d"
V1_OPERATOR_REVIEW_GIT_BLOB = "74590dce39f0c5bcab590db6df6e3f78475f74be"
V2_PARENT_INTEGRATION_GIT_BLOB = "22eb8708b600d15e6f3aa0e02e5697a7cf01a820"
V2_PARENT_REVIEW_GIT_BLOB = "c3a39dbb0a22d9350894a8f78b824af0b4e07a01"

ORIGINAL_V1_OPERATOR_BUILD = (
    v1_operator.build_pair06_v9_input_order_adapter_rejection_operator
)
ORIGINAL_V1_OPERATOR_DEPENDENCIES = v1_operator._scoped_dependency_contracts
ORIGINAL_V2_PARENT_BUILD = v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_OPERATOR_INTEGRATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_operator_integration_review"
)


class Pair06V9ActionableFeedbackV2OperatorIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2OperatorIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    operator = (
        v1_operator_review
        .pair06_v9_input_order_adapter_rejection_operator_integration_review_contract()
    )
    parent = (
        v2_parent_review
        .pair06_v9_actionable_feedback_v2_parent_integration_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_input_order_adapter_rejection_operator_integration_reviewed"
        )
        is True,
        "reviewed V1 adapter-rejection operator integration missing",
    )
    _require(
        operator.get("historical_operator_code_object_reused") is True
        and operator.get("call_scoped_dependency_binding_reviewed") is True
        and operator.get("call_scoped_parent_binding_reviewed") is True,
        "reviewed V1 operator integration invariant drift",
    )
    _require(
        operator.get("historical_preclaim_gpu_ordering_preserved") is True
        and operator.get("historical_one_attempt_cardinality_preserved") is True
        and operator.get("consumed_input_order_namespace_reusable") is False
        and operator.get("consumed_input_order_attempt_retry_authorized") is False
        and operator.get("new_execution_request_opened") is False
        and operator.get("runtime_execution_authorized") is False
        and operator.get("automatic_retry") is False,
        "reviewed V1 operator integration authority drift",
    )

    _require(
        parent.get("pair06_v9_actionable_feedback_v2_parent_integration_reviewed")
        is True,
        "reviewed actionable-feedback V2 parent integration missing",
    )
    _require(
        parent.get("historical_parent_run_code_reused") is True
        and parent.get("call_scoped_child_command_binding_reused") is True
        and parent.get("call_scoped_decision_response_binding_upgraded_to_v2")
        is True
        and parent.get("reviewed_actionable_feedback_v2_used") is True,
        "reviewed actionable-feedback V2 parent invariant drift",
    )
    _require(
        parent.get("malformed_unit_ids_coerced") is False
        and parent.get("malformed_unit_ids_accepted") is False
        and parent.get("consumed_input_order_attempt_retry_authorized") is False
        and parent.get("new_execution_request_opened") is False
        and parent.get("runtime_execution_authorized") is False
        and parent.get("automatic_retry") is False,
        "reviewed actionable-feedback V2 parent authority drift",
    )

    return {
        "v1_operator_integration_review": deepcopy(operator),
        "actionable_feedback_v2_parent_integration_review": deepcopy(parent),
    }


def _scoped_dependency_contracts() -> dict[str, Any]:
    """Revalidate V1 operator dependencies plus the reviewed V2 parent."""
    _dependencies()
    historical = ORIGINAL_V1_OPERATOR_DEPENDENCIES()
    return {
        **deepcopy(historical),
        "actionable_feedback_v2_parent_integration_review": deepcopy(
            _dependencies()["actionable_feedback_v2_parent_integration_review"]
        ),
    }


def _execute_v2_parent(
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
    """Future-only adapter matching the historical operator parent call shape."""
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

    scoped_parent = ORIGINAL_V2_PARENT_BUILD()
    return scoped_parent(
        attempt_id=attempt_id,
        attempt_claimed=attempt_claimed,
        runs_root=runs_root,
        frozen_source_root=frozen_source_root,
        exact_engine_root=exact_engine_root,
        execution_authorized=True,
        authority_check=authority_check,
    )


def build_pair06_v9_actionable_feedback_v2_operator() -> Any:
    """Build but never execute the reviewed V1 operator with a V2 parent binding."""
    _dependencies()

    _require(
        v1_operator.build_pair06_v9_input_order_adapter_rejection_operator
        is ORIGINAL_V1_OPERATOR_BUILD,
        "reviewed V1 operator builder drift before V2 scoped build",
    )
    _require(
        v1_operator._scoped_dependency_contracts
        is ORIGINAL_V1_OPERATOR_DEPENDENCIES,
        "reviewed V1 operator dependency binding drift before V2 scoped build",
    )
    _require(
        v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
        is ORIGINAL_V2_PARENT_BUILD,
        "reviewed V2 parent builder drift before V2 operator build",
    )

    v1_scoped = ORIGINAL_V1_OPERATOR_BUILD()
    _require(
        isinstance(v1_scoped, FunctionType),
        "reviewed V1 operator builder did not return FunctionType",
    )
    _require(
        v1_scoped.__globals__.get("_dependency_contracts")
        is ORIGINAL_V1_OPERATOR_DEPENDENCIES,
        "reviewed V1 operator dependency binding drift",
    )

    scoped_globals = dict(v1_scoped.__globals__)
    scoped_globals["_dependency_contracts"] = _scoped_dependency_contracts
    scoped_globals["order_parent"] = SimpleNamespace(
        execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload=(
            _execute_v2_parent
        )
    )

    scoped_execute = FunctionType(
        v1_scoped.__code__,
        scoped_globals,
        v1_scoped.__name__,
        v1_scoped.__defaults__,
        v1_scoped.__closure__,
    )
    scoped_execute.__kwdefaults__ = v1_scoped.__kwdefaults__

    _require(
        v1_operator.build_pair06_v9_input_order_adapter_rejection_operator
        is ORIGINAL_V1_OPERATOR_BUILD,
        "reviewed V1 operator builder mutated during V2 scoped build",
    )
    _require(
        v1_operator._scoped_dependency_contracts
        is ORIGINAL_V1_OPERATOR_DEPENDENCIES,
        "reviewed V1 operator dependencies mutated during V2 scoped build",
    )
    _require(
        v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
        is ORIGINAL_V2_PARENT_BUILD,
        "reviewed V2 parent builder mutated during V2 scoped build",
    )
    return scoped_execute


def pair06_v9_actionable_feedback_v2_operator_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "v1_operator_integration_git_blob": V1_OPERATOR_INTEGRATION_GIT_BLOB,
        "v1_operator_review_git_blob": V1_OPERATOR_REVIEW_GIT_BLOB,
        "v2_parent_integration_git_blob": V2_PARENT_INTEGRATION_GIT_BLOB,
        "v2_parent_review_git_blob": V2_PARENT_REVIEW_GIT_BLOB,
        "actionable_feedback_v2_operator_integration_implemented": True,
        "reviewed_v1_operator_integration_reused": True,
        "historical_operator_code_object_reused": True,
        "call_scoped_dependency_binding_upgraded_to_v2": True,
        "call_scoped_parent_binding_upgraded_to_v2": True,
        "reviewed_actionable_feedback_v2_parent_used": True,
        "v1_operator_integration_source_modified": False,
        "v2_parent_integration_source_modified": False,
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
        "feedback_requires_quoted_unit_ids_string": True,
        "feedback_rejects_json_array_unit_ids": True,
        "feedback_rejects_bare_integer_unit_ids": True,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "consumed_input_order_namespace_reusable": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "fresh_attempt_namespace_required_before_execution_request": True,
        "fresh_actionable_feedback_v2_activation_authorization_required": True,
        "fresh_operator_source_required_before_execution_request": True,
        "new_execution_request_opened": False,
        "actionable_feedback_v2_activation_authorization_accepted": False,
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
    raise Pair06V9ActionableFeedbackV2OperatorIntegrationHold(NEXT_GATE)
