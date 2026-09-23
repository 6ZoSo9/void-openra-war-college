from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_environment_observation_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_precision_environment():
    out = acceptance.pair06_v8_precision_environment_observation_acceptance_contract()
    assert out["pair06_v8_precision_environment_observation_accepted"] is True
    assert out["observer_sha256"] == (
        "371995496abafd6fda7f562aa4d2bbceb8c7b107d7345cfb5c2a1b5e069dafff"
    )
    assert out["accepted_python"] == (
        "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
    )
    assert out["accepted_python_major_minor"] == (3, 12)
    assert out["accepted_pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )


def test_accepted_observation_is_unique_and_bounded():
    out = acceptance.accept_pair06_v8_precision_environment_observation(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 6
    assert out["held_out"] is False
    assert out["python_bin_directory_count"] == 1
    assert out["accepted_interpreter_candidate_count"] == 1
    assert out["runtime_environment_observed"] is True
    assert out["runtime_environment_admitted"] is True
    assert out["runtime_environment_path_binding_eligible"] is True
    assert out["runtime_environment_path_bound"] is False
    assert out["filesystem_scan_read_only"] is True
    assert out["pip_freeze_observation_read_only"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("python_bin_directory_count", 2),
        ("accepted_interpreter_candidate_count", 0),
        ("accepted_python", "/tmp/python3.12"),
        ("accepted_python_major_minor", (3, 11)),
        ("accepted_pip_freeze_sha256", "0" * 64),
        ("accepted_v8_runtime_environment_validator_green", False),
        ("runtime_environment_admitted", False),
        ("model_load", True),
        ("model_inference", True),
        ("game_execution", True),
        ("pair15_execution", True),
    ],
)
def test_environment_evidence_mutation_is_rejected(field, value):
    evidence = dict(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.Pair06V8PrecisionEnvironmentObservationAcceptanceHold,
        match="pair06 V8 environment evidence drift",
    ):
        acceptance.accept_pair06_v8_precision_environment_observation(evidence)


def test_acceptance_keeps_runtime_and_mutation_authority_closed():
    out = acceptance.accept_pair06_v8_precision_environment_observation(
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
    out = acceptance.pair06_v8_precision_environment_observation_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_binding_and_load_entrypoints_hold():
    with pytest.raises(
        acceptance.Pair06V8PrecisionEnvironmentObservationAcceptanceHold,
        match="PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.bind_environment_path()
    with pytest.raises(
        acceptance.Pair06V8PrecisionEnvironmentObservationAcceptanceHold,
        match="PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        acceptance.load_runtime()
