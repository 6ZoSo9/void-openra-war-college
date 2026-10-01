"""Exact-blob review of the Pair-06 V9 input-order adapter-rejection shim.

Pins the source-only shim and focused regression tests. The review proves that
only the exact observed V8 adapter error `unit_ids invalid` is converted to a
deliberately unavailable sentinel action so the existing child validation loop
can reject it. No malformed value is coerced or accepted and every other V8
adapter error remains fatal/fail-closed.

This review performs no host I/O, model load, inference, game execution,
attempt claim, replay, training, deployment, chain, wallet/funds, or scheduler
action and grants none of those authorities.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_generation2
    as shim,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-response-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "e36e97ca81462bdc92137645b730a6fc70198c8f"

SHIM_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "adapter_rejection_response_generation2.py"
)
SHIM_GIT_BLOB = "5d6ec9e9f1cb575972f0ccd41e2e9c5ac99da101"

SHIM_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "adapter_rejection_response_generation2.py"
)
SHIM_TEST_GIT_BLOB = "35d611399501f897699984c01bb3daf831caae13"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_PARENT_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_parent_integration"
)


class Pair06V9InputOrderAdapterRejectionResponseReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionResponseReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = shim.pair06_v9_input_order_adapter_rejection_response_contract()

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline",
        "adapter-rejection shim scope drift",
    )
    _require(
        out.get("adapter_rejection_response_shim_implemented") is True,
        "adapter-rejection shim missing",
    )
    _require(
        out.get("observed_retryable_error") == "unit_ids invalid"
        and out.get("sentinel_tool")
        == "__v8_adapter_rejected_unit_ids_invalid__",
        "adapter-rejection identity drift",
    )
    for field in (
        "only_exact_observed_adapter_error_is_retryable",
        "other_v8_adapter_errors_still_propagate",
        "historical_decision_response_reused",
        "sentinel_is_deliberately_unavailable_tool",
    ):
        _require(
            out.get(field) is True,
            "adapter-rejection invariant drift: " + field,
        )
    for field in (
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "frozen_v8_runtime_source_modified",
        "historical_parent_source_modified",
        "world_mutation_before_child_validation",
        "consumed_input_order_attempt_retry_authorized",
        "new_execution_request_opened",
        "attempt_claim_created",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "adapter-rejection boundary drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (SHIM_PATH, SHIM_GIT_BLOB),
        (SHIM_TEST_PATH, SHIM_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_input_order_adapter_rejection_response_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "shim_path": SHIM_PATH,
        "shim_git_blob": SHIM_GIT_BLOB,
        "shim_test_path": SHIM_TEST_PATH,
        "shim_test_git_blob": SHIM_TEST_GIT_BLOB,
        "pair06_v9_input_order_adapter_rejection_response_reviewed": True,
        "observed_retryable_error": validated["observed_retryable_error"],
        "sentinel_tool": validated["sentinel_tool"],
        "only_exact_observed_adapter_error_is_retryable": True,
        "other_v8_adapter_errors_still_propagate": True,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "attempt_created": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_shim": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderAdapterRejectionResponseReviewHold(NEXT_GATE)
