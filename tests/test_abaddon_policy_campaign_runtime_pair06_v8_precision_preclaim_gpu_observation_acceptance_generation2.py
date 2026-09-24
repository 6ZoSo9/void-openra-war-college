from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_preclaim_gpu_observation_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_clean_precision_gpu_evidence():
    out = acceptance.pair06_v8_precision_preclaim_gpu_observation_acceptance_contract()
    assert out["pair06_v8_precision_preclaim_gpu_observation_accepted"] is True
    assert out["observer_sha256"] == (
        "899c77ff6dfa9d2708152754a1b073f9f856703e6eebffd282599a1672eec156"
    )
    assert out["canonical_main_head"] == (
        "b75d7a056d3aa6742532697c21758bcf733ab28b"
    )
    assert out["accepted_evidence_sha256"] == (
        "8ccd26d5a90cda5e75d6b7ce93501ddb240f5d9da2cf56f518f5ce9c96519237"
    )
    assert out["free_fraction_ppm"] == 909708
    assert out["compute_process_count"] == 0


def test_acceptance_pins_reviewed_observer_source():
    out = acceptance.pair06_v8_precision_preclaim_gpu_observation_acceptance_contract()
    assert out["observer_review_git_blob"] == (
        "37ea632d973d6bba7e4cc7210dedcfc7c1fd8025"
    )
    assert out["observer_review_source_sha256"] == (
        "81a676bdd69694282d9d36d1f673ea07fe600bba736b1958064c04a0c075ebfb"
    )


def test_accepted_snapshot_is_clean_but_nonreusable():
    out = acceptance.accept_pair06_v8_precision_preclaim_gpu_observation(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 6
    assert out["gpu_index"] == 0
    assert out["total_memory_bytes"] == 12820938752
    assert out["free_memory_bytes"] == 11663310848
    assert out["free_fraction_ppm"] == 909708
    assert out["compute_process_count"] == 0
    assert out["compute_processes"] == ()
    assert out["preclaim_gpu_admitted_at_observation"] is True
    assert out["historical_observation_only"] is True
    assert out["observation_reusable_for_future_claim"] is False
    assert out["fresh_reobservation_required_before_attempt_marker"] is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("free_memory_bytes", 5993660416),
        ("free_fraction_ppm", 467489),
        ("compute_process_count", 1),
        ("compute_processes", ({"pid": 2850305, "used_memory_bytes": 5695864832},)),
        ("observation_read_only", False),
        ("attempt_marker_created", True),
        ("model_load_performed", True),
        ("model_inference_performed", True),
        ("game_execution_performed", True),
        ("preclaim_gpu_admitted", False),
        ("admission_hold", "PAIR06_V8_PRECLAIM_GPU_FOREIGN_COMPUTE_PROCESS_HOLD"),
        ("observation_result", "HOLD"),
        ("observation_reusable_for_future_claim", True),
        ("retry_authorized", True),
        ("execution_authorized", True),
    ],
)
def test_precision_gpu_evidence_mutation_is_rejected(field, value):
    evidence = dict(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.Pair06V8PrecisionPreclaimGpuObservationAcceptanceHold,
        match="pair06 GPU evidence drift",
    ):
        acceptance.accept_pair06_v8_precision_preclaim_gpu_observation(evidence)


def test_acceptance_keeps_retry_and_execution_authority_closed():
    out = acceptance.accept_pair06_v8_precision_preclaim_gpu_observation(
        acceptance.EXPECTED_EVIDENCE
    )
    for field in (
        "retry_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
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
    out = acceptance.pair06_v8_precision_preclaim_gpu_observation_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECISION_PRECLAIM_GPU_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECISION_PRECLAIM_GPU_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_claim_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8PrecisionPreclaimGpuObservationAcceptanceHold,
        match="PAIR06_V8_PRECISION_PRECLAIM_GPU_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.claim_or_execute()
