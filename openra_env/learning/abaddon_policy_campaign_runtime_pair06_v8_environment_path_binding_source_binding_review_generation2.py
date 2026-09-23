"""Source-only review of the pair-06 V8 runtime-environment path binding."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_path_binding_generation2
    as binding,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-runtime-environment-path-binding-source-binding-review-contract.v1"
)

BINDING_GIT_BLOB = "fef22e79e6ca32ace9f018384692d2a9814d1013"
BINDING_SOURCE_SHA256 = (
    "e7b825486be3473214b0dd5d9e42ec18b99d86cf39bf66b3afbc133070342c7c"
)
BINDING_TEST_GIT_BLOB = "b162a7475b5a988ce1cdcb02d25514fb4c7aa7cc"
BINDING_TEST_SHA256 = (
    "7015384640cfac2604fb8e5821dbe85877d2569a94b911914336b4c7f05528dc"
)

NEXT_GATE = "PAIR06_V8_RUNTIME_LOAD_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_runtime_load_authorization_request"


class Pair06V8EnvironmentPathBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8EnvironmentPathBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_binding_cached() -> dict[str, Any]:
    contract = binding.pair06_v8_environment_path_binding_contract()
    _require(
        contract.get("pair06_v8_environment_path_binding_implemented") is True,
        "pair06 V8 environment-path binding missing",
    )
    _require(
        contract.get("pair06_v8_environment_path_binding_reviewed") is False,
        "pair06 V8 environment-path binding unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 environment-path slot drift")
    _require(contract.get("held_out") is False, "pair06 environment-path became held-out")
    _require(
        contract.get("python_path")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12",
        "pair06 bound interpreter path drift",
    )
    _require(
        contract.get("python_path_bound") is True,
        "pair06 interpreter path not bound",
    )
    _require(
        tuple(contract.get("python_major_minor", ())) == (3, 12),
        "pair06 bound Python version drift",
    )
    _require(
        contract.get("pip_freeze_sha256")
        == "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77",
        "pair06 bound pip-freeze drift",
    )
    _require(
        contract.get("runtime_environment_observation_reviewed") is True,
        "pair06 environment observation lineage missing",
    )
    _require(
        contract.get("runtime_environment_admitted") is True
        and contract.get("runtime_environment_path_bound") is True,
        "pair06 environment not admitted/bound",
    )
    _require(
        contract.get("runtime_environment_path_binding_performs_host_io") is False,
        "pair06 environment binding unexpectedly performs host I/O",
    )
    for field in (
        "runtime_load_authorized",
        "runtime_load_performed",
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "game_mutation_performed",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 environment-path authority drift: {field}")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 environment-path review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_environment_path_binding_review_contract() -> dict[str, Any]:
    reviewed = _validate_binding_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "binding_git_blob": BINDING_GIT_BLOB,
        "binding_source_sha256": BINDING_SOURCE_SHA256,
        "binding_test_git_blob": BINDING_TEST_GIT_BLOB,
        "binding_test_sha256": BINDING_TEST_SHA256,
        "separate_review_instrument": True,
        "binding_source_identity_pinned_by_git_blob": True,
        "binding_source_identity_pinned_by_sha256": True,
        "binding_test_identity_pinned_by_git_blob": True,
        "binding_test_identity_pinned_by_sha256": True,
        "pair06_v8_environment_path_binding_reviewed": True,
        "pair_slot": 6,
        "held_out": False,
        "work_root": reviewed["work_root"],
        "python_path": reviewed["python_path"],
        "python_path_bound": True,
        "python_major_minor": (3, 12),
        "pip_freeze_sha256": (
            "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
        ),
        "runtime_environment_observation_reviewed": True,
        "runtime_environment_admitted": True,
        "runtime_environment_path_bound": True,
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
        "reviewed_binding": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def request_runtime_load_authorization(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentPathBindingReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentPathBindingReviewHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
