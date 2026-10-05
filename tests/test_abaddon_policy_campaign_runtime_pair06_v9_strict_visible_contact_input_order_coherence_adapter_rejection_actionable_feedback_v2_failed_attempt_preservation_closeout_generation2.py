from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_closeout_generation2
    as closeout,
)


def test_closeout_binds_exact_host_preservation_result():
    out = (
        closeout
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract()
    )

    assert out["record_kind"] == "source_only_host_preservation_closeout"
    assert out["execution_control_main_head"] == (
        "e203d56e627fbcddb7f7b6d44652657b3ab58b46"
    )
    assert out["execution_control_main_tree"] == (
        "0483d9ac42b65a0f2bde501bee0aa8aae30dae18"
    )
    assert out["authorization_text_sha256"] == (
        "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
    )
    assert out["authorization_text_bytes"] == 186
    assert out["reviewed_request_sha256"] == (
        "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
    )
    assert out["reviewed_request_bytes"] == 3288
    assert out["launcher_source_sha256"] == (
        "1f8cdf4be60d581d3d7994f3d47e450e314d917658e7cfa310a6552e5a338d92"
    )
    assert out["preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )


def test_closeout_binds_consumed_v2_failed_attempt_evidence():
    out = (
        closeout
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract()
    )

    assert out["failure_class"] == "strict_contact_actionable_feedback_v2_exhausted"
    assert out["failure_round"] == 6
    assert out["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert out["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )

    assert out["attempt_consumed"] is True
    assert out["attempt_reusable"] is False
    assert out["attempt_authorization_reusable"] is False
    assert out["preservation_authorization_consumed"] is True
    assert out["preservation_authorization_reusable"] is False


def test_closeout_proves_preservation_invariants():
    out = (
        closeout
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract()
    )

    assert out["archive_atomic_rename_performed"] is True
    assert out["attempt_marker_inode_preserved"] is True
    assert out["warm_start_inode_preserved"] is True
    assert out["trajectory_inode_preserved"] is True
    assert out["source_worktree_removed_non_force"] is True
    assert out["engine_worktree_removed_non_force"] is True
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
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract()
    )
    assert out[field] is False


def test_closeout_advances_only_to_review():
    out = (
        closeout
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_closeout_contract()
    )

    assert out["runtime_output_observed"] is True
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_CLOSEOUT_REVIEW_REQUIRED"
    )

    with pytest.raises(
        RuntimeError,
        match="PRESERVATION_CLOSEOUT_REVIEW_REQUIRED",
    ):
        closeout.review_or_reopen()
