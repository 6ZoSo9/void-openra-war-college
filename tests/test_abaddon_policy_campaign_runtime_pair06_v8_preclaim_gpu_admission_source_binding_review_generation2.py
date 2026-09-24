from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_admission_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_preclaim_gpu_admission_source_and_test():
    out = review.pair06_v8_preclaim_gpu_admission_review_contract()
    assert out["admission_git_blob"] == (
        "af50d685fcb3eb8d1879289e5cf2667743a117ed"
    )
    assert out["admission_source_sha256"] == (
        "8ed38a671cba24940d6612d2cdb15cf813db67ad82ee817774f9450eb547dd29"
    )
    assert out["admission_test_git_blob"] == (
        "061ee4e89413d0ecd79eea62da89111afe52cb8d"
    )
    assert out["admission_test_sha256"] == (
        "8c842e15c21eb10f148e9296fe76c6f8d4b22dbd91dba4482a9621fa75cd1a57"
    )


def test_review_preserves_preclaim_gpu_admission_invariants():
    out = review.pair06_v8_preclaim_gpu_admission_review_contract()
    assert out["pair06_v8_preclaim_gpu_admission_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["gpu_index"] == 0
    assert out["foreign_compute_processes_allowed"] is False
    assert out["minimum_free_memory_fraction"] == {
        "numerator": 9,
        "denominator": 10,
    }
    assert out["admission_must_precede_attempt_marker"] is True
    assert out["read_only_observer_required"] is True
    assert out["prior_attempt_reusable"] is False


def test_review_remains_non_authorizing():
    out = review.pair06_v8_preclaim_gpu_admission_review_contract()
    for field in (
        "retry_authorized",
        "execution_authorized",
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


def test_review_advances_only_to_readonly_observer():
    out = review.pair06_v8_preclaim_gpu_admission_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_REQUIRED"


def test_runtime_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PreclaimGpuAdmissionReviewHold,
        match="PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_REQUIRED",
    ):
        review.observe_or_execute()
