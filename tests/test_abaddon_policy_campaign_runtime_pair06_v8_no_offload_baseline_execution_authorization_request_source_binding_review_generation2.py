from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_baseline_execution_authorization_request_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_no_offload_request_source_test_and_bytes():
    out = review.pair06_v8_no_offload_baseline_execution_authorization_request_review_contract()
    assert out["request_git_blob"] == "7ed5b11d66518a2eecd3d4a28f680b111ee5d624"
    assert out["request_source_sha256"] == (
        "55c197d0622572eced045dca8b1c86a11a4bf2a74beed7f4e3e2bed3c3449ed7"
    )
    assert out["request_test_git_blob"] == "9f2f37f2ef0fd9ac3885daf063fd50894893cbca"
    assert out["request_test_sha256"] == (
        "7783ebbbd597d644f7855c3f0ec3b429413009ec82b01354bd8b6974db22c2ae"
    )
    assert out["request_bytes_sha256"] == (
        "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
    )
    assert out["request_byte_length"] == 4118
    assert out["request_sha256"] == out["request_bytes_sha256"]


def test_review_confirms_fresh_no_offload_one_shot_only():
    out = review.pair06_v8_no_offload_baseline_execution_authorization_request_review_contract()
    assert out["pair06_v8_no_offload_baseline_execution_authorization_request_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["both_failed_attempts_archived"] is True
    assert out["first_spent_attempt_reusable"] is False
    assert out["second_spent_attempt_reusable"] is False
    assert out["no_offload_parent_generation_required"] is True
    assert out["single_gpu_cuda0_placement_required"] is True
    assert out["cpu_disk_meta_parameter_offload_allowed"] is False


def test_review_remains_proposal_only_and_non_authorizing():
    out = review.pair06_v8_no_offload_baseline_execution_authorization_request_review_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["pair06_no_offload_baseline_specific_authorization_accepted"] is False
    assert out["pair06_no_offload_baseline_execution_authorized"] is False
    assert out["pair06_no_offload_baseline_execution_performed"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_stops_at_explicit_no_offload_authorization():
    out = review.pair06_v8_no_offload_baseline_execution_authorization_request_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8NoOffloadBaselineExecutionAuthorizationRequestReviewHold,
        match="NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
