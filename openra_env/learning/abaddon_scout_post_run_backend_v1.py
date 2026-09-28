"""Concrete dormant read-only backend for scout post-run evidence.

This module closes the host-mechanism gap behind
abaddon_scout_post_run_observer_v1 without creating scout execution authority.
Nothing runs on import.

A future separately authorized launcher may explicitly compose this backend with
the already-reviewed observer adapter. The backend then proves five post-run
facts independently of runner cleanup prints:

* the exact durable attempt marker still exists and matches its SHA-256;
* ollama.service is exactly inactive;
* the exact canary engine container name is absent from rootless Docker;
* no process named ollama exists;
* the exact War College and OpenRA tracked checkouts are clean and at the
  caller-admitted War College commit / reviewed engine commit.

All host operations are read-only. No command capable of start/stop/restart,
container removal, process signaling, checkout mutation, model execution,
training, deployment, VOID-chain mutation, or funds action is accepted.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Any, Callable, Mapping, Protocol, Sequence

from openra_env.learning import abaddon_scout_external_attempt_guard_v1 as attempt_guard
from openra_env.learning import abaddon_scout_post_run_observer_v1 as observer


CONTRACT_SCHEMA = "void.abaddon.scout-post-run-readonly-backend-contract.v1"

SOURCE_ROOT = "/home/zoso/dev/openra-rl-war-college"
ENGINE_ROOT = SOURCE_ROOT + "/OpenRA"
EXPECTED_ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
SCOUT_DERIVED_RUNNER_GIT_BLOB = "40030e2ee61d17fd94abd1df733d3ea22650512b"

SERVICE_UNIT = "ollama.service"
MODEL_PROCESS_NAME = "ollama"
CONTAINER_PREFIX = "void-scout-repair-canary-"
DOCKER_CONTEXT = "rootless"
EXPECTED_DOCKER_CONTEXT_HOST = "unix:///run/user/1000/docker.sock"
EXPECTED_DOCKER_ROOT_DIR = "/home/zoso/.local/share/docker"

GIT = "/usr/bin/git"
SYSTEMCTL = "/usr/bin/systemctl"
PGREP = "/usr/bin/pgrep"
DOCKER = "/usr/bin/docker"

COMMAND_TIMEOUT_SECONDS = 5.0
MAX_STDOUT_BYTES = 1024 * 1024
MAX_STDERR_BYTES = 64 * 1024

SOURCE_HEAD_COMMAND = (GIT, "-C", SOURCE_ROOT, "rev-parse", "HEAD")
SOURCE_STATUS_COMMAND = (
    GIT,
    "-C",
    SOURCE_ROOT,
    "status",
    "--porcelain",
    "--untracked-files=all",
)
ENGINE_HEAD_COMMAND = (GIT, "-C", ENGINE_ROOT, "rev-parse", "HEAD")
ENGINE_STATUS_COMMAND = (
    GIT,
    "-C",
    ENGINE_ROOT,
    "status",
    "--porcelain",
    "--untracked-files=all",
)
SERVICE_INACTIVE_COMMAND = (SYSTEMCTL, "is-active", SERVICE_UNIT)
MODEL_PROCESS_COMMAND = (PGREP, "-x", MODEL_PROCESS_NAME)
DOCKER_CONTEXT_INSPECT_COMMAND = (
    DOCKER,
    "context",
    "inspect",
    DOCKER_CONTEXT,
)
DOCKER_INFO_COMMAND = (
    DOCKER,
    "--host",
    EXPECTED_DOCKER_CONTEXT_HOST,
    "info",
    "--format",
    "{{json .}}",
)

STATIC_ALLOWED_COMMANDS = frozenset(
    (
        SOURCE_HEAD_COMMAND,
        SOURCE_STATUS_COMMAND,
        ENGINE_HEAD_COMMAND,
        ENGINE_STATUS_COMMAND,
        SERVICE_INACTIVE_COMMAND,
        MODEL_PROCESS_COMMAND,
        DOCKER_CONTEXT_INSPECT_COMMAND,
        DOCKER_INFO_COMMAND,
    )
)

FORBIDDEN_COMMAND_TOKENS = frozenset(
    (
        "start",
        "stop",
        "restart",
        "reload",
        "enable",
        "disable",
        "kill",
        "pkill",
        "rm",
        "remove",
        "run",
        "exec",
        "create",
        "checkout",
        "switch",
        "reset",
        "clean",
        "pull",
        "fetch",
        "merge",
        "rebase",
        "commit",
        "push",
        "load",
    )
)

NEXT_GATE = "SCOUT_POST_RUN_BACKEND_SOURCE_BINDING_REVIEW_REQUIRED"


class ScoutPostRunBackendHold(RuntimeError):
    """A required independent post-run observation was unavailable or negative."""


class CommandRunner(Protocol):
    def __call__(self, args: Sequence[str]) -> Mapping[str, Any]:
        ...


class PathLstat(Protocol):
    def __call__(self, path: str) -> Any:
        ...


class PathResolver(Protocol):
    def __call__(self, path: str) -> str:
        ...


@dataclass(frozen=True)
class FileBackend:
    open_file: Callable[[str, int], int]
    fstat: Callable[[int], Any]
    read: Callable[[int, int], bytes]
    close: Callable[[int], None]


@dataclass(frozen=True)
class ScoutPostRunBackendInputs:
    experiment_id: str
    attempt_marker_path: str
    attempt_marker_sha256: str
    attempt_directory_identity: tuple[int, int]
    engine_container_name: str
    accepted_war_college_commit: str


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutPostRunBackendHold(code)


def _is_hex(value: Any, length: int) -> bool:
    return (
        type(value) is str
        and len(value) == length
        and all(char in "0123456789abcdef" for char in value)
    )


def _valid_experiment_id(value: Any) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= 128
        and value.startswith("abaddon-scout-")
        and "pair03" not in value
        and all(
            char in "abcdefghijklmnopqrstuvwxyz0123456789._-"
            for char in value
        )
    )


def _valid_container_name(value: Any) -> bool:
    if type(value) is not str or not value.startswith(CONTAINER_PREFIX):
        return False
    suffix = value[len(CONTAINER_PREFIX):]
    return bool(suffix) and suffix.isdigit() and int(suffix) > 0


def _container_absence_command(container_name: str) -> tuple[str, ...]:
    _require(_valid_container_name(container_name), "SCOUT_BACKEND_CONTAINER_NAME_INVALID")
    return (
        DOCKER,
        "--host",
        EXPECTED_DOCKER_CONTEXT_HOST,
        "ps",
        "-a",
        "--filter",
        f"name=^/{container_name}$",
        "--format",
        "{{.Names}}",
    )


def _validate_inputs(inputs: ScoutPostRunBackendInputs) -> ScoutPostRunBackendInputs:
    _require(
        isinstance(inputs, ScoutPostRunBackendInputs),
        "SCOUT_BACKEND_INPUTS_REQUIRED",
    )
    _require(
        _valid_experiment_id(inputs.experiment_id),
        "SCOUT_BACKEND_EXPERIMENT_ID_INVALID",
    )
    _require(
        _is_hex(inputs.attempt_marker_sha256, 64),
        "SCOUT_BACKEND_ATTEMPT_SHA256_INVALID",
    )
    _require(
        type(inputs.attempt_directory_identity) is tuple
        and len(inputs.attempt_directory_identity) == 2
        and all(
            type(value) is int and value >= 0
            for value in inputs.attempt_directory_identity
        ),
        "SCOUT_BACKEND_ATTEMPT_DIRECTORY_IDENTITY_INVALID",
    )
    _require(
        _is_hex(inputs.accepted_war_college_commit, 40),
        "SCOUT_BACKEND_WAR_COLLEGE_COMMIT_INVALID",
    )
    _require(
        _valid_container_name(inputs.engine_container_name),
        "SCOUT_BACKEND_CONTAINER_NAME_INVALID",
    )
    marker = Path(inputs.attempt_marker_path)
    _require(marker.is_absolute(), "SCOUT_BACKEND_MARKER_PATH_NOT_ABSOLUTE")
    _require(
        marker.name == attempt_guard.MARKER_NAME,
        "SCOUT_BACKEND_MARKER_NAME_DRIFT",
    )
    return inputs


def _validate_command(args: Sequence[str]) -> tuple[str, ...]:
    _require(
        isinstance(args, (tuple, list)),
        "SCOUT_BACKEND_COMMAND_SEQUENCE_REQUIRED",
    )
    command = tuple(args)
    if command in STATIC_ALLOWED_COMMANDS:
        return command

    _require(
        len(command) == 9
        and command[0:6]
        == (
            DOCKER,
            "--host",
            EXPECTED_DOCKER_CONTEXT_HOST,
            "ps",
            "-a",
            "--filter",
        )
        and command[7:] == ("--format", "{{.Names}}"),
        "SCOUT_BACKEND_COMMAND_NOT_REVIEWED",
    )
    prefix = "name=^/" + CONTAINER_PREFIX
    _require(
        command[6].startswith(prefix) and command[6].endswith("$"),
        "SCOUT_BACKEND_DOCKER_FILTER_DRIFT",
    )
    container = command[6][len("name=^/"):-1]
    _require(
        _valid_container_name(container),
        "SCOUT_BACKEND_CONTAINER_NAME_INVALID",
    )
    return command


def host_readonly_command_runner(args: Sequence[str]) -> dict[str, Any]:
    """Run one reviewed read-only command; never selected automatically."""
    command = _validate_command(args)
    lowered = {part.lower() for part in command[1:]}
    _require(
        lowered.isdisjoint(FORBIDDEN_COMMAND_TOKENS),
        "SCOUT_BACKEND_MUTATING_COMMAND_TOKEN_FORBIDDEN",
    )
    try:
        completed = subprocess.run(
            list(command),
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
                "GIT_OPTIONAL_LOCKS": "0",
            },
        )
    except subprocess.TimeoutExpired:
        raise ScoutPostRunBackendHold("SCOUT_BACKEND_COMMAND_TIMEOUT") from None

    _require(
        len(completed.stdout.encode("utf-8", errors="replace")) <= MAX_STDOUT_BYTES,
        "SCOUT_BACKEND_STDOUT_EXCEEDS_BOUND",
    )
    _require(
        len(completed.stderr.encode("utf-8", errors="replace")) <= MAX_STDERR_BYTES,
        "SCOUT_BACKEND_STDERR_EXCEEDS_BOUND",
    )
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def host_file_backend() -> FileBackend:
    """Construct the real read-only file backend without performing I/O."""
    return FileBackend(
        open_file=lambda path, flags: os.open(path, flags),
        fstat=os.fstat,
        read=os.read,
        close=os.close,
    )


def host_lstat_path(path: str) -> Any:
    return os.lstat(path)


def host_resolve_path(path: str) -> str:
    return str(Path(path).resolve(strict=True))


def _command_result(
    run_command: CommandRunner,
    command: tuple[str, ...],
    *,
    label: str,
    allowed_returncodes: frozenset[int],
) -> Mapping[str, Any]:
    _require(callable(run_command), f"{label}:COMMAND_RUNNER_REQUIRED")
    result = run_command(command)
    _require(isinstance(result, Mapping), f"{label}:COMMAND_RESULT_INVALID")
    _require(
        set(result) == {"returncode", "stdout", "stderr"},
        f"{label}:COMMAND_RESULT_FIELD_DRIFT",
    )
    _require(type(result["returncode"]) is int, f"{label}:RETURN_CODE_INVALID")
    _require(type(result["stdout"]) is str, f"{label}:STDOUT_INVALID")
    _require(type(result["stderr"]) is str, f"{label}:STDERR_INVALID")
    _require(
        result["returncode"] in allowed_returncodes,
        f"{label}:COMMAND_FAILED",
    )
    _require(
        len(result["stdout"].encode("utf-8", errors="replace")) <= MAX_STDOUT_BYTES,
        f"{label}:STDOUT_EXCEEDS_BOUND",
    )
    _require(
        len(result["stderr"].encode("utf-8", errors="replace")) <= MAX_STDERR_BYTES,
        f"{label}:STDERR_EXCEEDS_BOUND",
    )
    return result


def _directory_identity(value: Any) -> tuple[int, ...]:
    return (
        int(value.st_dev),
        int(value.st_ino),
        int(value.st_mode),
        int(value.st_nlink),
        int(value.st_uid),
        int(value.st_size),
        int(value.st_mtime_ns),
        int(value.st_ctime_ns),
    )


def _file_identity(value: Any) -> tuple[int, ...]:
    return _directory_identity(value)


def _observe_directory(
    path: str,
    *,
    lstat_path: PathLstat,
    resolve_path: PathResolver,
    label: str,
) -> tuple[int, ...]:
    _require(callable(lstat_path), f"{label}:LSTAT_BACKEND_REQUIRED")
    _require(callable(resolve_path), f"{label}:RESOLVER_REQUIRED")
    _require(resolve_path(path) == path, f"{label}:PATH_IDENTITY_DRIFT")
    value = lstat_path(path)
    _require(stat.S_ISDIR(value.st_mode), f"{label}:NOT_DIRECTORY")
    _require(not stat.S_ISLNK(value.st_mode), f"{label}:SYMLINK_FORBIDDEN")
    _require(value.st_nlink > 0, f"{label}:LINK_COUNT_INVALID")
    _require(value.st_uid == os.geteuid(), f"{label}:OWNER_DRIFT")
    return _directory_identity(value)


def probe_attempt_marker_present(
    inputs: ScoutPostRunBackendInputs,
    *,
    file_backend: FileBackend,
    lstat_path: PathLstat,
    resolve_path: PathResolver,
) -> bool:
    """Prove the exact create-only marker still exists and is unchanged."""
    _validate_inputs(inputs)
    _require(isinstance(file_backend, FileBackend), "SCOUT_BACKEND_FILE_BACKEND_REQUIRED")
    marker = Path(inputs.attempt_marker_path)
    parent = str(marker.parent)

    before_parent = _observe_directory(
        parent,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
        label="SCOUT_MARKER_PARENT",
    )
    parent_stat = lstat_path(parent)
    _require(
        (int(parent_stat.st_dev), int(parent_stat.st_ino))
        == inputs.attempt_directory_identity,
        "SCOUT_MARKER_PARENT_IDENTITY_DRIFT",
    )
    _require(
        stat.S_IMODE(parent_stat.st_mode) == 0o700,
        "SCOUT_MARKER_PARENT_MODE_DRIFT",
    )

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    try:
        fd = file_backend.open_file(str(marker), flags)
    except OSError as exc:
        raise ScoutPostRunBackendHold(
            f"SCOUT_MARKER_OPEN_FAILED:{type(exc).__name__}"
        ) from None

    try:
        before = file_backend.fstat(fd)
        _require(stat.S_ISREG(before.st_mode), "SCOUT_MARKER_NOT_REGULAR")
        _require(before.st_nlink == 1, "SCOUT_MARKER_LINK_COUNT_DRIFT")
        _require(before.st_uid == os.geteuid(), "SCOUT_MARKER_OWNER_DRIFT")
        _require(stat.S_IMODE(before.st_mode) == 0o600, "SCOUT_MARKER_MODE_DRIFT")
        _require(
            0 < before.st_size <= attempt_guard.MAX_MARKER_BYTES,
            "SCOUT_MARKER_SIZE_DRIFT",
        )

        raw = bytearray()
        while len(raw) <= attempt_guard.MAX_MARKER_BYTES:
            chunk = file_backend.read(
                fd,
                min(4096, attempt_guard.MAX_MARKER_BYTES + 1 - len(raw)),
            )
            _require(isinstance(chunk, bytes), "SCOUT_MARKER_READ_TYPE")
            if not chunk:
                break
            raw.extend(chunk)
        _require(
            0 < len(raw) <= attempt_guard.MAX_MARKER_BYTES,
            "SCOUT_MARKER_READ_BOUND",
        )

        after = file_backend.fstat(fd)
        _require(
            _file_identity(before) == _file_identity(after),
            "SCOUT_MARKER_GENERATION_CHANGED",
        )
    finally:
        file_backend.close(fd)

    after_parent = _observe_directory(
        parent,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
        label="SCOUT_MARKER_PARENT",
    )
    _require(
        before_parent == after_parent,
        "SCOUT_MARKER_PARENT_GENERATION_CHANGED",
    )

    raw_bytes = bytes(raw)
    _require(
        hashlib.sha256(raw_bytes).hexdigest() == inputs.attempt_marker_sha256,
        "SCOUT_MARKER_SHA256_DRIFT",
    )
    try:
        record = json.loads(raw_bytes.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ScoutPostRunBackendHold("SCOUT_MARKER_JSON_INVALID") from None
    _require(type(record) is dict, "SCOUT_MARKER_OBJECT_REQUIRED")
    _require(record.get("schema") == attempt_guard.SCHEMA, "SCOUT_MARKER_SCHEMA_DRIFT")
    _require(
        record.get("record_kind") == "attempt_consumed_not_execution_evidence",
        "SCOUT_MARKER_RECORD_KIND_DRIFT",
    )
    _require(
        record.get("experiment_id") == inputs.experiment_id,
        "SCOUT_MARKER_EXPERIMENT_ID_DRIFT",
    )
    _require(record.get("single_use_scope") is True, "SCOUT_MARKER_SINGLE_USE_DRIFT")
    for field in (
        "pair03_attempt_reused",
        "pair03_attempt_reset",
        "scout_execution_authorized",
        "scout_execution_performed",
        "reusable_execution_permit",
        "automatic_retry",
        "training_authorized",
        "automatic_policy_promotion",
    ):
        _require(record.get(field) is False, "SCOUT_MARKER_BOUNDARY_DRIFT:" + field)
    return True


def probe_runtime_service_inactive(
    *,
    run_command: CommandRunner,
) -> bool:
    result = _command_result(
        run_command,
        SERVICE_INACTIVE_COMMAND,
        label="SCOUT_SERVICE_INACTIVE",
        allowed_returncodes=frozenset((3,)),
    )
    _require(
        result["stdout"].strip() == "inactive",
        "SCOUT_SERVICE_NOT_INACTIVE",
    )
    return True


def _validate_rootless_context_mapping(
    *,
    run_command: CommandRunner,
) -> None:
    context_result = _command_result(
        run_command,
        DOCKER_CONTEXT_INSPECT_COMMAND,
        label="SCOUT_DOCKER_CONTEXT",
        allowed_returncodes=frozenset((0,)),
    )
    try:
        context_rows = json.loads(context_result["stdout"])
    except json.JSONDecodeError:
        raise ScoutPostRunBackendHold("SCOUT_DOCKER_CONTEXT_JSON_INVALID") from None
    _require(
        isinstance(context_rows, list) and len(context_rows) == 1,
        "SCOUT_DOCKER_CONTEXT_COUNT_DRIFT",
    )
    context = context_rows[0]
    _require(isinstance(context, Mapping), "SCOUT_DOCKER_CONTEXT_ROW_INVALID")
    _require(
        context.get("Name") == DOCKER_CONTEXT,
        "SCOUT_DOCKER_CONTEXT_NAME_DRIFT",
    )
    endpoints = context.get("Endpoints")
    _require(isinstance(endpoints, Mapping), "SCOUT_DOCKER_ENDPOINTS_MISSING")
    docker_endpoint = endpoints.get("docker")
    _require(
        isinstance(docker_endpoint, Mapping),
        "SCOUT_DOCKER_ENDPOINT_MISSING",
    )
    _require(
        docker_endpoint.get("Host") == EXPECTED_DOCKER_CONTEXT_HOST,
        "SCOUT_DOCKER_CONTEXT_HOST_DRIFT",
    )
    _require(
        docker_endpoint.get("SkipTLSVerify") is False,
        "SCOUT_DOCKER_CONTEXT_TLS_DRIFT",
    )


def _observe_rootless_docker_daemon_identity(
    *,
    run_command: CommandRunner,
) -> tuple[str, str, str]:
    info_result = _command_result(
        run_command,
        DOCKER_INFO_COMMAND,
        label="SCOUT_DOCKER_INFO",
        allowed_returncodes=frozenset((0,)),
    )
    try:
        info = json.loads(info_result["stdout"])
    except json.JSONDecodeError:
        raise ScoutPostRunBackendHold("SCOUT_DOCKER_INFO_JSON_INVALID") from None
    _require(isinstance(info, Mapping), "SCOUT_DOCKER_INFO_OBJECT_REQUIRED")
    security = info.get("SecurityOptions")
    _require(isinstance(security, list), "SCOUT_DOCKER_SECURITY_OPTIONS_MISSING")
    _require("name=rootless" in security, "SCOUT_DOCKER_NOT_ROOTLESS")
    _require(
        info.get("DockerRootDir") == EXPECTED_DOCKER_ROOT_DIR,
        "SCOUT_DOCKER_ROOT_DIR_DRIFT",
    )
    _require(info.get("OSType") == "linux", "SCOUT_DOCKER_OS_TYPE_DRIFT")
    daemon_id = info.get("ID")
    daemon_name = info.get("Name")
    _require(
        type(daemon_id) is str and 1 <= len(daemon_id) <= 256,
        "SCOUT_DOCKER_DAEMON_ID_MISSING",
    )
    _require(
        type(daemon_name) is str and 1 <= len(daemon_name) <= 256,
        "SCOUT_DOCKER_DAEMON_NAME_MISSING",
    )
    return daemon_id, daemon_name, EXPECTED_DOCKER_ROOT_DIR


def probe_engine_container_absent(
    inputs: ScoutPostRunBackendInputs,
    *,
    run_command: CommandRunner,
) -> bool:
    _validate_inputs(inputs)
    _validate_rootless_context_mapping(run_command=run_command)
    before_daemon = _observe_rootless_docker_daemon_identity(
        run_command=run_command
    )
    result = _command_result(
        run_command,
        _container_absence_command(inputs.engine_container_name),
        label="SCOUT_ENGINE_CONTAINER_ABSENT",
        allowed_returncodes=frozenset((0,)),
    )
    after_daemon = _observe_rootless_docker_daemon_identity(
        run_command=run_command
    )
    _require(
        before_daemon == after_daemon,
        "SCOUT_DOCKER_DAEMON_IDENTITY_CHANGED",
    )
    _require(
        result["stdout"].strip() == "",
        "SCOUT_ENGINE_CONTAINER_STILL_PRESENT",
    )
    return True

def probe_model_process_absent(
    *,
    run_command: CommandRunner,
) -> bool:
    result = _command_result(
        run_command,
        MODEL_PROCESS_COMMAND,
        label="SCOUT_MODEL_PROCESS_ABSENT",
        allowed_returncodes=frozenset((1,)),
    )
    _require(
        result["stdout"].strip() == "",
        "SCOUT_MODEL_PROCESS_STILL_PRESENT",
    )
    return True


def probe_source_checkout_clean(
    inputs: ScoutPostRunBackendInputs,
    *,
    run_command: CommandRunner,
    lstat_path: PathLstat,
    resolve_path: PathResolver,
) -> bool:
    _validate_inputs(inputs)
    source_before = _observe_directory(
        SOURCE_ROOT,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
        label="SCOUT_SOURCE_ROOT",
    )
    engine_before = _observe_directory(
        ENGINE_ROOT,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
        label="SCOUT_ENGINE_ROOT",
    )

    def observe_git_state() -> tuple[str, str, str, str]:
        source_head = _command_result(
            run_command,
            SOURCE_HEAD_COMMAND,
            label="SCOUT_SOURCE_HEAD",
            allowed_returncodes=frozenset((0,)),
        )["stdout"].strip()
        source_status = _command_result(
            run_command,
            SOURCE_STATUS_COMMAND,
            label="SCOUT_SOURCE_STATUS",
            allowed_returncodes=frozenset((0,)),
        )["stdout"]
        engine_head = _command_result(
            run_command,
            ENGINE_HEAD_COMMAND,
            label="SCOUT_ENGINE_HEAD",
            allowed_returncodes=frozenset((0,)),
        )["stdout"].strip()
        engine_status = _command_result(
            run_command,
            ENGINE_STATUS_COMMAND,
            label="SCOUT_ENGINE_STATUS",
            allowed_returncodes=frozenset((0,)),
        )["stdout"]
        return source_head, source_status, engine_head, engine_status

    first = observe_git_state()
    _require(
        first[0] == inputs.accepted_war_college_commit,
        "SCOUT_SOURCE_HEAD_DRIFT",
    )
    _require(first[1].strip() == "", "SCOUT_SOURCE_TRACKED_DIRTY")
    _require(first[2] == EXPECTED_ENGINE_COMMIT, "SCOUT_ENGINE_HEAD_DRIFT")
    _require(first[3].strip() == "", "SCOUT_ENGINE_TRACKED_DIRTY")

    second = observe_git_state()
    _require(first == second, "SCOUT_GIT_STATE_CHANGED_DURING_OBSERVATION")
    _require(
        second[0] == inputs.accepted_war_college_commit
        and second[1].strip() == ""
        and second[2] == EXPECTED_ENGINE_COMMIT
        and second[3].strip() == "",
        "SCOUT_GIT_FINAL_STATE_INVALID",
    )

    # The composite pass observes source before engine. Re-observe source after
    # the final engine commands so source changes during those commands cannot
    # be accepted as a clean post-run state.
    final_source_head = _command_result(
        run_command,
        SOURCE_HEAD_COMMAND,
        label="SCOUT_SOURCE_FINAL_HEAD",
        allowed_returncodes=frozenset((0,)),
    )["stdout"].strip()
    final_source_status = _command_result(
        run_command,
        SOURCE_STATUS_COMMAND,
        label="SCOUT_SOURCE_FINAL_STATUS",
        allowed_returncodes=frozenset((0,)),
    )["stdout"]
    _require(
        final_source_head == second[0]
        and final_source_status == second[1]
        and final_source_head == inputs.accepted_war_college_commit
        and final_source_status.strip() == "",
        "SCOUT_SOURCE_FINAL_RECHECK_DRIFT",
    )

    source_after = _observe_directory(
        SOURCE_ROOT,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
        label="SCOUT_SOURCE_ROOT",
    )
    engine_after = _observe_directory(
        ENGINE_ROOT,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
        label="SCOUT_ENGINE_ROOT",
    )
    _require(source_before == source_after, "SCOUT_SOURCE_GENERATION_CHANGED")
    _require(engine_before == engine_after, "SCOUT_ENGINE_GENERATION_CHANGED")
    return True


def build_scout_post_run_probes(
    inputs: ScoutPostRunBackendInputs,
    *,
    observation_authorized: bool,
    run_command: CommandRunner,
    file_backend: FileBackend,
    lstat_path: PathLstat,
    resolve_path: PathResolver,
) -> dict[str, Callable[[], bool]]:
    """Bind exact inputs to the five reviewed observer probes without running them."""
    _require(
        observation_authorized is True,
        "SCOUT_BACKEND_OBSERVATION_NOT_AUTHORIZED",
    )
    validated = _validate_inputs(inputs)
    _require(callable(run_command), "SCOUT_BACKEND_COMMAND_RUNNER_REQUIRED")
    _require(isinstance(file_backend, FileBackend), "SCOUT_BACKEND_FILE_BACKEND_REQUIRED")
    _require(callable(lstat_path), "SCOUT_BACKEND_LSTAT_REQUIRED")
    _require(callable(resolve_path), "SCOUT_BACKEND_RESOLVER_REQUIRED")

    return {
        "attempt_marker_present": lambda: probe_attempt_marker_present(
            validated,
            file_backend=file_backend,
            lstat_path=lstat_path,
            resolve_path=resolve_path,
        ),
        "runtime_service_inactive": lambda: probe_runtime_service_inactive(
            run_command=run_command
        ),
        "engine_container_absent": lambda: probe_engine_container_absent(
            validated,
            run_command=run_command,
        ),
        "model_process_absent": lambda: probe_model_process_absent(
            run_command=run_command
        ),
        "source_checkout_clean": lambda: probe_source_checkout_clean(
            validated,
            run_command=run_command,
            lstat_path=lstat_path,
            resolve_path=resolve_path,
        ),
    }


def collect_bound_scout_post_run_evidence(
    inputs: ScoutPostRunBackendInputs,
    *,
    observation_authorized: bool,
    read_authority_check: Callable[[], bool],
    run_command: CommandRunner,
    file_backend: FileBackend,
    lstat_path: PathLstat,
    resolve_path: PathResolver,
) -> bytes:
    """Compose the concrete backend with the existing fail-closed observer adapter."""
    probes = build_scout_post_run_probes(
        inputs,
        observation_authorized=observation_authorized,
        run_command=run_command,
        file_backend=file_backend,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
    )
    return observer.observe_post_run_state(
        experiment_id=inputs.experiment_id,
        attempt_marker_sha256=inputs.attempt_marker_sha256,
        observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
        read_authority_check=read_authority_check,
        probes=probes,
    )


def scout_post_run_backend_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "observer_implementation_git_blob": "11dfa40a861e6772258178bbc32840c670e47f9f",
        "attempt_guard_git_blob": "043225a7ff6528b9ae7f80994fe17480ad36ed3e",
        "derived_canary_runner_git_blob": SCOUT_DERIVED_RUNNER_GIT_BLOB,
        "source_root": SOURCE_ROOT,
        "engine_root": ENGINE_ROOT,
        "expected_engine_commit": EXPECTED_ENGINE_COMMIT,
        "service_unit": SERVICE_UNIT,
        "model_process_name": MODEL_PROCESS_NAME,
        "engine_container_prefix": CONTAINER_PREFIX,
        "docker_context": DOCKER_CONTEXT,
        "expected_docker_context_host": EXPECTED_DOCKER_CONTEXT_HOST,
        "expected_docker_root_dir": EXPECTED_DOCKER_ROOT_DIR,
        "required_observations": list(observer.REQUIRED_OBSERVATIONS),
        "attempt_marker_exact_sha_required": True,
        "attempt_marker_directory_identity_required": True,
        "attempt_marker_no_follow_required": True,
        "attempt_marker_private_mode_required": True,
        "service_inactive_query_implemented": True,
        "container_absence_query_implemented": True,
        "rootless_docker_identity_verified_before_container_absence": True,
        "container_absence_uses_verified_socket_directly": True,
        "docker_daemon_identity_rechecked_after_container_absence": True,
        "model_process_absence_query_implemented": True,
        "source_and_engine_git_observation_implemented": True,
        "git_optional_locks_disabled": True,
        "source_directory_generation_stability_required": True,
        "engine_directory_generation_stability_required": True,
        "git_state_double_observation_required": True,
        "source_final_recheck_after_engine_required": True,
        "host_command_runner_present": True,
        "host_file_backend_factory_present": True,
        "host_path_helpers_present": True,
        "automatic_host_backend_selection": False,
        "observation_requires_explicit_authority": True,
        "backend_source_binding_present": False,
        "host_observation_performed": False,
        "post_run_state_verified": False,
        "result_evidence_verified": False,
        "scout_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunBackendHold("SCOUT_BACKEND_EXECUTION_AUTHORITY_UNAVAILABLE")
