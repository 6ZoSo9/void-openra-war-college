"""Source-only parent-supervisor wiring for Pair-06 V9 input-order coherence.

The reviewed inference-safe no-offload V8 parent remains byte-for-byte
unchanged. This module delegates through the exact reviewed parent execution
code with a call-scoped copied globals namespace whose child-command builder
launches the separately reviewed input-order-coherent V9 child entrypoint.

No process-global parent child-command function is replaced. Existing model
loading/inference, CUDA:0 placement checks, socketpair creation, process-group
supervision, authority checks, durable attempt-claim prerequisite, receipt
construction, child retirement, and model-reference release remain owned by the
historical no-offload parent.

The wrapper requires explicit game execution authorization, historical V9 policy
activation authorization, and separate input-order-coherence activation
authorization. It creates no attempt claim, execution request, or attempt.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any, Callable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_source_binding_review_generation2
    as child_wiring_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "parent-supervisor-wiring-contract.v1"
)

ORDER_CHILD_WIRING_REVIEW_GIT_BLOB = (
    "7e96e32361b64f71ccf5c2cfd3c10a33c15429a1"
)
NO_OFFLOAD_PARENT_GIT_BLOB = "231758aeced0a57949dc39165df0f994e8473ebc"
NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB = (
    "6a65984b81e563def012c6da1405ad47747bb465"
)

PAIR_SLOT = 6
ARM = "baseline"

ORDER_CHILD_MODULE = (
    "openra_env.learning."
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "proto_game_child_entrypoint_generation2"
)

ORIGINAL_PARENT_RUN = parent.execute_pair06_v8_parent_supervisor_no_offload
ORIGINAL_CHILD_COMMAND = parent._child_command

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "parent_supervisor_wiring_review"
)


class Pair06V9InputOrderCoherenceParentWiringHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceParentWiringHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    child = (
        child_wiring_review
        .pair06_v9_input_order_coherence_proto_child_wiring_review_contract()
    )
    reviewed_parent = (
        parent_review
        .pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    )
    entry = child_entry.pair06_v9_input_order_coherence_child_entrypoint_contract()

    _require(
        child.get(
            "pair06_v9_input_order_coherence_proto_child_wiring_reviewed"
        )
        is True,
        "V9 input-order proto-child wiring not reviewed",
    )
    _require(
        child.get("order_coherent_decision_hook_reviewed") is True
        and child.get("membership_drift_still_fail_closed") is True,
        "V9 input-order child decision boundary drift",
    )
    _require(
        child.get("consumed_v9_attempt_retry_authorized") is False
        and child.get("new_execution_request_opened") is False
        and child.get("attempt_created") is False
        and child.get("runtime_execution_authorized") is False,
        "V9 input-order child unexpectedly grants execution lineage",
    )
    _require(
        child.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "V9 input-order parent-supervisor frontier drift",
    )

    _require(
        reviewed_parent.get(
            "pair06_v8_parent_launcher_supervisor_no_offload_reviewed"
        )
        is True,
        "reviewed no-offload parent missing",
    )
    _require(
        reviewed_parent.get("pair_slot") == PAIR_SLOT
        and reviewed_parent.get("arm") == ARM,
        "no-offload parent scope drift",
    )
    _require(
        reviewed_parent.get("inference_safe_no_offload_loader_reviewed") is True
        and reviewed_parent.get("cpu_disk_meta_parameter_offload_forbidden") is True
        and reviewed_parent.get(
            "all_parameters_cuda0_required_before_child_spawn"
        )
        is True,
        "no-offload parent placement invariant drift",
    )
    _require(
        reviewed_parent.get("automatic_retry") is False
        and reviewed_parent.get("execution_authorized") is False,
        "no-offload parent unexpectedly grants execution authority",
    )

    _require(
        entry.get(
            "pair06_v9_input_order_coherence_child_entrypoint_implemented"
        )
        is True,
        "V9 input-order child entrypoint missing",
    )
    _require(
        entry.get("existing_execution_confirmation_token_required") is True
        and entry.get("historical_v9_policy_activation_token_required") is True
        and entry.get("separate_order_coherence_activation_token_required")
        is True
        and entry.get("all_confirmation_tokens_distinct") is True,
        "V9 input-order child token boundary drift",
    )
    _require(
        entry.get("attempt_claim_created_by_entrypoint") is False
        and entry.get("execution_request_created_by_entrypoint") is False
        and entry.get("automatic_retry") is False,
        "V9 input-order child entrypoint unexpectedly creates execution lineage",
    )

    return {
        "input_order_child_wiring_review": deepcopy(child),
        "no_offload_parent_review": deepcopy(reviewed_parent),
        "input_order_child_entrypoint": deepcopy(entry),
    }


def _order_child_command(
    *,
    child_fd: int,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
) -> list[str]:
    return [
        str(parent.PROTO_PYTHON),
        "-B",
        "-m",
        ORDER_CHILD_MODULE,
        "--fd",
        str(child_fd),
        "--attempt-id",
        attempt_id,
        "--runs-root",
        runs_root,
        "--frozen-source-root",
        frozen_source_root,
        "--exact-engine-root",
        exact_engine_root,
        "--confirm",
        child_entry.CONFIRM_TOKEN,
        "--policy-confirm",
        child_entry.POLICY_CONFIRM_TOKEN,
        "--order-confirm",
        child_entry.ORDER_CONFIRM_TOKEN,
    ]


def _scoped_parent_run():
    _dependencies()
    _require(
        parent.execute_pair06_v8_parent_supervisor_no_offload
        is ORIGINAL_PARENT_RUN,
        "no-offload parent run function drift before scoped binding",
    )
    _require(
        parent._child_command is ORIGINAL_CHILD_COMMAND,
        "no-offload parent child-command factory drift before scoped binding",
    )

    scoped_globals = dict(ORIGINAL_PARENT_RUN.__globals__)
    scoped_globals["_child_command"] = _order_child_command
    scoped_run = FunctionType(
        ORIGINAL_PARENT_RUN.__code__,
        scoped_globals,
        ORIGINAL_PARENT_RUN.__name__,
        ORIGINAL_PARENT_RUN.__defaults__,
        ORIGINAL_PARENT_RUN.__closure__,
    )
    scoped_run.__kwdefaults__ = ORIGINAL_PARENT_RUN.__kwdefaults__
    return scoped_run


def execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload(
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
    """Delegate one no-offload parent call with call-scoped child-command binding."""
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
        "PAIR06_V8_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )

    scoped_run = _scoped_parent_run()
    try:
        result = scoped_run(
            attempt_id=attempt_id,
            attempt_claimed=attempt_claimed,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
            execution_authorized=True,
            authority_check=authority_check,
        )
        _require(
            isinstance(result, dict),
            "pair06 no-offload parent receipt must be object",
        )
        return result
    finally:
        _require(
            parent._child_command is ORIGINAL_CHILD_COMMAND,
            "process-global no-offload parent child-command factory mutated",
        )
        _require(
            parent.execute_pair06_v8_parent_supervisor_no_offload
            is ORIGINAL_PARENT_RUN,
            "process-global no-offload parent run function mutated",
        )


def pair06_v9_input_order_coherence_parent_wiring_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "order_child_wiring_review_git_blob": ORDER_CHILD_WIRING_REVIEW_GIT_BLOB,
        "no_offload_parent_git_blob": NO_OFFLOAD_PARENT_GIT_BLOB,
        "no_offload_parent_review_git_blob": NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "input_order_child_entrypoint_implemented": True,
        "existing_no_offload_parent_source_modified": False,
        "historical_no_offload_parent_run_code_reused": True,
        "call_scoped_child_command_binding_implemented": True,
        "process_global_child_command_builder_mutated": False,
        "process_global_parent_run_function_mutated": False,
        "new_concurrency_scope_leak_introduced": False,
        "existing_execution_confirmation_token_preserved": True,
        "historical_v9_policy_activation_token_preserved": True,
        "separate_order_coherence_activation_token_added": True,
        "all_confirmation_tokens_distinct": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "existing_no_offload_model_loader_reused": True,
        "existing_cuda0_placement_checks_reused": True,
        "existing_parent_decision_service_loop_reused": True,
        "existing_child_retirement_reused": True,
        "existing_parent_receipt_returned_unchanged": True,
        "existing_parent_automatic_retry": False,
        "durable_attempt_claim_required_by_existing_parent": True,
        "consumed_v9_attempt_retry_authorized": False,
        "attempt_claim_created_by_this_wiring": False,
        "execution_request_created_by_this_wiring": False,
        "attempt_created_by_this_wiring": False,
        "operator_entrypoint_wiring_implemented": False,
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
    raise Pair06V9InputOrderCoherenceParentWiringHold(NEXT_GATE)
