from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_preparation_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_candidate_execution_preparation_review_generation2.py"
)


def test_exact_source_dependencies_are_pinned():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    assert out["baseline_result_review_git_blob"] == (
        "877c9dd0969b1b2220f5d886da7521aa756a9742"
    )
    assert out["bounded_executor_git_blob"] == (
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
    )
    assert out["first_baseline_invocation_git_blob"] == (
        "5b790efaf4085deb15eaef538635fd11f5cad9a5"
    )


def test_candidate_policy_identities_are_exact():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    assert out["candidate_wrapper_git_blob"] == (
        "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
    )
    assert out["candidate_wrapper_sha256"] == (
        "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
    )
    assert out["candidate_fixture_git_blob"] == (
        "20091bff54edbb567127722fae81e5a5308737d2"
    )
    assert out["candidate_fixture_sha256"] == (
        "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
    )
    assert out["candidate_genome_sha256"] == (
        "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
    )
    assert out["abaddon_controller_sha256"] == (
        "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
    )
    assert out["abaddon_refiner_sha256"] == (
        "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
    )


def test_successful_baseline_is_bound_before_candidate_authorization():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    assert out["baseline_evidence_bound_before_candidate_authorization"] is True
    assert out["baseline_trajectory_sha256"] == (
        "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
    )
    assert out["baseline_summary_sha256"] == (
        "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
    )


def test_candidate_command_is_source_only_and_unexecuted():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    command = out["candidate_command"]
    assert out["candidate_command_materialization_source_only"] is True
    assert command["pair_slot"] == 3
    assert command["arm"] == "candidate"
    assert command["runtime_execution_authorized"] is False
    assert command["runtime_started"] is False
    assert command["process_spawn_implemented"] is False
    assert command["command_execution_performed"] is False
    assert command["model_inference_performed"] is False
    assert command["game_execution_performed"] is False
    assert command["training_performed"] is False


def test_repaired_baseline_runtime_safety_must_be_inherited():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    for field in (
        "repaired_readiness_path_must_be_inherited",
        "fresh_current_main_preflight_required",
        "cached_sudo_required",
        "revocation_sentinel_absent_required",
        "isolated_grpc_python_required",
        "exact_model_preload_before_readiness_required",
        "preload_must_not_perform_inference",
        "canonical_worktree_observation_required",
        "fresh_canonical_live_readiness_required",
        "baseline_trajectory_binding_required_for_candidate_receipt",
        "baseline_summary_binding_required_for_candidate_receipt",
    ):
        assert out[field] is True


def test_historical_executor_capability_is_not_candidate_specific_authority():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    assert out["bounded_executor_candidate_capability_reusable"] is True
    assert out["legacy_v2r13_authorization_sufficient_for_pair03_candidate"] is False
    assert out["candidate_specific_authorization_accepted"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is False
    assert out["candidate_invocation_implemented"] is False
    assert out["candidate_invocation_reviewed"] is False


def test_preparation_does_not_expand_follow_on_authority():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    assert out["automatic_retry"] is False
    for field in (
        "held_out_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_source_has_no_direct_host_action_imports():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "asyncio",
        "ctypes",
        "http",
        "httpx",
        "multiprocessing",
        "os",
        "pathlib",
        "requests",
        "shutil",
        "socket",
        "subprocess",
        "urllib",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden


def test_frontier_remains_candidate_authorization_required():
    out = review.v2r13_pair03_candidate_execution_preparation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03CandidateExecutionPreparationReviewHold,
        match="V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_candidate()
