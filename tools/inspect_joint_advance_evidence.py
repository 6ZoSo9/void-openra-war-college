#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import bench_joint_advance as bench

INSPECTION_MARKER = "VOID_WAR_COLLEGE_EVIDENCE_INSPECTION_V1"
INSPECTION_SCHEMA_VERSION = 1


def _generation(path: Path) -> dict[str, Any] | None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return None
    return {
        "device": metadata.st_dev,
        "inode": metadata.st_ino,
        "mode": stat.S_IMODE(metadata.st_mode),
        "size": metadata.st_size,
        "mtime_ns": metadata.st_mtime_ns,
        "ctime_ns": metadata.st_ctime_ns,
        "regular_file": stat.S_ISREG(metadata.st_mode),
        "symlink": stat.S_ISLNK(metadata.st_mode),
    }


def _artifact(path: Path, *, validate_report: bool = False) -> tuple[dict[str, Any], bytes | None]:
    generation = _generation(path)
    if generation is None:
        return {"present": False, "path": str(path)}, None

    row: dict[str, Any] = {
        "present": True,
        "path": str(path),
        "generation": generation,
        "read_only": True,
        "payload_sha256": None,
        "payload_bytes": None,
        "report_schema_valid": None,
        "report_terminal": None,
        "validation_error": None,
    }
    if not generation["regular_file"] or generation["symlink"]:
        row["validation_error"] = "ARTIFACT_NOT_REGULAR_FILE"
        return row, None
    if generation["mode"] != 0o400:
        row["validation_error"] = "ARTIFACT_MODE_NOT_0400"
        return row, None

    try:
        payload = bench._read_regular_read_only(path)
    except (OSError, bench.ContractError) as error:
        row["validation_error"] = f"{type(error).__name__}:{error}"
        return row, None

    row["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    row["payload_bytes"] = len(payload)
    if validate_report:
        if not payload:
            row["report_schema_valid"] = False
            row["validation_error"] = "EMPTY_PENDING_RESERVATION"
        else:
            try:
                report = bench._validate_recoverable_evidence(payload)
            except (OSError, bench.ContractError) as error:
                row["report_schema_valid"] = False
                row["validation_error"] = f"{type(error).__name__}:{error}"
            else:
                row["report_schema_valid"] = True
                row["report_terminal"] = report["run"]["terminal"]
    return row, payload


def _pending_aliases_final(
    final: dict[str, Any],
    pending: dict[str, Any],
) -> bool:
    final_generation = final.get("generation")
    pending_generation = pending.get("generation")
    if not isinstance(final_generation, dict) or not isinstance(pending_generation, dict):
        return False
    same_inode = (
        final_generation.get("device") == pending_generation.get("device")
        and final_generation.get("inode") == pending_generation.get("inode")
    )
    same_payload = (
        final.get("payload_sha256") is not None
        and final.get("payload_sha256") == pending.get("payload_sha256")
        and final.get("payload_bytes") == pending.get("payload_bytes")
    )
    return bool(same_inode and same_payload)


def _classify(
    *,
    final: dict[str, Any],
    pending: dict[str, Any],
    receipt: dict[str, Any],
    receipt_binds_final: bool,
    pending_aliases_final: bool,
) -> str:
    has_final = bool(final["present"])
    has_pending = bool(pending["present"])
    has_receipt = bool(receipt["present"])

    if not has_final and not has_pending and not has_receipt:
        return "EMPTY"
    if has_receipt and not has_final:
        return "RECEIPT_WITHOUT_FINAL_HOLD"
    if has_final and has_receipt and receipt_binds_final:
        if not has_pending:
            return "COMMITTED_LOCAL_UNTRUSTED"
        if pending_aliases_final:
            return "COMMITTED_LOCAL_UNTRUSTED_WITH_PENDING_ALIAS"
        return "COMMITTED_LOCAL_UNTRUSTED_WITH_FOREIGN_PENDING_HOLD"
    if has_final and has_receipt:
        return "FINAL_RECEIPT_BINDING_MISMATCH_HOLD"
    if has_final and has_pending:
        return "FINAL_AND_PENDING_WITHOUT_RECEIPT"
    if has_final:
        return "FINAL_WITHOUT_RECEIPT"
    if has_pending:
        if pending.get("payload_bytes") == 0:
            return "PENDING_RESERVATION_ONLY"
        return "PENDING_REPORT_ONLY"
    return "UNCLASSIFIED_HOLD"


def inspect_namespace(path: Path) -> dict[str, Any]:
    path = Path(os.path.abspath(os.fspath(path)))
    pending_path = bench._pending_path(path)
    receipt_path = bench._commit_receipt_path(path)
    paths = (path, pending_path, receipt_path)
    before = {str(candidate): _generation(candidate) for candidate in paths}

    final, final_payload = _artifact(path, validate_report=True)
    pending, pending_payload = _artifact(pending_path, validate_report=True)
    receipt, receipt_payload = _artifact(receipt_path, validate_report=False)

    receipt_binds_final = False
    receipt_validation_error: str | None = None
    if receipt_payload is not None and final_payload is not None:
        try:
            bench._validate_commit_receipt(receipt_payload, path, final_payload)
        except (OSError, bench.ContractError) as error:
            receipt_validation_error = f"{type(error).__name__}:{error}"
        else:
            receipt_binds_final = True
    elif receipt["present"]:
        receipt_validation_error = "FINAL_PAYLOAD_UNAVAILABLE"

    after = {str(candidate): _generation(candidate) for candidate in paths}
    if before != after:
        raise bench.ContractError("evidence namespace changed during read-only inspection")

    pending_aliases_final = _pending_aliases_final(final, pending)
    classification = _classify(
        final=final,
        pending=pending,
        receipt=receipt,
        receipt_binds_final=receipt_binds_final,
        pending_aliases_final=pending_aliases_final,
    )
    return {
        "marker": INSPECTION_MARKER,
        "schema_version": INSPECTION_SCHEMA_VERSION,
        "output_path": str(path),
        "classification": classification,
        "final": final,
        "pending": pending,
        "commit_receipt": receipt,
        "commit_receipt_binds_final": receipt_binds_final,
        "commit_receipt_validation_error": receipt_validation_error,
        "pending_aliases_final": pending_aliases_final,
        "countable": False,
        "producer_authentication": "ABSENT",
        "inspection_read_only": True,
        "automatic_recovery": False,
        "automatic_delete": False,
        "automatic_link": False,
        "automatic_rewrite": False,
        "namespace_generation_stable": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only classifier for interrupted JointAdvance evidence namespaces."
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        report = inspect_namespace(Path(args.output))
    except (OSError, bench.ContractError) as error:
        print(f"VOID_WAR_COLLEGE_EVIDENCE_INSPECTION_HOLD: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
