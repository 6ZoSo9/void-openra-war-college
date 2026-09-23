from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_lifetime_handoff_design_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_design_source_and_tests():
    out = review.pair06_v8_baseline_lifetime_handoff_design_review_contract()
    assert out["design_git_blob"] == "479206e01dea661cce45922a776b258c142a82c1"
    assert out["design_source_sha256"] == (
        "4df1bbcbd243ba9ddbcf21cf730aa315b006f82a8b62b183f319eaa02f1dc459"
    )
    assert out["design_test_git_blob"] == "b8a3cef2834efa5d89850505be4f509588c10ede"
    assert out["design_test_sha256"] == (
        "922f468f2fa6e3ec88beefdb848ed1640763e28a9a746a1dba9ee93f5bd1e00c"
    )


def test_review_confirms_nonpersistent_validation_load():
    out = review.pair06_v8_baseline_lifetime_handoff_design_review_contract()
    assert out["pair06_v8_baseline_lifetime_handoff_design_reviewed"] is True
    assert out["validation_load_completed"] is True
    assert out["validation_load_attempt_consumed"] is True
    assert out["validation_load_reusable_for_game"] is False
    assert out["cross_process_runtime_reuse_permitted"] is False
    assert out["persistent_runtime_handle_exported"] is False
    assert out["runtime_residency_after_launcher_attested"] is False


def test_review_requires_atomic_game_coupled_lifecycle():
    out = review.pair06_v8_baseline_lifetime_handoff_design_review_contract()
    assert out["game_coupled_runtime_lifecycle_required"] is True
    assert out["same_process_load_and_game_required"] is True
    assert out["fresh_environment_verification_required"] is True
    assert out["exact_17_asset_verification_required"] is True
    assert out["create_only_game_attempt_claim_required"] is True
    assert out["new_game_coupled_load_authorization_required"] is True
    assert out["new_game_execution_authorization_required"] is True
    assert out["single_authorization_must_cover_load_and_game"] is True


def test_review_grants_no_execution_authority():
    out = review.pair06_v8_baseline_lifetime_handoff_design_review_contract()
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
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_review_advances_only_to_game_coupled_runtime_implementation():
    out = review.pair06_v8_baseline_lifetime_handoff_design_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v8_baseline_game_coupled_runtime_implementation"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8BaselineLifetimeHandoffDesignReviewHold,
        match="PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_IMPLEMENTATION_REQUIRED",
    ):
        review.execute_or_load()
