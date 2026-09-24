from __future__ import annotations

import json
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)


def test_contract_closes_attempt_claim_and_invocation_implementation_only():
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()
    assert out["pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_implemented"] is True
    assert out["pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed"] is False
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
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()
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
        invocation.Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold,
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
        invocation.Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold,
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
        invocation.Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold,
        match="SUPERVISOR_SCOPE_HOLD",
    ):
        invocation._validate_supervisor_receipt(
            receipt,
            attempt_id="a" * 64,
        )


def test_contract_preserves_training_deployment_chain_and_funds_boundaries():
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()
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



def test_contract_requires_fresh_gpu_admission_before_claim():
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()
    assert out["reviewed_preclaim_gpu_observer_required"] is True
    assert out["historical_gpu_observation_nonreusable"] is True
    assert out["fresh_preclaim_gpu_observation_implemented"] is True
    assert out["fresh_preclaim_gpu_admission_required"] is True
    assert out["fresh_preclaim_gpu_observation_occurs_after_materialization"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["gpu_admission_hold_cleans_materialization_before_claim"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10


def test_fresh_gpu_helper_uses_reviewed_host_runner(monkeypatch):
    calls = {}

    def fake_observe(*, observation_authorized, command_runner):
        calls["authorized"] = observation_authorized
        calls["runner"] = command_runner
        return {
            "schema": invocation.gpu_admission.OBSERVATION_SCHEMA,
            "pair_slot": 6,
            "gpu_index": 0,
            "total_memory_bytes": 12_000,
            "free_memory_bytes": 11_000,
            "compute_processes": [],
            "observation_read_only": True,
            "attempt_marker_created": False,
            "model_load_performed": False,
            "model_inference_performed": False,
            "game_execution_performed": False,
        }

    def fake_admit(evidence):
        calls["evidence"] = evidence
        return {
            "preclaim_gpu_admitted": True,
            "execution_authorized": False,
        }

    monkeypatch.setattr(
        invocation.gpu_observer,
        "observe_pair06_v8_preclaim_gpu_readonly",
        fake_observe,
    )
    monkeypatch.setattr(
        invocation.gpu_admission,
        "evaluate_pair06_v8_preclaim_gpu_observation",
        fake_admit,
    )

    out = invocation._fresh_preclaim_gpu_observation()
    assert calls["authorized"] is True
    assert calls["runner"] is invocation.gpu_observer.host_nvidia_smi_readonly_runner
    assert calls["evidence"]["compute_processes"] == []
    assert out["admission"]["preclaim_gpu_admitted"] is True
    assert out["admission"]["execution_authorized"] is False


def test_fresh_gpu_helper_fails_closed_on_nonadmission(monkeypatch):
    monkeypatch.setattr(
        invocation.gpu_observer,
        "observe_pair06_v8_preclaim_gpu_readonly",
        lambda **kwargs: {
            "schema": invocation.gpu_admission.OBSERVATION_SCHEMA,
            "pair_slot": 6,
            "gpu_index": 0,
            "total_memory_bytes": 12_000,
            "free_memory_bytes": 5_000,
            "compute_processes": [{"pid": 123, "used_memory_bytes": 6_000}],
            "observation_read_only": True,
            "attempt_marker_created": False,
            "model_load_performed": False,
            "model_inference_performed": False,
            "game_execution_performed": False,
        },
    )
    monkeypatch.setattr(
        invocation.gpu_admission,
        "evaluate_pair06_v8_preclaim_gpu_observation",
        lambda evidence: {
            "preclaim_gpu_admitted": False,
            "execution_authorized": False,
        },
    )

    with pytest.raises(
        invocation.Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold,
        match="GPU_ADMISSION_NOT_GREEN",
    ):
        invocation._fresh_preclaim_gpu_observation()


def test_source_orders_gpu_admission_immediately_before_marker():
    source = Path(invocation.__file__).read_text(encoding="utf-8")
    function_start = source.index(
        "def execute_pair06_v8_baseline_game_receipt_bound_no_offload("
    )
    function_source = source[function_start:]
    materialize_at = function_source.index("materialization = _materialize(backend)")
    gpu_at = function_source.index(
        "gpu_preclaim = _fresh_preclaim_gpu_observation()"
    )
    marker_payload_at = function_source.index("marker_payload = {")
    marker_write_at = function_source.index(
        "_write_create_only(marker_path, marker_payload)"
    )
    supervisor_at = function_source.index(
        "supervisor.execute_pair06_v8_parent_supervisor_no_offload("
    )

    assert materialize_at < gpu_at < marker_payload_at < marker_write_at < supervisor_at


def test_historical_gpu_snapshot_cannot_be_reused_as_claim_authority():
    deps = invocation._dependency_contracts()
    history = deps["historical_precision_gpu_observation_review"]
    assert history["historical_observation_only"] is True
    assert history["observation_reusable_for_future_claim"] is False
    assert history["fresh_reobservation_required_before_attempt_marker"] is True
    assert history["retry_authorized"] is False
    assert history["attempt_marker_creation_authorized"] is False

def test_contract_advances_only_to_separate_source_review():
    out = invocation.pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        invocation.Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold,
        match="PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        invocation.authorize_or_execute()
