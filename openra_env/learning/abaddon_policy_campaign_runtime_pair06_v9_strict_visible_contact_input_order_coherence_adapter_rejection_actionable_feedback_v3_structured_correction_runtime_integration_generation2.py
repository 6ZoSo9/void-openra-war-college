"""Call-scoped runtime integration for Pair-06 V9 actionable-feedback V3.

The V2 parent path remains the execution skeleton and retains its exact
adapter-rejection response shim. This V3 layer changes only the decision
response binding used by that call-scoped parent:

* non-matching feedback delegates unchanged to the reviewed V2 response path;
* the exact reviewed V2 terminal feedback is upgraded to the reviewed V3
  structured correction before inference;
* the corrective retry preserves the reviewed transfer system prompt;
* generated output still passes through the unchanged frozen V8 translator;
* if malformed unit_ids is produced again, the existing V2 adapter-rejection
  shim remains responsible for fail-closed sentinel conversion.

No process-global function is mutated. Building or inspecting this integration
performs no host I/O, model load, inference, child spawn, game execution,
attempt claim, retry, replay, training, deployment, chain, wallet/funds, or
scheduler action and grants none of those authorities.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any, Callable, Mapping

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_parent_integration_generation2
    as v2_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_parent_integration_source_binding_review_generation2
    as v2_parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_generation2
    as v3_correction,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_source_binding_review_generation2
    as v3_correction_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "structured-correction-runtime-integration.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-"
    "actionable-feedback-v3-structured-correction"
)

V2_PARENT_INTEGRATION_GIT_BLOB = "22eb8708b600d15e6f3aa0e02e5697a7cf01a820"
V2_PARENT_REVIEW_GIT_BLOB = "c3a39dbb0a22d9350894a8f78b824af0b4e07a01"
V3_CORRECTION_GIT_BLOB = "9456c729db82284fa9a41e5bc728c254e0768caa"
V3_CORRECTION_REVIEW_GIT_BLOB = "437a0a35223b8b418fb3482407c8dc00d160f8e9"
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

ORIGINAL_V2_PARENT_BUILD = (
    v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
)
ORIGINAL_V2_DECISION_RESPONSE = v2_parent.ORIGINAL_V2_DECISION_RESPONSE

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_"
    "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v3_structured_correction_"
    "runtime_integration_review"
)


class Pair06V9ActionableFeedbackV3RuntimeIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3RuntimeIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    parent = (
        v2_parent_review
        .pair06_v9_actionable_feedback_v2_parent_integration_review_contract()
    )
    correction = (
        v3_correction_review
        .pair06_v9_actionable_feedback_v3_structured_correction_review_contract()
    )

    _require(
        parent.get("pair06_v9_actionable_feedback_v2_parent_integration_reviewed")
        is True,
        "reviewed V2 parent integration missing",
    )
    _require(
        parent.get("historical_parent_run_code_reused") is True
        and parent.get("call_scoped_child_command_binding_reused") is True
        and parent.get("call_scoped_decision_response_binding_upgraded_to_v2")
        is True
        and parent.get("reviewed_actionable_feedback_v2_used") is True,
        "reviewed V2 parent integration invariant drift",
    )
    _require(
        parent.get("process_global_parent_run_function_mutated") is False
        and parent.get("process_global_child_command_builder_mutated") is False
        and parent.get("process_global_decision_response_mutated") is False
        and parent.get("runtime_execution_authorized") is False
        and parent.get("automatic_retry") is False,
        "reviewed V2 parent integration boundary drift",
    )

    _require(
        correction.get(
            "pair06_v9_actionable_feedback_v3_structured_correction_reviewed"
        )
        is True,
        "reviewed V3 structured correction missing",
    )
    _require(
        correction.get("exact_v2_trigger") == v3_correction.V2_TRIGGER
        and correction.get("move_units_unit_ids_required_json_type") == "string"
        and correction.get("preserve_transfer_system_prompt_required") is True
        and correction.get("legacy_prompt_fallback_for_v3_correction_forbidden")
        is True,
        "reviewed V3 correction invariant drift",
    )
    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "runtime_execution_authorized",
        "automatic_retry",
    ):
        _require(
            correction.get(field) is False,
            "reviewed V3 correction boundary drift: " + field,
        )

    return {
        "v2_parent_integration_review": deepcopy(parent),
        "v3_structured_correction_review": deepcopy(correction),
    }


def _build_v3_runtime_turn(
    *,
    state: Mapping[str, Any],
    typed_tools: Any,
    tool_contract: Mapping[str, Any],
    doctrine: str,
    round_no: int,
    feedback: str,
) -> dict[str, Any]:
    """Build one corrective turn with transfer prompt + structured feedback."""
    correction = v3_correction.build_structured_correction_retry_context(
        feedback=feedback
    )
    baseline = v8_runtime.translate_campaign_turn_for_v8(
        state=state,
        typed_tools=typed_tools,
        tool_contract=tool_contract,
        doctrine=doctrine,
        round_no=round_no,
        feedback="",
    )
    _require(
        isinstance(baseline, Mapping),
        "V3 baseline runtime turn missing",
    )
    baseline = deepcopy(dict(baseline))
    binding = baseline.get("binding")
    messages = baseline.get("messages")
    tools = baseline.get("tools")
    _require(isinstance(binding, Mapping), "V3 baseline binding missing")
    _require(
        binding.get("system_prompt_family") == "transfer",
        "V3 baseline did not preserve transfer prompt",
    )
    _require(
        isinstance(messages, list)
        and len(messages) == 2
        and messages[0].get("role") == "system"
        and messages[1].get("role") == "user",
        "V3 baseline message shape drift",
    )
    _require(isinstance(tools, list) and bool(tools), "V3 runtime tools missing")
    runtime_names = binding.get("runtime_tool_names")
    _require(
        isinstance(runtime_names, list) and bool(runtime_names),
        "V3 runtime tool names missing",
    )

    user_prompt = v8_runtime._v8_current_state_prompt(
        state=state,
        tool_contract=tool_contract,
        runtime_tool_names=runtime_names,
        doctrine=doctrine,
        round_no=round_no,
        feedback=correction["structured_feedback"],
    )
    revised_messages = deepcopy(messages)
    revised_messages[0] = {
        "role": "system",
        "content": v8_runtime.TRANSFER_SYSTEM_PROMPT,
    }
    revised_messages[1] = {"role": "user", "content": user_prompt}

    revised_binding = deepcopy(dict(binding))
    revised_binding.update(
        {
            "system_prompt_family": "transfer",
            "v3_structured_correction_applied": True,
            "v3_exact_trigger_only": True,
            "v3_structured_feedback_sha256": correction[
                "structured_feedback_sha256"
            ],
            "legacy_prompt_fallback_used": False,
        }
    )

    body = {
        key: deepcopy(value)
        for key, value in baseline.items()
        if key != "runtime_input_sha256"
    }
    body["messages"] = revised_messages
    body["binding"] = revised_binding
    body["runtime_input_sha256"] = v8_runtime._sha256(body)
    return body


class _V3RuntimeProxy:
    """Delegate all normal turns; specialize only the exact V2 corrective retry."""

    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime

    def decide_campaign_turn(
        self,
        *,
        state: Mapping[str, Any],
        typed_tools: Any,
        tool_contract: Mapping[str, Any],
        doctrine: str,
        round_no: int,
        feedback: str = "",
    ) -> dict[str, Any]:
        if feedback != v3_correction.V2_TRIGGER:
            return self.runtime.decide_campaign_turn(
                state=state,
                typed_tools=typed_tools,
                tool_contract=tool_contract,
                doctrine=doctrine,
                round_no=round_no,
                feedback=feedback,
            )

        turn = _build_v3_runtime_turn(
            state=state,
            typed_tools=typed_tools,
            tool_contract=tool_contract,
            doctrine=doctrine,
            round_no=round_no,
            feedback=feedback,
        )
        raw = self.runtime.generate(
            messages=turn["messages"],
            tools=turn["tools"],
        )
        action = v8_runtime.translate_v8_output_to_campaign(
            text=raw,
            runtime_tools=turn["tools"],
            tool_contract=tool_contract,
        )
        return {
            "runtime_input": deepcopy(turn),
            "raw_model_output": raw,
            "campaign_action": action,
            "host_mutation_performed": False,
        }


def decision_response_with_v3_structured_correction(
    runtime: Any,
    request: Mapping[str, Any],
    *,
    seq: int,
    authority_check: Callable[[int, str], bool],
) -> dict[str, Any]:
    """Upgrade only the exact V2 corrective retry before reviewed V2 handling."""
    _dependencies()
    feedback = request.get("feedback")
    if feedback != v3_correction.V2_TRIGGER:
        return ORIGINAL_V2_DECISION_RESPONSE(
            runtime,
            request,
            seq=seq,
            authority_check=authority_check,
        )

    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V9_V3_AUTHORITY_REVOKED_BEFORE_STRUCTURED_CORRECTION",
    )
    proxy = _V3RuntimeProxy(runtime)
    return ORIGINAL_V2_DECISION_RESPONSE(
        proxy,
        request,
        seq=seq,
        authority_check=authority_check,
    )


def build_pair06_v9_actionable_feedback_v3_parent_run() -> Any:
    """Build but never execute the reviewed V2 parent with V3 response binding."""
    _dependencies()

    _require(
        v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
        is ORIGINAL_V2_PARENT_BUILD,
        "reviewed V2 parent builder drift before V3 scoped build",
    )
    _require(
        v2_parent.ORIGINAL_V2_DECISION_RESPONSE is ORIGINAL_V2_DECISION_RESPONSE,
        "reviewed V2 decision-response identity drift before V3 scoped build",
    )

    v2_scoped = ORIGINAL_V2_PARENT_BUILD()
    _require(
        isinstance(v2_scoped, FunctionType),
        "reviewed V2 parent builder did not return FunctionType",
    )
    _require(
        v2_scoped.__globals__.get("_decision_response")
        is ORIGINAL_V2_DECISION_RESPONSE,
        "reviewed V2 parent decision-response binding drift",
    )

    child_command = v2_scoped.__globals__.get("_child_command")
    scoped_globals = dict(v2_scoped.__globals__)
    scoped_globals["_decision_response"] = (
        decision_response_with_v3_structured_correction
    )
    scoped_run = FunctionType(
        v2_scoped.__code__,
        scoped_globals,
        v2_scoped.__name__,
        v2_scoped.__defaults__,
        v2_scoped.__closure__,
    )
    scoped_run.__kwdefaults__ = v2_scoped.__kwdefaults__

    _require(
        scoped_run.__globals__.get("_child_command") is child_command,
        "reviewed V2 child-command binding drift during V3 scoped build",
    )
    _require(
        v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
        is ORIGINAL_V2_PARENT_BUILD,
        "reviewed V2 parent builder mutated during V3 scoped build",
    )
    _require(
        v2_parent.ORIGINAL_V2_DECISION_RESPONSE is ORIGINAL_V2_DECISION_RESPONSE,
        "reviewed V2 decision-response identity mutated during V3 scoped build",
    )
    return scoped_run


def pair06_v9_actionable_feedback_v3_runtime_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "v2_parent_integration_git_blob": V2_PARENT_INTEGRATION_GIT_BLOB,
        "v2_parent_review_git_blob": V2_PARENT_REVIEW_GIT_BLOB,
        "v3_correction_git_blob": V3_CORRECTION_GIT_BLOB,
        "v3_correction_review_git_blob": V3_CORRECTION_REVIEW_GIT_BLOB,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "actionable_feedback_v3_runtime_integration_implemented": True,
        "reviewed_v2_parent_integration_reused": True,
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_preserved": True,
        "call_scoped_decision_response_binding_upgraded_to_v3": True,
        "exact_v2_feedback_trigger_only": True,
        "nonmatching_feedback_delegates_to_v2_unchanged": True,
        "structured_feedback_injected_into_user_prompt": True,
        "corrective_retry_transfer_prompt_preserved": True,
        "corrective_retry_legacy_prompt_fallback_used": False,
        "v2_adapter_rejection_fail_closed_shim_reused": True,
        "frozen_v8_tool_schema_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "six_attempt_bound_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "process_global_parent_run_function_mutated": False,
        "process_global_child_command_builder_mutated": False,
        "process_global_decision_response_mutated": False,
        "process_global_runtime_method_mutated": False,
        "builder_executes_parent": False,
        "builder_performs_host_io": False,
        "builder_loads_model": False,
        "builder_runs_inference": False,
        "builder_spawns_child": False,
        "builder_executes_game": False,
        "consumed_v2_attempt_retry_authorized": False,
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
        "execution_blockers": (
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_PARENT_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
        ),
        "next_gate": (
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_PARENT_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "next_change_class": (
            "source_only_pair06_v9_actionable_feedback_v3_parent_integration_review"
        ),
    }


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV3RuntimeIntegrationHold(NEXT_GATE)
