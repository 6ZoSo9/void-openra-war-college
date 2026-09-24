from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_result_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_second_preservation_acceptance_source_and_test():
    out = review.pair06_v8_second_preservation_result_review_contract()
    assert out["acceptance_git_blob"] == "462d0524324cbe8c69914d004acf03cec54de2e9"
    assert out["acceptance_source_sha256"] == (
        "8bc1249e6cb069d162745d8956fbc28bc68bf087ef1ef7c3cf108d34b5050269"
    )
    assert out["acceptance_test_git_blob"] == "0d5f2f7f8b7156242d29193ddd755eb593da3933"
    assert out["acceptance_test_sha256"] == (
        "a3673208b5e17036e4d035d69c8a60ead6b03c30dda61f8b4dd7c0305dd0f2db"
    )


def test_review_confirms_both_failed_attempts_preserved_and_fresh_root_available():
    out = review.pair06_v8_second_preservation_result_review_contract()
    assert out["pair06_v8_second_preservation_result_reviewed"] is True
    assert out["second_failed_attempt_archived"] is True
    assert out["second_failed_attempt_deleted"] is False
    assert out["prior_failed_attempt_archive_unchanged"] is True
    assert out["fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt"] is True
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_advances_only_to_no_offload_invocation():
    out = review.pair06_v8_second_preservation_result_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8SecondPreservationResultReviewHold,
        match="NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED",
    ):
        review.request_or_execute()
