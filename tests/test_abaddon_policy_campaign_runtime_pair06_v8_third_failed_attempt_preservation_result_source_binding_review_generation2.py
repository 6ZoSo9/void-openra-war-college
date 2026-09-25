from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_result_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_preservation_result_source_and_test():
    out = review.pair06_v8_third_preservation_result_review_contract()
    assert out["acceptance_git_blob"] == (
        "cf6b70a34704c9a7b19d0abf59ecad64ab663daf"
    )
    assert out["acceptance_source_sha256"] == (
        "fe8bbf57daa7613e1ab474b1fb268b97a93acef923c1a6651ef407cfe76a5816"
    )
    assert out["acceptance_test_git_blob"] == (
        "8d5e61467a6346cf7c9dfeee5d87908d02314000"
    )
    assert out["acceptance_test_sha256"] == (
        "c94a979e42c72560f0925c9ea7566304a95728e4b837efd0d662cdbf5fbc3a06"
    )


def test_review_pins_verified_preservation_receipt():
    out = review.pair06_v8_third_preservation_result_review_contract()
    assert out["preservation_receipt_logical_sha256"] == (
        "9a7ec01af0f80d7a0d0333c91fd5c07d9ae24e04eaf87455fb143385ec76070b"
    )
    assert out["preservation_receipt_file_sha256"] == (
        "12a2da73143db442f5620065f8c270ef8026a641da2afa938203e51ceeaa43f4"
    )
    assert out["preservation_receipt_bytes"] == 3130
    assert out["third_failed_attempt_archived"] is True
    assert out["third_failed_attempt_deleted"] is False
    assert out["fresh_baseline_arm_root_available"] is True


def test_review_rebinds_existing_gpu_gated_authorization():
    out = review.pair06_v8_third_preservation_result_review_contract()
    assert out["authorization_acceptance_git_blob"] == (
        "b1767053c72d53c3f713a986503d0806cdc9decc"
    )
    assert out["authorization_acceptance_source_sha256"] == (
        "2465ced181f1dd3f44f1f4a04b892678258d0ddbb8eb011e9ae4e398d9de1932"
    )
    assert out["authorized_request_sha256"] == (
        "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
    )
    assert out["authorized_main_head"] == (
        "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
    )
    assert out["existing_gpu_gated_authorization_accepted"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0


def test_review_preserves_gpu_admission_and_exclusions():
    out = review.pair06_v8_third_preservation_result_review_contract()
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "host_io_performed_by_review",
    ):
        assert out[field] is False


def test_review_advances_to_existing_authorized_precision_execution():
    out = review.pair06_v8_third_preservation_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RECEIPT_BOUND_PRECLAIM_GPU_PRECISION_EXECUTION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RECEIPT_BOUND_PRECLAIM_GPU_PRECISION_EXECUTION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ThirdPreservationResultReviewHold,
        match="RECEIPT_BOUND_PRECLAIM_GPU_PRECISION_EXECUTION_REQUIRED",
    ):
        review.execute()
