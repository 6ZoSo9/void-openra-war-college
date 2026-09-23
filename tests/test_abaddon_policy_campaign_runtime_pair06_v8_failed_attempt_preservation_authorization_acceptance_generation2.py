from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_authorized_main_marker_and_text():
    out = acceptance.pair06_v8_failed_attempt_preservation_authorization_acceptance_contract()
    assert out["pair06_v8_failed_attempt_preservation_authorization_accepted"] is True
    assert out["authorized_main_head"] == (
        "344f6e146e839582aa600b11ca5d1c31e46b124a"
    )
    assert out["authorized_attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["authorization_text_sha256"] == (
        "9830b62787aa5c8fb84af7c0394b62aec25d6154e53cb2b339af7bb38826ecbb"
    )
    assert out["authorization_text_bytes"] == 600


def test_acceptance_authorizes_only_preservation_mutations():
    out = acceptance.pair06_v8_failed_attempt_preservation_authorization_acceptance_contract()
    assert out["failed_attempt_preservation_authorized"] is True
    assert out["non_force_worktree_cleanup_authorized"] is True
    assert out["atomic_evidence_archive_authorized"] is True
    assert out["preservation_receipt_creation_authorized"] is True
    assert out["failed_attempt_deletion_authorized"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_acceptance_preserves_all_runtime_and_external_exclusions():
    out = acceptance.pair06_v8_failed_attempt_preservation_authorization_acceptance_contract()
    for field in (
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
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
    out = acceptance.pair06_v8_failed_attempt_preservation_authorization_acceptance_contract()
    assert out["next_gate"] == "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_AUTHORIZED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8FailedAttemptPreservationAuthorizationAcceptanceHold,
        match="PRESERVATION_AUTHORIZED",
    ):
        acceptance.preserve_or_retry()
