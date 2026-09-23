"""Source-only review of the pair-06 baseline V8 load-authorization acceptance."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_acceptance_generation2
    as authorization,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-load-authorization-acceptance-source-binding-review-contract.v1"
)

AUTHORIZATION_GIT_BLOB = "ba76fec2e9bd2ba48000c9ed832c357f619d19bc"
AUTHORIZATION_SOURCE_SHA256 = (
    "ff6281e0491bc64d29999e8b6dbe9ebdd8ddad70ba44fb030a9b3734656c8452"
)
AUTHORIZATION_TEST_GIT_BLOB = "2582a4acaef9f41fb2e418f3a25376ee9d2fb70e"
AUTHORIZATION_TEST_SHA256 = (
    "6491677e888087d509b3525ca166a697abbccd9556660f91bd2b110263541dac"
)

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_runtime_load_invocation"


class Pair06V8BaselineLoadAuthorizationAcceptanceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadAuthorizationAcceptanceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_authorization_cached() -> dict[str, Any]:
    contract = (
        authorization
        .pair06_v8_baseline_load_authorization_acceptance_contract()
    )
    _require(
        contract.get("request_review_git_blob")
        == "0b728390d7266be8d6081ab0e5589fd1e3236bfe",
        "pair06 request-review git identity drift",
    )
    _require(
        contract.get("request_review_source_sha256")
        == "42e7ffe8d67e4a99bc7ad18a8332a61931706d11d05b24cf918420f93d12d6c8",
        "pair06 request-review source identity drift",
    )
    _require(
        contract.get("authorization_accepted") is True,
        "pair06 baseline load authorization not accepted",
    )
    _require(
        contract.get("authorization_repository_attestation") is True,
        "pair06 repository authorization attestation missing",
    )
    _require(
        contract.get("authorization_cryptographic_proof") is False,
        "pair06 authorization unexpectedly claims cryptographic proof",
    )
    _require(
        contract.get("authorization_scope")
        == "single_pair06_baseline_v8_runtime_load",
        "pair06 authorization scope drift",
    )
    _require(contract.get("pair_slot") == 6, "pair06 authorization slot drift")
    _require(contract.get("arm") == "baseline", "pair06 authorization arm drift")
    _require(contract.get("held_out") is False, "pair06 authorization became held-out")
    _require(contract.get("baseline_first") is True, "pair06 baseline-first boundary missing")
    _require(
        contract.get("runtime_load_authorized") is True,
        "pair06 baseline runtime load not authorized",
    )
    _require(
        contract.get("maximum_runtime_load_attempts") == 1,
        "pair06 load-attempt bound drift",
    )
    _require(contract.get("automatic_retry") is False, "pair06 automatic retry enabled")
    _require(
        contract.get("load_attempt_consumption_required") is True
        and contract.get("create_only_load_attempt_marker_required") is True,
        "pair06 single-use load-attempt consumption missing",
    )
    _require(
        contract.get("runtime_load_invocation_implemented") is False
        and contract.get("runtime_load_performed") is False
        and contract.get("model_weights_loaded") is False,
        "pair06 authorization acceptance executed or implemented load",
    )
    _require(
        contract.get("fresh_runtime_environment_verification_required_before_load") is True
        and contract.get("runtime_asset_hash_verification_required_before_load") is True
        and contract.get("offline_only_model_load_required") is True
        and contract.get("authority_callback_required_at_load") is True,
        "pair06 preload safety boundary drift",
    )
    for field in (
        "candidate_runtime_load_authorized",
        "pair15_execution_authorized",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
        "game_execution_performed",
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        _require(contract.get(field) is False, f"pair06 authorization scope drift: {field}")
    _require(
        contract.get("next_gate") == NEXT_GATE,
        "pair06 authorization acceptance frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_baseline_load_authorization_acceptance_review_contract() -> dict[str, Any]:
    accepted = _validate_authorization_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_git_blob": AUTHORIZATION_GIT_BLOB,
        "authorization_source_sha256": AUTHORIZATION_SOURCE_SHA256,
        "authorization_test_git_blob": AUTHORIZATION_TEST_GIT_BLOB,
        "authorization_test_sha256": AUTHORIZATION_TEST_SHA256,
        "separate_review_instrument": True,
        "authorization_source_identity_pinned_by_git_blob": True,
        "authorization_source_identity_pinned_by_sha256": True,
        "authorization_test_identity_pinned_by_git_blob": True,
        "authorization_test_identity_pinned_by_sha256": True,
        "pair06_v8_baseline_load_authorization_acceptance_reviewed": True,
        "authorization_accepted": True,
        "authorization_scope": accepted["authorization_scope"],
        "authorization_attestation_sha256": accepted[
            "authorization_attestation_sha256"
        ],
        "authorization_repository_attestation": True,
        "authorization_cryptographic_proof": False,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "baseline_first": True,
        "runtime_load_authorized": True,
        "maximum_runtime_load_attempts": 1,
        "automatic_retry": False,
        "load_attempt_consumption_required": True,
        "create_only_load_attempt_marker_required": True,
        "runtime_load_invocation_implemented": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "candidate_runtime_load_authorized": False,
        "pair15_execution_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_authorization": deepcopy(accepted),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def invoke_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationAcceptanceReviewHold(NEXT_GATE)


def authorize_candidate_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationAcceptanceReviewHold(
        "PAIR06_V8_CANDIDATE_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
