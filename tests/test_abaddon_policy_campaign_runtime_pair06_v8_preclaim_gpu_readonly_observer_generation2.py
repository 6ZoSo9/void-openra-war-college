from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_readonly_observer_generation2
    as observer,
)


MIB = 1024 * 1024


class FakeRunner:
    def __init__(self, *, device_stdout, process_stdout=b""):
        self.device_stdout = device_stdout
        self.process_stdout = process_stdout
        self.calls = []

    def __call__(
        self,
        argv,
        *,
        timeout_seconds,
        maximum_stdout_bytes,
    ):
        exact = tuple(argv)
        self.calls.append(
            (exact, timeout_seconds, maximum_stdout_bytes)
        )
        if exact == observer.DEVICE_QUERY:
            stdout = self.device_stdout
        elif exact == observer.PROCESS_QUERY:
            stdout = self.process_stdout
        else:
            raise AssertionError(f"unexpected argv: {exact!r}")
        return {
            "returncode": 0,
            "stdout": stdout,
            "stderr": b"",
        }


def clean_runner():
    return FakeRunner(
        device_stdout=b"0, GPU-AAAA, 12288, 11520\n",
        process_stdout=b"",
    )


def test_contract_binds_reviewed_admission_and_readonly_boundary():
    out = observer.pair06_v8_preclaim_gpu_readonly_observer_contract()
    assert out["admission_review_git_blob"] == (
        "00876b15ce0317d548b14e98dd5c3a480f11c84f"
    )
    assert out["admission_review_source_sha256"] == (
        "3991a1bcb2ffe855495cb983c3a4540f947d2079d60c7bf8fd1283b8a6ca06ba"
    )
    assert out["pair_slot"] == 6
    assert out["gpu_index"] == 0
    assert out["nvidia_smi_path"] == "/usr/bin/nvidia-smi"
    assert out["host_nvidia_smi_readonly_runner_present"] is True
    assert out["automatic_command_runner_selection"] is False
    assert out["observation_requires_explicit_authority"] is True


def test_contract_has_no_mutating_or_runtime_capability():
    out = observer.pair06_v8_preclaim_gpu_readonly_observer_contract()
    for field in (
        "observer_grants_gpu_admission",
        "process_signal_implemented",
        "process_termination_implemented",
        "service_action_implemented",
        "attempt_marker_creation_implemented",
        "runtime_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "training_implemented",
        "policy_promotion_implemented",
        "deployment_implemented",
        "void_chain_mutation_implemented",
        "wallet_or_funds_action_implemented",
    ):
        assert out[field] is False


def test_observation_authority_is_checked_before_runner_call():
    runner = clean_runner()
    with pytest.raises(
        observer.Pair06V8PreclaimGpuReadonlyObserverHold,
        match="OBSERVATION_NOT_AUTHORIZED",
    ):
        observer.observe_pair06_v8_preclaim_gpu_readonly(
            observation_authorized=False,
            command_runner=runner,
        )
    assert runner.calls == []


def test_clean_cuda0_snapshot_matches_admission_schema():
    runner = clean_runner()
    evidence = observer.observe_pair06_v8_preclaim_gpu_readonly(
        observation_authorized=True,
        command_runner=runner,
    )
    assert [call[0] for call in runner.calls] == [
        observer.DEVICE_QUERY,
        observer.PROCESS_QUERY,
    ]
    assert evidence == {
        "schema": observer.admission.OBSERVATION_SCHEMA,
        "pair_slot": 6,
        "gpu_index": 0,
        "total_memory_bytes": 12288 * MIB,
        "free_memory_bytes": 11520 * MIB,
        "compute_processes": [],
        "observation_read_only": True,
        "attempt_marker_created": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }
    admitted = observer.admission.evaluate_pair06_v8_preclaim_gpu_observation(
        evidence
    )
    assert admitted["preclaim_gpu_admitted"] is True
    assert admitted["execution_authorized"] is False


def test_foreign_cuda0_process_is_observed_not_terminated():
    runner = FakeRunner(
        device_stdout=b"0, GPU-AAAA, 12288, 5756\n",
        process_stdout=(
            b"GPU-BBBB, 22, 512\n"
            b"GPU-AAAA, 2850305, 5427\n"
        ),
    )
    evidence = observer.observe_pair06_v8_preclaim_gpu_readonly(
        observation_authorized=True,
        command_runner=runner,
    )
    assert evidence["compute_processes"] == [
        {
            "pid": 2850305,
            "used_memory_bytes": 5427 * MIB,
        }
    ]
    with pytest.raises(
        observer.admission.Pair06V8PreclaimGpuAdmissionHold,
        match="FOREIGN_COMPUTE_PROCESS_HOLD",
    ):
        observer.admission.evaluate_pair06_v8_preclaim_gpu_observation(
            evidence
        )


def test_exact_cuda0_row_is_required():
    runner = FakeRunner(
        device_stdout=b"1, GPU-BBBB, 12288, 12000\n",
    )
    with pytest.raises(
        observer.Pair06V8PreclaimGpuReadonlyObserverHold,
        match="EXACT_CUDA0_REQUIRED",
    ):
        observer.observe_pair06_v8_preclaim_gpu_readonly(
            observation_authorized=True,
            command_runner=runner,
        )


def test_duplicate_cuda0_rows_fail_closed():
    runner = FakeRunner(
        device_stdout=(
            b"0, GPU-AAAA, 12288, 12000\n"
            b"0, GPU-BBBB, 12288, 12000\n"
        ),
    )
    with pytest.raises(
        observer.Pair06V8PreclaimGpuReadonlyObserverHold,
        match="DUPLICATE_DEVICE_INDEX",
    ):
        observer.observe_pair06_v8_preclaim_gpu_readonly(
            observation_authorized=True,
            command_runner=runner,
        )


def test_runner_nonzero_exit_fails_closed():
    class BadRunner:
        def __init__(self):
            self.calls = 0

        def __call__(self, argv, *, timeout_seconds, maximum_stdout_bytes):
            self.calls += 1
            return {
                "returncode": 1,
                "stdout": b"",
                "stderr": b"failed",
            }

    runner = BadRunner()
    with pytest.raises(
        observer.Pair06V8PreclaimGpuReadonlyObserverHold,
        match="DEVICE_QUERY_NONZERO_EXIT",
    ):
        observer.observe_pair06_v8_preclaim_gpu_readonly(
            observation_authorized=True,
            command_runner=runner,
        )
    assert runner.calls == 1


def test_host_runner_rejects_unreviewed_command_before_subprocess(monkeypatch):
    called = False

    def fake_run(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("subprocess must not run")

    monkeypatch.setattr(observer.subprocess, "run", fake_run)
    with pytest.raises(
        observer.Pair06V8PreclaimGpuReadonlyObserverHold,
        match="COMMAND_NOT_REVIEWED",
    ):
        observer.host_nvidia_smi_readonly_runner(
            ("/bin/echo", "bad"),
            timeout_seconds=1.0,
            maximum_stdout_bytes=1024,
        )
    assert called is False


def test_host_runner_uses_no_shell_and_exact_command(monkeypatch):
    seen = {}

    def fake_run(argv, **kwargs):
        seen["argv"] = tuple(argv)
        seen["kwargs"] = kwargs
        return SimpleNamespace(
            returncode=0,
            stdout=b"0, GPU-AAAA, 12288, 11520\n",
            stderr=b"",
        )

    monkeypatch.setattr(observer.subprocess, "run", fake_run)
    result = observer.host_nvidia_smi_readonly_runner(
        observer.DEVICE_QUERY,
        timeout_seconds=1.0,
        maximum_stdout_bytes=1024,
    )
    assert seen["argv"] == observer.DEVICE_QUERY
    assert seen["kwargs"]["shell"] is False
    assert seen["kwargs"]["stdin"] is observer.subprocess.DEVNULL
    assert result["returncode"] == 0


def test_contract_advances_only_to_source_binding_review():
    out = observer.pair06_v8_preclaim_gpu_readonly_observer_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        observer.Pair06V8PreclaimGpuReadonlyObserverHold,
        match="PAIR06_V8_PRECLAIM_GPU_READONLY_OBSERVER_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        observer.observe_or_execute()
