"""Source-only pair-06 accepted-V8 Precision host-path binding.

This source consumes the separately reviewed Precision host-path observation and
binds the exact model and adapter directories for pair 6. It performs no
filesystem access, environment check, model load, inference, game execution,
training, promotion, deployment, VOID-chain mutation, or wallet/funds action.

The accepted V8 loader still requires a live Python 3.12 + exact pip-freeze
environment check before any real model load can be considered.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_host_path_observation_source_binding_review_generation2
    as observation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-host-path-binding-contract.v1"
)

OBSERVATION_REVIEW_GIT_BLOB = "fb0fd4e5ad042c37f428265ea18919ee93b3cf5c"
OBSERVATION_REVIEW_SOURCE_SHA256 = (
    "07977371fb89e5d87ea30c292a72e31eda2ba719b21813963c80f9fd9f6dd34c"
)

PAIR_SLOT = 6
MODEL_DIR = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
ADAPTER_DIR = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"

EXPECTED_RUNTIME_PYTHON_MAJOR_MINOR = tuple(v8_runtime.RUNTIME_PYTHON_MAJOR_MINOR)
EXPECTED_RUNTIME_PIP_FREEZE_SHA256 = v8_runtime.RUNTIME_PIP_FREEZE_SHA256

NEXT_GATE = "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_runtime_environment_observation"


class Pair06V8HostPathBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8HostPathBindingHold(message)


@lru_cache(maxsize=1)
def _observation_cached() -> dict[str, Any]:
    contract = (
        observation_review
        .pair06_v8_precision_host_path_observation_review_contract()
    )
    _require(
        contract.get("pair06_v8_precision_host_path_observation_reviewed") is True,
        "pair06 V8 Precision observation not reviewed",
    )
    _require(contract.get("pair_slot") == PAIR_SLOT, "pair06 observation slot drift")
    _require(contract.get("held_out") is False, "pair06 observation became held-out")
    _require(
        contract.get("model_dir") == MODEL_DIR,
        "pair06 observed model dir drift",
    )
    _require(
        contract.get("adapter_dir") == ADAPTER_DIR,
        "pair06 observed adapter dir drift",
    )
    _require(
        contract.get("model_dir_candidate_count") == 1
        and contract.get("adapter_dir_candidate_count") == 1,
        "pair06 observed path uniqueness drift",
    )
    _require(
        contract.get("verified_asset_count") == 17,
        "pair06 observed asset count drift",
    )
    _require(
        contract.get("all_required_assets_exact_hash_verified") is True,
        "pair06 observed asset verification missing",
    )
    _require(
        contract.get("model_dir_path_binding_eligible") is True
        and contract.get("adapter_dir_path_binding_eligible") is True,
        "pair06 path binding not eligible",
    )
    _require(
        contract.get("runtime_load_authorized") is False
        and contract.get("runtime_load_performed") is False,
        "pair06 runtime load unexpectedly authorized/performed",
    )
    _require(
        contract.get("next_gate") == "PAIR06_V8_HOST_PATH_BINDING_SOURCE_REQUIRED",
        "pair06 path-binding source frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_host_path_binding_contract() -> dict[str, Any]:
    observed = _observation_cached()
    _require(MODEL_DIR != ADAPTER_DIR, "pair06 model/adapter paths not distinct")
    return {
        "schema": CONTRACT_SCHEMA,
        "observation_review_git_blob": OBSERVATION_REVIEW_GIT_BLOB,
        "observation_review_source_sha256": OBSERVATION_REVIEW_SOURCE_SHA256,
        "pair06_v8_host_path_binding_implemented": True,
        "pair06_v8_host_path_binding_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "held_out": False,
        "model_dir": MODEL_DIR,
        "adapter_dir": ADAPTER_DIR,
        "model_dir_path_bound": True,
        "adapter_dir_path_bound": True,
        "model_and_adapter_directories_distinct": True,
        "verified_asset_count": 17,
        "asset_hash_verification_inherited_from_reviewed_precision_observation": True,
        "runtime_environment_observation_required": True,
        "expected_runtime_python_major_minor": EXPECTED_RUNTIME_PYTHON_MAJOR_MINOR,
        "expected_runtime_pip_freeze_sha256": EXPECTED_RUNTIME_PIP_FREEZE_SHA256,
        "runtime_environment_observed": False,
        "runtime_environment_admitted": False,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "game_mutation_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_observation": deepcopy(observed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def bound_pair06_v8_paths() -> dict[str, str]:
    contract = pair06_v8_host_path_binding_contract()
    return {
        "model_dir": contract["model_dir"],
        "adapter_dir": contract["adapter_dir"],
    }


def observe_runtime_environment(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
