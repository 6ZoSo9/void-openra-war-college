from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_failed_retry_preservation_guard_repair_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_failed_retry_preservation_guard_repair_source_binding_review_generation2.py"
)


def test_exact_repair_identities_are_pinned():
    out = review.v2r13_failed_retry_preservation_guard_repair_review_contract()
    assert out["preservation_contract_git_blob"] == (
        "b38480ebcb32fb0397f722dad89193e8ec58cb98"
    )
    assert out["corrected_precision_tool_git_blob"] == (
        "812d78f28f8d7f0b486b1b2bb7cce3b9da2a2733"
    )
    assert out["corrected_precision_tool_source_sha256"] == (
        "cf003915c8e9d7cac58c080ac9455f815afc7bea120a4b5056718957ca02913c"
    )
    assert out["corrected_test_git_blob"] == (
        "1ac81d60ed4bdb7877d8bb34919952b4e83381fb"
    )
    assert out["corrected_test_sha256"] == (
        "ddba7d498fcc061fd477fd4c64052e95c62f8f433191f78b20208ecaec01d071"
    )


def test_review_binds_true_implementation_state():
    out = review.v2r13_failed_retry_preservation_guard_repair_review_contract()
    assert out["guard_repair_source_binding_present"] is True
    assert out["guard_repair_reviewed"] is True
    assert out["expected_preservation_implemented_value"] is True
    assert out["contract_implementation_guard_polarity_correct"] is True


def test_review_preserves_nonruntime_boundaries():
    out = review.v2r13_failed_retry_preservation_guard_repair_review_contract()
    assert out["preservation_invoked"] is False
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
    out = review.v2r13_failed_retry_preservation_guard_repair_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED"
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


def test_preservation_entrypoint_holds():
    with pytest.raises(
        review.V2R13FailedRetryPreservationGuardRepairReviewHold,
        match="V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED",
    ):
        review.invoke_preservation()
