#!/usr/bin/env python3
"""Recovery-capable operator handoff for Darwin precommitted evaluation records.

This source-only companion preserves the existing create-only precommit record format while
closing the publication-terminal ambiguity around file-fsync -> parent-directory-fsync.
Recovery never overwrites, deletes, renames, or chmods the record and never retroactively
authorizes calibration evidence produced before the recovery terminal.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path
from typing import Iterable, Mapping

import darwin_evaluation_precommit_record_v1 as record_contract
import darwin_heldout_evaluation_split_v1 as split
import darwin_precommitted_evaluation_plan_v1 as plan_contract

HANDOFF_MARKER = "VOID_WAR_COLLEGE_PRECOMMIT_RECOVERY_HANDOFF_V1"
MAX_JSON_BYTES = record_contract.MAX_JSON_BYTES


class RecoveryError(record_contract.RecordError):
    """Raised when publication recovery cannot establish exact durable authority."""


class PublicationDurabilityUncertain(RecoveryError):
    """Raised only after record-file durability when parent-directory durability is unknown."""


def _private_record_stat(info: os.stat_result) -> None:
    if not stat.S_ISREG(info.st_mode):
        raise RecoveryError("precommit record must be a regular file")
    if info.st_size <= 0 or info.st_size > MAX_JSON_BYTES:
        raise RecoveryError(f"precommit record must contain 1..{MAX_JSON_BYTES} bytes")
    if info.st_nlink != 1:
        raise RecoveryError("precommit record must have exactly one hard link")
    if hasattr(os, "getuid") and info.st_uid != os.getuid():
        raise RecoveryError("precommit record must be owned by the current uid")
    if stat.S_IMODE(info.st_mode) != 0o600:
        raise RecoveryError("precommit record mode must be exactly 0600")


def _read_retained_fd(fd: int, size: int) -> bytes:
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = os.read(fd, min(remaining, 65536))
        if not chunk:
            raise RecoveryError("precommit record changed or truncated during retained-fd read")
        chunks.append(chunk)
        remaining -= len(chunk)
    if os.read(fd, 1):
        raise RecoveryError("precommit record grew during retained-fd read")
    return b"".join(chunks)


def _decode_validate_record_bytes(
    raw: bytes,
    manifest: Mapping[str, object],
) -> dict[str, object]:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RecoveryError("precommit record is not valid UTF-8 JSON") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RecoveryError("precommit record is not valid JSON") from exc
    if not isinstance(value, dict):
        raise RecoveryError("precommit record JSON must be an object")
    if raw != (record_contract.canonical_json(value) + "\n").encode("utf-8"):
        raise RecoveryError("precommit record bytes are not canonical JSON plus one newline")
    return record_contract.validate_record(value, manifest)


def _visible_path_matches_retained_fd(path: Path, retained: os.stat_result) -> None:
    try:
        current = os.stat(path, follow_symlinks=False)
    except OSError as exc:
        raise RecoveryError(
            f"precommit record pathname unavailable after parent durability terminal: "
            f"{exc.strerror or exc}"
        ) from exc
    _private_record_stat(current)
    if (current.st_dev, current.st_ino) != (retained.st_dev, retained.st_ino):
        raise RecoveryError(
            "precommit record pathname no longer names the retained exact inode"
        )
    for field in ("st_size", "st_nlink", "st_uid"):
        if getattr(current, field) != getattr(retained, field):
            raise RecoveryError(
                f"precommit record pathname generation changed at {field}"
            )
    if stat.S_IMODE(current.st_mode) != stat.S_IMODE(retained.st_mode):
        raise RecoveryError("precommit record pathname mode changed during durability terminal")


def write_record_create_only_with_terminal(
    path: Path,
    record: Mapping[str, object],
) -> None:
    """Create, file-fsync, and parent-fsync one record while retaining exact inode authority."""
    payload = (record_contract.canonical_json(record) + "\n").encode("utf-8")
    if not payload or len(payload) > MAX_JSON_BYTES:
        raise RecoveryError(f"record payload exceeds {MAX_JSON_BYTES} bytes")

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise RecoveryError("record path already exists; create-only precommit refused") from exc
    except OSError as exc:
        raise RecoveryError(f"cannot create precommit record: {exc.strerror or exc}") from exc

    file_terminal = False
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(fd, payload[offset:])
            if written <= 0:
                raise RecoveryError("short write while publishing precommit record")
            offset += written
        os.fsync(fd)
        retained = os.fstat(fd)
        _private_record_stat(retained)
        if retained.st_size != len(payload):
            raise RecoveryError("published precommit record size mismatch")
        file_terminal = True
        try:
            record_contract._fsync_parent(path)
        except (record_contract.RecordError, OSError) as exc:
            raise PublicationDurabilityUncertain(
                "record bytes reached the file-fsync terminal but parent-directory "
                "durability is unconfirmed; do not overwrite/delete; run recover before "
                "starting or resuming calibration"
            ) from exc
        _visible_path_matches_retained_fd(path, retained)
    finally:
        os.close(fd)

    if not file_terminal:
        raise RecoveryError("precommit record did not reach the file durability terminal")


def recover_existing_record(
    path: Path,
    manifest: Mapping[str, object],
) -> dict[str, object]:
    """Establish a fresh parent-durability terminal for one exact existing record.

    Recovery is forward-only. It validates retained exact bytes/inode, fsyncs the parent,
    rechecks pathname identity and retained bytes, and grants no authority to earlier
    calibration or held-out evidence.
    """
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise RecoveryError(f"cannot open precommit record for recovery: {exc.strerror or exc}") from exc

    try:
        retained = os.fstat(fd)
        _private_record_stat(retained)
        before_raw = _read_retained_fd(fd, retained.st_size)
        record = _decode_validate_record_bytes(before_raw, manifest)

        # Recovery may follow an abrupt process loss before the original writer reached
        # its file-fsync terminal. Re-establish file durability on the retained exact
        # inode before making the parent-directory terminal authoritative.
        try:
            os.fsync(fd)
        except OSError as exc:
            raise RecoveryError(
                f"cannot fsync retained precommit record during recovery: {exc.strerror or exc}"
            ) from exc

        record_contract._fsync_parent(path)

        after_info = os.fstat(fd)
        _private_record_stat(after_info)
        if (after_info.st_dev, after_info.st_ino) != (retained.st_dev, retained.st_ino):
            raise RecoveryError("retained precommit record inode changed during recovery")
        if after_info.st_size != retained.st_size:
            raise RecoveryError("retained precommit record size changed during recovery")
        after_raw = _read_retained_fd(fd, after_info.st_size)
        if after_raw != before_raw:
            raise RecoveryError("retained precommit record bytes changed during recovery")
        _visible_path_matches_retained_fd(path, after_info)
        recovered = _decode_validate_record_bytes(after_raw, manifest)
        if recovered["record_digest"] != record["record_digest"]:
            raise RecoveryError("precommit record digest changed during recovery")
        return recovered
    finally:
        os.close(fd)


def _summary(
    status: str,
    record: Mapping[str, object],
    publication_terminal: str,
    safe_next_action: str,
) -> str:
    return record_contract.canonical_json(
        {
            "marker": HANDOFF_MARKER,
            "status": status,
            "record_id": record["record_id"],
            "record_digest": record["record_digest"],
            "plan_digest": record["plan_digest"],
            "split_digest": record["split_digest"],
            "benchmark_source_sha": record["benchmark_source_sha"],
            "publication_terminal": publication_terminal,
            "safe_next_action": safe_next_action,
            "prior_calibration_evidence_authority": "NONE",
            "retroactive_precalibration_time_authority": "NONE",
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "corpus_admission_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        }
    )


def _hold_summary(
    reason_code: str,
    reason: str,
    *,
    record_path_state: str = "UNKNOWN",
    safe_next_action: str = "STOP_AND_REVIEW",
) -> str:
    return record_contract.canonical_json(
        {
            "marker": HANDOFF_MARKER,
            "status": "HOLD",
            "reason_code": reason_code,
            "reason": reason,
            "record_path_state": record_path_state,
            "publication_terminal": "NOT_CONFIRMED",
            "safe_next_action": safe_next_action,
            "prior_calibration_evidence_authority": "NONE",
            "retroactive_precalibration_time_authority": "NONE",
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "corpus_admission_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        }
    )


def _build_parser() -> record_contract.StableArgumentParser:
    parser = record_contract.StableArgumentParser(
        description=(
            "Record, content-validate, or recover a Darwin evaluation precommit without "
            "executing runtime work."
        )
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        parser_class=record_contract.StableArgumentParser,
    )

    record = subparsers.add_parser("record", help="create one immutable local precommit record")
    record.add_argument("--manifest", required=True)
    record.add_argument("--record", required=True)
    record.add_argument("--record-id", required=True)
    record.add_argument("--benchmark-source-sha", required=True)
    record.add_argument("--calibration-base-seed", required=True)
    record.add_argument("--held-out-base-seed", required=True)
    record.add_argument("--concurrency", required=True)
    record.add_argument("--tick-batches", required=True)
    record.add_argument("--samples", required=True)
    record.add_argument("--repetitions", required=True)
    record.add_argument("--workload-profile", required=True, choices=plan_contract.WORKLOAD_PROFILES)

    validate = subparsers.add_parser(
        "validate",
        help="content-only validation; does not establish publication durability",
    )
    validate.add_argument("--manifest", required=True)
    validate.add_argument("--record", required=True)

    recover = subparsers.add_parser(
        "recover",
        help="establish a fresh parent-directory durability terminal for an exact existing record",
    )
    recover.add_argument("--manifest", required=True)
    recover.add_argument("--record", required=True)
    return parser


def _load_manifest(path: str) -> dict[str, object]:
    return split.validate_manifest(
        record_contract._bounded_read_json(Path(path), require_private=False)
    )


def _record_command(args: argparse.Namespace) -> dict[str, object]:
    manifest = _load_manifest(args.manifest)
    evaluation_plan = plan_contract.build_precommitted_evaluation_plan(
        manifest,
        args.benchmark_source_sha,
        record_contract._parse_positive_decimal(
            args.calibration_base_seed,
            "calibration_base_seed",
            split.MAX_RUNTIME_SEED,
        ),
        record_contract._parse_positive_decimal(
            args.held_out_base_seed,
            "held_out_base_seed",
            split.MAX_RUNTIME_SEED,
        ),
        record_contract._parse_csv_positive_decimals(args.concurrency, "concurrency", 8),
        record_contract._parse_csv_positive_decimals(args.tick_batches, "tick_batches", 10_000),
        record_contract._parse_positive_decimal(
            args.samples,
            "samples",
            plan_contract.MAX_SAMPLES,
        ),
        record_contract._parse_positive_decimal(
            args.repetitions,
            "repetitions",
            plan_contract.MAX_REPETITIONS,
        ),
        args.workload_profile,
    )
    record = record_contract.build_record(args.record_id, manifest, evaluation_plan)
    path = Path(args.record)
    write_record_create_only_with_terminal(path, record)
    return record_contract.load_and_validate_record(path, manifest)


def _validate_command(args: argparse.Namespace) -> dict[str, object]:
    manifest = _load_manifest(args.manifest)
    return record_contract.load_and_validate_record(Path(args.record), manifest)


def _recover_command(args: argparse.Namespace) -> dict[str, object]:
    manifest = _load_manifest(args.manifest)
    return recover_existing_record(Path(args.record), manifest)


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(list(argv) if argv is not None else None)
        if args.command == "record":
            record = _record_command(args)
            print(
                _summary(
                    "PRECOMMIT_RECORDED",
                    record,
                    "PARENT_DIRECTORY_FSYNC_CONFIRMED",
                    "CALIBRATION_MAY_START_FROM_THIS_TERMINAL",
                )
            )
        elif args.command == "validate":
            record = _validate_command(args)
            print(
                _summary(
                    "PRECOMMIT_CONTENT_REVALIDATED",
                    record,
                    "CONTENT_ONLY_NOT_PUBLICATION_TERMINAL",
                    "USE_RECOVER_IF_PUBLICATION_TERMINAL_WAS_LOST_OR_UNCERTAIN",
                )
            )
        else:
            record = _recover_command(args)
            print(
                _summary(
                    "PRECOMMIT_RECOVERED",
                    record,
                    "RECOVERY_PARENT_DIRECTORY_FSYNC_CONFIRMED",
                    "RESTART_CALIBRATION_AFTER_THIS_RECOVERY_TERMINAL",
                )
            )
    except record_contract.ArgumentContractError as exc:
        print(_hold_summary("ARGUMENT_ERROR", str(exc)), file=sys.stderr)
        return 2
    except record_contract.NumericArgumentError as exc:
        print(_hold_summary("NUMERIC_ARGUMENT_ERROR", str(exc)), file=sys.stderr)
        return 2
    except PublicationDurabilityUncertain as exc:
        print(
            _hold_summary(
                "PUBLICATION_DURABILITY_UNCERTAIN",
                str(exc),
                record_path_state="CREATE_ONLY_FILE_FSYNCED_PARENT_DURABILITY_UNCONFIRMED",
                safe_next_action="RECOVER_BEFORE_ANY_CALIBRATION",
            ),
            file=sys.stderr,
        )
        return 2
    except (RecoveryError, record_contract.RecordError, split.SplitError, OSError) as exc:
        print(_hold_summary("VALIDATION_ERROR", str(exc)), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
