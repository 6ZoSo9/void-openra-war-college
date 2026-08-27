#!/usr/bin/env python3
"""Bounded JointAdvance throughput and resource benchmark for VOID War College.

The module is deliberately importable without grpc or generated protobuf modules so
its source-only contracts can be tested on hosts without the OpenRA runtime. Runtime
imports occur only after ``run`` receives the explicit designated-host attestation.
"""

from __future__ import annotations

import argparse
import asyncio
import ctypes
import ctypes.util
import hashlib
import json
import math
import os
import platform
import re
import socket
import stat
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Iterable


MARKER = "VOID_WAR_COLLEGE_JOINT_ADVANCE_BENCHMARK_V1"
SCHEMA_VERSION = 1
OPERATION_SCHEMA = "void.war-college.joint-advance-operation.v1"
FROZEN_ENGINE_SHA = "1607a7a6501d42a47638393ecef8b22831064932"
FROZEN_WAR_COLLEGE_SHA = "973802ef0a614e5afa782ff20e231e18966ae3e5"
GENERATION = "ad1926569b12466c"
ALLOWED_CONCURRENCY = (1, 2, 4, 8)
ALLOWED_TERMINALS = {
    "success", "timeout", "rpc_error", "teardown_error", "not_executed",
}
RUN_TERMINALS = {
    "startup_error", "readiness_timeout", "channel_error", "cleanup_error",
    "output_error", "completed",
}
MAP_NAME = "singles.oramap"
BOTS = "Multi1:rl-agent,Multi0:rl-agent"
MAX_DAEMON_LOG_TAIL_BYTES = 65_536
MAX_EVIDENCE_BYTES = 16 * 1024 * 1024
TRANSIENT_KEYS = {"session_id", "episode_id", "transport_id", "request_id"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
GENERATION_RE = re.compile(r"^[0-9a-f]{16}$")
CANONICAL_POSITIVE_INT = re.compile(r"^[1-9][0-9]*$")


class ContractError(ValueError):
    """Raised when benchmark input or evidence violates the source contract."""


def require_sha40(value: str, label: str) -> str:
    if not SHA40.fullmatch(value):
        raise ContractError(f"{label} must be exactly 40 lowercase hex characters")
    return value


def parse_int_csv(
    raw: str,
    *,
    label: str,
    minimum: int,
    maximum: int,
    allowed: Iterable[int] | None = None,
) -> tuple[int, ...]:
    parts = raw.split(",")
    if not parts or any(not CANONICAL_POSITIVE_INT.fullmatch(part) for part in parts):
        raise ContractError(f"{label} must be canonical comma-separated positive integers")
    values = tuple(int(part) for part in parts)
    if len(set(values)) != len(values):
        raise ContractError(f"{label} must not contain duplicates")
    if any(value < minimum or value > maximum for value in values):
        raise ContractError(f"{label} must stay within [{minimum}, {maximum}]")
    if allowed is not None:
        allowed_set = set(allowed)
        if any(value not in allowed_set for value in values):
            raise ContractError(f"{label} contains an unsupported value")
    return values


def positive_int(raw: str, *, label: str, minimum: int, maximum: int) -> int:
    if not CANONICAL_POSITIVE_INT.fullmatch(raw):
        raise ContractError(f"{label} must be a canonical positive integer")
    value = int(raw)
    if value < minimum or value > maximum:
        raise ContractError(f"{label} must stay within [{minimum}, {maximum}]")
    return value


def percentile_nearest_rank(values: Iterable[float], percentile: float) -> float:
    samples = sorted(float(value) for value in values)
    if not samples:
        raise ContractError("percentile requires at least one sample")
    if not math.isfinite(percentile) or percentile < 0 or percentile > 100:
        raise ContractError("percentile must stay within [0, 100]")
    if percentile == 0:
        return samples[0]
    rank = math.ceil((percentile / 100) * len(samples))
    return samples[rank - 1]


def latency_summary(values: Iterable[float]) -> dict[str, float | int]:
    samples = [float(value) for value in values]
    if not samples:
        return {"count": 0}
    if any(not math.isfinite(value) or value < 0 for value in samples):
        raise ContractError("latency samples must be finite and nonnegative")
    return {
        "count": len(samples),
        "min_ms": min(samples),
        "p50_ms": percentile_nearest_rank(samples, 50),
        "p95_ms": percentile_nearest_rank(samples, 95),
        "max_ms": max(samples),
    }


def canonicalize_state(value: Any) -> Any:
    """Remove transport/session identity while preserving perspective and game state."""
    if isinstance(value, dict):
        return {
            key: canonicalize_state(value[key])
            for key in sorted(value)
            if key not in TRANSIENT_KEYS
        }
    if isinstance(value, list):
        return [canonicalize_state(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ContractError("canonical state contains a non-finite float")
        return value
    if value is None or isinstance(value, (bool, int, str)):
        return value
    raise ContractError(f"unsupported canonical state type: {type(value).__name__}")


def canonical_state_hash(value: Any) -> str:
    encoded = json.dumps(
        canonicalize_state(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_matrix(concurrency: tuple[int, ...], tick_batches: tuple[int, ...]) -> list[dict[str, int]]:
    cells = [
        {"concurrency": sessions, "ticks_per_joint_advance": ticks}
        for sessions in concurrency
        for ticks in tick_batches
    ]
    if not cells or len(cells) > 64:
        raise ContractError("benchmark matrix must contain between 1 and 64 cells")
    return cells


def matrix_may_continue(terminal: str) -> bool:
    if terminal not in ALLOWED_TERMINALS:
        raise ContractError(f"unsupported cell terminal: {terminal}")
    # Any other terminal can leave unknown or failed-to-destroy server state.
    # Stop and retire the disposable daemon instead of contaminating later cells.
    return terminal == "success"


def terminal_exit_code(report: dict[str, Any]) -> int:
    if report["run"]["terminal"] != "completed":
        return 1
    return 0 if all(cell["terminal"] == "success" for cell in report["cells"]) else 1


@dataclass(frozen=True)
class FinalCell:
    key: str
    terminal: str
    payload: dict[str, Any]


class CellLedger:
    """Exactly-once publication of immutable matrix-cell terminals."""

    def __init__(self) -> None:
        self._cells: dict[str, FinalCell] = {}

    def finalize(self, key: str, terminal: str, payload: dict[str, Any]) -> FinalCell:
        if terminal not in ALLOWED_TERMINALS:
            raise ContractError(f"unsupported cell terminal: {terminal}")
        if key in self._cells:
            raise ContractError(f"cell {key} already has a terminal")
        frozen = FinalCell(key=key, terminal=terminal, payload=json.loads(json.dumps(payload)))
        self._cells[key] = frozen
        return frozen

    def values(self) -> tuple[FinalCell, ...]:
        return tuple(self._cells[key] for key in sorted(self._cells))


async def retire_phase_tasks(
    operations: dict[str, Awaitable[Any]],
    *,
    deadline_s: float,
) -> CellLedger:
    """Publish immutable terminals, then retire every task before returning.

    This source-only helper is also the executable proof for the phase rule: a
    task completing after the monotonic deadline cannot rewrite its timeout, and
    no caller can start another phase until every old task has been consumed.
    """
    if not operations:
        raise ContractError("phase requires at least one operation")
    if not math.isfinite(deadline_s) or deadline_s <= 0:
        raise ContractError("phase deadline must be finite and positive")
    tasks = {key: asyncio.create_task(operation) for key, operation in operations.items()}
    reverse = {task: key for key, task in tasks.items()}
    done, pending = await asyncio.wait(tasks.values(), timeout=deadline_s)
    ledger = CellLedger()
    for task in done:
        key = reverse[task]
        try:
            task.result()
            ledger.finalize(key, "success", {})
        except Exception as error:
            ledger.finalize(key, "rpc_error", {
                "error_type": type(error).__name__,
                "error": str(error),
            })
    for task in pending:
        ledger.finalize(reverse[task], "timeout", {"deadline_seconds": deadline_s})
        task.cancel()
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)
    return ledger


async def run_owned_phase(
    operations: dict[str, Awaitable[Any]],
    *,
    deadline_s: float,
) -> dict[str, Any]:
    """Return keyed results only after every phase task is retired.

    On the first exception or the shared deadline, every unfinished sibling is
    cancelled and awaited before the exception escapes.  Callers may therefore
    begin teardown only after no create/advance operation can still mutate the
    runtime or its ownership ledger.
    """
    if not operations:
        raise ContractError("owned phase requires at least one operation")
    if not math.isfinite(deadline_s) or deadline_s <= 0:
        raise ContractError("owned phase deadline must be finite and positive")
    tasks = {key: asyncio.create_task(operation) for key, operation in operations.items()}
    try:
        done, pending = await asyncio.wait(
            tasks.values(), timeout=deadline_s, return_when=asyncio.FIRST_EXCEPTION,
        )
        failure: BaseException | None = None
        for key in sorted(tasks):
            task = tasks[key]
            if task in done and not task.cancelled():
                error = task.exception()
                if error is not None:
                    failure = error
                    break
        if failure is not None or pending:
            for task in pending:
                task.cancel()
            await asyncio.gather(*tasks.values(), return_exceptions=True)
            if failure is not None:
                raise failure
            raise asyncio.TimeoutError(f"owned phase exceeded {deadline_s}s")
        return {key: tasks[key].result() for key in sorted(tasks)}
    finally:
        unfinished = [task for task in tasks.values() if not task.done()]
        for task in unfinished:
            task.cancel()
        if unfinished:
            await asyncio.gather(*unfinished, return_exceptions=True)


def validate_provenance(
    engine_sha: str,
    war_college_sha: str,
    benchmark_source_sha: str,
    generation: str,
) -> dict[str, str]:
    require_sha40(engine_sha, "engine SHA")
    require_sha40(war_college_sha, "War College SHA")
    require_sha40(benchmark_source_sha, "benchmark source SHA")
    if not GENERATION_RE.fullmatch(generation):
        raise ContractError("generation must be exactly 16 lowercase hex characters")
    if engine_sha != FROZEN_ENGINE_SHA:
        raise ContractError("engine SHA is not the reviewed frozen generation")
    if war_college_sha != FROZEN_WAR_COLLEGE_SHA:
        raise ContractError("War College SHA is not the reviewed frozen generation")
    if generation != GENERATION:
        raise ContractError("generation is not the reviewed benchmark generation")
    return {
        "engine_sha": engine_sha,
        "war_college_sha": war_college_sha,
        "benchmark_source_sha": benchmark_source_sha,
        "generation": generation,
        "frozen_engine_sha": FROZEN_ENGINE_SHA,
        "frozen_war_college_sha": FROZEN_WAR_COLLEGE_SHA,
    }


def build_report(
    *,
    provenance: dict[str, str],
    parameters: dict[str, Any],
    cells: list[dict[str, Any]],
    executed_designated_host: bool,
    generated_at_utc: str,
    command: list[str],
    run: dict[str, Any] | None = None,
    host: dict[str, Any] | None = None,
    operation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runtime_evidence = "EXECUTED" if executed_designated_host else "PENDING_DESIGNATED_HOST"
    if not executed_designated_host and cells:
        raise ContractError("source-only evidence must not contain measured runtime cells")
    if not executed_designated_host and run is not None:
        raise ContractError("source-only evidence must not contain a runtime attempt terminal")
    if executed_designated_host:
        validate_operation(operation)
        if not isinstance(run, dict) or run.get("terminal") not in RUN_TERMINALS:
            raise ContractError("executed runtime evidence requires an exact run terminal")
        if run["terminal"] == "completed" and not cells:
            raise ContractError("completed runtime evidence requires terminal matrix cells")
    for cell in cells:
        if cell.get("terminal") not in ALLOWED_TERMINALS:
            raise ContractError("report contains an invalid matrix-cell terminal")
    report = {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "runtime_evidence": runtime_evidence,
        "generated_at_utc": generated_at_utc,
        "provenance": provenance,
        "command": command,
        "host": host if executed_designated_host else None,
        "run": run if executed_designated_host else None,
        "parameters": parameters,
        "operation": operation if executed_designated_host else None,
        "cells": cells,
    }
    # The in-memory contract must equal the stable JSON contract. In particular,
    # normalize tuples and reject values that JSON cannot represent faithfully.
    return json.loads(json.dumps(report, allow_nan=False))


def stable_json(report: dict[str, Any]) -> str:
    return json.dumps(
        report,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"


def operation_descriptor(
    provenance: dict[str, str],
    parameters: dict[str, Any],
    *,
    designated_hostname: str,
    openra_dir: Path,
) -> dict[str, Any]:
    if not isinstance(designated_hostname, str) or not designated_hostname:
        raise ContractError("designated hostname must be nonempty text")
    descriptor = {
        "provenance": provenance,
        "parameters": parameters,
        "designated_hostname": designated_hostname,
        "openra_dir": str(Path(openra_dir).resolve()),
    }
    descriptor = json.loads(json.dumps(descriptor, sort_keys=True, allow_nan=False))
    encoded = json.dumps(
        descriptor, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    return {
        "schema": OPERATION_SCHEMA,
        "descriptor": descriptor,
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def validate_operation(
    operation: Any,
    expected: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(operation, dict) or operation.get("schema") != OPERATION_SCHEMA:
        raise ContractError("evidence operation descriptor is absent or invalid")
    descriptor = operation.get("descriptor")
    if not isinstance(descriptor, dict):
        raise ContractError("evidence operation body is invalid")
    encoded = json.dumps(
        descriptor, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")
    if operation.get("sha256") != hashlib.sha256(encoded).hexdigest():
        raise ContractError("evidence operation digest mismatch")
    if expected is not None and operation != expected:
        raise ContractError("pending evidence does not match the current invocation")
    return operation


def human_summary(report: dict[str, Any]) -> str:
    terminals = {terminal: 0 for terminal in sorted(ALLOWED_TERMINALS)}
    for cell in report["cells"]:
        terminals[cell["terminal"]] += 1
    counts = ", ".join(f"{key}={value}" for key, value in terminals.items())
    run_terminal = report["run"]["terminal"] if report["run"] else "not_executed"
    return (
        f"{MARKER} runtime_evidence={report['runtime_evidence']} "
        f"run_terminal={run_terminal} cells={len(report['cells'])} {counts}"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def git_head(path: Path) -> str:
    try:
        value = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10,
        ).strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise ContractError(f"cannot bind Git HEAD for {path}: {error}") from error
    return require_sha40(value, f"Git HEAD for {path}")


def committed_file_bytes(repository_root: Path, commit_sha: str, path: Path) -> bytes:
    try:
        relative = path.resolve().relative_to(repository_root.resolve()).as_posix()
    except ValueError as error:
        raise ContractError("benchmark source is outside its repository") from error
    try:
        return subprocess.check_output(
            ["git", "-C", str(repository_root), "show", f"{commit_sha}:{relative}"],
            stderr=subprocess.STDOUT,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError) as error:
        raise ContractError(
            f"benchmark source is not committed at {commit_sha}: {error}"
        ) from error


def runtime_provenance(openra_dir: Path, expected: dict[str, str]) -> dict[str, Any]:
    repository_root = Path(__file__).resolve().parent
    source_path = Path(__file__).resolve()
    actual_benchmark_source = git_head(repository_root)
    actual_engine = git_head(openra_dir)
    if actual_benchmark_source != expected["benchmark_source_sha"]:
        raise ContractError("benchmark source Git HEAD differs from the asserted exact SHA")
    if actual_engine != expected["engine_sha"]:
        raise ContractError("OpenRA Git HEAD differs from the asserted exact SHA")
    live_source = source_path.read_bytes()
    committed_source = committed_file_bytes(
        repository_root, actual_benchmark_source, source_path,
    )
    if live_source != committed_source:
        raise ContractError("running benchmark bytes differ from the asserted Git generation")
    binary = openra_dir / "bin" / "OpenRA.dll"
    if not binary.is_file():
        raise ContractError(f"OpenRA runtime binary does not exist: {binary}")
    try:
        dotnet_version = subprocess.check_output(
            ["dotnet", "--version"], stderr=subprocess.STDOUT, text=True, timeout=10,
        ).strip()
    except (OSError, subprocess.SubprocessError) as error:
        raise ContractError(f"dotnet identity unavailable: {error}") from error
    return {
        "benchmark_source_git_head": actual_benchmark_source,
        "benchmark_source_sha256": hashlib.sha256(live_source).hexdigest(),
        "frozen_war_college_comparison_sha": expected["war_college_sha"],
        "engine_git_head": actual_engine,
        "openra_binary_sha256": sha256_file(binary),
        "dotnet_version": dotnet_version,
        "dotnet_version_sha256": hashlib.sha256(dotnet_version.encode("utf-8")).hexdigest(),
    }


def ensure_endpoint_unoccupied(port: int) -> None:
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        probe.bind(("127.0.0.1", port))
    except OSError as error:
        raise ContractError(f"127.0.0.1:{port} is already occupied") from error
    finally:
        probe.close()


def process_listener_identity(pid: int, port: int) -> dict[str, Any] | None:
    socket_inodes: set[str] = set()
    try:
        for descriptor in Path(f"/proc/{pid}/fd").iterdir():
            try:
                target = os.readlink(descriptor)
            except OSError:
                continue
            match = re.fullmatch(r"socket:\[([0-9]+)\]", target)
            if match:
                socket_inodes.add(match.group(1))
        wanted_port = f"{port:04X}"
        for table_name in ("tcp", "tcp6"):
            table = Path(f"/proc/{pid}/net/{table_name}")
            for line in table.read_text(encoding="ascii").splitlines()[1:]:
                fields = line.split()
                if len(fields) < 10:
                    continue
                local, state, inode = fields[1], fields[3], fields[9]
                if local.rsplit(":", 1)[-1] == wanted_port and state == "0A" and inode in socket_inodes:
                    return {"pid": pid, "port": port, "socket_inode": inode, "proc_table": table_name}
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        return None
    return None


class BoundedLogCapture:
    """Continuously drain daemon output while retaining only a bounded tail."""

    def __init__(self, stream: Any, max_tail_bytes: int = MAX_DAEMON_LOG_TAIL_BYTES) -> None:
        self.stream = stream
        self.max_tail_bytes = max_tail_bytes
        self.total_bytes = 0
        self._tail = bytearray()
        self._digest = hashlib.sha256()
        self._error: str | None = None
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._drain, name="openra-log-drain", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _drain(self) -> None:
        try:
            while True:
                chunk = self.stream.read(4096)
                if not chunk:
                    return
                with self._lock:
                    self.total_bytes += len(chunk)
                    self._digest.update(chunk)
                    self._tail.extend(chunk)
                    excess = len(self._tail) - self.max_tail_bytes
                    if excess > 0:
                        del self._tail[:excess]
        except Exception as error:
            with self._lock:
                self._error = f"{type(error).__name__}:{error}"

    def finish(self, timeout_s: float = 5.0) -> dict[str, Any]:
        self._thread.join(timeout_s)
        with self._lock:
            return {
                "total_bytes": self.total_bytes,
                "sha256": self._digest.hexdigest(),
                "tail_utf8": bytes(self._tail).decode("utf-8", errors="replace"),
                "tail_bytes": len(self._tail),
                "drain_error": self._error,
                "drain_thread_retired": not self._thread.is_alive(),
            }


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _evidence_generation(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _open_regular_read_only(path: Path) -> tuple[int, bytes, os.stat_result]:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ContractError(f"evidence artifact is not a regular file: {path}")
        if stat.S_IMODE(metadata.st_mode) != 0o400:
            raise ContractError(f"evidence artifact mode is not 0400: {path}")
        if metadata.st_size > MAX_EVIDENCE_BYTES:
            raise ContractError(f"evidence artifact exceeds {MAX_EVIDENCE_BYTES} bytes")

        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(64 * 1024, MAX_EVIDENCE_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_EVIDENCE_BYTES:
                raise ContractError(f"evidence artifact exceeds {MAX_EVIDENCE_BYTES} bytes")
        payload = b"".join(chunks)
        after = os.fstat(descriptor)
        if _evidence_generation(after) != _evidence_generation(metadata):
            raise ContractError(f"evidence artifact changed while being consumed: {path}")
        if len(payload) != metadata.st_size:
            raise ContractError(f"evidence artifact size changed while being consumed: {path}")
        return descriptor, payload, metadata
    except Exception:
        os.close(descriptor)
        raise


def _read_regular_read_only(path: Path) -> bytes:
    descriptor, payload, _ = _open_regular_read_only(path)
    os.close(descriptor)
    return payload


def _assert_path_generation(path: Path, descriptor: int, label: str) -> None:
    try:
        named = path.lstat()
    except FileNotFoundError as error:
        raise ContractError(f"{label} evidence name disappeared before commit") from error
    opened = os.fstat(descriptor)
    if not os.path.samestat(named, opened):
        raise ContractError(f"{label} evidence name changed generation before commit")
    if not stat.S_ISREG(named.st_mode) or stat.S_IMODE(named.st_mode) != 0o400:
        raise ContractError(f"{label} evidence name changed contract before commit")


def _link_open_inode_create_only(descriptor: int, destination: Path) -> None:
    """Link the retained open inode without re-resolving its mutable source name."""
    parent_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    parent_descriptor = os.open(destination.parent, parent_flags)
    try:
        library = ctypes.CDLL(ctypes.util.find_library("c") or None, use_errno=True)
        linkat = library.linkat
        linkat.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
        ]
        linkat.restype = ctypes.c_int
        result = linkat(
            descriptor,
            b"",
            parent_descriptor,
            os.fsencode(destination.name),
            0x1000,  # Linux AT_EMPTY_PATH: retained descriptor is link authority.
        )
        if result != 0:
            error_number = ctypes.get_errno()
            raise OSError(
                error_number,
                os.strerror(error_number),
                os.fspath(destination),
            )
    finally:
        os.close(parent_descriptor)


def _validate_recoverable_evidence(
    payload: bytes,
    expected_operation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        report = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(f"pending evidence is not canonical JSON: {error}") from error
    if not isinstance(report, dict) or report.get("marker") != MARKER:
        raise ContractError("pending evidence marker mismatch")
    if report.get("schema_version") != SCHEMA_VERSION:
        raise ContractError("pending evidence schema mismatch")
    if report.get("runtime_evidence") != "EXECUTED":
        raise ContractError("pending evidence is not an executed runtime attempt")
    validate_operation(report.get("operation"), expected_operation)
    provenance = report.get("provenance")
    if not isinstance(provenance, dict):
        raise ContractError("pending evidence provenance is absent")
    validate_provenance(
        provenance.get("engine_sha", ""),
        provenance.get("war_college_sha", ""),
        provenance.get("benchmark_source_sha", ""),
        provenance.get("generation", ""),
    )
    run = report.get("run")
    if not isinstance(run, dict) or run.get("terminal") not in RUN_TERMINALS:
        raise ContractError("pending evidence run terminal is invalid")
    return report


def _pending_path(path: Path) -> Path:
    return path.parent / f".{path.name}.pending"


def _retire_pending(staging: Path, parent: Path) -> tuple[bool, str | None]:
    try:
        staging.unlink()
        _fsync_directory(parent)
        return True, None
    except OSError as error:
        # The final link was already fenced.  A retained owned alias is recovery
        # evidence, not authority to downgrade or replace the committed final.
        return False, f"{type(error).__name__}:{error}"


def recover_owned_evidence(
    path: Path,
    expected_operation: dict[str, Any],
) -> bytes | None:
    """Converge an exact owned pending/final publication without runtime contact."""
    path = Path(os.path.abspath(os.fspath(path)))
    if not path.parent.is_dir():
        raise FileNotFoundError(f"evidence output parent must pre-exist: {path.parent}")
    staging = _pending_path(path)
    final_exists = os.path.lexists(path)
    pending_exists = os.path.lexists(staging)
    if not final_exists and not pending_exists:
        return None
    if final_exists and not pending_exists:
        raise FileExistsError(f"evidence output already exists: {path}")

    # A prior attempt may have failed while fencing the pending directory entry.
    # Re-establish that fence before trusting the surviving name as recovery
    # authority or using it as the source of a final hard link.
    _fsync_directory(path.parent)
    pending_descriptor, pending_payload, pending_metadata = _open_regular_read_only(staging)
    try:
        # Invocation identity is checked on bytes consumed from the retained
        # descriptor before that exact inode can become final authority.
        _validate_recoverable_evidence(pending_payload, expected_operation)
        _assert_path_generation(staging, pending_descriptor, "pending")
        if final_exists:
            final_descriptor, final_payload, final_metadata = _open_regular_read_only(path)
            try:
                if not os.path.samestat(final_metadata, pending_metadata):
                    raise ContractError("final evidence is not the owned pending inode")
                if final_payload != pending_payload:
                    raise ContractError("owned final and pending evidence bytes differ")
            finally:
                os.close(final_descriptor)
        else:
            _link_open_inode_create_only(pending_descriptor, path)

        os.fsync(pending_descriptor)
        _fsync_directory(path.parent)
        try:
            _assert_path_generation(staging, pending_descriptor, "pending")
        except ContractError:
            # Never unlink a foreign generation that replaced the owned alias.
            return pending_payload
        _retire_pending(staging, path.parent)
        return pending_payload
    finally:
        os.close(pending_descriptor)


def publish_evidence_create_only(path: Path, payload: bytes) -> dict[str, Any]:
    path = Path(os.path.abspath(os.fspath(path)))
    if len(payload) > MAX_EVIDENCE_BYTES:
        raise ContractError(f"evidence payload exceeds {MAX_EVIDENCE_BYTES} bytes")
    if not path.parent.is_dir():
        raise FileNotFoundError(f"evidence output parent must pre-exist: {path.parent}")
    if os.path.lexists(path) and not os.path.lexists(_pending_path(path)):
        raise FileExistsError(f"evidence output already exists: {path}")
    requested_report = _validate_recoverable_evidence(payload)
    requested_operation = requested_report["operation"]
    recovered = recover_owned_evidence(path, requested_operation)
    if recovered is not None:
        return {
            "path": str(path),
            "sha256": hashlib.sha256(recovered).hexdigest(),
            "bytes": len(recovered),
            "recovered": True,
            "payload_matches_request": recovered == payload,
        }

    staging = _pending_path(path)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(staging, flags, 0o600)
    retired = False
    retirement_error: str | None = None
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fchmod(stream.fileno(), 0o400)
            os.fsync(stream.fileno())
        # Make the pending name durable before it becomes recovery authority.
        # Retain the written descriptor so the later final link cannot resolve
        # a replacement generation through the mutable staging pathname.
        _fsync_directory(path.parent)
        _assert_path_generation(staging, descriptor, "pending")
        _link_open_inode_create_only(descriptor, path)
        _fsync_directory(path.parent)
        try:
            _assert_path_generation(staging, descriptor, "pending")
        except ContractError as error:
            # A replacement alias is not ours to remove after the exact owned
            # inode has been committed through the retained descriptor.
            retirement_error = f"{type(error).__name__}:{error}"
        else:
            retired, retirement_error = _retire_pending(staging, path.parent)
    except Exception:
        # The immutable pending inode is the recovery authority.  Never unlink
        # it after an ambiguous final-link or directory-durability terminal.
        raise
    finally:
        os.close(descriptor)
    return {
        "path": str(path),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "recovered": False,
        "payload_matches_request": True,
        "pending_retired": retired,
        "pending_retirement_error": retirement_error,
    }


def rss_bytes(pid: int) -> int | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text(encoding="utf-8").splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
        return None
    return None


class RssSampler:
    def __init__(self, pid: int) -> None:
        self.pid = pid
        self.before = rss_bytes(pid)
        self.peak = self.before
        self.after: int | None = None
        self.cell_before: int | None = None
        self.cell_peak: int | None = None
        self._stop = asyncio.Event()

    async def run(self) -> None:
        while not self._stop.is_set():
            value = rss_bytes(self.pid)
            if value is not None and (self.peak is None or value > self.peak):
                self.peak = value
            if value is not None and self.cell_before is not None and (
                self.cell_peak is None or value > self.cell_peak
            ):
                self.cell_peak = value
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=0.05)
            except TimeoutError:
                pass

    def stop(self) -> None:
        self.after = rss_bytes(self.pid)
        self._stop.set()

    def begin_cell(self) -> None:
        self.cell_before = rss_bytes(self.pid)
        self.cell_peak = self.cell_before

    def end_cell(self) -> dict[str, int | None]:
        after = rss_bytes(self.pid)
        result = {"before": self.cell_before, "peak": self.cell_peak, "after": after}
        self.cell_before = None
        self.cell_peak = None
        return result


def _runtime_modules() -> tuple[Any, Any, Any, Any]:
    try:
        import grpc  # type: ignore
        from google.protobuf.json_format import MessageToDict  # type: ignore
        from openra_env.generated import rl_bridge_pb2, rl_bridge_pb2_grpc  # type: ignore
    except ImportError as error:
        raise ContractError(f"runtime dependencies unavailable: {error}") from error
    return grpc, MessageToDict, rl_bridge_pb2, rl_bridge_pb2_grpc


def start_daemon(openra_dir: Path, port: int) -> subprocess.Popen[bytes]:
    if not openra_dir.is_dir():
        raise ContractError(f"OpenRA directory does not exist: {openra_dir}")
    binary = openra_dir / "bin" / "OpenRA.dll"
    if not binary.is_file():
        raise ContractError(f"OpenRA runtime binary does not exist: {binary}")
    env = os.environ.copy()
    env["DOTNET_ROLL_FORWARD"] = "LatestMajor"
    env["RL_GRPC_PORT"] = str(port)
    command = [
        "dotnet",
        str(binary),
        f"Engine.EngineDir={openra_dir}",
        "Game.Mod=ra",
        "Game.Platform=Null",
        f"Launch.MultiSession={port}",
    ]
    return subprocess.Popen(
        command,
        cwd=openra_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


async def wait_ready(
    stub: Any,
    pb2: Any,
    daemon: subprocess.Popen[bytes],
    port: int,
    timeout_s: float,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_s
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if daemon.poll() is not None:
            raise ContractError(f"spawned OpenRA daemon exited before readiness: rc={daemon.returncode}")
        identity = process_listener_identity(daemon.pid, port)
        if identity is None:
            await asyncio.sleep(0.05)
            continue
        try:
            await asyncio.wait_for(stub.GetState(pb2.StateRequest()), timeout=2.0)
            if daemon.poll() is not None:
                raise ContractError("spawned OpenRA daemon exited during readiness")
            confirmed = process_listener_identity(daemon.pid, port)
            if confirmed != identity:
                raise ContractError("spawned daemon listener identity changed during readiness")
            return confirmed
        except Exception as error:  # runtime boundary: grpc error subclasses vary
            last_error = error
            await asyncio.sleep(0.25)
    raise TimeoutError(f"daemon readiness exceeded {timeout_s}s: {last_error}")


async def wait_session_playing(
    stub: Any, pb2: Any, session_id: str, timeout_s: float,
) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        state = await asyncio.wait_for(
            stub.GetState(pb2.StateRequest(session_id=session_id)),
            timeout=min(5.0, timeout_s),
        )
        if getattr(state, "phase", None) == "playing":
            return
        await asyncio.sleep(0.05)
    raise TimeoutError(f"session {session_id} did not reach phase=playing")


def validate_joint_response(response: Any, session_id: str, requested_ticks: int) -> dict[str, Any]:
    if getattr(response, "session_id", None) != session_id:
        raise ContractError("JointAdvance response session binding mismatch")
    start_tick = getattr(response, "start_tick", None)
    end_tick = getattr(response, "end_tick", None)
    if not isinstance(start_tick, int) or not isinstance(end_tick, int):
        raise ContractError("JointAdvance response ticks must be exact integers")
    if end_tick - start_tick != requested_ticks:
        raise ContractError("JointAdvance response did not prove requested tick advancement")
    observations = list(getattr(response, "player_observations", ()))
    players = [getattr(observation, "player", None) for observation in observations]
    if len(players) != 2 or set(players) != {"Multi0", "Multi1"}:
        raise ContractError("JointAdvance response must contain exactly Multi0 and Multi1 perspectives")
    return {"start_tick": start_tick, "end_tick": end_tick, "players": sorted(players)}


async def destroy_sessions(
    stub: Any, pb2: Any, session_ids: list[str], timeout_s: float,
) -> dict[str, Any]:
    attempted = list(dict.fromkeys(session_ids))
    failures: list[str] = []
    latencies: list[float] = []
    destroyed: list[str] = []

    async def destroy(session_id: str) -> tuple[str, float]:
        started = time.monotonic()
        await stub.DestroySession(pb2.DestroySessionRequest(session_id=session_id))
        return session_id, (time.monotonic() - started) * 1000

    tasks = {session_id: asyncio.create_task(destroy(session_id)) for session_id in attempted}
    if tasks:
        done, pending = await asyncio.wait(tasks.values(), timeout=timeout_s)
        for session_id in attempted:
            task = tasks[session_id]
            if task in done:
                try:
                    retired_id, latency = task.result()
                    destroyed.append(retired_id)
                    latencies.append(latency)
                except Exception as error:
                    failures.append(f"{session_id}:{type(error).__name__}:{error}")
        for task in pending:
            task.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
            pending_ids = sorted(
                session_id for session_id, task in tasks.items() if task in pending
            )
            failures.extend(f"{session_id}:TimeoutError:total teardown deadline" for session_id in pending_ids)
    unretired = [session_id for session_id in attempted if session_id not in set(destroyed)]
    return {
        "failures": failures,
        "latency": latency_summary(latencies),
        "latency_samples_ms": latencies,
        "attempted_session_ids": attempted,
        "destroyed_session_ids": destroyed,
        "unretired_session_ids": unretired,
        "teardown_total_deadline_s": timeout_s,
        "cleanup_terminal": "complete" if not unretired else "daemon_retirement_required",
    }


async def run_repetition(
    *,
    stub: Any,
    pb2: Any,
    message_to_dict: Any,
    concurrency: int,
    ticks: int,
    samples: int,
    seed_base: int,
    repetition: int,
    rpc_timeout_s: float,
    teardown_timeout_s: float,
    teardown_records: list[dict[str, Any]],
) -> dict[str, Any]:
    session_id_by_slot: dict[int, str] = {}
    create_latencies: list[float] = []
    advance_latencies: list[float] = []
    hashes: dict[str, str] = {}
    teardown = {
        "failures": [], "latency": {"count": 0},
        "latency_samples_ms": [], "attempted_session_ids": [],
        "destroyed_session_ids": [], "unretired_session_ids": [],
        "cleanup_terminal": "complete",
    }
    create_phase_started = False
    create_phase_complete = False
    started = time.monotonic()
    try:
        async def create(slot: int) -> tuple[int, str, float]:
            t0 = time.monotonic()
            response = await asyncio.wait_for(
                stub.CreateSession(pb2.CreateSessionRequest(
                    map_name=MAP_NAME,
                    bots=BOTS,
                    seed=seed_base + slot,
                )),
                timeout=rpc_timeout_s,
            )
            # Record ownership immediately: if a sibling create fails or the
            # phase is cancelled, this session still has to be destroyed.
            if not isinstance(response.session_id, str) or not response.session_id:
                raise ContractError("CreateSession returned an invalid session ID")
            session_id_by_slot[slot] = response.session_id
            await wait_session_playing(stub, pb2, response.session_id, rpc_timeout_s)
            return slot, response.session_id, (time.monotonic() - t0) * 1000

        create_phase_started = True
        created_by_task = await run_owned_phase(
            {str(slot): create(slot) for slot in range(concurrency)},
            deadline_s=rpc_timeout_s,
        )
        create_phase_complete = True
        created = list(created_by_task.values())
        created.sort(key=lambda item: item[0])
        if [item[0] for item in created] != list(range(concurrency)):
            raise ContractError("CreateSession results do not cover every requested slot")
        if len(set(session_id_by_slot.values())) != concurrency:
            raise ContractError("CreateSession returned duplicate session ownership")
        create_latencies.extend(item[2] for item in created)

        final_by_slot: dict[int, dict[str, Any]] = {}
        validation_by_slot: dict[int, dict[str, Any]] = {}
        for _sample in range(samples):
            async def advance(slot: int, session_id: str) -> tuple[int, float, dict[str, Any]]:
                request = pb2.JointAdvanceRequest(
                    session_id=session_id,
                    ticks=ticks,
                    player_actions=[
                        pb2.PlayerCommandBatch(player="Multi0"),
                        pb2.PlayerCommandBatch(player="Multi1"),
                    ],
                )
                t0 = time.monotonic()
                response = await asyncio.wait_for(stub.JointAdvance(request), timeout=rpc_timeout_s)
                elapsed_ms = (time.monotonic() - t0) * 1000
                validation = validate_joint_response(response, session_id, ticks)
                as_dict = message_to_dict(response, preserving_proto_field_name=True)
                return slot, elapsed_ms, {"response": as_dict, "validation": validation}

            advanced_by_task = await run_owned_phase(
                {
                    str(slot): advance(slot, session_id_by_slot[slot])
                    for slot in range(concurrency)
                },
                deadline_s=rpc_timeout_s,
            )
            advanced = list(advanced_by_task.values())
            for slot, elapsed_ms, envelope in advanced:
                advance_latencies.append(elapsed_ms)
                final_by_slot[slot] = envelope["response"]
                validation_by_slot[slot] = envelope["validation"]

        for slot, response in sorted(final_by_slot.items()):
            hashes[str(slot)] = canonical_state_hash(response)
    finally:
        owned_session_ids = list(dict.fromkeys(
            session_id_by_slot[slot] for slot in sorted(session_id_by_slot)
        ))
        cleanup_task = asyncio.create_task(
            destroy_sessions(stub, pb2, owned_session_ids, teardown_timeout_s)
        )
        cancelled_during_cleanup = False
        try:
            teardown = await asyncio.shield(cleanup_task)
        except asyncio.CancelledError:
            # The work deadline may freeze the cell terminal, but it cannot
            # silently cancel cleanup for already-owned sessions.
            cancelled_during_cleanup = True
            teardown = await cleanup_task
        create_ambiguous = create_phase_started and not create_phase_complete
        teardown["create_commit_response_ambiguous"] = create_ambiguous
        teardown["cleanup_after_work_cancellation"] = cancelled_during_cleanup
        teardown["containment_required"] = bool(
            create_ambiguous or teardown["unretired_session_ids"]
        )
        if teardown["containment_required"]:
            teardown["cleanup_terminal"] = "daemon_retirement_required"
        teardown_records.append(teardown)
        if cancelled_during_cleanup:
            raise asyncio.CancelledError

    wall_s = time.monotonic() - started
    return {
        "repetition": repetition,
        "seed_by_slot": {str(slot): seed_base + slot for slot in range(concurrency)},
        "session_id_by_slot": {
            str(slot): session_id_by_slot[slot] for slot in sorted(session_id_by_slot)
        },
        "create_latency": latency_summary(create_latencies),
        "joint_advance_latency": latency_summary(advance_latencies),
        "joint_advance_calls": len(advance_latencies),
        "ticks_advanced_validated": len(advance_latencies) * ticks,
        "validated_ticks_per_second": (len(advance_latencies) * ticks) / wall_s if wall_s > 0 else 0,
        "canonical_hash_by_slot": hashes,
        "joint_advance_validation_by_slot": {
            str(slot): validation for slot, validation in sorted(validation_by_slot.items())
        },
        "teardown": teardown,
        "wall_seconds": wall_s,
    }


async def run_cell(
    *,
    stub: Any,
    pb2: Any,
    message_to_dict: Any,
    concurrency: int,
    ticks: int,
    samples: int,
    repetitions: int,
    seed_base: int,
    rpc_timeout_s: float,
    cell_timeout_s: float,
    teardown_timeout_s: float,
) -> tuple[str, dict[str, Any]]:
    started = time.monotonic()
    repetition_results: list[dict[str, Any]] = []
    teardown_records: list[dict[str, Any]] = []

    def teardown_evidence() -> dict[str, Any]:
        failures = [failure for record in teardown_records for failure in record["failures"]]
        samples = [
            sample
            for record in teardown_records
            for sample in record["latency_samples_ms"]
        ]
        return {
            "teardown_failures": failures,
            "teardown_latency": latency_summary(samples),
            "teardown_attempted_session_ids": [
                session_id for record in teardown_records
                for session_id in record["attempted_session_ids"]
            ],
            "teardown_destroyed_session_ids": [
                session_id for record in teardown_records
                for session_id in record["destroyed_session_ids"]
            ],
            "teardown_unretired_session_ids": [
                session_id for record in teardown_records
                for session_id in record["unretired_session_ids"]
            ],
            "create_commit_response_ambiguous": any(
                record["create_commit_response_ambiguous"] for record in teardown_records
            ),
            "cleanup_after_work_cancellation": any(
                record["cleanup_after_work_cancellation"] for record in teardown_records
            ),
            "containment_required": any(
                record["containment_required"] for record in teardown_records
            ),
            "cleanup_terminals": [
                record["cleanup_terminal"] for record in teardown_records
            ],
        }

    async def run_repetitions() -> None:
        for repetition in range(repetitions):
            repetition_results.append(await run_repetition(
                stub=stub,
                pb2=pb2,
                message_to_dict=message_to_dict,
                concurrency=concurrency,
                ticks=ticks,
                samples=samples,
                seed_base=seed_base,
                repetition=repetition,
                rpc_timeout_s=rpc_timeout_s,
                teardown_timeout_s=teardown_timeout_s,
                teardown_records=teardown_records,
            ))
    try:
        # asyncio.wait_for is available throughout the repository's Python >=3.10 range.
        await asyncio.wait_for(run_repetitions(), timeout=cell_timeout_s)
    except asyncio.TimeoutError as error:
        return "timeout", {
            "error": str(error),
            "completed_repetitions": len(repetition_results),
            **teardown_evidence(),
        }
    except Exception as error:
        return "rpc_error", {
            "error_type": type(error).__name__,
            "error": str(error),
            "completed_repetitions": len(repetition_results),
            **teardown_evidence(),
        }

    teardown = teardown_evidence()
    teardown_errors = teardown["teardown_failures"]
    hashes_by_slot: dict[str, list[str]] = {}
    for repetition in repetition_results:
        for slot, digest in repetition["canonical_hash_by_slot"].items():
            hashes_by_slot.setdefault(slot, []).append(digest)
    deterministic = all(len(set(digests)) == 1 for digests in hashes_by_slot.values())
    payload = {
        "repetitions": repetition_results,
        "same_seed_deterministic": deterministic,
        "hashes_by_slot": hashes_by_slot,
        "cell_wall_seconds": time.monotonic() - started,
        **teardown,
    }
    return (
        "teardown_error"
        if teardown_errors or teardown["containment_required"]
        else "success"
    ), payload


def finalize_unexecuted_cells(
    ledger: CellLedger,
    planned: list[dict[str, int]],
    *,
    blocked_by: str,
) -> None:
    for cell in planned:
        key = f"c{cell['concurrency']}-t{cell['ticks_per_joint_advance']}"
        ledger.finalize(key, "not_executed", {
            **cell,
            "blocked_by": blocked_by,
            "reason": "matrix retired after first non-success terminal",
            "process_rss_bytes": None,
        })


async def execute_runtime(
    args: argparse.Namespace,
    parameters: dict[str, Any],
    expected_provenance: dict[str, str],
) -> dict[str, Any]:
    """Attempt a designated-host run and always return a structured terminal."""
    actual_hostname = socket.gethostname()
    host = {
        "hostname": actual_hostname,
        "designated_hostname": args.designated_hostname,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
    }
    run: dict[str, Any] = {
        "terminal": "startup_error",
        "stage": "host_attestation",
        "error_type": None,
        "error": None,
        "listener_identity": None,
        "runtime_provenance": None,
        "daemon_log": None,
        "cleanup": {"failures": []},
    }
    ledger = CellLedger()
    daemon: subprocess.Popen[bytes] | None = None
    capture: BoundedLogCapture | None = None
    sampler: RssSampler | None = None
    sampler_task: asyncio.Task[Any] | None = None
    channel: Any | None = None
    planned = build_matrix(parameters["concurrency"], parameters["tick_batches"])
    try:
        if args.designated_hostname != actual_hostname:
            raise ContractError("designated hostname does not match this host")

        run["stage"] = "runtime_provenance"
        run["runtime_provenance"] = runtime_provenance(
            Path(args.openra_dir).resolve(), expected_provenance,
        )
        run["stage"] = "endpoint_preflight"
        ensure_endpoint_unoccupied(args.port)
        run["stage"] = "runtime_import"
        grpc, message_to_dict, pb2, pb2_grpc = _runtime_modules()

        run["stage"] = "daemon_startup"
        daemon = start_daemon(Path(args.openra_dir).resolve(), args.port)
        if daemon.stdout is None:
            raise ContractError("spawned daemon has no capturable output stream")
        capture = BoundedLogCapture(daemon.stdout)
        capture.start()
        sampler = RssSampler(daemon.pid)
        sampler_task = asyncio.create_task(sampler.run())
        channel = grpc.aio.insecure_channel(
            f"127.0.0.1:{args.port}",
            options=[
                ("grpc.max_receive_message_length", 64 * 1024 * 1024),
                ("grpc.max_send_message_length", 16 * 1024 * 1024),
            ],
        )
        stub = pb2_grpc.RLBridgeStub(channel)

        run["stage"] = "readiness"
        listener_identity = await wait_ready(
            stub, pb2, daemon, args.port, args.ready_timeout_s,
        )
        run["listener_identity"] = listener_identity

        for index, cell in enumerate(planned):
            key = f"c{cell['concurrency']}-t{cell['ticks_per_joint_advance']}"
            run["stage"] = f"cell:{key}"
            if daemon.poll() is not None:
                raise ContractError(f"spawned daemon exited before {key}: rc={daemon.returncode}")
            if process_listener_identity(daemon.pid, args.port) != listener_identity:
                raise ContractError(f"spawned daemon listener identity changed before {key}")
            sampler.begin_cell()
            terminal, payload = await run_cell(
                stub=stub,
                pb2=pb2,
                message_to_dict=message_to_dict,
                concurrency=cell["concurrency"],
                ticks=cell["ticks_per_joint_advance"],
                samples=args.samples,
                repetitions=args.repetitions,
                seed_base=args.seed,
                rpc_timeout_s=args.rpc_timeout_s,
                cell_timeout_s=args.cell_timeout_s,
                teardown_timeout_s=args.teardown_timeout_s,
            )
            payload.update(cell)
            payload["process_rss_bytes"] = sampler.end_cell()
            if daemon.poll() is not None or process_listener_identity(daemon.pid, args.port) != listener_identity:
                terminal = "rpc_error"
                payload["daemon_identity_error"] = "spawned daemon/listener ownership lost during cell"
            ledger.finalize(key, terminal, payload)
            if not matrix_may_continue(terminal):
                finalize_unexecuted_cells(ledger, planned[index + 1:], blocked_by=key)
                break

        run.update({"terminal": "completed", "stage": "matrix_complete"})
    except asyncio.TimeoutError as error:
        run.update({
            "terminal": "readiness_timeout" if run["stage"] == "readiness" else "channel_error",
            "error_type": type(error).__name__,
            "error": str(error),
        })
    except (ContractError, OSError, subprocess.SubprocessError) as error:
        startup_stages = {
            "host_attestation", "runtime_provenance", "endpoint_preflight",
            "runtime_import", "daemon_startup",
        }
        run.update({
            "terminal": "startup_error" if run["stage"] in startup_stages else (
                "readiness_timeout" if run["stage"] == "readiness" else "channel_error"
            ),
            "error_type": type(error).__name__,
            "error": str(error),
        })
    except Exception as error:  # grpc implementations expose varying exception classes
        run.update({
            "terminal": "channel_error",
            "error_type": type(error).__name__,
            "error": str(error),
        })
    finally:
        cleanup_failures: list[str] = []
        containment_required = any(
            bool(cell.payload.get("containment_required"))
            for cell in ledger.values()
        )
        if channel is not None:
            try:
                await channel.close()
            except Exception as error:
                cleanup_failures.append(f"channel:{type(error).__name__}:{error}")
        if sampler is not None:
            sampler.stop()
        if sampler_task is not None:
            try:
                await sampler_task
            except Exception as error:
                cleanup_failures.append(f"sampler:{type(error).__name__}:{error}")
        if daemon is not None:
            try:
                if daemon.poll() is None:
                    daemon.terminate()
                    try:
                        daemon.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        daemon.kill()
                        daemon.wait(timeout=5)
                run["daemon_returncode"] = daemon.returncode
            except Exception as error:
                cleanup_failures.append(f"daemon:{type(error).__name__}:{error}")
        if capture is not None:
            log = capture.finish()
            run["daemon_log"] = log
            if log["drain_error"] or not log["drain_thread_retired"]:
                cleanup_failures.append("daemon_log_drain_not_cleanly_retired")
        daemon_retired = daemon is not None and daemon.poll() is not None
        run["containment"] = {
            "required_by_cell": containment_required,
            "boundary": "disposable_daemon_retirement" if containment_required else "not_required",
            "daemon_retired": daemon_retired,
        }
        if containment_required and not daemon_retired:
            cleanup_failures.append("required_disposable_daemon_retirement_not_proven")
        run["cleanup"] = {"failures": cleanup_failures}
        if cleanup_failures and run["terminal"] == "completed":
            run.update({
                "terminal": "cleanup_error",
                "stage": "cleanup",
                "error_type": "CleanupError",
                "error": ";".join(cleanup_failures),
            })

    return {
        "cells": [
            {"key": cell.key, "terminal": cell.terminal, **cell.payload}
            for cell in ledger.values()
        ],
        "run": run,
        "host": host,
    }


def utc_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("mode", choices=("plan", "run"))
    result.add_argument("--engine-sha", required=True)
    result.add_argument("--war-college-sha", required=True)
    result.add_argument("--benchmark-source-sha", required=True)
    result.add_argument("--generation", default=GENERATION)
    result.add_argument("--concurrency", default="1,2,4,8")
    result.add_argument("--tick-batches", default="1,8,32,128")
    result.add_argument("--samples", default="5")
    result.add_argument("--repetitions", default="2")
    result.add_argument("--seed", default="2050")
    result.add_argument("--rpc-timeout-s", default="60")
    result.add_argument("--cell-timeout-s", default="900")
    result.add_argument("--teardown-timeout-s", default="10")
    result.add_argument("--ready-timeout-s", default="30")
    result.add_argument("--port", default="9999")
    result.add_argument("--openra-dir")
    result.add_argument("--output")
    result.add_argument("--designated-hostname")
    result.add_argument("--execute-designated-host", action="store_true")
    return result


def normalized_args(args: argparse.Namespace) -> dict[str, Any]:
    args.samples = positive_int(args.samples, label="samples", minimum=1, maximum=1000)
    args.repetitions = positive_int(args.repetitions, label="repetitions", minimum=2, maximum=10)
    args.seed = positive_int(args.seed, label="seed", minimum=1, maximum=2_147_483_647)
    args.rpc_timeout_s = positive_int(args.rpc_timeout_s, label="RPC timeout", minimum=1, maximum=600)
    args.cell_timeout_s = positive_int(args.cell_timeout_s, label="cell timeout", minimum=1, maximum=7200)
    args.teardown_timeout_s = positive_int(args.teardown_timeout_s, label="teardown timeout", minimum=1, maximum=120)
    args.ready_timeout_s = positive_int(args.ready_timeout_s, label="ready timeout", minimum=1, maximum=300)
    args.port = positive_int(args.port, label="port", minimum=1, maximum=65535)
    concurrency = parse_int_csv(
        args.concurrency,
        label="concurrency",
        minimum=1,
        maximum=8,
        allowed=ALLOWED_CONCURRENCY,
    )
    tick_batches = parse_int_csv(
        args.tick_batches,
        label="tick batches",
        minimum=1,
        maximum=10_000,
    )
    build_matrix(concurrency, tick_batches)
    return {
        "concurrency": list(concurrency),
        "tick_batches": list(tick_batches),
        "samples": args.samples,
        "repetitions": args.repetitions,
        "seed": args.seed,
        "rpc_timeout_s": args.rpc_timeout_s,
        "cell_timeout_s": args.cell_timeout_s,
        "teardown_timeout_s": args.teardown_timeout_s,
        "ready_timeout_s": args.ready_timeout_s,
        "port": args.port,
        "map_name": MAP_NAME,
        "bots": BOTS,
    }


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        provenance = validate_provenance(
            args.engine_sha,
            args.war_college_sha,
            args.benchmark_source_sha,
            args.generation,
        )
        parameters = normalized_args(args)
        if args.mode == "run":
            if not args.execute_designated_host:
                raise ContractError("run requires --execute-designated-host")
            if not args.openra_dir or not args.output or not args.designated_hostname:
                raise ContractError(
                    "run requires --openra-dir, --output, and --designated-hostname"
                )
            operation = operation_descriptor(
                provenance,
                parameters,
                designated_hostname=args.designated_hostname,
                openra_dir=Path(args.openra_dir),
            )
            recovered_payload = recover_owned_evidence(Path(args.output), operation)
            if recovered_payload is not None:
                report = _validate_recoverable_evidence(recovered_payload, operation)
                print(human_summary(report), file=sys.stderr)
                print(json.dumps(report, indent=2, sort_keys=True))
                return terminal_exit_code(report)
            outcome = asyncio.run(execute_runtime(args, parameters, provenance))
            report = build_report(
                provenance=provenance,
                parameters=parameters,
                cells=outcome["cells"],
                executed_designated_host=True,
                generated_at_utc=utc_now(),
                command=sys.argv if argv is None else [Path(sys.argv[0]).name, *argv],
                run=outcome["run"],
                host=outcome["host"],
                operation=operation,
            )
            try:
                payload = stable_json(report).encode("utf-8")
                publication = publish_evidence_create_only(Path(args.output), payload)
                if not publication["payload_matches_request"]:
                    report = _validate_recoverable_evidence(
                        _read_regular_read_only(Path(args.output).resolve())
                    )
            except (OSError, ContractError) as error:
                report["run"].update({
                    "terminal": "output_error",
                    "stage": "evidence_publication",
                    "error_type": type(error).__name__,
                    "error": str(error),
                })
                report = json.loads(json.dumps(report, allow_nan=False))
            print(human_summary(report), file=sys.stderr)
        else:
            if args.execute_designated_host:
                raise ContractError("plan must not use --execute-designated-host")
            report = build_report(
                provenance=provenance,
                parameters=parameters,
                cells=[],
                executed_designated_host=False,
                generated_at_utc=utc_now(),
                command=sys.argv if argv is None else [Path(sys.argv[0]).name, *argv],
            )
        print(json.dumps(report, indent=2, sort_keys=True))
        return terminal_exit_code(report) if args.mode == "run" else 0
    except (ContractError, OSError) as error:
        print(f"contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
