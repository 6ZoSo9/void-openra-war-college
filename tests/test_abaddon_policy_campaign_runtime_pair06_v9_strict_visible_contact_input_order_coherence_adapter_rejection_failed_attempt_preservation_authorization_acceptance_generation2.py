from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_user_authorization_and_main_snapshot():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract()
    )

    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["preservation_authorization_accepted"] is True
    assert out["preservation_authorized"] is True

    assert out["authorization_text_sha256"] == (
        "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
    )
    assert out["authorization_text_bytes"] == 35
    assert out["authorized_main_head"] == (
        "b36cafe6044012656d9a122653c2ddb5b9831f63"
    )
    assert out["authorized_main_tree"] == (
        "03b0a1ae8d8b050e50429c1f1617fb12953ebf1e"
    )
    assert out["canonical_main_bound_at_authorization_time"] is True


def test_acceptance_binds_exact_failed_attempt_scope():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract()
    )

    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert isinstance(out["authorized_reviewed_request_sha256"], str)
    assert len(out["authorized_reviewed_request_sha256"]) == 64
    assert out["authorized_reviewed_request_bytes"] > 0
    assert "failed-attempts" in out["archive_path"]
    assert out["preservation_receipt_path"].endswith(
        "-preservation-receipt.json"
    )


def test_acceptance_authorizes_only_reviewed_preservation_mutations():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract()
    )

    assert out["exact_evidence_validation_required_before_mutation"] is True
    assert out["non_force_git_worktree_removal_authorized"] is True
    assert out["engine_removed_before_source_authorized"] is True
    assert out["remaining_evidence_manifest_hashing_authorized"] is True
    assert out["atomic_baseline_archive_rename_authorized"] is True
    assert out["marker_and_run_inode_preservation_required"] is True
    assert out["create_only_preservation_receipt_authorized"] is True

    assert out["file_content_deletion_authorized"] is False
    assert out["force_worktree_removal_authorized"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
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
        "filesystem_mutation_performed_by_this_record",
        "git_worktree_mutation_performed_by_this_record",
        "archive_rename_performed_by_this_record",
        "preservation_receipt_created_by_this_record",
        "preservation_performed_by_this_record",
        "authorization_reusable_after_preservation",
    ),
)
def test_acceptance_record_performs_no_effect_and_grants_no_runtime_authority(field):
    out = (
        acceptance
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract()
    )
    assert out[field] is False


def test_acceptance_advances_only_to_authorized_preservation_launcher():
    out = (
        acceptance
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
    )


def test_preserve_holds():
    with pytest.raises(
        acceptance.Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceHold,
        match="AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED",
    ):
        acceptance.preserve()
