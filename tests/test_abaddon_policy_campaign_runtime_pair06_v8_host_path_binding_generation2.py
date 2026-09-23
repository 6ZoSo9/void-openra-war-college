from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_generation2
    as binding,
)


def test_binding_consumes_reviewed_precision_observation():
    out = binding.pair06_v8_host_path_binding_contract()
    assert out["observation_review_git_blob"] == (
        "fb0fd4e5ad042c37f428265ea18919ee93b3cf5c"
    )
    assert out["observation_review_source_sha256"] == (
        "07977371fb89e5d87ea30c292a72e31eda2ba719b21813963c80f9fd9f6dd34c"
    )
    assert out["pair06_v8_host_path_binding_implemented"] is True
    assert out["pair06_v8_host_path_binding_reviewed"] is False


def test_binding_sets_exact_precision_paths():
    out = binding.pair06_v8_host_path_binding_contract()
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["model_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
    )
    assert out["adapter_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
    )
    assert out["model_dir_path_bound"] is True
    assert out["adapter_dir_path_bound"] is True
    assert out["model_and_adapter_directories_distinct"] is True
    assert out["verified_asset_count"] == 17
    assert (
        out["asset_hash_verification_inherited_from_reviewed_precision_observation"]
        is True
    )
    assert binding.bound_pair06_v8_paths() == {
        "model_dir": out["model_dir"],
        "adapter_dir": out["adapter_dir"],
    }


def test_binding_requires_runtime_environment_observation():
    out = binding.pair06_v8_host_path_binding_contract()
    assert out["runtime_environment_observation_required"] is True
    assert out["expected_runtime_python_major_minor"] == (3, 12)
    assert len(out["expected_runtime_pip_freeze_sha256"]) == 64
    assert out["runtime_environment_observed"] is False
    assert out["runtime_environment_admitted"] is False


def test_binding_keeps_runtime_and_mutation_authority_closed():
    out = binding.pair06_v8_host_path_binding_contract()
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
        assert out[field] is False


def test_binding_advances_only_to_environment_observation():
    out = binding.pair06_v8_host_path_binding_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
    )


def test_environment_and_load_entrypoints_hold():
    with pytest.raises(
        binding.Pair06V8HostPathBindingHold,
        match="PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    ):
        binding.observe_runtime_environment()
    with pytest.raises(
        binding.Pair06V8HostPathBindingHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        binding.load_runtime()
