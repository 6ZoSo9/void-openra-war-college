from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_environment_observation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_tests():
    out = review.pair06_v8_precision_environment_observation_review_contract()
    assert out["acceptance_git_blob"] == (
        "3d054bdc04497da10f718141b357eaa35192cbc7"
    )
    assert out["acceptance_source_sha256"] == (
        "3e50e5a1735bd755b127705e1dabd7facbeed4baf0ce934d1b1b77652f6a79b7"
    )
    assert out["acceptance_test_git_blob"] == (
        "ca51273f9018b87801b7ae4b1bddc4944f03cb6e"
    )
    assert out["acceptance_test_sha256"] == (
        "9c8232a32029bfdd6288c3f8add3987b21ebb509bb15f498a76ae71f359c1266"
    )


def test_review_confirms_exact_accepted_environment():
    out = review.pair06_v8_precision_environment_observation_review_contract()
    assert out["pair06_v8_precision_environment_observation_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["work_root"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
    )
    assert out["accepted_python"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
    )
    assert out["accepted_python_major_minor"] == (3, 12)
    assert out["accepted_pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )
    assert out["python_bin_directory_count"] == 1
    assert out["accepted_interpreter_candidate_count"] == 1
    assert out["runtime_environment_observed"] is True
    assert out["runtime_environment_admitted"] is True
    assert out["runtime_environment_path_binding_eligible"] is True
    assert out["runtime_environment_path_bound"] is False


def test_review_keeps_runtime_and_mutation_authority_closed():
    out = review.pair06_v8_precision_environment_observation_review_contract()
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


def test_review_advances_only_to_environment_path_binding_source():
    out = review.pair06_v8_precision_environment_observation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_REQUIRED"
    )


def test_binding_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8PrecisionEnvironmentObservationReviewHold,
        match="PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_REQUIRED",
    ):
        review.bind_environment_path()
    with pytest.raises(
        review.Pair06V8PrecisionEnvironmentObservationReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
