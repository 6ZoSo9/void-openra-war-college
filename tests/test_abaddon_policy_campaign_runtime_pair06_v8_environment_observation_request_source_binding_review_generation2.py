from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_observation_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_request_source_and_tests():
    out = review.pair06_v8_environment_observation_request_review_contract()
    assert out["request_git_blob"] == (
        "840c518d9d8f21ae09390fde42fcc376125076d6"
    )
    assert out["request_source_sha256"] == (
        "6c4ad1b99e7de071da4d29edfe9b7e5c378b72839e96701dde1e26d10217f2d8"
    )
    assert out["request_test_git_blob"] == (
        "5e5a588d625af6fc1ce224878845b4948fb78eb5"
    )
    assert out["request_test_sha256"] == (
        "4223801ceca584499956efdbe0d991f8c450475739cfaced76bf9daffb8d2339"
    )


def test_review_confirms_exact_environment_observation_request():
    out = review.pair06_v8_environment_observation_request_review_contract()
    assert out["pair06_v8_environment_observation_request_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["work_root"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
    )
    assert out["interpreter_discovery_scope"] == "bounded_known_v8_work_root"
    assert out["expected_python_major_minor"] == (3, 12)
    assert out["expected_pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )
    assert out["exactly_one_accepted_interpreter_required"] is True
    assert out["pip_freeze_observation_read_only"] is True


def test_review_keeps_environment_and_runtime_unobserved():
    out = review.pair06_v8_environment_observation_request_review_contract()
    assert out["runtime_environment_observed"] is False
    assert out["runtime_environment_admitted"] is False
    assert out["runtime_environment_path_bound"] is False
    assert out["runtime_load_authorized"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False


def test_review_keeps_mutation_authority_closed():
    out = review.pair06_v8_environment_observation_request_review_contract()
    for field in (
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_precision_environment_observation():
    out = review.pair06_v8_environment_observation_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
    )


def test_observation_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8EnvironmentObservationRequestReviewHold,
        match="PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
    ):
        review.observe_precision_environment()
    with pytest.raises(
        review.Pair06V8EnvironmentObservationRequestReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
