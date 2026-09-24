from __future__ import annotations

import json
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_no_offload_generation2
    as invocation,
)


def test_contract_closes_attempt_claim_and_invocation_implementation_only():
    out = invocation.pair06_v8_baseline_attempt_invocation_no_offload_contract()
    assert out["pair06_v8_baseline_attempt_invocation_no_offload_implemented"] is True
    assert out["pair06_v8_baseline_attempt_invocation_no_offload_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["no_offload_parent_generation_required"] is True
    assert out["second_preservation_result_review_required"] is True
    assert out["reviewed_worktree_materializer_reused"] is True
    assert out["pair06_specific_git_backend_required"] is True
    assert out["preclaim_worktree_materialization_implemented"] is True
    assert out["preclaim_materialization_cleanup_on_hold_implemented"] is True
    assert out["durable_create_only_attempt_marker_implemented"] is True
    assert out["marker_deletion_api_implemented"] is False
    assert out["reset_api_implemented"] is False
    assert out["resume_api_implemented"] is False
    assert out["attempt_marker_precedes_model_load_and_child_spawn"] is True
    assert out["marker_sha256_is_attempt_id"] is True
    assert out["no_offload_parent_receipt_schema_required"] is True
    assert out["inference_safe_placement_receipt_required"] is True
    assert out["durable_execution_result_before_cleanup_implemented"] is True
    assert out["success_only_worktree_cleanup_implemented"] is True
    assert out["durable_cleanup_closeout_implemented"] is True
    assert out["runs_preserved_after_success"] is True


def test_contract_is_non_authorizing_and_one_shot():
    out = invocation.pair06_v8_baseline_attempt_invocation_no_offload_contract()
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["explicit_authorization_boolean_required"] is True
    assert out["explicit_confirmation_token_required"] is True
    assert out["pair06_baseline_specific_authorization_accepted"] is False
    assert out["attempt_consumed"] is False
    assert out["runtime_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["game_execution_performed"] is False
    assert out["candidate_execution_authorized"] is False
    assert out["pair15_execution_authorized"] is False


def test_create_only_writer_is_durable_and_refuses_collision(tmp_path):
    path = tmp_path / "evidence.json"
    first = {"schema": "test", "value": 1}
    digest = invocation._write_create_only(path, first)
    raw = (
        json.dumps(
            first,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    assert digest == invocation.hashlib.sha256(raw).hexdigest()
    assert path.read_bytes() == raw
    assert (path.stat().st_mode & 0o777) == 0o600

    with pytest.raises(
        invocation.Pair06V8BaselineAttemptInvocationNoOffloadHold,
        match="CREATE_ONLY_COLLISION",
    ):
        invocation._write_create_only(path, first)


def test_supervisor_receipt_validation_rejects_missing_cuda_placement():
    receipt = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-parent-launcher-supervisor-no-offload-receipt.v1"
        ),
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": "a" * 64,
        "attempt_claimed": True,
    }
    with pytest.raises(
        invocation.Pair06V8BaselineAttemptInvocationNoOffloadHold,
        match="INFERENCE_SAFE_PLACEMENT_HOLD",
    ):
        invocation._validate_supervisor_receipt(
            receipt,
            attempt_id="a" * 64,
        )


def test_supervisor_receipt_validation_rejects_scope_drift():
    receipt = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-parent-launcher-supervisor-no-offload-receipt.v1"
        ),
        "inference_safe_placement": {
            "all_parameters_cuda0": True,
            "input_embedding_cuda0": True,
            "cpu_parameter_count": 0,
            "meta_parameter_count": 0,
            "disk_offload_present": False,
        },
        "pair_slot": 15,
        "arm": "baseline",
        "attempt_id": "a" * 64,
        "attempt_claimed": True,
    }
    with pytest.raises(
        invocation.Pair06V8BaselineAttemptInvocationNoOffloadHold,
        match="SUPERVISOR_SCOPE_HOLD",
    ):
        invocation._validate_supervisor_receipt(
            receipt,
            attempt_id="a" * 64,
        )


def test_contract_preserves_training_deployment_chain_and_funds_boundaries():
    out = invocation.pair06_v8_baseline_attempt_invocation_no_offload_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["host_io_performed_by_contract_inspection"] is False


def test_contract_advances_only_to_separate_source_review():
    out = invocation.pair06_v8_baseline_attempt_invocation_no_offload_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        invocation.Pair06V8BaselineAttemptInvocationNoOffloadHold,
        match="PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        invocation.authorize_or_execute()
