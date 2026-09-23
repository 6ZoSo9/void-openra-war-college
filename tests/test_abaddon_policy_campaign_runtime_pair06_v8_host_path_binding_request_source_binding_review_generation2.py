from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_request_source_and_tests():
    out = review.pair06_v8_host_path_binding_request_review_contract()
    assert out["request_git_blob"] == (
        "ea2b399f7c3fe26caca43524c0c5b79a638e92fa"
    )
    assert out["request_source_sha256"] == (
        "923bac4c770648d9d75c319cfd849845bf7f7159b0a533b3e9083ff46885769a"
    )
    assert out["request_test_git_blob"] == (
        "22fd9fc5cb714e24a0d85b3f1df87a2b7ed685e4"
    )
    assert out["request_test_sha256"] == (
        "5a00f73719e22139e70c4912d8185c18cfe695f045fb438f879ea7583895db26"
    )


def test_review_confirms_precision_observation_frontier():
    out = review.pair06_v8_host_path_binding_request_review_contract()
    assert out["pair06_v8_host_path_binding_request_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["precision_host_observation_required"] is True
    assert out["host_observation_performed"] is False
    assert out["model_dir_path_bound"] is False
    assert out["adapter_dir_path_bound"] is False


def test_review_preserves_exact_asset_manifest():
    out = review.pair06_v8_host_path_binding_request_review_contract()
    assert out["required_asset_count"] == 17
    assert len(out["required_asset_manifest"]) == 17
    assert out["exact_hash_match_required_for_every_asset"] is True
    assert out["model_and_adapter_directories_must_be_distinct"] is True
    assert out["symlinked_required_files_allowed"] is False


def test_review_keeps_runtime_and_mutation_authority_closed():
    out = review.pair06_v8_host_path_binding_request_review_contract()
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


def test_review_advances_only_to_precision_host_observation():
    out = review.pair06_v8_host_path_binding_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED"
    )


def test_observation_and_load_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8HostPathBindingRequestReviewHold,
        match="PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED",
    ):
        review.observe_precision_host()
    with pytest.raises(
        review.Pair06V8HostPathBindingRequestReviewHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.load_runtime()
