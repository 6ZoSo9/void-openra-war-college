from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_second_preservation_source_and_test():
    out = review.pair06_v8_second_failed_attempt_preservation_review_contract()
    assert out["preservation_git_blob"] == "653521100d1b88f84e16cb1a233b3a9da48fee17"
    assert out["preservation_source_sha256"] == (
        "888228244f81370f0f1199e2c5f9de7a6281da178f3e119bff93d2718adbcd4c"
    )
    assert out["preservation_test_git_blob"] == "5be94aa349219daebbf6f9d2bade37312930524f"
    assert out["preservation_test_sha256"] == (
        "8bcd5c5e6de6d872e85e35f32e6f6f65839ff1b0dcdc813509f4900a7937d437"
    )


def test_review_confirms_second_archive_and_prior_history_protection():
    out = review.pair06_v8_second_failed_attempt_preservation_review_contract()
    assert out["pair06_v8_second_failed_attempt_preservation_reviewed"] is True
    assert out["attempt_marker_sha256"] == (
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
    )
    assert out["archive_name"] == "baseline-20260923T235031Z-446d8f92"
    assert out["prior_failed_attempt_archive_revalidated_before_and_after"] is True


def test_review_grants_no_retry_or_execution_authority():
    out = review.pair06_v8_second_failed_attempt_preservation_review_contract()
    assert out["failed_attempt_deletion_authorized"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["runtime_execution_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_second_preservation_invocation():
    out = review.pair06_v8_second_failed_attempt_preservation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED"
    )


def test_retry_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8SecondFailedAttemptPreservationReviewHold,
        match="SECOND_FAILED_ATTEMPT_PRESERVATION_INVOCATION_REQUIRED",
    ):
        review.invoke_or_retry()
