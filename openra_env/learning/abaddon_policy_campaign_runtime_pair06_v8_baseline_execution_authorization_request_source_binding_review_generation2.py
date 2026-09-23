"""Source-only review of the fixed pair-06 V8 baseline execution request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_execution_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-execution-authorization-request-review-contract.v1"
)

REQUEST_GIT_BLOB = "c68d79a9210259d6cc54373f2b3ba7eeffdb037d"
REQUEST_SOURCE_SHA256 = (
    "3aefebee23de9cf02ade3327d00b6b64021dc9b01f492efebe5b77534a421a31"
)
REQUEST_TEST_GIT_BLOB = "595382831314c8e4a920fe1db569b6e897ba8dee"
REQUEST_TEST_SHA256 = (
    "562bb8438887a2320a5822c777f2ac3389695f5d0fe8ae53f44623baf2c1979b"
)

NEXT_GATE = "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "explicit_pair06_v8_baseline_execution_authorization"


class Pair06V8BaselineExecutionAuthorizationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineExecutionAuthorizationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validate_cached() -> dict[str, Any]:
    contract = request.pair06_v8_baseline_execution_authorization_request_contract()
    proposal = contract.get("request")
    _require(isinstance(proposal, dict), "pair06 authorization request missing")
    _require(
        proposal.get("record_kind") == "proposal_only_not_authorization",
        "pair06 request is not proposal-only",
    )

    scope = proposal.get("proposed_scope")
    _require(isinstance(scope, dict), "pair06 proposed scope missing")
    expected = {
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
        "candidate_arm_included": False,
        "held_out_pair15_included": False,
        "pair03_replay_included": False,
        "pair09_replay_included": False,
    }
    _require(scope == expected, "pair06 proposed scope drift")

    architecture = proposal.get("runtime_architecture")
    _require(isinstance(architecture, dict), "pair06 runtime architecture missing")
    for field in (
        "v8_parent_process",
        "proto_grpc_game_child_process",
        "separate_virtualenv_site_packages_preserved",
        "inherited_unix_socketpair_only",
        "private_child_process_group",
    ):
        _require(architecture.get(field) is True, f"pair06 runtime architecture drift: {field}")
    _require(
        architecture.get("legacy_ollama_started") is False
        and architecture.get("legacy_ollama_contacted") is False,
        "pair06 legacy Ollama boundary drift",
    )

    evidence = proposal.get("evidence_order")
    _require(isinstance(evidence, dict), "pair06 evidence ordering missing")
    for field in (
        "preclaim_preparation_first",
        "durable_attempt_marker_before_model_load_or_child_spawn",
        "durable_execution_result_before_worktree_cleanup",
        "durable_cleanup_closeout_after_successful_cleanup",
        "runs_preserved",
    ):
        _require(evidence.get(field) is True, f"pair06 evidence order drift: {field}")

    _require(
        contract.get("matching_request_digest_grants_authority") is False,
        "pair06 request digest unexpectedly grants authority",
    )
    _require(
        contract.get("pair06_baseline_specific_authorization_accepted") is False
        and contract.get("pair06_baseline_execution_authorized") is False
        and contract.get("pair06_baseline_execution_performed") is False,
        "pair06 request prematurely authorizes execution",
    )
    authority = contract.get("authority")
    _require(
        isinstance(authority, dict)
        and authority
        and all(value is False for value in authority.values()),
        "pair06 request authority map drift",
    )
    _require(
        contract.get("next_gate") == NEXT_GATE,
        "pair06 request next gate drift",
    )
    return deepcopy(contract)


def pair06_v8_baseline_execution_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validate_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "pair06_v8_baseline_execution_authorization_request_source_binding_present": True,
        "pair06_v8_baseline_execution_authorization_request_reviewed": True,
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
        "matching_request_digest_grants_authority": False,
        "pair06_baseline_specific_authorization_accepted": False,
        "pair06_baseline_execution_authorized": False,
        "pair06_baseline_execution_performed": False,
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
    raise Pair06V8BaselineExecutionAuthorizationRequestReviewHold(NEXT_GATE)
