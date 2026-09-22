from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_evaluation_design_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_evaluation_design_source_binding_review_generation2.py"
)


def test_review_pins_exact_design_source_and_tests():
    out = review.v2r13_pair09_evaluation_design_review_contract()
    assert out["design_git_blob"] == "3e110288a6f0e4f14fbe9e591e8d1840cb786975"
    assert out["design_source_sha256"] == (
        "5690f1993fa7e2ea6cff28451c57bcbc725c57ae81450cc499839efea26f29bf"
    )
    assert out["design_test_git_blob"] == "272be1e4c070a721b56c287b7d3ecf7cc8a77511"
    assert out["design_test_sha256"] == (
        "2dfbcc54f70aa6490843d3c42dda2efb2df5a4ef5e7ce20dc99c70e721280aa5"
    )


def test_review_accepts_nonheld_baseline_first_pair09_design():
    out = review.v2r13_pair09_evaluation_design_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_evaluation_design_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arms"] == ("baseline", "candidate")
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["baseline_must_complete_before_candidate"] is True


def test_review_preserves_candidate_without_promotion_or_rejection():
    out = review.v2r13_pair09_evaluation_design_review_contract()
    assert out["candidate_policy_preserved_from_pair03"] is True
    assert out["candidate_policy_promoted"] is False
    assert out["candidate_policy_rejected"] is False
    assert out["candidate_replay_permitted"] is False


def test_review_advances_only_to_pair09_baseline_preparation():
    out = review.v2r13_pair09_evaluation_design_review_contract()
    assert out["pair09_baseline_execution_preparation_required"] is True
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["pair09_execution_performed"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_PREPARATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_PREPARATION_REQUIRED"
    )


def test_review_grants_no_training_promotion_or_external_authority():
    out = review.v2r13_pair09_evaluation_design_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
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


def test_execution_entrypoints_remain_closed():
    with pytest.raises(
        review.V2R13Pair09EvaluationDesignReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_NOT_AUTHORIZED",
    ):
        review.execute_pair09_baseline()

    with pytest.raises(
        review.V2R13Pair09EvaluationDesignReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_NOT_AUTHORIZED",
    ):
        review.execute_pair09_candidate()

    with pytest.raises(
        review.V2R13Pair09EvaluationDesignReviewHold,
        match="V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
    ):
        review.execute_held_out_pair()
