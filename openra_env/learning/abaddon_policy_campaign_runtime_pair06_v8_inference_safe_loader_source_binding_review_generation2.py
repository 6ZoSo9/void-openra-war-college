"""Source-only review of pair-06 V8 inference-safe no-offload loader."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_inference_safe_loader_generation2
    as loader,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-inference-safe-loader-review-contract.v1"
)

LOADER_GIT_BLOB = "02edc92db7823270b521f7429730ee3de230db4e"
LOADER_SOURCE_SHA256 = (
    "824d7e65e293ac8eb1a3e44bf33361a92fe806f268309556895be26baf9f962c"
)
LOADER_TEST_GIT_BLOB = "ae686f6d73faf85cebc5da6751808809ea1e815e"
LOADER_TEST_SHA256 = (
    "2059a642b9c7e77060273a45ad35c11603359a92d9098bd02e0a5797e6b96118"
)

NEXT_GATE = "PAIR06_V8_PARENT_SUPERVISOR_INFERENCE_SAFE_LOADER_BINDING_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_supervisor_inference_safe_loader_binding"


class Pair06V8InferenceSafeLoaderReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8InferenceSafeLoaderReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = loader.pair06_v8_inference_safe_loader_contract()
    _require(
        out.get("pair06_v8_inference_safe_loader_implemented") is True,
        "pair06 inference-safe loader missing",
    )
    _require(
        out.get("pair06_v8_inference_safe_loader_reviewed") is False,
        "pair06 inference-safe loader unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "pair06 inference-safe loader slot drift")
    _require(out.get("arm") == "baseline", "pair06 inference-safe loader arm drift")
    _require(out.get("device_map") == {"": 0}, "pair06 inference-safe device map drift")
    _require(out.get("offload_embedding") is False, "pair06 embedding offload re-enabled")

    for field in (
        "accepted_v8_assets_unchanged",
        "accepted_v8_tool_semantics_unchanged",
        "accepted_v8_environment_verification_reused",
        "accepted_v8_asset_verification_reused",
        "single_gpu_cuda0_required",
        "all_parameters_cuda0_verified_after_adapter_load",
        "input_embedding_cuda0_verified_after_adapter_load",
        "hf_device_map_cpu_disk_meta_rejected",
    ):
        _require(out.get(field) is True, f"inference-safe loader invariant drift: {field}")

    for field in (
        "cpu_embedding_offload_allowed",
        "cpu_parameter_offload_allowed",
        "disk_parameter_offload_allowed",
        "meta_parameter_allowed_after_load",
        "runtime_load_authorized",
        "runtime_load_performed",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
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
        _require(out.get(field) is False, f"inference-safe loader boundary drift: {field}")

    _require(
        out.get("next_gate")
        == "PAIR06_V8_INFERENCE_SAFE_LOADER_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 inference-safe loader frontier drift",
    )
    return deepcopy(out)


def pair06_v8_inference_safe_loader_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "loader_git_blob": LOADER_GIT_BLOB,
        "loader_source_sha256": LOADER_SOURCE_SHA256,
        "loader_test_git_blob": LOADER_TEST_GIT_BLOB,
        "loader_test_sha256": LOADER_TEST_SHA256,
        "pair06_v8_inference_safe_loader_source_binding_present": True,
        "pair06_v8_inference_safe_loader_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "device_map": {"": 0},
        "offload_embedding": False,
        "cpu_embedding_offload_allowed": False,
        "cpu_parameter_offload_allowed": False,
        "disk_parameter_offload_allowed": False,
        "meta_parameter_allowed_after_load": False,
        "all_parameters_cuda0_required": True,
        "input_embedding_cuda0_required": True,
        "runtime_load_authorized": False,
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
        "validated_loader": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8InferenceSafeLoaderReviewHold(NEXT_GATE)
