from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_lifetime_handoff_design_generation2
    as design,
)


def test_design_binds_exact_pair06_baseline_allocation():
    out = design.pair06_v8_baseline_lifetime_handoff_design_contract()
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-v8-accepted-model-control"


def test_design_records_validation_load_as_consumed_and_nonreusable():
    out = design.pair06_v8_baseline_lifetime_handoff_design_contract()
    assert out["validation_load_completed"] is True
    assert out["validation_load_attempt_consumed"] is True
    assert out["validation_load_reusable_for_game"] is False
    assert out["cross_process_runtime_reuse_permitted"] is False
    assert out["persistent_runtime_handle_exported"] is False
    assert out["runtime_residency_after_launcher_attested"] is False


def test_design_requires_atomic_same_process_game_lifecycle():
    out = design.pair06_v8_baseline_lifetime_handoff_design_contract()
    assert out["game_coupled_runtime_lifecycle_required"] is True
    assert out["same_process_load_and_game_required"] is True
    assert out["fresh_environment_verification_required"] is True
    assert out["exact_17_asset_verification_required"] is True
    assert out["create_only_game_attempt_claim_required"] is True
    assert out["new_game_coupled_load_authorization_required"] is True
    assert out["new_game_execution_authorization_required"] is True
    assert out["single_authorization_must_cover_load_and_game"] is True
    assert out["atomic_lifecycle"] == (
        "fresh_runtime_environment_verification",
        "exact_17_asset_verification",
        "create_only_game_attempt_claim",
        "exact_v8_runtime_load",
        "pair06_baseline_game_start",
        "model_inference_within_authorized_game_only",
        "runtime_and_game_cleanup",
        "durable_game_result_publication",
    )


def test_design_grants_no_runtime_or_game_authority():
    out = design.pair06_v8_baseline_lifetime_handoff_design_contract()
    for field in (
        "another_validation_load_authorized",
        "game_coupled_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "runtime_execution_performed",
        "model_inference_performed",
        "game_execution_performed",
        "candidate_runtime_load_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_design_advances_only_to_separate_source_binding_review():
    out = design.pair06_v8_baseline_lifetime_handoff_design_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        design.Pair06V8BaselineLifetimeHandoffDesignHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        design.execute_or_load()
