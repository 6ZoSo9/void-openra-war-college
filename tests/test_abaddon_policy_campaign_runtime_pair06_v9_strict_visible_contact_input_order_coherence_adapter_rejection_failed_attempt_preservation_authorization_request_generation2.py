from __future__ import annotations

import hashlib
import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_request_generation2
    as request,
)


def test_request_is_deterministic_and_digest_matches_exact_bytes():
    first = request.preservation_authorization_request()
    second = request.preservation_authorization_request()

    assert first == second

    raw = (
        json.dumps(
            first["request"],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")

    assert first["request_sha256"] == hashlib.sha256(raw).hexdigest()
    assert first["request_bytes"] == len(raw)
    assert first["request_bytes"] <= request.MAX_REQUEST_BYTES


def test_request_binds_exact_failed_attempt_and_preservation_source():
    out = request.preservation_authorization_request()
    record = out["request"]

    assert record["source_binding"]["preservation_stack_head"] == (
        "93944bd42f10b94b4133176e35a482370d1618d5"
    )
    assert record["source_binding"]["preservation_git_blob"] == (
        "342118e0e9edbba7472820ae99ff4c05203143d0"
    )
    assert record["source_binding"]["preservation_review_git_blob"] == (
        "6565b7b9c30c6f3d9bf67182bee64e7eae08c41a"
    )

    failed = record["failed_attempt"]
    assert failed["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert failed["warm_start_sha256"] == (
        "9ad33940dcc8199a61b6fa8bb5fb68f2eb8cc846fb745cf7e64c27e6e053b0e1"
    )
    assert failed["trajectory_sha256"] == (
        "4aaa1e944a2004b87c420d6a25d361bcd5316d992479d9a934cc1b10739b867a"
    )
    assert failed["attempt_consumed"] is True
    assert failed["attempt_reusable"] is False
    assert failed["authorization_reusable"] is False


def test_requested_preservation_is_evidence_only_and_non_force():
    record = request.preservation_authorization_request()["request"]
    requested = record["requested_preservation"]

    assert requested["exact_marker_and_run_artifacts_required"] is True
    assert requested["exact_clean_detached_registered_worktrees_required"] is True
    assert requested["engine_removed_before_source"] is True
    assert requested["non_force_git_worktree_remove_only"] is True
    assert requested["remaining_evidence_manifest_hashed"] is True
    assert requested["atomic_baseline_archive_rename_requested"] is True
    assert requested["marker_and_run_inode_preservation_required"] is True
    assert requested["create_only_preservation_receipt_requested"] is True

    assert requested["file_content_deletion_requested"] is False
    assert requested["force_worktree_removal_requested"] is False
    assert requested["runtime_retry_requested"] is False


def test_general_source_work_permission_is_not_preservation_authority():
    record = request.preservation_authorization_request()["request"]
    boundary = record["authorization_boundary"]

    assert boundary["preservation_authorization_requested"] is True
    assert boundary["fresh_explicit_user_authorization_required"] is True
    assert (
        boundary["general_source_work_authorization_is_preservation_authorization"]
        is False
    )
    assert boundary["matching_request_digest_grants_authority"] is False
    assert boundary["matching_request_bytes_grant_authority"] is False


@pytest.mark.parametrize("field", request.FALSE_AUTHORITY_FIELDS)
def test_request_record_grants_no_authority(field):
    record = request.preservation_authorization_request()["request"]
    assert record[field] is False


@pytest.mark.parametrize(
    "field",
    (
        "preservation_authorization_accepted",
        "request_grants_authority",
        "host_io_performed",
        "filesystem_mutation_performed",
        "git_worktree_mutation_performed",
        "archive_rename_performed",
        "preservation_receipt_created",
        "runtime_retry_authorized",
        "execution_request_opened",
        "runtime_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_validated_request_remains_non_authorizing(field):
    out = request.preservation_authorization_request()
    assert out[field] is False


def test_request_advances_only_to_source_binding_review():
    out = request.preservation_authorization_request()

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_AUTHORIZATION_REQUEST_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_accept_or_preserve_holds():
    with pytest.raises(
        request.Pair06V9AdapterRejectionPreservationAuthorizationRequestHold,
        match="PRESERVATION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.accept_or_preserve()
