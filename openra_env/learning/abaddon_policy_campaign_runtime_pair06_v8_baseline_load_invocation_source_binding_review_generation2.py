"""Source-only review of the one-shot pair-06 baseline V8 load invocation.

This review pins the exact invocation source and tests and confirms that
contract inspection remains inert. It grants no additional runtime authority
and performs no host observation, model load, inference, or game execution.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_invocation_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-load-invocation-source-binding-review-contract.v1"
)

INVOCATION_GIT_BLOB = "fde5a7c1c0f9ccb5823e9d86af84074218587df7"
INVOCATION_SOURCE_SHA256 = (
    "864e830cf2d62d3776321b75665f07b58f0b548d6a3dc114b0b9cd84eb9a2ea4"
)
INVOCATION_TEST_GIT_BLOB = "69abde74130d557b4071d006381f962eb3b751aa"
INVOCATION_TEST_SHA256 = (
    "62d3d6408cf630865626d60c1c8e232c9a420b3d570a03622b333109b85a3ff4"
)

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LOAD_PRECISION_EXECUTION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_baseline_runtime_load_precision_execution"


class Pair06V8BaselineLoadInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_invocation_cached() -> dict[str, Any]:
    contract = invocation.pair06_v8_baseline_load_invocation_contract()

    _require(
        contract.get("pair06_v8_baseline_load_invocation_implemented") is True,
        "pair06 baseline load invocation missing",
    )
    _require(
        contract.get("pair06_v8_baseline_load_invocation_reviewed") is False,
        "pair06 baseline load invocation unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 invocation slot drift")
    _require(contract.get("arm") == "baseline", "pair06 invocation arm drift")
    _require(contract.get("held_out") is False, "pair06 invocation became held-out")
    _require(
        contract.get("runtime_load_authorized_by_reviewed_dependency") is True,
        "pair06 invocation reviewed authorization dependency missing",
    )

    for field in (
        "explicit_authorization_boolean_required",
        "explicit_confirmation_token_required",
        "exact_current_main_required",
        "exact_invocation_source_sha256_required",
        "designated_python_required",
        "fresh_runtime_environment_verification_required",
        "runtime_asset_hash_verification_required",
        "offline_only_model_load_required",
        "revocation_check_required_before_claim",
        "revocation_check_required_after_claim",
        "single_use_attempt_consumption_required",
    ):
        _require(contract.get(field) is True, f"pair06 invocation gate drift: {field}")

    _require(
        contract.get("single_use_attempt_consumed") is False,
        "pair06 invocation contract inspection consumed attempt",
    )
    _require(
        contract.get("automatic_retry") is False,
        "pair06 invocation automatic retry enabled",
    )
    _require(
        contract.get("runtime_load_performed") is False
        and contract.get("model_weights_loaded") is False,
        "pair06 invocation contract inspection performed load",
    )

    for field in (
        "candidate_runtime_load_authorized",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
        "game_execution_performed",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 invocation scope drift: {field}")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 invocation review frontier drift",
    )

    dependencies = contract.get("dependencies")
    _require(isinstance(dependencies, dict), "pair06 invocation dependencies missing")
    authorization = dependencies.get("authorization_review")
    capability = dependencies.get("capability_review")
    _require(
        isinstance(authorization, dict)
        and authorization.get("runtime_load_authorized") is True
        and authorization.get("maximum_runtime_load_attempts") == 1
        and authorization.get("automatic_retry") is False,
        "pair06 invocation authorization dependency drift",
    )
    _require(
        isinstance(capability, dict)
        and capability.get("pair06_v8_runtime_capability_reviewed") is True
        and capability.get("runtime_loader_callable_bound") is True,
        "pair06 invocation capability dependency drift",
    )
    return deepcopy(contract)


def pair06_v8_baseline_load_invocation_review_contract() -> dict[str, Any]:
    reviewed = _validate_invocation_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "separate_review_instrument": True,
        "invocation_source_identity_pinned_by_git_blob": True,
        "invocation_source_identity_pinned_by_sha256": True,
        "invocation_test_identity_pinned_by_git_blob": True,
        "invocation_test_identity_pinned_by_sha256": True,
        "pair06_v8_baseline_load_invocation_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "runtime_load_authorized_by_reviewed_dependency": True,
        "explicit_authorization_boolean_required": True,
        "explicit_confirmation_token_required": True,
        "exact_current_main_required": True,
        "exact_invocation_source_sha256_required": True,
        "designated_python_required": True,
        "fresh_runtime_environment_verification_required": True,
        "runtime_asset_hash_verification_required": True,
        "offline_only_model_load_required": True,
        "revocation_check_required_before_claim": True,
        "revocation_check_required_after_claim": True,
        "single_use_attempt_consumption_required": True,
        "single_use_attempt_consumed": False,
        "automatic_retry": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "candidate_runtime_load_authorized": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_invocation": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadInvocationReviewHold(NEXT_GATE)


def execute_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadInvocationReviewHold(
        "PAIR06_V8_GAME_EXECUTION_NOT_AUTHORIZED"
    )
