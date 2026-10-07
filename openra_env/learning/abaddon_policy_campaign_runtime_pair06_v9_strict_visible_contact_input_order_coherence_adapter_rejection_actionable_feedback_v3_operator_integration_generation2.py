"""Source-only operator integration for Pair-06 V9 actionable-feedback V3.

This successor reuses the already-reviewed actionable-feedback V2 operator
integration and upgrades only its call-scoped parent delegate to the reviewed
V3 structured-correction parent integration.

The historical operator code object remains unchanged. Preclaim CUDA:0
ordering, one-attempt cardinality, durable claim ordering, V9 strict-contact,
input-order coherence, adapter-rejection fail-closed behavior, and zero
automatic retries remain inherited from the reviewed V2 operator integration.

This layer does not accept V3 activation authorization and does not create an
execution request. A later fresh V3 operator must add a distinct V3 activation
authorization gate and fresh evidence namespace before any execution request.

Import, contract inspection, dependency inspection, and operator building
perform no host I/O, model load, inference, child spawn, game execution,
attempt claim, retry, replay, training, deployment, chain, wallet/funds, or
scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType, SimpleNamespace
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_operator_integration_generation2
    as v2_operator,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_operator_integration_source_binding_review_generation2
    as v2_operator_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_generation2
    as v3_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_source_binding_review_generation2
    as v3_parent_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "operator-integration.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-"
    "actionable-feedback-v3-structured-correction"
)

V2_OPERATOR_INTEGRATION_GIT_BLOB = (
    "8a8b1114682940462934dfbfcf25e0dbd3a784a3"
)
V2_OPERATOR_REVIEW_GIT_BLOB = (
    "03d8f1fcfb50a97f2d4970da2b75ae051cef98d6"
)
V3_PARENT_INTEGRATION_GIT_BLOB = (
    "71a065ff3a38d5c298bbf16559b942af22d564ff"
)
V3_PARENT_REVIEW_GIT_BLOB = (
    "b82c6465656e0b06509034b90af8b79c659ae92b"
)

ORIGINAL_V2_OPERATOR_BUILD = (
    v2_operator.build_pair06_v9_actionable_feedback_v2_operator
)
ORIGINAL_V2_OPERATOR_DEPENDENCIES = v2_operator._scoped_dependency_contracts
ORIGINAL_V3_PARENT_BUILD = (
    v3_parent.build_pair06_v9_actionable_feedback_v3_parent_run
)

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_OPERATOR_INTEGRATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v3_operator_integration_review"
)


class Pair06V9ActionableFeedbackV3OperatorIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3OperatorIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    operator = (
        v2_operator_review
        .pair06_v9_actionable_feedback_v2_operator_integration_review_contract()
    )
    parent = (
        v3_parent_review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
    )

    _require(
        operator.get(
            "pair06_v9_actionable_feedback_v2_operator_integration_reviewed"
        )
        is True,
        "reviewed V2 operator integration missing",
    )
    for field in (
        "reviewed_v1_operator_integration_reused",
        "historical_operator_code_object_reused",
        "call_scoped_dependency_binding_upgraded_to_v2",
        "call_scoped_parent_binding_upgraded_to_v2",
        "historical_preclaim_gpu_ordering_preserved",
        "historical_one_attempt_cardinality_preserved",
    ):
        _require(
            operator.get(field) is True,
            "reviewed V2 operator invariant drift: " + field,
        )
    _require(
        operator.get("consumed_input_order_namespace_reusable") is False
        and operator.get("consumed_input_order_attempt_retry_authorized") is False
        and operator.get("new_execution_request_opened") is False
        and operator.get("runtime_execution_authorized") is False
        and operator.get("automatic_retry") is False,
        "reviewed V2 operator authority drift",
    )

    _require(
        parent.get("pair06_v9_actionable_feedback_v3_runtime_integration_reviewed")
        is True,
        "reviewed V3 parent integration missing",
    )
    for field in (
        "reviewed_v2_parent_integration_reused",
        "historical_parent_run_code_reused",
        "call_scoped_child_command_binding_preserved",
        "call_scoped_decision_response_binding_upgraded_to_v3",
        "exact_v2_feedback_trigger_only",
        "nonmatching_feedback_delegates_to_v2_unchanged",
        "structured_feedback_injected_into_user_prompt",
        "corrective_retry_transfer_prompt_preserved",
        "v2_adapter_rejection_fail_closed_shim_reused",
    ):
        _require(
            parent.get(field) is True,
            "reviewed V3 parent invariant drift: " + field,
        )
    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
        "runtime_execution_authorized",
        "automatic_retry",
    ):
        _require(
            parent.get(field) is False,
            "reviewed V3 parent boundary drift: " + field,
        )

    return {
        "v2_operator_integration_review": deepcopy(operator),
        "v3_parent_integration_review": deepcopy(parent),
    }


def _scoped_dependency_contracts() -> dict[str, Any]:
    """Revalidate inherited V2 operator dependencies plus the V3 parent."""
    _dependencies()
    historical = ORIGINAL_V2_OPERATOR_DEPENDENCIES()
    return {
        **deepcopy(historical),
        "actionable_feedback_v3_parent_integration_review": deepcopy(
            _dependencies()["v3_parent_integration_review"]
        ),
    }


def _execute_v3_parent(
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

    scoped_parent = ORIGINAL_V3_PARENT_BUILD()
    return scoped_parent(
        attempt_id=attempt_id,
        attempt_claimed=attempt_claimed,
        runs_root=runs_root,
        frozen_source_root=frozen_source_root,
        exact_engine_root=exact_engine_root,
        execution_authorized=True,
        authority_check=authority_check,
    )


def build_pair06_v9_actionable_feedback_v3_operator() -> Any:
    """Build but never execute the reviewed V2 operator with a V3 parent binding."""
    _dependencies()

    _require(
        v2_operator.build_pair06_v9_actionable_feedback_v2_operator
        is ORIGINAL_V2_OPERATOR_BUILD,
        "reviewed V2 operator builder drift before V3 scoped build",
    )
    _require(
        v2_operator._scoped_dependency_contracts
        is ORIGINAL_V2_OPERATOR_DEPENDENCIES,
        "reviewed V2 operator dependency binding drift before V3 scoped build",
    )
    _require(
        v3_parent.build_pair06_v9_actionable_feedback_v3_parent_run
        is ORIGINAL_V3_PARENT_BUILD,
        "reviewed V3 parent builder drift before V3 operator build",
    )

    v2_scoped = ORIGINAL_V2_OPERATOR_BUILD()
    _require(
        isinstance(v2_scoped, FunctionType),
        "reviewed V2 operator builder did not return FunctionType",
    )
    _require(
        v2_scoped.__globals__.get("_dependency_contracts")
        is ORIGINAL_V2_OPERATOR_DEPENDENCIES,
        "reviewed V2 operator dependency binding drift",
    )

    scoped_globals = dict(v2_scoped.__globals__)
    scoped_globals["_dependency_contracts"] = _scoped_dependency_contracts
    scoped_globals["order_parent"] = SimpleNamespace(
        execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload=(
            _execute_v3_parent
        )
    )

    scoped_execute = FunctionType(
        v2_scoped.__code__,
        scoped_globals,
        v2_scoped.__name__,
        v2_scoped.__defaults__,
        v2_scoped.__closure__,
    )
    scoped_execute.__kwdefaults__ = v2_scoped.__kwdefaults__

    _require(
        v2_operator.build_pair06_v9_actionable_feedback_v2_operator
        is ORIGINAL_V2_OPERATOR_BUILD,
        "reviewed V2 operator builder mutated during V3 scoped build",
    )
    _require(
        v2_operator._scoped_dependency_contracts
        is ORIGINAL_V2_OPERATOR_DEPENDENCIES,
        "reviewed V2 operator dependencies mutated during V3 scoped build",
    )
    _require(
        v3_parent.build_pair06_v9_actionable_feedback_v3_parent_run
        is ORIGINAL_V3_PARENT_BUILD,
        "reviewed V3 parent builder mutated during V3 scoped build",
    )
    return scoped_execute


def pair06_v9_actionable_feedback_v3_operator_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "v2_operator_integration_git_blob": V2_OPERATOR_INTEGRATION_GIT_BLOB,
        "v2_operator_review_git_blob": V2_OPERATOR_REVIEW_GIT_BLOB,
        "v3_parent_integration_git_blob": V3_PARENT_INTEGRATION_GIT_BLOB,
        "v3_parent_review_git_blob": V3_PARENT_REVIEW_GIT_BLOB,
        "actionable_feedback_v3_operator_integration_implemented": True,
        "reviewed_v2_operator_integration_reused": True,
        "historical_operator_code_object_reused": True,
        "call_scoped_dependency_binding_upgraded_to_v3": True,
        "call_scoped_parent_binding_upgraded_to_v3": True,
        "reviewed_actionable_feedback_v3_parent_used": True,
        "historical_preclaim_gpu_ordering_preserved": True,
        "historical_one_attempt_cardinality_preserved": True,
        "historical_automatic_retry_remains_false": True,
        "historical_execution_policy_order_authorizations_preserved": True,
        "structured_feedback_injected_into_user_prompt": True,
        "corrective_retry_transfer_prompt_preserved": True,
        "v2_adapter_rejection_fail_closed_shim_reused": True,
        "frozen_v8_tool_schema_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "six_attempt_bound_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "v2_operator_integration_source_modified": False,
        "v3_parent_integration_source_modified": False,
        "process_global_operator_execute_mutated": False,
        "process_global_operator_dependencies_mutated": False,
        "process_global_operator_parent_binding_mutated": False,
        "builder_executes_operator": False,
        "builder_performs_host_io": False,
        "builder_loads_model": False,
        "builder_runs_inference": False,
        "builder_spawns_child": False,
        "builder_executes_game": False,
        "consumed_v2_namespace_reusable": False,
        "consumed_v2_attempt_retry_authorized": False,
        "fresh_attempt_namespace_required_before_execution_request": True,
        "fresh_actionable_feedback_v3_activation_authorization_required": True,
        "fresh_operator_source_required_before_execution_request": True,
        "new_execution_request_opened": False,
        "actionable_feedback_v3_activation_authorization_accepted": False,
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
    raise Pair06V9ActionableFeedbackV3OperatorIntegrationHold(NEXT_GATE)
