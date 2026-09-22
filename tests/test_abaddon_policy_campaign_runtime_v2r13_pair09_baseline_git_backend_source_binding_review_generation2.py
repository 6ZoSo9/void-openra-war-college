from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_git_backend_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_baseline_git_backend_source_binding_review_generation2.py"
)


def test_review_pins_exact_backend_and_preflight_sources():
    out = review.v2r13_pair09_baseline_git_backend_review_contract()
    assert out["backend_git_blob"] == "9be2736081b67895faa9ecb5c4d978445a9f4a32"
    assert out["backend_source_sha256"] == (
        "32eb8b36a0f6e13ae710b63a0d40601595a52b9134766a2b414fdf7f12334647"
    )
    assert out["backend_test_git_blob"] == (
        "38acffa3b1a766dfcd611a7702526aed0c5e6eb6"
    )
    assert out["backend_test_sha256"] == (
        "adc4d4c64f50ba98ca7d45bbce094e035465c1cefd5de96c1eb43cb279a67c55"
    )
    assert out["preflight_review_git_blob"] == (
        "01f95aee884a699b3e46472c3a12bfbfb0c3332d"
    )
    assert out["preflight_review_source_sha256"] == (
        "8410d052bf15b2036323e12eb7b011c3a1e110fcd2f28df1d724cde3a25f53b2"
    )


def test_review_accepts_exact_pair09_baseline_backend():
    out = review.v2r13_pair09_baseline_git_backend_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_baseline_git_backend_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["fixed_source_root"] == "/home/zoso/dev/openra-rl-war-college"
    assert out["fixed_arm_root"].endswith(
        "/generation2/pair-09/baseline"
    )
    assert out["frozen_source_commit"] == (
        "973802ef0a614e5afa782ff20e231e18966ae3e5"
    )
    assert out["frozen_engine_commit"] == (
        "1607a7a6501d42a47638393ecef8b22831064932"
    )


def test_review_keeps_git_and_runtime_scope_closed():
    out = review.v2r13_pair09_baseline_git_backend_review_contract()
    assert out["fetch_implemented"] is False
    assert out["canonical_checkout_implemented"] is False
    assert out["force_remove_implemented"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_execution_performed"] is False
    assert out["automatic_retry"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_invocation_implementation():
    out = review.v2r13_pair09_baseline_git_backend_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED"
    )


def test_review_source_has_no_direct_host_action_surface():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "os", "pathlib", "socket", "subprocess", "urllib",
        "requests", "httpx", "asyncio", "multiprocessing",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_authorize_or_execute_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09BaselineGitBackendReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_baseline()
