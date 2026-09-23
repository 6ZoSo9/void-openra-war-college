"""Source-only review of the pair-06 V8 offload-safe generate adapter."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_offload_safe_generate_adapter_generation2
    as adapter,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-offload-safe-generate-adapter-review-contract.v1"
)

ADAPTER_GIT_BLOB = "45f970eb4160bf6d3c5eafcbd74705eef8802121"
ADAPTER_SOURCE_SHA256 = (
    "f1a78fc386965f1108c6ae7ce1b94c870b7d21208bf9c9f336f9fb46eecc446d"
)
ADAPTER_TEST_GIT_BLOB = "388aabe101bc319cc02e9ba1b91491272b3bcbd4"
ADAPTER_TEST_SHA256 = (
    "f53c6128c2bce961b09fda41bfd94a645671a326c20e397e4a599ff9b2ae3315"
)

NEXT_GATE = "PAIR06_V8_PARENT_SUPERVISOR_OFFLOAD_ADAPTER_BINDING_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_supervisor_offload_adapter_binding"


class Pair06V8OffloadSafeGenerateReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8OffloadSafeGenerateReviewHold(message)


@lru_cache(maxsize=1)
def _validate_cached() -> dict[str, Any]:
    contract = adapter.pair06_v8_offload_safe_generate_adapter_contract()
    _require(
        contract.get("pair06_v8_offload_safe_generate_adapter_implemented") is True,
        "pair06 offload-safe generate adapter missing",
    )
    _require(
        contract.get("pair06_v8_offload_safe_generate_adapter_reviewed") is False,
        "pair06 offload-safe adapter unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 adapter slot drift")
    _require(contract.get("arm") == "baseline", "pair06 adapter arm drift")

    for field in (
        "accepted_v8_runtime_source_unchanged",
        "model_asset_bytes_unchanged",
        "tokenizer_asset_bytes_unchanged",
        "tool_translation_unchanged",
        "host_validation_unchanged",
        "generate_instance_method_only_replaced",
        "input_device_from_embedding_weight",
        "cpu_embedding_supported",
        "cuda_embedding_supported",
        "meta_embedding_rejected",
    ):
        _require(contract.get(field) is True, f"pair06 adapter invariant drift: {field}")

    _require(
        contract.get("hard_coded_cuda_input_transfer_used") is False,
        "pair06 adapter still hard-codes CUDA input placement",
    )

    for field in (
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "automatic_retry",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 adapter authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_OFFLOAD_SAFE_GENERATE_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 adapter review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_offload_safe_generate_adapter_review_contract() -> dict[str, Any]:
    validated = _validate_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "adapter_git_blob": ADAPTER_GIT_BLOB,
        "adapter_source_sha256": ADAPTER_SOURCE_SHA256,
        "adapter_test_git_blob": ADAPTER_TEST_GIT_BLOB,
        "adapter_test_sha256": ADAPTER_TEST_SHA256,
        "pair06_v8_offload_safe_generate_adapter_source_binding_present": True,
        "pair06_v8_offload_safe_generate_adapter_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "accepted_v8_runtime_source_unchanged": True,
        "model_asset_bytes_unchanged": True,
        "tokenizer_asset_bytes_unchanged": True,
        "tool_translation_unchanged": True,
        "host_validation_unchanged": True,
        "generate_instance_method_only_replaced": True,
        "input_device_from_embedding_weight": True,
        "cpu_embedding_supported": True,
        "cuda_embedding_supported": True,
        "meta_embedding_rejected": True,
        "hard_coded_cuda_input_transfer_used": False,
        "model_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_adapter": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8OffloadSafeGenerateReviewHold(NEXT_GATE)
