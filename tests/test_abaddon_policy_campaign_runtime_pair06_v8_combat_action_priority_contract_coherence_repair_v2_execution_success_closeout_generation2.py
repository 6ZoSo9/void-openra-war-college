from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_generation2
    as closeout,
)


def test_closeout_pins_successful_v2_execution_identity():
    out = closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()

    assert out["authorized_main_head"] == (
        "d8b16f1c23a74803ac4ace94045fed147c3c69fe"
    )
    assert out["acceptance_merge"] == (
        "1dfbed07a95b2a5cf60eed8af49e8a3355810f17"
    )
    assert out["authorized_request_sha256"] == (
        "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
    )
    assert out["authorization_text_sha256"] == (
        "6cfe4dd78c02a55c2499163b01de6f5714e0b8573100b7a888177ff1a568d139"
    )
    assert out["invocation_source_sha256"] == (
        "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
    )

    assert out["attempt_marker_sha256"] == (
        "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207"
    )
    assert out["result_file_sha256"] == (
        "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4"
    )
    assert out["closeout_file_sha256"] == (
        "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1"
    )


def test_closeout_pins_completed_game_evidence():
    out = closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()

    assert out["run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T183337Z-feinter-s208354846"
    )
    assert out["trajectory_sha256"] == (
        "afc57351991c90dc21e4d2316ddd23fce8b01b9132a3435a9252de7227001ddc"
    )
    assert out["summary_sha256"] == (
        "a5d72287487849164e727836eee82dd5821ddb46f5803b995b1d67cc289075ab"
    )
    assert out["warm_start_sha256"] == (
        "f36f2717d34e028d02d1b7076d7de1cff65dce1ffed59710110f2adbf4ad700d"
    )
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["outcome"] == "DRAW_OR_UNFINISHED"
    assert out["model_inference_count"] == 36


def test_closeout_marks_attempt_and_authorization_spent():
    out = closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()

    assert out["attempt_consumed"] is True
    assert out["attempt_reusable"] is False
    assert out["authorization_reusable"] is False
    assert out["automatic_retry"] is False
    assert out["prior_consumed_marker_reusable"] is False
    assert out["prior_failed_run_reusable_as_authority"] is False


def test_closeout_preserves_safety_boundary():
    out = closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()

    assert out["game_execution_performed"] is True
    assert out["contract_coherence_repair_v2_used"] is True
    assert out["combat_priority_policy_activation_performed"] is True
    assert out["post_run_frozen_worktrees_green"] is True
    assert out["engine_container_removed"] is True
    assert out["session_destroyed"] is True

    for field in (
        "candidate_execution_performed",
        "held_out_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "runtime_execution_authorized_by_this_record",
        "retry_authorized_by_this_record",
        "replay_authorized_by_this_record",
        "training_authorized_by_this_record",
        "promotion_authorized_by_this_record",
        "deployment_authorized_by_this_record",
        "void_chain_mutation_authorized_by_this_record",
        "wallet_or_funds_action_authorized_by_this_record",
    ):
        assert out[field] is False


def test_closeout_is_source_only_and_requires_review():
    out = closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()
    assert out["runtime_output_observed"] is True
    assert out["repo_side_local_artifact_rehash_performed"] is False
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == "PAIR06_V8_COHERENT_V2_SUCCESS_REVIEW_REQUIRED"

    with pytest.raises(RuntimeError, match="SUCCESS_REVIEW_REQUIRED"):
        closeout.review_or_execute()
