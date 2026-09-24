from __future__ import annotations

import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)


def test_request_binds_gpu_gated_invocation():
    out = request.pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract()
    binding = out["request"]["source_binding"]
    assert binding["invocation_review_git_blob"] == (
        "77dbac309565beb804ac1c2936799574efe5de82"
    )
    assert binding["invocation_review_source_sha256"] == (
        "beec87bea767fdb0c13c14ed7072d49b8fb18db08f6745c22172931ce8843cce"
    )
    assert binding["invocation_source_sha256"] == (
        "302c6a472aa18f7829f46222c87bf192c19422c9d0622a23ad39995adabdc386"
    )


def test_request_preserves_spent_oom_lineage():
    out = request.pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract()
    lineage = out["request"]["lineage"]
    assert lineage["spent_receipt_bound_request_sha256"] == (
        "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
    )
    assert lineage["spent_receipt_bound_authorization_text_sha256"] == (
        "bc898d1349d281a83ee094563f34b7f21d6f4c02891014029d4a8a3fc6d28f0f"
    )
    assert lineage["spent_oom_attempt_marker_sha256"] == (
        "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
    )
    assert lineage["spent_receipt_bound_request_was_authorized"] is True
    assert lineage["spent_receipt_bound_attempt_consumed"] is True
    assert lineage["spent_receipt_bound_request_reusable"] is False
    assert lineage["spent_oom_attempt_reusable"] is False
    assert lineage["spent_oom_failure_type"] == "OutOfMemoryError"
    assert lineage["spent_oom_failure_stage"] == (
        "transformers.caching_allocator_warmup"
    )
    assert lineage["spent_oom_preclaim_free_memory_bytes"] == 5756354560
    assert lineage["spent_oom_foreign_compute_pid"] == 2850305


def test_request_requires_fresh_cuda0_admission():
    out = request.pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract()
    policy = out["request"]["gpu_admission_policy"]
    assert policy["gpu_index"] == 0
    assert policy["fresh_observation_required"] is True
    assert policy["fresh_observation_precedes_attempt_marker"] is True
    assert policy["zero_foreign_compute_processes_required"] is True
    assert policy["minimum_free_memory_fraction"] == {
        "numerator": 9,
        "denominator": 10,
    }
    assert policy["historical_clean_gpu_evidence_sha256"] == (
        "8ccd26d5a90cda5e75d6b7ce93501ddb240f5d9da2cf56f518f5ce9c96519237"
    )
    assert policy["historical_clean_gpu_observation_reusable"] is False
    assert policy["gpu_admission_hold_must_not_consume_attempt"] is True


def test_request_preserves_exact_pair06_scope():
    out = request.pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract()
    scope = out["request"]["proposed_scope"]
    assert scope["pair_slot"] == 6
    assert scope["arm"] == "baseline"
    assert scope["held_out"] is False
    assert scope["doctrine"] == "FEINTER"
    assert scope["seed"] == 208354846
    assert scope["rounds"] == 36
    assert scope["ticks_per_round"] == 25
    assert scope["starter_infantry"] == 4
    assert scope["staging_max_ticks"] == 800
    assert scope["maximum_attempts"] == 1
    assert scope["maximum_automatic_retries"] == 0
    assert scope["candidate_arm_included"] is False
    assert scope["held_out_pair15_included"] is False


def test_request_is_proposal_only_and_non_authorizing():
    out = request.pair06_v8_preclaim_gpu_baseline_execution_authorization_request_contract()
    assert out[
        "pair06_v8_preclaim_gpu_baseline_execution_authorization_request_implemented"
    ] is True
    assert out["pair06_preclaim_gpu_baseline_specific_authorization_accepted"] is False
    assert out["pair06_preclaim_gpu_baseline_execution_authorized"] is False
    assert out["pair06_preclaim_gpu_baseline_execution_performed"] is False
    assert out["matching_request_digest_grants_authority"] is False
    assert all(value is False for value in out["authority"].values())
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
        "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_request_bytes_are_fixed_and_tampering_fails():
    payload = request.build_pair06_v8_preclaim_gpu_baseline_execution_authorization_request()
    result = (
        request
        .validate_pair06_v8_preclaim_gpu_baseline_execution_authorization_request(
            payload
        )
    )
    assert result["request_bytes_valid"] is True
    assert len(result["request_sha256"]) == 64
    assert result["request_byte_length"] == len(payload)

    body = json.loads(payload)
    body["gpu_admission_policy"]["historical_clean_gpu_observation_reusable"] = True
    tampered = (
        json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    with pytest.raises(
        request.Pair06V8PreclaimGpuBaselineExecutionAuthorizationRequestHold,
        match="request bytes differ",
    ):
        request.validate_pair06_v8_preclaim_gpu_baseline_execution_authorization_request(
            tampered
        )


def test_execution_entrypoint_holds():
    with pytest.raises(
        request.Pair06V8PreclaimGpuBaselineExecutionAuthorizationRequestHold,
        match=(
            "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
            "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
        ),
    ):
        request.authorize_or_execute()
