from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_worktree_readiness_repair_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_first_baseline_worktree_readiness_repair_source_binding_review_generation2.py"
)


def test_exact_repair_identities_are_pinned():
    out = review.v2r13_first_baseline_worktree_readiness_repair_review_contract()
    assert out["repaired_invocation_git_blob"] == (
        "c5785b53ed0261981f25db116ceb1a43042a7580"
    )
    assert out["repaired_invocation_source_sha256"] == (
        "b840ae629eb2599aa61c6bad2661ca1f3d2dd4d66204579c980666325311816c"
    )
    assert out["repaired_test_git_blob"] == (
        "52f7d70e8ecb8b99efb85c5dc1aa17b52e258961"
    )
    assert out["repaired_test_sha256"] == (
        "8b1e97e732030ac2bb6cb0cbabff8b07926b1a0cdc1a77d76ba931352f054ed9"
    )


def test_review_accepts_exact_materializer_to_observer_bridge():
    out = review.v2r13_first_baseline_worktree_readiness_repair_review()
    assert out["materialization_receipt_direct_worktree_admission"] is False
    assert out["materialization_path_record_observed_before_live_readiness"] is True
    assert out["canonical_worktree_observation_validated_before_live_readiness"] is True
    assert out["explicit_host_lstat_backend_reviewed"] is True
    assert out["reviewed_git_observer_backend_reviewed"] is True
    assert out["reviewed_path_resolver_reviewed"] is True


def test_review_does_not_authorize_retry_or_expand_runtime_scope():
    out = review.v2r13_first_baseline_worktree_readiness_repair_review()
    assert out["runtime_retry_authorized_by_this_review"] is False
    assert out["automatic_retry"] is False
    assert out["candidate_arm_authorized_by_this_review"] is False
    assert out["held_out_arm_authorized_by_this_review"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_to_failed_attempt_forensics():
    out = review.v2r13_first_baseline_worktree_readiness_repair_review_contract()
    assert out["repair_source_binding_present"] is True
    assert out["repair_reviewed"] is True
    assert out["runtime_retry_authorized"] is False
    assert out["failed_attempt_forensics_required"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_FORENSICS_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_FORENSICS_REQUIRED"
    )
    assert out["source_frontier_closed"] is True


def test_review_source_has_no_host_io_imports():
    tree = ast.parse(
        REVIEW_SOURCE.read_text(encoding="utf-8"),
        filename=str(REVIEW_SOURCE),
    )
    forbidden = {
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "httpx",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_retry_entrypoint_holds_until_forensics():
    with pytest.raises(
        review.V2R13FirstBaselineReadinessRepairReviewHold,
        match="V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_FORENSICS_REQUIRED",
    ):
        review.retry_pair03_baseline()
