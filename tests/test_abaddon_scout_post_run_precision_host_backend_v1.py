from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_scout_external_attempt_guard_v1 as attempt_guard,
)
from openra_env.learning import (
    abaddon_scout_post_run_precision_host_backend_review_v1 as source_review,
)
from openra_env.learning import (
    abaddon_scout_post_run_precision_host_backend_v1 as backend,
)


REPO = Path(__file__).resolve().parents[1]
BACKEND_SOURCE = REPO / source_review.BACKEND_PATH
OBSERVER_SOURCE = REPO / source_review.OBSERVER_PATH
ATTEMPT_SOURCE = REPO / source_review.ATTEMPT_GUARD_PATH
EXPECTED_HEAD = "1" * 40


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


class FakeRunner:
    def __init__(self, overrides=None):
        self.calls: list[tuple[tuple[str, ...], str | None]] = []
        self.results = {
            backend.SYSTEMCTL_ACTIVE: {
                "returncode": 3,
                "stdout": "inactive\n",
                "stderr": "",
            },
            backend.SYSTEMCTL_ENABLED: {
                "returncode": 1,
                "stdout": "disabled\n",
                "stderr": "",
            },
            backend.DOCKER_CONTEXT_INSPECT: {
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "Name": "rootless",
                            "Endpoints": {
                                "docker": {
                                    "Host": "unix:///run/user/1000/docker.sock",
                                    "SkipTLSVerify": False,
                                }
                            },
                        }
                    ]
                ),
                "stderr": "",
            },
            backend.DOCKER_CONTAINER_LIST: {
                "returncode": 0,
                "stdout": "",
                "stderr": "",
            },
            backend.PGREP_OLLAMA: {
                "returncode": 1,
                "stdout": "",
                "stderr": "",
            },
            backend.GIT_HEAD: {
                "returncode": 0,
                "stdout": EXPECTED_HEAD + "\n",
                "stderr": "",
            },
            backend.GIT_STATUS: {
                "returncode": 0,
                "stdout": "",
                "stderr": "",
            },
        }
        if overrides:
            self.results.update(overrides)

    def __call__(self, args, *, cwd=None):
        command = tuple(args)
        self.calls.append((command, cwd))
        return dict(self.results[command])


class AttemptDirectory:
    def __init__(self, tmp_path: Path, *, marker: bool = True, mode: int = 0o600):
        self.path = tmp_path / "attempt"
        self.path.mkdir(mode=0o700)
        if marker:
            marker_path = self.path / attempt_guard.MARKER_NAME
            marker_path.write_bytes(b"{}\n")
            marker_path.chmod(mode)
        self.fd = os.open(self.path, os.O_RDONLY | os.O_DIRECTORY)
        st = os.fstat(self.fd)
        self.identity = (int(st.st_dev), int(st.st_ino))

    def close(self):
        os.close(self.fd)


def _backend(tmp_path, *, runner=None, authority=lambda: True, hostname=None):
    directory = AttemptDirectory(tmp_path)
    host = backend.ScoutPostRunPrecisionHostBackend(
        read_authority_check=authority,
        attempt_directory_fd=directory.fd,
        expected_attempt_directory_identity=directory.identity,
        expected_source_head=EXPECTED_HEAD,
        run_command=runner or FakeRunner(),
        hostname=hostname or (lambda: backend.EXPECTED_HOST),
    )
    return directory, host


def test_exact_source_bindings_are_current() -> None:
    assert _git_blob(BACKEND_SOURCE.read_bytes()) == source_review.BACKEND_GIT_BLOB
    assert _git_blob(OBSERVER_SOURCE.read_bytes()) == source_review.OBSERVER_GIT_BLOB
    assert (
        _git_blob(ATTEMPT_SOURCE.read_bytes())
        == source_review.ATTEMPT_GUARD_GIT_BLOB
    )


def test_source_binding_review_is_green_and_nonoperational() -> None:
    result = source_review.review_precision_host_backend_source(
        backend_bytes=BACKEND_SOURCE.read_bytes(),
        observer_bytes=OBSERVER_SOURCE.read_bytes(),
        attempt_guard_bytes=ATTEMPT_SOURCE.read_bytes(),
    )
    assert result["backend_source_reviewed"] is True
    assert result["precision_host_identity_bound"] is True
    assert result["rootless_docker_identity_bound"] is True
    assert result["host_observation_performed"] is False
    assert result["execution_authorized"] is False
    assert (
        result["next_gate"]
        == "SCOUT_POST_RUN_PRECISION_HOST_BACKEND_LIVE_QUALIFICATION_REQUIRED"
    )


def test_source_binding_rejects_backend_byte_drift() -> None:
    with pytest.raises(
        source_review.ScoutPostRunPrecisionHostBackendReviewHold,
        match="BACKEND_SOURCE_DRIFT",
    ):
        source_review.review_precision_host_backend_source(
            backend_bytes=BACKEND_SOURCE.read_bytes() + b"\n",
            observer_bytes=OBSERVER_SOURCE.read_bytes(),
            attempt_guard_bytes=ATTEMPT_SOURCE.read_bytes(),
        )


def test_all_five_backend_probes_positive_with_synthetic_readonly_host(tmp_path) -> None:
    directory, host = _backend(tmp_path)
    try:
        probes = host.probes()
        assert set(probes) == set(backend.observer.REQUIRED_OBSERVATIONS)
        assert {name: probe() for name, probe in probes.items()} == {
            name: True for name in backend.observer.REQUIRED_OBSERVATIONS
        }
    finally:
        directory.close()


def test_full_observer_composition_emits_five_positive_observations(tmp_path) -> None:
    directory = AttemptDirectory(tmp_path)
    calls = {"authority": 0}

    def authority():
        calls["authority"] += 1
        return True

    try:
        raw = backend.observe_post_run_with_precision_backend(
            experiment_id="abaddon-scout-canary-live-v1",
            attempt_marker_sha256="a" * 64,
            expected_source_head=EXPECTED_HEAD,
            attempt_directory_fd=directory.fd,
            expected_attempt_directory_identity=directory.identity,
            read_authority_check=authority,
            run_command=FakeRunner(),
            hostname=lambda: backend.EXPECTED_HOST,
        )
    finally:
        directory.close()

    record = json.loads(raw)
    assert record["schema"] == backend.observer.EVIDENCE_SCHEMA
    assert record["observations"] == {
        name: True for name in backend.observer.REQUIRED_OBSERVATIONS
    }
    assert all(value is False for value in record["claims"].values())
    assert calls["authority"] == 10


def test_missing_attempt_marker_returns_false_without_content_read(tmp_path) -> None:
    directory = AttemptDirectory(tmp_path, marker=False)
    host = backend.ScoutPostRunPrecisionHostBackend(
        read_authority_check=lambda: True,
        attempt_directory_fd=directory.fd,
        expected_attempt_directory_identity=directory.identity,
        expected_source_head=EXPECTED_HEAD,
        run_command=FakeRunner(),
        hostname=lambda: backend.EXPECTED_HOST,
    )
    try:
        assert host.attempt_marker_present() is False
    finally:
        directory.close()


def test_wrong_attempt_marker_mode_holds(tmp_path) -> None:
    directory = AttemptDirectory(tmp_path, mode=0o644)
    host = backend.ScoutPostRunPrecisionHostBackend(
        read_authority_check=lambda: True,
        attempt_directory_fd=directory.fd,
        expected_attempt_directory_identity=directory.identity,
        expected_source_head=EXPECTED_HEAD,
        run_command=FakeRunner(),
        hostname=lambda: backend.EXPECTED_HOST,
    )
    try:
        with pytest.raises(
            backend.ScoutPostRunPrecisionHostBackendHold,
            match="ATTEMPT_MARKER_METADATA_HOLD",
        ):
            host.attempt_marker_present()
    finally:
        directory.close()


@pytest.mark.parametrize(
    "overrides,method",
    [
        (
            {
                backend.SYSTEMCTL_ACTIVE: {
                    "returncode": 0,
                    "stdout": "active\n",
                    "stderr": "",
                }
            },
            "runtime_service_inactive",
        ),
        (
            {
                backend.DOCKER_CONTAINER_LIST: {
                    "returncode": 0,
                    "stdout": "void-scout-repair-canary-12345\n",
                    "stderr": "",
                }
            },
            "engine_container_absent",
        ),
        (
            {
                backend.PGREP_OLLAMA: {
                    "returncode": 0,
                    "stdout": "12345\n",
                    "stderr": "",
                }
            },
            "model_process_absent",
        ),
        (
            {
                backend.GIT_STATUS: {
                    "returncode": 0,
                    "stdout": " M tracked.py\n",
                    "stderr": "",
                }
            },
            "source_checkout_clean",
        ),
        (
            {
                backend.GIT_HEAD: {
                    "returncode": 0,
                    "stdout": "2" * 40 + "\n",
                    "stderr": "",
                }
            },
            "source_checkout_clean",
        ),
    ],
)
def test_adversarial_post_run_state_returns_false(tmp_path, overrides, method) -> None:
    directory, host = _backend(tmp_path, runner=FakeRunner(overrides))
    try:
        assert getattr(host, method)() is False
    finally:
        directory.close()


def test_wrong_hostname_holds_before_command(tmp_path) -> None:
    runner = FakeRunner()
    directory, host = _backend(
        tmp_path,
        runner=runner,
        hostname=lambda: "not-precision",
    )
    try:
        with pytest.raises(
            backend.ScoutPostRunPrecisionHostBackendHold,
            match="HOSTNAME_DRIFT",
        ):
            host.runtime_service_inactive()
        assert runner.calls == []
    finally:
        directory.close()


def test_revoked_authority_holds_before_command(tmp_path) -> None:
    runner = FakeRunner()
    directory, host = _backend(
        tmp_path,
        runner=runner,
        authority=lambda: False,
    )
    try:
        with pytest.raises(
            backend.ScoutPostRunPrecisionHostBackendHold,
            match="READ_AUTHORITY_REQUIRED",
        ):
            host.engine_container_absent()
        assert runner.calls == []
    finally:
        directory.close()


def test_docker_context_identity_drift_holds(tmp_path) -> None:
    runner = FakeRunner(
        {
            backend.DOCKER_CONTEXT_INSPECT: {
                "returncode": 0,
                "stdout": json.dumps(
                    [
                        {
                            "Name": "rootless",
                            "Endpoints": {
                                "docker": {
                                    "Host": "unix:///var/run/docker.sock",
                                    "SkipTLSVerify": False,
                                }
                            },
                        }
                    ]
                ),
                "stderr": "",
            }
        }
    )
    directory, host = _backend(tmp_path, runner=runner)
    try:
        with pytest.raises(
            backend.ScoutPostRunPrecisionHostBackendHold,
            match="DOCKER_ENDPOINT_DRIFT",
        ):
            host.engine_container_absent()
    finally:
        directory.close()


def test_command_allowlist_rejects_mutating_argv() -> None:
    with pytest.raises(
        backend.ScoutPostRunPrecisionHostBackendHold,
        match="COMMAND_NOT_REVIEWED",
    ):
        backend._validate_command(
            (backend.DOCKER, "rm", "-f", "anything"),
            cwd=None,
        )


def test_git_commands_require_exact_designated_repo_cwd() -> None:
    with pytest.raises(
        backend.ScoutPostRunPrecisionHostBackendHold,
        match="GIT_CWD_DRIFT",
    ):
        backend._validate_command(
            backend.GIT_HEAD,
            cwd="/tmp/not-reviewed",
        )


def test_backend_contract_has_no_mutation_or_execution_authority() -> None:
    contract = backend.precision_post_run_backend_contract()
    assert contract["expected_host"] == "zoso-Precision-Tower-7810"
    assert contract["system_service"] == "ollama.service"
    assert contract["service_scope"] == "system"
    assert contract["docker_context"] == "rootless"
    assert contract["docker_host"] == "unix:///run/user/1000/docker.sock"
    assert contract["canary_container_prefix"] == "void-scout-repair-canary-"
    for field in (
        "shell_execution_implemented",
        "attempt_marker_content_read_implemented",
        "service_mutation_implemented",
        "container_mutation_implemented",
        "git_mutation_implemented",
        "model_http_request_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "automatic_retry_implemented",
        "automatic_backend_invocation",
        "execution_authority_created",
    ):
        assert contract[field] is False


def test_operational_authorizers_always_hold() -> None:
    with pytest.raises(
        backend.ScoutPostRunPrecisionHostBackendHold,
        match="OBSERVATION_ONLY",
    ):
        backend.authorize_or_execute()
    with pytest.raises(
        source_review.ScoutPostRunPrecisionHostBackendReviewHold,
        match=source_review.NEXT_GATE,
    ):
        source_review.authorize_live_observation_or_execute()
