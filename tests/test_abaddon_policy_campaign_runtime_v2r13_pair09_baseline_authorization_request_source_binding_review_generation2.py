from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_source_binding_review_generation2.py"
)


def test_review_pins_exact_request_source_and_tests():
    out = review.v2r13_pair09_baseline_authorization_request_review_contract()
    assert out["request_git_blob"] == "8d49f5fbc73c574884e1e262eb929395551b6419"
    assert out["request_source_sha256"] == (
        "cc0d6f16227528ddee9e65903b10c579180ffbdae6567a229919400f6476daa0"
    )
    assert out["request_test_git_blob"] == "3983bd11da5f3428d87461962c7d4ba194e7e22b"
    assert out["request_test_sha256"] == (
        "73d96d6714ebe706054cd7cb3befc9466028f14500409e54edb0db2f92c3c5c1"
    )


def test_review_accepts_only_exact_pair09_baseline_proposal_scope():
    out = review.v2r13_pair09_baseline_authorization_request_review_contract()
    assert out["separate_review_instrument"] is True
    assert out["pair09_baseline_authorization_request_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_baseline_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["proposal_only_not_authorization"] is True


def test_review_confirms_request_bytes_and_history_do_not_grant_authority():
    out = review.v2r13_pair09_baseline_authorization_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["historical_pair03_runtime_authority_sufficient"] is False
    assert out["legacy_six_arm_authorization_sufficient"] is False


def test_review_preserves_all_runtime_gates():
    out = review.v2r13_pair09_baseline_authorization_request_review_contract()
    assert out["required_runtime_gates"] == (
        "pair09_baseline_specific_operator_authorization_accepted",
        "exact_pair09_baseline_invocation_source_reviewed",
        "fresh_current_main_host_preflight",
        "cached_sudo_authority",
        "live_revocation_sentinel_absent",
        "isolated_grpc_python",
        "exact_model_preload_before_readiness_without_inference",
        "canonical_worktree_observation",
        "fresh_canonical_live_readiness_before_inference",
        "create_only_pair09_baseline_attempt_consumption",
    )


def test_review_carries_no_execution_or_followon_authority():
    out = review.v2r13_pair09_baseline_authorization_request_review_contract()
    for field in (
        "pair09_baseline_specific_authorization_accepted",
        "pair09_baseline_execution_authorized",
        "pair09_baseline_execution_performed",
        "pair09_candidate_execution_authorized",
        "held_out_execution_authorized",
        "operator_authenticated",
        "source_inventory_verified",
        "runtime_readiness_verified",
        "authorization_consumption_implemented",
        "authorization_consumed",
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


def test_review_stops_at_explicit_pair09_baseline_authorization():
    out = review.v2r13_pair09_baseline_authorization_request_review_contract()
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


def test_authorize_or_execute_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09BaselineAuthorizationRequestReviewHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_pair09_baseline()
