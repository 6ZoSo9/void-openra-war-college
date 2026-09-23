from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_repaired_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_repaired_request_source_and_test():
    out = review.pair06_v8_repaired_baseline_execution_authorization_request_review_contract()
    assert out["request_git_blob"] == "9cb4b07ae31142005ddc202e02b6fbf397fcb9a5"
    assert out["request_source_sha256"] == (
        "3a9548eda5a25cdab6183c265a4492aa0d18a39ce39013b0016210c5a83916b3"
    )
    assert out["request_test_git_blob"] == "36b7f78c0edc6a5c02da025532a08813c0057096"
    assert out["request_test_sha256"] == (
        "9be522fe7a687bc9d65094d3657557e5de15f62c722824cd79299a5fe55c52db"
    )


def test_review_confirms_fresh_repaired_one_shot_only():
    out = review.pair06_v8_repaired_baseline_execution_authorization_request_review_contract()
    assert out["pair06_v8_repaired_baseline_execution_authorization_request_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["spent_request_reusable"] is False
    assert out["spent_attempt_reusable"] is False
    assert out["offload_safe_generate_binding_required"] is True


def test_review_remains_proposal_only_and_non_authorizing():
    out = review.pair06_v8_repaired_baseline_execution_authorization_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["pair06_repaired_baseline_specific_authorization_accepted"] is False
    assert out["pair06_repaired_baseline_execution_authorized"] is False
    assert out["pair06_repaired_baseline_execution_performed"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_preserves_external_boundaries():
    out = review.pair06_v8_repaired_baseline_execution_authorization_request_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_stops_at_explicit_repaired_authorization():
    out = review.pair06_v8_repaired_baseline_execution_authorization_request_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8RepairedBaselineExecutionAuthorizationRequestReviewHold,
        match="REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
