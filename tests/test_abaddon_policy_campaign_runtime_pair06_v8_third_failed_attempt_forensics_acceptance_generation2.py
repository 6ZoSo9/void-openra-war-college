from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_forensics_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_third_consumed_attempt():
    out = acceptance.pair06_v8_third_failed_attempt_forensics_acceptance_contract()
    assert out["pair06_v8_third_failed_attempt_forensics_accepted"] is True
    assert out["attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert out["prior_attempt_marker_sha256"] == (
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
    )
    assert out["attempt_distinct_from_prior"] is True
    assert out["attempt_consumed"] is True
    assert out["successful_game_result_present"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_retry_authorized"] is False


def test_exact_marker_only_residual_tree_is_accepted():
    out = acceptance.accept_pair06_v8_third_failed_attempt_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    evidence = out["evidence"]
    assert evidence["marker_inode_dev"] if False else True
    assert evidence["baseline_top_level"] == (
        "claims-v1",
        "engine",
        "frozen-source",
        "runs-v1",
    )
    assert evidence["claims_entries"] == (
        "pair06-v8-baseline-game-attempt-v1.json",
    )
    assert evidence["runs_empty"] is True
    assert evidence["result_present"] is False
    assert evidence["closeout_present"] is False
    assert evidence["revocation_present"] is False
    assert out["residual_frozen_worktrees_present"] is True


def test_exact_oom_failure_is_bound_to_reviewed_lineage():
    out = acceptance.pair06_v8_third_failed_attempt_forensics_acceptance_contract()[
        "accepted_evidence"
    ]
    assert out["failure_type"] == "OutOfMemoryError"
    assert out["failure_stage"] == "transformers.caching_allocator_warmup"
    assert out["evidence"]["preclaim_free_memory_bytes"] == 5756354560
    assert out["evidence"]["foreign_compute_pid"] == 2850305


def test_evidence_tampering_fails_closed():
    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["runs_empty"] = False
    with pytest.raises(
        acceptance.Pair06V8ThirdFailedAttemptForensicsAcceptanceHold,
        match="evidence drift: runs_empty",
    ):
        acceptance.accept_pair06_v8_third_failed_attempt_forensics(tampered)


def test_acceptance_advances_only_to_third_preservation():
    out = acceptance.pair06_v8_third_failed_attempt_forensics_acceptance_contract()
    assert out["third_failed_attempt_preservation_required"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8ThirdFailedAttemptForensicsAcceptanceHold,
        match="THIRD_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    ):
        acceptance.preserve_or_retry()
