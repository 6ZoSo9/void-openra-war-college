from __future__ import annotations

from copy import deepcopy
import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_result_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_green_preservation_terminal():
    out = acceptance.pair06_v8_failed_attempt_preservation_result_acceptance_contract()
    assert out["pair06_v8_failed_attempt_preservation_result_accepted"] is True
    assert out["attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["failed_attempt_archived"] is True
    assert out["failed_attempt_deleted"] is False
    assert out["fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt"] is True


def test_evidence_tampering_fails_closed():
    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["automatic_retry"] = True
    with pytest.raises(
        acceptance.Pair06V8FailedAttemptPreservationResultAcceptanceHold,
        match="preservation evidence drift: automatic_retry",
    ):
        acceptance.accept_pair06_v8_failed_attempt_preservation_result(tampered)


def test_acceptance_grants_no_retry_or_external_authority():
    out = acceptance.pair06_v8_failed_attempt_preservation_result_acceptance_contract()[
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


def test_acceptance_advances_only_to_new_repaired_request():
    out = acceptance.pair06_v8_failed_attempt_preservation_result_acceptance_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8FailedAttemptPreservationResultAcceptanceHold,
        match="REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        acceptance.request_or_execute()
