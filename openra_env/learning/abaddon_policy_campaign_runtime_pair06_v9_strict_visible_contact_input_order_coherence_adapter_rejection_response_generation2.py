"""Source-only adapter-rejection response shim for Pair-06 V9 input-order coherence.

The consumed input-order attempt exposed one parent-side adapter failure:
the frozen V8 campaign runtime raised
`V8CampaignRuntimeError("unit_ids invalid")` after inference and before the
child received a DECIDE_RESPONSE.

This module does not modify the frozen V8 parser or translator and does not
coerce malformed unit_ids values. It wraps the already-reviewed historical
parent decision-response helper and converts only that exact observed adapter
error into a deliberately unavailable sentinel campaign action. The existing
V9 child validation loop can then reject the sentinel without world mutation
and use its already-bounded decision retry budget.

Every other V8 adapter error propagates unchanged. Import and contract
inspection perform no host I/O, model load, inference, game execution, attempt
claim, replay, training, deployment, chain, wallet/funds, or scheduler action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Callable, Mapping

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as parent_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-response-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
OBSERVED_RETRYABLE_ERROR = "unit_ids invalid"
SENTINEL_TOOL = "__v8_adapter_rejected_unit_ids_invalid__"

NO_OFFLOAD_PARENT_GIT_BLOB = "231758aeced0a57949dc39165df0f994e8473ebc"
NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB = "6a65984b81e563def012c6da1405ad47747bb465"
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

ORIGINAL_DECISION_RESPONSE = parent._decision_response

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_RESPONSE_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_response_review"
)


class Pair06V9InputOrderAdapterRejectionResponseHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionResponseHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    reviewed = (
        parent_review
        .pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    )
    _require(
        reviewed.get(
            "pair06_v8_parent_launcher_supervisor_no_offload_reviewed"
        )
        is True,
        "reviewed no-offload parent missing",
    )
    _require(
        reviewed.get("pair_slot") == PAIR_SLOT
        and reviewed.get("arm") == ARM,
        "reviewed no-offload parent scope drift",
    )
    _require(
        reviewed.get("automatic_retry") is False
        and reviewed.get("execution_authorized") is False,
        "reviewed no-offload parent authority drift",
    )
    return {"no_offload_parent_review": deepcopy(reviewed)}


def decision_response_with_observed_adapter_rejection(
    runtime: Any,
    request: Mapping[str, Any],
    *,
    seq: int,
    authority_check: Callable[[int, str], bool],
) -> dict[str, Any]:
    """Return historical response, except for the one observed retryable adapter error."""
    _dependencies()
    try:
        return ORIGINAL_DECISION_RESPONSE(
            runtime,
            request,
            seq=seq,
            authority_check=authority_check,
        )
    except v8_runtime.V8CampaignRuntimeError as exc:
        if str(exc) != OBSERVED_RETRYABLE_ERROR:
            raise

        _require(
            authority_check(PAIR_SLOT, ARM) is True,
            "PAIR06_V9_INPUT_ORDER_AUTHORITY_REVOKED_AFTER_ADAPTER_REJECTION",
        )
        return {
            "type": "DECIDE_RESPONSE",
            "seq": seq,
            "protocol_version": 1,
            "pair_slot": PAIR_SLOT,
            "arm": ARM,
            "attempt_id": request["attempt_id"],
            "round_no": request["round_no"],
            "attempt_no": request["attempt_no"],
            "campaign_action": {
                "tool": SENTINEL_TOOL,
                "arguments": {},
            },
            "host_mutation_performed": False,
        }


def pair06_v9_input_order_adapter_rejection_response_contract() -> dict[str, Any]:
    dependencies = deepcopy(_dependencies())
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "observed_retryable_error": OBSERVED_RETRYABLE_ERROR,
        "sentinel_tool": SENTINEL_TOOL,
        "no_offload_parent_git_blob": NO_OFFLOAD_PARENT_GIT_BLOB,
        "no_offload_parent_review_git_blob": NO_OFFLOAD_PARENT_REVIEW_GIT_BLOB,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "adapter_rejection_response_shim_implemented": True,
        "only_exact_observed_adapter_error_is_retryable": True,
        "other_v8_adapter_errors_still_propagate": True,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "frozen_v8_runtime_source_modified": False,
        "historical_parent_source_modified": False,
        "historical_decision_response_reused": True,
        "sentinel_is_deliberately_unavailable_tool": True,
        "world_mutation_before_child_validation": False,
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
    raise Pair06V9InputOrderAdapterRejectionResponseHold(NEXT_GATE)
