"""Source-only review of repaired pair-06 V8 baseline execution request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_repaired_baseline_execution_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-repaired-baseline-execution-authorization-request-review-contract.v1"
)

REQUEST_GIT_BLOB = "9cb4b07ae31142005ddc202e02b6fbf397fcb9a5"
REQUEST_SOURCE_SHA256 = (
    "3a9548eda5a25cdab6183c265a4492aa0d18a39ce39013b0016210c5a83916b3"
)
REQUEST_TEST_GIT_BLOB = "36b7f78c0edc6a5c02da025532a08813c0057096"
REQUEST_TEST_SHA256 = (
    "9be522fe7a687bc9d65094d3657557e5de15f62c722824cd79299a5fe55c52db"
)
REQUEST_BYTES_SHA256 = "31c0069869915eb01221d7ea0aa867c0517df0a702eeff58ca69f70dec07a410"

NEXT_GATE = "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "explicit_pair06_v8_repaired_baseline_execution_authorization"


class Pair06V8RepairedBaselineExecutionAuthorizationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8RepairedBaselineExecutionAuthorizationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.pair06_v8_repaired_baseline_execution_authorization_request_contract()
    proposal = out.get("request")
    _require(isinstance(proposal, dict), "repaired pair06 request missing")
    _require(
        proposal.get("record_kind") == "proposal_only_not_authorization",
        "repaired pair06 request is not proposal-only",
    )
    lineage = proposal.get("repair_lineage")
    _require(isinstance(lineage, dict), "repaired pair06 lineage missing")
    _require(
        lineage.get("spent_request_sha256")
        == "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae",
        "spent request identity drift",
    )
    _require(
        lineage.get("spent_attempt_marker_sha256")
        == "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930",
        "spent attempt identity drift",
    )
    _require(lineage.get("spent_attempt_reusable") is False, "spent attempt became reusable")
    _require(lineage.get("failed_attempt_archived") is True, "spent attempt archive missing")
    _require(
        lineage.get("offload_safe_generate_binding_required") is True,
        "offload-safe binding requirement missing",
    )
    _require(
        lineage.get("hard_coded_cuda_input_transfer_allowed") is False,
        "hard-coded CUDA transfer unexpectedly allowed",
    )
    _require(lineage.get("fresh_attempt_required") is True, "fresh attempt requirement missing")

    scope = proposal.get("proposed_scope")
    _require(isinstance(scope, dict), "repaired pair06 scope missing")
    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False,
        "repaired pair06 scope drift",
    )
    _require(
        scope.get("maximum_attempts") == 1
        and scope.get("maximum_automatic_retries") == 0,
        "repaired pair06 cardinality drift",
    )
    _require(
        out.get("spent_request_reusable") is False
        and out.get("spent_attempt_reusable") is False,
        "spent request or attempt became reusable",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "repaired request digest unexpectedly grants authority",
    )
    _require(
        out.get("pair06_repaired_baseline_specific_authorization_accepted") is False
        and out.get("pair06_repaired_baseline_execution_authorized") is False
        and out.get("pair06_repaired_baseline_execution_performed") is False,
        "repaired pair06 request prematurely authorizes execution",
    )
    authority = out.get("authority")
    _require(
        isinstance(authority, dict)
        and authority
        and all(value is False for value in authority.values()),
        "repaired pair06 authority map drift",
    )
    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "repaired pair06 request byte digest drift",
    )
    _require(out.get("next_gate") == NEXT_GATE, "repaired pair06 next gate drift")
    return deepcopy(out)


def pair06_v8_repaired_baseline_execution_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "request_bytes_sha256": REQUEST_BYTES_SHA256,
        "pair06_v8_repaired_baseline_execution_authorization_request_source_binding_present": True,
        "pair06_v8_repaired_baseline_execution_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "request_byte_length": validated["request_byte_length"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "spent_request_reusable": False,
        "spent_attempt_reusable": False,
        "offload_safe_generate_binding_required": True,
        "matching_request_digest_grants_authority": False,
        "pair06_repaired_baseline_specific_authorization_accepted": False,
        "pair06_repaired_baseline_execution_authorized": False,
        "pair06_repaired_baseline_execution_performed": False,
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
    raise Pair06V8RepairedBaselineExecutionAuthorizationRequestReviewHold(NEXT_GATE)
