"""Pair-06 V8 offload-safe generate adapter.

The accepted V8 runtime source remains byte-for-byte frozen. This adapter is
applied only to one already-loaded pair-06 runtime instance after the reviewed
loader returns. It replaces only the instance's generate method so tokenizer
tensors follow the actual input-embedding weight device rather than an
unconditional CUDA transfer.

This is required for accepted loads where Accelerate/Unsloth offloads the input
embedding to CPU because of GPU memory pressure.

Import and contract inspection perform no host I/O, model load, inference,
game execution, subprocess/service action, training, deployment, VOID-chain
mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from types import MethodType
from typing import Any, Mapping, Sequence

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-offload-safe-generate-adapter-contract.v1"
)

V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"
V8_RUNTIME_SOURCE_SHA256 = (
    "faf4b64ea4755fabdbdfc778f3df534a87f056a638763aa1560c7965c482b5af"
)

PAIR_SLOT = 6
ARM = "baseline"

NEXT_GATE = "PAIR06_V8_OFFLOAD_SAFE_GENERATE_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_offload_safe_generate_adapter_review"


class Pair06V8OffloadSafeGenerateHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8OffloadSafeGenerateHold(message)


def _input_device(runtime: Any) -> Any:
    model = getattr(runtime, "model", None)
    _require(model is not None, "pair06 V8 runtime model missing")
    getter = getattr(model, "get_input_embeddings", None)
    _require(callable(getter), "pair06 V8 input-embedding accessor missing")
    embedding = getter()
    weight = getattr(embedding, "weight", None)
    device = getattr(weight, "device", None)
    device_type = getattr(device, "type", None)
    _require(
        device_type in {"cpu", "cuda"},
        "pair06 V8 input-embedding device unsupported",
    )
    return device


def _offload_safe_generate(
    runtime: Any,
    *,
    messages: Sequence[Mapping[str, Any]],
    tools: Sequence[Mapping[str, Any]],
) -> str:
    _require(
        len(messages) == 2,
        "V8 runtime requires exact two-message current input",
    )
    v8_runtime._current_runtime_names(tools)

    tokenizer = getattr(runtime, "tokenizer", None)
    torch_module = getattr(runtime, "_torch", None)
    model = getattr(runtime, "model", None)
    _require(tokenizer is not None, "pair06 V8 tokenizer missing")
    _require(torch_module is not None, "pair06 V8 torch module missing")
    _require(model is not None, "pair06 V8 model missing")

    prompt = tokenizer.apply_chat_template(
        list(messages),
        tools=list(tools),
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    encoded = tokenizer(
        prompt,
        return_tensors="pt",
        add_special_tokens=False,
    )
    _require(
        isinstance(encoded, Mapping)
        and "input_ids" in encoded,
        "pair06 V8 tokenizer output missing input_ids",
    )

    input_device = _input_device(runtime)
    moved = {}
    for key, value in encoded.items():
        mover = getattr(value, "to", None)
        _require(callable(mover), f"pair06 V8 encoded tensor not movable: {key}")
        moved[key] = mover(input_device)

    prompt_len = int(moved["input_ids"].shape[1])
    inference_mode = getattr(torch_module, "inference_mode", None)
    _require(callable(inference_mode), "pair06 V8 inference_mode missing")

    with inference_mode():
        output = model.generate(
            **moved,
            max_new_tokens=v8_runtime.MAX_NEW_TOKENS,
            do_sample=False,
            use_cache=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_ids = output[0, prompt_len:].detach().cpu()
    return tokenizer.decode(
        new_ids,
        skip_special_tokens=True,
    ).strip()


def bind_pair06_v8_offload_safe_generate(runtime: Any) -> Any:
    """Bind one already-loaded pair-06 runtime instance to offload-safe input placement."""
    _require(
        isinstance(runtime, v8_runtime.FrozenV8LocalToolRuntime),
        "pair06 V8 runtime type drift",
    )
    _require(
        getattr(runtime, "_void_pair06_offload_safe_generate_bound", False)
        is False,
        "pair06 V8 offload-safe generate already bound",
    )
    _input_device(runtime)

    def bound(
        self: Any,
        *,
        messages: Sequence[Mapping[str, Any]],
        tools: Sequence[Mapping[str, Any]],
    ) -> str:
        return _offload_safe_generate(
            self,
            messages=messages,
            tools=tools,
        )

    runtime.generate = MethodType(bound, runtime)
    runtime._void_pair06_offload_safe_generate_bound = True
    return runtime


def pair06_v8_offload_safe_generate_adapter_contract() -> dict[str, Any]:
    runtime_contract = v8_runtime.v8_tool_runtime_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "v8_runtime_source_sha256": V8_RUNTIME_SOURCE_SHA256,
        "pair06_v8_offload_safe_generate_adapter_implemented": True,
        "pair06_v8_offload_safe_generate_adapter_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
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
        "model_load_performed": False,
        "model_inference_performed": False,
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
        "accepted_runtime_contract": deepcopy(runtime_contract),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8OffloadSafeGenerateHold(NEXT_GATE)
