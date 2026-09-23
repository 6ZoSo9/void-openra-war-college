from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_request_generation2
    as request,
)


def test_request_binds_exact_reviewed_capability():
    out = request.pair06_v8_host_path_binding_request_contract()
    assert out["capability_review_git_blob"] == (
        "8e405b4d03a7a7310dbedd9fae0edbe9976b4637"
    )
    assert out["capability_review_source_sha256"] == (
        "5c4836135629ea47e5e38f6aff0bc61201f754b8354152768e9fbf89c5e000fb"
    )
    assert out["v8_runtime_git_blob"] == (
        "fd0e72767ba199e88af9e9eb2455c03ace027a14"
    )


def test_request_defines_exact_17_file_manifest():
    out = request.pair06_v8_host_path_binding_request_contract()
    assert out["required_model_asset_count"] == 12
    assert out["required_adapter_asset_count"] == 5
    assert out["required_asset_count"] == 17
    manifest = out["required_asset_manifest"]
    assert len(manifest) == 17
    assert sum(row["scope"] == "model_dir" for row in manifest) == 12
    assert sum(row["scope"] == "adapter_dir" for row in manifest) == 5
    for row in manifest:
        assert row["relative_path"]
        assert len(row["sha256"]) == 64
        assert set(row["sha256"]) <= set("0123456789abcdef")


def test_request_has_no_host_observation_or_binding():
    out = request.pair06_v8_host_path_binding_request_contract()
    assert out["pair_slot"] == 6
    assert out["host_path_binding_request_implemented"] is True
    assert out["host_path_binding_request_reviewed"] is False
    assert out["precision_host_observation_required"] is True
    assert out["host_observation_performed"] is False
    assert out["filesystem_scan_performed_by_contract"] is False
    assert out["model_dir_path_bound"] is False
    assert out["adapter_dir_path_bound"] is False
    assert out["model_dir_candidate_count"] == 0
    assert out["adapter_dir_candidate_count"] == 0


def test_request_requires_exact_hashes_and_plain_files():
    out = request.pair06_v8_host_path_binding_request_contract()
    assert out["exact_hash_match_required_for_every_asset"] is True
    assert out["model_and_adapter_directories_must_be_distinct"] is True
    assert out["symlinked_required_files_allowed"] is False


def test_request_keeps_runtime_and_mutation_authority_closed():
    out = request.pair06_v8_host_path_binding_request_contract()
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


def test_request_advances_only_to_precision_host_observation():
    out = request.pair06_v8_host_path_binding_request_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED"
    )


def test_binding_and_load_entrypoints_hold():
    with pytest.raises(
        request.Pair06V8HostPathBindingRequestHold,
        match="PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED",
    ):
        request.bind_host_paths()
    with pytest.raises(
        request.Pair06V8HostPathBindingRequestHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        request.load_runtime()
