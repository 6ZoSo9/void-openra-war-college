from __future__ import annotations

import json
import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_generation2
    as request,
)


def test_request_binds_both_spent_attempts_and_no_offload_generation():
    out = request.pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_contract()
    lineage = out["request"]["repair_lineage"]
    assert lineage["first_spent_attempt_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert lineage["second_spent_attempt_sha256"] == (
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
    )
    assert lineage["first_spent_attempt_reusable"] is False
    assert lineage["second_spent_attempt_reusable"] is False
    assert lineage["both_failed_attempts_archived"] is True
    assert lineage["fresh_attempt_required"] is True
    assert lineage["no_offload_parent_generation_required"] is True
    assert lineage["no_offload_parent_receipt_schema_bound"] is True
    assert lineage["inference_safe_placement_receipt_required"] is True
    assert lineage["held_superseded_request_sha256"] == (
        "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
    )
    assert lineage["held_superseded_request_preclaim"] is True
    assert lineage["held_superseded_request_attempt_consumed"] is False
    assert lineage["held_superseded_request_reusable"] is False
    assert lineage["single_gpu_cuda0_placement_required"] is True
    assert lineage["cpu_disk_meta_parameter_offload_allowed"] is False


def test_request_preserves_exact_pair06_scope():
    out = request.pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_contract()
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
    out = request.pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_contract()
    assert out["pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request_implemented"] is True
    assert out["pair06_no_offload_baseline_specific_authorization_accepted"] is False
    assert out["pair06_no_offload_baseline_execution_authorized"] is False
    assert out["pair06_no_offload_baseline_execution_performed"] is False
    assert out["matching_request_digest_grants_authority"] is False
    assert all(value is False for value in out["authority"].values())
    assert out["next_gate"] == (
        "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_request_bytes_are_fixed_and_tampering_fails():
    payload = request.build_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request()
    result = request.validate_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request(
        payload
    )
    assert result["request_bytes_valid"] is True
    assert len(result["request_sha256"]) == 64

    body = json.loads(payload)
    body["repair_lineage"]["second_spent_attempt_reusable"] = True
    tampered = (
        json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    with pytest.raises(
        request.Pair06V8NoOffloadReceiptBoundBaselineExecutionAuthorizationRequestHold,
        match="request bytes differ",
    ):
        request.validate_pair06_v8_no_offload_receipt_bound_baseline_execution_authorization_request(
            tampered
        )


def test_execution_entrypoint_holds():
    with pytest.raises(
        request.Pair06V8NoOffloadReceiptBoundBaselineExecutionAuthorizationRequestHold,
        match="NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        request.authorize_or_execute()
