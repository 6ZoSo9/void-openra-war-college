from __future__ import annotations

from copy import deepcopy
import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_result_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_second_green_preservation_terminal():
    out = acceptance.pair06_v8_second_preservation_result_acceptance_contract()
    assert out["pair06_v8_second_preservation_result_accepted"] is True
    assert out["attempt_marker_sha256"] == (
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
    )
    assert out["archive_name"] == "baseline-20260923T235031Z-446d8f92"
    assert out["second_failed_attempt_archived"] is True
    assert out["second_failed_attempt_deleted"] is False
    assert out["prior_failed_attempt_archive_unchanged"] is True
    assert out["fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt"] is True


def test_evidence_tampering_fails_closed():
    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["automatic_retry"] = True
    with pytest.raises(
        acceptance.Pair06V8SecondPreservationResultAcceptanceHold,
        match="second preservation evidence drift: automatic_retry",
    ):
        acceptance.accept_pair06_v8_second_preservation_result(tampered)


def test_acceptance_grants_no_retry_or_external_authority():
    out = acceptance.pair06_v8_second_preservation_result_acceptance_contract()[
        "accepted_evidence"
    ]
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["training_authorized"] is False
    assert out["deployment_authorized"] is False
    assert out["void_chain_mutation_authorized"] is False
    assert out["wallet_or_funds_action_authorized"] is False


def test_acceptance_advances_only_to_no_offload_invocation_generation():
    out = acceptance.pair06_v8_second_preservation_result_acceptance_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8SecondPreservationResultAcceptanceHold,
        match="NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED",
    ):
        acceptance.request_or_execute()
