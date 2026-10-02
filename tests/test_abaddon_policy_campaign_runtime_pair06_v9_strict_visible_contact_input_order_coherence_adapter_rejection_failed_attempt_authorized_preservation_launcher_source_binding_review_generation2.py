from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_authorized_preservation_launcher_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_launcher_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_preservation_launcher_review_contract()
    )

    assert out["launcher_path"] == review.LAUNCHER_PATH
    assert out["launcher_git_blob"] == review.LAUNCHER_GIT_BLOB
    assert out["launcher_test_path"] == review.LAUNCHER_TEST_PATH
    assert out["launcher_test_git_blob"] == review.LAUNCHER_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.LAUNCHER_PATH).read_bytes()) == (
        review.LAUNCHER_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.LAUNCHER_TEST_PATH).read_bytes()) == (
        review.LAUNCHER_TEST_GIT_BLOB
    )


def test_review_binds_exact_authorization_and_marker():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_preservation_launcher_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_authorized_preservation_launcher_reviewed"
    ] is True
    assert out["attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["authorization_text_sha256"] == (
        "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
    )
    assert out["authorization_text_bytes"] == 35


def test_review_preserves_exact_one_shot_preservation_boundary():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_preservation_launcher_review_contract()
    )

    assert out["exact_current_main_required"] is True
    assert out["exact_launcher_source_sha256_required"] is True
    assert out["explicit_launcher_confirmation_token_required"] is True
    assert out["preservation_delegation_exactly_once"] is True
    assert out["non_force_worktree_removal_required"] is True
    assert out["atomic_archive_rename_required"] is True
    assert out["create_only_preservation_receipt_required"] is True


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
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
        .pair06_v9_adapter_rejection_authorized_preservation_launcher_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_host_preservation():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_preservation_launcher_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_HOST_PRESERVATION_REQUIRED"
    )


def test_preserve_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionAuthorizedPreservationLauncherReviewHold,
        match="AUTHORIZED_HOST_PRESERVATION_REQUIRED",
    ):
        review.preserve()
