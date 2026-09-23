from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_path_binding_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_binding_source_and_tests():
    out = review.pair06_v8_environment_path_binding_review_contract()
    assert out["binding_git_blob"] == (
        "fef22e79e6ca32ace9f018384692d2a9814d1013"
    )
    assert out["binding_source_sha256"] == (
        "e7b825486be3473214b0dd5d9e42ec18b99d86cf39bf66b3afbc133070342c7c"
    )
    assert out["binding_test_git_blob"] == (
        "b162a7475b5a988ce1cdcb02d25514fb4c7aa7cc"
    )
    assert out["binding_test_sha256"] == (
        "7015384640cfac2604fb8e5821dbe85877d2569a94b911914336b4c7f05528dc"
    )


def test_review_confirms_exact_bound_environment():
    out = review.pair06_v8_environment_path_binding_review_contract()
    assert out["pair06_v8_environment_path_binding_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
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


def test_review_keeps_runtime_and_mutation_authority_closed():
    out = review.pair06_v8_environment_path_binding_review_contract()
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


def test_review_advances_only_to_runtime_load_authorization_request():
    out = review.pair06_v8_environment_path_binding_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_LOAD_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_LOAD_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_request_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8EnvironmentPathBindingReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_runtime_load_authorization()
    with pytest.raises(
        review.Pair06V8EnvironmentPathBindingReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
