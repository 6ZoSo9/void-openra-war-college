from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_invocation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_invocation_source_binding_review_generation2.py"
)


def test_exact_retry_invocation_identities_are_pinned():
    out = review.v2r13_pair03_baseline_retry_invocation_review_contract()
    assert out["retry_invocation_git_blob"] == (
        "3f9605c07ed4a3face78be0f8bb745ec9aebb1d8"
    )
    assert out["retry_invocation_source_sha256"] == (
        "4115abf23f7ab1570cf84ac9c74867a3d01a8af63213c4a4de3c84facbe2d33e"
    )
    assert out["precision_cli_git_blob"] == (
        "d9d30a856e958b423951fc602e55b7b24926f3ab"
    )
    assert out["precision_cli_source_sha256"] == (
        "84bbf23334fbe154b16345a2f60fa5763f9a1c9f3f5714bc1be6e186b0872935"
    )
    assert out["retry_test_git_blob"] == (
        "c8db66b3db36c359f54376a9186ad4a5f6096e13"
    )
    assert out["retry_test_sha256"] == (
        "6f87962e39d03ad0386def73e36463b8baa0a71ece7d2decb1ee4c0c9783bcd7"
    )


def test_review_scope_is_exactly_one_pair03_baseline_retry():
    out = review.v2r13_pair03_baseline_retry_invocation_review_contract()
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["retry_index"] == 1
    assert out["max_retry_executions"] == 1
    assert out["retry_execution_authorized"] is True
    assert out["retry_execution_invoked"] is False
    assert out["retry_execution_performed"] is False
    assert out["automatic_retry"] is False


def test_review_requires_preservation_recheck_and_repaired_executor():
    out = review.v2r13_pair03_baseline_retry_invocation_review_contract()
    assert out["live_preservation_recheck_reviewed"] is True
    assert out["repaired_first_baseline_executor_reuse_reviewed"] is True


def test_review_does_not_expand_authority():
    out = review.v2r13_pair03_baseline_retry_invocation_review_contract()
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


def test_review_advances_only_to_explicit_retry_invocation():
    out = review.v2r13_pair03_baseline_retry_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_REQUIRED"
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


def test_retry_entrypoint_holds_until_explicit_invocation():
    with pytest.raises(
        review.V2R13Pair03BaselineRetryInvocationReviewHold,
        match="V2R13_PAIR03_BASELINE_RETRY_INVOCATION_REQUIRED",
    ):
        review.invoke_retry()
