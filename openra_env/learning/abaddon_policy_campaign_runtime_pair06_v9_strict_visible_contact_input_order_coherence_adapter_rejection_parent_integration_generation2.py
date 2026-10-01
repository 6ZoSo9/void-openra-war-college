"""Source-only parent integration for Pair-06 V9 adapter-rejection handling.

This module composes two already-separated source gates without executing them:
* the reviewed input-order child command factory; and
* the reviewed exact-error adapter-rejection response shim.

The historical no-offload parent remains byte-for-byte unchanged. A builder
returns a new FunctionType using the exact historical parent code object and a
copied globals namespace where only `_child_command` and
`_decision_response` are replaced. Process-global parent functions are never
mutated.

Building or inspecting this integration performs no host I/O, model load,
inference, child spawn, game execution, attempt claim, replay, training,
deployment, chain, wallet/funds, or scheduler action and grants none of those
authorities. The consumed input-order attempt remains non-retryable.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_generation2
    as order_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_source_binding_review_generation2
    as order_parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_generation2
    as adapter_response,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_source_binding_review_generation2
    as adapter_response_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-parent-integration-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = "pair06-v9-input-order-coherence-adapter-rejection-retry-v1"

NO_OFFLOAD_PARENT_GIT_BLOB = "231758aeced0a57949dc39165df0f994e8473ebc"
ORDER_PARENT_GIT_BLOB = "607cf5ff20f46769609208a261132434ef966785"

ORIGINAL_PARENT_RUN = parent.execute_pair06_v8_parent_supervisor_no_offload
ORIGINAL_CHILD_COMMAND = parent._child_command
ORIGINAL_DECISION_RESPONSE = parent._decision_response

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_PARENT_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_parent_integration_review"
)


class Pair06V9InputOrderAdapterRejectionParentIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionParentIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    historical = (
        parent_review
        .pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    )
    order = (
        order_parent_review
        .pair06_v9_input_order_coherence_parent_wiring_review_contract()
    )
    adapter = (
        adapter_response_review
        .pair06_v9_input_order_adapter_rejection_response_review_contract()
    )

    _require(
        historical.get(
            "pair06_v8_parent_launcher_supervisor_no_offload_reviewed"
        )
        is True,
        "historical no-offload parent review missing",
    )
    _require(
        historical.get("pair_slot") == PAIR_SLOT
        and historical.get("arm") == ARM
        and historical.get("automatic_retry") is False
        and historical.get("execution_authorized") is False,
        "historical no-offload parent boundary drift",
    )

    _require(
        order.get("pair06_v9_input_order_coherence_parent_wiring_reviewed")
        is True
        and order.get("input_order_child_entrypoint_reviewed") is True,
        "input-order parent wiring review missing",
    )
    _require(
        order.get("historical_parent_run_code_reused_reviewed") is True
        and order.get("call_scoped_child_command_binding_reviewed") is True
        and order.get("durable_attempt_claim_prerequisite_preserved") is True
        and order.get("no_offload_cuda0_parent_path_preserved") is True,
        "input-order parent reviewed runtime boundary drift",
    )
    _require(
        order.get("process_global_child_command_builder_mutated") is False
        and order.get("process_global_parent_run_function_mutated") is False
        and order.get("new_concurrency_scope_leak_introduced") is False
        and order.get("consumed_v9_attempt_retry_authorized") is False
        and order.get("execution_request_created") is False
        and order.get("attempt_claim_created") is False
        and order.get("attempt_created") is False
        and order.get("runtime_execution_authorized") is False
        and order.get("automatic_retry") is False,
        "input-order parent reviewed authority boundary drift",
    )

    _require(
        adapter.get(
            "pair06_v9_input_order_adapter_rejection_response_reviewed"
        )
        is True,
        "adapter-rejection response review missing",
    )
    _require(
        adapter.get("observed_retryable_error") == "unit_ids invalid"
        and adapter.get("only_exact_observed_adapter_error_is_retryable")
        is True
        and adapter.get("other_v8_adapter_errors_still_propagate") is True,
        "adapter-rejection response boundary drift",
    )
    _require(
        adapter.get("malformed_unit_ids_coerced") is False
        and adapter.get("malformed_unit_ids_accepted") is False
        and adapter.get("consumed_input_order_attempt_retry_authorized")
        is False
        and adapter.get("runtime_execution_authorized") is False,
        "adapter-rejection response authority drift",
    )

    return {
        "no_offload_parent_review": deepcopy(historical),
        "input_order_parent_review": deepcopy(order),
        "adapter_rejection_response_review": deepcopy(adapter),
    }


def build_pair06_v9_input_order_adapter_rejection_parent_run() -> Any:
    """Build, but do not execute, the exact historical parent with two scoped bindings."""
    _dependencies()

    _require(
        parent.execute_pair06_v8_parent_supervisor_no_offload
        is ORIGINAL_PARENT_RUN,
        "historical parent run function drift before scoped build",
    )
    _require(
        parent._child_command is ORIGINAL_CHILD_COMMAND,
        "historical parent child-command function drift before scoped build",
    )
    _require(
        parent._decision_response is ORIGINAL_DECISION_RESPONSE,
        "historical parent decision-response function drift before scoped build",
    )

    scoped_globals = dict(ORIGINAL_PARENT_RUN.__globals__)
    scoped_globals["_child_command"] = order_parent._order_child_command
    scoped_globals["_decision_response"] = (
        adapter_response.decision_response_with_observed_adapter_rejection
    )

    scoped_run = FunctionType(
        ORIGINAL_PARENT_RUN.__code__,
        scoped_globals,
        ORIGINAL_PARENT_RUN.__name__,
        ORIGINAL_PARENT_RUN.__defaults__,
        ORIGINAL_PARENT_RUN.__closure__,
    )
    scoped_run.__kwdefaults__ = ORIGINAL_PARENT_RUN.__kwdefaults__

    _require(
        parent.execute_pair06_v8_parent_supervisor_no_offload
        is ORIGINAL_PARENT_RUN,
        "process-global historical parent run function mutated during build",
    )
    _require(
        parent._child_command is ORIGINAL_CHILD_COMMAND,
        "process-global historical child-command function mutated during build",
    )
    _require(
        parent._decision_response is ORIGINAL_DECISION_RESPONSE,
        "process-global historical decision-response function mutated during build",
    )
    return scoped_run


def pair06_v9_input_order_adapter_rejection_parent_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "no_offload_parent_git_blob": NO_OFFLOAD_PARENT_GIT_BLOB,
        "order_parent_git_blob": ORDER_PARENT_GIT_BLOB,
        "adapter_rejection_parent_integration_implemented": True,
        "historical_parent_source_modified": False,
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_reused": True,
        "call_scoped_decision_response_binding_implemented": True,
        "input_order_child_command_used": True,
        "reviewed_adapter_rejection_response_used": True,
        "process_global_parent_run_function_mutated": False,
        "process_global_child_command_builder_mutated": False,
        "process_global_decision_response_mutated": False,
        "builder_executes_parent": False,
        "builder_performs_host_io": False,
        "builder_loads_model": False,
        "builder_runs_inference": False,
        "builder_spawns_child": False,
        "builder_executes_game": False,
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
    raise Pair06V9InputOrderAdapterRejectionParentIntegrationHold(NEXT_GATE)
