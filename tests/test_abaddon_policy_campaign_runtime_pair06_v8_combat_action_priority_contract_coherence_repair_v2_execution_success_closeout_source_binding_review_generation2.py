from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_merged_closeout_source_and_tests():
    out = review.pair06_v8_combat_priority_coherent_v2_success_review_contract()
    assert out["closeout_main_head"] == (
        "c28dbbfaa750da6405be7a2557ce32ae1ad4d810"
    )
    assert out["closeout_git_blob"] == (
        "6a12d64061cf449f40fb2e6fae4201ba6fff3d27"
    )
    assert out["closeout_source_sha256"] == (
        "a6026a7dff86b98e57572dddb0c6388aaeffd6ba3c3d612e8f1b3a4616ae1b2c"
    )
    assert out["closeout_test_git_blob"] == (
        "221cf2a24777c2d0ca8e58a8fbc5c64116c5cdf1"
    )
    assert out["closeout_test_sha256"] == (
        "488f55c0ebf5f2d5f8fc6007c28ba31f50744deefa43d73459d9211e7d4e4171"
    )


def test_review_pins_successful_runtime_artifacts():
    out = review.pair06_v8_combat_priority_coherent_v2_success_review_contract()

    assert out["attempt_marker_sha256"] == (
        "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207"
    )
    assert out["result_file_sha256"] == (
        "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4"
    )
    assert out["closeout_file_sha256"] == (
        "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1"
    )
    assert out["run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T183337Z-feinter-s208354846"
    )
    assert out["rounds_completed"] == 36
    assert out["final_tick"] == 3551
    assert out["outcome"] == "DRAW_OR_UNFINISHED"


def test_review_closes_attempt_and_authorization():
    out = review.pair06_v8_combat_priority_coherent_v2_success_review_contract()
    assert out["attempt_consumed"] is True
    assert out["attempt_reusable"] is False
    assert out["authorization_reusable"] is False
    assert out["automatic_retry"] is False
    assert out["lineage_closed"] is True
    assert out["new_execution_request_opened"] is False


def test_review_grants_no_follow_on_authority():
    out = review.pair06_v8_combat_priority_coherent_v2_success_review_contract()

    for field in (
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "retry_authorized",
        "replay_authorized",
        "training_authorized",
        "promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_closes_source_frontier():
    out = review.pair06_v8_combat_priority_coherent_v2_success_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == "PAIR06_V8_COHERENT_V2_SUCCESS_LINEAGE_CLOSED"
    assert out["next_change_class"] == "none"

    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentV2SuccessReviewHold,
        match="SUCCESS_LINEAGE_CLOSED",
    ):
        review.execute_or_reopen()
