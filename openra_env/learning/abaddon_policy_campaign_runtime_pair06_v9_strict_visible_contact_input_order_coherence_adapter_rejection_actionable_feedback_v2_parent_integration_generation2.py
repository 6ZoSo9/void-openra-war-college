"""Source-only V2 parent integration for Pair-06 V9 adapter-rejection feedback.

This layer composes two already-reviewed source gates:
* the reviewed V1 adapter-rejection parent integration; and
* the reviewed actionable adapter-rejection feedback V2 shim.

The V1 parent integration already reuses the exact historical no-offload parent
code object with call-scoped child-command and decision-response bindings. This
successor preserves that reviewed child-command binding and changes only the
copied globals namespace's `_decision_response` binding from reviewed V1 to
reviewed actionable V2.

Building or inspecting this integration performs no host I/O, model load,
inference, child spawn, game execution, attempt claim, retry, replay, training,
deployment, chain, wallet/funds, or scheduler action and grants none of those
authorities. The consumed input-order attempt remains non-retryable.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_generation2
    as v1_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_source_binding_review_generation2
    as v1_parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_generation2
    as v2_feedback,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_source_binding_review_generation2
    as v2_feedback_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-actionable-feedback-v2-parent-integration-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2"
)

V1_PARENT_INTEGRATION_GIT_BLOB = "381f30278f58ebfd66348807f56251bd16a9ce92"
V1_PARENT_REVIEW_GIT_BLOB = "81c65183dea163a9cec9bade063d3045045522e0"
V2_FEEDBACK_GIT_BLOB = "02ada3893596a2596ad8f980d7e1a0b5fe8faf92"
V2_FEEDBACK_REVIEW_GIT_BLOB = "e1931048b9e8e589b0749d68e11376569da33612"

ORIGINAL_V1_PARENT_BUILD = (
    v1_parent.build_pair06_v9_input_order_adapter_rejection_parent_run
)
ORIGINAL_V1_DECISION_RESPONSE = (
    v1_parent.adapter_response.decision_response_with_observed_adapter_rejection
)
ORIGINAL_V2_DECISION_RESPONSE = (
    v2_feedback.decision_response_with_actionable_adapter_rejection_feedback
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_PARENT_INTEGRATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_parent_integration_review"
)


class Pair06V9ActionableFeedbackV2ParentIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2ParentIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    parent = (
        v1_parent_review
        .pair06_v9_input_order_adapter_rejection_parent_integration_review_contract()
    )
    feedback = (
        v2_feedback_review
        .pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract()
    )

    _require(
        parent.get(
            "pair06_v9_input_order_adapter_rejection_parent_integration_reviewed"
        )
        is True,
        "reviewed V1 adapter-rejection parent integration missing",
    )
    _require(
        parent.get("historical_parent_run_code_reused") is True
        and parent.get("call_scoped_child_command_binding_reused") is True
        and parent.get("call_scoped_decision_response_binding_implemented")
        is True,
        "reviewed V1 parent integration invariant drift",
    )
    _require(
        parent.get("malformed_unit_ids_coerced") is False
        and parent.get("malformed_unit_ids_accepted") is False
        and parent.get("consumed_input_order_attempt_retry_authorized")
        is False
        and parent.get("new_execution_request_opened") is False
        and parent.get("runtime_execution_authorized") is False
        and parent.get("automatic_retry") is False,
        "reviewed V1 parent integration authority drift",
    )

    _require(
        feedback.get(
            "pair06_v9_adapter_rejection_actionable_feedback_v2_reviewed"
        )
        is True,
        "reviewed actionable feedback V2 missing",
    )
    _require(
        feedback.get("feedback_requires_quoted_unit_ids_string") is True
        and feedback.get("feedback_rejects_json_array_unit_ids") is True
        and feedback.get("feedback_rejects_bare_integer_unit_ids") is True,
        "actionable feedback V2 wire-format boundary drift",
    )
    _require(
        feedback.get("malformed_unit_ids_coerced") is False
        and feedback.get("malformed_unit_ids_accepted") is False
        and feedback.get("consumed_attempt_retry_authorized") is False
        and feedback.get("new_execution_request_opened") is False
        and feedback.get("runtime_execution_authorized") is False
        and feedback.get("automatic_retry") is False,
        "actionable feedback V2 authority drift",
    )

    return {
        "v1_parent_integration_review": deepcopy(parent),
        "actionable_feedback_v2_review": deepcopy(feedback),
    }


def build_pair06_v9_actionable_feedback_v2_parent_run() -> Any:
    """Build, but never execute, the reviewed parent with only V2 feedback changed."""
    _dependencies()

    _require(
        v1_parent.build_pair06_v9_input_order_adapter_rejection_parent_run
        is ORIGINAL_V1_PARENT_BUILD,
        "reviewed V1 parent builder drift before V2 scoped build",
    )
    _require(
        v2_feedback.decision_response_with_actionable_adapter_rejection_feedback
        is ORIGINAL_V2_DECISION_RESPONSE,
        "reviewed V2 decision-response function drift before scoped build",
    )

    v1_scoped = ORIGINAL_V1_PARENT_BUILD()
    _require(
        isinstance(v1_scoped, FunctionType),
        "reviewed V1 parent builder did not return FunctionType",
    )
    _require(
        v1_scoped.__globals__.get("_decision_response")
        is ORIGINAL_V1_DECISION_RESPONSE,
        "reviewed V1 parent decision-response binding drift",
    )

    child_command = v1_scoped.__globals__.get("_child_command")
    scoped_globals = dict(v1_scoped.__globals__)
    scoped_globals["_decision_response"] = ORIGINAL_V2_DECISION_RESPONSE

    scoped_run = FunctionType(
        v1_scoped.__code__,
        scoped_globals,
        v1_scoped.__name__,
        v1_scoped.__defaults__,
        v1_scoped.__closure__,
    )
    scoped_run.__kwdefaults__ = v1_scoped.__kwdefaults__

    _require(
        scoped_run.__globals__.get("_child_command") is child_command,
        "reviewed V1 child-command binding drift during V2 scoped build",
    )
    _require(
        v1_parent.build_pair06_v9_input_order_adapter_rejection_parent_run
        is ORIGINAL_V1_PARENT_BUILD,
        "reviewed V1 parent builder mutated during V2 scoped build",
    )
    _require(
        v1_parent.adapter_response.decision_response_with_observed_adapter_rejection
        is ORIGINAL_V1_DECISION_RESPONSE,
        "reviewed V1 decision-response function mutated during V2 scoped build",
    )
    return scoped_run


def pair06_v9_actionable_feedback_v2_parent_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "v1_parent_integration_git_blob": V1_PARENT_INTEGRATION_GIT_BLOB,
        "v1_parent_review_git_blob": V1_PARENT_REVIEW_GIT_BLOB,
        "v2_feedback_git_blob": V2_FEEDBACK_GIT_BLOB,
        "v2_feedback_review_git_blob": V2_FEEDBACK_REVIEW_GIT_BLOB,
        "actionable_feedback_v2_parent_integration_implemented": True,
        "reviewed_v1_parent_integration_reused": True,
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_reused": True,
        "call_scoped_decision_response_binding_upgraded_to_v2": True,
        "reviewed_actionable_feedback_v2_used": True,
        "v1_parent_integration_source_modified": False,
        "v1_feedback_source_modified": False,
        "v2_feedback_source_modified": False,
        "process_global_parent_run_function_mutated": False,
        "process_global_child_command_builder_mutated": False,
        "process_global_decision_response_mutated": False,
        "builder_executes_parent": False,
        "builder_performs_host_io": False,
        "builder_loads_model": False,
        "builder_runs_inference": False,
        "builder_spawns_child": False,
        "builder_executes_game": False,
        "feedback_requires_quoted_unit_ids_string": True,
        "feedback_rejects_json_array_unit_ids": True,
        "feedback_rejects_bare_integer_unit_ids": True,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
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
    raise Pair06V9ActionableFeedbackV2ParentIntegrationHold(NEXT_GATE)
