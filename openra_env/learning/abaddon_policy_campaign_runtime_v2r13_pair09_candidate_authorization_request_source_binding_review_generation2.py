"""Source-only review of the fixed V2R13 pair-09 candidate request.

This review pins the exact request source and tests and verifies that the request
remains proposal-only. It grants no candidate execution authority and performs
no host, runtime, model, game, training, deployment, VOID-chain, wallet, or
funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-authorization-request-review-contract.v1"
)

REQUEST_GIT_BLOB = "f58ca2f133e2366092c103c339f622d5198ed4c3"
REQUEST_SOURCE_SHA256 = (
    "f612b365eae1b3df000c2beb790db9617efa4f20bca2e59694a01c9aedba724d"
)
REQUEST_TEST_GIT_BLOB = "fe8873a7557d14b68998a91a87f685a800201458"
REQUEST_TEST_SHA256 = (
    "6c25f720eeb5f2c58ffd67a5b5772058fdba82c5fa5e1c8826b31b8f442911be"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_v2r13_pair09_candidate_execution_authorization"


class V2R13Pair09CandidateAuthorizationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateAuthorizationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validate_request_cached() -> dict[str, Any]:
    contract = request.pair09_candidate_authorization_request_contract()
    record = contract.get("request")
    _require(isinstance(record, dict), "candidate request record missing")
    _require(contract.get("request_bytes_valid") is True, "candidate request bytes invalid")
    _require(contract.get("next_gate") == NEXT_GATE, "candidate request frontier drift")
    _require(
        record.get("record_kind") == "proposal_only_not_authorization",
        "candidate request unexpectedly claims authority",
    )
    _require(
        record.get("proposed_scope")
        == {
            "pair_slot": 9,
            "arm": "candidate",
            "held_out": False,
            "maximum_candidate_attempts": 1,
            "maximum_automatic_retries": 0,
            "baseline_rerun_included": False,
            "held_out_arm_included": False,
            "other_pair_slots_included": False,
        },
        "candidate request scope drift",
    )

    baseline = record.get("baseline_reference")
    _require(isinstance(baseline, dict), "baseline reference missing")
    _require(baseline.get("seed") == 1496195137, "baseline seed drift")
    _require(baseline.get("round_limit") == 36, "baseline round limit drift")
    _require(
        baseline.get("trajectory_sha256")
        == "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700",
        "baseline trajectory drift",
    )
    _require(
        baseline.get("summary_sha256")
        == "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189",
        "baseline summary drift",
    )
    _require(
        baseline.get("result_file_sha256")
        == "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2",
        "baseline result-file drift",
    )

    candidate = record.get("candidate_reference")
    _require(isinstance(candidate, dict), "candidate reference missing")
    _require(
        candidate.get("wrapper_sha256")
        == "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f",
        "candidate wrapper drift",
    )
    _require(
        candidate.get("fixture_sha256")
        == "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768",
        "candidate fixture drift",
    )
    _require(
        candidate.get("semantic_genome_sha256")
        == "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089",
        "candidate genome drift",
    )

    _require(
        tuple(record.get("required_runtime_gates", ()))
        == request.REQUIRED_RUNTIME_GATES,
        "candidate runtime gate set drift",
    )
    _require(
        record.get("legacy_six_arm_authorization_sufficient") is False,
        "legacy authority became sufficient",
    )
    _require(
        record.get("matching_request_digest_grants_authority") is False,
        "matching digest unexpectedly grants authority",
    )
    _require(
        record.get("runtime_gates_enforced_by_this_module") is False,
        "request unexpectedly enforces runtime gates",
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


def v2r13_pair09_candidate_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validate_request_cached()
    record = validated["request"]
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "separate_review_instrument": True,
        "pair09_candidate_authorization_request_reviewed": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "maximum_candidate_attempts": 1,
        "maximum_automatic_retries": 0,
        "proposal_only_not_authorization": True,
        "baseline_rerun_included": False,
        "matching_request_digest_grants_authority": False,
        "legacy_six_arm_authorization_sufficient": False,
        "pair09_candidate_specific_authorization_accepted": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_candidate_execution_performed": False,
        "pair09_candidate_invocation_implemented": False,
        "pair09_candidate_invocation_reviewed": False,
        "operator_authenticated": False,
        "source_inventory_verified": False,
        "baseline_evidence_bytes_verified": False,
        "runtime_readiness_verified": False,
        "authorization_consumption_implemented": False,
        "authorization_consumed": False,
        "pair09_baseline_rerun_authorized": False,
        "held_out_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "required_runtime_gates": tuple(record["required_runtime_gates"]),
        "validated_request": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateAuthorizationRequestReviewHold(NEXT_GATE)
