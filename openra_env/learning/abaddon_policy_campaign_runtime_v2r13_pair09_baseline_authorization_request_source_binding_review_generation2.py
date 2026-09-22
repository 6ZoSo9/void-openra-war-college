"""Source-only review of the fixed V2R13 pair-09 baseline authorization request.

This instrument pins the exact request source and tests and verifies that the
request is proposal-only. Exact bytes, a matching digest, historical pair-03
authority, or the legacy six-arm capability never grant execution authority.

The next gate remains explicit pair-09 baseline execution authorization.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-authorization-request-source-binding-review-contract.v1"
)

REQUEST_GIT_BLOB = "8d49f5fbc73c574884e1e262eb929395551b6419"
REQUEST_SOURCE_SHA256 = (
    "cc0d6f16227528ddee9e65903b10c579180ffbdae6567a229919400f6476daa0"
)
REQUEST_TEST_GIT_BLOB = "3983bd11da5f3428d87461962c7d4ba194e7e22b"
REQUEST_TEST_SHA256 = (
    "73d96d6714ebe706054cd7cb3befc9466028f14500409e54edb0db2f92c3c5c1"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_v2r13_pair09_baseline_execution_authorization"


class V2R13Pair09BaselineAuthorizationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineAuthorizationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validate_request_cached() -> dict[str, Any]:
    contract = request.pair09_baseline_authorization_request_contract()
    record = contract.get("request")
    _require(isinstance(record, dict), "authorization request record missing")

    _require(contract.get("request_bytes_valid") is True, "request bytes not validated")
    _require(
        contract.get("next_gate") == NEXT_GATE,
        "request validation frontier drift",
    )
    _require(
        record.get("record_kind") == "proposal_only_not_authorization",
        "request unexpectedly claims authority",
    )
    _require(
        record.get("proposed_scope")
        == {
            "pair_slot": 9,
            "arm": "baseline",
            "held_out": False,
            "maximum_baseline_attempts": 1,
            "maximum_automatic_retries": 0,
            "candidate_arm_included": False,
            "held_out_arm_included": False,
            "pair03_replay_included": False,
        },
        "request scope drift",
    )
    _require(
        record.get("evaluation_order")
        == {
            "baseline_first": True,
            "candidate_must_wait_for_baseline_result_review": True,
        },
        "request evaluation order drift",
    )
    _require(
        record.get("runtime_reference")
        == {"selection_key": "apollyon-v2r13-qualified-predecessor"},
        "request runtime reference drift",
    )
    _require(
        tuple(record.get("required_runtime_gates", ()))
        == request.REQUIRED_RUNTIME_GATES,
        "required runtime gate set drift",
    )
    _require(
        record.get("historical_pair03_runtime_authority_sufficient") is False,
        "historical pair03 authority became sufficient",
    )
    _require(
        record.get("legacy_six_arm_authorization_sufficient") is False,
        "legacy six-arm authority became sufficient",
    )
    _require(
        record.get("matching_request_digest_grants_authority") is False,
        "matching digest unexpectedly grants authority",
    )
    _require(
        record.get("runtime_gates_enforced_by_this_module") is False,
        "request module unexpectedly enforces runtime gates",
    )
    _require(
        record.get("next_gate") == NEXT_GATE,
        "request record frontier drift",
    )

    authority = record.get("authority")
    _require(isinstance(authority, dict) and authority, "request authority map missing")
    _require(
        set(authority) == set(request.FALSE_AUTHORITY_FIELDS),
        "request authority field set drift",
    )
    _require(
        all(value is False for value in authority.values()),
        "request carries non-false authority",
    )
    validated_authority = contract.get("authority")
    _require(
        isinstance(validated_authority, dict)
        and set(validated_authority) == set(request.FALSE_AUTHORITY_FIELDS)
        and all(value is False for value in validated_authority.values()),
        "validated request authority drift",
    )

    return deepcopy(contract)


def v2r13_pair09_baseline_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validate_request_cached()
    request_record = validated["request"]
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "separate_review_instrument": True,
        "request_source_identity_pinned_by_git_blob": True,
        "request_source_identity_pinned_by_sha256": True,
        "request_test_identity_pinned_by_git_blob": True,
        "request_test_identity_pinned_by_sha256": True,
        "pair09_baseline_authorization_request_reviewed": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "maximum_baseline_attempts": 1,
        "maximum_automatic_retries": 0,
        "proposal_only_not_authorization": True,
        "matching_request_digest_grants_authority": False,
        "historical_pair03_runtime_authority_sufficient": False,
        "legacy_six_arm_authorization_sufficient": False,
        "pair09_baseline_specific_authorization_accepted": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "pair09_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "operator_authenticated": False,
        "source_inventory_verified": False,
        "runtime_readiness_verified": False,
        "authorization_consumption_implemented": False,
        "authorization_consumed": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "required_runtime_gates": tuple(request_record["required_runtime_gates"]),
        "validated_request": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineAuthorizationRequestReviewHold(NEXT_GATE)
