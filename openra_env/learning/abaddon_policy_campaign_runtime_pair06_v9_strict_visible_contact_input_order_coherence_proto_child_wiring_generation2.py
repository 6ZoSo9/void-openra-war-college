"""Source-only proto-child wiring for the V9 input-order coherence repair.

This layer advances only the reviewed pair-06 V9 child decision hook. The
reviewed V8 proto-game child source and reviewed V9 strict-contact child wiring
remain unchanged.

Unlike the historical V9 child wrapper, this layer does not replace the
process-global proto-child hook factory. It executes the exact reviewed V8 child
run code with a call-scoped copied globals namespace whose hook-factory binding
points to a V9 child-hook subclass using the reviewed input-order-coherent
decision hook.

The existing child execution gate and V9 policy-activation gate remain required,
and a separate input-order-coherence activation gate is added. This source opens
no execution request, creates no attempt, and grants no runtime activation,
execution, replay, training, promotion, deployment, chain, wallet/funds, or
scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as proto_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_generation2
    as order_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_source_binding_review_generation2
    as order_integration_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_generation2
    as historical_v9_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_source_binding_review_generation2
    as historical_v9_child_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "proto-child-wiring-contract.v1"
)

ORDER_INTEGRATION_GIT_BLOB = "166e4e84fd657adcdd752e53c8c6fd8ea555006b"
ORDER_INTEGRATION_REVIEW_GIT_BLOB = "f17cadd048f4437d66792ae76dd1a096b475eba7"
HISTORICAL_V9_CHILD_GIT_BLOB = "5fc4c66b0c0f23edb8c4932bba1c743fd63b9b12"
HISTORICAL_V9_CHILD_REVIEW_GIT_BLOB = (
    "747dd644fdff569745854f5a3d35758e150e5d2f"
)
V8_PROTO_CHILD_GIT_BLOB = "7ea5d27c2d2bb499dfec4c00d2812d7ed043f8bc"

PAIR_SLOT = 6
ARM = "baseline"

ORIGINAL_V8_CHILD_RUN = proto_child.run_pair06_v8_proto_game_child
ORIGINAL_V8_CHILD_HOOKS = proto_child.Pair06V8ProtoChildHooks
HISTORICAL_V9_CHILD_HOOKS = (
    historical_v9_child.Pair06V9StrictVisibleContactProtoChildHooks
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "proto_child_wiring_review"
)


class Pair06V9InputOrderCoherenceProtoChildWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceProtoChildWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    integration = (
        order_integration_review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )
    historical = (
        historical_v9_child_review
        .pair06_v9_strict_visible_contact_proto_child_wiring_review_contract()
    )

    _require(
        integration.get(
            "pair06_v9_input_order_coherence_runtime_integration_reviewed"
        )
        is True,
        "V9 input-order runtime integration not reviewed",
    )
    _require(
        integration.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 input-order runtime policy id drift",
    )
    for field in (
        "historical_adapted_decision_code_reused_reviewed",
        "call_scoped_policy_binding_reviewed",
        "concurrency_scope_leak_closed_reviewed",
        "typed_tool_membership_exact_match_required",
        "typed_tool_order_canonicalized_to_offered_order",
        "membership_drift_still_fail_closed",
    ):
        _require(
            integration.get(field) is True,
            "V9 input-order runtime review invariant drift: " + field,
        )
    _require(
        integration.get("process_global_policy_function_mutated") is False
        and integration.get("consumed_v9_attempt_retry_authorized") is False
        and integration.get("new_execution_request_opened") is False,
        "V9 input-order runtime authority/global-state drift",
    )
    _require(
        integration.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "PROTO_CHILD_WIRING_REQUIRED"
        ),
        "V9 input-order proto-child frontier drift",
    )

    _require(
        historical.get(
            "pair06_v9_strict_visible_contact_proto_child_wiring_reviewed"
        )
        is True,
        "historical V9 proto-child wiring not reviewed",
    )
    _require(
        historical.get("original_child_execution_authorization_gate_preserved")
        is True
        and historical.get("additional_v9_policy_activation_gate_required")
        is True
        and historical.get("coherent_v9_tool_contract_path_preserved") is True,
        "historical V9 proto-child authorization/coherence drift",
    )
    _require(
        historical.get("new_execution_request_opened") is False
        and historical.get("attempt_created") is False
        and historical.get("runtime_execution_authorized") is False,
        "historical V9 proto-child unexpectedly grants execution lineage",
    )

    return {
        "input_order_runtime_integration_review": deepcopy(integration),
        "historical_v9_proto_child_review": deepcopy(historical),
    }


class Pair06V9InputOrderCoherentProtoChildHooks(HISTORICAL_V9_CHILD_HOOKS):
    """Historical V9 child hooks with only the decision hook advanced."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        super().__init__(legacy, sock, attempt_id)

        historical_decision_hooks = self._decision_hooks
        _require(
            getattr(historical_decision_hooks, "_installed", False) is False,
            "historical V9 decision hooks unexpectedly installed at construction",
        )

        self._decision_hooks = (
            order_integration.Pair06V9InputOrderCoherentDecisionHooks(
                legacy,
                self._ipc_decider,
            )
        )
        self.v9_strict_visible_contact_decision_hook_bound = True
        self.input_order_coherence_decision_hook_bound = True


def _scoped_v8_child_run():
    _dependencies()
    _require(
        proto_child.run_pair06_v8_proto_game_child is ORIGINAL_V8_CHILD_RUN,
        "V8 proto-child run function drift before scoped binding",
    )
    _require(
        proto_child.Pair06V8ProtoChildHooks is ORIGINAL_V8_CHILD_HOOKS,
        "V8 proto-child hook factory drift before scoped binding",
    )

    scoped_globals = dict(ORIGINAL_V8_CHILD_RUN.__globals__)
    scoped_globals["Pair06V8ProtoChildHooks"] = (
        Pair06V9InputOrderCoherentProtoChildHooks
    )
    scoped_run = FunctionType(
        ORIGINAL_V8_CHILD_RUN.__code__,
        scoped_globals,
        ORIGINAL_V8_CHILD_RUN.__name__,
        ORIGINAL_V8_CHILD_RUN.__defaults__,
        ORIGINAL_V8_CHILD_RUN.__closure__,
    )
    scoped_run.__kwdefaults__ = ORIGINAL_V8_CHILD_RUN.__kwdefaults__
    return scoped_run


def run_pair06_v9_input_order_coherence_proto_game_child(
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
    """Delegate one child call without mutating the process-global hook factory."""
    _dependencies()

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
        "PAIR06_V8_CHILD_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )

    scoped_run = _scoped_v8_child_run()
    try:
        result = scoped_run(
            sock=sock,
            attempt_id=attempt_id,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
            execution_authorized=True,
        )
        _require(
            isinstance(result, dict),
            "pair06 V9 input-order proto-child result must be object",
        )
        return result
    finally:
        _require(
            proto_child.Pair06V8ProtoChildHooks is ORIGINAL_V8_CHILD_HOOKS,
            "process-global V8 proto-child hook factory mutated",
        )
        _require(
            proto_child.run_pair06_v8_proto_game_child is ORIGINAL_V8_CHILD_RUN,
            "process-global V8 proto-child run function mutated",
        )


def pair06_v9_input_order_coherence_proto_child_wiring_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "order_integration_git_blob": ORDER_INTEGRATION_GIT_BLOB,
        "order_integration_review_git_blob": ORDER_INTEGRATION_REVIEW_GIT_BLOB,
        "historical_v9_child_git_blob": HISTORICAL_V9_CHILD_GIT_BLOB,
        "historical_v9_child_review_git_blob": (
            HISTORICAL_V9_CHILD_REVIEW_GIT_BLOB
        ),
        "v8_proto_child_git_blob": V8_PROTO_CHILD_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "input_order_coherence_proto_child_wiring_implemented": True,
        "historical_v9_proto_child_source_modified": False,
        "existing_v8_proto_child_source_modified": False,
        "historical_v9_proto_child_hook_subclass_reused": True,
        "order_coherent_decision_hook_bound": True,
        "historical_v8_child_run_code_reused": True,
        "call_scoped_child_hook_factory_binding_implemented": True,
        "process_global_child_hook_factory_mutated": False,
        "process_global_child_run_function_mutated": False,
        "new_concurrency_scope_leak_introduced": False,
        "original_child_execution_authorization_gate_preserved": True,
        "historical_v9_policy_activation_gate_preserved": True,
        "additional_order_coherence_activation_gate_required": True,
        "reviewed_order_coherent_decision_hook_used": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "existing_ipc_decider_reused": True,
        "existing_legacy_runner_reused": True,
        "existing_portable_worktree_binding_reused": True,
        "consumed_v9_attempt_retry_authorized": False,
        "parent_supervisor_repair_wiring_implemented": False,
        "operator_repair_wiring_implemented": False,
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
    raise Pair06V9InputOrderCoherenceProtoChildWiringHold(NEXT_GATE)
