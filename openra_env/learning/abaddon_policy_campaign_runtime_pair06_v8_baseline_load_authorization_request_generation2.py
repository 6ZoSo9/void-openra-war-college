"""Source-only authorization request for one pair-06 baseline V8 model load.

This request is deliberately non-authorizing. It records the exact reviewed
model, adapter, and Python environment required for pair-06 baseline-first
evaluation and advances only to an explicit human runtime-load authorization
gate.

It does not load model weights, run inference, execute a game, authorize the
candidate arm, touch held-out pair 15, train, promote, deploy, mutate VOID-chain
state, or touch wallets/funds.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_source_binding_review_generation2
    as capability_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_path_binding_source_binding_review_generation2
    as environment_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_source_binding_review_generation2
    as host_path_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-load-authorization-request-contract.v1"
)

ENVIRONMENT_REVIEW_GIT_BLOB = "212ac021820e75bd53938f7df4c8610f51c077f7"
ENVIRONMENT_REVIEW_SOURCE_SHA256 = (
    "851dd76524ac5c5a878a6b7f128a351f0115f76985d626145da3b2d1c67ea77e"
)
HOST_PATH_REVIEW_GIT_BLOB = "c162a8013894ebcb6f310432c96e7daf2c9de3d0"
HOST_PATH_REVIEW_SOURCE_SHA256 = (
    "49c4f44f6f164595fb9c50290b81aa56b62261b4924e859dfd7383a6e84ad07a"
)
CAPABILITY_REVIEW_GIT_BLOB = "8e405b4d03a7a7310dbedd9fae0edbe9976b4637"
CAPABILITY_REVIEW_SOURCE_SHA256 = (
    "5c4836135629ea47e5e38f6aff0bc61201f754b8354152768e9fbf89c5e000fb"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
MODEL_DIR = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
ADAPTER_DIR = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
PYTHON_PATH = (
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
)
PYTHON_MAJOR_MINOR = (3, 12)
PIP_FREEZE_SHA256 = (
    "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
)
RUNTIME_SELECTION_KEY = "apollyon-v3-v8-accepted-model-control"
ACTIVATION_KIND = "inprocess_accepted_v8_runtime"

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "human_pair06_v8_baseline_runtime_load_authorization"


class Pair06V8BaselineLoadAuthorizationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadAuthorizationRequestHold(message)


@lru_cache(maxsize=1)
def _dependencies_cached() -> dict[str, Any]:
    capability = capability_review.pair06_v8_runtime_capability_review_contract()
    environment = environment_review.pair06_v8_environment_path_binding_review_contract()
    host_paths = host_path_review.pair06_v8_host_path_binding_review_contract()

    _require(
        capability.get("pair06_v8_runtime_capability_reviewed") is True,
        "pair06 V8 capability not reviewed",
    )
    _require(capability.get("pair_slot") == PAIR_SLOT, "pair06 capability slot drift")
    _require(capability.get("held_out") is False, "pair06 capability became held-out")
    _require(
        capability.get("runtime_selection_key") == RUNTIME_SELECTION_KEY,
        "pair06 capability runtime selection drift",
    )
    _require(
        capability.get("activation_kind") == ACTIVATION_KIND,
        "pair06 capability activation-kind drift",
    )
    _require(
        capability.get("runtime_loader_callable_bound") is True,
        "pair06 V8 loader callable missing",
    )
    _require(
        capability.get("runtime_load_authorized") is False
        and capability.get("runtime_load_performed") is False,
        "pair06 V8 capability already authorized/loaded",
    )

    _require(
        environment.get("pair06_v8_environment_path_binding_reviewed") is True,
        "pair06 V8 environment path not reviewed",
    )
    _require(environment.get("pair_slot") == PAIR_SLOT, "pair06 environment slot drift")
    _require(environment.get("held_out") is False, "pair06 environment became held-out")
    _require(
        environment.get("python_path") == PYTHON_PATH,
        "pair06 Python path drift",
    )
    _require(
        tuple(environment.get("python_major_minor", ())) == PYTHON_MAJOR_MINOR,
        "pair06 Python version drift",
    )
    _require(
        environment.get("pip_freeze_sha256") == PIP_FREEZE_SHA256,
        "pair06 pip-freeze drift",
    )
    _require(
        environment.get("runtime_environment_admitted") is True
        and environment.get("runtime_environment_path_bound") is True,
        "pair06 environment not admitted/bound",
    )
    _require(
        environment.get("runtime_load_authorized") is False
        and environment.get("runtime_load_performed") is False,
        "pair06 environment already authorizes/performs load",
    )
    _require(
        environment.get("next_gate")
        == "PAIR06_V8_RUNTIME_LOAD_AUTHORIZATION_REQUEST_REQUIRED",
        "pair06 environment request frontier drift",
    )

    _require(
        host_paths.get("pair06_v8_host_path_binding_reviewed") is True,
        "pair06 V8 host paths not reviewed",
    )
    _require(host_paths.get("pair_slot") == PAIR_SLOT, "pair06 host-path slot drift")
    _require(
        host_paths.get("model_dir") == MODEL_DIR,
        "pair06 model-dir drift",
    )
    _require(
        host_paths.get("adapter_dir") == ADAPTER_DIR,
        "pair06 adapter-dir drift",
    )
    _require(
        host_paths.get("model_dir_path_bound") is True
        and host_paths.get("adapter_dir_path_bound") is True,
        "pair06 model/adapter paths not bound",
    )
    _require(
        host_paths.get("verified_asset_count") == 17,
        "pair06 verified asset count drift",
    )
    _require(
        host_paths.get("runtime_load_authorized") is False
        and host_paths.get("runtime_load_performed") is False,
        "pair06 host-path review already authorizes/performs load",
    )

    return {
        "capability_review": deepcopy(capability),
        "environment_review": deepcopy(environment),
        "host_path_review": deepcopy(host_paths),
    }


def pair06_v8_baseline_load_authorization_request_contract() -> dict[str, Any]:
    dependencies = _dependencies_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "environment_review_git_blob": ENVIRONMENT_REVIEW_GIT_BLOB,
        "environment_review_source_sha256": ENVIRONMENT_REVIEW_SOURCE_SHA256,
        "host_path_review_git_blob": HOST_PATH_REVIEW_GIT_BLOB,
        "host_path_review_source_sha256": HOST_PATH_REVIEW_SOURCE_SHA256,
        "capability_review_git_blob": CAPABILITY_REVIEW_GIT_BLOB,
        "capability_review_source_sha256": CAPABILITY_REVIEW_SOURCE_SHA256,
        "runtime_load_authorization_request_implemented": True,
        "runtime_load_authorization_request_reviewed": False,
        "runtime_load_authorization_requested": True,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "baseline_first": True,
        "candidate_runtime_load_requested": False,
        "candidate_runtime_load_authorized": False,
        "pair15_execution_authorized": False,
        "runtime_selection_key": RUNTIME_SELECTION_KEY,
        "activation_kind": ACTIVATION_KIND,
        "model_dir": MODEL_DIR,
        "adapter_dir": ADAPTER_DIR,
        "python_path": PYTHON_PATH,
        "python_major_minor": PYTHON_MAJOR_MINOR,
        "pip_freeze_sha256": PIP_FREEZE_SHA256,
        "exact_17_asset_verification_reviewed": True,
        "runtime_environment_observation_reviewed": True,
        "runtime_environment_admitted": True,
        "runtime_environment_path_bound": True,
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "game_mutation_performed": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": deepcopy(dependencies),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_runtime_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationRequestHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationRequestHold(
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_NOT_AUTHORIZED"
    )


def execute_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadAuthorizationRequestHold(
        "PAIR06_BASELINE_GAME_EXECUTION_NOT_AUTHORIZED"
    )
