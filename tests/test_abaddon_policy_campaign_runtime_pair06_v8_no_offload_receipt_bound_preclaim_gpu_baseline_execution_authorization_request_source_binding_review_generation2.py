from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_request_source_test_and_bytes():
    out = (
        review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    assert out["request_git_blob"] == (
        "6fd00cbca51eb08eda313e5996154033ab6c1275"
    )
    assert out["request_source_sha256"] == (
        "bbfc9f51c115b6b86e150f458bf95ab318d12d6408f9b731a1c16e2b7aee3298"
    )
    assert out["request_test_git_blob"] == (
        "3d45b74c57fd97151f7ee29e1f2745098a2e332c"
    )
    assert out["request_test_sha256"] == (
        "c486db92a3c35fac2c1a3fcd2d91fded4052946d3c616a74753141b55daf9705"
    )
    assert out["request_bytes_sha256"] == (
        "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
    )
    assert out["request_byte_length"] == 4785


def test_review_confirms_fresh_gpu_gate():
    out = (
        review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["historical_clean_gpu_observation_reusable"] is False


def test_review_preserves_spent_request_and_oom_attempt():
    out = (
        review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    assert out["spent_receipt_bound_request_sha256"] == (
        "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
    )
    assert out["spent_receipt_bound_request_reusable"] is False
    assert out["spent_oom_attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["spent_oom_attempt_reusable"] is False


def test_review_is_still_proposal_only():
    out = (
        review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    assert out["matching_request_digest_grants_authority"] is False
    assert out["pair06_preclaim_gpu_baseline_specific_authorization_accepted"] is False
    assert out["pair06_preclaim_gpu_baseline_execution_authorized"] is False
    assert out["pair06_preclaim_gpu_baseline_execution_performed"] is False
    for field in (
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_explicit_authorization():
    out = (
        review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PreclaimGpuRequestReviewHold,
        match=(
            "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
            "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
        ),
    ):
        review.authorize_or_execute()
