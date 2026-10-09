"""Narrow deterministic V4 repair for Pair-06 move_units unit_ids wire format.

The consumed actionable-feedback V3 attempt proved that stronger retry prompting
still allowed the deterministic model to emit the same semantically clear but
wire-invalid move_units unit_ids value until the six-attempt bound exhausted.

V4 does not relax the host validator and does not accept arbitrary malformed
values.  It defines a pure, source-only canonicalization boundary for exactly
two unambiguous representations produced by the accepted textual parser:

* one positive integer actor id; or
* a non-empty list of distinct positive integer actor ids.

Every candidate id must be present in CURRENT STATE own_units.  Only then may
the value be rendered as the already-required comma-separated JSON string and
revalidated through the unchanged frozen V8 translator.  Existing string
values and non-move_units output are passed through unchanged.  Empty lists,
duplicates, booleans, floats, nested values, foreign ids, missing coordinates,
or any other shape remain fail-closed.

This module performs no host I/O, model load, inference, game execution,
attempt claim, retry, replay, training, deployment, chain, wallet/funds, or
scheduler mutation and grants none of those authorities.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
from typing import Any, Mapping, Sequence

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_source_binding_review_generation2
    as v3_correction_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_source_binding_review_generation2
    as v3_runtime_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_authorized_execution_launcher_source_binding_review_generation2
    as v3_launcher_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v4-"
    "unit-ids-canonicalization-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"

V3_CORRECTION_REVIEW_GIT_BLOB = "437a0a35223b8b418fb3482407c8dc00d160f8e9"
V3_RUNTIME_REVIEW_GIT_BLOB = "b82c6465656e0b06509034b90af8b79c659ae92b"
V3_LAUNCHER_REVIEW_GIT_BLOB = "e9436a9322f193d6e032a9b54e1bacb1a7ed9d74"
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

CONSUMED_V3_MAIN_HEAD = "e983220f85e35c024bcc0da8dec418bcd8342e03"
OBSERVED_V3_TERMINAL_FEEDBACK = (
    "function_not_offered:"
    "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
    "not_json_array_or_bare_integer__"
)
OBSERVED_V3_FAILED_ROUND = 6
OBSERVED_V3_MAX_ATTEMPTS = 6

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V4_UNIT_IDS_CANONICALIZATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v4_unit_ids_"
    "canonicalization_review"
)


class Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    correction = (
        v3_correction_review
        .pair06_v9_actionable_feedback_v3_structured_correction_review_contract()
    )
    runtime = (
        v3_runtime_review
        .pair06_v9_actionable_feedback_v3_runtime_integration_review_contract()
    )
    launcher = (
        v3_launcher_review
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract()
    )

    _require(
        correction.get(
            "pair06_v9_actionable_feedback_v3_structured_correction_reviewed"
        )
        is True
        and correction.get("move_units_unit_ids_required_json_type") == "string"
        and correction.get("malformed_unit_ids_coerced") is False,
        "reviewed V3 correction boundary drift",
    )
    _require(
        runtime.get(
            "pair06_v9_actionable_feedback_v3_runtime_integration_reviewed"
        )
        is True
        and runtime.get("structured_feedback_injected_into_user_prompt") is True
        and runtime.get("malformed_unit_ids_coerced") is False
        and runtime.get("automatic_retry") is False,
        "reviewed V3 runtime integration boundary drift",
    )
    _require(
        launcher.get(
            "pair06_v9_actionable_feedback_v3_authorized_execution_launcher_reviewed"
        )
        is True
        and launcher.get("maximum_attempts") == 1
        and launcher.get("maximum_automatic_retries") == 0
        and launcher.get("authorization_reusable_after_attempt_claim") is False,
        "reviewed V3 launcher one-shot boundary drift",
    )
    _require(
        v8_runtime.v8_tool_runtime_contract().get("host_validation_unchanged")
        is True,
        "frozen V8 host-validation boundary drift",
    )
    return {
        "v3_correction_review": deepcopy(correction),
        "v3_runtime_review": deepcopy(runtime),
        "v3_launcher_review": deepcopy(launcher),
    }


def _current_owned_ids(state: Mapping[str, Any]) -> tuple[int, ...]:
    _require(isinstance(state, Mapping), "current state must be mapping")
    rows = state.get("units_summary")
    _require(isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)),
             "current own_units summary missing")
    ids: list[int] = []
    for row in rows:
        _require(isinstance(row, Mapping), "current own_units row invalid")
        value = row.get("id")
        _require(type(value) is int and value > 0, "current own_units id invalid")
        ids.append(value)
    _require(len(ids) == len(set(ids)), "current own_units ids duplicated")
    return tuple(ids)


def _candidate_ids(value: Any) -> tuple[int, ...] | None:
    if type(value) is int:
        _require(value > 0, "move_units unit_ids integer must be positive")
        return (value,)
    if isinstance(value, list):
        _require(bool(value), "move_units unit_ids list must be non-empty")
        _require(
            all(type(item) is int and item > 0 for item in value),
            "move_units unit_ids list must contain only positive integers",
        )
        ids = tuple(value)
        _require(
            len(ids) == len(set(ids)),
            "move_units unit_ids list must not contain duplicates",
        )
        return ids
    return None


def canonicalize_move_units_unit_ids(
    *,
    raw_model_output: str,
    state: Mapping[str, Any],
) -> dict[str, Any]:
    """Canonically repair only unambiguous owned move_units ids.

    The returned text must still pass the unchanged frozen V8 parser/translator
    before any host validator may see the action.
    """
    _dependencies()
    _require(
        isinstance(raw_model_output, str) and bool(raw_model_output.strip()),
        "raw model output required",
    )
    parsed = v8_runtime.parse_v8_tool_output(raw_model_output)
    tool = parsed["tool"]
    args = deepcopy(dict(parsed["arguments"]))

    if tool != "move_units":
        return {
            "raw_model_output": raw_model_output,
            "canonical_raw_model_output": raw_model_output,
            "canonicalization_applied": False,
            "reason": "non_move_units_passthrough",
            "owned_ids_checked": False,
            "host_validation_performed": False,
        }

    _require(
        {"unit_ids", "target_x", "target_y"}.issubset(args),
        "move_units required arguments missing before V4 canonicalization",
    )
    value = args["unit_ids"]
    if isinstance(value, str):
        return {
            "raw_model_output": raw_model_output,
            "canonical_raw_model_output": raw_model_output,
            "canonicalization_applied": False,
            "reason": "unit_ids_already_string",
            "owned_ids_checked": False,
            "host_validation_performed": False,
        }

    ids = _candidate_ids(value)
    _require(
        ids is not None,
        "move_units unit_ids shape is not V4-canonicalizable",
    )
    owned = set(_current_owned_ids(state))
    _require(
        all(value in owned for value in ids),
        "move_units unit_ids contains id absent from current own_units",
    )

    args["unit_ids"] = ",".join(str(value) for value in ids)
    ordered_keys = ("unit_ids", "target_x", "target_y", "queued")
    body = []
    for key in ordered_keys:
        if key not in args:
            continue
        rendered = json.dumps(args[key], ensure_ascii=True, separators=(",", ":"))
        body.append(f"<parameter={key}>{rendered}</parameter>")
    canonical = (
        "<tool_call><function=move_units>"
        + "".join(body)
        + "</function></tool_call>"
    )

    # Re-run the unchanged frozen parser and translator now.  This proves the
    # repair produces only a value the existing V8 boundary already accepts.
    translated = v8_runtime.translate_v8_output_to_campaign(
        text=canonical,
        runtime_tools=[
            tool
            for tool in v8_runtime._ACCEPTED_TOOLS
            if tool.get("function", {}).get("name") == "move_units"
        ],
        tool_contract={
            "offered_tool_names": ["move_units"],
            "production_functions": {},
            "legal_buildings": [],
            "legal_units": [],
        },
    )
    _require(
        translated.get("tool") == "move_units",
        "V4 canonicalized output did not survive frozen V8 translator",
    )

    return {
        "raw_model_output": raw_model_output,
        "canonical_raw_model_output": canonical,
        "canonicalization_applied": True,
        "reason": "owned_integer_ids_to_required_string",
        "canonical_unit_ids": args["unit_ids"],
        "canonicalized_ids": list(ids),
        "owned_ids_checked": True,
        "frozen_v8_translation_revalidated": True,
        "host_validation_performed": False,
    }


def pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "v3_correction_review_git_blob": V3_CORRECTION_REVIEW_GIT_BLOB,
        "v3_runtime_review_git_blob": V3_RUNTIME_REVIEW_GIT_BLOB,
        "v3_launcher_review_git_blob": V3_LAUNCHER_REVIEW_GIT_BLOB,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "consumed_v3_main_head": CONSUMED_V3_MAIN_HEAD,
        "observed_v3_terminal_feedback": OBSERVED_V3_TERMINAL_FEEDBACK,
        "observed_v3_failed_round": OBSERVED_V3_FAILED_ROUND,
        "observed_v3_max_attempts": OBSERVED_V3_MAX_ATTEMPTS,
        "v4_unit_ids_canonicalization_implemented": True,
        "canonicalizable_bare_positive_integer": True,
        "canonicalizable_nonempty_distinct_positive_integer_list": True,
        "all_candidate_ids_must_be_currently_owned": True,
        "existing_string_passes_through_unchanged": True,
        "non_move_units_passes_through_unchanged": True,
        "foreign_ids_fail_closed": True,
        "empty_list_fails_closed": True,
        "duplicate_ids_fail_closed": True,
        "boolean_ids_fail_closed": True,
        "float_ids_fail_closed": True,
        "nested_ids_fail_closed": True,
        "canonical_output_revalidated_by_frozen_v8_translator": True,
        "frozen_v8_runtime_source_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "host_validator_bypassed": False,
        "world_mutation_performed": False,
        "consumed_v3_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "attempt_claim_created": False,
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
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationHold(NEXT_GATE)
