"""Actionable V2 feedback shim for the observed Pair-06 V9 adapter rejection.

V1 remains immutable historical evidence. This layer wraps the exact reviewed
V1 response shim and changes only its deliberately unavailable sentinel name.

The V2 sentinel encodes the missing wire-format instruction that the consumed
fresh attempt demonstrated the model did not recover from:
`move_units.unit_ids` must be a quoted string, for example "123" or
"123,456"; it must not be a JSON array/list and must not be a bare integer.

The strict-contact retry loop already forwards
`function_not_offered:<sentinel>` verbatim as guard feedback. Therefore this
layer improves only the retry feedback text. It does not modify the frozen V8
parser/translator, does not coerce or accept malformed values, does not change
the six-attempt decision bound, and performs no host mutation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Callable, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_generation2
    as v1,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_source_binding_review_generation2
    as v1_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"

V1_RESPONSE_GIT_BLOB = "5d6ec9e9f1cb575972f0ccd41e2e9c5ac99da101"
V1_RESPONSE_REVIEW_GIT_BLOB = "a8eaa4725074a16a607425319fda5af5130f0737"

V1_SENTINEL_TOOL = "__v8_adapter_rejected_unit_ids_invalid__"
V2_SENTINEL_TOOL = (
    "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
    "not_json_array_or_bare_integer__"
)
EXPECTED_CHILD_FEEDBACK = "function_not_offered:" + V2_SENTINEL_TOOL

QUOTED_STRING_EXAMPLE_SINGLE = '"123"'
QUOTED_STRING_EXAMPLE_MULTIPLE = '"123,456"'
INVALID_JSON_ARRAY_EXAMPLE = "[123,456]"
INVALID_BARE_INTEGER_EXAMPLE = "123"

ORIGINAL_V1_RESPONSE = v1.decision_response_with_observed_adapter_rejection

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_review"
)


class Pair06V9AdapterRejectionActionableFeedbackV2Hold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionActionableFeedbackV2Hold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    reviewed = v1_review.pair06_v9_input_order_adapter_rejection_response_review_contract()

    _require(
        reviewed.get("pair06_v9_input_order_adapter_rejection_response_reviewed")
        is True,
        "V1 adapter-rejection response review missing",
    )
    _require(
        reviewed.get("shim_git_blob") == V1_RESPONSE_GIT_BLOB,
        "V1 adapter-rejection source identity drift",
    )
    _require(
        reviewed.get("sentinel_tool") == V1_SENTINEL_TOOL
        and reviewed.get("observed_retryable_error") == "unit_ids invalid",
        "V1 adapter-rejection sentinel identity drift",
    )
    _require(
        reviewed.get("only_exact_observed_adapter_error_is_retryable") is True
        and reviewed.get("other_v8_adapter_errors_still_propagate") is True
        and reviewed.get("malformed_unit_ids_coerced") is False
        and reviewed.get("malformed_unit_ids_accepted") is False,
        "V1 adapter-rejection safety boundary drift",
    )
    _require(
        reviewed.get("runtime_execution_authorized") is False
        and reviewed.get("automatic_retry") is False
        and reviewed.get("new_execution_request_opened") is False,
        "V1 adapter-rejection authority drift",
    )

    return {"v1_adapter_rejection_response_review": deepcopy(reviewed)}


def decision_response_with_actionable_adapter_rejection_feedback(
    runtime: Any,
    request: Mapping[str, Any],
    *,
    seq: int,
    authority_check: Callable[[int, str], bool],
) -> dict[str, Any]:
    """Pass through every V1 response except the exact V1 unavailable sentinel."""
    _dependencies()

    out = ORIGINAL_V1_RESPONSE(
        runtime,
        request,
        seq=seq,
        authority_check=authority_check,
    )
    _require(isinstance(out, dict), "V1 adapter-rejection response missing")

    action = out.get("campaign_action")
    if not isinstance(action, Mapping) or action.get("tool") != V1_SENTINEL_TOOL:
        return out

    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V9_ADAPTER_REJECTION_V2_AUTHORITY_REVOKED_AFTER_V1_SENTINEL",
    )

    repaired = deepcopy(out)
    repaired["campaign_action"] = {
        **deepcopy(dict(action)),
        "tool": V2_SENTINEL_TOOL,
    }
    return repaired


def pair06_v9_adapter_rejection_actionable_feedback_v2_contract() -> dict[str, Any]:
    deps = deepcopy(_dependencies())

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "v1_response_git_blob": V1_RESPONSE_GIT_BLOB,
        "v1_response_review_git_blob": V1_RESPONSE_REVIEW_GIT_BLOB,
        "v1_sentinel_tool": V1_SENTINEL_TOOL,
        "v2_sentinel_tool": V2_SENTINEL_TOOL,
        "expected_child_feedback": EXPECTED_CHILD_FEEDBACK,
        "quoted_string_example_single": QUOTED_STRING_EXAMPLE_SINGLE,
        "quoted_string_example_multiple": QUOTED_STRING_EXAMPLE_MULTIPLE,
        "invalid_json_array_example": INVALID_JSON_ARRAY_EXAMPLE,
        "invalid_bare_integer_example": INVALID_BARE_INTEGER_EXAMPLE,
        "actionable_feedback_v2_implemented": True,
        "v1_source_modified": False,
        "v1_success_responses_pass_through_unchanged": True,
        "only_v1_sentinel_is_rewritten": True,
        "feedback_requires_quoted_unit_ids_string": True,
        "feedback_rejects_json_array_unit_ids": True,
        "feedback_rejects_bare_integer_unit_ids": True,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "six_attempt_decision_bound_modified": False,
        "host_validation_modified": False,
        "world_mutation_before_child_validation": False,
        "consumed_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "attempt_claim_created": False,
        "attempt_created": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "dependencies": deps,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionActionableFeedbackV2Hold(NEXT_GATE)
