from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_gpu_gated_invocation_source_and_test():
    out = (
        review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )
    assert out["invocation_git_blob"] == (
        "ef9ed62758db399d6d59e6b782df8ed5587ed9bb"
    )
    assert out["invocation_source_sha256"] == (
        "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386"
    )
    assert out["invocation_test_git_blob"] == (
        "509d5876606bdedae34a4307b9dc5dd32c59a428"
    )
    assert out["invocation_test_sha256"] == (
        "05d4cacf12c1ee1ee4510b932e68975bf57f0a35be0474da19bebc2295d3c8f4"
    )


def test_review_requires_fresh_cuda0_admission_before_marker():
    out = (
        review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )
    assert out[
        "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_reviewed"
    ] is True
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["historical_gpu_observation_reusable"] is False


def test_review_marks_prior_request_and_oom_attempt_nonreusable():
    out = (
        review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )
    assert out["spent_receipt_bound_request_sha256"] == (
        "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
    )
    assert out["spent_receipt_bound_request_reusable"] is False
    assert out["spent_oom_attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["spent_oom_attempt_reusable"] is False


def test_review_remains_non_authorizing():
    out = (
        review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )
    assert out["explicit_authorization_required"] is True
    for field in (
        "pair06_baseline_specific_authorization_accepted",
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


def test_review_advances_only_to_new_gpu_gated_request():
    out = (
        review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PreclaimGpuInvocationReviewHold,
        match="PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.authorize_or_execute()
