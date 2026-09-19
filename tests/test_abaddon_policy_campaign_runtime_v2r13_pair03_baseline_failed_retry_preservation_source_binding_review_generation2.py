from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_source_binding_review_generation2.py"
)


def test_exact_preservation_identities_are_pinned():
    out = review.v2r13_pair03_baseline_failed_retry_preservation_review_contract()
    assert out["preservation_contract_git_blob"] == (
        "b38480ebcb32fb0397f722dad89193e8ec58cb98"
    )
    assert out["preservation_contract_source_sha256"] == (
        "0d8aa7948afbb5e85d9b61d7d1911f82c4c498f29b1fbf3136d1fb4e138e0569"
    )
    assert out["precision_tool_git_blob"] == (
        "344d3e0cc811f0dc9c3b5450c4b0b69d9a4c0c38"
    )
    assert out["precision_tool_source_sha256"] == (
        "4a4c7ffdf247604e504b59c8d0d35e9c7152eed64fd8ed809dee39d77eed0a50"
    )
    assert out["preservation_test_git_blob"] == (
        "4b58cd554ac81ff46471d53382c731579a9830bc"
    )
    assert out["preservation_test_sha256"] == (
        "1b8c1537d4fbacbdd75c68a371c71f1e0a51ceca15f36726a2fbc67c9e8750cc"
    )


def test_review_accepts_exact_preservation_semantics():
    out = review.v2r13_pair03_baseline_failed_retry_preservation_review_contract()
    assert out["preservation_source_binding_present"] is True
    assert out["preservation_reviewed"] is True
    assert out["precision_tool_reviewed"] is True
    assert out["same_filesystem_atomic_rename_reviewed"] is True
    assert out["no_delete_api_reviewed"] is True
    assert out["original_first_attempt_archive_preservation_reviewed"] is True


def test_review_does_not_grant_another_retry():
    out = review.v2r13_pair03_baseline_failed_retry_preservation_review_contract()
    assert out["preservation_invoked"] is False
    assert out["failed_retry_deletion_authorized"] is False
    assert out["additional_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_execution_performed"] is False
    assert out["model_load_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
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
    out = review.v2r13_pair03_baseline_failed_retry_preservation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED"
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


def test_preservation_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineFailedRetryPreservationReviewHold,
        match="V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED",
    ):
        review.invoke_preservation()
