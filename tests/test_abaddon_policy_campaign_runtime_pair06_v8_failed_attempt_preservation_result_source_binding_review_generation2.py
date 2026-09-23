from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_result_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_test():
    out = review.pair06_v8_failed_attempt_preservation_result_review_contract()
    assert out["acceptance_git_blob"] == "81de2f81579ce96669e3341d19ac242d556a4568"
    assert out["acceptance_source_sha256"] == (
        "cadfee2343a2ec8fb00cc7a01c954472dd2afe1f01eb6dc86030e3d58f6cb67f"
    )
    assert out["acceptance_test_git_blob"] == "989168e73534ddd2096f498bf0e7ae19e4351022"
    assert out["acceptance_test_sha256"] == (
        "7869b65afd1ff1ee2264364750bd01676e64f4ac8b223e983bfa5b9a5f0c3611"
    )


def test_review_confirms_green_archive_and_fresh_root_availability():
    out = review.pair06_v8_failed_attempt_preservation_result_review_contract()
    assert out["pair06_v8_failed_attempt_preservation_result_reviewed"] is True
    assert out["failed_attempt_archived"] is True
    assert out["failed_attempt_deleted"] is False
    assert out["fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt"] is True
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_preserves_all_execution_boundaries():
    out = review.pair06_v8_failed_attempt_preservation_result_review_contract()
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_new_repaired_request():
    out = review.pair06_v8_failed_attempt_preservation_result_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8FailedAttemptPreservationResultReviewHold,
        match="REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_or_execute()
