"""Consume exactly one V2R13 pair-09 baseline launch slot.

This filesystem guard is a prerequisite only. It is not operator
authentication, runtime authorization, execution evidence, or a reusable
permit. The caller must supply an already-admitted private directory.

A successful claim creates one durable marker. Existing or uncertain markers
always HOLD. There is intentionally no reset, delete, retry, or resume API.
Importing this module performs no host action.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_generation2
    as request,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_source_binding_review_generation2
    as request_review,
)

MARKER_NAME = "pair-09-baseline-attempt-v1.json"
CLAIM_CONFIRMATION = (
    "VOID_ABADDON_GENERATION2_V2R13_RESERVE_PAIR09_BASELINE_ATTEMPT"
)
SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-attempt-consumption.v1"
)
MAX_MARKER_BYTES = 2048
MAX_IO_CALLS = 64


class V2R13Pair09BaselineAttemptHold(RuntimeError):
    def __init__(self, code: str, *, marker_may_exist: bool = False):
        super().__init__(code)
        self.marker_may_exist = marker_may_exist


def _require(condition: bool, code: str, *, consumed: bool = False) -> None:
    if not condition:
        raise V2R13Pair09BaselineAttemptHold(
            code,
            marker_may_exist=consumed,
        )


def _validate_request_review() -> dict[str, Any]:
    reviewed = (
        request_review
        .v2r13_pair09_baseline_authorization_request_review_contract()
    )
    _require(
        reviewed.get("pair09_baseline_authorization_request_reviewed") is True,
        "PAIR09_BASELINE_ATTEMPT_REQUEST_NOT_REVIEWED",
    )
    _require(
        reviewed.get("proposal_only_not_authorization") is True,
        "PAIR09_BASELINE_ATTEMPT_REQUEST_AUTHORITY_DRIFT",
    )
    _require(
        reviewed.get("pair_slot") == 9
        and reviewed.get("arm") == "baseline"
        and reviewed.get("held_out") is False,
        "PAIR09_BASELINE_ATTEMPT_SCOPE_DRIFT",
    )
    _require(
        reviewed.get("maximum_baseline_attempts") == 1
        and reviewed.get("maximum_automatic_retries") == 0,
        "PAIR09_BASELINE_ATTEMPT_CARDINALITY_DRIFT",
    )
    _require(
        reviewed.get("pair09_baseline_specific_authorization_accepted") is False
        and reviewed.get("pair09_baseline_execution_authorized") is False
        and reviewed.get("pair09_baseline_execution_performed") is False,
        "PAIR09_BASELINE_ATTEMPT_PREMATURE_AUTHORITY",
    )
    return reviewed


def _directory(
    fd: int,
    expected: tuple[int, int],
    *,
    consumed: bool,
) -> None:
    observed = os.fstat(fd)
    _require(
        stat.S_ISDIR(observed.st_mode)
        and (observed.st_dev, observed.st_ino) == expected
        and observed.st_uid == os.geteuid()
        and stat.S_IMODE(observed.st_mode) == 0o700
        and observed.st_nlink > 0,
        "PAIR09_BASELINE_ATTEMPT_DIRECTORY_HOLD",
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


def consume_pair09_baseline_attempt(
    *,
    directory_fd: int,
    expected_directory_identity: tuple[int, int],
    request_bytes: bytes,
    invocation_source_sha256: str,
    confirm: str,
) -> dict[str, Any]:
    """Create and sync the fixed one-use pair-09 baseline marker."""

    _require(
        type(confirm) is str and confirm == CLAIM_CONFIRMATION,
        "PAIR09_BASELINE_ATTEMPT_CONFIRMATION_REQUIRED",
    )
    _validate_request_review()

    try:
        validated = request.validate_pair09_baseline_authorization_request(
            request_bytes
        )
    except request.V2R13Pair09BaselineAuthorizationRequestHold:
        raise V2R13Pair09BaselineAttemptHold(
            "PAIR09_BASELINE_ATTEMPT_REQUEST_INVALID"
        ) from None

    request_sha256 = validated.get("request_sha256")
    _require(
        type(request_sha256) is str
        and len(request_sha256) == 64
        and all(c in "0123456789abcdef" for c in request_sha256),
        "PAIR09_BASELINE_ATTEMPT_REQUEST_DIGEST_INVALID",
    )
    _require(
        type(invocation_source_sha256) is str
        and len(invocation_source_sha256) == 64
        and all(c in "0123456789abcdef" for c in invocation_source_sha256),
        "PAIR09_BASELINE_ATTEMPT_SOURCE_IDENTITY_INVALID",
    )
    _require(
        type(directory_fd) is int and directory_fd >= 0,
        "PAIR09_BASELINE_ATTEMPT_FD_INVALID",
    )
    _require(
        type(expected_directory_identity) is tuple
        and len(expected_directory_identity) == 2
        and all(
            type(v) is int and v >= 0
            for v in expected_directory_identity
        ),
        "PAIR09_BASELINE_ATTEMPT_DIRECTORY_IDENTITY_INVALID",
    )
    _require(
        os.name == "posix"
        and hasattr(os, "O_NOFOLLOW")
        and hasattr(os, "O_CLOEXEC")
        and hasattr(os, "geteuid"),
        "PAIR09_BASELINE_ATTEMPT_PLATFORM_UNSUPPORTED",
    )

    record = {
        "schema": SCHEMA,
        "record_kind": "attempt_consumed_not_execution_evidence",
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "request_sha256": request_sha256,
        "invocation_source_sha256": invocation_source_sha256,
        "pair09_baseline_specific_authorization_accepted": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "reusable_execution_permit": False,
        "automatic_retry": False,
    }
    raw = (
        json.dumps(record, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    _require(
        len(raw) <= MAX_MARKER_BYTES,
        "PAIR09_BASELINE_ATTEMPT_MARKER_BOUND",
    )

    owned_directory = None
    marker = None
    marker_may_exist = False
    failed = False
    try:
        owned_directory = os.dup(directory_fd)
        _directory(
            owned_directory,
            expected_directory_identity,
            consumed=False,
        )

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
            raise V2R13Pair09BaselineAttemptHold(
                "PAIR09_BASELINE_ATTEMPT_ALREADY_EXISTS",
                marker_may_exist=True,
            ) from None

        os.fchmod(marker, 0o600)

        offset = 0
        for _ in range(MAX_IO_CALLS):
            if offset == len(raw):
                break
            written = os.write(marker, raw[offset:])
            _require(
                type(written) is int
                and 0 < written <= len(raw) - offset,
                "PAIR09_BASELINE_ATTEMPT_WRITE_HOLD",
                consumed=True,
            )
            offset += written

        _require(
            offset == len(raw),
            "PAIR09_BASELINE_ATTEMPT_WRITE_BOUND",
            consumed=True,
        )

        after_write = os.fstat(marker)
        _require(
            stat.S_ISREG(after_write.st_mode)
            and after_write.st_nlink == 1
            and after_write.st_uid == os.geteuid()
            and stat.S_IMODE(after_write.st_mode) == 0o600
            and after_write.st_size == len(raw),
            "PAIR09_BASELINE_ATTEMPT_FILE_HOLD",
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
            _require(
                bool(chunk),
                "PAIR09_BASELINE_ATTEMPT_SHORT_READ",
                consumed=True,
            )
            observed.extend(chunk)

        _require(
            bytes(observed) == raw and os.read(marker, 1) == b"",
            "PAIR09_BASELINE_ATTEMPT_READBACK_HOLD",
            consumed=True,
        )

        current = os.fstat(marker)
        named = os.stat(
            MARKER_NAME,
            dir_fd=owned_directory,
            follow_symlinks=False,
        )
        _require(
            _file_identity(after_write)
            == _file_identity(current)
            == _file_identity(named),
            "PAIR09_BASELINE_ATTEMPT_FILE_CHANGED",
            consumed=True,
        )
        _directory(
            owned_directory,
            expected_directory_identity,
            consumed=True,
        )

        return {
            **record,
            "single_use_slot_consumed": True,
            "marker_name": MARKER_NAME,
            "marker_sha256": hashlib.sha256(raw).hexdigest(),
            "marker_bytes": len(raw),
            "directory_identity": expected_directory_identity,
        }
    except V2R13Pair09BaselineAttemptHold:
        failed = True
        raise
    except OSError:
        failed = True
        raise V2R13Pair09BaselineAttemptHold(
            "PAIR09_BASELINE_ATTEMPT_IO_HOLD",
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
            raise V2R13Pair09BaselineAttemptHold(
                "PAIR09_BASELINE_ATTEMPT_CLOSE_HOLD",
                marker_may_exist=marker_may_exist,
            )


def pair09_baseline_attempt_guard_contract() -> dict[str, Any]:
    reviewed = _validate_request_review()
    return {
        "schema": SCHEMA,
        "marker_name": MARKER_NAME,
        "claim_confirmation": CLAIM_CONFIRMATION,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "single_use_attempt_consumption_implemented": True,
        "create_only_marker_required": True,
        "existing_or_uncertain_marker_holds": True,
        "marker_deletion_api_implemented": False,
        "reset_api_implemented": False,
        "resume_api_implemented": False,
        "automatic_retry": False,
        "pair09_baseline_specific_authorization_accepted": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "pair09_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "request_review": reviewed,
        "next_gate": (
            "V2R13_PAIR09_BASELINE_ATTEMPT_GUARD_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "next_change_class": (
            "source_only_v2r13_pair09_baseline_attempt_guard_"
            "source_binding_review"
        ),
    }
