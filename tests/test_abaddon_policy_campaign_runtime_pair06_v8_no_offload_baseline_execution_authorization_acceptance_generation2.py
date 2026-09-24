from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_baseline_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_authorization_is_bound_but_unconsumed_preclaim():
    out = acceptance.pair06_v8_no_offload_execution_authorization_acceptance_contract()
    assert out["authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
    )
    assert out["authorized_main_head"] == (
        "d0fec8faabe34a13ab530fb73d1ce21cad1b79f7"
    )
    assert out["authorization_text_sha256"] == (
        "1159b0b9f8e1914c69343ee2091f72bac573ce11a04b1543bd3b44b65b1722f5"
    )
    assert out["authorization_text_bytes"] == 827
    assert out["preclaim_hold"] is True
    assert out["receipt_schema_binding_repair_canonical"] is True
    assert out["repair_canonical_main_head"] == (
        "9c0b5ecea847abe5b9d997b1cda4f86bbe3e9287"
    )
    assert out["historical_no_offload_invocation_preserved"] is True
    assert out["historical_invocation_git_blob"] == (
        "b93255245f4d622dfb2cf0ddd6f97c3592f87cdc"
    )
    assert out["historical_invocation_source_sha256"] == (
        "4be25b850afc45cd34b977308add5cd288ce95411c683ca6545e0fb2fd6a0529"
    )
    assert out["receipt_bound_invocation_git_blob"] == (
        "f22313cc3481b806a30dee5a7009b62c25293f17"
    )
    assert out["receipt_bound_invocation_source_sha256"] == (
        "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
    )
    assert out["held_authorization_superseded"] is True
    assert out["attempt_marker_created"] is False
    assert out["attempt_consumed"] is False


def test_receipt_schema_mismatch_is_exact_hold_reason():
    out = acceptance.pair06_v8_no_offload_execution_authorization_acceptance_contract()
    assert out["preclaim_hold_reason"] == (
        "no_offload_parent_receipt_schema_vs_invocation_validator_mismatch"
    )
    assert out["expected_parent_receipt_schema"].endswith(
        "pair06-v8-parent-launcher-supervisor-no-offload-receipt.v1"
    )
    assert out["observed_invocation_expected_schema"].endswith(
        "pair06-v8-parent-launcher-supervisor-receipt.v1"
    )


def test_no_execution_occurred_and_old_authorization_cannot_follow_changed_main():
    out = acceptance.pair06_v8_no_offload_execution_authorization_acceptance_contract()
    for field in (
        "attempt_marker_created",
        "attempt_consumed",
        "runtime_load_performed",
        "model_inference_performed",
        "child_spawn_performed",
        "game_execution_performed",
        "automatic_retry",
        "authorization_reusable_after_main_or_request_change",
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


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8NoOffloadAuthorizationAcceptanceHold,
        match="RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        acceptance.execute()
