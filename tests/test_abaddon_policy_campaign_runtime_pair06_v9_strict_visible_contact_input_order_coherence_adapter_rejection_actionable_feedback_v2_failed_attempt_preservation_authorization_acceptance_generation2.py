from __future__ import annotations

import hashlib

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_reviewed_request_and_user_authorization():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )

    assert out["reviewed_request_sha256"] == (
        "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
    )
    assert out["reviewed_request_bytes"] == 3288
    raw = out["authorization_text"].encode("utf-8")
    assert len(raw) == 186
    assert hashlib.sha256(raw).hexdigest() == (
        "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
    )


def test_acceptance_binds_canonical_main_at_authorization_time():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )

    assert out["canonical_main_head_at_authorization"] == (
        "000a8a01c29a8b42e91cb30f935ef63b72407f02"
    )
    assert out["canonical_main_tree_at_authorization"] == (
        "49b201ba723bcd4b8cab162f2d2d954534da6621"
    )


def test_acceptance_scope_is_exact_consumed_failed_attempt_preservation():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )

    assert out["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["attempt_marker_bytes"] == 2208
    assert out["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert out["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )
    assert out["archive_path"].endswith(
        "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
    )
    assert out["preservation_receipt_path"].endswith(
        "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823-preservation-receipt.json"
    )


@pytest.mark.parametrize(
    "field",
    (
        "preservation_authorization_accepted",
        "preservation_authorized",
        "filesystem_mutation_authorized",
        "git_worktree_mutation_authorized",
        "archive_rename_authorized",
        "preservation_receipt_creation_authorized",
        "authority_scope_exact_reviewed_preservation_only",
    ),
)
def test_acceptance_grants_only_reviewed_preservation_authority(field):
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )
    assert out[field] is True


@pytest.mark.parametrize(
    "field",
    (
        "preservation_performed",
        "runtime_retry_authorized",
        "execution_request_opened",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_acceptance_does_not_cross_runtime_or_funds_boundaries(field):
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )
    assert out[field] is False


def test_authorized_preservation_call_is_exact_and_non_executing():
    call = acceptance.authorized_preservation_call()
    assert call == {
        "preservation_authorized": True,
        "confirm": (
            "VOID_PAIR06_V9_PRESERVE_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_35B75823"
        ),
    }


def test_next_gate_is_host_preservation_execution():
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_HOST_EXECUTION_REQUIRED"
    )

    with pytest.raises(
        acceptance.Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceHold,
        match="PRESERVATION_HOST_EXECUTION_REQUIRED",
    ):
        acceptance.execute_or_retry()
