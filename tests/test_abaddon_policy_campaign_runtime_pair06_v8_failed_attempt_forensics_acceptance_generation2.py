from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_forensics_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_consumed_attempt():
    out = acceptance.pair06_v8_failed_attempt_forensics_acceptance_contract()
    assert out["pair06_v8_failed_attempt_forensics_accepted"] is True
    assert out["attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["attempt_consumed"] is True
    assert out["successful_game_result_present"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_retry_authorized"] is False


def test_exact_evidence_accepts_and_tampering_fails_closed():
    out = acceptance.accept_pair06_v8_failed_attempt_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["warm_start_preserved"] is True
    assert out["trajectory_preserved"] is True
    assert out["summary_present"] is False
    assert out["residual_frozen_worktrees_present"] is True

    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["attempt_consumed"] = False
    with pytest.raises(
        acceptance.Pair06V8FailedAttemptForensicsAcceptanceHold,
        match="evidence drift: attempt_consumed",
    ):
        acceptance.accept_pair06_v8_failed_attempt_forensics(tampered)


def test_acceptance_preserves_failure_scope_and_no_retry_authority():
    out = acceptance.pair06_v8_failed_attempt_forensics_acceptance_contract()[
        "accepted_evidence"
    ]
    assert out["warm_start_completed"] is True
    assert out["controller_handoff_reached"] is True
    assert out["first_v8_inference_failed"] is True
    assert out["successful_game_result_present"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["training_authorized"] is False
    assert out["deployment_authorized"] is False


def test_acceptance_advances_only_to_preservation():
    out = acceptance.pair06_v8_failed_attempt_forensics_acceptance_contract()
    assert out["failed_attempt_preservation_required"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_REQUIRED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8FailedAttemptForensicsAcceptanceHold,
        match="PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    ):
        acceptance.preserve_or_retry()
