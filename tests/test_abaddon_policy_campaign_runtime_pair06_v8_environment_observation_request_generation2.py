from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_observation_request_generation2
    as request,
)


def test_request_binds_reviewed_host_path_binding():
    out = request.pair06_v8_environment_observation_request_contract()
    assert out["path_review_git_blob"] == (
        "c162a8013894ebcb6f310432c96e7daf2c9de3d0"
    )
    assert out["path_review_source_sha256"] == (
        "49c4f44f6f164595fb9c50290b81aa56b62261b4924e859dfd7383a6e84ad07a"
    )
    assert out["pair_slot"] == 6
    assert out["held_out"] is False


def test_request_defines_exact_v8_environment_identity():
    out = request.pair06_v8_environment_observation_request_contract()
    assert out["work_root"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
    )
    assert out["interpreter_discovery_scope"] == "bounded_known_v8_work_root"
    assert out["interpreter_candidate_count"] == 0
    assert out["expected_python_major_minor"] == (3, 12)
    assert out["expected_pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )
    assert out["exactly_one_accepted_interpreter_required"] is True
    assert out["pip_freeze_observation_read_only"] is True


def test_request_performs_no_environment_observation():
    out = request.pair06_v8_environment_observation_request_contract()
    assert out["pair06_v8_environment_observation_request_implemented"] is True
    assert out["pair06_v8_environment_observation_request_reviewed"] is False
    assert out["runtime_environment_observed"] is False
    assert out["runtime_environment_admitted"] is False
    assert out["runtime_environment_path_bound"] is False


def test_request_keeps_runtime_and_mutation_authority_closed():
    out = request.pair06_v8_environment_observation_request_contract()
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


def test_request_advances_only_to_precision_environment_observation():
    out = request.pair06_v8_environment_observation_request_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
    )


def test_observation_and_load_entrypoints_hold():
    with pytest.raises(
        request.Pair06V8EnvironmentObservationRequestHold,
        match="PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    ):
        request.observe_precision_environment()
    with pytest.raises(
        request.Pair06V8EnvironmentObservationRequestHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        request.load_runtime()
