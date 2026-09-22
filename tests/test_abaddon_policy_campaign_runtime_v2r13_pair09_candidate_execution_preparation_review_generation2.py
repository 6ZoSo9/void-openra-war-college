from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_execution_preparation_review_generation2
    as review,
)


def test_preparation_pins_exact_baseline_and_runtime_sources():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
    assert out["baseline_result_review_git_blob"] == (
        "e0f663b144aa2036d7dba2a8d001f8f061f2f892"
    )
    assert out["baseline_result_review_source_sha256"] == (
        "acda9a94d229e73381aa45e6898f55b7eb066b67bb1bc29685276518026b9431"
    )
    assert out["command_materializer_git_blob"] == (
        "4836360e0d284454f815a2a2e32078d2565e6dea"
    )
    assert out["bounded_executor_git_blob"] == (
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
    )


def test_preparation_binds_completed_pair09_baseline():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
    assert out["candidate_execution_preparation_reviewed"] is True
    assert out["pair_slot"] == 9
    assert out["candidate_arm"] == "candidate"
    assert out["held_out"] is False
    assert out["baseline_evidence_bound_before_candidate_authorization"] is True
    assert out["baseline_attempt_exhausted"] is True
    assert out["baseline_valid_for_pairwise_comparison"] is True
    assert out["baseline_trajectory_sha256"] == (
        "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
    )
    assert out["baseline_summary_sha256"] == (
        "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
    )
    assert out["baseline_result_file_sha256"] == (
        "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
    )


def test_pair09_candidate_is_matched_to_baseline_controls():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
    assert out["matched_pair_seed"] == 1496195137
    assert out["matched_pair_round_limit"] == 36
    assert out["matched_pair_runtime_selection_key"] == (
        "apollyon-v2r13-qualified-predecessor"
    )
    assert tuple(out["baseline_command"]["runner_argv"]) == tuple(
        out["candidate_command"]["runner_argv"]
    )
    assert tuple(out["matched_pair_runner_argv"]) == tuple(
        out["candidate_command"]["runner_argv"]
    )
    assert (
        out["baseline_command"]["opponent_snapshot_sha256"]
        == out["candidate_command"]["opponent_snapshot_sha256"]
        == out["matched_pair_opponent_snapshot_sha256"]
    )
    assert (
        out["baseline_command"]["runtime_realization_sha256"]
        == out["candidate_command"]["runtime_realization_sha256"]
        == out["matched_pair_runtime_realization_sha256"]
    )


def test_candidate_policy_identities_are_exact():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
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


def test_candidate_command_remains_source_only():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
    command = out["candidate_command"]
    assert out["candidate_command_source_only"] is True
    assert command["pair_slot"] == 9
    assert command["arm"] == "candidate"
    assert command["runtime_execution_authorized"] is False
    assert command["runtime_started"] is False
    assert command["process_spawn_implemented"] is False
    assert command["command_execution_performed"] is False
    assert command["model_load_performed"] is False
    assert command["model_inference_performed"] is False
    assert command["game_execution_performed"] is False
    assert command["training_performed"] is False
    assert command["weights_updated"] is False


def test_preparation_grants_no_execution_or_followon_authority():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
    assert out["legacy_six_arm_authorization_sufficient"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is False
    assert out["another_baseline_execution_authorized"] is False
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


def test_preparation_advances_only_to_authorization_request():
    out = review.v2r13_pair09_candidate_execution_preparation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair09CandidateExecutionPreparationReviewHold,
        match="V2R13_PAIR09_CANDIDATE_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.authorize_or_execute_candidate()
