from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry2_execution_evidence_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry2_execution_evidence_source_binding_review_generation2.py"
)


def test_exact_acceptance_identities_are_pinned():
    out = review.v2r13_pair03_baseline_retry2_execution_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == (
        "037730c77bc67cbd722becc30fc898b50cba842b"
    )
    assert out["acceptance_source_sha256"] == (
        "189f500b329c852c69da6b78736e0ae028ca5c77dd28875f79023852ed033695"
    )
    assert out["acceptance_test_git_blob"] == (
        "8b2a70e4368b60b6182ea29f6fa82906bc936881"
    )
    assert out["acceptance_test_sha256"] == (
        "5514ab6de3928165d1ce23cb08e562250aba0541a4ce59ac9051d3a53ebe5147"
    )


def test_review_binds_completed_retry2_result():
    out = review.v2r13_pair03_baseline_retry2_execution_evidence_review_contract()
    assert out["retry2_execution_evidence_source_binding_present"] is True
    assert out["retry2_execution_evidence_reviewed"] is True
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["retry_index"] == 2
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["rounds_completed"] == 36
    assert out["trajectory_sha256"] == (
        "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
    )
    assert out["summary_sha256"] == (
        "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
    )


def test_review_records_authority_exhausted():
    out = review.v2r13_pair03_baseline_retry2_execution_evidence_review_contract()
    assert out["retry_authorization_consumed"] is True
    assert out["remaining_retry_executions"] == 0
    assert out["another_retry_authorized"] is False
    assert out["candidate_arm_authorized"] is False
    assert out["candidate_arm_executed"] is False
    assert out["held_out_arm_authorized"] is False
    assert out["held_out_arm_executed"] is False


def test_review_keeps_training_and_promotion_closed():
    out = review.v2r13_pair03_baseline_retry2_execution_evidence_review_contract()
    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


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


def test_review_advances_only_to_baseline_result_review():
    out = review.v2r13_pair03_baseline_retry2_execution_evidence_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["baseline_result_review_required"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_RESULT_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_PAIR03_BASELINE_RESULT_REVIEW_REQUIRED"


def test_follow_on_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineRetry2ExecutionEvidenceReviewHold,
        match="V2R13_PAIR03_BASELINE_RESULT_REVIEW_REQUIRED",
    ):
        review.authorize_follow_on_execution()
