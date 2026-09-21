from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_canary_opponent_source_binding_review_v1 as review


def test_review_binds_exact_deterministic_opponent_after_seed_selection():
    out = review.scout_repair_opponent_source_binding_review()
    assert out["seed_derivation"]["seed"] == 1100292357
    assert out["opponent_source_reviewed"] is True
    assert out["opponent"] == {
        "implementation": "deterministic_pressure_opponent_v1",
        "source_identity": {
            "path": review.OPPONENT_PATH,
            "git_blob": review.OPPONENT_GIT_BLOB,
            "sha256": review.OPPONENT_SHA256,
            "committed_on_accepted_main_verified": False,
        },
        "model_backed": False,
        "deterministic_required": True,
        "same_for_both_arms": True,
        "proposal_only": True,
        "unchanged_host_validation_required": True,
        "execution_authority": False,
    }


def test_review_does_not_fake_accepted_main_or_runtime_acceptance():
    out = review.scout_repair_opponent_source_binding_review()
    assert out["accepted_main_head_with_repair"] is None
    assert out["runtime_image_identity"] is None
    assert out["attempt_directory"] is None
    assert out["attempt_guard_source_identity"] is None
    assert out["invocation_source_identities"] is None
    assert out["post_run_evidence_contract"] is None


def test_authority_stays_closed():
    out = review.scout_repair_opponent_source_binding_review()
    assert out["execution_authorized"] is False
    assert out["execution_performed"] is False
    assert out["automatic_retry"] is False
    assert out["opponent"]["execution_authority"] is False
    assert out["next_gate"] == review.NEXT_GATE


def test_review_is_stable_and_independent():
    first = review.scout_repair_opponent_source_binding_review()
    first["opponent"]["source_identity"]["committed_on_accepted_main_verified"] = True
    later = review.scout_repair_opponent_source_binding_review()
    assert later["opponent"]["source_identity"]["committed_on_accepted_main_verified"] is False


def test_execution_entrypoint_always_holds():
    with pytest.raises(review.ScoutRepairOpponentSourceBindingHold, match=review.NEXT_GATE):
        review.authorize_or_execute(authorized=True)


def test_source_only_import_surface():
    tree = ast.parse(Path(review.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "copy", "typing", "openra_env.learning"}
