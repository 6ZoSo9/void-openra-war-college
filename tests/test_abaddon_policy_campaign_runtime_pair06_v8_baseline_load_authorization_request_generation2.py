from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_request_generation2
    as request,
)


def test_request_binds_exact_reviewed_runtime_inputs():
    out = request.pair06_v8_baseline_load_authorization_request_contract()
    assert out["environment_review_git_blob"] == (
        "212ac021820e75bd53938f7df4c8610f51c077f7"
    )
    assert out["host_path_review_git_blob"] == (
        "c162a8013894ebcb6f310432c96e7daf2c9de3d0"
    )
    assert out["capability_review_git_blob"] == (
        "8e405b4d03a7a7310dbedd9fae0edbe9976b4637"
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["runtime_selection_key"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    assert out["activation_kind"] == "inprocess_accepted_v8_runtime"
    assert out["model_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
    )
    assert out["adapter_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
    )
    assert out["python_path"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
    )
    assert out["python_major_minor"] == (3, 12)
    assert out["pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )


def test_request_requests_but_does_not_grant_runtime_load_authority():
    out = request.pair06_v8_baseline_load_authorization_request_contract()
    assert out["runtime_load_authorization_request_implemented"] is True
    assert out["runtime_load_authorization_request_reviewed"] is False
    assert out["runtime_load_authorization_requested"] is True
    assert out["runtime_load_authorized"] is False
    assert out["runtime_load_performed"] is False
    assert out["candidate_runtime_load_requested"] is False
    assert out["candidate_runtime_load_authorized"] is False
    assert out["pair15_execution_authorized"] is False


def test_request_preserves_reviewed_preload_boundaries():
    out = request.pair06_v8_baseline_load_authorization_request_contract()
    assert out["exact_17_asset_verification_reviewed"] is True
    assert out["runtime_environment_observation_reviewed"] is True
    assert out["runtime_environment_admitted"] is True
    assert out["runtime_environment_path_bound"] is True
    assert out["automatic_retry"] is False


def test_request_keeps_execution_and_mutation_closed():
    out = request.pair06_v8_baseline_load_authorization_request_contract()
    for field in (
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "game_mutation_performed",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_request_frontier_is_explicit_human_authorization():
    out = request.pair06_v8_baseline_load_authorization_request_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED"
    )


def test_authorization_load_and_game_entrypoints_hold():
    with pytest.raises(
        request.Pair06V8BaselineLoadAuthorizationRequestHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED",
    ):
        request.authorize_runtime_load()
    with pytest.raises(
        request.Pair06V8BaselineLoadAuthorizationRequestHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        request.load_runtime()
    with pytest.raises(
        request.Pair06V8BaselineLoadAuthorizationRequestHold,
        match="PAIR06_BASELINE_GAME_EXECUTION_NOT_AUTHORIZED",
    ):
        request.execute_game()
