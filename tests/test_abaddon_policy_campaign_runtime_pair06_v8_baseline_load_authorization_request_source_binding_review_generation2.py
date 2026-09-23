from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_request_source_and_tests():
    out = review.pair06_v8_baseline_load_authorization_request_review_contract()
    assert out["request_git_blob"] == (
        "9c0dd9c22c56dcc9656fda6d860420dff0653cff"
    )
    assert out["request_source_sha256"] == (
        "6bd28bbaaad3f6deb779ce8e6e1b85ebf9afba4f5053dff3547a7c27e5565ddd"
    )
    assert out["request_test_git_blob"] == (
        "ed6d4b5f5558c10a9934ad623a8125ba2a5d8509"
    )
    assert out["request_test_sha256"] == (
        "a0aaf7d9d52e55b2569efeb7f4b842318ab9d53cb2c3174ccfc4a35548e506c8"
    )


def test_review_confirms_baseline_only_load_request():
    out = review.pair06_v8_baseline_load_authorization_request_review_contract()
    assert out["pair06_v8_baseline_load_authorization_request_reviewed"] is True
    assert out["runtime_load_authorization_requested"] is True
    assert out["runtime_load_authorized"] is False
    assert out["runtime_load_performed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["candidate_runtime_load_requested"] is False
    assert out["candidate_runtime_load_authorized"] is False
    assert out["pair15_execution_authorized"] is False


def test_review_preserves_exact_runtime_inputs():
    out = review.pair06_v8_baseline_load_authorization_request_review_contract()
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


def test_review_keeps_execution_and_mutation_closed():
    out = review.pair06_v8_baseline_load_authorization_request_review_contract()
    for field in (
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_review_frontier_is_explicit_human_authorization():
    out = review.pair06_v8_baseline_load_authorization_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED"
    )


def test_authorization_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8BaselineLoadAuthorizationRequestReviewHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_runtime_load()
    with pytest.raises(
        review.Pair06V8BaselineLoadAuthorizationRequestReviewHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
