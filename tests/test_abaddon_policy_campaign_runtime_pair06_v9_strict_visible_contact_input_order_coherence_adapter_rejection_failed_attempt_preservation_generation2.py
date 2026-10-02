from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_generation2
    as preservation,
)


def test_contract_binds_exact_consumed_failure_and_stays_nonexecuting():
    out = (
        preservation
        .pair06_v9_input_order_adapter_rejection_failed_attempt_preservation_contract()
    )

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

    assert out["source_worktree_commit"] == (
        "973802ef0a614e5afa782ff20e231e18966ae3e5"
    )
    assert out["source_worktree_tree"] == (
        "d8a2af418af00e95ca0f203a2f0264851f2308c6"
    )
    assert out["engine_worktree_commit"] == (
        "1607a7a6501d42a47638393ecef8b22831064932"
    )
    assert out["engine_worktree_tree"] == (
        "bf562078c53edda3e6545f501b73ba1273c5df49"
    )

    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["new_execution_request_opened"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["game_execution_authorized"] is False


def test_contract_requires_exact_safe_preservation_shape():
    out = (
        preservation
        .pair06_v9_input_order_adapter_rejection_failed_attempt_preservation_contract()
    )

    assert out["exact_consumed_marker_required"] is True
    assert out["exact_run_artifacts_required"] is True
    assert out["result_must_be_absent"] is True
    assert out["closeout_must_be_absent"] is True
    assert out["summary_must_be_absent"] is True
    assert out["exact_clean_detached_registered_worktrees_required"] is True
    assert out["non_force_worktree_removal_only"] is True
    assert out["engine_removed_before_source"] is True
    assert out["remaining_evidence_manifest_hashed"] is True
    assert out["atomic_baseline_archive_rename_implemented"] is True
    assert out["attempt_marker_inode_preserved"] is True
    assert out["run_artifact_inode_preserved"] is True
    assert out["create_only_preservation_receipt_implemented"] is True


def test_manifest_hashes_regular_files_without_mutation(tmp_path: Path):
    root = tmp_path / "evidence"
    nested = root / "nested"
    nested.mkdir(parents=True)
    first = root / "a.txt"
    second = nested / "b.bin"
    first.write_bytes(b"alpha")
    second.write_bytes(b"beta")

    before = {
        first: first.read_bytes(),
        second: second.read_bytes(),
    }
    rows = preservation._evidence_manifest(root)

    assert [row["relative_path"] for row in rows] == [
        "a.txt",
        "nested/b.bin",
    ]
    assert rows[0]["sha256"] == hashlib.sha256(b"alpha").hexdigest()
    assert rows[1]["sha256"] == hashlib.sha256(b"beta").hexdigest()
    assert first.read_bytes() == before[first]
    assert second.read_bytes() == before[second]


def test_manifest_rejects_symlinked_evidence(tmp_path: Path):
    root = tmp_path / "evidence"
    root.mkdir()
    target = root / "target.txt"
    target.write_text("evidence", encoding="utf-8")
    (root / "link.txt").symlink_to(target)

    with pytest.raises(
        preservation.Pair06V9AdapterRejectionFailedAttemptPreservationHold,
        match="evidence file type drift",
    ):
        preservation._evidence_manifest(root)


def test_create_only_receipt_refuses_overwrite(tmp_path: Path):
    receipt = tmp_path / "receipt.json"
    payload = {"schema": "test", "value": 1}

    digest = preservation._write_create_only(receipt, payload)

    assert digest == hashlib.sha256(
        preservation._stable_bytes(payload)
    ).hexdigest()

    with pytest.raises(FileExistsError):
        preservation._write_create_only(receipt, payload)


def test_missing_preservation_authority_holds_before_host_inspection():
    with pytest.raises(
        preservation.Pair06V9AdapterRejectionFailedAttemptPreservationHold,
        match="PRESERVATION_AUTHORIZATION_REQUIRED",
    ):
        preservation.preserve_pair06_v9_input_order_adapter_rejection_failed_attempt(
            preservation_authorized=False,
            confirm=preservation.CONFIRM_TOKEN,
        )


def test_wrong_confirmation_holds_before_host_inspection():
    with pytest.raises(
        preservation.Pair06V9AdapterRejectionFailedAttemptPreservationHold,
        match="PRESERVATION_CONFIRMATION_REQUIRED",
    ):
        preservation.preserve_pair06_v9_input_order_adapter_rejection_failed_attempt(
            preservation_authorized=True,
            confirm="wrong",
        )


def test_source_contains_no_force_remove_or_retry_surface():
    source = Path(preservation.__file__).read_text(encoding="utf-8")

    assert "worktree\", \"remove" in source
    assert "--force" not in source
    assert "rm -rf" not in source
    assert "runtime_retry_authorized\": False" in source
    assert "automatic_retry\": False" in source


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_contract_grants_no_execution_or_follow_on_authority(field):
    out = (
        preservation
        .pair06_v9_input_order_adapter_rejection_failed_attempt_preservation_contract()
    )
    assert out[field] is False


def test_contract_advances_only_to_source_binding_review():
    out = (
        preservation
        .pair06_v9_input_order_adapter_rejection_failed_attempt_preservation_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_preserve_holds():
    with pytest.raises(
        preservation.Pair06V9AdapterRejectionFailedAttemptPreservationHold,
        match="FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        preservation.review_or_preserve()
