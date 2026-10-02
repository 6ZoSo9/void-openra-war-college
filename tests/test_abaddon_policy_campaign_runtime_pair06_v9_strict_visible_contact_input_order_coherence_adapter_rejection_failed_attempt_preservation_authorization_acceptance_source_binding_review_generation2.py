from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract()
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


def test_review_binds_exact_authorization_and_main_snapshot():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_preservation_authorization_acceptance_reviewed"
    ] is True
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
    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )


def test_review_accepts_only_preservation_and_no_runtime_authority():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract()
    )

    assert out["preservation_authorization_accepted"] is True
    assert out["preservation_authorized"] is True
    assert out["non_force_git_worktree_removal_authorized"] is True
    assert out["atomic_baseline_archive_rename_authorized"] is True
    assert out["create_only_preservation_receipt_authorized"] is True

    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["execution_request_opened"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["preservation_performed"] is False
    assert out["authorization_reusable_after_preservation"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "execution_request_opened",
        "runtime_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "preservation_performed",
        "authorization_reusable_after_preservation",
    ),
)
def test_review_grants_no_runtime_or_follow_on_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorized_preservation_launcher():
    out = (
        review
        .pair06_v9_adapter_rejection_preservation_authorization_acceptance_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED"
    )


def test_preserve_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionPreservationAuthorizationAcceptanceReviewHold,
        match="AUTHORIZED_PRESERVATION_LAUNCHER_REQUIRED",
    ):
        review.preserve()
