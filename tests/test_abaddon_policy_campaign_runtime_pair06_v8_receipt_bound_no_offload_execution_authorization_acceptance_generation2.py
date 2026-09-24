from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_receipt_bound_no_offload_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_authorization_binds_exact_request_main_and_text():
    out = (
        acceptance
        .pair06_v8_receipt_bound_no_offload_execution_authorization_acceptance_contract()
    )
    assert out["authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
    )
    assert out["authorized_request_bytes"] == 4828
    assert out["authorized_main_head"] == (
        "bdb305aeaec8288b817d648dcc86124b26f4b4c4"
    )
    assert out["authorization_text_sha256"] == (
        "bc898d1349d281a83ee094563f34b7f21d6f4c02891014029d4a8a3fc6d28f0f"
    )
    assert out["authorization_text_bytes"] == 966


def test_authorization_is_one_fresh_pair06_baseline_attempt_only():
    out = (
        acceptance
        .pair06_v8_receipt_bound_no_offload_execution_authorization_acceptance_contract()
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["receipt_bound_no_offload_execution_authorized"] is True
    assert out["runtime_load_authorized"] is True
    assert out["model_inference_authorized"] is True
    assert out["game_execution_authorized"] is True
    assert out["single_gpu_cuda0_placement_required"] is True
    assert out["cpu_disk_meta_parameter_offload_allowed"] is False


def test_old_lineage_is_not_reusable():
    out = (
        acceptance
        .pair06_v8_receipt_bound_no_offload_execution_authorization_acceptance_contract()
    )
    assert out["superseded_request_reusable"] is False
    assert out["superseded_request_attempt_consumed"] is False
    assert out["first_spent_request_reusable"] is False
    assert out["second_spent_request_reusable"] is False
    assert out["first_spent_attempt_reusable"] is False
    assert out["second_spent_attempt_reusable"] is False


def test_exclusions_remain_false():
    out = (
        acceptance
        .pair06_v8_receipt_bound_no_offload_execution_authorization_acceptance_contract()
    )
    for field in (
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
        "attempt_marker_created_by_this_record",
        "execution_performed_by_this_record",
        "authorization_reusable_after_attempt_claim",
    ):
        assert out[field] is False


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8ReceiptBoundNoOffloadAuthorizationAcceptanceHold,
        match="RECEIPT_BOUND_NO_OFFLOAD_EXECUTION_AUTHORIZED",
    ):
        acceptance.execute()
