from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_authorization_request_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_candidate_authorization_request_source_binding_review_generation2.py"
)


def test_review_pins_exact_request_source_and_tests():
    out = review.v2r13_pair09_candidate_authorization_request_review_contract()
    assert out["request_git_blob"] == "f58ca2f133e2366092c103c339f622d5198ed4c3"
    assert out["request_source_sha256"] == (
        "f612b365eae1b3df000c2beb790db9617efa4f20bca2e59694a01c9aedba724d"
    )
    assert out["request_test_git_blob"] == "fe8873a7557d14b68998a91a87f685a800201458"
    assert out["request_test_sha256"] == (
        "6c25f720eeb5f2c58ffd67a5b5772058fdba82c5fa5e1c8826b31b8f442911be"
    )


def test_review_accepts_only_exact_pair09_candidate_scope():
    out = review.v2r13_pair09_candidate_authorization_request_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_candidate_authorization_request_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["maximum_candidate_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["proposal_only_not_authorization"] is True
    assert out["baseline_rerun_included"] is False


def test_review_preserves_runtime_gate_set():
    out = review.v2r13_pair09_candidate_authorization_request_review_contract()
    assert out["required_runtime_gates"] == (
        "pair09_candidate_specific_operator_authorization_accepted",
        "exact_pair09_candidate_invocation_source_reviewed",
        "fresh_current_main_host_preflight",
        "cached_sudo_authority",
        "live_revocation_sentinel_absent",
        "isolated_grpc_python",
        "exact_model_preload_before_readiness_without_inference",
        "canonical_worktree_observation",
        "fresh_canonical_live_readiness_before_inference",
        "exact_pair09_baseline_result_reverified",
        "exact_pair03_preserved_evidence_reverified",
        "exact_candidate_policy_binding_reverified",
        "create_only_pair09_candidate_attempt_consumption",
    )


def test_review_confirms_request_bytes_do_not_grant_authority():
    out = review.v2r13_pair09_candidate_authorization_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["legacy_six_arm_authorization_sufficient"] is False


def test_review_carries_no_execution_or_followon_authority():
    out = review.v2r13_pair09_candidate_authorization_request_review_contract()
    for field in (
        "pair09_candidate_specific_authorization_accepted",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "pair09_candidate_invocation_implemented",
        "pair09_candidate_invocation_reviewed",
        "operator_authenticated",
        "source_inventory_verified",
        "baseline_evidence_bytes_verified",
        "runtime_readiness_verified",
        "authorization_consumption_implemented",
        "authorization_consumed",
        "pair09_baseline_rerun_authorized",
        "held_out_execution_authorized",
        "automatic_retry",
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


def test_review_stops_at_explicit_candidate_authorization():
    out = review.v2r13_pair09_candidate_authorization_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateAuthorizationRequestReviewHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_candidate()
