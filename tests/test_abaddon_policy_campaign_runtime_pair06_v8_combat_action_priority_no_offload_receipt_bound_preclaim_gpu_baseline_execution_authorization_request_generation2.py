from __future__ import annotations

import hashlib
import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)


def test_request_is_deterministic_canonical_json():
    first = request.build_pair06_v8_combat_priority_execution_authorization_request()
    second = request.build_pair06_v8_combat_priority_execution_authorization_request()
    assert first == second
    assert first.endswith(b"\n")
    decoded = json.loads(first)
    assert decoded["record_kind"] == "proposal_only_not_authorization"
    assert hashlib.sha256(first).hexdigest() == (
        request.validate_pair06_v8_combat_priority_execution_authorization_request(
            first
        )["request_sha256"]
    )


def test_request_binds_exact_reviewed_combat_priority_invocation():
    out = request.pair06_v8_combat_priority_execution_authorization_request_contract()
    binding = out["request"]["source_binding"]
    assert binding["invocation_review_main_head"] == (
        "3bdc27aca30e0926626410bbedc7d445f4a3dd77"
    )
    assert binding["invocation_review_git_blob"] == (
        "222db31907543f2b776d811f309488e8dc95706a"
    )
    assert binding["invocation_review_source_sha256"] == (
        "297b53a9f934722c0f1f355e52776c40bd9923e0cd5fbb30cca9c427f2a5f7f2"
    )
    assert binding["invocation_source_sha256"] == (
        "db383a1a833599d2b444dc4a07d6d1c08ef75e6e5c5dc6fd50cbe173ce5e39dd"
    )


def test_request_marks_prior_successful_lineage_spent_and_nonreusable():
    lineage = (
        request
        .pair06_v8_combat_priority_execution_authorization_request_contract()
        ["request"]["lineage"]
    )
    assert lineage["prior_spent_gpu_gated_request_sha256"] == (
        "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
    )
    assert lineage["prior_spent_authorization_text_sha256"] == (
        "3cdbfa07fcc1fa14ab0ce01a7e5456b1bf16583ceda5baee16a0191e8a3cf011"
    )
    assert lineage["prior_spent_attempt_marker_sha256"] == (
        "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
    )
    assert lineage["prior_result_file_sha256"] == (
        "f1a3a1ffec2957b984212e5c11067a477934a1c484020dcb2e6398764a117440"
    )
    assert lineage["prior_closeout_file_sha256"] == (
        "f0227597d44ecfc5ae07fdc473a2ca9bda71085fba9970279dedf31d5ac24920"
    )
    assert lineage["prior_spent_gpu_gated_request_reusable"] is False
    assert lineage["prior_spent_authorization_reusable"] is False
    assert lineage["prior_spent_attempt_reusable"] is False
    assert lineage["prior_successful_attempt_consumed"] is True


def test_request_preserves_gpu_and_one_shot_scope():
    proposal = (
        request
        .pair06_v8_combat_priority_execution_authorization_request_contract()
        ["request"]
    )
    gpu = proposal["gpu_admission_policy"]
    scope = proposal["proposed_scope"]
    assert gpu["gpu_index"] == 0
    assert gpu["fresh_observation_required"] is True
    assert gpu["fresh_observation_precedes_attempt_marker"] is True
    assert gpu["zero_foreign_compute_processes_required"] is True
    assert gpu["minimum_free_memory_fraction"] == {
        "numerator": 9,
        "denominator": 10,
    }
    assert scope["maximum_attempts"] == 1
    assert scope["maximum_automatic_retries"] == 0
    assert scope["candidate_arm_included"] is False
    assert scope["held_out_pair15_included"] is False
    assert scope["pair03_replay_included"] is False
    assert scope["pair09_replay_included"] is False


def test_request_requires_distinct_policy_activation_authority():
    proposal = (
        request
        .pair06_v8_combat_priority_execution_authorization_request_contract()
        ["request"]
    )
    activation = proposal["policy_activation"]
    assert activation["policy_id"] == (
        "pair06-v8-combat-action-priority-envelope-v1"
    )
    assert activation["policy_activation_requested"] is True
    assert activation[
        "separate_policy_activation_authorization_required"
    ] is True
    assert activation["separate_policy_confirmation_required"] is True
    assert activation["request_digest_grants_policy_activation"] is False


def test_matching_request_digest_never_grants_authority():
    out = request.pair06_v8_combat_priority_execution_authorization_request_contract()
    assert out["matching_request_digest_grants_authority"] is False
    for value in out["authority"].values():
        assert value is False
    for field in (
        "combat_priority_execution_authorization_accepted",
        "combat_priority_policy_activation_authorization_accepted",
        "combat_priority_execution_authorized",
        "combat_priority_policy_activation_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        assert out[field] is False


def test_validator_rejects_modified_request_bytes():
    payload = request.build_pair06_v8_combat_priority_execution_authorization_request()
    with pytest.raises(
        request.Pair06V8CombatPriorityExecutionAuthorizationRequestHold,
        match="request bytes differ",
    ):
        request.validate_pair06_v8_combat_priority_execution_authorization_request(
            payload + b" "
        )


def test_request_advances_only_to_source_binding_review():
    out = request.pair06_v8_combat_priority_execution_authorization_request_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        request.Pair06V8CombatPriorityExecutionAuthorizationRequestHold,
        match="AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.authorize_or_execute()
