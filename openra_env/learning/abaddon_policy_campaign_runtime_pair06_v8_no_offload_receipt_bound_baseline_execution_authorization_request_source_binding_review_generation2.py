"""Source-only review of the replacement receipt-bound no-offload pair-06 request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-receipt-bound-baseline-execution-authorization-request-review-contract.v1"
)

REQUEST_GIT_BLOB = "d1f821cd2ec12c11045f1af16e521b6331c2b804"
REQUEST_SOURCE_SHA256 = (
    "7b8f12e7cc904702abca02383fbe27482538c00da685c99711b79d985d45649c"
)
REQUEST_TEST_GIT_BLOB = "78714d94cd9428ba43f91bcd24f8076b2199efe4"
REQUEST_TEST_SHA256 = (
    "55dd521cb2201df14890f748c3a806e923c58a34494e21ae576f05ff73a2657f"
)
REQUEST_BYTES_SHA256 = (
    "61caa61dfa4426b4acf53a05a816dd0dc1fbaa8b60843ff3c8248cd27d8367f7"
)
REQUEST_BYTE_LENGTH = 4828

SUPERSEDED_REQUEST_SHA256 = (
    "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
)

NEXT_GATE = (
    "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "explicit_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization"
)


class Pair06V8ReceiptBoundRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ReceiptBoundRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        request
        .pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_contract()
    )
    proposal = out.get("request")
    _require(isinstance(proposal, dict), "receipt-bound request missing")
    _require(
        proposal.get("record_kind") == "proposal_only_not_authorization",
        "receipt-bound request is not proposal-only",
    )
    lineage = proposal.get("repair_lineage")
    _require(isinstance(lineage, dict), "receipt-bound lineage missing")
    _require(
        lineage.get("held_superseded_request_sha256") == SUPERSEDED_REQUEST_SHA256,
        "superseded request identity drift",
    )
    _require(
        lineage.get("held_superseded_request_authorized") is True
        and lineage.get("held_superseded_request_preclaim") is True
        and lineage.get("held_superseded_request_attempt_consumed") is False
        and lineage.get("held_superseded_request_reusable") is False,
        "superseded request state drift",
    )
    _require(
        lineage.get("held_superseded_request_supersede_reason")
        == "no_offload_parent_receipt_schema_vs_invocation_validator_mismatch",
        "superseded request reason drift",
    )
    _require(
        lineage.get("no_offload_parent_receipt_schema_bound") is True
        and lineage.get("inference_safe_placement_receipt_required") is True,
        "receipt binding invariant missing",
    )
    _require(
        lineage.get("both_failed_attempts_archived") is True
        and lineage.get("fresh_attempt_required") is True,
        "archive/fresh-attempt lineage drift",
    )
    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "receipt-bound request digest drift",
    )
    _require(
        out.get("request_byte_length") == REQUEST_BYTE_LENGTH,
        "receipt-bound request byte length drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "receipt-bound request digest unexpectedly grants authority",
    )
    authority = out.get("authority")
    _require(
        isinstance(authority, dict)
        and authority
        and all(value is False for value in authority.values()),
        "receipt-bound request authority drift",
    )
    _require(out.get("next_gate") == NEXT_GATE, "receipt-bound request frontier drift")
    return deepcopy(out)


def pair06_v8_no_offload_receipt_bound_request_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "request_bytes_sha256": REQUEST_BYTES_SHA256,
        "request_byte_length": REQUEST_BYTE_LENGTH,
        "pair06_v8_no_offload_receipt_bound_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "superseded_request_sha256": SUPERSEDED_REQUEST_SHA256,
        "superseded_request_attempt_consumed": False,
        "superseded_request_reusable": False,
        "no_offload_parent_receipt_schema_bound": True,
        "inference_safe_placement_receipt_required": True,
        "matching_request_digest_grants_authority": False,
        "pair06_no_offload_baseline_specific_authorization_accepted": False,
        "pair06_no_offload_baseline_execution_authorized": False,
        "pair06_no_offload_baseline_execution_performed": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ReceiptBoundRequestReviewHold(NEXT_GATE)
