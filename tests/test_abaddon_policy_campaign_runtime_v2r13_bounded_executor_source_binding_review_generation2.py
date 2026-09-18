from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as executor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
EXECUTOR_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2.py"
)
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_bounded_executor_source_binding_review_generation2.py"
)


def test_exact_executor_identities_are_pinned():
    out = review.v2r13_bounded_executor_source_binding_review_contract()
    assert out["executor_git_blob"] == "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
    assert out["executor_source_sha256"] == (
        "92e92fb32b23b56a3986519d47f44653bb293739f03360de90b32ebf72664a16"
    )
    assert out["executor_test_git_blob"] == "8bbc22fced55191da23b110f79a83cae8b796ecd"
    assert out["executor_test_sha256"] == (
        "41216421831edc80223638674946261288d76f23b9024a5f232475f7a41c0fff"
    )


def test_review_accepts_exact_six_arm_v2r13_surface():
    out = review.v2r13_bounded_executor_source_binding_review()
    assert out["authorization_scope"] == "v2r13_lane_only"
    assert out["authorized_pair_slots"] == (3, 9, 15)
    assert out["held_out_pair_slots"] == (15,)
    assert out["authorized_arms"] == ("baseline", "candidate")
    assert out["authorized_execution_arm_count"] == 6
    rows = out["validated_executor"]["execution_plans"]
    assert len(rows) == 6
    assert {(row["pair_slot"], row["arm"]) for row in rows} == {
        (3, "baseline"),
        (3, "candidate"),
        (9, "baseline"),
        (9, "candidate"),
        (15, "baseline"),
        (15, "candidate"),
    }


def test_held_out_classification_is_exact():
    rows = review.v2r13_bounded_executor_source_binding_review()[
        "validated_executor"
    ]["execution_plans"]
    for row in rows:
        assert row["held_out"] is (row["pair_slot"] == 15)


def test_review_preserves_readiness_cleanup_and_revocation_invariants():
    out = review.v2r13_bounded_executor_source_binding_review()
    assert out["fresh_readiness_required_before_inference"] is True
    assert out["readiness_failure_cleanup_reviewed"] is True
    assert out["successful_runtime_cleanup_observation_reviewed"] is True
    assert out["revocation_checks_reviewed"] is True
    assert out["automatic_retry"] is False


def test_review_does_not_execute_or_expand_authority():
    out = review.v2r13_bounded_executor_source_binding_review()
    assert out["other_runtime_lanes_authorized"] is False
    assert out["runtime_execution_authorization_accepted"] is True
    assert out["runtime_execution_implemented"] is True
    assert out["runtime_execution_performed"] is False
    assert out["host_preflight_completed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_source_frontier_closes_only_to_host_preflight():
    out = review.v2r13_bounded_executor_source_binding_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_source_blockers"] == ()
    assert out["execution_blockers"] == (
        "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_REQUIRED"
    assert out["next_change_class"] == "v2r13_runtime_execution_host_preflight"


def test_executor_source_has_no_direct_network_or_subprocess_backend():
    tree = ast.parse(
        EXECUTOR_SOURCE.read_text(encoding="utf-8"),
        filename=str(EXECUTOR_SOURCE),
    )
    forbidden = {"subprocess", "socket", "http", "httpx", "requests", "urllib"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_executor_source_contains_required_runtime_safety_hooks():
    tree = ast.parse(
        EXECUTOR_SOURCE.read_text(encoding="utf-8"),
        filename=str(EXECUTOR_SOURCE),
    )
    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert "execute_v2r13_arm" in functions
    assert "guarded_start" in functions
    assert "recorded_cleanup" in functions
    assert "_run_artifact_receipt" in functions

    classes = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }
    assert "_FreshReadinessHooks" in classes


def test_review_source_itself_is_host_action_free():
    tree = ast.parse(
        REVIEW_SOURCE.read_text(encoding="utf-8"),
        filename=str(REVIEW_SOURCE),
    )
    forbidden = {
        "asyncio",
        "ctypes",
        "http",
        "httpx",
        "multiprocessing",
        "os",
        "pathlib",
        "requests",
        "shutil",
        "socket",
        "subprocess",
        "urllib",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_tampered_executor_contract_is_rejected(monkeypatch):
    original = executor.bounded_v2r13_runtime_executor_contract

    def tampered():
        value = deepcopy(original())
        value["automatic_retry"] = True
        return value

    review._validate_executor_cached.cache_clear()
    monkeypatch.setattr(
        executor,
        "bounded_v2r13_runtime_executor_contract",
        tampered,
    )
    try:
        with pytest.raises(
            review.V2R13BoundedExecutorSourceBindingReviewHold,
            match="automatic retry enabled",
        ):
            review.v2r13_bounded_executor_source_binding_review()
    finally:
        review._validate_executor_cached.cache_clear()


def test_review_execution_entrypoint_holds_at_host_preflight():
    with pytest.raises(
        review.V2R13BoundedExecutorSourceBindingReviewHold,
        match="V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_REQUIRED",
    ):
        review.execute_reviewed_v2r13_runtime()


def test_review_other_runtime_lane_holds():
    with pytest.raises(
        review.V2R13BoundedExecutorSourceBindingReviewHold,
        match="AUTHORIZATION_SCOPE_V2R13_ONLY",
    ):
        review.execute_other_runtime_lane()
