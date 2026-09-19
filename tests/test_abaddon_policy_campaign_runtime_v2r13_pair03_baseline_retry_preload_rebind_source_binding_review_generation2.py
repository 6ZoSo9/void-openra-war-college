from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_preload_rebind_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_preload_rebind_source_binding_review_generation2.py"
)


def test_exact_rebound_retry_identities_are_pinned():
    out = review.v2r13_pair03_baseline_retry_preload_rebind_review_contract()
    assert out["rebound_retry_git_blob"] == (
        "f75bcc19120db9044dbdafe629ab2c625b6a19a9"
    )
    assert out["rebound_retry_source_sha256"] == (
        "cc69c2c231f2c520184ddafe966989d23b002f853c1b3b9a311600cef5119b46"
    )
    assert out["rebound_retry_test_git_blob"] == (
        "76620e62259670cc63ac1d254e0600a3dd828536"
    )
    assert out["rebound_retry_test_sha256"] == (
        "54cb2515d6d8901a90a0600a32229887459f67f1c9bff79445907b9fa61571d4"
    )


def test_review_requires_both_readiness_repairs():
    out = review.v2r13_pair03_baseline_retry_preload_rebind_review_contract()
    assert out["retry_preload_rebind_source_binding_present"] is True
    assert out["retry_preload_rebind_reviewed"] is True
    assert out["worktree_readiness_repair_review_required"] is True
    assert out["model_preload_repair_review_required"] is True
    assert out["exact_v2r13_model_preload_before_readiness_required"] is True
    assert out["model_preload_inference_forbidden"] is True


def test_review_does_not_create_another_retry():
    out = review.v2r13_pair03_baseline_retry_preload_rebind_review_contract()
    assert out["automatic_retry"] is False
    assert out["additional_retry_authorized"] is False
    assert out["runtime_execution_invoked"] is False
    assert out["runtime_execution_performed"] is False
    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_to_failed_retry_forensics():
    out = review.v2r13_pair03_baseline_retry_preload_rebind_review_contract()
    assert out["failed_retry_forensics_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_FORENSICS_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_FORENSICS_REQUIRED"
    )


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


def test_execution_entrypoint_holds_at_forensics_gate():
    with pytest.raises(
        review.V2R13Pair03BaselineRetryPreloadRebindReviewHold,
        match="V2R13_PAIR03_BASELINE_FAILED_RETRY_FORENSICS_REQUIRED",
    ):
        review.execute_retry()
