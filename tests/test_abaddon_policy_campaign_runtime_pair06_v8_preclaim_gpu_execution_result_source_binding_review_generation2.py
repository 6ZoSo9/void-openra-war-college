from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_result_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_result_source_and_test():
    out = review.pair06_v8_preclaim_gpu_execution_result_review_contract()
    assert out["acceptance_git_blob"] == (
        "9af8a4afc676946ff470852438a3ecda854399e1"
    )
    assert out["acceptance_source_sha256"] == (
        "2f16dd723d97d40b424f8b18abcd529ea93115b7b0a1807c2d826b0974669efc"
    )
    assert out["acceptance_test_git_blob"] == (
        "6c49b1bf366a1cbec54a2a30fbd22323f973a9a6"
    )
    assert out["acceptance_test_sha256"] == (
        "47f661a44a814034c4426f9d5ba33236ad7750dd90c50eb9dd16101f57506c22"
    )


def test_review_binds_exact_consumed_attempt_and_durable_outputs():
    out = review.pair06_v8_preclaim_gpu_execution_result_review_contract()
    assert out["pair06_v8_preclaim_gpu_execution_result_reviewed"] is True
    assert out["authorized_request_sha256"] == (
        "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
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
    assert out["attempt_consumed"] is True
    assert out["authorization_reusable"] is False


def test_review_binds_completion_terminal():
    out = review.pair06_v8_preclaim_gpu_execution_result_review_contract()
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["model_inference_count"] == 36


def test_review_keeps_all_ungranted_actions_false():
    out = review.pair06_v8_preclaim_gpu_execution_result_review_contract()
    for field in (
        "candidate_execution_performed",
        "held_out_execution_performed",
        "automatic_retry_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_review_advances_only_to_post_run_diagnostic():
    out = review.pair06_v8_preclaim_gpu_execution_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_POST_RUN_COMBAT_UTILITY_AND_REJECTION_DIAGNOSTIC_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_POST_RUN_COMBAT_UTILITY_AND_REJECTION_DIAGNOSTIC_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PreclaimGpuExecutionResultReviewHold,
        match="POST_RUN_COMBAT_UTILITY_AND_REJECTION_DIAGNOSTIC_REQUIRED",
    ):
        review.execute_or_promote()
