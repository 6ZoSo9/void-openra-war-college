from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_preservation_source_and_test():
    out = review.pair06_v8_failed_attempt_preservation_review_contract()
    assert out["preservation_git_blob"] == (
        "ff4de10454fc958d5ca459bd7a3eea6a27a17e64"
    )
    assert out["preservation_source_sha256"] == (
        "05f11516233d7c602244878e8aa066f1a8aae7ea59e3c0641f0cbe494f518c26"
    )
    assert out["preservation_test_git_blob"] == (
        "25cd570a90b105e3eca8e95d84e8547e37ff0b26"
    )
    assert out["preservation_test_sha256"] == (
        "d2f1845dcb29b1f62618e34c36532ae62613f66a6138304937b7ee93df48fb62"
    )


def test_review_confirms_preservation_without_retry_authority():
    out = review.pair06_v8_failed_attempt_preservation_review_contract()
    assert out["pair06_v8_failed_attempt_preservation_reviewed"] is True
    assert out["attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["failed_attempt_deletion_authorized"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_execution_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False


def test_review_preserves_external_boundaries():
    out = review.pair06_v8_failed_attempt_preservation_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_preservation_invocation():
    out = review.pair06_v8_failed_attempt_preservation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED"
    )


def test_retry_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8FailedAttemptPreservationReviewHold,
        match="PRESERVATION_INVOCATION_REQUIRED",
    ):
        review.invoke_or_retry()
