from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_binding_source_and_tests():
    out = review.pair06_v8_host_path_binding_review_contract()
    assert out["binding_git_blob"] == (
        "e92b0bc331e709e5eecbba1e4321aea0f9935bd3"
    )
    assert out["binding_source_sha256"] == (
        "827e216fde7c8c4eee4a7e51e89f272c417911a53bb787764e55eddf08b79079"
    )
    assert out["binding_test_git_blob"] == (
        "1e9a0acbca174800beb2f2003b5fd17efbaa01d1"
    )
    assert out["binding_test_sha256"] == (
        "b72147cf4c8f8dc2ab6a3bcc979c5aae7814e4112a0494ab47f8b09eb3e350d6"
    )


def test_review_confirms_exact_bound_paths():
    out = review.pair06_v8_host_path_binding_review_contract()
    assert out["pair06_v8_host_path_binding_reviewed"] is True
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
    assert out["verified_asset_count"] == 17


def test_review_requires_exact_runtime_environment_observation():
    out = review.pair06_v8_host_path_binding_review_contract()
    assert out["runtime_environment_observation_required"] is True
    assert out["expected_runtime_python_major_minor"] == (3, 12)
    assert out["expected_runtime_pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )
    assert out["runtime_environment_observed"] is False
    assert out["runtime_environment_admitted"] is False


def test_review_keeps_runtime_and_mutation_authority_closed():
    out = review.pair06_v8_host_path_binding_review_contract()
    for field in (
        "runtime_load_authorized",
        "runtime_load_performed",
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_environment_observation():
    out = review.pair06_v8_host_path_binding_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
    )


def test_environment_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8HostPathBindingReviewHold,
        match="PAIR06_V8_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    ):
        review.observe_runtime_environment()
    with pytest.raises(
        review.Pair06V8HostPathBindingReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
