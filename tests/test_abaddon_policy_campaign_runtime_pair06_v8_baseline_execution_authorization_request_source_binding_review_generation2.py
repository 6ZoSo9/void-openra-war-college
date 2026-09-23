from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_request_source_and_test():
    out = review.pair06_v8_baseline_execution_authorization_request_review_contract()
    assert out["request_git_blob"] == "7dff647cc9ffd7354b7fc9e16532ef51161d3d94"
    assert out["request_source_sha256"] == (
        "42496124e11e561bb4d0f34b3473a3f5948f3e1e9af33ecfb42afffa7e6b9e31"
    )
    assert out["request_test_git_blob"] == "595382831314c8e4a920fe1db569b6e897ba8dee"
    assert out["request_test_sha256"] == (
        "562bb8438887a2320a5822c777f2ac3389695f5d0fe8ae53f44623baf2c1979b"
    )


def test_review_confirms_exact_one_shot_scope():
    out = review.pair06_v8_baseline_execution_authorization_request_review_contract()
    assert out["pair06_v8_baseline_execution_authorization_request_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-v8-accepted-model-control"
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0


def test_review_remains_proposal_only_and_non_authorizing():
    out = review.pair06_v8_baseline_execution_authorization_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["pair06_baseline_specific_authorization_accepted"] is False
    assert out["pair06_baseline_execution_authorized"] is False
    assert out["pair06_baseline_execution_performed"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_preserves_external_boundaries():
    out = review.pair06_v8_baseline_execution_authorization_request_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_stops_at_explicit_authorization():
    out = review.pair06_v8_baseline_execution_authorization_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8BaselineExecutionAuthorizationRequestReviewHold,
        match="PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
