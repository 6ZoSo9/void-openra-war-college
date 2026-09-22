from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_evidence_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_evidence_source_binding_review_generation2.py"
)


def test_exact_acceptance_identities_are_pinned():
    out = review.v2r13_pair03_candidate_execution_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == "79f9a674272a2bf67f315d79cc61778a8f53408d"
    assert out["acceptance_source_sha256"] == (
        "97d5d6127fa450207e32d4262d21490d8bcc15633779644142af27fdba8d57de"
    )
    assert out["acceptance_test_git_blob"] == "cb35ebdddcefa6110baf3b1fa5d63df60911fcfc"
    assert out["acceptance_test_sha256"] == (
        "e087428b5a9469ec234ba0cdc32f4010e1f0405655c1140d750e142a82f86317"
    )


def test_review_binds_completed_candidate_result():
    out = review.v2r13_pair03_candidate_execution_evidence_review_contract()
    assert out["candidate_execution_evidence_source_binding_present"] is True
    assert out["candidate_execution_evidence_reviewed"] is True
    assert out["pair_slot"] == 3
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["trajectory_sha256"] == (
        "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65"
    )
    assert out["summary_sha256"] == (
        "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0"
    )


def test_review_records_consumed_nonreplayable_attempt():
    out = review.v2r13_pair03_candidate_execution_evidence_review_contract()
    assert out["candidate_attempt_consumed"] is True
    assert out["candidate_execution_performed"] is True
    assert out["candidate_completed_result_present"] is True
    assert out["candidate_execution_replay_required"] is False
    assert out["candidate_execution_replay_permitted"] is False
    assert out["runtime_cleanup_completed"] is True
    assert out["fresh_runtime_readiness_admitted"] is True
    assert out["completed_baseline_preserved"] is True


def test_review_keeps_all_follow_on_authority_closed():
    out = review.v2r13_pair03_candidate_execution_evidence_review_contract()
    assert out["automatic_retry"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["pair09_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
    for field in (
        "training_authorized", "training_performed",
        "weights_update_authorized", "weights_updated",
        "automatic_policy_promotion_authorized", "automatic_policy_promotion",
        "deployment_authorized", "deployment_performed",
        "void_chain_mutation_authorized", "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized", "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_review_source_is_host_action_free():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "os", "pathlib", "socket", "subprocess",
        "urllib", "requests", "httpx",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_review_advances_only_to_candidate_result_review():
    out = review.v2r13_pair03_candidate_execution_evidence_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["candidate_result_review_required"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_RESULT_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_PAIR03_CANDIDATE_RESULT_REVIEW_REQUIRED"


def test_follow_on_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03CandidateExecutionEvidenceReviewHold,
        match="V2R13_PAIR03_CANDIDATE_RESULT_REVIEW_REQUIRED",
    ):
        review.authorize_follow_on_execution()
