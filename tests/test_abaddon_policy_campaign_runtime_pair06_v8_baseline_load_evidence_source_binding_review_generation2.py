from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_evidence_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_tests():
    out = review.pair06_v8_baseline_load_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == (
        "d99e829b0cab74d03c7964b1b43cca19c7623f3a"
    )
    assert out["acceptance_source_sha256"] == (
        "25b9cb96b0f153f31748fde9f5e93df33454d6c8738e36ad7be84f7d394cfbbd"
    )
    assert out["acceptance_test_git_blob"] == (
        "5eb293962affb23ba5e4ab06513ba4a065409b17"
    )
    assert out["acceptance_test_sha256"] == (
        "c127fb543beada2f68ee71ec062d387e1e5823019797298036e55dd8f7367be4"
    )


def test_review_confirms_exact_consumed_baseline_load():
    out = review.pair06_v8_baseline_load_evidence_review_contract()
    assert out["pair06_v8_baseline_load_evidence_source_binding_present"] is True
    assert out["pair06_v8_baseline_load_evidence_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["attempt_consumed"] is True
    assert out["maximum_attempts"] == 1
    assert out["runtime_load_performed"] is True
    assert out["model_weights_loaded"] is True
    assert out["persistent_runtime_handle_exported"] is False
    assert out["runtime_residency_after_launcher_attested"] is False
    assert out["automatic_retry"] is False


def test_review_confirms_exact_runtime_environment_and_assets():
    out = review.pair06_v8_baseline_load_evidence_review_contract()
    assert out["runtime_environment_verified"] is True
    assert out["runtime_assets_verified"] is True
    assert out["verified_asset_count"] == 17


def test_review_preserves_inference_game_candidate_and_heldout_boundaries():
    out = review.pair06_v8_baseline_load_evidence_review_contract()
    for field in (
        "another_baseline_load_authorized",
        "candidate_runtime_load_authorized",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
        "game_execution_performed",
        "pair15_execution_authorized",
        "pair15_execution_performed",
    ):
        assert out[field] is False


def test_review_preserves_training_deployment_chain_and_funds_boundaries():
    out = review.pair06_v8_baseline_load_evidence_review_contract()
    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_review_advances_only_to_runtime_lifetime_handoff_design():
    out = review.pair06_v8_baseline_load_evidence_review_contract()
    assert out["runtime_lifetime_handoff_design_required"] is True
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v8_baseline_runtime_lifetime_handoff_design"
    )


def test_follow_on_execution_holds_until_runtime_lifetime_handoff_design():
    with pytest.raises(
        review.Pair06V8BaselineLoadEvidenceReviewHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_REQUIRED",
    ):
        review.authorize_game_execution()
