from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_inference_safe_loader_generation2
    as loader,
)


class Device:
    def __init__(self, device_type: str, index=None):
        self.type = device_type
        self.index = index

    def __str__(self):
        if self.index is None:
            return self.type
        return f"{self.type}:{self.index}"


class Parameter:
    def __init__(self, device_type: str, index=None, size=1):
        self.device = Device(device_type, index)
        self._size = size

    def numel(self):
        return self._size


class Model:
    def __init__(self, parameters, *, embedding_device=("cuda", 0), device_map=None):
        self._parameters = parameters
        self.hf_device_map = device_map
        self._embedding = SimpleNamespace(
            weight=SimpleNamespace(
                device=Device(*embedding_device),
            )
        )

    def named_parameters(self):
        return list(self._parameters)

    def get_input_embeddings(self):
        return self._embedding


def test_contract_forbids_all_inference_offload_and_stays_non_authorizing():
    out = loader.pair06_v8_inference_safe_loader_contract()
    assert out["pair06_v8_inference_safe_loader_implemented"] is True
    assert out["pair06_v8_inference_safe_loader_reviewed"] is False
    assert out["device_map"] == {"": 0}
    assert out["single_gpu_cuda0_required"] is True
    assert out["offload_embedding"] is False
    assert out["cpu_embedding_offload_allowed"] is False
    assert out["cpu_parameter_offload_allowed"] is False
    assert out["disk_parameter_offload_allowed"] is False
    assert out["meta_parameter_allowed_after_load"] is False
    assert out["runtime_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_cuda0_model_passes_placement_admission():
    model = Model(
        [
            ("embed.weight", Parameter("cuda", 0, 10)),
            ("layer.0.weight", Parameter("cuda", 0, 20)),
        ],
        device_map={"": 0},
    )
    out = loader._assert_cuda_zero_resident(model)
    assert out["all_observed_device_maps_cuda0"] is True
    assert out["all_parameters_cuda0"] is True
    assert out["input_embedding_cuda0"] is True
    assert out["parameter_count"] == 2
    assert out["parameter_numel"] == 30


@pytest.mark.parametrize(
    ("name", "device_type"),
    [
        ("cpu_layer", "cpu"),
        ("meta_layer", "meta"),
    ],
)
def test_cpu_or_meta_parameter_fails_closed(name, device_type):
    model = Model(
        [(name, Parameter(device_type))],
        embedding_device=("cuda", 0),
        device_map={"": 0},
    )
    with pytest.raises(
        loader.Pair06V8InferenceSafeLoaderHold,
        match="PARAMETER_NOT_CUDA0",
    ):
        loader._assert_cuda_zero_resident(model)


@pytest.mark.parametrize("value", ["cpu", "disk", "meta", "cuda:1", 1])
def test_non_cuda0_device_map_entry_fails_closed(value):
    model = Model(
        [("layer.weight", Parameter("cuda", 0))],
        device_map={"language_model.layers.0": value},
    )
    with pytest.raises(
        loader.Pair06V8InferenceSafeLoaderHold,
        match="OFFLOAD_FORBIDDEN",
    ):
        loader._assert_cuda_zero_resident(model)


def test_cpu_embedding_fails_closed_even_when_other_parameters_are_cuda():
    model = Model(
        [("layer.weight", Parameter("cuda", 0))],
        embedding_device=("cpu", None),
        device_map={"": 0},
    )
    with pytest.raises(
        loader.Pair06V8InferenceSafeLoaderHold,
        match="EMBEDDING_NOT_CUDA0",
    ):
        loader._assert_cuda_zero_resident(model)


def test_execution_entrypoint_holds():
    with pytest.raises(
        loader.Pair06V8InferenceSafeLoaderHold,
        match="SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        loader.execute_or_retry()
