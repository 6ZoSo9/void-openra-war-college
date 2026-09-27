from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)


def test_request_is_proposal_only_and_binds_v2_invocation():
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )
    proposal = out["request"]

    assert out[
        "pair06_v8_combat_priority_coherent_v2_execution_authorization_request_implemented"
    ] is True
    assert proposal["record_kind"] == "proposal_only_not_authorization"
    assert proposal["source_binding"]["invocation_review_main_head"] == (
        "bc0b6938323ad9cf31457f1af02d120598445dac"
    )
    assert proposal["source_binding"]["invocation_review_git_blob"] == (
        "8e78f768c1a701d4c7b3afec0665faf2bfa256e8"
    )
    assert proposal["source_binding"]["invocation_review_source_sha256"] == (
        "74eca7280dfac30cac0fd10ee857f9fc11deb7c7c20d145463f47631137433ad"
    )
    assert proposal["source_binding"]["invocation_source_sha256"] == (
        "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
    )


def test_request_seals_prior_consumed_request_authorization_and_attempt():
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )
    lineage = out["request"]["lineage"]

    assert lineage["prior_consumed_request_sha256"] == (
        "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
    )
    assert lineage["prior_consumed_request_reusable"] is False
    assert lineage["prior_consumed_authorization_text_sha256"] == (
        "e8a71c19b5849665a169743b849368dd326b5c6cc26a1f585def71f448fb94ca"
    )
    assert lineage["prior_consumed_authorization_reusable"] is False
    assert lineage["prior_consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert lineage["prior_consumed_attempt_reusable"] is False
    assert lineage["prior_consumed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert lineage["prior_consumed_run_preserved"] is True
    assert lineage["prior_consumed_run_reusable_as_authority"] is False
    assert lineage["prior_consumed_result_present"] is False
    assert lineage["prior_consumed_closeout_present"] is False


def test_request_requires_v2_mapping_coherence():
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )
    mapping = out["request"]["mapping_coherence"]

    assert mapping["v1_production_function_pruning_required"] is True
    assert mapping["v2_legal_building_reconstruction_required"] is True
    assert mapping["v2_legal_unit_reconstruction_required"] is True
    assert mapping["translator_legal_building_mapping_coherence_required"] is True
    assert mapping["translator_legal_unit_mapping_coherence_required"] is True
    assert mapping["normal_mode_identity_required"] is True


def test_request_scope_is_exactly_one_pair06_baseline_attempt():
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )
    scope = out["request"]["proposed_scope"]

    assert scope["pair_slot"] == 6
    assert scope["arm"] == "baseline"
    assert scope["held_out"] is False
    assert scope["doctrine"] == "FEINTER"
    assert scope["seed"] == 208354846
    assert scope["rounds"] == 36
    assert scope["ticks_per_round"] == 25
    assert scope["maximum_attempts"] == 1
    assert scope["maximum_automatic_retries"] == 0
    assert scope["candidate_arm_included"] is False
    assert scope["held_out_pair15_included"] is False
    assert scope["pair03_replay_included"] is False
    assert scope["pair09_replay_included"] is False


def test_request_requires_fresh_gpu_and_fresh_dual_authority():
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )
    proposal = out["request"]
    gpu = proposal["gpu_admission_policy"]
    activation = proposal["policy_activation"]

    assert gpu["fresh_observation_required"] is True
    assert gpu["fresh_observation_precedes_attempt_marker"] is True
    assert gpu["zero_foreign_compute_processes_required"] is True
    assert gpu["minimum_free_memory_fraction"] == {
        "numerator": 9,
        "denominator": 10,
    }
    assert gpu["historical_gpu_observation_reusable"] is False
    assert gpu["gpu_admission_hold_must_not_consume_attempt"] is True

    assert activation["policy_id"] == (
        "pair06-v8-combat-action-priority-envelope-v1"
    )
    assert activation["policy_activation_requested"] is True
    assert activation[
        "separate_policy_activation_authorization_required"
    ] is True
    assert activation["separate_policy_confirmation_required"] is True
    assert activation["request_digest_grants_policy_activation"] is False


def test_request_grants_no_authority():
    out = (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()
    )

    for field in (
        "v2_coherent_execution_authorization_accepted",
        "v2_coherent_policy_activation_authorization_accepted",
        "v2_coherent_execution_authorized",
        "v2_coherent_policy_activation_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        assert out[field] is False

    assert out["matching_request_digest_grants_authority"] is False
    assert all(value is False for value in out["authority"].values())


def test_exact_request_roundtrip_and_next_gate():
    payload = (
        request
        .build_pair06_v8_combat_priority_coherent_v2_execution_authorization_request()
    )
    assert len(payload) == 5670
    import hashlib
    assert hashlib.sha256(payload).hexdigest() == (
        "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
    )
    validated = (
        request
        .validate_pair06_v8_combat_priority_coherent_v2_execution_authorization_request(
            payload
        )
    )

    assert validated["request_bytes_valid"] is True
    assert validated["request_byte_length"] == len(payload)
    assert validated["next_gate"] == request.NEXT_GATE
    assert (
        request
        .pair06_v8_combat_priority_coherent_v2_execution_authorization_request_contract()[
            "next_gate"
        ]
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
            "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
        )
    )


def test_entrypoint_holds():
    with pytest.raises(
        request.Pair06V8CombatPriorityCoherentV2AuthorizationRequestHold,
        match="EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.authorize_or_execute()
