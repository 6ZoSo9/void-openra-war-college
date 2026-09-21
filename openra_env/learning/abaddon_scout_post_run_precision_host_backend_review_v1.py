"""Source binding review for the Precision scout post-run host backend.

The review accepts exact source bytes only. It does not import the backend,
execute a command, inspect the host, read an attempt marker, or grant execution
authority.
"""

from __future__ import annotations

import ast
import hashlib
from typing import Any


SCHEMA = "void.abaddon.scout-post-run-precision-host-backend-review.v1"

BACKEND_PATH = (
    "openra_env/learning/abaddon_scout_post_run_precision_host_backend_v1.py"
)
BACKEND_GIT_BLOB = "503f1f9a9b0d30e7ab9e1226cb8e146699cfe4e0"

OBSERVER_PATH = "openra_env/learning/abaddon_scout_post_run_observer_v1.py"
OBSERVER_GIT_BLOB = "11dfa40a861e6772258178bbc32840c670e47f9f"

ATTEMPT_GUARD_PATH = (
    "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py"
)
ATTEMPT_GUARD_GIT_BLOB = "043225a7ff6528b9ae7f80994fe17480ad36ed3e"

NEXT_GATE = "SCOUT_POST_RUN_PRECISION_HOST_BACKEND_LIVE_QUALIFICATION_REQUIRED"


class ScoutPostRunPrecisionHostBackendReviewHold(ValueError):
    pass


def _require(value: bool, code: str) -> None:
    if not value:
        raise ScoutPostRunPrecisionHostBackendReviewHold(code)


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def _decode(raw: bytes, label: str) -> str:
    _require(type(raw) is bytes and len(raw) > 0, f"{label}_bytes_required")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ScoutPostRunPrecisionHostBackendReviewHold(
            f"{label}_utf8_required"
        ) from error


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def review_precision_host_backend_source(
    *,
    backend_bytes: bytes,
    observer_bytes: bytes,
    attempt_guard_bytes: bytes,
) -> dict[str, Any]:
    backend_source = _decode(backend_bytes, "backend")
    observer_source = _decode(observer_bytes, "observer")
    attempt_source = _decode(attempt_guard_bytes, "attempt_guard")

    _require(
        _git_blob(backend_bytes) == BACKEND_GIT_BLOB,
        "SCOUT_POST_RUN_BACKEND_SOURCE_DRIFT",
    )
    _require(
        _git_blob(observer_bytes) == OBSERVER_GIT_BLOB,
        "SCOUT_POST_RUN_OBSERVER_SOURCE_DRIFT",
    )
    _require(
        _git_blob(attempt_guard_bytes) == ATTEMPT_GUARD_GIT_BLOB,
        "SCOUT_POST_RUN_ATTEMPT_GUARD_SOURCE_DRIFT",
    )

    try:
        tree = ast.parse(backend_source, filename=BACKEND_PATH)
        ast.parse(observer_source, filename=OBSERVER_PATH)
        ast.parse(attempt_source, filename=ATTEMPT_GUARD_PATH)
    except SyntaxError as error:
        raise ScoutPostRunPrecisionHostBackendReviewHold(
            "SCOUT_POST_RUN_REVIEWED_SOURCE_SYNTAX_INVALID"
        ) from error

    subprocess_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _call_name(node.func) == "subprocess.run"
    ]
    _require(
        len(subprocess_calls) == 1,
        "SCOUT_POST_RUN_SUBPROCESS_CALL_SHAPE_DRIFT",
    )
    for keyword in subprocess_calls[0].keywords:
        _require(
            keyword.arg != "shell",
            "SCOUT_POST_RUN_SHELL_EXECUTION_FORBIDDEN",
        )

    _require(
        "os.stat(" in backend_source
        and "dir_fd=self._attempt_directory_fd" in backend_source
        and "follow_symlinks=False" in backend_source,
        "SCOUT_POST_RUN_ATTEMPT_METADATA_PROBE_DRIFT",
    )
    _require(
        "open(attempt_guard.MARKER_NAME" not in backend_source,
        "SCOUT_POST_RUN_ATTEMPT_CONTENT_OPEN_FORBIDDEN",
    )
    _require(
        'OLLAMA_SERVICE = "ollama.service"' in backend_source
        and 'EXPECTED_HOST = "zoso-Precision-Tower-7810"' in backend_source,
        "SCOUT_POST_RUN_PRECISION_SYSTEM_IDENTITY_DRIFT",
    )
    _require(
        'DOCKER_CONTEXT = "rootless"' in backend_source
        and 'EXPECTED_DOCKER_HOST = "unix:///run/user/1000/docker.sock"'
        in backend_source
        and 'CANARY_CONTAINER_PREFIX = "void-scout-repair-canary-"'
        in backend_source,
        "SCOUT_POST_RUN_DOCKER_IDENTITY_DRIFT",
    )
    _require(
        'EXPECTED_REPO_ROOT = "/home/zoso/dev/openra-rl-war-college"'
        in backend_source,
        "SCOUT_POST_RUN_REPO_IDENTITY_DRIFT",
    )

    for forbidden in (
        "shell=True",
        "sudo",
        "docker run",
        "docker rm",
        "docker stop",
        "systemctl stop",
        "systemctl start",
        "systemctl restart",
        "git reset",
        "git checkout",
        "git clean",
        "git fetch",
        "git pull",
        "/v1/chat/completions",
        "ollama_tool_call",
    ):
        _require(
            forbidden not in backend_source,
            f"SCOUT_POST_RUN_FORBIDDEN_SOURCE_TOKEN:{forbidden}",
        )

    required_methods = {
        "attempt_marker_present",
        "runtime_service_inactive",
        "engine_container_absent",
        "model_process_absent",
        "source_checkout_clean",
        "probes",
    }
    method_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    _require(
        required_methods <= method_names,
        "SCOUT_POST_RUN_REQUIRED_BACKEND_METHOD_MISSING",
    )

    return {
        "schema": SCHEMA,
        "backend_path": BACKEND_PATH,
        "backend_git_blob": BACKEND_GIT_BLOB,
        "observer_path": OBSERVER_PATH,
        "observer_git_blob": OBSERVER_GIT_BLOB,
        "attempt_guard_path": ATTEMPT_GUARD_PATH,
        "attempt_guard_git_blob": ATTEMPT_GUARD_GIT_BLOB,
        "backend_source_reviewed": True,
        "observer_source_bound": True,
        "attempt_guard_source_bound": True,
        "precision_host_identity_bound": True,
        "system_ollama_service_bound": True,
        "rootless_docker_identity_bound": True,
        "canary_container_namespace_bound": True,
        "source_checkout_identity_bound": True,
        "shell_execution_present": False,
        "attempt_marker_content_read_present": False,
        "service_mutation_present": False,
        "container_mutation_present": False,
        "git_mutation_present": False,
        "model_request_present": False,
        "game_execution_present": False,
        "automatic_retry_present": False,
        "host_observation_performed": False,
        "execution_authorized": False,
        "next_gate": NEXT_GATE,
    }


def authorize_live_observation_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunPrecisionHostBackendReviewHold(NEXT_GATE)
