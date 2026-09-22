from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_attempt_guard_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_candidate_attempt_guard_source_binding_review_generation2.py"
)


def test_review_pins_exact_guard_source_and_tests():
    out = review.v2r13_pair09_candidate_attempt_guard_review_contract()
    assert out["guard_git_blob"] == "0540e4472af8b7da11e16b118b3bd373e7e9b92c"
    assert out["guard_source_sha256"] == (
        "aa025315c94dd2c25a9faa6cdb5d44e1f1314dc2b67c42e781801cd6695f7982"
    )
    assert out["guard_test_git_blob"] == "9113245d666657e2a3cbf19f6598011c0b9a2696"
    assert out["guard_test_sha256"] == (
        "420618367caeadd1080997912bd77983f0cb1eb1450917610cec6e6afd399de8"
    )


def test_review_accepts_only_single_use_candidate_guard():
    out = review.v2r13_pair09_candidate_attempt_guard_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_candidate_attempt_guard_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["single_use_attempt_consumption_reviewed"] is True
    assert out["create_only_marker_reviewed"] is True
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["marker_is_execution_authority"] is False
    assert out["reset_api_present"] is False
    assert out["delete_api_present"] is False
    assert out["resume_api_present"] is False


def test_review_carries_no_candidate_or_followon_authority():
    out = review.v2r13_pair09_candidate_attempt_guard_review_contract()
    for field in (
        "pair09_candidate_specific_authorization_accepted",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "held_out_execution_authorized",
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


def test_review_advances_only_to_candidate_host_preflight():
    out = review.v2r13_pair09_candidate_attempt_guard_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_HOST_PREFLIGHT_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_HOST_PREFLIGHT_IMPLEMENTATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateAttemptGuardReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_candidate()
