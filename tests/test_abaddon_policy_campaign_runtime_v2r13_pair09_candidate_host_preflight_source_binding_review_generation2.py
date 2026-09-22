from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_host_preflight_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_candidate_host_preflight_source_binding_review_generation2.py"
)


def test_review_pins_exact_preflight_source_and_tests():
    out = review.v2r13_pair09_candidate_host_preflight_review_contract()
    assert out["preflight_git_blob"] == "1cc236ac9706fef4731d3335d5ba53cd181c38c3"
    assert out["preflight_source_sha256"] == (
        "17a38abe77b3c06fb178ad641ba59bf3b319485df6aa3c17202ddc39006462e8"
    )
    assert out["preflight_test_git_blob"] == "fba24796ecc7ddec730625eadb8bd61dc29c4d85"
    assert out["preflight_test_sha256"] == (
        "19f301b07489e949888976363a3168497942b41cfa4c2a110a82db3b061fea5d"
    )


def test_review_accepts_exact_candidate_preflight_requirements():
    out = review.v2r13_pair09_candidate_host_preflight_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_candidate_host_preflight_reviewed"] is True
    assert out["read_only_host_collection_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["pair03_baseline_preservation_reviewed"] is True
    assert out["pair03_candidate_preservation_reviewed"] is True
    assert out["pair09_baseline_preservation_reviewed"] is True
    assert out["pair09_candidate_absence_reviewed"] is True
    assert out["held_out_pair15_absence_reviewed"] is True
    assert out["preserved_evidence_count"] == 12


def test_review_carries_no_execution_or_mutation_authority():
    out = review.v2r13_pair09_candidate_host_preflight_review_contract()
    for field in (
        "legacy_runtime_authority_inherited",
        "single_use_attempt_consumed",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "runtime_started",
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


def test_review_advances_only_to_restricted_git_backend():
    out = review.v2r13_pair09_candidate_host_preflight_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_GIT_BACKEND_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_GIT_BACKEND_IMPLEMENTATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateHostPreflightReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_candidate()
