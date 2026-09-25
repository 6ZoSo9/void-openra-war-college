from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_preservation_source_and_test():
    out = review.pair06_v8_third_failed_attempt_preservation_review_contract()
    assert out["preservation_git_blob"] == (
        "2c00cf095fcd3a675f84fe08b8b72346186fe06f"
    )
    assert out["preservation_source_sha256"] == (
        "bff90c9c8eb7080fe7c5db793ad6df25e897ee589b0445952abe255a2a8cba29"
    )
    assert out["preservation_test_git_blob"] == (
        "563e1a6dbefc6af34426b9d32bd2d4711bd89b2d"
    )
    assert out["preservation_test_sha256"] == (
        "242a98aec886c36d94f91e5e1e764aa2a3e0a644a333ba6d66294e299878d175"
    )


def test_review_binds_exact_consumed_marker_and_archive():
    out = review.pair06_v8_third_failed_attempt_preservation_review_contract()
    assert out["pair06_v8_third_failed_attempt_preservation_reviewed"] is True
    assert out["attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["archive_name"] == "baseline-3ad564f9"
    assert out["marker_only_claims_required"] is True
    assert out["empty_runs_required"] is True


def test_review_requires_evidence_preserving_archive_strategy():
    out = review.pair06_v8_third_failed_attempt_preservation_review_contract()
    assert out["non_force_worktree_removal_required"] is True
    assert out["atomic_archive_rename_required"] is True
    assert out["evidence_inode_preservation_required"] is True
    assert out["prior_archives_must_remain_unchanged"] is True
    assert out["failed_attempt_deleted"] is False


def test_review_keeps_retry_and_execution_closed():
    out = review.pair06_v8_third_failed_attempt_preservation_review_contract()
    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_precision_preservation():
    out = review.pair06_v8_third_failed_attempt_preservation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_PRECISION_EXECUTION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_PRECISION_EXECUTION_REQUIRED"
    )


def test_retry_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ThirdFailedAttemptPreservationReviewHold,
        match="THIRD_FAILED_ATTEMPT_PRESERVATION_PRECISION_EXECUTION_REQUIRED",
    ):
        review.preserve_or_retry()
