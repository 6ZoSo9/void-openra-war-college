"""Source-only binding of the accepted pair-06 V8 Precision interpreter path.

This source consumes separately reviewed Precision environment evidence and
binds the exact accepted Python interpreter used by the V8 runtime. It performs
no filesystem access, subprocess action, model load, inference, game execution,
training, promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_environment_observation_source_binding_review_generation2
    as observation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-runtime-environment-path-binding-contract.v1"
)

OBSERVATION_REVIEW_GIT_BLOB = "0f1aa52169d01bb6d384e4858253d07e46e31311"
OBSERVATION_REVIEW_SOURCE_SHA256 = (
    "1e52c7feb497241e7b453ca9047917ab456dc86d21523699ace3b3f5916b14b1"
)

PAIR_SLOT = 6
WORK_ROOT = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
PYTHON_PATH = WORK_ROOT + "/venv/bin/python3.12"
PYTHON_MAJOR_MINOR = (3, 12)
PIP_FREEZE_SHA256 = (
    "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
)

NEXT_GATE = (
    "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_runtime_environment_path_binding_source_binding_review"
)


class Pair06V8EnvironmentPathBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8EnvironmentPathBindingHold(message)


@lru_cache(maxsize=1)
def _observation_cached() -> dict[str, Any]:
    contract = (
        observation_review
        .pair06_v8_precision_environment_observation_review_contract()
    )
    _require(
        contract.get("pair06_v8_precision_environment_observation_reviewed") is True,
        "pair06 V8 Precision environment observation not reviewed",
    )
    _require(contract.get("pair_slot") == PAIR_SLOT, "pair06 environment slot drift")
    _require(contract.get("held_out") is False, "pair06 environment became held-out")
    _require(contract.get("work_root") == WORK_ROOT, "pair06 environment work-root drift")
    _require(
        contract.get("accepted_python") == PYTHON_PATH,
        "pair06 accepted interpreter path drift",
    )
    _require(
        tuple(contract.get("accepted_python_major_minor", ()))
        == PYTHON_MAJOR_MINOR,
        "pair06 accepted Python version drift",
    )
    _require(
        contract.get("accepted_pip_freeze_sha256") == PIP_FREEZE_SHA256,
        "pair06 accepted pip-freeze drift",
    )
    _require(
        contract.get("accepted_interpreter_candidate_count") == 1,
        "pair06 accepted interpreter uniqueness drift",
    )
    _require(
        contract.get("runtime_environment_observed") is True
        and contract.get("runtime_environment_admitted") is True,
        "pair06 runtime environment not observed/admitted",
    )
    _require(
        contract.get("runtime_environment_path_binding_eligible") is True,
        "pair06 runtime environment not path-binding eligible",
    )
    _require(
        contract.get("runtime_environment_path_bound") is False,
        "pair06 runtime environment path already bound",
    )
    _require(
        contract.get("runtime_load_authorized") is False
        and contract.get("runtime_load_performed") is False,
        "pair06 runtime load unexpectedly authorized/performed",
    )
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_REQUIRED",
        "pair06 environment path-binding frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_environment_path_binding_contract() -> dict[str, Any]:
    observed = _observation_cached()
    _require(PYTHON_PATH.startswith(WORK_ROOT + "/"), "pair06 interpreter escaped work root")
    return {
        "schema": CONTRACT_SCHEMA,
        "observation_review_git_blob": OBSERVATION_REVIEW_GIT_BLOB,
        "observation_review_source_sha256": OBSERVATION_REVIEW_SOURCE_SHA256,
        "pair06_v8_environment_path_binding_implemented": True,
        "pair06_v8_environment_path_binding_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "held_out": False,
        "work_root": WORK_ROOT,
        "python_path": PYTHON_PATH,
        "python_path_bound": True,
        "python_major_minor": PYTHON_MAJOR_MINOR,
        "pip_freeze_sha256": PIP_FREEZE_SHA256,
        "runtime_environment_observation_reviewed": True,
        "runtime_environment_admitted": True,
        "runtime_environment_path_bound": True,
        "runtime_environment_path_binding_performs_host_io": False,
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


def bound_pair06_v8_environment() -> dict[str, Any]:
    contract = pair06_v8_environment_path_binding_contract()
    return {
        "python_path": contract["python_path"],
        "python_major_minor": contract["python_major_minor"],
        "pip_freeze_sha256": contract["pip_freeze_sha256"],
    }


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentPathBindingHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
