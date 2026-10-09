"""Call-scoped runtime integration for Pair-06 actionable-feedback V4.

V3 proved that deterministic structured feedback reached the retry path but the
model could still repeat an unambiguous wire-invalid move_units.unit_ids value.
V4 therefore changes only the corrective retry binding:

* non-matching feedback delegates to the reviewed V3 response unchanged;
* the exact reviewed terminal feedback still uses the reviewed V3 structured
  corrective turn and transfer prompt;
* model output first passes through the unchanged frozen V8 translator;
* only exact V8CampaignRuntimeError("unit_ids invalid") may invoke the reviewed
  V4 canonicalizer;
* the V4 canonicalizer requires every repaired integer actor id to be currently
  owned and then revalidates its output through the same frozen V8 translator;
* every other parser/translator error propagates unchanged.

The reviewed V2 fail-closed adapter shim remains outside this proxy.  If V4
cannot safely canonicalize the exact malformed value, the exception propagates
and the existing bounded rejection path remains in force.

No process-global function is mutated. Building or inspecting this integration
performs no host I/O, model load, inference, game execution, attempt claim,
retry, replay, training, deployment, chain, wallet/funds, or scheduler action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from types import FunctionType
from typing import Any, Callable, Mapping

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_generation2
    as v3_runtime,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_source_binding_review_generation2
    as v3_runtime_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_unit_ids_canonicalization_generation2
    as v4_repair,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_unit_ids_canonicalization_source_binding_review_generation2
    as v4_repair_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v4-"
    "runtime-integration.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-"
    "actionable-feedback-v4-unit-ids-canonicalization"
)

V3_RUNTIME_INTEGRATION_GIT_BLOB = "71a065ff3a38d5c298bbf16559b942af22d564ff"
V3_RUNTIME_REVIEW_GIT_BLOB = "b82c6465656e0b06509034b90af8b79c659ae92b"
V4_REPAIR_GIT_BLOB = "05a0e5be44d5f871c194f4a70826436e4bb2aed2"
V4_REPAIR_REVIEW_GIT_BLOB = "4d0bf8058da16acd65abef86cd88f62c618a9f83"

ORIGINAL_V3_PARENT_BUILD = (
    v3_runtime.build_pair06_v9_actionable_feedback_v3_parent_run
)
ORIGINAL_V3_DECISION_RESPONSE = (
    v3_runtime.decision_response_with_v3_structured_correction
)
ORIGINAL_V2_DECISION_RESPONSE = v3_runtime.ORIGINAL_V2_DECISION_RESPONSE

TRIGGER = v4_repair.OBSERVED_V3_TERMINAL_FEEDBACK
RETRYABLE_TRANSLATOR_ERROR = "unit_ids invalid"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V4_RUNTIME_INTEGRATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v4_runtime_integration_review"
)


class Pair06V9ActionableFeedbackV4RuntimeIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV4RuntimeIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    v3 = (
        v3_runtime_review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
    )
    v4 = (
        v4_repair_review
        .pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract()
    )

    _require(
        v3.get("pair06_v9_actionable_feedback_v3_runtime_integration_reviewed")
        is True,
        "reviewed V3 runtime integration missing",
    )
    _require(
        v3.get("structured_feedback_injected_into_user_prompt") is True
        and v3.get("corrective_retry_transfer_prompt_preserved") is True
        and v3.get("v2_adapter_rejection_fail_closed_shim_reused") is True,
        "reviewed V3 corrective runtime boundary drift",
    )
    _require(
        v3.get("runtime_execution_authorized") is False
        and v3.get("automatic_retry") is False,
        "reviewed V3 runtime integration authority drift",
    )

    _require(
        v4.get(
            "pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_reviewed"
        )
        is True,
        "reviewed V4 unit_ids canonicalization missing",
    )
    _require(
        v4.get("all_candidate_ids_must_be_currently_owned") is True
        and v4.get("foreign_ids_fail_closed") is True
        and v4.get("duplicate_ids_fail_closed") is True
        and v4.get("canonical_output_revalidated_by_frozen_v8_translator")
        is True,
        "reviewed V4 repair safety boundary drift",
    )
    _require(
        v4.get("host_validator_modified") is False
        and v4.get("host_validator_bypassed") is False
        and v4.get("consumed_v3_attempt_retry_authorized") is False
        and v4.get("new_execution_request_opened") is False
        and v4.get("runtime_execution_authorized") is False
        and v4.get("automatic_retry") is False,
        "reviewed V4 repair authority drift",
    )

    return {
        "v3_runtime_integration_review": deepcopy(v3),
        "v4_unit_ids_canonicalization_review": deepcopy(v4),
    }


class _V4RuntimeProxy:
    """Specialize only the exact corrective retry; delegate everything else."""

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
        if feedback != TRIGGER:
            return self.runtime.decide_campaign_turn(
                state=state,
                typed_tools=typed_tools,
                tool_contract=tool_contract,
                doctrine=doctrine,
                round_no=round_no,
                feedback=feedback,
            )

        turn = v3_runtime._build_v3_runtime_turn(
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

        canonicalization = {
            "canonicalization_applied": False,
            "reason": "frozen_v8_translation_accepted_original_output",
        }
        translated_text = raw
        try:
            action = v8_runtime.translate_v8_output_to_campaign(
                text=raw,
                runtime_tools=turn["tools"],
                tool_contract=tool_contract,
            )
        except v8_runtime.V8CampaignRuntimeError as exc:
            if str(exc) != RETRYABLE_TRANSLATOR_ERROR:
                raise

            canonicalization = v4_repair.canonicalize_move_units_unit_ids(
                raw_model_output=raw,
                state=state,
                runtime_tools=turn["tools"],
                tool_contract=tool_contract,
            )
            _require(
                canonicalization.get("canonicalization_applied") is True,
                "V4 exact unit_ids error did not produce safe canonicalization",
            )
            translated_text = canonicalization["canonical_raw_model_output"]
            action = v8_runtime.translate_v8_output_to_campaign(
                text=translated_text,
                runtime_tools=turn["tools"],
                tool_contract=tool_contract,
            )

        return {
            "runtime_input": deepcopy(turn),
            "raw_model_output": raw,
            "translated_model_output": translated_text,
            "v4_unit_ids_canonicalization": deepcopy(canonicalization),
            "campaign_action": action,
            "host_mutation_performed": False,
        }


def decision_response_with_v4_unit_ids_canonicalization(
    runtime: Any,
    request: Mapping[str, Any],
    *,
    seq: int,
    authority_check: Callable[[int, str], bool],
) -> dict[str, Any]:
    """Upgrade only the exact corrective retry; otherwise preserve V3 behavior."""
    _dependencies()
    if request.get("feedback") != TRIGGER:
        return ORIGINAL_V3_DECISION_RESPONSE(
            runtime,
            request,
            seq=seq,
            authority_check=authority_check,
        )

    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V9_V4_AUTHORITY_REVOKED_BEFORE_CANONICALIZED_CORRECTION",
    )
    proxy = _V4RuntimeProxy(runtime)
    return ORIGINAL_V2_DECISION_RESPONSE(
        proxy,
        request,
        seq=seq,
        authority_check=authority_check,
    )


def build_pair06_v9_actionable_feedback_v4_parent_run() -> Any:
    """Build but never execute the reviewed V3 parent with V4 response binding."""
    _dependencies()

    _require(
        v3_runtime.build_pair06_v9_actionable_feedback_v3_parent_run
        is ORIGINAL_V3_PARENT_BUILD,
        "reviewed V3 parent builder drift before V4 scoped build",
    )
    _require(
        v3_runtime.decision_response_with_v3_structured_correction
        is ORIGINAL_V3_DECISION_RESPONSE,
        "reviewed V3 decision response drift before V4 scoped build",
    )

    v3_scoped = ORIGINAL_V3_PARENT_BUILD()
    _require(
        isinstance(v3_scoped, FunctionType),
        "reviewed V3 parent builder did not return FunctionType",
    )
    _require(
        v3_scoped.__globals__.get("_decision_response")
        is ORIGINAL_V3_DECISION_RESPONSE,
        "reviewed V3 parent decision-response binding drift",
    )

    child_command = v3_scoped.__globals__.get("_child_command")
    scoped_globals = dict(v3_scoped.__globals__)
    scoped_globals["_decision_response"] = (
        decision_response_with_v4_unit_ids_canonicalization
    )
    scoped_run = FunctionType(
        v3_scoped.__code__,
        scoped_globals,
        v3_scoped.__name__,
        v3_scoped.__defaults__,
        v3_scoped.__closure__,
    )
    scoped_run.__kwdefaults__ = v3_scoped.__kwdefaults__

    _require(
        scoped_run.__globals__.get("_child_command") is child_command,
        "reviewed V3 child-command binding drift during V4 scoped build",
    )
    _require(
        v3_runtime.build_pair06_v9_actionable_feedback_v3_parent_run
        is ORIGINAL_V3_PARENT_BUILD,
        "reviewed V3 parent builder mutated during V4 scoped build",
    )
    _require(
        v3_runtime.decision_response_with_v3_structured_correction
        is ORIGINAL_V3_DECISION_RESPONSE,
        "reviewed V3 decision response mutated during V4 scoped build",
    )
    return scoped_run


def pair06_v9_actionable_feedback_v4_runtime_integration_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "v3_runtime_integration_git_blob": V3_RUNTIME_INTEGRATION_GIT_BLOB,
        "v3_runtime_review_git_blob": V3_RUNTIME_REVIEW_GIT_BLOB,
        "v4_repair_git_blob": V4_REPAIR_GIT_BLOB,
        "v4_repair_review_git_blob": V4_REPAIR_REVIEW_GIT_BLOB,
        "actionable_feedback_v4_runtime_integration_implemented": True,
        "reviewed_v3_parent_integration_reused": True,
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_preserved": True,
        "call_scoped_decision_response_binding_upgraded_to_v4": True,
        "exact_terminal_feedback_trigger_only": True,
        "nonmatching_feedback_delegates_to_v3_unchanged": True,
        "reviewed_v3_structured_turn_reused": True,
        "corrective_retry_transfer_prompt_preserved": True,
        "original_output_first_checked_by_frozen_v8_translator": True,
        "v4_repair_only_after_exact_unit_ids_invalid": True,
        "current_owned_ids_required_for_repair": True,
        "canonical_output_revalidated_by_frozen_v8_translator": True,
        "other_v8_translation_errors_propagate": True,
        "unsafe_or_ambiguous_unit_ids_fail_closed": True,
        "v2_adapter_rejection_fail_closed_shim_reused": True,
        "frozen_v8_runtime_source_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "host_validator_bypassed": False,
        "six_attempt_bound_modified": False,
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
        "consumed_v3_attempt_retry_authorized": False,
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


def review_wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV4RuntimeIntegrationHold(NEXT_GATE)
