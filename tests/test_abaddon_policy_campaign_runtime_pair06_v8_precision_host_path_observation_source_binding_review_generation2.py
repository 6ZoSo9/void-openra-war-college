from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_host_path_observation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_tests():
    out = review.pair06_v8_precision_host_path_observation_review_contract()
    assert out["acceptance_git_blob"] == (
        "df31976eba984e5e2ee35250043a836059c835ef"
    )
    assert out["acceptance_source_sha256"] == (
        "e852c56a7f3cbe97998fb4363eaacf57463895babf11b62f4332c010d986f872"
    )
    assert out["acceptance_test_git_blob"] == (
        "5f9a74bc8a26fa0d1fed5fe3119e275d85cfaa2c"
    )
    assert out["acceptance_test_sha256"] == (
        "1587df7abb5a63544c39a87f067246587f6bec671bac7098ad3bbac7731b4180"
    )


def test_review_confirms_exact_host_paths_and_assets():
    out = review.pair06_v8_precision_host_path_observation_review_contract()
    assert out["pair06_v8_precision_host_path_observation_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["model_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
    )
    assert out["adapter_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
    )
    assert out["model_dir_candidate_count"] == 1
    assert out["adapter_dir_candidate_count"] == 1
    assert out["verified_asset_count"] == 17
    assert out["all_required_assets_exact_hash_verified"] is True
    assert out["host_asset_mutation"] is False
    assert out["model_dir_path_binding_eligible"] is True
    assert out["adapter_dir_path_binding_eligible"] is True


def test_review_keeps_runtime_and_mutation_authority_closed():
    out = review.pair06_v8_precision_host_path_observation_review_contract()
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


def test_review_advances_only_to_host_path_binding_source():
    out = review.pair06_v8_precision_host_path_observation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_HOST_PATH_BINDING_SOURCE_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_HOST_PATH_BINDING_SOURCE_REQUIRED"


def test_binding_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8PrecisionHostPathObservationReviewHold,
        match="PAIR06_V8_HOST_PATH_BINDING_SOURCE_REQUIRED",
    ):
        review.bind_host_paths()
    with pytest.raises(
        review.Pair06V8PrecisionHostPathObservationReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
