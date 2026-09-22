from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_invocation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_candidate_invocation_source_binding_review_generation2.py"
)


def test_review_pins_exact_invocation_cli_and_tests():
    out = review.v2r13_pair09_candidate_invocation_review_contract()
    assert out["invocation_git_blob"] == (
        "1c8a845a76569dd656cb11ad09593c24713a8ce2"
    )
    assert out["invocation_source_sha256"] == (
        "4858f3fe148829d050604746cd64fa426963370a71029f95d7cc40bb71b5ba7c"
    )
    assert out["invocation_test_git_blob"] == (
        "7717bf608b6c995ef9acc3f107bac6752c0ce43a"
    )
    assert out["invocation_test_sha256"] == (
        "9dac5c7e10e8feee66a2e1d6315cb5e7482c8892d579672173282edd094ef79b"
    )
    assert out["precision_cli_git_blob"] == (
        "6be5d1e346afeb699a6c8fe251c5b2c397315f6e"
    )
    assert out["precision_cli_source_sha256"] == (
        "221ff13d4872024dc2288a7d51f039133a66f8767336e2c9f6b83ca1f9801ff8"
    )
    assert out["precision_cli_test_git_blob"] == (
        "c74ba630cda19363abf2b627f371dfdc80b390da"
    )
    assert out["precision_cli_test_sha256"] == (
        "4db3385e61f57a4b316bb4f87ea08cb99d8093b8a4dc553962f6c3382c89981e"
    )


def test_review_accepts_exact_pair09_candidate_scope():
    out = review.v2r13_pair09_candidate_invocation_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_candidate_invocation_source_binding_present"] is True
    assert out["pair09_candidate_invocation_reviewed"] is True
    assert out["precision_cli_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["single_use_attempt"] is True
    assert out["automatic_retry"] is False


def test_precision_cli_requires_all_explicit_operator_inputs():
    out = review.v2r13_pair09_candidate_invocation_review_contract()
    assert out["precision_cli_requires_expected_main_head"] is True
    assert out["precision_cli_requires_explicit_authorization"] is True
    assert out["precision_cli_requires_explicit_confirmation"] is True
    assert out["precision_cli_pins_reviewed_invocation_source_sha256"] is True


def test_review_grants_no_runtime_or_followon_authority():
    out = review.v2r13_pair09_candidate_invocation_review_contract()
    for field in (
        "operator_authenticated",
        "pair09_candidate_specific_authorization_accepted",
        "single_use_attempt_consumed",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "pair09_baseline_rerun_authorized",
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


def test_review_stops_at_explicit_pair09_candidate_authorization():
    out = review.v2r13_pair09_candidate_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "trusted_operator_v2r13_pair09_candidate_execution_authorization"
    )


def test_authorize_or_execute_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateInvocationReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_candidate()
