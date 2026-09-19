from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_source_binding_review_generation2.py"
)


def test_exact_preservation_identities_are_pinned():
    out = review.v2r13_pair03_baseline_failed_attempt_preservation_review_contract()
    assert out["preservation_git_blob"] == (
        "a00bea0b49121664988a80e85db10ea4496b0779"
    )
    assert out["preservation_source_sha256"] == (
        "6dae62de49f2757bbd216e22db9f42c983735fa47f90e85f26b8fa888ba1fdaf"
    )
    assert out["precision_cli_git_blob"] == (
        "0e0fbf7b1bd76ea392a90c80bb9bcbfcb55fc17c"
    )
    assert out["precision_cli_source_sha256"] == (
        "d07eb7761f727df66bf61a8a29fb839a14c1e40b130dd0585e7a90179a83443b"
    )
    assert out["preservation_test_git_blob"] == (
        "b742b2f56a72e2d8259213c61dff8c3cb81c5586"
    )
    assert out["preservation_test_sha256"] == (
        "54a20aee0cb55f096a2c9cc55b13fe961e6daf9e90ef34b24b5f450740ff5cb1"
    )


def test_review_preserves_exact_archival_semantics():
    out = review.v2r13_pair03_baseline_failed_attempt_preservation_review()
    assert out["preservation_reviewed"] is True
    assert out["failed_attempt_deletion_authorized"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_execution_performed"] is False


def test_review_does_not_expand_authority():
    out = review.v2r13_pair03_baseline_failed_attempt_preservation_review()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_preservation_invocation():
    out = review.v2r13_pair03_baseline_failed_attempt_preservation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["preservation_source_binding_present"] is True
    assert out["preservation_reviewed"] is True
    assert out["preservation_invoked"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED"
    )


def test_review_source_is_host_action_free():
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


def test_preservation_invocation_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineFailedAttemptPreservationReviewHold,
        match="V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
    ):
        review.invoke_preservation()
