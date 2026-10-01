from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_fresh_authorization_and_canonical_main():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["authorization_text_sha256"] == (
        "ad1edd0797e2ec6d95d0a4346a09d1a6d02e7f47ba32029cd6d80ec48c532af3"
    )
    assert out["authorization_text_bytes"] == 13
    assert out["authorized_main_head"] == (
        "b30533b6f3855845e24eeabc1729e8113358cdbb"
    )
    assert out["authorized_main_tree"] == (
        "d78ade6ea0a8a53634417eea424ebb0a3b1e03a5"
    )
    assert out["canonical_main_bound_at_authorization_time"] is True


def test_acceptance_binds_exact_reviewed_request():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()
    reviewed = out["reviewed_request"]

    assert out["authorized_request_sha256"] == reviewed["request_bytes_sha256"]
    assert out["authorized_request_bytes"] == reviewed["request_byte_length"]
    assert out["request_review_git_blob"] == (
        "19afaae0a30ddebb22e37ba7b5004d370fb97517"
    )
    assert out["request_source_git_blob"] == (
        "1110cd7fc41f390f579e2207ac2fc9d0bfa4adcf"
    )
    assert out["request_test_git_blob"] == (
        "e03d008ff79f2428994b4f877a3c0477868be632"
    )
    assert out["request_review_test_git_blob"] == (
        "4788c6068b35bc2a71020d58ea03c424c431de85"
    )


def test_acceptance_preserves_single_attempt_gpu_gate_and_fresh_namespace():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_order_evidence_namespace_required"] is True
    assert out["historical_v9_attempt_reusable"] is False
    assert out["historical_v9_authorization_reusable"] is False


def test_gpu_failure_blocks_all_runtime_effects():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    assert out["gpu_admission_failure_must_not_create_attempt_marker"] is True
    assert out["gpu_admission_failure_must_not_activate_policy"] is True
    assert out["gpu_admission_failure_must_not_activate_order_coherence"] is True
    assert out["gpu_admission_failure_must_not_load_model"] is True
    assert out["gpu_admission_failure_must_not_execute_inference"] is True
    assert out["gpu_admission_failure_must_not_execute_game"] is True


def test_acceptance_authorizes_only_after_fresh_gpu_admission():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    assert out["receipt_bound_preclaim_gpu_execution_authorized"] is True
    assert out["v9_policy_activation_authorized"] is True
    assert out["v9_order_coherence_activation_authorized"] is True
    assert out["attempt_marker_creation_authorized_after_fresh_gpu_admission"] is True
    assert out["policy_activation_authorized_after_fresh_gpu_admission"] is True
    assert out["order_coherence_activation_authorized_after_fresh_gpu_admission"] is True
    assert out["runtime_load_authorized_after_fresh_gpu_admission"] is True
    assert out["model_inference_authorized_after_fresh_gpu_admission"] is True
    assert out["game_execution_authorized_after_fresh_gpu_admission"] is True


@pytest.mark.parametrize(
    "field",
    (
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
        "scheduler_mutation_authorized",
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "order_coherence_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
    ),
)
def test_acceptance_record_performs_no_effect_and_grants_no_extra_authority(field):
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()
    assert out[field] is False


def test_three_authorizations_become_nonreusable_after_attempt_claim():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    assert out["execution_authorization_reusable_after_attempt_claim"] is False
    assert out["policy_activation_authorization_reusable_after_attempt_claim"] is False
    assert out[
        "order_coherence_activation_authorization_reusable_after_attempt_claim"
    ] is False


def test_acceptance_advances_only_to_authorized_launcher_source_gate():
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        acceptance.Pair06V9InputOrderCoherenceAuthorizationAcceptanceHold,
        match="INPUT_ORDER_COHERENCE_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED",
    ):
        acceptance.execute()
