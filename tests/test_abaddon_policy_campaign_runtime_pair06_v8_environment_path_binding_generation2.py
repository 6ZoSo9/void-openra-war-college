from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_path_binding_generation2
    as binding,
)


def test_binding_consumes_reviewed_environment_observation():
    out = binding.pair06_v8_environment_path_binding_contract()
    assert out["observation_review_git_blob"] == (
        "0f1aa52169d01bb6d384e4858253d07e46e31311"
    )
    assert out["observation_review_source_sha256"] == (
        "1e52c7feb497241e7b453ca9047917ab456dc86d21523699ace3b3f5916b14b1"
    )
    assert out["pair06_v8_environment_path_binding_implemented"] is True
    assert out["pair06_v8_environment_path_binding_reviewed"] is False


def test_binding_sets_exact_python_environment():
    out = binding.pair06_v8_environment_path_binding_contract()
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["work_root"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
    )
    assert out["python_path"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
    )
    assert out["python_path_bound"] is True
    assert out["python_major_minor"] == (3, 12)
    assert out["pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )
    assert out["runtime_environment_observation_reviewed"] is True
    assert out["runtime_environment_admitted"] is True
    assert out["runtime_environment_path_bound"] is True
    assert out["runtime_environment_path_binding_performs_host_io"] is False
    assert binding.bound_pair06_v8_environment() == {
        "python_path": out["python_path"],
        "python_major_minor": out["python_major_minor"],
        "pip_freeze_sha256": out["pip_freeze_sha256"],
    }


def test_binding_keeps_runtime_and_mutation_authority_closed():
    out = binding.pair06_v8_environment_path_binding_contract()
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


def test_binding_advances_only_to_separate_source_review():
    out = binding.pair06_v8_environment_path_binding_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_runtime_load_entrypoint_holds():
    with pytest.raises(
        binding.Pair06V8EnvironmentPathBindingHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        binding.load_runtime()
