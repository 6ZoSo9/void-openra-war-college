from __future__ import annotations

import pytest

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_offload_safe_generate_adapter_generation2
    as adapter,
)


class FakeDevice:
    def __init__(self, device_type: str):
        self.type = device_type

    def __repr__(self) -> str:
        return self.type


class FakeTensor:
    def __init__(self, *, shape=(1, 7)):
        self.shape = shape
        self.to_device = None

    def to(self, device):
        self.to_device = device
        return self


class FakeGeneratedIds:
    def detach(self):
        return self

    def cpu(self):
        return self


class FakeOutput:
    def __getitem__(self, key):
        return FakeGeneratedIds()


class FakeInferenceMode:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeTorch:
    @staticmethod
    def inference_mode():
        return FakeInferenceMode()


class FakeTokenizer:
    pad_token_id = 0
    eos_token_id = 1

    def __init__(self):
        self.encoded = {
            "input_ids": FakeTensor(),
            "attention_mask": FakeTensor(),
        }

    def apply_chat_template(self, messages, **kwargs):
        return "prompt"

    def __call__(self, prompt, **kwargs):
        return self.encoded

    def decode(self, ids, **kwargs):
        return (
            "<tool_call><function=advance><parameter=ticks>50</parameter>"
            "</function></tool_call>"
        )


class FakeModel:
    def __init__(self, device):
        self.device = device
        self.generated = None

    def get_input_embeddings(self):
        class Embedding:
            pass

        embedding = Embedding()
        embedding.weight = type("Weight", (), {"device": self.device})()
        return embedding

    def generate(self, **kwargs):
        self.generated = kwargs
        return FakeOutput()


def runtime_for(device_type: str):
    return v8_runtime.FrozenV8LocalToolRuntime(
        model=FakeModel(FakeDevice(device_type)),
        tokenizer=FakeTokenizer(),
        torch_module=FakeTorch(),
    )


def tools():
    return v8_runtime.translate_campaign_turn_for_v8(
        state={
            "tick": 390,
            "economy": {"cash": 4700, "ore": 0, "harvester_count": 0},
            "power_balance": 60,
            "military": {},
            "units_summary": [],
            "buildings_summary": [],
            "enemy_summary": [],
            "enemy_buildings_summary": [],
            "production_items": [],
            "available_production": [],
            "map": {"width": 112, "height": 54, "name": "Singles"},
            "explored_percent": 4.25,
        },
        typed_tools=[{
            "type": "function",
            "function": {
                "name": "advance",
                "description": "advance",
                "parameters": {"type": "object", "properties": {}},
            },
        }],
        tool_contract={
            "production_contract_version": "typed-production-functions-v1",
            "legal_buildings": [],
            "legal_units": [],
            "production_functions": {},
            "offered_tool_names": ["advance"],
        },
        doctrine="FEINTER",
        round_no=1,
    )


@pytest.mark.parametrize("device_type", ["cpu", "cuda"])
def test_bound_generate_moves_every_encoded_tensor_to_embedding_device(device_type):
    runtime = runtime_for(device_type)
    turn = tools()
    expected_device = runtime.model.device

    adapter.bind_pair06_v8_offload_safe_generate(runtime)
    raw = runtime.generate(
        messages=turn["messages"],
        tools=turn["tools"],
    )

    assert raw.startswith("<tool_call>")
    assert runtime.tokenizer.encoded["input_ids"].to_device is expected_device
    assert runtime.tokenizer.encoded["attention_mask"].to_device is expected_device
    assert runtime.model.generated["input_ids"].to_device is expected_device
    assert runtime.model.generated["attention_mask"].to_device is expected_device


def test_meta_embedding_fails_closed_before_binding():
    runtime = runtime_for("meta")
    with pytest.raises(
        adapter.Pair06V8OffloadSafeGenerateHold,
        match="device unsupported",
    ):
        adapter.bind_pair06_v8_offload_safe_generate(runtime)


def test_double_binding_fails_closed():
    runtime = runtime_for("cpu")
    adapter.bind_pair06_v8_offload_safe_generate(runtime)
    with pytest.raises(
        adapter.Pair06V8OffloadSafeGenerateHold,
        match="already bound",
    ):
        adapter.bind_pair06_v8_offload_safe_generate(runtime)


def test_contract_changes_no_accepted_runtime_or_authority():
    out = adapter.pair06_v8_offload_safe_generate_adapter_contract()
    assert out["pair06_v8_offload_safe_generate_adapter_implemented"] is True
    assert out["pair06_v8_offload_safe_generate_adapter_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["accepted_v8_runtime_source_unchanged"] is True
    assert out["model_asset_bytes_unchanged"] is True
    assert out["tokenizer_asset_bytes_unchanged"] is True
    assert out["tool_translation_unchanged"] is True
    assert out["host_validation_unchanged"] is True
    assert out["generate_instance_method_only_replaced"] is True
    assert out["input_device_from_embedding_weight"] is True
    assert out["cpu_embedding_supported"] is True
    assert out["cuda_embedding_supported"] is True
    assert out["hard_coded_cuda_input_transfer_used"] is False
    assert out["model_load_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["automatic_retry"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False


def test_execution_entrypoint_holds():
    with pytest.raises(
        adapter.Pair06V8OffloadSafeGenerateHold,
        match="SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        adapter.execute_or_retry()
