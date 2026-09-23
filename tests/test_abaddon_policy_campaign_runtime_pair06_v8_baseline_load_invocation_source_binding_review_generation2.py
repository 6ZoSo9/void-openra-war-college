from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_invocation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_invocation_source_and_tests():
    out = review.pair06_v8_baseline_load_invocation_review_contract()
    assert out["invocation_git_blob"] == (
        "fde5a7c1c0f9ccb5823e9d86af84074218587df7"
    )
    assert out["invocation_source_sha256"] == (
        "864e830cf2d62d3776321b75665f07b58f0b548d6a3dc114b0b9cd84eb9a2ea4"
    )
    assert out["invocation_test_git_blob"] == (
        "69abde74130d557b4071d006381f962eb3b751aa"
    )
    assert out["invocation_test_sha256"] == (
        "62d3d6408cf630865626d60c1c8e232c9a420b3d570a03622b333109b85a3ff4"
    )


def test_review_confirms_exact_single_baseline_load_scope():
    out = review.pair06_v8_baseline_load_invocation_review_contract()
    assert out["pair06_v8_baseline_load_invocation_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["runtime_load_authorized_by_reviewed_dependency"] is True
    assert out["single_use_attempt_consumption_required"] is True
    assert out["single_use_attempt_consumed"] is False
    assert out["automatic_retry"] is False


def test_review_confirms_all_operational_guards_remain_required():
    out = review.pair06_v8_baseline_load_invocation_review_contract()
    for field in (
        "explicit_authorization_boolean_required",
        "explicit_confirmation_token_required",
        "exact_current_main_required",
        "exact_invocation_source_sha256_required",
        "designated_python_required",
        "fresh_runtime_environment_verification_required",
        "runtime_asset_hash_verification_required",
        "offline_only_model_load_required",
        "revocation_check_required_before_claim",
        "revocation_check_required_after_claim",
    ):
        assert out[field] is True


def test_review_contract_inspection_performs_no_load_or_execution():
    out = review.pair06_v8_baseline_load_invocation_review_contract()
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False


def test_review_does_not_expand_candidate_heldout_or_mutating_authority():
    out = review.pair06_v8_baseline_load_invocation_review_contract()
    for field in (
        "candidate_runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_precision_runtime_load_execution():
    out = review.pair06_v8_baseline_load_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_PRECISION_EXECUTION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_PRECISION_EXECUTION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "trusted_operator_pair06_v8_baseline_runtime_load_precision_execution"
    )


def test_review_runtime_and_game_entrypoints_hold():
    with pytest.raises(
        review.Pair06V8BaselineLoadInvocationReviewHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_PRECISION_EXECUTION_REQUIRED",
    ):
        review.execute_runtime_load()
    with pytest.raises(
        review.Pair06V8BaselineLoadInvocationReviewHold,
        match="PAIR06_V8_GAME_EXECUTION_NOT_AUTHORIZED",
    ):
        review.execute_game()
