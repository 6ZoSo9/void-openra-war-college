from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_closeout_generation2
    as closeout,
)


def test_closeout_binds_exact_host_preservation_result():
    out = (
        closeout
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()
    )

    assert out["record_kind"] == "source_only_host_preservation_closeout"
    assert out["authorized_main_head"] == (
        "43f95480eafa642c8203552fbc00d8edd522d74c"
    )
    assert out["authorized_main_tree"] == (
        "50db944a47dc386fa7f8814aad45683df907f259"
    )
    assert out["launcher_source_sha256"] == (
        "1456f8b30d9af526b8f4e6937bc20a417a5f58ba6dbfa7dfdbe0e11738273c84"
    )
    assert out["preservation_receipt_sha256"] == (
        "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
    )


def test_closeout_binds_consumed_failed_attempt_evidence():
    out = (
        closeout
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()
    )

    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["warm_start_sha256"] == (
        "9ad33940dcc8199a61b6fa8bb5fb68f2eb8cc846fb745cf7e64c27e6e053b0e1"
    )
    assert out["trajectory_sha256"] == (
        "4aaa1e944a2004b87c420d6a25d361bcd5316d992479d9a934cc1b10739b867a"
    )

    assert out["attempt_consumed"] is True
    assert out["attempt_reusable"] is False
    assert out["attempt_authorization_reusable"] is False
    assert out["preservation_authorization_consumed"] is True
    assert out["preservation_authorization_reusable"] is False


def test_closeout_proves_preservation_invariants():
    out = (
        closeout
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()
    )

    assert out["archive_atomic_rename_performed"] is True
    assert out["attempt_marker_inode_preserved"] is True
    assert out["warm_start_inode_preserved"] is True
    assert out["trajectory_inode_preserved"] is True
    assert out["single_authorized_preservation_consumed"] is True
    assert "failed-attempts" in out["archive_path"]
    assert out["preservation_receipt_path"].endswith(
        "-preservation-receipt.json"
    )


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "scheduler_mutation_performed",
        "repo_side_local_artifact_rehash_performed",
    ),
)
def test_closeout_grants_no_runtime_or_follow_on_authority(field):
    out = (
        closeout
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()
    )
    assert out[field] is False


def test_closeout_records_observed_runtime_output_only():
    out = (
        closeout
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()
    )

    assert out["runtime_output_observed"] is True
    assert out["repo_side_local_artifact_rehash_performed"] is False


def test_closeout_advances_only_to_review():
    out = (
        closeout
        .pair06_v9_adapter_rejection_failed_attempt_preservation_closeout_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_CLOSEOUT_REVIEW_REQUIRED"
    )


def test_review_or_reopen_holds():
    with pytest.raises(
        RuntimeError,
        match="PRESERVATION_CLOSEOUT_REVIEW_REQUIRED",
    ):
        closeout.review_or_reopen()
