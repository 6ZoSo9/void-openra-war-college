from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_authorization_request_and_main():
    out = (
        acceptance
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract()
    )
    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["authorization_text_sha256"] == (
        "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
    )
    assert out["authorization_text_bytes"] == 682
    assert out["authorized_request_sha256"] == (
        "dc9ed1487e2d218001d178eab66b29958d98c1fa7eb30760bfaf7998fe679dfc"
    )
    assert out["authorized_request_bytes"] == 3473
    assert out["authorized_main_head"] == (
        "69538ff6c0e2d82d7ab4e0ecdfe28b867ef48e35"
    )
    assert out["authorized_main_tree"] == (
        "be5ed71f0f1f5feaf86107964ebd6746fb9c1512"
    )
    assert out["canonical_main_bound_at_authorization_time"] is True


def test_acceptance_authorizes_only_reviewed_preservation_scope():
    out = (
        acceptance
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract()
    )

    for field in (
        "preservation_authorization_accepted",
        "preservation_authorized",
        "filesystem_mutation_authorized",
        "git_worktree_mutation_authorized",
        "archive_rename_authorized",
        "preservation_receipt_creation_authorized",
        "exact_evidence_validation_authorized",
        "non_force_reviewed_worktree_removal_authorized",
        "engine_before_source_removal_required",
        "atomic_archive_rename_authorized",
        "inode_preservation_required",
        "create_only_preservation_receipt_authorized",
    ):
        assert out[field] is True

    assert out["first_v2_archive_mutation_authorized"] is False
    assert out["prior_preservation_authorization_reusable"] is False
    assert out["prior_execution_authorization_reusable"] is False
    assert out["preservation_performed_by_this_record"] is False


def test_acceptance_binds_second_exhaustion_evidence():
    out = (
        acceptance
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract()
    )
    assert out["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["warm_start_sha256"] == (
        "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    )
    assert out["trajectory_sha256"] == (
        "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    )
    assert out["predecessor_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert out["archive_path"].endswith("ee1b4fc5")


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
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_acceptance_grants_no_runtime_or_follow_on_authority(field):
    out = (
        acceptance
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract()
    )
    assert out[field] is False


def test_acceptance_advances_only_to_authorized_preservation_launcher():
    out = (
        acceptance
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
        "AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
    )

    with pytest.raises(
        acceptance.Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceHold,
        match="AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED",
    ):
        acceptance.preserve()
