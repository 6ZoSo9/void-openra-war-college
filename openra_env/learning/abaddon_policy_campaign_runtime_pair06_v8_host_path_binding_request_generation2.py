"""Source-only host-path binding request for pair-06 accepted V8 runtime.

The pair-06 V8 capability is reviewed separately. Repository state intentionally
contains no canonical Precision-local model_dir or adapter_dir path.

This module defines the exact read-only evidence shape required to bind those
two directories on Precision. It performs no filesystem scan, path binding,
model load, inference, game execution, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_source_binding_review_generation2
    as capability_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-host-path-binding-request-contract.v1"
)

CAPABILITY_REVIEW_GIT_BLOB = "8e405b4d03a7a7310dbedd9fae0edbe9976b4637"
CAPABILITY_REVIEW_SOURCE_SHA256 = (
    "5c4836135629ea47e5e38f6aff0bc61201f754b8354152768e9fbf89c5e000fb"
)
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

PAIR_SLOT = 6
MODEL_SCOPE = "model_dir"
ADAPTER_SCOPE = "adapter_dir"

MODEL_ASSETS = (
    ("config.json", v8_runtime.BASE_MODEL_CONFIG_SHA256),
    ("model.safetensors-00001-of-00002.safetensors", v8_runtime.BASE_MODEL_SHARD1_SHA256),
    ("model.safetensors-00002-of-00002.safetensors", v8_runtime.BASE_MODEL_SHARD2_SHA256),
    ("model.safetensors.index.json", v8_runtime.BASE_MODEL_INDEX_SHA256),
    ("chat_template.jinja", v8_runtime.CHAT_TEMPLATE_SHA256),
    ("tokenizer.json", v8_runtime.TOKENIZER_JSON_SHA256),
    ("tokenizer_config.json", v8_runtime.TOKENIZER_CONFIG_SHA256),
    ("merges.txt", v8_runtime.MERGES_SHA256),
    ("vocab.json", v8_runtime.VOCAB_SHA256),
    ("added_tokens.json", v8_runtime.ADDED_TOKENS_SHA256),
    ("special_tokens_map.json", v8_runtime.SPECIAL_TOKENS_MAP_SHA256),
    ("processor_config.json", v8_runtime.PROCESSOR_CONFIG_SHA256),
)

ADAPTER_ASSETS = (
    ("adapter_config.json", v8_runtime.V8_ADAPTER_CONFIG_SHA256),
    ("adapter_model.safetensors", v8_runtime.V8_ADAPTER_SHA256),
    ("chat_template.jinja", v8_runtime.CHAT_TEMPLATE_SHA256),
    ("tokenizer.json", v8_runtime.TOKENIZER_JSON_SHA256),
    ("tokenizer_config.json", v8_runtime.V8_ADAPTER_TOKENIZER_CONFIG_SHA256),
)

NEXT_GATE = "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_precision_host_path_observation"


class Pair06V8HostPathBindingRequestHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8HostPathBindingRequestHold(message)


@lru_cache(maxsize=1)
def _capability_cached() -> dict[str, Any]:
    contract = capability_review.pair06_v8_runtime_capability_review_contract()
    _require(
        contract.get("pair06_v8_runtime_capability_reviewed") is True,
        "pair06 V8 capability not reviewed",
    )
    _require(contract.get("pair_slot") == PAIR_SLOT, "pair06 capability slot drift")
    _require(contract.get("held_out") is False, "pair06 capability became held-out")
    _require(
        contract.get("runtime_selection_key")
        == "apollyon-v3-v8-accepted-model-control",
        "pair06 V8 runtime selection drift",
    )
    _require(
        contract.get("activation_kind") == "inprocess_accepted_v8_runtime",
        "pair06 V8 activation kind drift",
    )
    _require(
        contract.get("model_dir_path_bound") is False
        and contract.get("adapter_dir_path_bound") is False,
        "pair06 V8 paths already bound",
    )
    _require(
        contract.get("runtime_load_authorized") is False
        and contract.get("runtime_load_performed") is False,
        "pair06 V8 runtime load already authorized/performed",
    )
    _require(
        contract.get("next_gate") == "PAIR06_V8_HOST_PATH_BINDING_REQUIRED",
        "pair06 V8 path-binding frontier drift",
    )
    return deepcopy(contract)


def _manifest() -> tuple[dict[str, str], ...]:
    rows = []
    for scope, assets in (
        (MODEL_SCOPE, MODEL_ASSETS),
        (ADAPTER_SCOPE, ADAPTER_ASSETS),
    ):
        for relative_path, sha256 in assets:
            _require(
                isinstance(relative_path, str) and bool(relative_path),
                "pair06 V8 asset relative path invalid",
            )
            _require(
                isinstance(sha256, str)
                and len(sha256) == 64
                and all(c in "0123456789abcdef" for c in sha256),
                "pair06 V8 asset SHA-256 invalid",
            )
            rows.append(
                {
                    "scope": scope,
                    "relative_path": relative_path,
                    "sha256": sha256,
                }
            )
    _require(len(rows) == 17, "pair06 V8 asset manifest cardinality drift")
    return tuple(rows)


def pair06_v8_host_path_binding_request_contract() -> dict[str, Any]:
    capability = _capability_cached()
    manifest = _manifest()
    return {
        "schema": CONTRACT_SCHEMA,
        "capability_review_git_blob": CAPABILITY_REVIEW_GIT_BLOB,
        "capability_review_source_sha256": CAPABILITY_REVIEW_SOURCE_SHA256,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "host_path_binding_request_implemented": True,
        "host_path_binding_request_reviewed": False,
        "precision_host_observation_required": True,
        "host_observation_performed": False,
        "filesystem_scan_performed_by_contract": False,
        "model_dir_path_bound": False,
        "adapter_dir_path_bound": False,
        "model_dir_candidate_count": 0,
        "adapter_dir_candidate_count": 0,
        "required_model_asset_count": len(MODEL_ASSETS),
        "required_adapter_asset_count": len(ADAPTER_ASSETS),
        "required_asset_count": len(manifest),
        "required_asset_manifest": deepcopy(manifest),
        "exact_hash_match_required_for_every_asset": True,
        "model_and_adapter_directories_must_be_distinct": True,
        "symlinked_required_files_allowed": False,
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
        "reviewed_capability": deepcopy(capability),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def bind_host_paths(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingRequestHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingRequestHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
