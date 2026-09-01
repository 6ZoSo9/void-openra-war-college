#!/usr/bin/env python3
"""Create-only operator handoff for Darwin precommitted evaluation plans.

This source-only CLI turns the in-memory precommit contract into a process-independent
artifact. A trainer records one canonical plan before calibration, and any later process
must re-open and validate that exact artifact before interpreting calibration or held-out
results.

The artifact is a local create-only precommit witness, not an external timestamp,
signature, runtime-evidence receipt, or promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Iterable, Mapping

import darwin_heldout_evaluation_split_v1 as split
import darwin_precommitted_evaluation_plan_v1 as plan_contract

MARKER = "VOID_WAR_COLLEGE_PRECOMMITTED_EVALUATION_RECORD_V1"
HANDOFF_MARKER = "VOID_WAR_COLLEGE_PRECOMMIT_OPERATOR_HANDOFF_V1"
SCHEMA_VERSION = 1
MAX_JSON_BYTES = 1_048_576
RECORD_ID_RE = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}\Z")
SHA64_RE = re.compile(r"[0-9a-f]{64}\Z")
POSITIVE_DECIMAL_RE = re.compile(r"[1-9][0-9]*\Z")


class RecordError(ValueError):
    """Raised when the process-independent precommit record fails closed."""


class ArgumentContractError(RecordError):
    """Raised when CLI argument shape fails the machine-readable terminal contract."""


class NumericArgumentError(RecordError):
    """Raised before integer conversion when a decimal token exceeds its field domain."""


class StableArgumentParser(argparse.ArgumentParser):
    """Argument parser whose expected invocation errors remain inside the JSON contract."""

    def error(self, message: str) -> None:
        raise ArgumentContractError(message)


def parse_unique_args(
    parser: StableArgumentParser,
    argv: Iterable[str] | None,
) -> argparse.Namespace:
    """Reject ambiguous repeated long options before any file-system access."""
    tokens = list(argv) if argv is not None else sys.argv[1:]
    seen: set[str] = set()
    for token in tokens:
        if token == "--":
            break
        if not token.startswith("--"):
            continue
        option = token.split("=", 1)[0]
        if option in seen:
            parser.error(f"argument {option}: may not be repeated")
        seen.add(option)
    return parser.parse_args(tokens)


# Retain the historical internal name for imported draft callers while making
# duplicate-option admission one explicit shared public contract.
_parse_unique_args = parse_unique_args


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _validate_record_id(value: object) -> str:
    if not isinstance(value, str) or not RECORD_ID_RE.fullmatch(value):
        raise RecordError(
            "record_id must be 1..64 lowercase [a-z0-9._-] characters and start alphanumeric"
        )
    return value


def _parse_positive_decimal(value: str, label: str, maximum: int) -> int:
    if not isinstance(value, str) or not POSITIVE_DECIMAL_RE.fullmatch(value):
        raise NumericArgumentError(f"{label} must be a canonical positive decimal")
    maximum_text = str(maximum)
    if len(value) > len(maximum_text) or (
        len(value) == len(maximum_text) and value > maximum_text
    ):
        raise NumericArgumentError(f"{label} must be in 1..{maximum}")
    return int(value, 10)


def _parse_csv_positive_decimals(
    value: str,
    label: str,
    maximum: int,
) -> tuple[int, ...]:
    if not value or " " in value or "\t" in value or "\n" in value:
        raise NumericArgumentError(
            f"{label} must be a comma-separated canonical decimal list"
        )
    parts = value.split(",")
    if not all(parts):
        raise NumericArgumentError(
            f"{label} must be a comma-separated canonical decimal list"
        )
    result = tuple(_parse_positive_decimal(part, label, maximum) for part in parts)
    if not result:
        raise NumericArgumentError(f"{label} must not be empty")
    return result


def _bounded_read_json(path: Path, *, require_private: bool) -> dict[str, object]:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise RecordError(f"cannot open {path}: {exc.strerror or exc}") from exc

    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise RecordError(f"{path} must be a regular file")
        if info.st_size <= 0 or info.st_size > MAX_JSON_BYTES:
            raise RecordError(f"{path} must contain 1..{MAX_JSON_BYTES} bytes")
        if require_private:
            if info.st_nlink != 1:
                raise RecordError("precommit record must have exactly one hard link")
            if hasattr(os, "getuid") and info.st_uid != os.getuid():
                raise RecordError("precommit record must be owned by the current uid")
            if stat.S_IMODE(info.st_mode) != 0o600:
                raise RecordError("precommit record mode must be exactly 0600")

        chunks: list[bytes] = []
        remaining = info.st_size
        while remaining:
            chunk = os.read(fd, min(remaining, 65536))
            if not chunk:
                raise RecordError(f"{path} changed or truncated during bounded read")
            chunks.append(chunk)
            remaining -= len(chunk)
        if os.read(fd, 1):
            raise RecordError(f"{path} grew during bounded read")
    finally:
        os.close(fd)

    raw = b"".join(chunks)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RecordError(f"{path} is not valid UTF-8 JSON") from exc
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RecordError(f"{path} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise RecordError(f"{path} JSON must be an object")
    if require_private and raw != (canonical_json(value) + "\n").encode("utf-8"):
        raise RecordError("precommit record bytes are not canonical JSON plus one newline")
    return value


def build_record(
    record_id: object,
    manifest: Mapping[str, object],
    evaluation_plan: Mapping[str, object],
) -> dict[str, object]:
    rid = _validate_record_id(record_id)
    verified_manifest = split.validate_manifest(manifest)
    if not isinstance(evaluation_plan, Mapping):
        raise RecordError("evaluation_plan must be an object")
    plan_digest = evaluation_plan.get("plan_digest")
    if not isinstance(plan_digest, str) or not SHA64_RE.fullmatch(plan_digest):
        raise RecordError("evaluation plan digest must be exactly 64 lowercase hex characters")
    verified_plan = plan_contract.validate_precommitted_evaluation_plan(
        evaluation_plan,
        verified_manifest,
        plan_digest,
    )

    core: dict[str, object] = {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "record_id": rid,
        "plan_digest": verified_plan["plan_digest"],
        "split_digest": verified_plan["split_digest"],
        "benchmark_source_sha": verified_plan["shared_parameters"]["benchmark_source_sha"],
        "engine_frozen_commit": verified_plan["engine_frozen_commit"],
        "war_college_comparison_point": verified_plan["war_college_comparison_point"],
        "generation": verified_plan["generation"],
        "plan": verified_plan,
        "record_policy": {
            "recorded_before_calibration_required": True,
            "create_only_publication": True,
            "overwrite_authority": "NONE",
            "delete_replace_authority": "NONE",
            "external_timestamp_authority": "NONE",
            "signature_authority": "NONE",
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "corpus_admission_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        },
    }
    return {**core, "record_digest": _sha256_json(core)}


def validate_record(
    record: Mapping[str, object],
    manifest: Mapping[str, object],
) -> dict[str, object]:
    if not isinstance(record, Mapping):
        raise RecordError("record must be an object")
    expected_keys = {
        "marker",
        "schema_version",
        "record_id",
        "plan_digest",
        "split_digest",
        "benchmark_source_sha",
        "engine_frozen_commit",
        "war_college_comparison_point",
        "generation",
        "plan",
        "record_policy",
        "record_digest",
    }
    if set(record) != expected_keys:
        raise RecordError("record keys are not schema-exact")
    if record["marker"] != MARKER or record["schema_version"] != SCHEMA_VERSION:
        raise RecordError("record marker/schema mismatch")
    rid = _validate_record_id(record["record_id"])
    if not isinstance(record["plan_digest"], str) or not SHA64_RE.fullmatch(record["plan_digest"]):
        raise RecordError("record plan_digest is invalid")
    if not isinstance(record["record_digest"], str) or not SHA64_RE.fullmatch(record["record_digest"]):
        raise RecordError("record_digest is invalid")

    verified_manifest = split.validate_manifest(manifest)
    verified_plan = plan_contract.validate_precommitted_evaluation_plan(
        record["plan"],
        verified_manifest,
        record["plan_digest"],
    )
    rebuilt = build_record(rid, verified_manifest, verified_plan)
    if canonical_json(rebuilt) != canonical_json(dict(record)):
        raise RecordError("record content is not canonical for the precommitted plan")
    return rebuilt


def _fsync_parent(path: Path) -> None:
    parent = path.parent if str(path.parent) else Path(".")
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(parent, flags)
    except OSError as exc:
        raise RecordError(f"cannot open record parent directory: {exc.strerror or exc}") from exc
    try:
        os.fsync(fd)
    except OSError as exc:
        raise RecordError(f"cannot fsync record parent directory: {exc.strerror or exc}") from exc
    finally:
        os.close(fd)


def write_record_create_only(path: Path, record: Mapping[str, object]) -> None:
    payload = (canonical_json(record) + "\n").encode("utf-8")
    if not payload or len(payload) > MAX_JSON_BYTES:
        raise RecordError(f"record payload exceeds {MAX_JSON_BYTES} bytes")

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise RecordError("record path already exists; create-only precommit refused") from exc
    except OSError as exc:
        raise RecordError(f"cannot create precommit record: {exc.strerror or exc}") from exc

    try:
        offset = 0
        while offset < len(payload):
            written = os.write(fd, payload[offset:])
            if written <= 0:
                raise RecordError("short write while publishing precommit record")
            offset += written
        os.fsync(fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise RecordError("published precommit record is not a regular file")
        if info.st_nlink != 1:
            raise RecordError("published precommit record must have exactly one hard link")
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise RecordError("published precommit record must be owned by the current uid")
        if stat.S_IMODE(info.st_mode) != 0o600:
            raise RecordError("published precommit record mode must be exactly 0600")
        if info.st_size != len(payload):
            raise RecordError("published precommit record size mismatch")
    finally:
        os.close(fd)

    _fsync_parent(path)


def load_and_validate_record(path: Path, manifest: Mapping[str, object]) -> dict[str, object]:
    return validate_record(_bounded_read_json(path, require_private=True), manifest)


def _summary(status: str, record: Mapping[str, object]) -> str:
    return canonical_json(
        {
            "marker": HANDOFF_MARKER,
            "status": status,
            "record_id": record["record_id"],
            "record_digest": record["record_digest"],
            "plan_digest": record["plan_digest"],
            "split_digest": record["split_digest"],
            "benchmark_source_sha": record["benchmark_source_sha"],
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "corpus_admission_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        }
    )


def _hold_summary(reason_code: str, reason: str) -> str:
    return canonical_json(
        {
            "marker": HANDOFF_MARKER,
            "status": "HOLD",
            "reason_code": reason_code,
            "reason": reason,
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "corpus_admission_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        }
    )


def _build_parser() -> StableArgumentParser:
    parser = StableArgumentParser(
        description="Record or revalidate a Darwin evaluation precommit without executing runtime work."
    )
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        parser_class=StableArgumentParser,
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
        "validate", help="fresh-process restart/resume validation of an existing record"
    )
    validate.add_argument("--manifest", required=True)
    validate.add_argument("--record", required=True)
    return parser


def _record_command(args: argparse.Namespace) -> dict[str, object]:
    manifest = split.validate_manifest(
        _bounded_read_json(Path(args.manifest), require_private=False)
    )
    evaluation_plan = plan_contract.build_precommitted_evaluation_plan(
        manifest,
        args.benchmark_source_sha,
        _parse_positive_decimal(
            args.calibration_base_seed,
            "calibration_base_seed",
            split.MAX_RUNTIME_SEED,
        ),
        _parse_positive_decimal(
            args.held_out_base_seed,
            "held_out_base_seed",
            split.MAX_RUNTIME_SEED,
        ),
        _parse_csv_positive_decimals(args.concurrency, "concurrency", 8),
        _parse_csv_positive_decimals(args.tick_batches, "tick_batches", 10_000),
        _parse_positive_decimal(args.samples, "samples", plan_contract.MAX_SAMPLES),
        _parse_positive_decimal(
            args.repetitions,
            "repetitions",
            plan_contract.MAX_REPETITIONS,
        ),
        args.workload_profile,
    )
    record = build_record(args.record_id, manifest, evaluation_plan)
    record_path = Path(args.record)
    write_record_create_only(record_path, record)
    return load_and_validate_record(record_path, manifest)


def _validate_command(args: argparse.Namespace) -> dict[str, object]:
    manifest = split.validate_manifest(
        _bounded_read_json(Path(args.manifest), require_private=False)
    )
    return load_and_validate_record(Path(args.record), manifest)


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_parser()
    try:
        args = parse_unique_args(parser, argv)
        if args.command == "record":
            record = _record_command(args)
            print(_summary("PRECOMMIT_RECORDED", record))
        else:
            record = _validate_command(args)
            print(_summary("PRECOMMIT_REVALIDATED", record))
    except ArgumentContractError as exc:
        print(_hold_summary("ARGUMENT_ERROR", str(exc)), file=sys.stderr)
        return 2
    except NumericArgumentError as exc:
        print(_hold_summary("NUMERIC_ARGUMENT_ERROR", str(exc)), file=sys.stderr)
        return 2
    except (RecordError, split.SplitError, OSError) as exc:
        print(_hold_summary("VALIDATION_ERROR", str(exc)), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
