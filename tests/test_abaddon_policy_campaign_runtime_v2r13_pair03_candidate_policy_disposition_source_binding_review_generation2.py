from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_policy_disposition_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_candidate_policy_disposition_source_binding_review_generation2.py"
)


def test_review_pins_exact_disposition_source_and_tests():
    out = review.v2r13_pair03_candidate_policy_disposition_review_contract()
    assert out["disposition_git_blob"] == "de74c9107d29e8f415330b75e4b4cd2c1c288146"
    assert out["disposition_source_sha256"] == (
        "1dbe6ed33d1f2946267173612e2f06355b83c8e338da612f8abce99fe5194f0a"
    )
    assert out["disposition_test_git_blob"] == "351c2a2f17db052bf51a46d3acb58a2551398bf2"
    assert out["disposition_test_sha256"] == (
        "802f06ffa9bc9a95c00a676308a3c216ecaab1b583d5bd82c7b0dd0b683fd922"
    )


def test_review_is_separate_and_accepts_preservation_disposition():
    out = review.v2r13_pair03_candidate_policy_disposition_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["policy_disposition_reviewed"] is True
    assert out["policy_disposition"] == (
        "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION"
    )
    assert out["candidate_preserved_as_evidence"] is True
    assert out["candidate_promoted"] is False
    assert out["candidate_rejected"] is False


def test_review_advances_only_to_pair09_design():
    out = review.v2r13_pair03_candidate_policy_disposition_review_contract()
    assert out["additional_bounded_evaluation_required"] is True
    assert out["pair09_evaluation_design_required"] is True
    assert out["pair09_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_EVALUATION_DESIGN_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_PAIR09_EVALUATION_DESIGN_REQUIRED"


def test_review_keeps_replay_training_promotion_and_external_authority_closed():
    out = review.v2r13_pair03_candidate_policy_disposition_review_contract()
    assert out["candidate_replay_permitted"] is False
    for field in (
        "training_authorized", "training_performed",
        "weights_update_authorized", "weights_updated",
        "automatic_policy_promotion_authorized", "automatic_policy_promotion",
        "deployment_authorized", "deployment_performed",
        "void_chain_mutation_authorized", "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized", "wallet_or_funds_action_performed",
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


def test_execution_and_promotion_entrypoints_remain_closed():
    with pytest.raises(
        review.V2R13Pair03CandidatePolicyDispositionReviewHold,
        match="V2R13_PAIR09_EXECUTION_NOT_AUTHORIZED",
    ):
        review.authorize_pair09_execution()

    with pytest.raises(
        review.V2R13Pair03CandidatePolicyDispositionReviewHold,
        match="V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
    ):
        review.authorize_held_out_execution()

    with pytest.raises(
        review.V2R13Pair03CandidatePolicyDispositionReviewHold,
        match="V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
    ):
        review.promote_or_train_candidate()
