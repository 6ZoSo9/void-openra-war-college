from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_invocation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_baseline_invocation_source_binding_review_generation2.py"
)


def test_review_pins_exact_invocation_cli_and_tests():
    out = review.v2r13_pair09_baseline_invocation_review_contract()
    assert out["invocation_git_blob"] == "9ae40fdb2976f3d6bb38e8bf6aaf4c884ae13292"
    assert out["invocation_source_sha256"] == (
        "1920cf9892f0962cd7b14b12db7848eda7d45552c3b43ef96ba2cb5b68c2cd4a"
    )
    assert out["invocation_test_git_blob"] == (
        "01bb7df18cacc09fb15ed88e2a773dd3c9fd4b40"
    )
    assert out["invocation_test_sha256"] == (
        "b56827c30561363f84d2a7725ef150a8f36e92ca65c30190f2f9d3e504105b55"
    )
    assert out["precision_cli_git_blob"] == (
        "7f44099744feafe1a8cf1d239c5280da63257795"
    )
    assert out["precision_cli_source_sha256"] == (
        "7b2c54ff17941cf905690a561f787c429e164d8d351800ddb09e69e7d1f04ecf"
    )
    assert out["precision_cli_test_git_blob"] == (
        "9d6a9ec187fa62e1b1e6c0701686fdb1a85efa70"
    )
    assert out["precision_cli_test_sha256"] == (
        "63b9eaa9acaa4599b651f47ea301adce4b7b3d2f17da80c61534712ab84e7aea"
    )


def test_review_accepts_exact_pair09_baseline_scope():
    out = review.v2r13_pair09_baseline_invocation_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_baseline_invocation_source_binding_present"] is True
    assert out["pair09_baseline_invocation_reviewed"] is True
    assert out["precision_cli_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["single_use_attempt"] is True
    assert out["automatic_retry"] is False


def test_precision_cli_requires_all_explicit_operator_inputs():
    out = review.v2r13_pair09_baseline_invocation_review_contract()
    assert out["precision_cli_requires_expected_main_head"] is True
    assert out["precision_cli_requires_explicit_authorization"] is True
    assert out["precision_cli_requires_explicit_confirmation"] is True
    assert out["precision_cli_pins_reviewed_invocation_source_sha256"] is True


def test_review_grants_no_runtime_or_followon_authority():
    out = review.v2r13_pair09_baseline_invocation_review_contract()
    assert out["operator_authenticated"] is False
    for field in (
        "pair09_baseline_specific_authorization_accepted",
        "single_use_attempt_consumed",
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
        "runtime_execution_invoked_by_review",
        "model_inference_invoked_by_review",
        "game_execution_invoked_by_review",
    ):
        assert out[field] is False


def test_review_stops_at_explicit_pair09_baseline_authorization():
    out = review.v2r13_pair09_baseline_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "trusted_operator_v2r13_pair09_baseline_execution_authorization"
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
        review.V2R13Pair09BaselineInvocationReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_baseline()
