from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_source_binding_review_generation2.py"
)


def test_exact_invocation_identities_are_pinned():
    out = review.v2r13_first_baseline_invocation_source_binding_review_contract()
    assert out["invocation_git_blob"] == (
        "3f4580948aca13a1748703fa0a38a01463a10352"
    )
    assert out["invocation_source_sha256"] == (
        "9b1fdab1d371113e68a01f07ae221b60e7a8975aec51639e0fb7d28dadfe893b"
    )
    assert out["precision_cli_git_blob"] == (
        "f543834f86ff52be41498123b423cc1ab9e75f49"
    )
    assert out["precision_cli_source_sha256"] == (
        "255838f63a26dd7c85d29a37ae4df28385698a6f579a0ce27b8c899f5c9857a3"
    )
    assert out["invocation_test_git_blob"] == (
        "8d0c351a7f851f07f464155d0c539f3b255c3809"
    )
    assert out["invocation_test_sha256"] == (
        "ec941066059d485196a99d61fcb2731c4dc2948c5bbb5b36108f929403326373"
    )


def test_review_scope_is_exact_pair03_baseline():
    out = review.v2r13_first_baseline_invocation_source_binding_review()
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["candidate_arm_reviewed_for_execution"] is False
    assert out["held_out_arm_reviewed_for_execution"] is False


def test_review_preserves_runtime_safety_gates():
    out = review.v2r13_first_baseline_invocation_source_binding_review()
    assert out["current_main_preflight_required"] is True
    assert out["cached_sudo_required"] is True
    assert out["revocation_sentinel_required_absent"] is True
    assert out["restricted_git_backend_reviewed"] is True
    assert out["fresh_readiness_before_inference_reviewed"] is True
    assert out["automatic_retry"] is False


def test_review_does_not_execute_or_expand_authority():
    out = review.v2r13_first_baseline_invocation_source_binding_review()
    assert out["runtime_execution_authorized"] is True
    assert out["runtime_execution_invoked"] is False
    assert out["runtime_execution_performed"] is False
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


def test_source_frontier_closes_to_first_baseline_invocation_only():
    out = review.v2r13_first_baseline_invocation_source_binding_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_source_blockers"] == ()
    assert out["execution_blockers"] == (
        "V2R13_FIRST_BASELINE_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_FIRST_BASELINE_INVOCATION_REQUIRED"
    assert out["next_change_class"] == (
        "precision_v2r13_pair03_baseline_invocation"
    )


def test_review_source_itself_is_host_action_free():
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


def test_review_invocation_entrypoint_holds():
    with pytest.raises(
        review.V2R13FirstBaselineInvocationSourceBindingReviewHold,
        match="V2R13_FIRST_BASELINE_INVOCATION_REQUIRED",
    ):
        review.invoke_first_baseline()
