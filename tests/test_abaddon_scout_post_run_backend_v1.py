from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning import abaddon_scout_post_run_backend_v1 as backend


def _marker_bytes(experiment_id: str) -> bytes:
    record = {
        "schema": backend.attempt_guard.SCHEMA,
        "record_kind": "attempt_consumed_not_execution_evidence",
        "experiment_id": experiment_id,
        "request_sha256": "0" * 64,
        "launcher_contract_git_blob": "0" * 40,
        "single_use_scope": True,
        "pair03_attempt_reused": False,
        "pair03_attempt_reset": False,
        "scout_execution_authorized": False,
        "scout_execution_performed": False,
        "reusable_execution_permit": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_policy_promotion": False,
    }
    return (
        json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _inputs(tmp_path: Path):
    directory = tmp_path / "attempt"
    directory.mkdir(mode=0o700)
    experiment_id = "abaddon-scout-source-bound-v1-attempt-001"
    raw = _marker_bytes(experiment_id)
    marker = directory / backend.attempt_guard.MARKER_NAME
    marker.write_bytes(raw)
    marker.chmod(0o600)
    parent_stat = directory.stat()
    return (
        backend.ScoutPostRunBackendInputs(
            experiment_id=experiment_id,
            attempt_marker_path=str(marker),
            attempt_marker_sha256=hashlib.sha256(raw).hexdigest(),
            attempt_directory_identity=(parent_stat.st_dev, parent_stat.st_ino),
            engine_container_name="void-scout-repair-canary-4242",
            accepted_war_college_commit="a" * 40,
        ),
        raw,
    )


def _stat(*, ino: int, mode: int):
    return SimpleNamespace(
        st_dev=7,
        st_ino=ino,
        st_mode=mode,
        st_nlink=2 if _is_dir(mode) else 1,
        st_uid=os.geteuid(),
        st_size=4096 if _is_dir(mode) else 0,
        st_mtime_ns=11,
        st_ctime_ns=12,
    )


def _is_dir(mode: int) -> bool:
    import stat
    return stat.S_ISDIR(mode)


class FakePaths:
    def __init__(self):
        import stat
        self.rows = {
            backend.SOURCE_ROOT: _stat(ino=100, mode=stat.S_IFDIR | 0o755),
            backend.ENGINE_ROOT: _stat(ino=101, mode=stat.S_IFDIR | 0o755),
        }

    def lstat(self, path):
        if path in self.rows:
            return self.rows[path]
        return os.lstat(path)

    def resolve(self, path):
        if path in self.rows:
            return path
        return str(Path(path).resolve(strict=True))


class FakeRunner:
    def __init__(self, inputs):
        self.inputs = inputs
        self.calls = []
        self.rows = {
            backend.SERVICE_INACTIVE_COMMAND: {
                "returncode": 3,
                "stdout": "inactive\n",
                "stderr": "",
            },
            backend.MODEL_PROCESS_COMMAND: {
                "returncode": 1,
                "stdout": "",
                "stderr": "",
            },
            backend.DOCKER_CONTEXT_INSPECT_COMMAND: {
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "Name": backend.DOCKER_CONTEXT,
                            "Endpoints": {
                                "docker": {
                                    "Host": backend.EXPECTED_DOCKER_CONTEXT_HOST,
                                    "SkipTLSVerify": False,
                                }
                            },
                        }
                    ],
                    sort_keys=True,
                ),
                "stderr": "",
            },
            backend.DOCKER_INFO_COMMAND: {
                "returncode": 0,
                "stdout": json.dumps(
                    {
                        "SecurityOptions": ["name=rootless"],
                        "DockerRootDir": backend.EXPECTED_DOCKER_ROOT_DIR,
                        "OSType": "linux",
                    },
                    sort_keys=True,
                ),
                "stderr": "",
            },
            backend.SOURCE_HEAD_COMMAND: {
                "returncode": 0,
                "stdout": inputs.accepted_war_college_commit + "\n",
                "stderr": "",
            },
            backend.SOURCE_STATUS_COMMAND: {
                "returncode": 0,
                "stdout": "",
                "stderr": "",
            },
            backend.ENGINE_HEAD_COMMAND: {
                "returncode": 0,
                "stdout": backend.EXPECTED_ENGINE_COMMIT + "\n",
                "stderr": "",
            },
            backend.ENGINE_STATUS_COMMAND: {
                "returncode": 0,
                "stdout": "",
                "stderr": "",
            },
            backend._container_absence_command(inputs.engine_container_name): {
                "returncode": 0,
                "stdout": "",
                "stderr": "",
            },
        }

    def __call__(self, args):
        command = tuple(args)
        self.calls.append(command)
        if command not in self.rows:
            raise AssertionError(f"unexpected command: {command!r}")
        return deepcopy(self.rows[command])


def test_contract_binds_real_canary_runtime_identities_without_authority():
    out = backend.scout_post_run_backend_contract()
    assert out["derived_canary_runner_git_blob"] == (
        "40030e2ee61d17fd94abd1df733d3ea22650512b"
    )
    assert out["service_unit"] == "ollama.service"
    assert out["model_process_name"] == "ollama"
    assert out["engine_container_prefix"] == "void-scout-repair-canary-"
    assert out["docker_context"] == "rootless"
    assert out["expected_engine_commit"] == (
        "1607a7a6501d42a47638393ecef8b22831064932"
    )
    assert out["automatic_host_backend_selection"] is False
    assert out["git_optional_locks_disabled"] is True
    assert out["backend_source_binding_present"] is False
    assert out["host_observation_performed"] is False
    assert out["scout_execution_authorized"] is False


def test_build_probes_requires_authority_before_host_calls(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    paths = FakePaths()
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="OBSERVATION_NOT_AUTHORIZED",
    ):
        backend.build_scout_post_run_probes(
            inputs,
            observation_authorized=False,
            run_command=runner,
            file_backend=backend.host_file_backend(),
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )
    assert runner.calls == []


def test_exact_marker_probe_accepts_private_stable_matching_marker(tmp_path):
    inputs, _ = _inputs(tmp_path)
    paths = FakePaths()
    assert backend.probe_attempt_marker_present(
        inputs,
        file_backend=backend.host_file_backend(),
        lstat_path=paths.lstat,
        resolve_path=paths.resolve,
    ) is True


def test_marker_byte_drift_fails_closed(tmp_path):
    inputs, raw = _inputs(tmp_path)
    Path(inputs.attempt_marker_path).write_bytes(raw + b"x")
    Path(inputs.attempt_marker_path).chmod(0o600)
    paths = FakePaths()
    with pytest.raises(backend.ScoutPostRunBackendHold):
        backend.probe_attempt_marker_present(
            inputs,
            file_backend=backend.host_file_backend(),
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )


def test_marker_symlink_fails_closed(tmp_path):
    inputs, _ = _inputs(tmp_path)
    marker = Path(inputs.attempt_marker_path)
    target = marker.with_name("target")
    marker.rename(target)
    marker.symlink_to(target.name)
    paths = FakePaths()
    with pytest.raises(backend.ScoutPostRunBackendHold):
        backend.probe_attempt_marker_present(
            inputs,
            file_backend=backend.host_file_backend(),
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )



def test_copied_marker_in_different_private_directory_fails_identity_binding(tmp_path):
    inputs, raw = _inputs(tmp_path)
    copied_dir = tmp_path / "copied"
    copied_dir.mkdir(mode=0o700)
    copied = copied_dir / backend.attempt_guard.MARKER_NAME
    copied.write_bytes(raw)
    copied.chmod(0o600)
    changed = backend.ScoutPostRunBackendInputs(
        experiment_id=inputs.experiment_id,
        attempt_marker_path=str(copied),
        attempt_marker_sha256=inputs.attempt_marker_sha256,
        attempt_directory_identity=inputs.attempt_directory_identity,
        engine_container_name=inputs.engine_container_name,
        accepted_war_college_commit=inputs.accepted_war_college_commit,
    )
    paths = FakePaths()
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="SCOUT_MARKER_PARENT_IDENTITY_DRIFT",
    ):
        backend.probe_attempt_marker_present(
            changed,
            file_backend=backend.host_file_backend(),
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )

def test_service_inactive_requires_exact_systemd_inactive_semantics(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    assert backend.probe_runtime_service_inactive(run_command=runner) is True
    runner.rows[backend.SERVICE_INACTIVE_COMMAND] = {
        "returncode": 0,
        "stdout": "active\n",
        "stderr": "",
    }
    with pytest.raises(backend.ScoutPostRunBackendHold):
        backend.probe_runtime_service_inactive(run_command=runner)


def test_model_process_absence_distinguishes_no_match_from_error(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    assert backend.probe_model_process_absent(run_command=runner) is True
    runner.rows[backend.MODEL_PROCESS_COMMAND] = {
        "returncode": 2,
        "stdout": "",
        "stderr": "error",
    }
    with pytest.raises(backend.ScoutPostRunBackendHold, match="COMMAND_FAILED"):
        backend.probe_model_process_absent(run_command=runner)


def test_container_absence_requires_successful_exact_empty_rootless_listing(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    assert backend.probe_engine_container_absent(
        inputs,
        run_command=runner,
    ) is True
    command = backend._container_absence_command(inputs.engine_container_name)
    runner.rows[command] = {
        "returncode": 0,
        "stdout": inputs.engine_container_name + "\n",
        "stderr": "",
    }
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="STILL_PRESENT",
    ):
        backend.probe_engine_container_absent(inputs, run_command=runner)



def test_container_absence_rejects_wrong_rootless_context_host(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    payload = json.loads(runner.rows[backend.DOCKER_CONTEXT_INSPECT_COMMAND]["stdout"])
    payload[0]["Endpoints"]["docker"]["Host"] = "unix:///var/run/docker.sock"
    runner.rows[backend.DOCKER_CONTEXT_INSPECT_COMMAND]["stdout"] = json.dumps(payload)
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="SCOUT_DOCKER_CONTEXT_HOST_DRIFT",
    ):
        backend.probe_engine_container_absent(inputs, run_command=runner)
    assert backend._container_absence_command(inputs.engine_container_name) not in runner.calls


def test_container_absence_rejects_nonrootless_daemon(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    payload = json.loads(runner.rows[backend.DOCKER_INFO_COMMAND]["stdout"])
    payload["SecurityOptions"] = []
    runner.rows[backend.DOCKER_INFO_COMMAND]["stdout"] = json.dumps(payload)
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="SCOUT_DOCKER_NOT_ROOTLESS",
    ):
        backend.probe_engine_container_absent(inputs, run_command=runner)
    assert backend._container_absence_command(inputs.engine_container_name) not in runner.calls

def test_source_probe_binds_exact_heads_cleanliness_and_directory_generation(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    paths = FakePaths()
    assert backend.probe_source_checkout_clean(
        inputs,
        run_command=runner,
        lstat_path=paths.lstat,
        resolve_path=paths.resolve,
    ) is True
    runner.rows[backend.SOURCE_STATUS_COMMAND]["stdout"] = " M file.py\n"
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="SOURCE_TRACKED_DIRTY",
    ):
        backend.probe_source_checkout_clean(
            inputs,
            run_command=runner,
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )



def test_source_probe_rejects_state_change_between_first_and_second_pass(tmp_path):
    inputs, _ = _inputs(tmp_path)
    paths = FakePaths()

    class DriftingRunner(FakeRunner):
        def __init__(self, inputs):
            super().__init__(inputs)
            self.source_status_calls = 0

        def __call__(self, args):
            command = tuple(args)
            if command == backend.SOURCE_STATUS_COMMAND:
                self.source_status_calls += 1
                self.calls.append(command)
                if self.source_status_calls == 2:
                    return {
                        "returncode": 0,
                        "stdout": "?? late-file\n",
                        "stderr": "",
                    }
                return deepcopy(self.rows[command])
            return super().__call__(args)

    runner = DriftingRunner(inputs)
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="SCOUT_GIT_STATE_CHANGED_DURING_OBSERVATION",
    ):
        backend.probe_source_checkout_clean(
            inputs,
            run_command=runner,
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )

def test_bound_collection_composes_five_independent_probes_in_adapter_order(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    paths = FakePaths()
    authority_calls = []

    def authority():
        authority_calls.append(len(authority_calls) + 1)
        return True

    raw = backend.collect_bound_scout_post_run_evidence(
        inputs,
        observation_authorized=True,
        read_authority_check=authority,
        run_command=runner,
        file_backend=backend.host_file_backend(),
        lstat_path=paths.lstat,
        resolve_path=paths.resolve,
    )
    record = json.loads(raw)
    assert record["observations"] == {
        name: True for name in backend.observer.REQUIRED_OBSERVATIONS
    }
    assert authority_calls == [1, 2, 3, 4, 5]
    assert runner.calls == [
        backend.SERVICE_INACTIVE_COMMAND,
        backend.DOCKER_CONTEXT_INSPECT_COMMAND,
        backend.DOCKER_INFO_COMMAND,
        backend._container_absence_command(inputs.engine_container_name),
        backend.MODEL_PROCESS_COMMAND,
        backend.SOURCE_HEAD_COMMAND,
        backend.SOURCE_STATUS_COMMAND,
        backend.ENGINE_HEAD_COMMAND,
        backend.ENGINE_STATUS_COMMAND,
        backend.SOURCE_HEAD_COMMAND,
        backend.SOURCE_STATUS_COMMAND,
        backend.ENGINE_HEAD_COMMAND,
        backend.ENGINE_STATUS_COMMAND,
    ]
    assert all(record["claims"][name] is False for name in record["claims"])


def test_revoked_authority_stops_before_next_backend_probe(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    paths = FakePaths()
    values = iter((True, False))

    with pytest.raises(
        backend.observer.ScoutPostRunObserverHold,
        match="AUTHORITY_REQUIRED:runtime_service_inactive",
    ):
        backend.collect_bound_scout_post_run_evidence(
            inputs,
            observation_authorized=True,
            read_authority_check=lambda: next(values),
            run_command=runner,
            file_backend=backend.host_file_backend(),
            lstat_path=paths.lstat,
            resolve_path=paths.resolve,
        )
    assert runner.calls == []


def test_invalid_or_unbound_container_identity_fails_before_commands(tmp_path):
    inputs, _ = _inputs(tmp_path)
    runner = FakeRunner(inputs)
    changed = backend.ScoutPostRunBackendInputs(
        experiment_id=inputs.experiment_id,
        attempt_marker_path=inputs.attempt_marker_path,
        attempt_marker_sha256=inputs.attempt_marker_sha256,
        attempt_directory_identity=inputs.attempt_directory_identity,
        engine_container_name="not-the-canary-container",
        accepted_war_college_commit=inputs.accepted_war_college_commit,
    )
    with pytest.raises(backend.ScoutPostRunBackendHold):
        backend.build_scout_post_run_probes(
            changed,
            observation_authorized=True,
            run_command=runner,
            file_backend=backend.host_file_backend(),
            lstat_path=FakePaths().lstat,
            resolve_path=FakePaths().resolve,
        )
    assert runner.calls == []



def test_host_runner_disables_git_optional_locks(monkeypatch):
    observed = {}

    class Completed:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(args, **kwargs):
        observed["args"] = tuple(args)
        observed["env"] = dict(kwargs["env"])
        return Completed()

    monkeypatch.setattr(backend.subprocess, "run", fake_run)
    out = backend.host_readonly_command_runner(backend.SOURCE_STATUS_COMMAND)
    assert out["returncode"] == 0
    assert observed["args"] == backend.SOURCE_STATUS_COMMAND
    assert observed["env"]["GIT_OPTIONAL_LOCKS"] == "0"



def test_host_runner_rejects_mutating_or_unreviewed_commands_before_subprocess(monkeypatch):
    calls = []

    def trap(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("subprocess must not be reached")

    monkeypatch.setattr(backend.subprocess, "run", trap)
    with pytest.raises(backend.ScoutPostRunBackendHold):
        backend.host_readonly_command_runner(
            (backend.SYSTEMCTL, "start", backend.SERVICE_UNIT)
        )
    with pytest.raises(backend.ScoutPostRunBackendHold):
        backend.host_readonly_command_runner(
            (backend.DOCKER, "rm", "anything")
        )
    assert calls == []


def test_authorize_or_execute_always_holds():
    with pytest.raises(
        backend.ScoutPostRunBackendHold,
        match="EXECUTION_AUTHORITY_UNAVAILABLE",
    ):
        backend.authorize_or_execute()
