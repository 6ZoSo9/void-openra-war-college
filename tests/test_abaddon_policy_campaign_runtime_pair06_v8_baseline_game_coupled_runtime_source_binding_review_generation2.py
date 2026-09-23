from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_game_coupled_runtime_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_runtime_core_and_tests():
    out = review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    assert out["runtime_core_git_blob"] == "032966cc0e41a1841eee4637b4c9d798de16a562"
    assert out["runtime_core_source_sha256"] == (
        "2aa75242b04dbf533ab6fa100524209844cd9f7c029f6b3a736867c4d6a842d6"
    )
    assert out["runtime_core_test_git_blob"] == "2337b3848d4bb294d409e5132159b4248ab3ccc0"
    assert out["runtime_core_test_sha256"] == (
        "9179039fcc75cbc5125ce413271465b16cdab3c09cb35f1aa9724d1190e5f85a"
    )


def test_review_confirms_exact_pair06_baseline_core():
    out = review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    assert out["pair06_v8_baseline_game_coupled_runtime_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-v8-accepted-model-control"


def test_review_confirms_same_process_load_game_and_authority_checks():
    out = review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    assert out["same_process_load_and_game_implemented"] is True
    assert out["authority_check_before_load_implemented"] is True
    assert out["authority_check_before_each_inference_implemented"] is True
    assert out["fresh_environment_verification_delegated_to_reviewed_loader"] is True
    assert out["exact_asset_verification_delegated_to_reviewed_loader"] is True
    assert out["model_reference_release_in_finally_implemented"] is True


def test_review_keeps_adapter_claim_invocation_as_separate_gates():
    out = review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    assert out["game_runner_adapter_required"] is True
    assert out["game_runner_adapter_implemented"] is False
    assert out["durable_game_attempt_claim_implemented"] is False
    assert out["operator_invocation_implemented"] is False


def test_review_grants_no_execution_authority():
    out = review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    for field in (
        "game_coupled_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "runtime_execution_performed",
        "model_inference_performed",
        "game_execution_performed",
        "candidate_runtime_load_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_review_advances_only_to_apollyon_decision_adapter():
    out = review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v8_baseline_apollyon_decision_adapter_implementation"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8BaselineGameCoupledRuntimeReviewHold,
        match="PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_IMPLEMENTATION_REQUIRED",
    ):
        review.execute_game()
