"""Precision read-only host backend for scout post-run observation.

This module implements the five concrete probe callbacks required by
abaddon_scout_post_run_observer_v1 for the reviewed Precision host.

Import performs no host action. Every public probe rechecks an explicit read
authority callback immediately before observation. Commands are fixed, bounded,
read-only argv vectors; there is no shell, service mutation, container mutation,
Git mutation, model request, game execution, retry, or credential/wallet access.

The attempt marker probe reads metadata only. It never opens marker contents.
"""

from __future__ import annotations

import json
import os
import stat
import subprocess
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Protocol

from openra_env.learning import abaddon_scout_external_attempt_guard_v1 as attempt_guard
from openra_env.learning import abaddon_scout_post_run_observer_v1 as observer


CONTRACT_SCHEMA = "void.abaddon.scout-post-run-precision-host-backend-contract.v1"
EXPECTED_HOST = "zoso-Precision-Tower-7810"
EXPECTED_REPO_ROOT = "/home/zoso/dev/openra-rl-war-college"

SYSTEMCTL = "/usr/bin/systemctl"
DOCKER = "/usr/bin/docker"
PGREP = "/usr/bin/pgrep"
GIT = "/usr/bin/git"

OLLAMA_SERVICE = "ollama.service"
OLLAMA_PROCESS_NAME = "ollama"

DOCKER_CONTEXT = "rootless"
EXPECTED_DOCKER_HOST = "unix:///run/user/1000/docker.sock"
CANARY_CONTAINER_PREFIX = "void-scout-repair-canary-"

COMMAND_TIMEOUT_SECONDS = 5.0
MAX_STDOUT_BYTES = 4 * 1024 * 1024
MAX_STDERR_BYTES = 64 * 1024

SYSTEMCTL_ACTIVE = (SYSTEMCTL, "is-active", OLLAMA_SERVICE)
SYSTEMCTL_ENABLED = (SYSTEMCTL, "is-enabled", OLLAMA_SERVICE)
DOCKER_CONTEXT_INSPECT = (DOCKER, "context", "inspect", DOCKER_CONTEXT)
DOCKER_CONTAINER_LIST = (
    DOCKER,
    "--context",
    DOCKER_CONTEXT,
    "ps",
    "-a",
    "--format",
    "{{.Names}}",
)
PGREP_OLLAMA = (PGREP, "-x", OLLAMA_PROCESS_NAME)
GIT_HEAD = (GIT, "rev-parse", "HEAD")
GIT_STATUS = (
    GIT,
    "status",
    "--porcelain=v1",
    "--untracked-files=no",
)

FIXED_COMMANDS = frozenset(
    (
        SYSTEMCTL_ACTIVE,
        SYSTEMCTL_ENABLED,
        DOCKER_CONTEXT_INSPECT,
        DOCKER_CONTAINER_LIST,
        PGREP_OLLAMA,
        GIT_HEAD,
        GIT_STATUS,
    )
)

FORBIDDEN_TOKENS = frozenset(
    (
        "start",
        "stop",
        "restart",
        "reload",
        "enable",
        "disable",
        "mask",
        "unmask",
        "run",
        "exec",
        "create",
        "rm",
        "remove",
        "kill",
        "pause",
        "unpause",
        "pull",
        "push",
        "build",
        "tag",
        "rmi",
        "prune",
        "commit",
        "checkout",
        "reset",
        "merge",
        "rebase",
        "clean",
        "fetch",
    )
)

SHA40 = frozenset("0123456789abcdef")


class ScoutPostRunPrecisionHostBackendHold(RuntimeError):
    pass


class CommandRunner(Protocol):
    def __call__(
        self,
        args: Sequence[str],
        *,
        cwd: str | None = None,
    ) -> Mapping[str, Any]:
        ...


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutPostRunPrecisionHostBackendHold(code)


def _valid_sha40(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 40
        and all(character in SHA40 for character in value)
    )


def _validate_command(
    args: Sequence[str],
    *,
    cwd: str | None,
) -> tuple[str, ...]:
    _require(
        isinstance(args, (tuple, list)),
        "SCOUT_POST_RUN_COMMAND_SEQUENCE_REQUIRED",
    )
    command = tuple(args)
    _require(
        command in FIXED_COMMANDS,
        "SCOUT_POST_RUN_COMMAND_NOT_REVIEWED",
    )
    lowered = {part.lower() for part in command[1:]}
    _require(
        lowered.isdisjoint(FORBIDDEN_TOKENS),
        "SCOUT_POST_RUN_MUTATING_COMMAND_TOKEN_FORBIDDEN",
    )
    if command in {GIT_HEAD, GIT_STATUS}:
        _require(
            cwd == EXPECTED_REPO_ROOT,
            "SCOUT_POST_RUN_GIT_CWD_DRIFT",
        )
    else:
        _require(cwd is None, "SCOUT_POST_RUN_NON_GIT_CWD_FORBIDDEN")
    return command


def host_readonly_command_runner(
    args: Sequence[str],
    *,
    cwd: str | None = None,
) -> dict[str, Any]:
    """Run exactly one reviewed read-only command; never selected automatically."""
    command = _validate_command(args, cwd=cwd)
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
            env={
                "HOME": "/home/zoso",
                "LANG": "C",
                "LC_ALL": "C",
                "PATH": "/usr/bin:/bin",
            },
        )
    except (subprocess.TimeoutExpired, OSError) as error:
        raise ScoutPostRunPrecisionHostBackendHold(
            f"SCOUT_POST_RUN_COMMAND_FAILED:{type(error).__name__}"
        ) from error

    stdout = completed.stdout.encode("utf-8", errors="replace")
    stderr = completed.stderr.encode("utf-8", errors="replace")
    _require(
        len(stdout) <= MAX_STDOUT_BYTES,
        "SCOUT_POST_RUN_STDOUT_EXCEEDS_BOUND",
    )
    _require(
        len(stderr) <= MAX_STDERR_BYTES,
        "SCOUT_POST_RUN_STDERR_EXCEEDS_BOUND",
    )
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _command_result(
    run_command: CommandRunner,
    command: tuple[str, ...],
    *,
    cwd: str | None = None,
) -> Mapping[str, Any]:
    _require(callable(run_command), "SCOUT_POST_RUN_COMMAND_RUNNER_REQUIRED")
    result = run_command(command, cwd=cwd)
    _require(
        isinstance(result, Mapping),
        "SCOUT_POST_RUN_COMMAND_RESULT_OBJECT_REQUIRED",
    )
    _require(
        set(result) == {"returncode", "stdout", "stderr"},
        "SCOUT_POST_RUN_COMMAND_RESULT_FIELDS_DRIFT",
    )
    _require(
        type(result["returncode"]) is int,
        "SCOUT_POST_RUN_COMMAND_RETURNCODE_INVALID",
    )
    _require(
        type(result["stdout"]) is str and type(result["stderr"]) is str,
        "SCOUT_POST_RUN_COMMAND_OUTPUT_TYPE_INVALID",
    )
    _require(
        len(result["stdout"].encode("utf-8")) <= MAX_STDOUT_BYTES,
        "SCOUT_POST_RUN_COMMAND_STDOUT_BOUND",
    )
    _require(
        len(result["stderr"].encode("utf-8")) <= MAX_STDERR_BYTES,
        "SCOUT_POST_RUN_COMMAND_STDERR_BOUND",
    )
    return result


def _validate_rootless_context(raw: str) -> None:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ScoutPostRunPrecisionHostBackendHold(
            "SCOUT_POST_RUN_DOCKER_CONTEXT_JSON_INVALID"
        ) from error
    _require(
        isinstance(value, list) and len(value) == 1,
        "SCOUT_POST_RUN_DOCKER_CONTEXT_COUNT_DRIFT",
    )
    row = value[0]
    _require(
        isinstance(row, Mapping) and row.get("Name") == DOCKER_CONTEXT,
        "SCOUT_POST_RUN_DOCKER_CONTEXT_NAME_DRIFT",
    )
    endpoints = row.get("Endpoints")
    _require(
        isinstance(endpoints, Mapping),
        "SCOUT_POST_RUN_DOCKER_ENDPOINTS_MISSING",
    )
    docker_endpoint = endpoints.get("docker")
    _require(
        isinstance(docker_endpoint, Mapping)
        and docker_endpoint.get("Host") == EXPECTED_DOCKER_HOST
        and docker_endpoint.get("SkipTLSVerify") is False,
        "SCOUT_POST_RUN_DOCKER_ENDPOINT_DRIFT",
    )


class ScoutPostRunPrecisionHostBackend:
    """Five exact callbacks for observe_post_run_state."""

    def __init__(
        self,
        *,
        read_authority_check: Callable[[], bool],
        attempt_directory_fd: int,
        expected_attempt_directory_identity: tuple[int, int],
        expected_source_head: str,
        run_command: CommandRunner = host_readonly_command_runner,
    ):
        _require(
            callable(read_authority_check),
            "SCOUT_POST_RUN_AUTHORITY_CALLBACK_REQUIRED",
        )
        _require(
            type(attempt_directory_fd) is int and attempt_directory_fd >= 0,
            "SCOUT_POST_RUN_ATTEMPT_DIRECTORY_FD_INVALID",
        )
        _require(
            type(expected_attempt_directory_identity) is tuple
            and len(expected_attempt_directory_identity) == 2
            and all(type(value) is int and value > 0 for value in expected_attempt_directory_identity),
            "SCOUT_POST_RUN_ATTEMPT_DIRECTORY_IDENTITY_INVALID",
        )
        _require(
            _valid_sha40(expected_source_head),
            "SCOUT_POST_RUN_EXPECTED_SOURCE_HEAD_INVALID",
        )
        _require(
            callable(run_command),
            "SCOUT_POST_RUN_COMMAND_RUNNER_REQUIRED",
        )
        self._authority_check = read_authority_check
        self._attempt_directory_fd = attempt_directory_fd
        self._attempt_directory_identity = expected_attempt_directory_identity
        self._expected_source_head = expected_source_head
        self._run_command = run_command

    def _authority(self) -> None:
        try:
            allowed = self._authority_check()
        except Exception as error:
            raise ScoutPostRunPrecisionHostBackendHold(
                f"SCOUT_POST_RUN_AUTHORITY_ERROR:{type(error).__name__}"
            ) from None
        _require(
            allowed is True,
            "SCOUT_POST_RUN_READ_AUTHORITY_REQUIRED",
        )

    def _attempt_directory(self) -> os.stat_result:
        current = os.fstat(self._attempt_directory_fd)
        _require(
            stat.S_ISDIR(current.st_mode)
            and (int(current.st_dev), int(current.st_ino))
            == self._attempt_directory_identity,
            "SCOUT_POST_RUN_ATTEMPT_DIRECTORY_CHANGED",
        )
        return current

    def attempt_marker_present(self) -> bool:
        self._authority()
        self._attempt_directory()
        try:
            marker = os.stat(
                attempt_guard.MARKER_NAME,
                dir_fd=self._attempt_directory_fd,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            return False
        except OSError as error:
            raise ScoutPostRunPrecisionHostBackendHold(
                f"SCOUT_POST_RUN_ATTEMPT_MARKER_STAT_ERROR:{type(error).__name__}"
            ) from None
        self._attempt_directory()
        _require(
            stat.S_ISREG(marker.st_mode)
            and marker.st_nlink == 1
            and marker.st_uid == os.geteuid()
            and stat.S_IMODE(marker.st_mode) == 0o600
            and 0 < marker.st_size <= attempt_guard.MAX_MARKER_BYTES,
            "SCOUT_POST_RUN_ATTEMPT_MARKER_METADATA_HOLD",
        )
        return True

    def runtime_service_inactive(self) -> bool:
        self._authority()
        active = _command_result(
            self._run_command,
            SYSTEMCTL_ACTIVE,
        )
        enabled = _command_result(
            self._run_command,
            SYSTEMCTL_ENABLED,
        )
        active_text = active["stdout"].strip()
        enabled_text = enabled["stdout"].strip()
        _require(
            active["returncode"] in {0, 3, 4}
            and enabled["returncode"] in {0, 1, 3, 4},
            "SCOUT_POST_RUN_SYSTEMD_RETURNCODE_UNEXPECTED",
        )
        return active_text == "inactive" and enabled_text == "disabled"

    def engine_container_absent(self) -> bool:
        self._authority()
        context = _command_result(
            self._run_command,
            DOCKER_CONTEXT_INSPECT,
        )
        _require(
            context["returncode"] == 0,
            "SCOUT_POST_RUN_DOCKER_CONTEXT_COMMAND_FAILED",
        )
        _validate_rootless_context(context["stdout"])

        containers = _command_result(
            self._run_command,
            DOCKER_CONTAINER_LIST,
        )
        _require(
            containers["returncode"] == 0,
            "SCOUT_POST_RUN_DOCKER_CONTAINER_LIST_FAILED",
        )
        names = []
        for line in containers["stdout"].splitlines():
            name = line.strip()
            if not name:
                continue
            _require(
                len(name) <= 255
                and all(character.isalnum() or character in "_.-" for character in name),
                "SCOUT_POST_RUN_DOCKER_CONTAINER_NAME_INVALID",
            )
            names.append(name)
        return not any(name.startswith(CANARY_CONTAINER_PREFIX) for name in names)

    def model_process_absent(self) -> bool:
        self._authority()
        result = _command_result(
            self._run_command,
            PGREP_OLLAMA,
        )
        if result["returncode"] == 1 and result["stdout"].strip() == "":
            return True
        if result["returncode"] == 0:
            rows = [row.strip() for row in result["stdout"].splitlines() if row.strip()]
            _require(
                all(row.isdigit() for row in rows),
                "SCOUT_POST_RUN_PGREP_OUTPUT_INVALID",
            )
            return len(rows) == 0
        raise ScoutPostRunPrecisionHostBackendHold(
            "SCOUT_POST_RUN_PGREP_RETURNCODE_UNEXPECTED"
        )

    def source_checkout_clean(self) -> bool:
        self._authority()
        head = _command_result(
            self._run_command,
            GIT_HEAD,
            cwd=EXPECTED_REPO_ROOT,
        )
        status_result = _command_result(
            self._run_command,
            GIT_STATUS,
            cwd=EXPECTED_REPO_ROOT,
        )
        _require(
            head["returncode"] == 0 and status_result["returncode"] == 0,
            "SCOUT_POST_RUN_GIT_COMMAND_FAILED",
        )
        return (
            head["stdout"].strip() == self._expected_source_head
            and status_result["stdout"] == ""
        )

    def probes(self) -> dict[str, Callable[[], bool]]:
        probes = {
            "attempt_marker_present": self.attempt_marker_present,
            "runtime_service_inactive": self.runtime_service_inactive,
            "engine_container_absent": self.engine_container_absent,
            "model_process_absent": self.model_process_absent,
            "source_checkout_clean": self.source_checkout_clean,
        }
        _require(
            set(probes) == set(observer.REQUIRED_OBSERVATIONS),
            "SCOUT_POST_RUN_PROBE_SET_DRIFT",
        )
        return probes


def observe_post_run_with_precision_backend(
    *,
    experiment_id: str,
    attempt_marker_sha256: str,
    expected_source_head: str,
    attempt_directory_fd: int,
    expected_attempt_directory_identity: tuple[int, int],
    read_authority_check: Callable[[], bool],
    run_command: CommandRunner = host_readonly_command_runner,
) -> bytes:
    """Compose the existing observer with this exact backend; never automatic."""
    backend = ScoutPostRunPrecisionHostBackend(
        read_authority_check=read_authority_check,
        attempt_directory_fd=attempt_directory_fd,
        expected_attempt_directory_identity=expected_attempt_directory_identity,
        expected_source_head=expected_source_head,
        run_command=run_command,
    )
    return observer.observe_post_run_state(
        experiment_id=experiment_id,
        attempt_marker_sha256=attempt_marker_sha256,
        observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
        read_authority_check=read_authority_check,
        probes=backend.probes(),
    )


def precision_post_run_backend_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "expected_host": EXPECTED_HOST,
        "expected_repo_root": EXPECTED_REPO_ROOT,
        "system_service": OLLAMA_SERVICE,
        "service_scope": "system",
        "docker_context": DOCKER_CONTEXT,
        "docker_host": EXPECTED_DOCKER_HOST,
        "canary_container_prefix": CANARY_CONTAINER_PREFIX,
        "attempt_marker_name": attempt_guard.MARKER_NAME,
        "required_observations": observer.REQUIRED_OBSERVATIONS,
        "allowed_commands": tuple(sorted(FIXED_COMMANDS)),
        "command_timeout_seconds": COMMAND_TIMEOUT_SECONDS,
        "maximum_stdout_bytes": MAX_STDOUT_BYTES,
        "maximum_stderr_bytes": MAX_STDERR_BYTES,
        "shell_execution_implemented": False,
        "attempt_marker_content_read_implemented": False,
        "service_mutation_implemented": False,
        "container_mutation_implemented": False,
        "git_mutation_implemented": False,
        "model_http_request_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "automatic_retry_implemented": False,
        "observation_requires_explicit_authority": True,
        "automatic_backend_invocation": False,
        "execution_authority_created": False,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunPrecisionHostBackendHold(
        "SCOUT_POST_RUN_BACKEND_OBSERVATION_ONLY"
    )
