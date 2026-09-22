from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_source_binding_review_generation2.py"
)


def test_review_pins_exact_preflight_source_and_tests():
    out = review.v2r13_pair09_baseline_host_preflight_review_contract()
    assert out["preflight_git_blob"] == "fc40d30be98db04fa783ab0534e8ab8eb869ce2d"
    assert out["preflight_source_sha256"] == (
        "a8d0a9ff633a88bde75bd166e8d750756344b2e52f769667246a6c8817675244"
    )
    assert out["preflight_test_git_blob"] == (
        "fc505322b7f05c3150442e9192189eadde6db1a3"
    )
    assert out["preflight_test_sha256"] == (
        "e06f3d21f574d83a41191cf8b282059ea57aadc189ebbefcbbbf0f24d43dc7be"
    )


def test_review_accepts_pair03_preservation_and_pair09_absence():
    out = review.v2r13_pair09_baseline_host_preflight_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_baseline_host_preflight_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["read_only_host_collection_reviewed"] is True
    assert out["pair03_baseline_preservation_reviewed"] is True
    assert out["pair03_candidate_preservation_reviewed"] is True
    assert out["pair09_baseline_absence_reviewed"] is True
    assert out["pair09_candidate_absence_reviewed"] is True
    assert out["held_out_pair15_absence_reviewed"] is True


def test_review_inherits_no_runtime_authority():
    out = review.v2r13_pair09_baseline_host_preflight_review_contract()
    assert out["legacy_structural_projection_is_host_observation"] is False
    assert out["legacy_runtime_authority_inherited"] is False
    assert out["single_use_attempt_consumed"] is False
    assert out["pair09_baseline_specific_authorization_accepted"] is False
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["pair09_baseline_execution_performed"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
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
    out = review.v2r13_pair09_baseline_host_preflight_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_v2r13_pair09_baseline_invocation_implementation"
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
        review.V2R13Pair09BaselineHostPreflightReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_baseline()
