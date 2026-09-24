from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_authorized_main_marker_archive_and_text():
    out = (
        acceptance
        .pair06_v8_second_failed_attempt_preservation_authorization_acceptance_contract()
    )
    assert out[
        "pair06_v8_second_failed_attempt_preservation_authorization_accepted"
    ] is True
    assert out["authorized_main_head"] == (
        "88edd6d4b69e6d6869b74dca85df3fc3b0bd5a23"
    )
    assert out["authorized_attempt_marker_sha256"] == (
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
    )
    assert out["authorized_archive_name"] == (
        "baseline-20260923T235031Z-446d8f92"
    )
    assert out["authorization_text_sha256"] == (
        "5c2f8ddd1893a88bf706666ad5482b236bd4a5b4e6a0c8dfa52f6948ac2561fc"
    )
    assert out["authorization_text_bytes"] == 745


def test_acceptance_authorizes_only_second_preservation_mutations():
    out = (
        acceptance
        .pair06_v8_second_failed_attempt_preservation_authorization_acceptance_contract()
    )
    assert out["failed_attempt_preservation_authorized"] is True
    assert out["non_force_worktree_cleanup_authorized"] is True
    assert out["atomic_evidence_archive_authorized"] is True
    assert out["prior_failed_attempt_revalidation_authorized"] is True
    assert out["preservation_receipt_creation_authorized"] is True
    assert out["failed_attempt_deletion_authorized"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_acceptance_preserves_all_runtime_and_external_exclusions():
    out = (
        acceptance
        .pair06_v8_second_failed_attempt_preservation_authorization_acceptance_contract()
    )
    for field in (
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["preservation_performed"] is False


def test_acceptance_stops_at_authorized_preservation():
    out = (
        acceptance
        .pair06_v8_second_failed_attempt_preservation_authorization_acceptance_contract()
    )
    assert out["next_gate"] == (
        "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_AUTHORIZED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8SecondFailedAttemptPreservationAuthorizationAcceptanceHold,
        match="SECOND_FAILED_ATTEMPT_PRESERVATION_AUTHORIZED",
    ):
        acceptance.preserve_or_retry()
