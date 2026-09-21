"""Create-only durable attempt guard for a future Abaddon scout experiment.

This guard consumes one caller-admitted slot in a private directory. It is not
operator authentication, runtime authorization, source custody, or execution
evidence. Existing or uncertain markers always HOLD and are never deleted,
rewritten, reset, or reused.

Import has no host effects. There is no CLI, game callback, runtime start,
execution function, reset API, or resume API.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from typing import Any

from openra_env.learning import abaddon_scout_external_launcher_contract_review_v1 as review
from openra_env.learning import abaddon_scout_external_launcher_contract_v1 as contract


MARKER_NAME = "abaddon-scout-external-attempt-v1.json"
CLAIM_CONFIRMATION = "VOID_ABADDON_SCOUT_RESERVE_FRESH_ATTEMPT_V1"
SCHEMA = "void.abaddon.scout-external-attempt-consumption.v1"
MAX_MARKER_BYTES = 4096
MAX_IO_CALLS = 128


class ScoutExternalAttemptHold(RuntimeError):
    """No runtime action may follow an uncertain or rejected attempt claim."""

    def __init__(self, code: str, *, marker_may_exist: bool = False):
        super().__init__(code)
        self.marker_may_exist = marker_may_exist


def _require(condition: bool, code: str, *, consumed: bool = False) -> None:
    if not condition:
        raise ScoutExternalAttemptHold(code, marker_may_exist=consumed)


def _directory(fd: int, expected: tuple[int, int], *, consumed: bool) -> None:
    observed = os.fstat(fd)
    _require(
        stat.S_ISDIR(observed.st_mode)
        and (observed.st_dev, observed.st_ino) == expected
        and observed.st_uid == os.geteuid()
        and stat.S_IMODE(observed.st_mode) == 0o700
        and observed.st_nlink > 0,
        "SCOUT_ATTEMPT_DIRECTORY_HOLD",
        consumed=consumed,
    )


def _file_identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_uid,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _valid_experiment_id(value: Any) -> bool:
    if type(value) is not str or not 1 <= len(value) <= 128:
        return False
    if not value.startswith("abaddon-scout-") or "pair03" in value:
        return False
    return all(character in "abcdefghijklmnopqrstuvwxyz0123456789._-" for character in value)


def consume_scout_attempt(
    *,
    directory_fd: int,
    expected_directory_identity: tuple[int, int],
    request_bytes: bytes,
    experiment_id: str,
    launcher_contract_git_blob: str,
    confirm: str,
) -> dict[str, Any]:
    """Create, sync, and read back one fixed attempt marker or HOLD.

    The directory descriptor and experiment identity are admitted caller inputs;
    this guard does not authenticate either. The fixed marker name enforces only
    one cooperative attempt in the admitted persistent directory.

    Successful consumption still grants no runtime authority.
    """
    _require(
        type(confirm) is str and confirm == CLAIM_CONFIRMATION,
        "SCOUT_ATTEMPT_CONFIRMATION_REQUIRED",
    )
    try:
        validated = contract.validate_scout_launcher_request(request_bytes)
    except contract.ScoutExternalLauncherContractHold:
        raise ScoutExternalAttemptHold("SCOUT_ATTEMPT_REQUEST_INVALID") from None
    _require(
        validated["request_sha256"] == contract.REQUEST_SHA256,
        "SCOUT_ATTEMPT_REQUEST_DRIFT",
    )
    _require(
        type(launcher_contract_git_blob) is str
        and launcher_contract_git_blob == review.CONTRACT_GIT_BLOB,
        "SCOUT_ATTEMPT_LAUNCHER_SOURCE_DRIFT",
    )
    _require(_valid_experiment_id(experiment_id), "SCOUT_ATTEMPT_EXPERIMENT_ID_INVALID")
    _require(type(directory_fd) is int and directory_fd >= 0, "SCOUT_ATTEMPT_FD_INVALID")
    _require(
        type(expected_directory_identity) is tuple
        and len(expected_directory_identity) == 2
        and all(type(value) is int and value >= 0 for value in expected_directory_identity),
        "SCOUT_ATTEMPT_DIRECTORY_IDENTITY_INVALID",
    )
    _require(
        os.name == "posix"
        and hasattr(os, "O_NOFOLLOW")
        and hasattr(os, "O_CLOEXEC")
        and hasattr(os, "geteuid"),
        "SCOUT_ATTEMPT_PLATFORM_UNSUPPORTED",
    )

    record = {
        "schema": SCHEMA,
        "record_kind": "attempt_consumed_not_execution_evidence",
        "experiment_id": experiment_id,
        "request_sha256": contract.REQUEST_SHA256,
        "launcher_contract_git_blob": review.CONTRACT_GIT_BLOB,
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
    raw = (
        json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")
    _require(len(raw) <= MAX_MARKER_BYTES, "SCOUT_ATTEMPT_MARKER_BOUND")

    owned_directory = None
    marker = None
    marker_may_exist = False
    failed = False
    try:
        owned_directory = os.dup(directory_fd)
        _directory(owned_directory, expected_directory_identity, consumed=False)
        os.fsync(owned_directory)

        marker_may_exist = True
        try:
            marker = os.open(
                MARKER_NAME,
                os.O_RDWR
                | os.O_CREAT
                | os.O_EXCL
                | os.O_NOFOLLOW
                | os.O_CLOEXEC,
                0o600,
                dir_fd=owned_directory,
            )
        except FileExistsError:
            raise ScoutExternalAttemptHold(
                "SCOUT_ATTEMPT_ALREADY_EXISTS",
                marker_may_exist=True,
            ) from None

        os.fchmod(marker, 0o600)
        offset = 0
        for _ in range(MAX_IO_CALLS):
            if offset == len(raw):
                break
            written = os.write(marker, raw[offset:])
            _require(
                type(written) is int and 0 < written <= len(raw) - offset,
                "SCOUT_ATTEMPT_WRITE_HOLD",
                consumed=True,
            )
            offset += written
        _require(offset == len(raw), "SCOUT_ATTEMPT_WRITE_BOUND", consumed=True)

        after_write = os.fstat(marker)
        _require(
            stat.S_ISREG(after_write.st_mode)
            and after_write.st_nlink == 1
            and after_write.st_uid == os.geteuid()
            and stat.S_IMODE(after_write.st_mode) == 0o600
            and after_write.st_size == len(raw),
            "SCOUT_ATTEMPT_FILE_HOLD",
            consumed=True,
        )

        os.fsync(marker)
        os.fsync(owned_directory)
        os.lseek(marker, 0, os.SEEK_SET)

        observed = bytearray()
        for _ in range(MAX_IO_CALLS):
            if len(observed) == len(raw):
                break
            chunk = os.read(marker, len(raw) - len(observed))
            _require(bool(chunk), "SCOUT_ATTEMPT_SHORT_READ", consumed=True)
            observed.extend(chunk)
        _require(
            bytes(observed) == raw and os.read(marker, 1) == b"",
            "SCOUT_ATTEMPT_READBACK_HOLD",
            consumed=True,
        )

        current = os.fstat(marker)
        named = os.stat(MARKER_NAME, dir_fd=owned_directory, follow_symlinks=False)
        _require(
            _file_identity(after_write)
            == _file_identity(current)
            == _file_identity(named),
            "SCOUT_ATTEMPT_FILE_CHANGED",
            consumed=True,
        )
        _directory(owned_directory, expected_directory_identity, consumed=True)

        return {
            **record,
            "single_use_slot_consumed": True,
            "marker_name": MARKER_NAME,
            "marker_sha256": hashlib.sha256(raw).hexdigest(),
            "marker_bytes": len(raw),
            "directory_identity": expected_directory_identity,
        }
    except ScoutExternalAttemptHold:
        failed = True
        raise
    except OSError:
        failed = True
        raise ScoutExternalAttemptHold(
            "SCOUT_ATTEMPT_IO_HOLD",
            marker_may_exist=marker_may_exist,
        ) from None
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
        if close_failed and not failed:
            raise ScoutExternalAttemptHold(
                "SCOUT_ATTEMPT_CLOSE_HOLD",
                marker_may_exist=marker_may_exist,
            )
