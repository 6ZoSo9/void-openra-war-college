from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_preclaim_gpu_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_request_main_and_user_text():
    out = acceptance.pair06_v8_combat_priority_execution_authorization_acceptance_contract()
    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
    )
    assert out["authorized_request_bytes"] == 5098
    assert out["authorized_main_head"] == (
        "564fb5b4aa404cfc18e3e90b8df4a1a49109e858"
    )
    assert out["authorization_text_sha256"] == (
        "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
    )
    assert out["authorization_text_bytes"] == 11


def test_acceptance_pins_request_review_source_and_invocation():
    out = acceptance.pair06_v8_combat_priority_execution_authorization_acceptance_contract()
    assert out["request_review_git_blob"] == (
        "8ef081192c4859428b3a16a167c2b58345137e73"
    )
    assert out["request_review_source_sha256"] == (
        "f885004187a10520b6ab8e72a21a7e526db20a3d13a97e5cf73933f677b3e807"
    )
    assert out["request_review_test_git_blob"] == (
        "4feb24d495f16cd709ec61a06b329ed3076cced5"
    )
    assert out["request_review_test_sha256"] == (
        "2ca5e9c99fc7b7f1cfd7f49afa4914947095962eb156c64dab9dcf280ef640d9"
    )
    assert out["invocation_review_git_blob"] == (
        "222db31907543f2b776d811f309488e8dc95706a"
    )
    assert out["invocation_source_sha256"] == (
        "db383a1a833599d2b444dc4a07d6d1c08ef75e6e5c5dc6fd50cbe173ce5e39dd"
    )


def test_execution_and_policy_activation_require_fresh_gpu_admission():
    out = acceptance.pair06_v8_combat_priority_execution_authorization_acceptance_contract()
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["gpu_admission_failure_must_not_create_attempt_marker"] is True
    assert out["gpu_admission_failure_must_not_activate_policy"] is True
    assert out["gpu_admission_failure_must_not_load_model"] is True
    assert out["gpu_admission_failure_must_not_execute_inference"] is True
    assert out["gpu_admission_failure_must_not_execute_game"] is True
    assert out["attempt_marker_creation_authorized_after_fresh_gpu_admission"] is True
    assert out["policy_activation_authorized_after_fresh_gpu_admission"] is True
    assert out["runtime_load_authorized_after_fresh_gpu_admission"] is True
    assert out["model_inference_authorized_after_fresh_gpu_admission"] is True
    assert out["game_execution_authorized_after_fresh_gpu_admission"] is True


def test_acceptance_is_single_use_and_prior_lineage_nonreusable():
    out = acceptance.pair06_v8_combat_priority_execution_authorization_acceptance_contract()
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["execution_authorization_reusable_after_attempt_claim"] is False
    assert out["policy_activation_authorization_reusable_after_attempt_claim"] is False
    assert out["prior_spent_request_reusable"] is False
    assert out["prior_authorization_reusable"] is False
    assert out["prior_attempt_reusable"] is False
    assert out["prior_result_reusable_as_authority"] is False
    assert out["prior_closeout_reusable_as_authority"] is False
    assert out["spent_oom_attempt_reusable"] is False


def test_acceptance_preserves_unrelated_authority_boundaries():
    out = acceptance.pair06_v8_combat_priority_execution_authorization_acceptance_contract()
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
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
    ):
        assert out[field] is False


def test_acceptance_advances_to_exact_authorized_execution_gate():
    out = acceptance.pair06_v8_combat_priority_execution_authorization_acceptance_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED"
    )


def test_execute_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8CombatPriorityAuthorizationAcceptanceHold,
        match="COMBAT_ACTION_PRIORITY_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED",
    ):
        acceptance.execute()
