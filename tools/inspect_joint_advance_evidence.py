#!/usr/bin/env python3
from __future__ import annotations

import argparse
import errno
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


class InspectionFailure(bench.ContractError):
    """A read-only inspection failure with a stable automation reason code."""

    def __init__(self, reason_code: str, detail: str) -> None:
        self.reason_code = reason_code
        super().__init__(detail)


def _inspection_error_report(path: Path, error: BaseException) -> dict[str, Any]:
    if isinstance(error, InspectionFailure):
        reason_code = error.reason_code
    elif isinstance(error, PermissionError):
        reason_code = "NAMESPACE_ACCESS_DENIED"
    elif isinstance(error, FileNotFoundError):
        reason_code = "NAMESPACE_ENTRY_NOT_FOUND"
    elif isinstance(error, OSError):
        reason_code = "NAMESPACE_ACQUISITION_FAILED"
    else:
        reason_code = "INSPECTION_CONTRACT_ERROR"
    return {
        "marker": INSPECTION_MARKER,
        "schema_version": INSPECTION_SCHEMA_VERSION,
        "output_path": str(Path(os.path.abspath(os.fspath(path)))),
        "classification": "INSPECTION_ERROR_HOLD",
        "reason_code": reason_code,
        "error_type": type(error).__name__,
        "artifacts_inspected": False,
        "artifact_authority": "NONE",
        "countable": False,
        "producer_authentication": "ABSENT",
        "inspection_read_only": True,
        "automatic_recovery": False,
        "automatic_delete": False,
        "automatic_link": False,
        "automatic_rewrite": False,
        "namespace_generation_stable": False,
    }


def _generation_from_stat(metadata: os.stat_result) -> dict[str, Any]:
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


def _generation(path: Path) -> dict[str, Any] | None:
    try:
        return _generation_from_stat(path.lstat())
    except FileNotFoundError:
        return None


def _read_descriptor(descriptor: int) -> bytes:
    before = _generation_from_stat(os.fstat(descriptor))
    chunks: list[bytes] = []
    offset = 0
    while True:
        chunk = os.pread(descriptor, 64 * 1024, offset)
        if not chunk:
            break
        chunks.append(chunk)
        offset += len(chunk)
        if offset > bench.MAX_EVIDENCE_BYTES:
            raise bench.ContractError(
                f"evidence artifact exceeds {bench.MAX_EVIDENCE_BYTES} bytes"
            )
    after = _generation_from_stat(os.fstat(descriptor))
    if before != after or offset != before["size"]:
        raise bench.ContractError("evidence artifact changed while its retained fd was read")
    return b"".join(chunks)


def _open_artifact_descriptor(parent_descriptor: int, name: str) -> int:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        return os.open(name, flags, dir_fd=parent_descriptor)
    except OSError as error:
        if error.errno != errno.ELOOP or not hasattr(os, "O_PATH"):
            raise
        return os.open(
            name,
            os.O_PATH | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=parent_descriptor,
        )


def _matrix_summary(
    report: dict[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    cells_by_key = {cell["key"]: cell for cell in report["cells"]}
    planned_keys = [
        f"c{planned['concurrency']}-t{planned['ticks_per_joint_advance']}"
        for planned in bench.build_matrix(
            tuple(report["parameters"]["concurrency"]),
            tuple(report["parameters"]["tick_batches"]),
        )
    ]
    ordered_cells = [
        cells_by_key[key] for key in planned_keys if key in cells_by_key
    ]
    missing_keys = [key for key in planned_keys if key not in cells_by_key]
    first_non_success = next(
        (
            {"key": cell["key"], "terminal": cell["terminal"]}
            for cell in ordered_cells
            if cell["terminal"] != "success"
        ),
        None,
    )
    first_incomplete = next(
        (
            {"key": key, "state": "missing"}
            if key not in cells_by_key
            else {
                "key": key,
                "state": "present",
                "terminal": cells_by_key[key]["terminal"],
            }
            for key in planned_keys
            if key not in cells_by_key
            or cells_by_key[key]["terminal"] != "success"
        ),
        None,
    )
    return (
        [cell["terminal"] for cell in ordered_cells],
        {
            "planned_cell_count": len(planned_keys),
            "cell_count": len(ordered_cells),
            "missing_cell_count": len(missing_keys),
            "first_missing": missing_keys[0] if missing_keys else None,
            "first_incomplete": first_incomplete,
            "success_count": sum(
                cell["terminal"] == "success" for cell in ordered_cells
            ),
            "non_success_count": sum(
                cell["terminal"] != "success" for cell in ordered_cells
            ),
            "blocked_cell_count": sum(
                cell["terminal"] == "not_executed" for cell in ordered_cells
            ),
            "first_non_success": first_non_success,
        },
    )


def _artifact(
    parent_descriptor: int,
    name: str,
    path: Path,
    *,
    validate_report: bool = False,
) -> tuple[dict[str, Any], bytes | None, int | None]:
    try:
        descriptor = _open_artifact_descriptor(parent_descriptor, name)
    except FileNotFoundError:
        return {"present": False, "path": str(path)}, None, None

    generation = _generation_from_stat(os.fstat(descriptor))

    row: dict[str, Any] = {
        "present": True,
        "path": str(path),
        "generation": generation,
        "read_only": True,
        "payload_sha256": None,
        "payload_bytes": None,
        "report_schema_valid": None,
        "report_schema_compatible": None,
        "report_schema_version": None,
        "report_terminal": None,
        "report_cell_terminals": None,
        "report_matrix_summary": None,
        "validation_error": None,
    }
    if not generation["regular_file"] or generation["symlink"]:
        row["validation_error"] = "ARTIFACT_NOT_REGULAR_FILE"
        return row, None, descriptor
    if generation["mode"] != 0o400:
        row["validation_error"] = "ARTIFACT_MODE_NOT_0400"
        return row, None, descriptor

    try:
        payload = _read_descriptor(descriptor)
    except (OSError, bench.ContractError) as error:
        row["validation_error"] = f"{type(error).__name__}:{error}"
        return row, None, descriptor

    row["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    row["payload_bytes"] = len(payload)
    if validate_report:
        if not payload:
            row["report_schema_valid"] = False
            row["validation_error"] = "EMPTY_PENDING_RESERVATION"
        else:
            try:
                report = bench._validate_recoverable_evidence(payload)
            except bench.IncompatibleEvidenceSchemaError as error:
                row["report_schema_valid"] = False
                row["report_schema_compatible"] = False
                row["report_schema_version"] = error.actual
                row["validation_error"] = f"INCOMPATIBLE_SCHEMA_HOLD:{error}"
            except (OSError, bench.ContractError) as error:
                row["report_schema_valid"] = False
                row["validation_error"] = f"{type(error).__name__}:{error}"
            else:
                row["report_schema_valid"] = True
                row["report_schema_compatible"] = True
                row["report_schema_version"] = report["schema_version"]
                row["report_terminal"] = report["run"]["terminal"]
                (
                    row["report_cell_terminals"],
                    row["report_matrix_summary"],
                ) = _matrix_summary(report)
    return row, payload, descriptor


def _require_retained_namespace_stable(
    parent_path: Path,
    parent_descriptor: int,
    artifacts: tuple[tuple[str, dict[str, Any], int | None], ...],
) -> None:
    retained_parent_metadata = os.fstat(parent_descriptor)
    retained_parent = _generation_from_stat(retained_parent_metadata)
    try:
        canonical_parent_metadata = parent_path.lstat()
        canonical_parent = _generation_from_stat(canonical_parent_metadata)
    except FileNotFoundError as error:
        raise InspectionFailure(
            "NAMESPACE_GENERATION_UNSTABLE",
            "evidence output parent disappeared during read-only inspection"
        ) from error
    if (
        not stat.S_ISDIR(retained_parent_metadata.st_mode)
        or not os.path.samestat(retained_parent_metadata, canonical_parent_metadata)
        or retained_parent != canonical_parent
    ):
        raise InspectionFailure(
            "NAMESPACE_GENERATION_UNSTABLE",
            "evidence output parent changed generation during read-only inspection"
        )

    for name, row, descriptor in artifacts:
        if descriptor is None:
            try:
                os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            except FileNotFoundError:
                continue
            raise InspectionFailure(
                "NAMESPACE_GENERATION_UNSTABLE",
                f"evidence artifact {name} appeared during read-only inspection"
            )
        try:
            named = _generation_from_stat(
                os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
            )
        except FileNotFoundError as error:
            raise InspectionFailure(
                "NAMESPACE_GENERATION_UNSTABLE",
                f"evidence artifact {name} disappeared during read-only inspection"
            ) from error
        opened = _generation_from_stat(os.fstat(descriptor))
        if row.get("generation") != opened or named != opened:
            raise InspectionFailure(
                "NAMESPACE_GENERATION_UNSTABLE",
                f"evidence artifact {name} changed generation during read-only inspection"
            )


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

    primary_report = final if has_final else pending
    if primary_report.get("report_schema_compatible") is False:
        return "INCOMPATIBLE_SCHEMA_HOLD"
    if not has_final and not has_pending and not has_receipt:
        return "EMPTY"
    if has_receipt and not has_final:
        return "RECEIPT_WITHOUT_FINAL_HOLD"
    if has_final and has_receipt and receipt_binds_final:
        if final.get("report_schema_valid") is not True:
            return "CURRENT_SCHEMA_INVALID_HOLD"
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
    parent_path = path.parent
    parent_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(parent_path, parent_flags)
    except FileNotFoundError as error:
        raise InspectionFailure(
            "OUTPUT_PARENT_NOT_FOUND", "evidence output parent does not exist"
        ) from error
    except NotADirectoryError as error:
        raise InspectionFailure(
            "OUTPUT_PARENT_NOT_DIRECTORY", "evidence output parent is not a directory"
        ) from error
    except PermissionError as error:
        raise InspectionFailure(
            "OUTPUT_PARENT_ACCESS_DENIED", "evidence output parent cannot be inspected"
        ) from error
    except OSError as error:
        raise InspectionFailure(
            "OUTPUT_PARENT_OPEN_FAILED", "evidence output parent could not be opened"
        ) from error
    descriptors: list[int] = []
    try:
        final, final_payload, final_descriptor = _artifact(
            parent_descriptor, path.name, path, validate_report=True,
        )
        if final_descriptor is not None:
            descriptors.append(final_descriptor)
        pending, pending_payload, pending_descriptor = _artifact(
            parent_descriptor, pending_path.name, pending_path, validate_report=True,
        )
        if pending_descriptor is not None:
            descriptors.append(pending_descriptor)
        receipt, receipt_payload, receipt_descriptor = _artifact(
            parent_descriptor, receipt_path.name, receipt_path, validate_report=False,
        )
        if receipt_descriptor is not None:
            descriptors.append(receipt_descriptor)

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

        _require_retained_namespace_stable(
            parent_path,
            parent_descriptor,
            (
                (path.name, final, final_descriptor),
                (pending_path.name, pending, pending_descriptor),
                (receipt_path.name, receipt, receipt_descriptor),
            ),
        )

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
    finally:
        for descriptor in descriptors:
            os.close(descriptor)
        os.close(parent_descriptor)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only classifier for interrupted JointAdvance evidence namespaces."
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    output_path = Path(args.output)
    try:
        report = inspect_namespace(output_path)
    except (OSError, bench.ContractError) as error:
        report = _inspection_error_report(output_path, error)
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        print(
            f"VOID_WAR_COLLEGE_EVIDENCE_INSPECTION_HOLD:"
            f"{report['reason_code']}:{report['error_type']}",
            file=sys.stderr,
        )
        return 2
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
