"""Source-only acceptance of one pair-06 baseline V8 runtime-load authorization.

The operator explicitly instructed the War College control session to continue
after the reviewed authorization-request PR stack was green. This module records
that instruction as a repository attestation for exactly one pair-06 BASELINE
V8 model-load attempt.

This is deliberately narrower than game execution:
* candidate runtime load is not authorized;
* held-out pair 15 remains closed;
* no inference or game execution is authorized;
* no training, weight update, promotion, deployment, VOID-chain mutation, or
  wallet/funds action is authorized;
* zero automatic retries are authorized.

Import and contract inspection perform no host I/O and do not load model
weights.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from functools import lru_cache
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-load-authorization-acceptance-contract.v1"
)

REQUEST_REVIEW_GIT_BLOB = "0b728390d7266be8d6081ab0e5589fd1e3236bfe"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "42e7ffe8d67e4a99bc7ad18a8332a61931706d11d05b24cf918420f93d12d6c8"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
AUTHORIZATION_SCOPE = "single_pair06_baseline_v8_runtime_load"
MAX_RUNTIME_LOAD_ATTEMPTS = 1

AUTHORIZATION_ATTESTATION = {
    "authorization_basis": "explicit_operator_continue_instruction_in_control_session",
    "authorization_date": "2026-09-23",
    "authorization_granted": True,
    "authorization_scope": AUTHORIZATION_SCOPE,
    "pair_slot": PAIR_SLOT,
    "arm": ARM,
    "held_out": HELD_OUT,
    "maximum_runtime_load_attempts": MAX_RUNTIME_LOAD_ATTEMPTS,
    "maximum_automatic_retries": 0,
    "candidate_runtime_load_authorized": False,
    "pair15_execution_authorized": False,
    "game_execution_authorized": False,
    "training_authorized": False,
    "weights_update_authorized": False,
    "automatic_policy_promotion_authorized": False,
    "deployment_authorized": False,
    "void_chain_mutation_authorized": False,
    "wallet_or_funds_action_authorized": False,
    "cryptographic_operator_signature_present": False,
    "repository_authorization_attestation": True,
}

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_runtime_load_invocation"


class Pair06V8BaselineLoadAuthorizationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadAuthorizationAcceptanceHold(message)


def _digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        dict(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@lru_cache(maxsize=1)
def _request_review_cached() -> dict[str, Any]:
    contract = (
        request_review
        .pair06_v8_baseline_load_authorization_request_review_contract()
    )
    _require(
        contract.get("pair06_v8_baseline_load_authorization_request_reviewed")
        is True,
        "pair06 baseline load authorization request not reviewed",
    )
    _require(
        contract.get("runtime_load_authorization_requested") is True,
        "pair06 baseline load authority not requested",
    )
    _require(
        contract.get("runtime_load_authorized") is False,
        "pair06 baseline load request unexpectedly self-authorized",
    )
    _require(
        contract.get("runtime_load_performed") is False,
        "pair06 baseline load request already performed",
    )
    _require(contract.get("pair_slot") == PAIR_SLOT, "pair06 authorization slot drift")
    _require(contract.get("arm") == ARM, "pair06 authorization arm drift")
    _require(contract.get("held_out") is False, "pair06 authorization became held-out")
    _require(contract.get("baseline_first") is True, "pair06 baseline-first boundary missing")
    _require(
        contract.get("candidate_runtime_load_authorized") is False,
        "pair06 candidate load authority leaked",
    )
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution authority leaked",
    )
    _require(
        contract.get("automatic_retry") is False,
        "pair06 automatic retry unexpectedly enabled",
    )
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED",
        "pair06 authorization-request frontier drift",
    )
    return deepcopy(contract)


def _validate_authorization(value: Mapping[str, Any]) -> dict[str, Any]:
    _require(isinstance(value, Mapping), "authorization must be object")
    supplied = dict(value)
    _require(
        set(supplied) == set(AUTHORIZATION_ATTESTATION),
        "authorization field-set drift",
    )
    for field, expected in AUTHORIZATION_ATTESTATION.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"authorization drift: {field}",
        )
    return deepcopy(supplied)


def accept_pair06_v8_baseline_load_authorization(
    authorization: Mapping[str, Any],
) -> dict[str, Any]:
    reviewed = _request_review_cached()
    accepted = _validate_authorization(authorization)
    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "authorization_accepted": True,
        "authorization": accepted,
        "authorization_attestation_sha256": _digest(accepted),
        "authorization_repository_attestation": True,
        "authorization_cryptographic_proof": False,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "baseline_first": True,
        "runtime_load_authorized": True,
        "maximum_runtime_load_attempts": MAX_RUNTIME_LOAD_ATTEMPTS,
        "automatic_retry": False,
        "load_attempt_consumption_required": True,
        "create_only_load_attempt_marker_required": True,
        "runtime_load_invocation_implemented": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "fresh_runtime_environment_verification_required_before_load": True,
        "runtime_asset_hash_verification_required_before_load": True,
        "offline_only_model_load_required": True,
        "authority_callback_required_at_load": True,
        "candidate_runtime_load_authorized": False,
        "pair15_execution_authorized": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "reviewed_request": deepcopy(reviewed),
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def pair06_v8_baseline_load_authorization_acceptance_contract() -> dict[str, Any]:
    return accept_pair06_v8_baseline_load_authorization(AUTHORIZATION_ATTESTATION)


def invoke_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationAcceptanceHold(NEXT_GATE)


def authorize_candidate_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationAcceptanceHold(
        "PAIR06_V8_CANDIDATE_RUNTIME_LOAD_NOT_AUTHORIZED"
    )


def execute_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationAcceptanceHold(
        "PAIR06_V8_GAME_EXECUTION_NOT_AUTHORIZED"
    )
