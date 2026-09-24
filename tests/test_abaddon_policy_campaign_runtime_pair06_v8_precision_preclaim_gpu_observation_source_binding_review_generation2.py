from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_preclaim_gpu_observation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_test():
    out = review.pair06_v8_precision_preclaim_gpu_observation_review_contract()
    assert out["acceptance_git_blob"] == (
        "d7ce43d57a0640a15f84a9de66f4897bf0b71307"
    )
    assert out["acceptance_source_sha256"] == (
        "169223f26bf706bc87d48c365549e6a5148bf3bd755709e4eb4e35d729172daf"
    )
    assert out["acceptance_test_git_blob"] == (
        "7e296d2fffc3d3e56c89aed9eef6f21c4482e701"
    )
    assert out["acceptance_test_sha256"] == (
        "04bb4a78053b201a44a571d38343d7086cb1ffb0b12aa9559702e793df92980c"
    )


def test_review_confirms_exact_clean_precision_gpu_observation():
    out = review.pair06_v8_precision_preclaim_gpu_observation_review_contract()
    assert out["pair06_v8_precision_preclaim_gpu_observation_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["gpu_index"] == 0
    assert out["free_fraction_ppm"] == 909708
    assert out["compute_process_count"] == 0
    assert out["preclaim_gpu_admitted_at_observation"] is True


def test_review_preserves_nonreuse_rule():
    out = review.pair06_v8_precision_preclaim_gpu_observation_review_contract()
    assert out["historical_observation_only"] is True
    assert out["observation_reusable_for_future_claim"] is False
    assert out["fresh_reobservation_required_before_attempt_marker"] is True


def test_review_keeps_attempt_and_execution_authority_closed():
    out = review.pair06_v8_precision_preclaim_gpu_observation_review_contract()
    for field in (
        "retry_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_invocation_integration_source():
    out = review.pair06_v8_precision_preclaim_gpu_observation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECLAIM_GPU_INVOCATION_INTEGRATION_SOURCE_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECLAIM_GPU_INVOCATION_INTEGRATION_SOURCE_REQUIRED"
    )


def test_claim_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PrecisionPreclaimGpuObservationReviewHold,
        match="PAIR06_V8_PRECLAIM_GPU_INVOCATION_INTEGRATION_SOURCE_REQUIRED",
    ):
        review.claim_or_execute()
