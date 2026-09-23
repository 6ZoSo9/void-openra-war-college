"""Source-only request for pair-06 accepted-V8 runtime environment observation.

The pair-06 Precision model and adapter paths are reviewed separately. The
accepted V8 loader also requires an exact Python interpreter/package identity
before any real model load can be considered.

This request defines only the read-only evidence shape for Precision:
* Python major/minor must be 3.12;
* pip-freeze stdout SHA-256 must match the accepted V8 runtime;
* interpreter discovery must remain bounded to the known V8 work root;
* exactly one accepted interpreter candidate is required.

Import or contract inspection performs no filesystem scan, subprocess action,
model load, inference, game execution, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_source_binding_review_generation2
    as path_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-runtime-environment-observation-request-contract.v1"
)

PATH_REVIEW_GIT_BLOB = "c162a8013894ebcb6f310432c96e7daf2c9de3d0"
PATH_REVIEW_SOURCE_SHA256 = (
    "49c4f44f6f164595fb9c50290b81aa56b62261b4924e859dfd7383a6e84ad07a"
)

PAIR_SLOT = 6
WORK_ROOT = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
EXPECTED_PYTHON_MAJOR_MINOR = (3, 12)
EXPECTED_PIP_FREEZE_SHA256 = (
    "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
)

NEXT_GATE = "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_precision_runtime_environment_observation"


class Pair06V8EnvironmentObservationRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8EnvironmentObservationRequestHold(message)


@lru_cache(maxsize=1)
def _path_binding_cached() -> dict[str, Any]:
    contract = path_review.pair06_v8_host_path_binding_review_contract()
    _require(
        contract.get("pair06_v8_host_path_binding_reviewed") is True,
        "pair06 V8 host-path binding not reviewed",
    )
    _require(contract.get("pair_slot") == PAIR_SLOT, "pair06 path binding slot drift")
    _require(contract.get("held_out") is False, "pair06 path binding became held-out")
    _require(
        contract.get("model_dir_path_bound") is True
        and contract.get("adapter_dir_path_bound") is True,
        "pair06 V8 host paths not bound",
    )
    _require(
        contract.get("verified_asset_count") == 17,
        "pair06 V8 asset verification count drift",
    )
    _require(
        contract.get("runtime_environment_observation_required") is True,
        "pair06 V8 runtime environment observation no longer required",
    )
    _require(
        tuple(contract.get("expected_runtime_python_major_minor", ()))
        == EXPECTED_PYTHON_MAJOR_MINOR,
        "pair06 V8 expected Python drift",
    )
    _require(
        contract.get("expected_runtime_pip_freeze_sha256")
        == EXPECTED_PIP_FREEZE_SHA256,
        "pair06 V8 expected pip-freeze drift",
    )
    _require(
        contract.get("runtime_environment_observed") is False
        and contract.get("runtime_environment_admitted") is False,
        "pair06 V8 environment already observed/admitted",
    )
    _require(
        contract.get("runtime_load_authorized") is False
        and contract.get("runtime_load_performed") is False,
        "pair06 V8 runtime load unexpectedly authorized/performed",
    )
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
        "pair06 V8 environment observation frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_environment_observation_request_contract() -> dict[str, Any]:
    bound = _path_binding_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "path_review_git_blob": PATH_REVIEW_GIT_BLOB,
        "path_review_source_sha256": PATH_REVIEW_SOURCE_SHA256,
        "pair06_v8_environment_observation_request_implemented": True,
        "pair06_v8_environment_observation_request_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "held_out": False,
        "work_root": WORK_ROOT,
        "interpreter_discovery_scope": "bounded_known_v8_work_root",
        "interpreter_candidate_count": 0,
        "expected_python_major_minor": EXPECTED_PYTHON_MAJOR_MINOR,
        "expected_pip_freeze_sha256": EXPECTED_PIP_FREEZE_SHA256,
        "exactly_one_accepted_interpreter_required": True,
        "pip_freeze_observation_read_only": True,
        "runtime_environment_observed": False,
        "runtime_environment_admitted": False,
        "runtime_environment_path_bound": False,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_host_path_binding": deepcopy(bound),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_precision_environment(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentObservationRequestHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentObservationRequestHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
