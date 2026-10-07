"""Structured corrective retry context for the repeated Pair-06 V9 move_units wire-format failure.

V2 proved that the exact adapter rejection reached the retry loop but encoding
the repair only inside a deliberately unavailable sentinel tool name was not
sufficient: the next model decisions still exhausted the six-attempt bound.

V3 remains source-only. For exactly that reviewed V2 terminal feedback it
builds a deterministic, compact correction payload that tells the model:
* move_units.unit_ids is a JSON string, never an array/list or integer;
* one id is encoded as {"unit_ids":"135"};
* multiple ids are encoded as {"unit_ids":"135,137"};
* ids must come from current own_units; and
* exactly one currently offered tool call must be returned.

V3 also specifies that corrective retries retain the reviewed transfer system
prompt instead of falling back to the legacy prompt family. The frozen V8 tool
schema, parser/translator, host validator, six-attempt bound, current state,
and tool surface remain unchanged.

This source performs no host I/O, model load, inference, game execution,
attempt claim, retry, training, deployment, chain, wallet/funds, or scheduler
mutation and grants none of those authorities.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from typing import Any

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_source_binding_review_generation2
    as v2_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_closeout_source_binding_review_generation2
    as closeout_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "structured-correction-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"

V2_FEEDBACK_REVIEW_GIT_BLOB = "e1931048b9e8e589b0749d68e11376569da33612"
SECOND_EXHAUSTION_CLOSEOUT_REVIEW_GIT_BLOB = (
    "4dadc961e02cd13893bd842bc6ee727c443b55a2"
)
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

V2_TRIGGER = (
    "function_not_offered:"
    "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
    "not_json_array_or_bare_integer__"
)
V3_FEEDBACK_PREFIX = "PAIR06_V9_STRUCTURED_CORRECTION_V3="

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v3_structured_correction_review"
)


class Pair06V9ActionableFeedbackV3StructuredCorrectionHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3StructuredCorrectionHold(message)


def _stable_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest()


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    v2 = v2_review.pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract()
    closeout = (
        closeout_review
        .pair06_v9_v2_second_exhaustion_preservation_closeout_review_contract()
    )

    _require(
        v2.get("pair06_v9_adapter_rejection_actionable_feedback_v2_reviewed")
        is True,
        "reviewed V2 actionable feedback missing",
    )
    _require(
        v2.get("expected_child_feedback") == V2_TRIGGER,
        "reviewed V2 terminal feedback identity drift",
    )
    _require(
        v2.get("feedback_requires_quoted_unit_ids_string") is True
        and v2.get("feedback_rejects_json_array_unit_ids") is True
        and v2.get("feedback_rejects_bare_integer_unit_ids") is True,
        "reviewed V2 wire-format boundary drift",
    )
    _require(
        v2.get("malformed_unit_ids_coerced") is False
        and v2.get("malformed_unit_ids_accepted") is False,
        "reviewed V2 parser boundary drift",
    )

    _require(
        closeout.get(
            "pair06_v9_v2_second_exhaustion_preservation_closeout_reviewed"
        )
        is True,
        "second V2 exhaustion closeout review missing",
    )
    _require(
        closeout.get("attempt_marker_sha256")
        == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
        and closeout.get("preservation_receipt_sha256")
        == "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021",
        "second V2 exhaustion closeout identity drift",
    )
    _require(
        closeout.get("same_v2_retry_recommended") is False
        and closeout.get("structured_correction_v3_required") is True
        and closeout.get("runtime_retry_authorized") is False
        and closeout.get("new_execution_request_opened") is False,
        "second V2 exhaustion closeout frontier drift",
    )

    move_tools = [
        tool
        for tool in v8_runtime._ACCEPTED_TOOLS
        if tool.get("function", {}).get("name") == "move_units"
    ]
    _require(len(move_tools) == 1, "frozen V8 move_units tool identity drift")
    params = move_tools[0]["function"]["parameters"]
    props = params["properties"]
    _require(
        props.get("unit_ids") == {"type": "string"},
        "frozen V8 move_units.unit_ids schema is not string",
    )
    _require(
        v8_runtime.FINAL_ACCEPTANCE_TRANSFER_CORRECT
        > v8_runtime.FINAL_ACCEPTANCE_LEGACY_CORRECT,
        "V8 transfer prompt no longer outperforms legacy acceptance",
    )

    return {
        "v2_feedback_review": deepcopy(v2),
        "second_exhaustion_closeout_review": deepcopy(closeout),
    }


def _correction_payload() -> dict[str, Any]:
    return {
        "argument": "unit_ids",
        "ids_source": "CURRENT STATE own_units id values",
        "instruction": (
            "Choose exactly one CURRENT_ALLOWED_TOOL_NAMES action. "
            "If choosing move_units, encode unit_ids as one JSON string. "
            "Use one actor id or comma-separated actor ids from current own_units. "
            "Do not return unit_ids as an array/list or integer."
        ),
        "invalid_bare_integer_argument_json": '{"unit_ids":135}',
        "invalid_json_array_argument_json": '{"unit_ids":[135,137]}',
        "kind": "wire_format_correction",
        "reason_code": "move_units_unit_ids_must_be_string",
        "required_json_type": "string",
        "required_value_format": "one_actor_id_or_comma_separated_actor_ids",
        "tool": "move_units",
        "valid_multiple_argument_json": '{"unit_ids":"135,137"}',
        "valid_single_argument_json": '{"unit_ids":"135"}',
    }


def build_structured_correction_retry_context(*, feedback: str) -> dict[str, Any]:
    """Build deterministic corrective retry context for only the exact V2 trigger."""
    _dependencies()
    _require(
        type(feedback) is str and feedback == V2_TRIGGER,
        "PAIR06_V9_V3_STRUCTURED_CORRECTION_EXACT_V2_TRIGGER_REQUIRED",
    )

    payload = _correction_payload()
    feedback_out = V3_FEEDBACK_PREFIX + _stable_json(payload)

    return {
        "schema": CONTRACT_SCHEMA + ".retry-context",
        "input_feedback": feedback,
        "structured_feedback": feedback_out,
        "structured_feedback_sha256": _sha256_text(feedback_out),
        "structured_payload": deepcopy(payload),
        "system_prompt": v8_runtime.TRANSFER_SYSTEM_PROMPT,
        "system_prompt_family": "transfer",
        "preserve_transfer_system_prompt": True,
        "legacy_system_prompt_selected": False,
        "exact_trigger_only": True,
        "frozen_v8_tool_schema_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "six_attempt_bound_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "host_mutation_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def pair06_v9_actionable_feedback_v3_structured_correction_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    example = build_structured_correction_retry_context(feedback=V2_TRIGGER)

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "v2_feedback_review_git_blob": V2_FEEDBACK_REVIEW_GIT_BLOB,
        "second_exhaustion_closeout_review_git_blob": (
            SECOND_EXHAUSTION_CLOSEOUT_REVIEW_GIT_BLOB
        ),
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "exact_v2_trigger": V2_TRIGGER,
        "v3_feedback_prefix": V3_FEEDBACK_PREFIX,
        "structured_correction_v3_implemented": True,
        "exact_v2_trigger_only": True,
        "move_units_unit_ids_required_json_type": "string",
        "move_units_unit_ids_source": "CURRENT STATE own_units id values",
        "valid_single_argument_json": '{"unit_ids":"135"}',
        "valid_multiple_argument_json": '{"unit_ids":"135,137"}',
        "invalid_json_array_argument_json": '{"unit_ids":[135,137]}',
        "invalid_bare_integer_argument_json": '{"unit_ids":135}',
        "preserve_transfer_system_prompt_required": True,
        "legacy_prompt_fallback_for_v3_correction_forbidden": True,
        "reviewed_transfer_acceptance_correct": (
            v8_runtime.FINAL_ACCEPTANCE_TRANSFER_CORRECT
        ),
        "reviewed_legacy_acceptance_correct": (
            v8_runtime.FINAL_ACCEPTANCE_LEGACY_CORRECT
        ),
        "frozen_v8_tool_schema_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "six_attempt_bound_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "consumed_v2_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "contract_inspection_performs_host_io": False,
        "example_retry_context": deepcopy(example),
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED",
        ),
        "next_gate": (
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED"
        ),
        "next_change_class": (
            "source_only_pair06_v9_actionable_feedback_v3_structured_correction_"
            "runtime_integration"
        ),
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV3StructuredCorrectionHold(
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED"
    )
