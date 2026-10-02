from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_preservation_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract()
    )

    assert out["preservation_path"] == review.PRESERVATION_PATH
    assert out["preservation_git_blob"] == review.PRESERVATION_GIT_BLOB
    assert out["preservation_test_path"] == review.PRESERVATION_TEST_PATH
    assert out["preservation_test_git_blob"] == review.PRESERVATION_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.PRESERVATION_PATH).read_bytes()) == (
        review.PRESERVATION_GIT_BLOB
    )
    assert _git_blob_sha1(
        (ROOT / review.PRESERVATION_TEST_PATH).read_bytes()
    ) == review.PRESERVATION_TEST_GIT_BLOB


def test_review_binds_exact_failed_attempt_evidence():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_failed_attempt_preservation_reviewed"
    ] is True
    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["warm_start_sha256"] == (
        "9ad33940dcc8199a61b6fa8bb5fb68f2eb8cc846fb745cf7e64c27e6e053b0e1"
    )
    assert out["warm_start_bytes"] == 229255
    assert out["trajectory_sha256"] == (
        "4aaa1e944a2004b87c420d6a25d361bcd5316d992479d9a934cc1b10739b867a"
    )
    assert out["trajectory_bytes"] == 58075


def test_review_preserves_only_evidence_and_grants_no_retry():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract()
    )

    assert out["non_force_worktree_removal_only"] is True
    assert out["atomic_baseline_archive_rename_reviewed"] is True
    assert out["evidence_inode_preservation_reviewed"] is True
    assert out["create_only_preservation_receipt_reviewed"] is True

    assert out["preservation_authorization_accepted"] is False
    assert out["preservation_performed"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["new_execution_request_opened"] is False


@pytest.mark.parametrize(
    "field",
    (
        "preservation_authorization_accepted",
        "preservation_performed",
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_mutation_or_execution_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_preservation_authorization_request():
    out = (
        review
        .pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_request_or_preserve_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionFailedAttemptPreservationReviewHold,
        match="FAILED_ATTEMPT_PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_or_preserve()
