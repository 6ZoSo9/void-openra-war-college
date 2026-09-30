from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_fresh_user_authorization():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

    assert out["authorization_record_kind"] == "explicit_user_authorization"
    assert out["authorization_accepted"] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["authorized_main_head"] == (
        "bfe8f06245ed2951d247973df927a756a37cfbfd"
    )
    assert out["authorization_text_sha256"] == (
        "d41fd580d15b4d59491fbb7a2b635946656bbb6c6ae61bcc9222085e23a45bd6"
    )
    assert out["authorization_text_bytes"] == 362


def test_acceptance_binds_exact_reviewed_request_identity():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()
    reviewed = out["reviewed_request"]

    assert out["authorized_request_sha256"] == reviewed["request_bytes_sha256"]
    assert out["authorized_request_bytes"] == reviewed["request_byte_length"]
    assert out["request_review_git_blob"] == (
        "8565d587e57335a2a30940effa40713ae6a7315a"
    )
    assert out["request_source_git_blob"] == (
        "1fcc9968ae6032613096fdbcd9550ca718cd257f"
    )
    assert out["request_test_git_blob"] == (
        "b8737c0040de2e2f0e3437f9b9496c18ba17408a"
    )
    assert out["request_review_test_git_blob"] == (
        "9a5f805ca434411f40f9a222e36426a62705f6bf"
    )


def test_authorized_scope_is_exactly_one_v9_baseline_attempt():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-qwen35-4b-lora-v1"
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False


def test_fresh_gpu_admission_still_precedes_any_effect():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

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


def test_acceptance_authorizes_only_after_fresh_gpu_admission():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

    assert out["receipt_bound_preclaim_gpu_execution_authorized"] is True
    assert out["v9_policy_activation_authorized"] is True
    assert out["attempt_marker_creation_authorized_after_fresh_gpu_admission"] is True
    assert out["policy_activation_authorized_after_fresh_gpu_admission"] is True
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
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
    ),
)
def test_acceptance_record_performs_no_effect_and_grants_no_extra_authority(field):
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()
    assert out[field] is False


def test_authorization_becomes_nonreusable_after_attempt_claim():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

    assert out["execution_authorization_reusable_after_attempt_claim"] is False
    assert out["policy_activation_authorization_reusable_after_attempt_claim"] is False


def test_acceptance_advances_only_to_preclaim_gpu_execution_gate():
    out = acceptance.pair06_v9_execution_authorization_acceptance_contract()

    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_RECEIPT_BOUND_PRECLAIM_GPU_"
        "EXECUTION_AUTHORIZED"
    )


def test_execute_holds():
    with pytest.raises(
        acceptance.Pair06V9StrictVisibleContactAuthorizationAcceptanceHold,
        match="RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED",
    ):
        acceptance.execute()
