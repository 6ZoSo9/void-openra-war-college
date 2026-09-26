from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_preclaim_gpu_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_request_main_and_user_text():
    out = acceptance.pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract()

    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
    )
    assert out["authorized_request_bytes"] == 4998
    assert out["authorized_main_head"] == (
        "3ca55f3d6327d5e12c1f1e6b3d3ae4adf09ea009"
    )
    assert out["authorization_text_sha256"] == (
        "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
    )
    assert out["authorization_text_bytes"] == 457


def test_acceptance_pins_request_review_and_invocation():
    out = acceptance.pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract()

    assert out["request_review_git_blob"] == (
        "8c9f55231e2d62194f0ecba2469e9fb83784af37"
    )
    assert out["request_review_source_sha256"] == (
        "8dd65c5c4f19fecebe0d4e320f6cde5895ee51a90f55c1e45f961deb97123258"
    )
    assert out["request_review_test_git_blob"] == (
        "33111ba3ba4219fc7ed10d9ccbef37fd0d855c16"
    )
    assert out["request_review_test_sha256"] == (
        "7e7def0cb44a75de0227e1bfec423023e05764325922fea1a98c9d6f7c7cbf84"
    )
    assert out["invocation_source_sha256"] == (
        "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095"
    )


def test_fresh_gpu_admission_conditions_all_runtime_authority():
    out = acceptance.pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract()

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


def test_acceptance_is_single_use_and_prior_failed_lineage_is_nonreusable():
    out = acceptance.pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract()

    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["execution_authorization_reusable_after_attempt_claim"] is False
    assert out["policy_activation_authorization_reusable_after_attempt_claim"] is False

    assert out["prior_failed_request_sha256"] == (
        "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
    )
    assert out["prior_failed_request_reusable"] is False
    assert out["prior_failed_authorization_text_sha256"] == (
        "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
    )
    assert out["prior_failed_authorization_reusable"] is False
    assert out["prior_failed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["prior_failed_attempt_reusable"] is False
    assert out["prior_failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert out["prior_failed_run_reusable_as_authority"] is False


def test_acceptance_preserves_unrelated_authority_boundaries():
    out = acceptance.pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract()

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
    out = acceptance.pair06_v8_combat_priority_coherent_execution_authorization_acceptance_contract()

    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED"
    )


def test_execute_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8CombatPriorityCoherentAuthorizationAcceptanceHold,
        match="CONTRACT_COHERENCE_REPAIR_RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED",
    ):
        acceptance.execute()
