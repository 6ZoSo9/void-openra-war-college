"""Source-only review of the pair-06 V8 Precision host-path binding."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_generation2
    as binding,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-host-path-binding-source-binding-review-contract.v1"
)

BINDING_GIT_BLOB = "e92b0bc331e709e5eecbba1e4321aea0f9935bd3"
BINDING_SOURCE_SHA256 = (
    "827e216fde7c8c4eee4a7e51e89f272c417911a53bb787764e55eddf08b79079"
)
BINDING_TEST_GIT_BLOB = "1e9a0acbca174800beb2f2003b5fd17efbaa01d1"
BINDING_TEST_SHA256 = (
    "b72147cf4c8f8dc2ab6a3bcc979c5aae7814e4112a0494ab47f8b09eb3e350d6"
)

NEXT_GATE = "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_runtime_environment_observation"


class Pair06V8HostPathBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8HostPathBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_binding_cached() -> dict[str, Any]:
    contract = binding.pair06_v8_host_path_binding_contract()
    _require(
        contract.get("pair06_v8_host_path_binding_implemented") is True,
        "pair06 V8 host-path binding missing",
    )
    _require(
        contract.get("pair06_v8_host_path_binding_reviewed") is False,
        "pair06 V8 host-path binding unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 host-path binding slot drift")
    _require(contract.get("held_out") is False, "pair06 host-path binding became held-out")
    _require(
        contract.get("model_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model",
        "pair06 bound model dir drift",
    )
    _require(
        contract.get("adapter_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8",
        "pair06 bound adapter dir drift",
    )
    _require(
        contract.get("model_dir_path_bound") is True
        and contract.get("adapter_dir_path_bound") is True,
        "pair06 V8 host paths not fully bound",
    )
    _require(
        contract.get("model_and_adapter_directories_distinct") is True,
        "pair06 model/adapter distinctness lost",
    )
    _require(
        contract.get("verified_asset_count") == 17,
        "pair06 bound asset verification count drift",
    )
    _require(
        contract.get(
            "asset_hash_verification_inherited_from_reviewed_precision_observation"
        )
        is True,
        "pair06 asset verification lineage missing",
    )
    _require(
        contract.get("runtime_environment_observation_required") is True,
        "pair06 V8 runtime environment observation not required",
    )
    _require(
        tuple(contract.get("expected_runtime_python_major_minor", ())) == (3, 12),
        "pair06 V8 expected Python drift",
    )
    _require(
        contract.get("expected_runtime_pip_freeze_sha256")
        == "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77",
        "pair06 V8 expected pip-freeze drift",
    )
    _require(
        contract.get("runtime_environment_observed") is False
        and contract.get("runtime_environment_admitted") is False,
        "pair06 V8 runtime environment already observed/admitted",
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
        _require(contract.get(field) is False, f"pair06 host-path authority drift: {field}")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
        "pair06 host-path binding frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_host_path_binding_review_contract() -> dict[str, Any]:
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
        "pair06_v8_host_path_binding_reviewed": True,
        "pair_slot": 6,
        "held_out": False,
        "model_dir": reviewed["model_dir"],
        "adapter_dir": reviewed["adapter_dir"],
        "model_dir_path_bound": True,
        "adapter_dir_path_bound": True,
        "verified_asset_count": 17,
        "runtime_environment_observation_required": True,
        "expected_runtime_python_major_minor": (3, 12),
        "expected_runtime_pip_freeze_sha256": (
            "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
        ),
        "runtime_environment_observed": False,
        "runtime_environment_admitted": False,
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


def observe_runtime_environment(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingReviewHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
