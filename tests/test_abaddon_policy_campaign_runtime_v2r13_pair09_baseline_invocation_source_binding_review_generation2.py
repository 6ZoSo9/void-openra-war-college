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
    assert out["invocation_git_blob"] == "312215c5b82296f15200544a61cc500d908ff9cf"
    assert out["invocation_source_sha256"] == (
        "815d824bfa7aabc2659ff1fd2e4407c81dff7d5101103ac6868e6c1dfa5b768b"
    )
    assert out["invocation_test_git_blob"] == (
        "eea23bdc6a453689d3f77de160761aaf453a5639"
    )
    assert out["invocation_test_sha256"] == (
        "c347ceb4584cd6bfbfe1f517d772097cb3b70f226bf680670c04e2f26147b4cc"
    )
    assert out["precision_cli_git_blob"] == (
        "c9e26cffd595e5dde8b4e166ee25abcf43496345"
    )
    assert out["precision_cli_source_sha256"] == (
        "0b24777dcbe290375323bb852754fe873fc65e4d32004ddad0f986e00df8607f"
    )
    assert out["precision_cli_test_git_blob"] == (
        "8a31d97fc828d5322840ba61446c8a03415acdbc"
    )
    assert out["precision_cli_test_sha256"] == (
        "9173453692f017682813c8195454b6abd6dc99356821e7ceef37e641c6126e33"
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
