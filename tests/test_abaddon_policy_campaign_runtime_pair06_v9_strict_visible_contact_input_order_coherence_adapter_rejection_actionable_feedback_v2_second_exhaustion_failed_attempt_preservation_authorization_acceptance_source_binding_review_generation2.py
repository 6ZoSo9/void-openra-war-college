from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract()
    )

    assert out["acceptance_path"] == review.ACCEPTANCE_PATH
    assert out["acceptance_git_blob"] == review.ACCEPTANCE_GIT_BLOB
    assert out["acceptance_test_path"] == review.ACCEPTANCE_TEST_PATH
    assert out["acceptance_test_git_blob"] == review.ACCEPTANCE_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_PATH).read_bytes()) == (
        review.ACCEPTANCE_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_TEST_PATH).read_bytes()) == (
        review.ACCEPTANCE_TEST_GIT_BLOB
    )


def test_review_binds_exact_authorization_request_and_main():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract()
    )

    assert out[
        "pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_reviewed"
    ] is True
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


def test_review_accepts_only_preservation_scope():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract()
    )

    assert out["preservation_authorization_accepted"] is True
    assert out["preservation_authorized"] is True
    assert out["filesystem_mutation_authorized"] is True
    assert out["git_worktree_mutation_authorized"] is True
    assert out["archive_rename_authorized"] is True
    assert out["preservation_receipt_creation_authorized"] is True

    assert out["first_v2_archive_mutation_authorized"] is False
    assert out["prior_preservation_authorization_reusable"] is False
    assert out["prior_execution_authorization_reusable"] is False
    assert out["preservation_performed_by_this_record"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "execution_request_opened",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_runtime_or_follow_on_authority(field):
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorized_preservation_launcher():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_authorization_acceptance_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
        "AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9V2SecondExhaustionPreservationAuthorizationAcceptanceReviewHold,
        match="AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED",
    ):
        review.preserve()
