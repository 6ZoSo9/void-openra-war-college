from __future__ import annotations

import hashlib
import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_request_generation2
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


def test_request_binds_exact_v2_failed_attempt_and_preservation_source():
    record = request.preservation_authorization_request()["request"]

    assert record["source_binding"]["preservation_stack_head"] == (
        "ee6a45530e6982771cfc3ec92e838fa224885cc3"
    )
    assert record["source_binding"]["preservation_git_blob"] == (
        "92981d23b580059fd3419cfe95daea561aab6add"
    )
    assert record["source_binding"]["preservation_review_git_blob"] == (
        "62f21456cbd358cf8cff9d621d4530485b9531f5"
    )

    failed = record["failed_attempt"]
    assert failed["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert failed["attempt_marker_bytes"] == 2208
    assert failed["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert failed["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )
    assert failed["failure_class"] == "strict_contact_actionable_feedback_v2_exhausted"
    assert failed["failure_round"] == 6
    assert failed["maximum_decision_attempts"] == 6
    assert failed["attempt_consumed"] is True
    assert failed["attempt_reusable"] is False
    assert failed["authorization_reusable"] is False


def test_requested_preservation_is_evidence_only_and_non_force():
    requested = request.preservation_authorization_request()["request"][
        "requested_preservation"
    ]

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
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_accept_or_preserve_holds():
    with pytest.raises(
        request.Pair06V9ActionableFeedbackV2PreservationAuthorizationRequestHold,
        match="PRESERVATION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.accept_or_preserve()
