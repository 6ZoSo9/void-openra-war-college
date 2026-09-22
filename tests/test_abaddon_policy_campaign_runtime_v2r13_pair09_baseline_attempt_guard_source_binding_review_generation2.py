from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_source_binding_review_generation2.py"
)


def test_review_pins_exact_guard_and_request_review_sources():
    out = review.v2r13_pair09_baseline_attempt_guard_review_contract()
    assert out["guard_git_blob"] == "4f3a470247196dde8fd7b7ad4807f1025adfb9b8"
    assert out["guard_source_sha256"] == (
        "9e2c65cca456549efd6904d5a8b8745364398b52dcd5836ecc62fa52f43c3ef9"
    )
    assert out["guard_test_git_blob"] == "399175c091e4671e2a2ea435149cb0321c8df164"
    assert out["guard_test_sha256"] == (
        "efa53c929f58635e520026095b5696d3497fbd86654d6cf9019dc854d87bed7e"
    )
    assert out["request_review_git_blob"] == (
        "8342290da226a053e56a328885bd80bb5a77587f"
    )
    assert out["request_review_source_sha256"] == (
        "50c4acaf6bdf1bbba063cf4670caaa8f23118fccfabbf917243b2cd71d2253a7"
    )


def test_review_accepts_create_only_single_use_guard():
    out = review.v2r13_pair09_baseline_attempt_guard_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_baseline_attempt_guard_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["single_use_attempt_consumption_reviewed"] is True
    assert out["create_only_marker_reviewed"] is True
    assert out["existing_or_uncertain_marker_holds"] is True


def test_marker_is_neither_authority_nor_execution_evidence():
    out = review.v2r13_pair09_baseline_attempt_guard_review_contract()
    assert out["marker_is_execution_authority"] is False
    assert out["marker_is_execution_evidence"] is False
    assert out["marker_deletion_api_implemented"] is False
    assert out["reset_api_implemented"] is False
    assert out["resume_api_implemented"] is False
    assert out["automatic_retry"] is False


def test_review_keeps_all_execution_and_followon_authority_closed():
    out = review.v2r13_pair09_baseline_attempt_guard_review_contract()
    for field in (
        "pair09_baseline_specific_authorization_accepted",
        "pair09_baseline_execution_authorized",
        "pair09_baseline_execution_performed",
        "pair09_candidate_execution_authorized",
        "held_out_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_invocation_implementation():
    out = review.v2r13_pair09_baseline_attempt_guard_review_contract()
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
        review.V2R13Pair09BaselineAttemptGuardReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_baseline()
