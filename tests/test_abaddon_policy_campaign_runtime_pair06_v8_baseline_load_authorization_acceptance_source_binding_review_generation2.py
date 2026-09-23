from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_acceptance_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_authorization_source_and_tests():
    out = review.pair06_v8_baseline_load_authorization_acceptance_review_contract()
    assert out["authorization_git_blob"] == (
        "ba76fec2e9bd2ba48000c9ed832c357f619d19bc"
    )
    assert out["authorization_source_sha256"] == (
        "ff6281e0491bc64d29999e8b6dbe9ebdd8ddad70ba44fb030a9b3734656c8452"
    )
    assert out["authorization_test_git_blob"] == (
        "2582a4acaef9f41fb2e418f3a25376ee9d2fb70e"
    )
    assert out["authorization_test_sha256"] == (
        "6491677e888087d509b3525ca166a697abbccd9556660f91bd2b110263541dac"
    )


def test_review_accepts_only_one_pair06_baseline_load_authority():
    out = review.pair06_v8_baseline_load_authorization_acceptance_review_contract()
    assert out["pair06_v8_baseline_load_authorization_acceptance_reviewed"] is True
    assert out["authorization_accepted"] is True
    assert out["authorization_scope"] == "single_pair06_baseline_v8_runtime_load"
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["runtime_load_authorized"] is True
    assert out["maximum_runtime_load_attempts"] == 1
    assert out["automatic_retry"] is False


def test_review_preserves_single_use_preload_safety_boundaries():
    out = review.pair06_v8_baseline_load_authorization_acceptance_review_contract()
    assert out["load_attempt_consumption_required"] is True
    assert out["create_only_load_attempt_marker_required"] is True
    assert out["runtime_load_invocation_implemented"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False


def test_review_does_not_expand_authority():
    out = review.pair06_v8_baseline_load_authorization_acceptance_review_contract()
    for field in (
        "candidate_runtime_load_authorized",
        "pair15_execution_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_is_repository_attestation_not_crypto_proof():
    out = review.pair06_v8_baseline_load_authorization_acceptance_review_contract()
    assert out["authorization_repository_attestation"] is True
    assert out["authorization_cryptographic_proof"] is False


def test_review_frontier_is_runtime_load_invocation_implementation():
    out = review.pair06_v8_baseline_load_authorization_acceptance_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED"
    )


def test_runtime_and_candidate_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8BaselineLoadAuthorizationAcceptanceReviewHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED",
    ):
        review.invoke_runtime_load()
    with pytest.raises(
        review.Pair06V8BaselineLoadAuthorizationAcceptanceReviewHold,
        match="PAIR06_V8_CANDIDATE_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        review.authorize_candidate_runtime_load()
