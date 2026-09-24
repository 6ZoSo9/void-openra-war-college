from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_generation2
    as preservation,
)


def test_contract_binds_third_consumed_attempt_and_archive():
    out = preservation.pair06_v8_third_failed_attempt_preservation_contract()
    assert out["forensics_acceptance_git_blob"] == (
        "053e311c286a904b26e3ef407e76e46b565d3c81"
    )
    assert out["forensics_acceptance_source_sha256"] == (
        "75a11e237915dd22eb15f6cf0347ad44bfe1644e667e1562e0827e9d57b15f0e"
    )
    assert out["attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["archive_name"] == "baseline-3ad564f9"
    assert out["marker_only_claims_required"] is True
    assert out["empty_runs_required"] is True


def test_preservation_requires_exact_confirmation_before_mutation(monkeypatch):
    monkeypatch.setattr(
        preservation,
        "_validate_prior_archives",
        lambda: (_ for _ in ()).throw(
            AssertionError("must not inspect runtime before confirmation")
        ),
    )
    with pytest.raises(
        preservation.Pair06V8ThirdFailedAttemptPreservationHold,
        match="THIRD_FAILED_ATTEMPT_PRESERVATION_CONFIRMATION_REQUIRED",
    ):
        preservation.preserve_third_failed_pair06_v8_attempt(confirm="wrong")


def test_contract_preserves_exact_nonforce_atomic_strategy():
    out = preservation.pair06_v8_third_failed_attempt_preservation_contract()
    assert out["exact_registered_clean_detached_worktrees_required"] is True
    assert out["non_force_worktree_removal_implemented"] is True
    assert out["atomic_same_filesystem_rename_implemented"] is True
    assert out["inode_identity_preservation_checked"] is True
    assert out["marker_rehashed_after_archive"] is True
    assert out[
        "both_prior_failed_attempt_archives_revalidated_before_and_after"
    ] is True


def test_contract_grants_no_retry_or_execution_authority():
    out = preservation.pair06_v8_third_failed_attempt_preservation_contract()
    assert out["failed_attempt_deletion_implemented"] is False
    assert out["runtime_retry_implemented_by_this_source"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
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


def test_contract_advances_only_to_separate_review():
    out = preservation.pair06_v8_third_failed_attempt_preservation_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_retry_entrypoint_holds():
    with pytest.raises(
        preservation.Pair06V8ThirdFailedAttemptPreservationHold,
        match="THIRD_FAILED_ATTEMPT_RETRY_NOT_AUTHORIZED",
    ):
        preservation.authorize_retry()
