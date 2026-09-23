from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_generation2
    as preservation,
)


def test_contract_requires_exact_preservation_without_retry_authority():
    out = preservation.pair06_v8_failed_attempt_preservation_contract()
    assert out["attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["exact_failed_tree_required"] is True
    assert out["exact_registered_clean_detached_worktrees_required"] is True
    assert out["non_force_worktree_removal_implemented"] is True
    assert out["atomic_same_filesystem_rename_implemented"] is True
    assert out["inode_identity_preservation_checked"] is True
    assert out["marker_warm_start_trajectory_rehashed_after_archive"] is True
    assert out["failed_attempt_deletion_implemented"] is False
    assert out["runtime_retry_implemented_by_this_source"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_preservation_requires_exact_confirmation(monkeypatch):
    monkeypatch.setattr(
        preservation,
        "_git",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("must not touch git before confirmation")
        ),
    )
    with pytest.raises(
        preservation.Pair06V8FailedAttemptPreservationHold,
        match="PRESERVATION_CONFIRMATION_REQUIRED",
    ):
        preservation.preserve_failed_pair06_v8_attempt(confirm="wrong")


def test_contract_preserves_external_boundaries():
    out = preservation.pair06_v8_failed_attempt_preservation_contract()
    for field in (
        "runtime_start_implemented",
        "model_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "training_implemented",
        "weights_update_implemented",
        "automatic_policy_promotion_implemented",
        "deployment_implemented",
        "void_chain_mutation_implemented",
        "wallet_or_funds_action_implemented",
    ):
        assert out[field] is False


def test_contract_advances_only_to_separate_source_review():
    out = preservation.pair06_v8_failed_attempt_preservation_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_retry_entrypoint_holds():
    with pytest.raises(
        preservation.Pair06V8FailedAttemptPreservationHold,
        match="RETRY_NOT_AUTHORIZED",
    ):
        preservation.authorize_retry()
