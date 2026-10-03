"""Source-only Pair-06 V9 adapter-feedback proto-child wiring.

This layer composes the merged adapter-feedback decision overlay with the
already-reviewed input-order proto-child path without modifying either
historical source file.

It reuses the exact historical input-order child run and V8 child-builder code
through call-scoped FunctionType globals. Only the proto-child hook binding is
advanced to the adapter-feedback decision hook.

Import and contract inspection perform no model, game, child-process, service,
network, chain, wallet, funds, training, deployment, or scheduler action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_feedback_overlay_generation2
    as feedback_overlay,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_generation2
    as historical_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_source_binding_review_generation2
    as historical_wiring_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-feedback-proto-child-wiring-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"

FEEDBACK_OVERLAY_GIT_BLOB = "f720d70d2f7068eeeb05324d3a89aaf6b86daa84"
HISTORICAL_WIRING_GIT_BLOB = "1b87cb5596c219e6118f4b69845dbecaa29a3ace"
HISTORICAL_WIRING_REVIEW_GIT_BLOB = (
    "7e96e32361b64f71ccf5c2cfd3c10a33c15429a1"
)

ORIGINAL_SCOPED_V8_CHILD_RUN = historical_wiring._scoped_v8_child_run
ORIGINAL_INPUT_ORDER_CHILD_RUN = (
    historical_wiring.run_pair06_v9_input_order_coherence_proto_game_child
)
ORIGINAL_INPUT_ORDER_HOOKS = (
    historical_wiring.Pair06V9InputOrderCoherentProtoChildHooks
)

NEXT_GATE = (
    "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
    "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_adapter_rejection_feedback_"
    "proto_child_wiring_review"
)


class Pair06V9AdapterFeedbackProtoChildWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterFeedbackProtoChildWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    historical = (
        historical_wiring_review
        .pair06_v9_input_order_coherence_proto_child_wiring_review_contract()
    )
    feedback = (
        feedback_overlay
        .pair06_v9_adapter_rejection_feedback_overlay_contract()
    )

    _require(
        historical.get(
            "pair06_v9_input_order_coherence_proto_child_wiring_reviewed"
        )
        is True,
        "historical input-order proto-child wiring not reviewed",
    )
    _require(
        historical.get("order_coherent_decision_hook_reviewed") is True
        and historical.get("call_scoped_child_hook_factory_binding_reviewed")
        is True,
        "historical input-order child binding drift",
    )
    _require(
        historical.get("consumed_v9_attempt_retry_authorized") is False
        and historical.get("runtime_execution_authorized") is False,
        "historical input-order child authority drift",
    )

    _require(
        feedback.get("adapter_rejection_feedback_overlay_implemented") is True,
        "adapter-feedback overlay missing",
    )
    _require(
        feedback.get("exact_sentinel_only") is True
        and feedback.get("sentinel_accepted") is False
        and feedback.get("sentinel_host_validation_performed") is False
        and feedback.get("sentinel_world_mutation_performed") is False
        and feedback.get("sentinel_retry_feedback") == "unit_ids invalid",
        "adapter-feedback overlay invariant drift",
    )
    _require(
        feedback.get("execution_authorized") is False
        and feedback.get("consumed_attempt_retry_authorized") is False
        and feedback.get("automatic_retry") is False,
        "adapter-feedback overlay authority drift",
    )

    return {
        "historical_input_order_wiring_review": deepcopy(historical),
        "feedback_overlay": deepcopy(feedback),
    }


class Pair06V9AdapterFeedbackProtoChildHooks(ORIGINAL_INPUT_ORDER_HOOKS):
    """Historical input-order child hooks with only the decision hook advanced."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        super().__init__(legacy, sock, attempt_id)

        prior = self._decision_hooks
        _require(
            getattr(prior, "_installed", False) is False,
            "historical decision hooks unexpectedly installed at construction",
        )

        self._decision_hooks = (
            feedback_overlay.Pair06V9AdapterRejectionFeedbackDecisionHooks(
                legacy,
                self._ipc_decider,
            )
        )
        self.v9_adapter_feedback_decision_hook_bound = True


def _scoped_feedback_v8_child_run():
    """Reuse the reviewed V8-child builder with one local hook substitution."""
    _dependencies()
    _require(
        historical_wiring._scoped_v8_child_run
        is ORIGINAL_SCOPED_V8_CHILD_RUN,
        "historical scoped V8 child builder drift",
    )
    _require(
        historical_wiring.Pair06V9InputOrderCoherentProtoChildHooks
        is ORIGINAL_INPUT_ORDER_HOOKS,
        "historical input-order child hook factory drift",
    )

    scoped_globals = dict(ORIGINAL_SCOPED_V8_CHILD_RUN.__globals__)
    scoped_globals["Pair06V9InputOrderCoherentProtoChildHooks"] = (
        Pair06V9AdapterFeedbackProtoChildHooks
    )
    scoped_builder = FunctionType(
        ORIGINAL_SCOPED_V8_CHILD_RUN.__code__,
        scoped_globals,
        ORIGINAL_SCOPED_V8_CHILD_RUN.__name__,
        ORIGINAL_SCOPED_V8_CHILD_RUN.__defaults__,
        ORIGINAL_SCOPED_V8_CHILD_RUN.__closure__,
    )
    scoped_builder.__kwdefaults__ = ORIGINAL_SCOPED_V8_CHILD_RUN.__kwdefaults__
    result = scoped_builder()

    _require(
        historical_wiring._scoped_v8_child_run
        is ORIGINAL_SCOPED_V8_CHILD_RUN,
        "historical scoped V8 child builder mutated",
    )
    _require(
        historical_wiring.Pair06V9InputOrderCoherentProtoChildHooks
        is ORIGINAL_INPUT_ORDER_HOOKS,
        "historical input-order child hook factory mutated",
    )
    return result


def _scoped_input_order_child_run():
    """Reuse exact historical input-order child-run code call-scopingly."""
    _dependencies()
    _require(
        historical_wiring.run_pair06_v9_input_order_coherence_proto_game_child
        is ORIGINAL_INPUT_ORDER_CHILD_RUN,
        "historical input-order child run drift",
    )

    scoped_globals = dict(ORIGINAL_INPUT_ORDER_CHILD_RUN.__globals__)
    scoped_globals["_scoped_v8_child_run"] = _scoped_feedback_v8_child_run
    scoped_run = FunctionType(
        ORIGINAL_INPUT_ORDER_CHILD_RUN.__code__,
        scoped_globals,
        ORIGINAL_INPUT_ORDER_CHILD_RUN.__name__,
        ORIGINAL_INPUT_ORDER_CHILD_RUN.__defaults__,
        ORIGINAL_INPUT_ORDER_CHILD_RUN.__closure__,
    )
    scoped_run.__kwdefaults__ = ORIGINAL_INPUT_ORDER_CHILD_RUN.__kwdefaults__

    _require(
        historical_wiring.run_pair06_v9_input_order_coherence_proto_game_child
        is ORIGINAL_INPUT_ORDER_CHILD_RUN,
        "historical input-order child run mutated during scoped build",
    )
    return scoped_run


def run_pair06_v9_adapter_feedback_proto_game_child(
    *,
    sock: Any,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    policy_activation_authorized: bool,
    order_coherence_activation_authorized: bool,
    execution_authorized: bool,
) -> dict[str, Any]:
    """Delegate through historical gates with the new call-scoped hook."""
    _dependencies()
    scoped_run = _scoped_input_order_child_run()
    try:
        result = scoped_run(
            sock=sock,
            attempt_id=attempt_id,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
            policy_activation_authorized=policy_activation_authorized,
            order_coherence_activation_authorized=(
                order_coherence_activation_authorized
            ),
            execution_authorized=execution_authorized,
        )
        _require(
            isinstance(result, dict),
            "adapter-feedback proto-child result must be object",
        )
        return result
    finally:
        _require(
            historical_wiring._scoped_v8_child_run
            is ORIGINAL_SCOPED_V8_CHILD_RUN,
            "historical scoped V8 child builder mutated",
        )
        _require(
            historical_wiring.run_pair06_v9_input_order_coherence_proto_game_child
            is ORIGINAL_INPUT_ORDER_CHILD_RUN,
            "historical input-order child run mutated",
        )
        _require(
            historical_wiring.Pair06V9InputOrderCoherentProtoChildHooks
            is ORIGINAL_INPUT_ORDER_HOOKS,
            "historical input-order hook factory mutated",
        )


def pair06_v9_adapter_feedback_proto_child_wiring_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "feedback_overlay_git_blob": FEEDBACK_OVERLAY_GIT_BLOB,
        "historical_wiring_git_blob": HISTORICAL_WIRING_GIT_BLOB,
        "historical_wiring_review_git_blob": HISTORICAL_WIRING_REVIEW_GIT_BLOB,
        "adapter_feedback_proto_child_wiring_implemented": True,
        "historical_input_order_proto_child_source_modified": False,
        "historical_input_order_proto_child_review_modified": False,
        "feedback_overlay_source_modified": False,
        "historical_input_order_child_hook_subclass_reused": True,
        "feedback_decision_hook_bound": True,
        "exact_sentinel_retry_feedback_preserved": True,
        "sentinel_retry_feedback": "unit_ids invalid",
        "historical_scoped_v8_child_builder_code_reused": True,
        "historical_input_order_child_run_code_reused": True,
        "call_scoped_feedback_hook_binding_implemented": True,
        "process_global_child_hook_factory_mutated": False,
        "process_global_child_run_function_mutated": False,
        "new_concurrency_scope_leak_introduced": False,
        "original_child_execution_authorization_gate_preserved": True,
        "historical_v9_policy_activation_gate_preserved": True,
        "input_order_coherence_activation_gate_preserved": True,
        "consumed_v9_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "attempt_created": False,
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
        "scheduler_mutation_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterFeedbackProtoChildWiringHold(NEXT_GATE)
