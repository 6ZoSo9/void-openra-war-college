"""Consume one candidate launch slot in a caller-admitted private directory.

This is a filesystem prerequisite, not operator authentication or an execution
permit. A future reviewed invocation must enforce authorization, source/baseline
identity, readiness and revocation, then call this guard before any runtime
start. All invocations must use the SAME persistent directory; choosing a new
one, deleting state, rollback, hostile same-UID mutation and storage lying about
fsync are outside this cooperative local-filesystem contract.

Import has no host effects. There is no CLI, game callback, reset or resume API.
Existing or uncertain markers always HOLD; their contents are never trusted.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2
    as request,
)

MARKER_NAME = "pair-03-candidate-attempt-v1.json"
CLAIM_CONFIRMATION = "VOID_ABADDON_GENERATION2_V2R13_RESERVE_PAIR03_CANDIDATE_ATTEMPT"
REQUEST_SHA256 = "5025174efdf945f206119c1f25cb3a5d07bcb87ed3de8ccd93e3d9b1e3354a87"
SCHEMA = "void.abaddon.generation2.v2r13-pair03-candidate-attempt-consumption.v1"
MAX_MARKER_BYTES = 2048
MAX_IO_CALLS = 64


class CandidateAttemptHold(RuntimeError):
    """No launch may follow this terminal, even when a marker was created."""

    def __init__(self, code: str, *, marker_may_exist: bool = False):
        super().__init__(code)
        self.marker_may_exist = marker_may_exist


def _require(condition: bool, code: str, *, consumed: bool = False) -> None:
    if not condition:
        raise CandidateAttemptHold(code, marker_may_exist=consumed)


def _directory(fd: int, expected: tuple[int, int], *, consumed: bool) -> None:
    observed = os.fstat(fd)
    _require(
        stat.S_ISDIR(observed.st_mode)
        and (observed.st_dev, observed.st_ino) == expected
        and observed.st_uid == os.geteuid()
        and stat.S_IMODE(observed.st_mode) == 0o700
        and observed.st_nlink > 0,
        "CANDIDATE_ATTEMPT_DIRECTORY_HOLD", consumed=consumed,
    )


def _file_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
        value.st_uid, value.st_size, value.st_mtime_ns, value.st_ctime_ns,
    )


def consume_candidate_attempt(
    *, directory_fd: int, expected_directory_identity: tuple[int, int],
    request_bytes: bytes, invocation_source_sha256: str, confirm: str,
) -> dict[str, Any]:
    """Create and sync a fixed one-use marker, or HOLD without deleting it.

    The descriptor is borrowed and duplicated; the caller retains ownership.
    Its expected identity is an independently admitted caller input, NOT a host
    attestation. ``confirm`` confirms this state write only, never a game run.
    Source SHA-256 is a recorded expectation, not verified executed-code custody.
    No result or existing marker is a transferable/reusable execution permit.
    """
    _require(type(confirm) is str and confirm == CLAIM_CONFIRMATION,
             "CANDIDATE_ATTEMPT_CONFIRMATION_REQUIRED")
    try:
        validated = request.validate_candidate_authorization_request(request_bytes)
    except request.V2R13Pair03CandidateAuthorizationRequestHold:
        raise CandidateAttemptHold("CANDIDATE_ATTEMPT_REQUEST_INVALID") from None
    _require(validated["request_sha256"] == REQUEST_SHA256, "CANDIDATE_ATTEMPT_REQUEST_DRIFT")
    _require(
        type(invocation_source_sha256) is str
        and len(invocation_source_sha256) == 64
        and all(c in "0123456789abcdef" for c in invocation_source_sha256),
        "CANDIDATE_ATTEMPT_SOURCE_IDENTITY_INVALID",
    )
    _require(type(directory_fd) is int and directory_fd >= 0, "CANDIDATE_ATTEMPT_FD_INVALID")
    _require(
        type(expected_directory_identity) is tuple and len(expected_directory_identity) == 2
        and all(type(v) is int and v >= 0 for v in expected_directory_identity),
        "CANDIDATE_ATTEMPT_DIRECTORY_IDENTITY_INVALID",
    )
    _require(
        os.name == "posix" and hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_CLOEXEC")
        and hasattr(os, "geteuid"), "CANDIDATE_ATTEMPT_PLATFORM_UNSUPPORTED",
    )
    record = {
        "schema": SCHEMA, "record_kind": "attempt_consumed_not_execution_evidence",
        "pair_slot": 3, "arm": "candidate", "held_out": False,
        "request_sha256": REQUEST_SHA256,
        "invocation_source_sha256": invocation_source_sha256,
        "candidate_execution_authorized": False, "candidate_execution_performed": False,
        "reusable_execution_permit": False, "automatic_retry": False,
    }
    raw = (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    _require(len(raw) <= MAX_MARKER_BYTES, "CANDIDATE_ATTEMPT_MARKER_BOUND")
    owned_directory = None
    marker = None
    marker_may_exist = False
    failed = False
    try:
        owned_directory = os.dup(directory_fd)
        _directory(owned_directory, expected_directory_identity, consumed=False)
        # A failed pre-creation sync consumes no slot and dispatches nothing.
        os.fsync(owned_directory)
        marker_may_exist = True
        try:
            marker = os.open(
                MARKER_NAME, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                0o600, dir_fd=owned_directory,
            )
        except FileExistsError:
            raise CandidateAttemptHold("CANDIDATE_ATTEMPT_ALREADY_EXISTS", marker_may_exist=True) from None
        os.fchmod(marker, 0o600)  # Only the newly created, owned inode.
        offset = 0
        for _ in range(MAX_IO_CALLS):
            if offset == len(raw):
                break
            written = os.write(marker, raw[offset:])
            _require(type(written) is int and 0 < written <= len(raw) - offset,
                     "CANDIDATE_ATTEMPT_WRITE_HOLD", consumed=True)
            offset += written
        _require(offset == len(raw), "CANDIDATE_ATTEMPT_WRITE_BOUND", consumed=True)
        after_write = os.fstat(marker)
        _require(
            stat.S_ISREG(after_write.st_mode) and after_write.st_nlink == 1
            and after_write.st_uid == os.geteuid() and stat.S_IMODE(after_write.st_mode) == 0o600
            and after_write.st_size == len(raw), "CANDIDATE_ATTEMPT_FILE_HOLD", consumed=True,
        )
        os.fsync(marker)
        os.fsync(owned_directory)
        os.lseek(marker, 0, os.SEEK_SET)
        observed = bytearray()
        for _ in range(MAX_IO_CALLS):
            if len(observed) == len(raw):
                break
            chunk = os.read(marker, len(raw) - len(observed))
            _require(bool(chunk), "CANDIDATE_ATTEMPT_SHORT_READ", consumed=True)
            observed.extend(chunk)
        _require(bytes(observed) == raw and os.read(marker, 1) == b"",
                 "CANDIDATE_ATTEMPT_READBACK_HOLD", consumed=True)
        current = os.fstat(marker)
        named = os.stat(MARKER_NAME, dir_fd=owned_directory, follow_symlinks=False)
        _require(
            _file_identity(after_write) == _file_identity(current) == _file_identity(named),
            "CANDIDATE_ATTEMPT_FILE_CHANGED", consumed=True,
        )
        _directory(owned_directory, expected_directory_identity, consumed=True)
        return {
            **record, "single_use_slot_consumed": True, "marker_name": MARKER_NAME,
            "marker_sha256": hashlib.sha256(raw).hexdigest(), "marker_bytes": len(raw),
            "directory_identity": expected_directory_identity,
        }
    except CandidateAttemptHold:
        failed = True
        raise
    except OSError:
        failed = True
        raise CandidateAttemptHold("CANDIDATE_ATTEMPT_IO_HOLD", marker_may_exist=marker_may_exist) from None
    except BaseException:
        failed = True
        raise
    finally:
        close_failed = False
        for descriptor in (marker, owned_directory):
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    close_failed = True
        # Do not mask the primary failure or retry a close against a reused FD.
        if close_failed and not failed:
            raise CandidateAttemptHold("CANDIDATE_ATTEMPT_CLOSE_HOLD", marker_may_exist=marker_may_exist)
