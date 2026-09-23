"""Source-only review of the pair-06 baseline V8 runtime-load authorization request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-load-authorization-request-source-binding-review-contract.v1"
)

REQUEST_GIT_BLOB = "9c0dd9c22c56dcc9656fda6d860420dff0653cff"
REQUEST_SOURCE_SHA256 = (
    "6bd28bbaaad3f6deb779ce8e6e1b85ebf9afba4f5053dff3547a7c27e5565ddd"
)
REQUEST_TEST_GIT_BLOB = "ed6d4b5f5558c10a9934ad623a8125ba2a5d8509"
REQUEST_TEST_SHA256 = (
    "a0aaf7d9d52e55b2569efeb7f4b842318ab9d53cb2c3174ccfc4a35548e506c8"
)

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "human_pair06_v8_baseline_runtime_load_authorization"


class Pair06V8BaselineLoadAuthorizationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadAuthorizationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validate_request_cached() -> dict[str, Any]:
    contract = request.pair06_v8_baseline_load_authorization_request_contract()

    _require(
        contract.get("runtime_load_authorization_request_implemented") is True,
        "pair06 baseline V8 load request missing",
    )
    _require(
        contract.get("runtime_load_authorization_request_reviewed") is False,
        "pair06 baseline V8 load request unexpectedly self-reviewed",
    )
    _require(
        contract.get("runtime_load_authorization_requested") is True,
        "pair06 baseline V8 load authority not requested",
    )
    _require(
        contract.get("runtime_load_authorized") is False,
        "pair06 baseline V8 load prematurely authorized",
    )
    _require(
        contract.get("runtime_load_performed") is False,
        "pair06 baseline V8 load already performed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 load request slot drift")
    _require(contract.get("arm") == "baseline", "pair06 load request arm drift")
    _require(contract.get("held_out") is False, "pair06 load request became held-out")
    _require(contract.get("baseline_first") is True, "pair06 baseline-first boundary missing")
    _require(
        contract.get("candidate_runtime_load_requested") is False
        and contract.get("candidate_runtime_load_authorized") is False,
        "pair06 candidate load authority leaked",
    )
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution prematurely authorized",
    )
    _require(
        contract.get("runtime_selection_key")
        == "apollyon-v3-v8-accepted-model-control",
        "pair06 runtime selection drift",
    )
    _require(
        contract.get("activation_kind") == "inprocess_accepted_v8_runtime",
        "pair06 activation-kind drift",
    )
    _require(
        contract.get("model_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model",
        "pair06 model-dir drift",
    )
    _require(
        contract.get("adapter_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8",
        "pair06 adapter-dir drift",
    )
    _require(
        contract.get("python_path")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12",
        "pair06 Python-path drift",
    )
    _require(
        tuple(contract.get("python_major_minor", ())) == (3, 12),
        "pair06 Python version drift",
    )
    _require(
        contract.get("pip_freeze_sha256")
        == "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77",
        "pair06 pip-freeze drift",
    )
    _require(
        contract.get("exact_17_asset_verification_reviewed") is True
        and contract.get("runtime_environment_observation_reviewed") is True
        and contract.get("runtime_environment_admitted") is True
        and contract.get("runtime_environment_path_bound") is True,
        "pair06 reviewed preload prerequisites incomplete",
    )
    _require(contract.get("automatic_retry") is False, "pair06 automatic retry enabled")
    for field in (
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "game_mutation_performed",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 load request authority drift: {field}")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED",
        "pair06 baseline load authorization frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_baseline_load_authorization_request_review_contract() -> dict[str, Any]:
    reviewed = _validate_request_cached()
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
        "pair06_v8_baseline_load_authorization_request_reviewed": True,
        "runtime_load_authorization_requested": True,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "baseline_first": True,
        "candidate_runtime_load_requested": False,
        "candidate_runtime_load_authorized": False,
        "pair15_execution_authorized": False,
        "model_dir": reviewed["model_dir"],
        "adapter_dir": reviewed["adapter_dir"],
        "python_path": reviewed["python_path"],
        "python_major_minor": (3, 12),
        "pip_freeze_sha256": reviewed["pip_freeze_sha256"],
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_request": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationRequestReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationRequestReviewHold(
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
