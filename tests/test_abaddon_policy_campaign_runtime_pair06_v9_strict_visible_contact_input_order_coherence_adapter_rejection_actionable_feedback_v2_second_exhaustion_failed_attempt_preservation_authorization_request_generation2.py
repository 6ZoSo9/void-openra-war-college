from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_request_generation2
    as request,
)


def test_request_binds_exact_second_exhaustion_evidence():
    out = request.preservation_authorization_request()
    record = out["request"]
    failed = record["failed_attempt"]

    assert record["record_kind"] == "proposal_only_not_authorization"
    assert failed["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert failed["attempt_marker_bytes"] == 2208
    assert failed["warm_start_sha256"] == (
        "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    )
    assert failed["trajectory_sha256"] == (
        "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    )
    assert failed["predecessor_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert failed["attempt_consumed"] is True
    assert failed["attempt_reusable"] is False
    assert failed["execution_authorization_reusable"] is False


def test_request_preservation_scope_is_narrow_and_distinct():
    record = request.preservation_authorization_request()["request"]
    scope = record["requested_preservation"]

    assert scope["archive_name"].endswith("ee1b4fc5")
    assert scope["exact_marker_and_run_artifacts_required"] is True
    assert scope["exact_clean_detached_registered_worktrees_required"] is True
    assert scope["engine_removed_before_source"] is True
    assert scope["non_force_git_worktree_remove_only"] is True
    assert scope["remaining_evidence_manifest_hashed"] is True
    assert scope["atomic_baseline_archive_rename_requested"] is True
    assert scope["marker_and_run_inode_preservation_required"] is True
    assert scope["create_only_preservation_receipt_requested"] is True
    assert scope["first_v2_archive_must_remain_unchanged"] is True
    assert scope["file_content_deletion_requested"] is False
    assert scope["force_worktree_removal_requested"] is False
    assert scope["runtime_retry_requested"] is False


def test_request_requires_fresh_preservation_authorization():
    boundary = request.preservation_authorization_request()["request"][
        "authorization_boundary"
    ]
    assert boundary["preservation_authorization_requested"] is True
    assert boundary["fresh_explicit_user_authorization_required"] is True
    assert (
        boundary["general_source_work_authorization_is_preservation_authorization"]
        is False
    )
    assert boundary["matching_request_digest_grants_authority"] is False
    assert boundary["matching_request_bytes_grant_authority"] is False
    assert boundary["prior_preservation_authorization_reusable"] is False
    assert boundary["prior_execution_authorization_reusable"] is False


@pytest.mark.parametrize("field", request.FALSE_AUTHORITY_FIELDS)
def test_request_grants_no_authority(field):
    out = request.preservation_authorization_request()
    assert out["request"][field] is False


def test_request_performs_no_host_mutation():
    out = request.preservation_authorization_request()
    assert out["request_grants_authority"] is False
    assert out["host_io_performed"] is False
    assert out["filesystem_mutation_performed"] is False
    assert out["git_worktree_mutation_performed"] is False
    assert out["archive_rename_performed"] is False
    assert out["preservation_receipt_created"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["execution_request_opened"] is False


def test_request_advances_only_to_source_binding_review():
    out = request.preservation_authorization_request()
    assert isinstance(out["request_sha256"], str)
    assert len(out["request_sha256"]) == 64
    assert out["request_bytes"] > 0
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
        "PRESERVATION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
    )
    with pytest.raises(
        request.Pair06V9V2SecondExhaustionPreservationAuthorizationRequestHold,
        match="SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.accept_or_preserve()
