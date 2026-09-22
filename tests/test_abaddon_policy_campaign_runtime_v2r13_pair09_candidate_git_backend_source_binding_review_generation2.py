from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_git_backend_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_candidate_git_backend_source_binding_review_generation2.py"
)


def test_review_pins_exact_backend_source_and_tests():
    out = review.v2r13_pair09_candidate_git_backend_review_contract()
    assert out["backend_git_blob"] == "6cb3b780d9beab0dcaaacae4ccb3ffd24701489d"
    assert out["backend_source_sha256"] == (
        "ab76220fbca190e8b9ef25f4b8148187f6454d590ed73d53ecee609cb68fafee"
    )
    assert out["backend_test_git_blob"] == "c703a89fd12d0b1ebd63a50a4e63e004fd2af6b4"
    assert out["backend_test_sha256"] == (
        "6faf828f1b7405786bfb907146c1eaf0b409ebaad4bf68dddeb5b75807afa00a"
    )


def test_review_accepts_only_exact_pair09_candidate_backend():
    out = review.v2r13_pair09_candidate_git_backend_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_candidate_git_backend_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["binding_count"] == 2
    assert out["restricted_git_worktree_backend_reviewed"] is True


def test_review_preserves_restricted_command_boundary():
    out = review.v2r13_pair09_candidate_git_backend_review_contract()
    for field in (
        "fetch_implemented",
        "canonical_checkout_implemented",
        "force_remove_implemented",
        "reset_implemented",
        "clean_implemented",
        "config_implemented",
        "prune_implemented",
        "runtime_execution_authorized",
        "runtime_execution_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


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


def test_review_advances_only_to_candidate_invocation():
    out = review.v2r13_pair09_candidate_git_backend_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_INVOCATION_IMPLEMENTATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateGitBackendReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_candidate()
