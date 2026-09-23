from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_host_path_observation_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_precision_observation():
    out = acceptance.pair06_v8_precision_host_path_observation_acceptance_contract()
    assert out["pair06_v8_precision_host_path_observation_accepted"] is True
    assert out["observer_sha256"] == (
        "033f3ded80191902d74687c5f12a5f03e9f12d956a7c293ee706999acdf59c18"
    )
    assert out["model_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
    )
    assert out["adapter_dir"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
    )
    assert out["verified_asset_count"] == 17


def test_accepted_observation_is_bounded_and_exact():
    out = acceptance.accept_pair06_v8_precision_host_path_observation(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["model_dir_candidate_count"] == 1
    assert out["adapter_dir_candidate_count"] == 1
    assert out["all_required_assets_exact_hash_verified"] is True
    assert out["host_observation_completed"] is True
    assert out["host_observation_green"] is True
    assert out["host_asset_mutation"] is False
    assert out["model_dir_path_binding_eligible"] is True
    assert out["adapter_dir_path_binding_eligible"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model_dir_candidate_count", 2),
        ("adapter_dir_candidate_count", 0),
        ("verified_asset_count", 16),
        ("accepted_v8_asset_verifier_green", False),
        ("host_asset_mutation", True),
        ("model_load", True),
        ("model_inference", True),
        ("game_execution", True),
        ("pair15_execution", True),
    ],
)
def test_observation_mutation_is_rejected(field, value):
    evidence = dict(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.Pair06V8PrecisionHostPathObservationAcceptanceHold,
        match="pair06 V8 observation evidence drift",
    ):
        acceptance.accept_pair06_v8_precision_host_path_observation(evidence)


def test_acceptance_keeps_runtime_and_mutation_authority_closed():
    out = acceptance.accept_pair06_v8_precision_host_path_observation(
        acceptance.EXPECTED_EVIDENCE
    )
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


def test_acceptance_advances_only_to_separate_source_review():
    out = acceptance.pair06_v8_precision_host_path_observation_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_binding_and_load_entrypoints_hold():
    with pytest.raises(
        acceptance.Pair06V8PrecisionHostPathObservationAcceptanceHold,
        match="PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.bind_host_paths()
    with pytest.raises(
        acceptance.Pair06V8PrecisionHostPathObservationAcceptanceHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        acceptance.load_runtime()
