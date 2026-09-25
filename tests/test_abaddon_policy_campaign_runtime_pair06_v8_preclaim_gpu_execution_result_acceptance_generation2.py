from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_result_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_successful_attempt():
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()
    assert out["pair06_v8_preclaim_gpu_execution_result_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
    )
    assert out["authorized_main_head"] == (
        "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
    )
    assert out["attempt_marker_sha256"] == (
        "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
    )
    assert out["result_file_sha256"] == (
        "f1a3a1ffec2957b984212e5c11067a477934a1c484020dcb2e6398764a117440"
    )
    assert out["closeout_file_sha256"] == (
        "f0227597d44ecfc5ae07fdc473a2ca9bda71085fba9970279dedf31d5ac24920"
    )


def test_acceptance_binds_exact_game_terminal():
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()
    assert out["run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260925T070348Z-feinter-s208354846"
    )
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["model_inference_count"] == 36
    assert out["child_retirement_terminal"] == "natural_exit"
    assert out["warm_start_sha256"] == (
        "8ce4205d4d61a36a7aab503f5ff1b298020d564e08ab6e9e2302cd5623f679f8"
    )
    assert out["trajectory_sha256"] == (
        "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
    )
    assert out["summary_sha256"] == (
        "ae9692fbddd48fb95b9ee1d4737b1ad6ed1aae3ddb2eff80c45a7efde548b6f8"
    )


def test_acceptance_binds_fresh_gpu_admission():
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()
    assert out["preclaim_gpu_free_memory_bytes"] == 11647582208
    assert out["preclaim_gpu_total_memory_bytes"] == 12820938752
    assert out["preclaim_gpu_compute_process_count"] == 0
    assert out["fresh_preclaim_gpu_admitted"] is True


def test_candidate_only_is_not_candidate_arm_execution():
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()
    assert out["runtime_output_candidate_only"] is True
    assert out["candidate_execution_performed"] is False
    assert out["held_out_execution_performed"] is False
    assert out["automatic_corpus_admission"] is False


def test_no_unauthorized_side_effects_or_retry():
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()
    for field in (
        "automatic_retry_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "authorization_reusable_after_attempt_claim",
    ):
        assert out[field] is False


def test_acceptance_advances_only_to_source_review():
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECLAIM_GPU_EXECUTION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECLAIM_GPU_EXECUTION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8PreclaimGpuExecutionResultAcceptanceHold,
        match="PRECLAIM_GPU_EXECUTION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.execute_or_promote()
