from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_no_offload_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_no_offload_invocation_source_and_test():
    out = review.pair06_v8_baseline_attempt_invocation_no_offload_review_contract()
    assert out["invocation_git_blob"] == "2d5528c73770b8a60770486c70d1aa64c6c67ee8"
    assert out["invocation_source_sha256"] == (
        "d8d1598ea2c016a6b27fb2e109e1a6eb2fca3f0535687ab48db47e2fb742ea91"
    )
    assert out["invocation_test_git_blob"] == "b8539b8bb358525580cc9fae4f9e88f63e9892ee"
    assert out["invocation_test_sha256"] == (
        "e1e539a5816b8ea632d89f8cebc38138bba84887c8bf2aec0fb0ee6f959b66e2"
    )


def test_review_confirms_new_no_offload_one_shot_only():
    out = review.pair06_v8_baseline_attempt_invocation_no_offload_review_contract()
    assert out["pair06_v8_baseline_attempt_invocation_no_offload_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["no_offload_parent_generation_required"] is True
    assert out["second_preservation_result_review_required"] is True
    assert out["no_offload_parent_receipt_schema_required"] is True
    assert out["inference_safe_placement_receipt_required"] is True
    assert out["attempt_marker_create_only"] is True
    assert out["postclaim_reset_or_resume_available"] is False


def test_review_remains_non_authorizing():
    out = review.pair06_v8_baseline_attempt_invocation_no_offload_review_contract()
    assert out["explicit_authorization_required"] is True
    assert out["pair06_baseline_specific_authorization_accepted"] is False
    assert out["runtime_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_advances_only_to_fresh_no_offload_request():
    out = review.pair06_v8_baseline_attempt_invocation_no_offload_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8BaselineInvocationNoOffloadReviewHold,
        match="NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.execute_or_authorize()
