from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_authorization_source_binding_review_generation2
    as review,
)


def test_exact_authorization_identities_are_pinned():
    out = review.v2r13_pair03_baseline_additional_retry_authorization_review_contract()
    assert out["authorization_git_blob"] == (
        "231d234462a701a89be6cf8201f7fce738e929c5"
    )
    assert out["authorization_source_sha256"] == (
        "373988ef8981dadbbc83c5d0a5aeae4b137c110dd2699692067f979079a96c4a"
    )
    assert out["authorization_test_git_blob"] == (
        "19534bc00e64e67537d431c5b785657d77f0fb50"
    )
    assert out["authorization_test_sha256"] == (
        "b3ea36f3bc1e6807b778bed33f17cb9969dd9a8ae2f485b7a993661a0656f3ab"
    )


def test_review_authorizes_exactly_one_retry_index_two():
    out = review.v2r13_pair03_baseline_additional_retry_authorization_review_contract()
    assert out["authorization_source_binding_present"] is True
    assert out["authorization_reviewed"] is True
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["retry_index"] == 2
    assert out["single_additional_pair03_baseline_retry_authorized"] is True
    assert out["max_additional_retry_executions"] == 1
    assert out["total_retry_executions_authorized"] == 2
    assert out["additional_retry_execution_authorized_now"] is True
    assert out["additional_retry_execution_performed"] is False


def test_review_keeps_auto_retry_and_scope_closed():
    out = review.v2r13_pair03_baseline_additional_retry_authorization_review_contract()
    assert out["automatic_retry"] is False
    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_invocation_implementation():
    out = review.v2r13_pair03_baseline_additional_retry_authorization_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineAdditionalRetryAuthorizationReviewHold,
        match="V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED",
    ):
        review.execute_additional_retry()
