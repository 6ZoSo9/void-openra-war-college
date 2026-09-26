from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)


def test_request_is_proposal_only_and_binds_coherent_invocation():
    out = request.pair06_v8_combat_priority_coherent_execution_authorization_request_contract()
    proposal = out["request"]

    assert out[
        "pair06_v8_combat_priority_coherent_execution_authorization_request_implemented"
    ] is True
    assert proposal["record_kind"] == "proposal_only_not_authorization"
    assert proposal["source_binding"]["invocation_review_main_head"] == (
        "c941b437d63d82174af2849013d33e8d7ae29a86"
    )
    assert proposal["source_binding"]["invocation_review_git_blob"] == (
        "92ac3f8b09aa22be4ed2acf72834da7bc9db08b4"
    )
    assert proposal["source_binding"]["invocation_review_source_sha256"] == (
        "05bdcf091a19c0acdc2b40d19617d1c6e15b5788bed8a4e074554795a9d27100"
    )
    assert proposal["source_binding"]["invocation_source_sha256"] == (
        "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095"
    )


def test_request_seals_failed_request_authorization_and_attempt():
    out = request.pair06_v8_combat_priority_coherent_execution_authorization_request_contract()
    lineage = out["request"]["lineage"]

    assert lineage["prior_failed_request_sha256"] == (
        "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
    )
    assert lineage["prior_failed_request_reusable"] is False
    assert lineage["prior_failed_authorization_text_sha256"] == (
        "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
    )
    assert lineage["prior_failed_authorization_reusable"] is False
    assert lineage["prior_failed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert lineage["prior_failed_attempt_reusable"] is False
    assert lineage["prior_failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert lineage["prior_failed_run_reusable_as_authority"] is False
    assert lineage["prior_failed_result_present"] is False
    assert lineage["prior_failed_closeout_present"] is False


def test_request_scope_is_exactly_one_pair06_baseline_attempt():
    out = request.pair06_v8_combat_priority_coherent_execution_authorization_request_contract()
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
    out = request.pair06_v8_combat_priority_coherent_execution_authorization_request_contract()
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
    out = request.pair06_v8_combat_priority_coherent_execution_authorization_request_contract()

    for field in (
        "coherent_execution_authorization_accepted",
        "coherent_policy_activation_authorization_accepted",
        "coherent_execution_authorized",
        "coherent_policy_activation_authorized",
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
        .build_pair06_v8_combat_priority_coherent_execution_authorization_request()
    )
    validated = (
        request
        .validate_pair06_v8_combat_priority_coherent_execution_authorization_request(
            payload
        )
    )

    assert validated["request_bytes_valid"] is True
    assert validated["request_byte_length"] == len(payload)
    assert validated["next_gate"] == request.NEXT_GATE
    assert request.pair06_v8_combat_priority_coherent_execution_authorization_request_contract()[
        "next_gate"
    ] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        request.Pair06V8CombatPriorityCoherentAuthorizationRequestHold,
        match="EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.authorize_or_execute()
