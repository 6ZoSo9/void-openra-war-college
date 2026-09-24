"""Inference-safe pair-06 loader for the accepted Apollyon V8 runtime.

The accepted V8 model/tokenizer/adapter bytes and tool semantics remain
unchanged. The repair is strictly placement policy for pair-06 inference:

* disable Unsloth embedding offload explicitly;
* force the exact model onto CUDA device 0 instead of allowing CPU/disk
  dispatch;
* after PEFT adapter attachment, fail closed if any model parameter is not on
  CUDA or if any observed hf_device_map entry names CPU/disk/meta;
* require the input embedding itself to be CUDA resident.

This closes the two observed first-inference failures:
1. CUDA input ids against a CPU-offloaded input embedding;
2. CPU hidden state reaching Qwen3.5 GatedDeltaNet's Triton kernel.

Import and contract inspection perform no model load, inference, game action,
training, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import os
from pathlib import Path
from typing import Any, Mapping, Protocol

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-inference-safe-loader-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"

DEVICE_MAP = {"": 0}
OFFLOAD_EMBEDDING = False

NEXT_GATE = "PAIR06_V8_INFERENCE_SAFE_LOADER_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_inference_safe_loader_review"


class Pair06V8InferenceSafeLoaderHold(RuntimeError):
    pass


class AuthorityCheck(Protocol):
    def __call__(self, pair_slot: int, arm: str) -> bool:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8InferenceSafeLoaderHold(message)


def _device_type(device: Any) -> str:
    value = getattr(device, "type", None)
    return value if isinstance(value, str) else str(device).split(":", 1)[0]


def _device_index(device: Any) -> int | None:
    value = getattr(device, "index", None)
    if value is None:
        text = str(device)
        if ":" in text:
            try:
                return int(text.rsplit(":", 1)[1])
            except ValueError:
                return None
        return None
    return int(value)


def _map_value_is_cuda_zero(value: Any) -> bool:
    if type(value) is int:
        return value == 0
    text = str(value).lower()
    return text in {"0", "cuda", "cuda:0"}


def _observed_device_maps(model: Any) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[int] = set()
    queue = [model]

    while queue:
        current = queue.pop(0)
        if current is None or id(current) in seen:
            continue
        seen.add(id(current))

        mapping = getattr(current, "hf_device_map", None)
        if isinstance(mapping, Mapping):
            result.append(dict(mapping))

        for name in ("base_model", "model"):
            child = getattr(current, name, None)
            if child is not None and id(child) not in seen:
                queue.append(child)

    return result


def _assert_cuda_zero_resident(model: Any) -> dict[str, Any]:
    maps = _observed_device_maps(model)
    for mapping in maps:
        for name, device in mapping.items():
            _require(
                _map_value_is_cuda_zero(device),
                f"PAIR06_V8_INFERENCE_OFFLOAD_FORBIDDEN:{name}:{device}",
            )

    named_parameters = getattr(model, "named_parameters", None)
    _require(callable(named_parameters), "pair06 V8 model has no named_parameters")

    parameter_count = 0
    parameter_numel = 0
    for name, parameter in named_parameters():
        parameter_count += 1
        device = getattr(parameter, "device", None)
        _require(
            _device_type(device) == "cuda" and _device_index(device) in (None, 0),
            f"PAIR06_V8_INFERENCE_PARAMETER_NOT_CUDA0:{name}:{device}",
        )
        numel = getattr(parameter, "numel", None)
        if callable(numel):
            parameter_numel += int(numel())

    _require(parameter_count > 0, "pair06 V8 model has no parameters")

    getter = getattr(model, "get_input_embeddings", None)
    _require(callable(getter), "pair06 V8 input embedding accessor missing")
    embedding = getter()
    weight = getattr(embedding, "weight", None)
    device = getattr(weight, "device", None)
    _require(
        _device_type(device) == "cuda" and _device_index(device) in (None, 0),
        f"PAIR06_V8_INFERENCE_EMBEDDING_NOT_CUDA0:{device}",
    )

    return {
        "device_map_count": len(maps),
        "all_observed_device_maps_cuda0": True,
        "parameter_count": parameter_count,
        "parameter_numel": parameter_numel,
        "all_parameters_cuda0": True,
        "input_embedding_device": str(device),
        "input_embedding_cuda0": True,
        "cpu_parameter_count": 0,
        "meta_parameter_count": 0,
        "disk_offload_present": False,
    }


def load_pair06_v8_inference_safe_runtime(
    *,
    model_dir: str,
    adapter_dir: str,
    runtime_load_authorized: bool,
    authority_check: AuthorityCheck,
):
    """Load exact accepted V8 bytes with CPU/disk offload forbidden for inference."""

    _require(
        runtime_load_authorized is True,
        "PAIR06_V8_INFERENCE_SAFE_LOAD_AUTHORIZATION_REQUIRED",
    )
    _require(callable(authority_check), "pair06 V8 authority callback required")
    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V8_INFERENCE_SAFE_LOAD_AUTHORITY_REVOKED",
    )

    model_path = Path(model_dir).expanduser().resolve()
    adapter_path = Path(adapter_dir).expanduser().resolve()
    _require(model_path != adapter_path, "pair06 V8 model/adapter dirs must differ")

    v8_runtime.verify_v8_runtime_environment()
    v8_runtime.verify_v8_runtime_assets(
        model_dir=model_path,
        adapter_dir=adapter_path,
    )

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    __import__("unsloth")
    import torch
    from peft import PeftModel
    from unsloth import FastModel

    _require(torch.cuda.is_available(), "pair06 V8 CUDA unavailable")
    _require(torch.cuda.device_count() >= 1, "pair06 V8 CUDA device 0 unavailable")

    torch.manual_seed(v8_runtime.GENERATION_SEED)
    torch.cuda.manual_seed_all(v8_runtime.GENERATION_SEED)

    model, processor = FastModel.from_pretrained(
        model_name=str(model_path),
        max_seq_length=v8_runtime.MAX_SEQUENCE_LENGTH,
        dtype=torch.bfloat16,
        load_in_4bit=False,
        load_in_8bit=False,
        full_finetuning=False,
        local_files_only=True,
        offload_embedding=OFFLOAD_EMBEDDING,
        device_map=deepcopy(DEVICE_MAP),
    )

    tokenizer = getattr(processor, "tokenizer", processor)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    _require(
        tokenizer.pad_token_id is not None,
        "tokenizer has no usable pad/eos token",
    )

    model = PeftModel.from_pretrained(
        model,
        str(adapter_path),
        is_trainable=False,
        local_files_only=True,
    )
    model.eval()

    placement = _assert_cuda_zero_resident(model)
    runtime = v8_runtime.FrozenV8LocalToolRuntime(
        model=model,
        tokenizer=tokenizer,
        torch_module=torch,
    )
    runtime._void_pair06_inference_safe_placement = deepcopy(placement)
    return runtime


def pair06_v8_inference_safe_loader_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_inference_safe_loader_implemented": True,
        "pair06_v8_inference_safe_loader_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "accepted_v8_assets_unchanged": True,
        "accepted_v8_tool_semantics_unchanged": True,
        "accepted_v8_environment_verification_reused": True,
        "accepted_v8_asset_verification_reused": True,
        "device_map": deepcopy(DEVICE_MAP),
        "single_gpu_cuda0_required": True,
        "offload_embedding": OFFLOAD_EMBEDDING,
        "cpu_embedding_offload_allowed": False,
        "cpu_parameter_offload_allowed": False,
        "disk_parameter_offload_allowed": False,
        "meta_parameter_allowed_after_load": False,
        "all_parameters_cuda0_verified_after_adapter_load": True,
        "input_embedding_cuda0_verified_after_adapter_load": True,
        "hf_device_map_cpu_disk_meta_rejected": True,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8InferenceSafeLoaderHold(NEXT_GATE)
