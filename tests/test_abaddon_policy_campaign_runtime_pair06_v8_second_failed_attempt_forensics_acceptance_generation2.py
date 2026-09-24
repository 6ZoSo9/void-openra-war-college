from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_forensics_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_second_consumed_attempt():
    out = acceptance.pair06_v8_second_failed_attempt_forensics_acceptance_contract()
    assert out["pair06_v8_second_failed_attempt_forensics_accepted"] is True
    assert out["attempt_marker_sha256"] == (
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
    )
    assert out["prior_attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["attempt_distinct_from_prior"] is True
    assert out["attempt_consumed"] is True
    assert out["successful_game_result_present"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_retry_authorized"] is False


def test_exact_evidence_accepts_and_tampering_fails_closed():
    out = acceptance.accept_pair06_v8_second_failed_attempt_forensics(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["warm_start_preserved"] is True
    assert out["trajectory_preserved"] is True
    assert out["summary_present"] is False
    assert out["prior_archive_preserved"] is True
    assert out["prior_attempt_reused"] is False

    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["prior_attempt_reused"] = True
    with pytest.raises(
        acceptance.Pair06V8SecondFailedAttemptForensicsAcceptanceHold,
        match="evidence drift: prior_attempt_reused",
    ):
        acceptance.accept_pair06_v8_second_failed_attempt_forensics(tampered)


def test_acceptance_records_exact_second_failure_class():
    out = acceptance.pair06_v8_second_failed_attempt_forensics_acceptance_contract()[
        "accepted_evidence"
    ]
    assert out["warm_start_completed"] is True
    assert out["controller_handoff_reached"] is True
    assert out["first_controller_inference_failed"] is True
    assert out["failure_class"] == "qwen35_gated_delta_triton_cpu_pointer"
    assert out["runtime_retry_authorized"] is False


def test_acceptance_advances_only_to_second_preservation():
    out = acceptance.pair06_v8_second_failed_attempt_forensics_acceptance_contract()
    assert out["second_failed_attempt_preservation_required"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8SecondFailedAttemptForensicsAcceptanceHold,
        match="SECOND_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    ):
        acceptance.preserve_or_retry()
