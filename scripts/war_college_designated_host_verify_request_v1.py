#!/usr/bin/env python3
"""One-shot designated-host request verifier for the War College."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_VERIFY_REQUEST_V1"
SCHEMA_VERSION = 1
REQUEST_MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_VERIFY_REQUEST_BUNDLE_V1"
REQUEST_SCHEMA_VERSION = 1
REQUEST_ID_RE = re.compile(r"wcrq1_[0-9a-f]{32}\Z")

EXPECTED_UID = 1000
EXPECTED_GID = 1000
EXPECTED_WRAPPER_PATH = Path("/home/zoso/.local/libexec/void-war-college-evidence-verifier-v1.py")
EXPECTED_DATA_DIR = Path("/home/zoso/dev/void-node/data_a")
EXPECTED_RUNTIME_REPOSITORY = Path("/home/zoso/dev/openra-rl-war-college-worktrees/designated-host-runtime-bae61935")
EXPECTED_RUNTIME_SOURCE_COMMIT = "bae61935b956c5f7ebce005c0fef69ec86f69d09"
EXPECTED_RUNTIME_BLOBS = {'scripts/controller_attempt_admission_store_v1.py': '5f03230bd8af50ccbb265a6173a3a7d52a6e09b8', 'scripts/verify_controller_evidence_isolation_v1.py': '3f3ca8ae70c3005dea45b153017f7e0e0caa1296', 'scripts/verify_controller_evidence_producer_auth_v1.py': 'cce13a7ff4d36e21cc4719625e2b3c116e851889', 'scripts/verify_controller_evidence_with_durable_currentness_v1.py': '2d7a583e45df8d803b21b534c2d80ce9f1a787f7', 'scripts/war_college_designated_producer_trust_root_v1.py': 'ac3394d03ecadb0112edd67c565d44c740e63d76'}

REQUEST_FILE = "request.json"
EVIDENCE_FILE = "evidence.json"
AUTH_FILE = "producer-auth.json"
REQUEST_KEYS = {
    "marker",
    "schema_version",
    "request_id",
    "evidence_sha256",
    "producer_auth_sha256",
}
MAX_REQUEST_BYTES = 8 * 1024
MAX_EVIDENCE_BYTES = 128 * 1024
MAX_AUTH_BYTES = 128 * 1024
LOWER_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
GIT = "/usr/bin/git"


class WrapperHold(ValueError):
    pass


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _json_no_duplicates(raw: bytes, hold: str) -> Any:
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise WrapperHold(hold)
            result[key] = value
        return result

    try:
        text = raw.decode("utf-8", "strict")
        return json.loads(text, object_pairs_hook=hook)
    except WrapperHold:
        raise
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise WrapperHold(hold) from error


def _run_git(*args: str) -> str:
    cp = subprocess.run(
        [GIT, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
        },
    )
    if cp.returncode != 0:
        raise WrapperHold("HOLD_RUNTIME_SOURCE_GIT_FAILURE")
    return cp.stdout.strip()


def _verify_runtime_source() -> None:
    repo = EXPECTED_RUNTIME_REPOSITORY
    try:
        resolved = repo.resolve(strict=True)
    except OSError as error:
        raise WrapperHold("HOLD_RUNTIME_REPOSITORY_NOT_FOUND") from error
    if resolved != repo:
        raise WrapperHold("HOLD_RUNTIME_REPOSITORY_SYMLINKED")
    if Path.cwd().resolve(strict=True) != repo:
        raise WrapperHold("HOLD_RUNTIME_WORKING_DIRECTORY_MISMATCH")
    if _run_git("-C", str(repo), "rev-parse", "HEAD") != EXPECTED_RUNTIME_SOURCE_COMMIT:
        raise WrapperHold("HOLD_RUNTIME_SOURCE_COMMIT_MISMATCH")
    if _run_git("-C", str(repo), "status", "--porcelain", "--untracked-files=all"):
        raise WrapperHold("HOLD_RUNTIME_WORKTREE_NOT_CLEAN")
    for path, expected_blob in sorted(EXPECTED_RUNTIME_BLOBS.items()):
        actual = _run_git("-C", str(repo), "rev-parse", f"HEAD:{path}")
        if actual != expected_blob:
            raise WrapperHold("HOLD_RUNTIME_ARTIFACT_BLOB_MISMATCH")


def _require_dir_record(fd: int, *, exact_mode: int | None = None) -> None:
    st = os.fstat(fd)
    if not stat.S_ISDIR(st.st_mode):
        raise WrapperHold("HOLD_REQUEST_DIRECTORY_NOT_DIRECTORY")
    if st.st_uid != EXPECTED_UID or st.st_gid != EXPECTED_GID:
        raise WrapperHold("HOLD_REQUEST_DIRECTORY_OWNER_MISMATCH")
    mode = stat.S_IMODE(st.st_mode)
    if mode & 0o022:
        raise WrapperHold("HOLD_REQUEST_DIRECTORY_GROUP_OR_OTHER_WRITABLE")
    if exact_mode is not None and mode != exact_mode:
        raise WrapperHold("HOLD_REQUEST_DIRECTORY_MODE_MISMATCH")


def _open_dir_at(parent_fd: int, name: str, *, exact_mode: int | None = None) -> int:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(name, flags, dir_fd=parent_fd)
    except OSError as error:
        raise WrapperHold("HOLD_REQUEST_DIRECTORY_OPEN_FAILURE") from error
    try:
        _require_dir_record(fd, exact_mode=exact_mode)
    except Exception:
        os.close(fd)
        raise
    return fd


def _open_regular_at(
    directory_fd: int,
    name: str,
    *,
    maximum_bytes: int,
    exact_mode: int = 0o400,
) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    try:
        fd = os.open(name, flags, dir_fd=directory_fd)
    except OSError as error:
        raise WrapperHold("HOLD_REQUEST_FILE_OPEN_FAILURE") from error
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise WrapperHold("HOLD_REQUEST_FILE_NOT_REGULAR")
        if before.st_uid != EXPECTED_UID or before.st_gid != EXPECTED_GID:
            raise WrapperHold("HOLD_REQUEST_FILE_OWNER_MISMATCH")
        if stat.S_IMODE(before.st_mode) != exact_mode:
            raise WrapperHold("HOLD_REQUEST_FILE_MODE_MISMATCH")
        if before.st_size > maximum_bytes:
            raise WrapperHold("HOLD_REQUEST_FILE_TOO_LARGE")

        chunks: list[bytes] = []
        remaining = maximum_bytes + 1
        while remaining:
            chunk = os.read(fd, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        identity = lambda value: (
            value.st_dev,
            value.st_ino,
            value.st_size,
            value.st_mtime_ns,
            stat.S_IMODE(value.st_mode),
        )
        if identity(before) != identity(after) or len(raw) != before.st_size:
            raise WrapperHold("HOLD_REQUEST_FILE_CHANGED_DURING_READ")
        if len(raw) > maximum_bytes:
            raise WrapperHold("HOLD_REQUEST_FILE_TOO_LARGE")
        return raw
    finally:
        os.close(fd)


def _open_bundle(request_id: str, data_dir: Path) -> tuple[bytes, bytes, bytes]:
    if REQUEST_ID_RE.fullmatch(request_id) is None:
        raise WrapperHold("HOLD_REQUEST_ID_INVALID")
    try:
        resolved_data = data_dir.resolve(strict=True)
    except OSError as error:
        raise WrapperHold("HOLD_DATA_DIR_NOT_FOUND") from error
    if resolved_data != data_dir:
        raise WrapperHold("HOLD_DATA_DIR_SYMLINKED")

    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        data_fd = os.open(str(data_dir), flags)
    except OSError as error:
        raise WrapperHold("HOLD_DATA_DIR_OPEN_FAILURE") from error

    fds = [data_fd]
    try:
        _require_dir_record(data_fd)
        war_fd = _open_dir_at(data_fd, "war_college")
        fds.append(war_fd)
        root_fd = _open_dir_at(war_fd, "verifier_requests_v1", exact_mode=0o700)
        fds.append(root_fd)
        request_fd = _open_dir_at(root_fd, request_id, exact_mode=0o700)
        fds.append(request_fd)

        names = set(os.listdir(request_fd))
        if names != {REQUEST_FILE, EVIDENCE_FILE, AUTH_FILE}:
            raise WrapperHold("HOLD_REQUEST_BUNDLE_ENTRIES_NOT_EXACT")

        request_raw = _open_regular_at(
            request_fd, REQUEST_FILE, maximum_bytes=MAX_REQUEST_BYTES
        )
        evidence_raw = _open_regular_at(
            request_fd, EVIDENCE_FILE, maximum_bytes=MAX_EVIDENCE_BYTES
        )
        auth_raw = _open_regular_at(
            request_fd, AUTH_FILE, maximum_bytes=MAX_AUTH_BYTES
        )
        return request_raw, evidence_raw, auth_raw
    finally:
        for fd in reversed(fds):
            try:
                os.close(fd)
            except OSError:
                pass


def _validate_request(
    request_id: str,
    request_raw: bytes,
    evidence_raw: bytes,
    auth_raw: bytes,
) -> dict[str, Any]:
    request = _json_no_duplicates(request_raw, "HOLD_REQUEST_JSON_INVALID")
    if type(request) is not dict or set(request) != REQUEST_KEYS:
        raise WrapperHold("HOLD_REQUEST_SCHEMA_DRIFT")
    if request_raw != _canonical_json_bytes(request):
        raise WrapperHold("HOLD_REQUEST_JSON_NOT_CANONICAL")
    if request.get("marker") != REQUEST_MARKER:
        raise WrapperHold("HOLD_REQUEST_MARKER_MISMATCH")
    if request.get("schema_version") != REQUEST_SCHEMA_VERSION:
        raise WrapperHold("HOLD_REQUEST_SCHEMA_VERSION_MISMATCH")
    if request.get("request_id") != request_id:
        raise WrapperHold("HOLD_REQUEST_ID_MISMATCH")
    evidence_sha = request.get("evidence_sha256")
    auth_sha = request.get("producer_auth_sha256")
    if type(evidence_sha) is not str or LOWER_SHA256_RE.fullmatch(evidence_sha) is None:
        raise WrapperHold("HOLD_REQUEST_EVIDENCE_SHA256_INVALID")
    if type(auth_sha) is not str or LOWER_SHA256_RE.fullmatch(auth_sha) is None:
        raise WrapperHold("HOLD_REQUEST_AUTH_SHA256_INVALID")
    if hashlib.sha256(evidence_raw).hexdigest() != evidence_sha:
        raise WrapperHold("HOLD_REQUEST_EVIDENCE_SHA256_MISMATCH")
    if hashlib.sha256(auth_raw).hexdigest() != auth_sha:
        raise WrapperHold("HOLD_REQUEST_AUTH_SHA256_MISMATCH")
    return request


def _process_request(
    request_id: str,
    *,
    data_dir: Path,
    verify_callable: Callable[[Any, Any], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    request_raw, evidence_raw, auth_raw = _open_bundle(request_id, data_dir)
    request = _validate_request(request_id, request_raw, evidence_raw, auth_raw)

    evidence = _json_no_duplicates(evidence_raw, "HOLD_EVIDENCE_JSON_INVALID")
    auth_record = _json_no_duplicates(auth_raw, "HOLD_PRODUCER_AUTH_JSON_INVALID")

    if verify_callable is None:
        runtime_repo = str(EXPECTED_RUNTIME_REPOSITORY)
        if runtime_repo not in sys.path:
            sys.path.insert(0, runtime_repo)
        from scripts import verify_controller_evidence_isolation_v1 as structural
        from scripts import verify_controller_evidence_with_durable_currentness_v1 as integration

        structural._json_depth_preflight(evidence_raw)
        verify_callable = integration.verify_and_consume_evidence

    verifier_report = verify_callable(evidence, auth_record)
    if type(verifier_report) is not dict:
        raise WrapperHold("HOLD_VERIFIER_REPORT_INVALID")

    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "request_id": request_id,
        "runtime_source_commit": EXPECTED_RUNTIME_SOURCE_COMMIT,
        "evidence_sha256": request["evidence_sha256"],
        "producer_auth_sha256": request["producer_auth_sha256"],
        "verifier_contract": verifier_report.get("contract"),
        "verifier_phase": verifier_report.get("phase"),
        "verifier_holds": list(verifier_report.get("holds", [])),
        "consumption_sha256": verifier_report.get("consumption_sha256"),
        "runtime_evidence": verifier_report.get("runtime_evidence"),
        "private_key_read": False,
        "request_bundle_mutated": False,
    }


def _hold_report(request_id: str | None, hold: str) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "request_id": request_id,
        "runtime_source_commit": EXPECTED_RUNTIME_SOURCE_COMMIT,
        "verifier_contract": "HOLD",
        "verifier_holds": [hold],
        "private_key_read": False,
        "request_bundle_mutated": False,
    }


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    request_id = args[0] if len(args) == 1 else None
    try:
        if len(args) != 1:
            raise WrapperHold("HOLD_REQUEST_ID_ARGUMENT_REQUIRED")
        if REQUEST_ID_RE.fullmatch(request_id or "") is None:
            raise WrapperHold("HOLD_REQUEST_ID_INVALID")
        if os.getuid() != EXPECTED_UID or os.getgid() != EXPECTED_GID:
            raise WrapperHold("HOLD_RUNTIME_PROCESS_OWNER_MISMATCH")
        if Path(__file__).resolve(strict=True) != EXPECTED_WRAPPER_PATH:
            raise WrapperHold("HOLD_WRAPPER_PATH_MISMATCH")
        if os.environ.get("VOID_DATA_DIR") != str(EXPECTED_DATA_DIR):
            raise WrapperHold("HOLD_VOID_DATA_DIR_ENVIRONMENT_MISMATCH")
        if (
            os.environ.get("VOID_WAR_COLLEGE_RUNTIME_REPOSITORY")
            != str(EXPECTED_RUNTIME_REPOSITORY)
        ):
            raise WrapperHold("HOLD_RUNTIME_REPOSITORY_ENVIRONMENT_MISMATCH")
        if (
            os.environ.get("VOID_WAR_COLLEGE_RUNTIME_SOURCE_COMMIT")
            != EXPECTED_RUNTIME_SOURCE_COMMIT
        ):
            raise WrapperHold("HOLD_RUNTIME_SOURCE_COMMIT_ENVIRONMENT_MISMATCH")
        _verify_runtime_source()
        report = _process_request(request_id, data_dir=EXPECTED_DATA_DIR)
    except WrapperHold as error:
        report = _hold_report(request_id, str(error))
    except (OSError, ValueError, RecursionError) as error:
        report = _hold_report(
            request_id, f"HOLD_WRAPPER_FAILURE:{type(error).__name__}"
        )

    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report.get("verifier_contract") == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
