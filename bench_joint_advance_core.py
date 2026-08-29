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
from typing import Any, Awaitable, Callable, Iterable


MARKER = "VOID_WAR_COLLEGE_JOINT_ADVANCE_BENCHMARK_V1"
SCHEMA_VERSION = 7
PROTO_INT32_MIN = -(2**31)
PROTO_INT32_MAX = 2**31 - 1
PUBLICATION_RECEIPT_MARKER = "VOID_WAR_COLLEGE_EVIDENCE_COMMIT_RECEIPT_V1"
PUBLICATION_RECEIPT_SCHEMA_VERSION = 1
LOCAL_EVIDENCE_MARKER = "VOID_WAR_COLLEGE_UNTRUSTED_LOCAL_EVIDENCE_V1"
LOCAL_EVIDENCE_SCHEMA_VERSION = 1
OPERATION_SCHEMA = "void.war-college.joint-advance-operation.v1"
FROZEN_ENGINE_SHA = "1607a7a6501d42a47638393ecef8b22831064932"
FROZEN_WAR_COLLEGE_SHA = "973802ef0a614e5afa782ff20e231e18966ae3e5"
GENERATION = "ad1926569b12466c"
ALLOWED_CONCURRENCY = (1, 2, 4, 8)
WORKLOAD_PROFILES = ("noop_control", "stop_owned_unit")
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


class IncompatibleEvidenceSchemaError(ContractError):
    """Raised when preserved evidence uses a known but unsupported schema."""

    def __init__(self, actual: int, expected: int) -> None:
        self.actual = actual
        self.expected = expected
        super().__init__(
            f"pending evidence schema {actual} is incompatible with current schema {expected}"
        )


def require_proto_int32_tick(value: Any, label: str) -> int:
    """Require the exact scalar domain carried by protobuf ``int32`` tick fields."""
    if type(value) is not int or not PROTO_INT32_MIN <= value <= PROTO_INT32_MAX:
        raise ContractError(
            f"{label} must be an exact protobuf signed-int32 integer"
        )
    return value


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
    containment: RuntimeTaskContainment,
    retirement_timeout_s: float | None = None,
) -> CellLedger:
    """Publish immutable terminals and bound cancellation-resistant retirement.

    Timed-out tasks cannot rewrite their immutable terminals.  Tasks that do not
    retire within the explicit cancellation budget transfer to caller-owned
    containment before this helper fails, so they cannot become untracked work.
    """
    if not operations:
        raise ContractError("phase requires at least one operation")
    if not math.isfinite(deadline_s) or deadline_s <= 0:
        raise ContractError("phase deadline must be finite and positive")
    if not isinstance(containment, RuntimeTaskContainment):
        raise ContractError("phase requires caller-owned task containment")
    if retirement_timeout_s is None:
        retirement_timeout_s = deadline_s
    if not math.isfinite(retirement_timeout_s) or retirement_timeout_s <= 0:
        raise ContractError("phase retirement deadline must be finite and positive")

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
        retired, unretired = await asyncio.wait(
            pending,
            timeout=retirement_timeout_s,
        )
        for task in retired:
            _consume_late_owned_phase_completion(task)
        if unretired:
            for task in unretired:
                containment.transfer(task)
            keys = ",".join(sorted(reverse[task] for task in unretired))
            raise ContractError(
                f"phase cancellation retirement exceeded total deadline: {keys}"
            )
    return ledger


def _consume_late_owned_phase_completion(task: asyncio.Task[Any]) -> None:
    """Consume detached asynchronous work without granting it evidence authority."""
    try:
        task.result()
    except BaseException:
        pass


class RuntimeTaskContainment:
    """Retain cancellation-resistant RPC handles through daemon containment."""

    def __init__(self) -> None:
        self.required = False
        self.tasks: set[asyncio.Task[Any]] = set()

    def transfer(self, task: asyncio.Task[Any]) -> None:
        self.required = True
        self.tasks.add(task)

        def consume(completed: asyncio.Task[Any]) -> None:
            self.tasks.discard(completed)
            _consume_late_owned_phase_completion(completed)

        task.add_done_callback(consume)

    def pending(self) -> set[asyncio.Task[Any]]:
        return {task for task in self.tasks if not task.done()}


async def retire_contained_tasks(
    containment: RuntimeTaskContainment,
    timeout_s: float,
) -> int:
    """Bound post-daemon retirement of RPC tasks transferred from owned phases."""
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise ContractError("contained-task retirement deadline must be finite and positive")
    pending = containment.pending()
    if not pending:
        return 0
    for task in pending:
        task.cancel()
    _done, pending = await asyncio.wait(pending, timeout=timeout_s)
    return len(pending)


async def close_channel_with_total_deadline(
    channel: Any,
    timeout_s: float,
) -> str | None:
    """Bound channel-close ownership so daemon retirement remains reachable."""
    if not math.isfinite(timeout_s) or timeout_s <= 0:
        raise ContractError("channel-close deadline must be finite and positive")
    close_task = asyncio.create_task(channel.close())
    done, _pending = await asyncio.wait({close_task}, timeout=timeout_s)
    if close_task in done:
        try:
            close_task.result()
        except Exception as error:
            return f"{type(error).__name__}:{error}"
        return None
    close_task.cancel()
    close_task.add_done_callback(_consume_late_owned_phase_completion)
    return f"TimeoutError:total channel-close deadline {timeout_s}s"


async def run_owned_phase(
    operations: dict[str, Awaitable[Any]],
    *,
    deadline_s: float,
    containment: RuntimeTaskContainment | None = None,
) -> dict[str, Any]:
    """Return keyed results within one total phase-and-retirement deadline.

    A failed or expired phase cancels unfinished siblings and uses only the
    remaining phase budget for cancellation retirement.  Work that suppresses
    cancellation is detached from result/evidence consumption and transferred
    to the caller's session teardown or disposable-daemon containment path.
    """
    if not operations:
        raise ContractError("owned phase requires at least one operation")
    if not math.isfinite(deadline_s) or deadline_s <= 0:
        raise ContractError("owned phase deadline must be finite and positive")
    deadline = time.monotonic() + deadline_s
    tasks = {key: asyncio.create_task(operation) for key, operation in operations.items()}
    reverse = {task: key for key, task in tasks.items()}
    observed_late: set[asyncio.Task[Any]] = set()

    def observe_late(tasks_to_observe: Iterable[asyncio.Task[Any]]) -> None:
        for task in tasks_to_observe:
            if task not in observed_late:
                observed_late.add(task)
                if containment is None:
                    task.add_done_callback(_consume_late_owned_phase_completion)
                else:
                    containment.transfer(task)

    try:
        done, pending = await asyncio.wait(
            tasks.values(),
            timeout=max(0.0, deadline - time.monotonic()),
            return_when=asyncio.FIRST_EXCEPTION,
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
            retired: set[asyncio.Task[Any]] = set()
            unretired = set(pending)
            if pending:
                retired, unretired = await asyncio.wait(
                    pending,
                    timeout=max(0.0, deadline - time.monotonic()),
                )
                for task in retired:
                    _consume_late_owned_phase_completion(task)
            if unretired:
                observe_late(unretired)
                keys = ",".join(sorted(reverse[task] for task in unretired))
                if failure is not None:
                    raise ContractError(
                        f"owned phase failed with {type(failure).__name__}: {failure}; "
                        "cancellation retirement exceeded total deadline for "
                        f"operation keys: {keys}"
                    ) from failure
                raise asyncio.TimeoutError(
                    f"owned phase exceeded {deadline_s}s with unretired operation keys: {keys}"
                )
            if failure is not None:
                raise failure
            raise asyncio.TimeoutError(f"owned phase exceeded {deadline_s}s")
        return {key: tasks[key].result() for key in sorted(tasks)}
    finally:
        unfinished = [task for task in tasks.values() if not task.done()]
        for task in unfinished:
            task.cancel()
        observe_late(unfinished)


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


def _fsync_directory(path_or_descriptor: Path | int) -> None:
    """Fsync either a directory path or an already-retained directory fd."""
    if isinstance(path_or_descriptor, int):
        os.fsync(path_or_descriptor)
        return
    descriptor = os.open(
        path_or_descriptor,
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
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


def _assert_parent_path_generation(parent: Path, descriptor: int) -> None:
    try:
        named = os.stat(parent, follow_symlinks=False)
    except FileNotFoundError as error:
        raise ContractError("evidence parent namespace disappeared before commit") from error
    opened = os.fstat(descriptor)
    if not os.path.samestat(named, opened):
        raise ContractError("evidence parent namespace changed generation before commit")
    if not stat.S_ISDIR(named.st_mode):
        raise ContractError("evidence parent namespace changed contract before commit")


def _entry_exists(parent_descriptor: int, name: str) -> bool:
    try:
        os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False


def _assert_entry_generation(
    parent_descriptor: int,
    name: str,
    descriptor: int,
    label: str,
) -> None:
    try:
        named = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except FileNotFoundError as error:
        raise ContractError(f"{label} evidence name disappeared before commit") from error
    opened = os.fstat(descriptor)
    if not os.path.samestat(named, opened):
        raise ContractError(f"{label} evidence name changed generation before commit")
    if not stat.S_ISREG(named.st_mode) or stat.S_IMODE(named.st_mode) != 0o400:
        raise ContractError(f"{label} evidence name changed contract before commit")


def _link_open_inode_create_only(
    descriptor: int,
    parent_descriptor: int,
    destination_name: str,
) -> None:
    """Link the retained inode into the retained parent directory generation."""
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
        os.fsencode(destination_name),
        0x1000,  # Linux AT_EMPTY_PATH: retained descriptor is link authority.
    )
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), destination_name)


def _require_exact_fields(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ContractError(f"{label} fields are not exact")
    return value


def _require_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{label} must be an exact finite number")
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ContractError(f"{label} must be an exact finite nonnegative number")
    return result


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ContractError(f"{label} must be an exact string list")
    return value


def _validate_latency_evidence(value: Any, label: str) -> None:
    if not isinstance(value, dict) or isinstance(value.get("count"), bool) or not isinstance(
        value.get("count"), int
    ) or value["count"] < 0:
        raise ContractError(f"{label} count is invalid")
    if value["count"] == 0:
        _require_exact_fields(value, {"count"}, label)
        return
    _require_exact_fields(value, {"count", "min_ms", "p50_ms", "p95_ms", "max_ms"}, label)
    samples = [
        _require_number(value[field], f"{label}.{field}")
        for field in ("min_ms", "p50_ms", "p95_ms", "max_ms")
    ]
    if samples != sorted(samples):
        raise ContractError(f"{label} percentile ordering is invalid")


def _validate_teardown_evidence(value: Any, label: str) -> None:
    fields = {
        "failures", "latency", "latency_samples_ms", "attempted_session_ids",
        "destroyed_session_ids", "unretired_session_ids", "teardown_total_deadline_s",
        "cleanup_terminal", "create_commit_response_ambiguous",
        "cleanup_after_work_cancellation", "containment_required",
    }
    value = _require_exact_fields(value, fields, label)
    failures = _require_string_list(value["failures"], f"{label}.failures")
    attempted = _require_string_list(value["attempted_session_ids"], f"{label}.attempted")
    destroyed = _require_string_list(value["destroyed_session_ids"], f"{label}.destroyed")
    unretired = _require_string_list(value["unretired_session_ids"], f"{label}.unretired")
    if len(attempted) != len(set(attempted)) or any(item not in attempted for item in destroyed):
        raise ContractError(f"{label} session accounting is invalid")
    if unretired != [item for item in attempted if item not in set(destroyed)]:
        raise ContractError(f"{label} unretired-session accounting is invalid")
    samples = value["latency_samples_ms"]
    if not isinstance(samples, list):
        raise ContractError(f"{label} latency samples are invalid")
    for sample in samples:
        _require_number(sample, f"{label}.latency_samples_ms")
    _validate_latency_evidence(value["latency"], f"{label}.latency")
    if value["latency"]["count"] != len(samples) or len(destroyed) != len(samples):
        raise ContractError(f"{label} latency/session accounting is inconsistent")
    if value["latency"] != latency_summary(samples):
        raise ContractError(f"{label} latency summary is not bound to raw samples")
    teardown_total_deadline_s = value["teardown_total_deadline_s"]
    if type(teardown_total_deadline_s) is not int or teardown_total_deadline_s <= 0:
        raise ContractError(f"{label}.deadline must be an exact positive integer")
    for field in (
        "create_commit_response_ambiguous", "cleanup_after_work_cancellation",
        "containment_required",
    ):
        if not isinstance(value[field], bool):
            raise ContractError(f"{label}.{field} must be boolean")
    expected_containment = bool(value["create_commit_response_ambiguous"] or unretired)
    if value["containment_required"] != expected_containment:
        raise ContractError(f"{label} containment accounting is inconsistent")
    expected_terminal = "daemon_retirement_required" if expected_containment else "complete"
    if value["cleanup_terminal"] != expected_terminal:
        raise ContractError(f"{label} cleanup terminal is inconsistent")
    if failures and not unretired:
        raise ContractError(f"{label} failures require an unretired session")


def _validate_repetition_evidence(value: Any, label: str) -> None:
    fields = {
        "repetition", "seed_by_slot", "session_id_by_slot", "create_latency",
        "joint_advance_latency", "joint_advance_calls", "ticks_advanced_validated",
        "validated_ticks_per_second", "canonical_hash_by_slot",
        "joint_advance_validation_by_slot", "teardown", "wall_seconds",
        "workload_profile", "bootstrap_joint_advance_calls",
        "bootstrap_ticks_advanced_validated", "bootstrap_validation_by_slot",
        "end_to_end_wall_seconds",
    }
    value = _require_exact_fields(value, fields, label)
    for field in (
        "repetition", "joint_advance_calls", "ticks_advanced_validated",
        "bootstrap_joint_advance_calls", "bootstrap_ticks_advanced_validated",
    ):
        if isinstance(value[field], bool) or not isinstance(value[field], int) or value[field] < 0:
            raise ContractError(f"{label}.{field} must be an exact nonnegative integer")
    if value["joint_advance_calls"] == 0 or value["ticks_advanced_validated"] == 0:
        raise ContractError(f"{label} completed work accounting must be positive")
    throughput = value["validated_ticks_per_second"]
    wall_seconds = value["wall_seconds"]
    end_to_end_wall_seconds = value["end_to_end_wall_seconds"]
    if type(throughput) is not float or not math.isfinite(throughput) or throughput < 0:
        raise ContractError(f"{label}.throughput must be an exact finite float")
    if type(wall_seconds) is not float or not math.isfinite(wall_seconds) or wall_seconds <= 0:
        raise ContractError(f"{label}.wall_seconds must be an exact finite positive float")
    if (
        type(end_to_end_wall_seconds) is not float
        or not math.isfinite(end_to_end_wall_seconds)
        or end_to_end_wall_seconds < wall_seconds
    ):
        raise ContractError(
            f"{label}.end_to_end_wall_seconds must cover measured wall time"
        )
    expected_throughput = value["ticks_advanced_validated"] / wall_seconds
    if throughput != expected_throughput:
        raise ContractError(
            f"{label} throughput does not equal validated ticks divided by wall time"
        )
    _validate_latency_evidence(value["create_latency"], f"{label}.create_latency")
    _validate_latency_evidence(value["joint_advance_latency"], f"{label}.advance_latency")
    if value["joint_advance_latency"]["count"] != value["joint_advance_calls"]:
        raise ContractError(f"{label} call/latency accounting is inconsistent")
    if not isinstance(value["joint_advance_validation_by_slot"], dict):
        raise ContractError(f"{label} validation-by-slot must be an exact object")
    for field in ("seed_by_slot", "session_id_by_slot", "canonical_hash_by_slot"):
        if not isinstance(value[field], dict):
            raise ContractError(f"{label}.{field} must be an exact object")
    slots = sorted(value["seed_by_slot"])
    if slots != sorted(value["session_id_by_slot"]) or slots != sorted(
        value["canonical_hash_by_slot"]
    ) or slots != sorted(value["joint_advance_validation_by_slot"]):
        raise ContractError(f"{label} slot evidence is incomplete")
    profile = value["workload_profile"]
    if profile not in WORKLOAD_PROFILES:
        raise ContractError(f"{label} workload profile is invalid")
    bootstrap = value["bootstrap_validation_by_slot"]
    if not isinstance(bootstrap, dict):
        raise ContractError(f"{label} bootstrap validation must be an exact object")
    if profile == "noop_control":
        if value["bootstrap_joint_advance_calls"] != 0 or value[
            "bootstrap_ticks_advanced_validated"
        ] != 0 or bootstrap:
            raise ContractError(f"{label} noop control cannot claim action bootstrap work")
    else:
        if value["bootstrap_joint_advance_calls"] != len(slots) or value[
            "bootstrap_ticks_advanced_validated"
        ] != len(slots) or sorted(bootstrap) != slots:
            raise ContractError(f"{label} action bootstrap coverage is inconsistent")
        for slot, candidate in bootstrap.items():
            item = _require_exact_fields(
                candidate, {"start_tick", "end_tick", "players", "purpose"},
                f"{label}.bootstrap[{slot}]",
            )
            require_proto_int32_tick(
                item["start_tick"], f"{label}.bootstrap[{slot}].start_tick"
            )
            require_proto_int32_tick(
                item["end_tick"], f"{label}.bootstrap[{slot}].end_tick"
            )
            if (
                item["end_tick"] - item["start_tick"] != 1
                or item["players"] != ["Multi0", "Multi1"]
                or item["purpose"] != "owned_actor_and_order_count_bootstrap"
            ):
                raise ContractError(f"{label} action bootstrap evidence is invalid")
    if len(set(value["session_id_by_slot"].values())) != len(slots):
        raise ContractError(f"{label} session ownership is not unique")
    for slot in slots:
        if not isinstance(slot, str) or not slot.isdigit():
            raise ContractError(f"{label} slot key is invalid")
        if isinstance(value["seed_by_slot"][slot], bool) or not isinstance(
            value["seed_by_slot"][slot], int
        ):
            raise ContractError(f"{label} seed is not an exact integer")
        if not isinstance(value["session_id_by_slot"][slot], str) or not value[
            "session_id_by_slot"
        ][slot]:
            raise ContractError(f"{label} session ID is invalid")
        if not isinstance(value["canonical_hash_by_slot"][slot], str) or not re.fullmatch(
            r"[0-9a-f]{64}", value["canonical_hash_by_slot"][slot]
        ):
            raise ContractError(f"{label} canonical hash is invalid")
        validations = value["joint_advance_validation_by_slot"][slot]
        samples_per_slot, remainder = divmod(value["joint_advance_calls"], len(slots))
        if (
            remainder
            or samples_per_slot <= 0
            or not isinstance(validations, list)
            or len(validations) != samples_per_slot
        ):
            raise ContractError(f"{label} validated sample coverage is inconsistent")
        previous_end_tick: int | None = (
            bootstrap[slot]["end_tick"]
            if profile == "stop_owned_unit"
            else None
        )
        for sample, candidate in enumerate(validations):
            validation = _require_exact_fields(
                candidate,
                {
                    "start_tick", "end_tick", "players", "workload_profile",
                    "commands_submitted", "actor_id_by_player", "order_count_before",
                    "order_count_after", "application_proven",
                },
                f"{label}.validation[{slot}][{sample}]",
            )
            for field in ("start_tick", "end_tick"):
                require_proto_int32_tick(
                    validation[field], f"{label}.validation[{slot}][{sample}].{field}"
                )
            if validation["end_tick"] <= validation["start_tick"]:
                raise ContractError(f"{label} validated tick advancement is invalid")
            if validation["players"] != ["Multi0", "Multi1"]:
                raise ContractError(f"{label} validated perspectives are invalid")
            if validation["workload_profile"] != profile or validation[
                "application_proven"
            ] is not True:
                raise ContractError(f"{label} command-pressure profile is not proven")
            command_fields = (
                validation["actor_id_by_player"], validation["order_count_before"],
                validation["order_count_after"],
            )
            if profile == "noop_control":
                if validation["commands_submitted"] != 0 or any(command_fields):
                    raise ContractError(f"{label} noop control contains command pressure")
            else:
                if validation["commands_submitted"] != 2 or any(
                    set(field) != {"Multi0", "Multi1"} for field in command_fields
                ):
                    raise ContractError(f"{label} action command coverage is invalid")
                for player in ("Multi0", "Multi1"):
                    actor_id = validation["actor_id_by_player"][player]
                    before = validation["order_count_before"][player]
                    after = validation["order_count_after"][player]
                    if type(actor_id) is not int or actor_id <= 0 or type(before) is not int or (
                        before < 0 or type(after) is not int or after <= before
                    ):
                        raise ContractError(f"{label} action application evidence is invalid")
            if previous_end_tick is not None and validation["start_tick"] != previous_end_tick:
                raise ContractError(f"{label} validated tick intervals are not continuous")
            previous_end_tick = validation["end_tick"]
    _validate_teardown_evidence(value["teardown"], f"{label}.teardown")
    create_latency = value["create_latency"]
    create_max_s = (
        float(create_latency["max_ms"]) / 1000
        if create_latency["count"]
        else 0.0
    )
    teardown_latency = value["teardown"]["latency"]
    teardown_max_s = (
        float(teardown_latency["max_ms"]) / 1000
        if teardown_latency["count"]
        else 0.0
    )
    observed_phase_lower_bound = wall_seconds + create_max_s + teardown_max_s
    rounding_slack = 8 * max(
        math.ulp(end_to_end_wall_seconds),
        math.ulp(observed_phase_lower_bound),
    )
    if end_to_end_wall_seconds + rounding_slack < observed_phase_lower_bound:
        raise ContractError(
            f"{label}.end_to_end_wall_seconds does not cover observed nonoverlapping phases"
        )


def _validate_parameters_evidence(parameters: Any) -> dict[str, Any]:
    fields = {
        "concurrency", "tick_batches", "samples", "repetitions", "seed",
        "rpc_timeout_s", "cell_timeout_s", "teardown_timeout_s", "ready_timeout_s",
        "port", "map_name", "bots", "workload_profile",
    }
    parameters = _require_exact_fields(parameters, fields, "pending evidence parameters")
    concurrency = parameters["concurrency"]
    tick_batches = parameters["tick_batches"]
    if not isinstance(concurrency, list) or not concurrency or any(
        isinstance(value, bool) or not isinstance(value, int) or value not in ALLOWED_CONCURRENCY
        for value in concurrency
    ) or len(concurrency) != len(set(concurrency)):
        raise ContractError("pending evidence concurrency matrix is invalid")
    if not isinstance(tick_batches, list) or not tick_batches or any(
        isinstance(value, bool) or not isinstance(value, int) or value <= 0 or value > 10_000
        for value in tick_batches
    ) or len(tick_batches) != len(set(tick_batches)):
        raise ContractError("pending evidence tick matrix is invalid")
    for field in (
        "samples", "repetitions", "seed", "rpc_timeout_s", "cell_timeout_s",
        "teardown_timeout_s", "ready_timeout_s", "port",
    ):
        if isinstance(parameters[field], bool) or not isinstance(parameters[field], int) or parameters[
            field
        ] <= 0:
            raise ContractError(f"pending evidence parameter {field} is invalid")
    if parameters["repetitions"] < 2 or parameters["map_name"] != MAP_NAME or parameters[
        "bots"
    ] != BOTS:
        raise ContractError("pending evidence fixed benchmark parameters are invalid")
    if parameters["workload_profile"] not in WORKLOAD_PROFILES:
        raise ContractError("pending evidence workload profile is invalid")
    if parameters["seed"] + max(concurrency) - 1 > 2_147_483_647:
        raise ContractError("pending evidence seed/slot range exceeds the runtime integer domain")
    build_matrix(tuple(concurrency), tuple(tick_batches))
    return parameters


def _validate_cell_evidence(cell: dict[str, Any], parameters: dict[str, Any]) -> None:
    terminal = cell.get("terminal")
    if terminal not in ALLOWED_TERMINALS:
        raise ContractError("pending evidence contains an invalid matrix-cell terminal")
    if terminal == "not_executed":
        _require_exact_fields(
            cell,
            {"key", "terminal", "concurrency", "ticks_per_joint_advance", "blocked_by",
             "reason", "process_rss_bytes", "process_cpu_seconds"},
            "not-executed matrix cell",
        )
        if not isinstance(cell["blocked_by"], str) or not isinstance(cell["reason"], str):
            raise ContractError("not-executed matrix-cell reason is invalid")
        if cell["process_rss_bytes"] is not None or cell["process_cpu_seconds"] is not None:
            raise ContractError("not-executed matrix cell must not claim resource evidence")
        return
    common = {
        "key", "terminal", "concurrency", "ticks_per_joint_advance", "process_rss_bytes",
        "process_cpu_seconds",
        "teardown_failures", "teardown_latency", "teardown_attempted_session_ids",
        "teardown_destroyed_session_ids", "teardown_unretired_session_ids",
        "create_commit_response_ambiguous", "cleanup_after_work_cancellation",
        "daemon_identity_lost", "containment_required", "cleanup_terminals",
    }
    success = common | {
        "repetitions", "same_seed_deterministic", "hashes_by_slot", "cell_wall_seconds",
    }
    failure = common | {"error", "completed_repetitions"}
    if terminal == "rpc_error":
        failure |= {"error_type"}
        if cell.get("daemon_identity_lost") is True:
            failure |= {"prior_cell_terminal", "prior_cell_failure"}
    _require_exact_fields(
        cell, success if terminal in {"success", "teardown_error"} else failure,
        "matrix cell",
    )
    for field in ("concurrency", "ticks_per_joint_advance"):
        if isinstance(cell[field], bool) or not isinstance(cell[field], int) or cell[field] <= 0:
            raise ContractError(f"matrix cell {field} is invalid")
    rss = _require_exact_fields(
        cell["process_rss_bytes"], {"before", "peak", "after"}, "matrix-cell RSS",
    )
    for value in rss.values():
        if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
            raise ContractError("matrix-cell RSS scalar is invalid")
    for endpoint in ("before", "after"):
        if rss[endpoint] is not None and (
            rss["peak"] is None or rss[endpoint] > rss["peak"]
        ):
            raise ContractError("matrix-cell RSS peak does not cover observed endpoints")
    cpu = _require_exact_fields(
        cell["process_cpu_seconds"],
        {
            "clock_ticks_per_second", "before_ticks", "after_ticks",
            "delta_ticks", "delta_seconds",
        },
        "matrix-cell CPU",
    )
    for field in ("before_ticks", "after_ticks", "delta_ticks"):
        value = cpu[field]
        if value is not None and (type(value) is not int or value < 0):
            raise ContractError("matrix-cell CPU tick scalar is invalid")
    clock_ticks = cpu["clock_ticks_per_second"]
    if clock_ticks is not None and (type(clock_ticks) is not int or clock_ticks <= 0):
        raise ContractError("matrix-cell CPU clock tick rate is invalid")
    delta_seconds = cpu["delta_seconds"]
    if delta_seconds is not None and (
        type(delta_seconds) is not float
        or not math.isfinite(delta_seconds)
        or delta_seconds < 0
    ):
        raise ContractError("matrix-cell CPU seconds scalar is invalid")
    before_ticks = cpu["before_ticks"]
    after_ticks = cpu["after_ticks"]
    if before_ticks is None or after_ticks is None:
        if clock_ticks is not None or cpu["delta_ticks"] is not None or delta_seconds is not None:
            raise ContractError("matrix-cell CPU delta requires both tick endpoints")
    else:
        if clock_ticks is None or after_ticks < before_ticks:
            raise ContractError("matrix-cell CPU delta is not endpoint-bound")
        expected_delta_ticks = after_ticks - before_ticks
        if (
            cpu["delta_ticks"] != expected_delta_ticks
            or delta_seconds != expected_delta_ticks / clock_ticks
        ):
            raise ContractError("matrix-cell CPU delta is not exact-tick-bound")
    _require_string_list(cell["teardown_failures"], "matrix-cell teardown failures")
    _require_string_list(cell["teardown_attempted_session_ids"], "matrix-cell attempted")
    _require_string_list(cell["teardown_destroyed_session_ids"], "matrix-cell destroyed")
    unretired = _require_string_list(cell["teardown_unretired_session_ids"], "matrix-cell unretired")
    terminals = _require_string_list(cell["cleanup_terminals"], "matrix-cell cleanup terminals")
    _validate_latency_evidence(cell["teardown_latency"], "matrix-cell teardown latency")
    for field in (
        "create_commit_response_ambiguous", "cleanup_after_work_cancellation",
        "daemon_identity_lost", "containment_required",
    ):
        if not isinstance(cell[field], bool):
            raise ContractError(f"matrix-cell {field} must be boolean")
    if cell["containment_required"] != bool(
        cell["create_commit_response_ambiguous"] or unretired
        or cell["daemon_identity_lost"]
    ) or cell["containment_required"] != ("daemon_retirement_required" in terminals):
        raise ContractError("matrix-cell containment accounting is inconsistent")
    if cell["daemon_identity_lost"]:
        if terminal != "rpc_error":
            raise ContractError("daemon identity loss requires an RPC-error terminal")
        prior_terminal = cell["prior_cell_terminal"]
        prior_failure = cell["prior_cell_failure"]
        if prior_terminal not in {"success", "timeout", "rpc_error", "teardown_error"}:
            raise ContractError("daemon identity loss prior terminal is invalid")
        if prior_terminal == "success":
            if prior_failure is not None:
                raise ContractError("successful prior cell cannot claim a prior failure")
        else:
            prior_failure = _require_exact_fields(
                prior_failure,
                {"terminal", "error_type", "error"},
                "daemon identity loss prior cell failure",
            )
            if prior_failure["terminal"] != prior_terminal or not isinstance(
                prior_failure["error_type"], str
            ) or not isinstance(prior_failure["error"], str):
                raise ContractError("daemon identity loss prior failure is inconsistent")
    if terminal in {"success", "teardown_error"}:
        if not isinstance(cell["repetitions"], list) or not cell["repetitions"]:
            raise ContractError("completed matrix cell lacks repetition evidence")
        for index, repetition in enumerate(cell["repetitions"]):
            _validate_repetition_evidence(repetition, f"matrix-cell repetition {index}")
        if len(cell["repetitions"]) != parameters["repetitions"] or [
            repetition["repetition"] for repetition in cell["repetitions"]
        ] != list(range(parameters["repetitions"])):
            raise ContractError("matrix-cell repetition coverage is incomplete")
        for repetition in cell["repetitions"]:
            if repetition["teardown"]["teardown_total_deadline_s"] != parameters[
                "teardown_timeout_s"
            ]:
                raise ContractError(
                    "matrix-cell teardown deadline is not operation-parameter-bound"
                )
            if repetition["workload_profile"] != parameters["workload_profile"]:
                raise ContractError("matrix-cell workload profile is not parameter-bound")
            expected_slots = [str(slot) for slot in range(cell["concurrency"])]
            if sorted(repetition["seed_by_slot"]) != expected_slots:
                raise ContractError("matrix-cell concurrency/slot coverage is inconsistent")
            if repetition["create_latency"]["count"] != cell["concurrency"]:
                raise ContractError(
                    "matrix-cell create latency population is inconsistent"
                )
            expected_seed_by_slot = {
                str(slot): parameters["seed"] + slot
                for slot in range(cell["concurrency"])
            }
            if repetition["seed_by_slot"] != expected_seed_by_slot:
                raise ContractError("matrix-cell seed/slot evidence is not operation-bound")
            if repetition["joint_advance_calls"] != parameters["samples"] * cell[
                "concurrency"
            ] or repetition["ticks_advanced_validated"] != repetition[
                "joint_advance_calls"
            ] * cell["ticks_per_joint_advance"]:
                raise ContractError("matrix-cell advancement accounting is inconsistent")
            for validations in repetition["joint_advance_validation_by_slot"].values():
                for validation in validations:
                    if validation["end_tick"] - validation["start_tick"] != cell[
                        "ticks_per_joint_advance"
                    ]:
                        raise ContractError("matrix-cell validated tick delta is inconsistent")
        if not isinstance(cell["same_seed_deterministic"], bool) or not isinstance(
            cell["hashes_by_slot"], dict
        ):
            raise ContractError("matrix-cell determinism evidence is invalid")
        expected_hash_series = {
            slot: [repetition["canonical_hash_by_slot"][slot] for repetition in cell["repetitions"]]
            for slot in sorted(cell["repetitions"][0]["canonical_hash_by_slot"])
        }
        if cell["hashes_by_slot"] != expected_hash_series or cell[
            "same_seed_deterministic"
        ] != all(len(set(series)) == 1 for series in expected_hash_series.values()):
            raise ContractError("matrix-cell deterministic hash accounting is inconsistent")
        records = [repetition["teardown"] for repetition in cell["repetitions"]]
        if cell["teardown_failures"] != [
            failure for record in records for failure in record["failures"]
        ] or cell["teardown_attempted_session_ids"] != [
            session for record in records for session in record["attempted_session_ids"]
        ] or cell["teardown_destroyed_session_ids"] != [
            session for record in records for session in record["destroyed_session_ids"]
        ] or cell["teardown_unretired_session_ids"] != [
            session for record in records for session in record["unretired_session_ids"]
        ] or cell["cleanup_terminals"] != [record["cleanup_terminal"] for record in records]:
            raise ContractError("matrix-cell teardown aggregation is inconsistent")
        teardown_samples = [
            sample for record in records for sample in record["latency_samples_ms"]
        ]
        if cell["teardown_latency"] != latency_summary(teardown_samples):
            raise ContractError("matrix-cell teardown latency aggregation is inconsistent")
        _require_number(cell["cell_wall_seconds"], "matrix-cell wall time")
        if terminal == "success" and (
            not cell["same_seed_deterministic"] or cell["teardown_failures"]
            or cell["containment_required"]
        ):
            raise ContractError("successful matrix cell contradicts its evidence")
        if terminal == "teardown_error" and not (
            cell["teardown_failures"] or cell["containment_required"]
        ):
            raise ContractError("teardown-error matrix cell lacks cleanup evidence")
    else:
        if isinstance(cell["completed_repetitions"], bool) or not isinstance(
            cell["completed_repetitions"], int
        ) or cell["completed_repetitions"] < 0 or not isinstance(cell["error"], str):
            raise ContractError("failed matrix-cell evidence is invalid")
        if terminal == "rpc_error" and not isinstance(cell["error_type"], str):
            raise ContractError("RPC-error matrix-cell type is invalid")


def _validate_host_and_run(host: Any, run: Any, descriptor: dict[str, Any]) -> None:
    host = _require_exact_fields(
        host, {"hostname", "designated_hostname", "platform", "python", "cpu_count"},
        "pending evidence host",
    )
    for field in ("hostname", "designated_hostname", "platform", "python"):
        if not isinstance(host[field], str) or not host[field]:
            raise ContractError(f"pending evidence host {field} is invalid")
    if host["hostname"] != descriptor.get("designated_hostname") or host[
        "designated_hostname"
    ] != descriptor.get("designated_hostname"):
        raise ContractError("pending evidence host does not match the designated invocation")
    if host["cpu_count"] is not None and (
        isinstance(host["cpu_count"], bool) or not isinstance(host["cpu_count"], int)
        or host["cpu_count"] <= 0
    ):
        raise ContractError("pending evidence CPU count is invalid")

    required = {
        "terminal", "stage", "error_type", "error", "listener_identity",
        "runtime_provenance", "daemon_log", "cleanup", "containment",
    }
    allowed = required | {"daemon_returncode", "publication_terminal_persistence_error"}
    if not isinstance(run, dict) or not required.issubset(run) or not set(run).issubset(allowed):
        raise ContractError("pending evidence run fields are not exact")
    if run["terminal"] not in RUN_TERMINALS or not isinstance(run["stage"], str):
        raise ContractError("pending evidence run terminal is invalid")
    for field in ("error_type", "error"):
        if run[field] is not None and not isinstance(run[field], str):
            raise ContractError(f"pending evidence run {field} is invalid")
    cleanup = _require_exact_fields(run["cleanup"], {"failures"}, "runtime cleanup")
    _require_string_list(cleanup["failures"], "runtime cleanup failures")
    containment = _require_exact_fields(
        run["containment"], {"required_by_cell", "boundary", "daemon_retired"},
        "runtime containment",
    )
    if not isinstance(containment["required_by_cell"], bool) or not isinstance(
        containment["daemon_retired"], bool
    ) or containment["boundary"] not in {"not_required", "disposable_daemon_retirement"}:
        raise ContractError("runtime containment scalars are invalid")
    if containment["required_by_cell"] != (
        containment["boundary"] == "disposable_daemon_retirement"
    ):
        raise ContractError("runtime containment boundary is inconsistent")
    listener = run["listener_identity"]
    if listener is not None:
        listener = _require_exact_fields(
            listener, {"pid", "port", "socket_inode", "proc_table"},
            "runtime listener identity",
        )
        if any(
            isinstance(listener[field], bool) or not isinstance(listener[field], int)
            for field in ("pid", "port")
        ) or not isinstance(listener["socket_inode"], str) or listener[
            "proc_table"
        ] not in {"tcp", "tcp6"}:
            raise ContractError("runtime listener identity scalars are invalid")
    provenance = run["runtime_provenance"]
    if provenance is not None:
        provenance = _require_exact_fields(
            provenance,
            {"benchmark_source_git_head", "benchmark_source_sha256",
             "frozen_war_college_comparison_sha", "engine_git_head",
             "openra_binary_sha256", "dotnet_version", "dotnet_version_sha256"},
            "runtime provenance",
        )
        for field, pattern in (
            ("benchmark_source_git_head", r"[0-9a-f]{40}"),
            ("frozen_war_college_comparison_sha", r"[0-9a-f]{40}"),
            ("engine_git_head", r"[0-9a-f]{40}"),
            ("benchmark_source_sha256", r"[0-9a-f]{64}"),
            ("openra_binary_sha256", r"[0-9a-f]{64}"),
            ("dotnet_version_sha256", r"[0-9a-f]{64}"),
        ):
            if not isinstance(provenance[field], str) or not re.fullmatch(pattern, provenance[field]):
                raise ContractError(f"runtime provenance {field} is invalid")
        if not isinstance(provenance["dotnet_version"], str) or not provenance["dotnet_version"]:
            raise ContractError("runtime dotnet identity is invalid")
    log = run["daemon_log"]
    if log is not None:
        log = _require_exact_fields(
            log,
            {"total_bytes", "sha256", "tail_utf8", "tail_bytes", "drain_error",
             "drain_thread_retired"}, "daemon log",
        )
        if any(
            isinstance(log[field], bool) or not isinstance(log[field], int) or log[field] < 0
            for field in ("total_bytes", "tail_bytes")
        ) or log["tail_bytes"] > min(log["total_bytes"], MAX_DAEMON_LOG_TAIL_BYTES):
            raise ContractError("daemon log byte accounting is invalid")
        if not isinstance(log["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", log["sha256"]):
            raise ContractError("daemon log digest is invalid")
        if not isinstance(log["tail_utf8"], str) or (
            log["drain_error"] is not None and not isinstance(log["drain_error"], str)
        ) or not isinstance(log["drain_thread_retired"], bool):
            raise ContractError("daemon log terminal is invalid")
    if "daemon_returncode" in run and (
        isinstance(run["daemon_returncode"], bool) or not isinstance(run["daemon_returncode"], int)
    ):
        raise ContractError("daemon return code is invalid")
    if run["terminal"] == "completed" and (
        run["stage"] != "matrix_complete" or run["error"] is not None
        or run["error_type"] is not None or listener is None or provenance is None
        or log is None or not containment["daemon_retired"] or cleanup["failures"]
        or "daemon_returncode" not in run
    ):
        raise ContractError("completed runtime terminal lacks complete runtime provenance")


def _validate_run_global_cpu_evidence(
    cells: list[dict[str, Any]],
    planned: list[dict[str, int]],
) -> None:
    """Conserve one daemon CPU counter lineage across the planned matrix order."""
    cells_by_key = {cell["key"]: cell for cell in cells}
    clock_ticks_per_second: int | None = None
    previous_after_ticks: int | None = None
    for planned_cell in planned:
        key = (
            f"c{planned_cell['concurrency']}-"
            f"t{planned_cell['ticks_per_joint_advance']}"
        )
        cell = cells_by_key.get(key)
        if cell is None or cell["terminal"] == "not_executed":
            continue
        cpu = cell["process_cpu_seconds"]
        before_ticks = cpu["before_ticks"]
        after_ticks = cpu["after_ticks"]
        if before_ticks is None or after_ticks is None:
            continue
        current_clock = cpu["clock_ticks_per_second"]
        if clock_ticks_per_second is None:
            clock_ticks_per_second = current_clock
        elif current_clock != clock_ticks_per_second:
            raise ContractError(
                "run-global CPU clock tick rate is inconsistent across matrix cells"
            )
        if previous_after_ticks is not None and before_ticks < previous_after_ticks:
            raise ContractError(
                "run-global CPU cumulative ticks regress across matrix cells"
            )
        previous_after_ticks = after_ticks


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
    try:
        canonical_payload = stable_json(report).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContractError(f"pending evidence is not stable canonical JSON: {error}") from error
    if canonical_payload != payload:
        raise ContractError("pending evidence is not stable canonical JSON")
    expected_fields = {
        "marker", "schema_version", "runtime_evidence", "generated_at_utc",
        "provenance", "command", "host", "run", "parameters", "operation", "cells",
    }
    if set(report) != expected_fields:
        raise ContractError("pending evidence report fields are not exact")
    if type(report["schema_version"]) is not int:
        raise ContractError("pending evidence schema version is not an exact integer")
    if report["schema_version"] != SCHEMA_VERSION:
        raise IncompatibleEvidenceSchemaError(report["schema_version"], SCHEMA_VERSION)
    if report["runtime_evidence"] != "EXECUTED":
        raise ContractError("pending evidence is not an executed runtime attempt")

    operation = validate_operation(report["operation"], expected_operation)
    provenance = report["provenance"]
    if not isinstance(provenance, dict):
        raise ContractError("pending evidence provenance is absent")
    validated_provenance = validate_provenance(
        provenance.get("engine_sha", ""),
        provenance.get("war_college_sha", ""),
        provenance.get("benchmark_source_sha", ""),
        provenance.get("generation", ""),
    )
    if provenance != validated_provenance:
        raise ContractError("pending evidence provenance fields are not exact")

    parameters = _validate_parameters_evidence(report["parameters"])
    descriptor = operation["descriptor"]
    if descriptor.get("provenance") != provenance:
        raise ContractError("pending evidence operation does not bind report provenance")
    if descriptor.get("parameters") != parameters:
        raise ContractError("pending evidence operation does not bind report parameters")

    command = report["command"]
    if not isinstance(command, list) or not command or not all(
        isinstance(argument, str) for argument in command
    ):
        raise ContractError("pending evidence command is invalid")
    host = report["host"]
    if not isinstance(report["generated_at_utc"], str) or not report["generated_at_utc"]:
        raise ContractError("pending evidence generation time is invalid")

    run = report["run"]
    _validate_host_and_run(host, run, descriptor)
    cells = report["cells"]
    if not isinstance(cells, list) or not all(isinstance(cell, dict) for cell in cells):
        raise ContractError("pending evidence matrix cells are invalid")
    for cell in cells:
        _validate_cell_evidence(cell, parameters)
    concurrency = parameters["concurrency"]
    tick_batches = parameters["tick_batches"]
    planned = build_matrix(tuple(concurrency), tuple(tick_batches))
    expected_cell_keys = sorted(
        f"c{cell['concurrency']}-t{cell['ticks_per_joint_advance']}"
        for cell in planned
    )
    actual_cell_keys = [cell.get("key") for cell in cells]
    if not all(isinstance(key, str) for key in actual_cell_keys):
        raise ContractError("pending evidence matrix-cell keys are invalid")
    if len(actual_cell_keys) != len(set(actual_cell_keys)):
        raise ContractError("pending evidence matrix-cell keys are not unique")
    if any(key not in expected_cell_keys for key in actual_cell_keys):
        raise ContractError("pending evidence contains an unplanned matrix cell")
    _validate_run_global_cpu_evidence(cells, planned)
    if run["terminal"] == "completed" and actual_cell_keys != expected_cell_keys:
        raise ContractError("completed pending evidence does not close the planned matrix")

    rebuilt = build_report(
        provenance=provenance,
        parameters=parameters,
        cells=cells,
        executed_designated_host=True,
        generated_at_utc=report["generated_at_utc"],
        command=command,
        run=run,
        host=host,
        operation=operation,
    )
    if rebuilt != report:
        raise ContractError("pending evidence report does not match the closed schema")
    return report


def _pending_path(path: Path) -> Path:
    return path.parent / f".{path.name}.pending"


def _commit_receipt_path(path: Path) -> Path:
    return path.parent / f".{path.name}.commit"


def _commit_receipt_payload(path: Path, evidence_payload: bytes) -> bytes:
    receipt = {
        "marker": PUBLICATION_RECEIPT_MARKER,
        "schema_version": PUBLICATION_RECEIPT_SCHEMA_VERSION,
        "state": "COMMITTED",
        "evidence_name": path.name,
        "evidence_sha256": hashlib.sha256(evidence_payload).hexdigest(),
        "evidence_bytes": len(evidence_payload),
    }
    return stable_json(receipt).encode("utf-8")


def _validate_commit_receipt(
    receipt_payload: bytes,
    path: Path,
    evidence_payload: bytes,
) -> dict[str, Any]:
    try:
        receipt = json.loads(receipt_payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(f"evidence commit receipt is not canonical JSON: {error}") from error
    if not isinstance(receipt, dict) or set(receipt) != {
        "marker", "schema_version", "state", "evidence_name",
        "evidence_sha256", "evidence_bytes",
    }:
        raise ContractError("evidence commit receipt fields are not exact")
    if (
        not isinstance(receipt["marker"], str)
        or not isinstance(receipt["schema_version"], int)
        or isinstance(receipt["schema_version"], bool)
        or not isinstance(receipt["state"], str)
        or not isinstance(receipt["evidence_name"], str)
        or not isinstance(receipt["evidence_sha256"], str)
        or not isinstance(receipt["evidence_bytes"], int)
        or isinstance(receipt["evidence_bytes"], bool)
    ):
        raise ContractError("evidence commit receipt scalar types are not exact")
    if stable_json(receipt).encode("utf-8") != receipt_payload:
        raise ContractError("evidence commit receipt is not stable canonical JSON")
    expected = json.loads(_commit_receipt_payload(path, evidence_payload))
    if receipt != expected:
        raise ContractError("evidence commit receipt does not bind the canonical report")
    return receipt


def load_locally_committed_evidence(
    path: Path,
    expected_operation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Load durable local bytes without granting producer or countability authority.

    A schema-valid pending or final report and its locally self-issued commit
    receipt prove publication durability, not designated-host producer identity.
    The explicit wrapper prevents a local receipt from being confused with a
    producer-authenticated acceptance record.
    """
    path = Path(os.path.abspath(os.fspath(path)))
    evidence_payload = _read_regular_read_only(path)
    report = _validate_recoverable_evidence(evidence_payload, expected_operation)
    receipt_payload = _read_regular_read_only(_commit_receipt_path(path))
    receipt = _validate_commit_receipt(receipt_payload, path, evidence_payload)
    return {
        "marker": LOCAL_EVIDENCE_MARKER,
        "schema_version": LOCAL_EVIDENCE_SCHEMA_VERSION,
        "countable": False,
        "producer_authentication": "ABSENT",
        "report": report,
        "commit_receipt": receipt,
    }


def load_committed_evidence(
    path: Path,
    expected_operation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fail closed: this source generation has no countable-evidence trust root.

    A future consumer may authenticate a producer-issued attestation only when
    its verifier and immutable trust root are owned outside the evidence
    claimant and reviewed as a separate authority boundary.  This benchmark
    intentionally accepts no callbacks, verifier objects, paths, environment
    variables, or caller-supplied keys as substitutes for that boundary.
    """
    load_locally_committed_evidence(path, expected_operation)
    raise ContractError(
        "committed evidence is not countable: trusted producer attestation "
        "and an externally bound immutable trust root are not implemented"
    )


def _retire_pending(
    parent_descriptor: int,
    staging_name: str,
) -> tuple[bool, str | None]:
    try:
        os.unlink(staging_name, dir_fd=parent_descriptor)
        _fsync_directory(parent_descriptor)
        return True, None
    except OSError as error:
        # The final link was already fenced.  A retained owned alias is recovery
        # evidence, not authority to downgrade or replace the committed final.
        return False, f"{type(error).__name__}:{error}"


@dataclass
class EvidenceReservation:
    """Retained exact-inode authority for one evidence publication attempt."""

    path: Path
    staging: Path
    descriptor: int | None
    parent_descriptor: int | None

    def close(self) -> None:
        if self.descriptor is not None:
            os.close(self.descriptor)
            self.descriptor = None
        if self.parent_descriptor is not None:
            os.close(self.parent_descriptor)
            self.parent_descriptor = None


def require_unused_evidence_namespace(path: Path) -> None:
    """Fail closed on evidence from an earlier process or attempt.

    A source-only report and its public operation digest cannot authenticate the
    designated host that allegedly produced it.  Automatic recovery is therefore
    forbidden until a separately trusted producer-issued binding exists.  Keep
    any pending artifact intact for explicit reconciliation.
    """
    path = Path(os.path.abspath(os.fspath(path)))
    if not path.parent.is_dir():
        raise FileNotFoundError(f"evidence output parent must pre-exist: {path.parent}")
    staging = _pending_path(path)
    receipt = _commit_receipt_path(path)
    if os.path.lexists(path):
        raise FileExistsError(f"evidence output already exists: {path}")
    if os.path.lexists(receipt):
        raise ContractError(
            "evidence commit receipt requires explicit reconciliation; "
            "automatic recovery is disabled"
        )
    if os.path.lexists(staging):
        raise ContractError(
            "pending evidence requires explicit reconciliation; automatic recovery "
            "is disabled because producer provenance is not authenticated"
        )


def reserve_evidence_namespace(path: Path) -> EvidenceReservation:
    """Durably reserve the exact pending inode before any runtime contact.

    The reservation is deliberately a mode-0400 empty pending artifact until the
    benchmark report is complete.  An interrupted attempt therefore requires
    explicit reconciliation and can never be mistaken for completed evidence.
    """
    path = Path(os.path.abspath(os.fspath(path)))
    staging = _pending_path(path)
    receipt = _commit_receipt_path(path)
    parent_flags = (
        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        parent_descriptor = os.open(path.parent, parent_flags)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"evidence output parent must pre-exist: {path.parent}"
        ) from error
    try:
        _assert_parent_path_generation(path.parent, parent_descriptor)
        if _entry_exists(parent_descriptor, path.name):
            raise FileExistsError(f"evidence output already exists: {path}")
        if _entry_exists(parent_descriptor, receipt.name):
            raise ContractError(
                "evidence commit receipt requires explicit reconciliation; "
                "automatic recovery is disabled"
            )
        if _entry_exists(parent_descriptor, staging.name):
            raise ContractError(
                "pending evidence requires explicit reconciliation; automatic recovery "
                "is disabled because producer provenance is not authenticated"
            )
    except Exception:
        os.close(parent_descriptor)
        raise
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(staging.name, flags, 0o400, dir_fd=parent_descriptor)
    try:
        os.fchmod(descriptor, 0o400)
        os.fsync(descriptor)
        _fsync_directory(parent_descriptor)
        _assert_entry_generation(
            parent_descriptor, staging.name, descriptor, "pending reservation",
        )
        _assert_parent_path_generation(path.parent, parent_descriptor)
        if _entry_exists(parent_descriptor, path.name):
            raise FileExistsError(
                f"evidence output appeared while reserving the attempt: {path}"
            )
        return EvidenceReservation(
            path=path,
            staging=staging,
            descriptor=descriptor,
            parent_descriptor=parent_descriptor,
        )
    except Exception:
        os.close(descriptor)
        os.close(parent_descriptor)
        # Preserve the exact reservation name after any ambiguous durability or
        # namespace terminal.  It is not execution evidence and grants no retry
        # authority, but it truthfully fences this interrupted attempt.
        raise


def _write_reserved_payload(reservation: EvidenceReservation, payload: bytes) -> None:
    if reservation.descriptor is None or reservation.parent_descriptor is None:
        raise ContractError("evidence reservation is already closed")
    if len(payload) > MAX_EVIDENCE_BYTES:
        raise ContractError(f"evidence payload exceeds {MAX_EVIDENCE_BYTES} bytes")
    _validate_recoverable_evidence(payload)
    descriptor = reservation.descriptor
    os.lseek(descriptor, 0, os.SEEK_SET)
    os.ftruncate(descriptor, 0)
    with os.fdopen(descriptor, "wb", closefd=False) as stream:
        stream.write(payload)
        stream.flush()
        os.fchmod(stream.fileno(), 0o400)
        os.fsync(stream.fileno())


def _publish_commit_receipt_create_only(
    reservation: EvidenceReservation,
    evidence_payload: bytes,
) -> dict[str, Any]:
    if reservation.descriptor is None or reservation.parent_descriptor is None:
        raise ContractError("evidence reservation is already closed")
    path = reservation.path
    descriptor = reservation.descriptor
    parent_descriptor = reservation.parent_descriptor
    receipt = _commit_receipt_path(path)
    if _entry_exists(parent_descriptor, receipt.name):
        raise FileExistsError(f"evidence commit receipt already exists: {receipt}")
    _assert_entry_generation(parent_descriptor, path.name, descriptor, "final")
    _assert_parent_path_generation(path.parent, parent_descriptor)

    payload = _commit_receipt_payload(path, evidence_payload)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    receipt_descriptor = os.open(receipt.name, flags, 0o400, dir_fd=parent_descriptor)
    try:
        os.fchmod(receipt_descriptor, 0o400)
        with os.fdopen(receipt_descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(parent_descriptor)
        _assert_entry_generation(
            parent_descriptor, receipt.name, receipt_descriptor, "commit receipt",
        )
        _assert_entry_generation(parent_descriptor, path.name, descriptor, "final")
        _assert_parent_path_generation(path.parent, parent_descriptor)
    finally:
        os.close(receipt_descriptor)
    return {
        "path": str(receipt),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }


def publish_evidence_create_only(
    path: Path,
    payload: bytes,
    *,
    reservation: EvidenceReservation | None = None,
) -> dict[str, Any]:
    path = Path(os.path.abspath(os.fspath(path)))
    if len(payload) > MAX_EVIDENCE_BYTES:
        raise ContractError(f"evidence payload exceeds {MAX_EVIDENCE_BYTES} bytes")

    owns_reservation = reservation is None
    if reservation is None:
        reservation = reserve_evidence_namespace(path)
    if reservation.path != path or reservation.staging != _pending_path(path):
        raise ContractError("evidence reservation does not match the output path")
    if reservation.descriptor is None or reservation.parent_descriptor is None:
        raise ContractError("evidence reservation is already closed")

    staging = reservation.staging
    descriptor = reservation.descriptor
    parent_descriptor = reservation.parent_descriptor
    retired = False
    retirement_error: str | None = None
    commit_receipt: dict[str, Any] | None = None
    succeeded = False
    try:
        _write_reserved_payload(reservation, payload)
        # The pending name was made durable by reserve_evidence_namespace before
        # runtime contact. Retain both its exact descriptor and exact parent
        # directory so neither source nor destination authority is re-resolved.
        _assert_entry_generation(parent_descriptor, staging.name, descriptor, "pending")
        _assert_parent_path_generation(path.parent, parent_descriptor)
        if _entry_exists(parent_descriptor, path.name):
            raise FileExistsError(f"evidence output already exists: {path}")
        _link_open_inode_create_only(descriptor, parent_descriptor, path.name)
        _fsync_directory(parent_descriptor)
        _assert_entry_generation(parent_descriptor, path.name, descriptor, "final")
        _assert_parent_path_generation(path.parent, parent_descriptor)
        # This separately durable, content-addressed receipt is the canonical
        # commit point. A crash before it exists leaves only uncountable pending
        # or final bytes; schema-valid report bytes alone grant no completion.
        commit_receipt = _publish_commit_receipt_create_only(reservation, payload)
        try:
            _assert_entry_generation(parent_descriptor, staging.name, descriptor, "pending")
        except ContractError as error:
            # A replacement alias is not ours to remove after the exact owned
            # inode has been committed through the retained descriptor.
            retirement_error = f"{type(error).__name__}:{error}"
        else:
            retired, retirement_error = _retire_pending(
                parent_descriptor, staging.name,
            )
        _assert_entry_generation(parent_descriptor, path.name, descriptor, "final")
        _assert_parent_path_generation(path.parent, parent_descriptor)
        succeeded = True
    except Exception:
        # The immutable pending inode is the recovery authority.  Never unlink
        # it after an ambiguous final-link or directory-durability terminal.
        raise
    finally:
        # Callers that reserved before runtime retain the exact inode after a
        # publication error so they can persist the truthful output_error
        # terminal. Standalone helper calls own and always close their lease.
        if owns_reservation or succeeded:
            reservation.close()
    return {
        "path": str(path),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "recovered": False,
        "payload_matches_request": True,
        "pending_retired": retired,
        "pending_retirement_error": retirement_error,
        "commit_receipt": commit_receipt,
    }


def rss_bytes(pid: int) -> int | None:
    try:
        for line in Path(f"/proc/{pid}/status").read_text(encoding="utf-8").splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
        return None
    return None


def process_cpu_sample(pid: int) -> tuple[int, int] | None:
    """Return exact daemon user+system CPU ticks and their Linux clock rate.

    The process name in ``/proc/<pid>/stat`` may contain spaces, so fields
    are indexed only after its final closing parenthesis. Missing process data
    is represented as ``None``, never fabricated as zero work.
    """
    try:
        stat_line = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        fields = stat_line[stat_line.rindex(")") + 2:].split()
        # fields[0] is procfs field 3 (state); utime/stime are fields 14/15.
        clock_ticks = os.sysconf("SC_CLK_TCK")
        if not isinstance(clock_ticks, int) or clock_ticks <= 0:
            return None
        ticks = int(fields[11]) + int(fields[12])
        if ticks < 0:
            return None
        return ticks, clock_ticks
    except (
        FileNotFoundError, PermissionError, ProcessLookupError, ValueError,
        IndexError, OSError,
    ):
        return None


def process_cpu_interval(
    before: tuple[int, int] | None, after: tuple[int, int] | None,
) -> dict[str, int | float | None]:
    """Build one fail-closed interval without subtracting cumulative floats."""
    before_ticks = before[0] if before is not None else None
    after_ticks = after[0] if after is not None else None
    empty = {
        "clock_ticks_per_second": None,
        "before_ticks": before_ticks,
        "after_ticks": after_ticks,
        "delta_ticks": None,
        "delta_seconds": None,
    }
    if before is None or after is None:
        return empty
    if (
        type(before[0]) is not int or type(before[1]) is not int
        or type(after[0]) is not int or type(after[1]) is not int
        or before[0] < 0 or after[0] < before[0]
        or before[1] <= 0 or after[1] != before[1]
    ):
        return empty
    delta_ticks = after[0] - before[0]
    return {
        "clock_ticks_per_second": before[1],
        "before_ticks": before[0],
        "after_ticks": after[0],
        "delta_ticks": delta_ticks,
        "delta_seconds": delta_ticks / before[1],
    }


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
        if after is not None and (self.cell_peak is None or after > self.cell_peak):
            self.cell_peak = after
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


def _joint_observations_by_player(response: Any) -> dict[str, Any]:
    wrappers = list(getattr(response, "player_observations", ()))
    players = [getattr(wrapper, "player", None) for wrapper in wrappers]
    if len(players) != 2 or set(players) != {"Multi0", "Multi1"}:
        raise ContractError("JointAdvance response must contain exactly Multi0 and Multi1 perspectives")
    observations: dict[str, Any] = {}
    for wrapper in wrappers:
        has_field = getattr(wrapper, "HasField", None)
        if callable(has_field) and not has_field("observation"):
            raise ContractError(f"JointAdvance {wrapper.player} perspective lacks observation payload")
        observation = getattr(wrapper, "observation", None)
        if observation is None:
            raise ContractError(f"JointAdvance {wrapper.player} perspective lacks observation payload")
        observations[wrapper.player] = observation
    return observations


def _exact_order_count(observation: Any, player: str) -> int:
    military = getattr(observation, "military", None)
    count = getattr(military, "order_count", None)
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise ContractError(f"JointAdvance {player} order_count is not an exact nonnegative integer")
    return count


def build_stop_owned_unit_batches(pb2: Any, response: Any) -> tuple[list[Any], dict[str, Any]]:
    observations = _joint_observations_by_player(response)
    batches: list[Any] = []
    expectation: dict[str, Any] = {}
    for player in ("Multi0", "Multi1"):
        observation = observations[player]
        actor_ids = sorted(
            getattr(unit, "actor_id", None)
            for unit in getattr(observation, "units", ())
            if isinstance(getattr(unit, "actor_id", None), int)
            and not isinstance(getattr(unit, "actor_id", None), bool)
            and getattr(unit, "actor_id", None) > 0
        )
        if not actor_ids:
            raise ContractError(f"stop_owned_unit lacks an owned unit for {player}")
        actor_id = actor_ids[0]
        before = _exact_order_count(observation, player)
        batches.append(pb2.PlayerCommandBatch(
            player=player,
            commands=[pb2.Command(action=pb2.STOP, actor_id=actor_id)],
        ))
        expectation[player] = {"actor_id": actor_id, "order_count_before": before}
    return batches, expectation


def validate_joint_response(
    response: Any,
    session_id: str,
    requested_ticks: int,
    *,
    workload_profile: str = "noop_control",
    command_expectation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if getattr(response, "session_id", None) != session_id:
        raise ContractError("JointAdvance response session binding mismatch")
    start_tick = getattr(response, "start_tick", None)
    end_tick = getattr(response, "end_tick", None)
    require_proto_int32_tick(start_tick, "JointAdvance response start_tick")
    require_proto_int32_tick(end_tick, "JointAdvance response end_tick")
    if end_tick - start_tick != requested_ticks:
        raise ContractError("JointAdvance response did not prove requested tick advancement")
    observations = _joint_observations_by_player(response)
    if workload_profile == "noop_control":
        if command_expectation not in (None, {}):
            raise ContractError("noop_control cannot claim action-bearing command evidence")
        return {
            "start_tick": start_tick, "end_tick": end_tick,
            "players": sorted(observations), "workload_profile": workload_profile,
            "commands_submitted": 0, "actor_id_by_player": {},
            "order_count_before": {}, "order_count_after": {},
            "application_proven": True,
        }
    if workload_profile != "stop_owned_unit" or not isinstance(command_expectation, dict) or set(
        command_expectation
    ) != {"Multi0", "Multi1"}:
        raise ContractError("action-bearing JointAdvance command expectation is invalid")
    actor_id_by_player: dict[str, int] = {}
    before_by_player: dict[str, int] = {}
    after_by_player: dict[str, int] = {}
    for player in ("Multi0", "Multi1"):
        expected = command_expectation[player]
        if not isinstance(expected, dict) or set(expected) != {"actor_id", "order_count_before"}:
            raise ContractError("stop_owned_unit command expectation is malformed")
        actor_id = expected["actor_id"]
        before = expected["order_count_before"]
        after = _exact_order_count(observations[player], player)
        if type(actor_id) is not int or actor_id <= 0 or type(before) is not int or before < 0:
            raise ContractError("stop_owned_unit command expectation uses invalid scalars")
        if after <= before:
            raise ContractError(f"stop_owned_unit did not prove order application for {player}")
        actor_id_by_player[player] = actor_id
        before_by_player[player] = before
        after_by_player[player] = after
    return {
        "start_tick": start_tick, "end_tick": end_tick,
        "players": sorted(observations), "workload_profile": workload_profile,
        "commands_submitted": 2, "actor_id_by_player": actor_id_by_player,
        "order_count_before": before_by_player, "order_count_after": after_by_player,
        "application_proven": True,
    }


async def destroy_sessions(
    stub: Any, pb2: Any, session_ids: list[str], timeout_s: float,
) -> dict[str, Any]:
    attempted = list(dict.fromkeys(session_ids))
    failures: list[str] = []
    latencies: list[float] = []
    destroyed: list[str] = []
    deadline = time.monotonic() + timeout_s

    async def destroy(session_id: str) -> tuple[str, float]:
        started = time.monotonic()
        await stub.DestroySession(pb2.DestroySessionRequest(session_id=session_id))
        return session_id, (time.monotonic() - started) * 1000

    def consume_late_completion(task: asyncio.Task[Any]) -> None:
        # A cancellation-resistant RPC must not extend the total deadline. Its
        # session remains unretired and therefore requires daemon containment;
        # consume any eventual terminal only to avoid an orphan-task warning.
        try:
            task.result()
        except BaseException:
            pass

    tasks = {session_id: asyncio.create_task(destroy(session_id)) for session_id in attempted}
    if tasks:
        remaining = max(0.0, deadline - time.monotonic())
        done, pending = await asyncio.wait(tasks.values(), timeout=remaining)
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
            task.add_done_callback(consume_late_completion)
        if pending:
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
    containment: RuntimeTaskContainment | None = None,
    workload_profile: str = "noop_control",
    monotonic_clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    if workload_profile not in WORKLOAD_PROFILES:
        raise ContractError("unsupported workload profile")
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
    create_phase_accepting_results = False
    end_to_end_started = monotonic_clock()
    measured_wall_s: float | None = None
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
            if not create_phase_accepting_results:
                raise ContractError("CreateSession response arrived after owned phase terminal")
            # Record ownership immediately: if a sibling create fails or the
            # phase is cancelled, this session still has to be destroyed.
            if not isinstance(response.session_id, str) or not response.session_id:
                raise ContractError("CreateSession returned an invalid session ID")
            session_id_by_slot[slot] = response.session_id
            await wait_session_playing(stub, pb2, response.session_id, rpc_timeout_s)
            return slot, response.session_id, (time.monotonic() - t0) * 1000

        create_phase_started = True
        create_phase_accepting_results = True
        try:
            created_by_task = await run_owned_phase(
                {str(slot): create(slot) for slot in range(concurrency)},
                deadline_s=rpc_timeout_s,
                containment=containment,
            )
            create_phase_complete = True
        finally:
            create_phase_accepting_results = False
        created = list(created_by_task.values())
        created.sort(key=lambda item: item[0])
        if [item[0] for item in created] != list(range(concurrency)):
            raise ContractError("CreateSession results do not cover every requested slot")
        if len(set(session_id_by_slot.values())) != concurrency:
            raise ContractError("CreateSession returned duplicate session ownership")
        create_latencies.extend(item[2] for item in created)

        bootstrap_validation_by_slot: dict[int, dict[str, Any]] = {}
        previous_response_by_slot: dict[int, Any] = {}
        if workload_profile == "stop_owned_unit":
            async def bootstrap(slot: int, session_id: str) -> tuple[int, Any, dict[str, Any]]:
                response = await asyncio.wait_for(
                    stub.JointAdvance(pb2.JointAdvanceRequest(
                        session_id=session_id,
                        ticks=1,
                        player_actions=[
                            pb2.PlayerCommandBatch(player="Multi0"),
                            pb2.PlayerCommandBatch(player="Multi1"),
                        ],
                    )),
                    timeout=rpc_timeout_s,
                )
                validation = validate_joint_response(response, session_id, 1)
                return slot, response, {
                    "start_tick": validation["start_tick"],
                    "end_tick": validation["end_tick"],
                    "players": validation["players"],
                    "purpose": "owned_actor_and_order_count_bootstrap",
                }

            bootstrapped = await run_owned_phase(
                {
                    str(slot): bootstrap(slot, session_id_by_slot[slot])
                    for slot in range(concurrency)
                },
                deadline_s=rpc_timeout_s,
                containment=containment,
            )
            for slot, response, validation in bootstrapped.values():
                previous_response_by_slot[slot] = response
                bootstrap_validation_by_slot[slot] = validation

        final_by_slot: dict[int, dict[str, Any]] = {}
        validation_by_slot: dict[int, list[dict[str, Any]]] = {}
        measured_started = monotonic_clock()
        for _sample in range(samples):
            async def advance(slot: int, session_id: str) -> tuple[int, float, dict[str, Any]]:
                command_expectation = None
                if workload_profile == "stop_owned_unit":
                    player_actions, command_expectation = build_stop_owned_unit_batches(
                        pb2, previous_response_by_slot[slot],
                    )
                else:
                    player_actions = [
                        pb2.PlayerCommandBatch(player="Multi0"),
                        pb2.PlayerCommandBatch(player="Multi1"),
                    ]
                request = pb2.JointAdvanceRequest(
                    session_id=session_id,
                    ticks=ticks,
                    player_actions=player_actions,
                )
                t0 = time.monotonic()
                response = await asyncio.wait_for(stub.JointAdvance(request), timeout=rpc_timeout_s)
                elapsed_ms = (time.monotonic() - t0) * 1000
                validation = validate_joint_response(
                    response,
                    session_id,
                    ticks,
                    workload_profile=workload_profile,
                    command_expectation=command_expectation,
                )
                as_dict = message_to_dict(response, preserving_proto_field_name=True)
                return slot, elapsed_ms, {
                    "raw_response": response, "response": as_dict, "validation": validation,
                }

            advanced_by_task = await run_owned_phase(
                {
                    str(slot): advance(slot, session_id_by_slot[slot])
                    for slot in range(concurrency)
                },
                deadline_s=rpc_timeout_s,
                containment=containment,
            )
            advanced = list(advanced_by_task.values())
            for slot, elapsed_ms, envelope in advanced:
                advance_latencies.append(elapsed_ms)
                previous_response_by_slot[slot] = envelope["raw_response"]
                final_by_slot[slot] = envelope["response"]
                interval_chain = validation_by_slot.setdefault(slot, [])
                expected_start_tick = (
                    interval_chain[-1]["end_tick"]
                    if interval_chain
                    else bootstrap_validation_by_slot.get(slot, {}).get("end_tick")
                )
                if (
                    expected_start_tick is not None
                    and envelope["validation"]["start_tick"] != expected_start_tick
                ):
                    raise ContractError(
                        "JointAdvance responses do not prove continuous tick advancement"
                    )
                interval_chain.append(envelope["validation"])

        measured_wall_s = monotonic_clock() - measured_started
        if measured_wall_s <= 0:
            raise ContractError("measured JointAdvance phase wall time must be positive")

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

    end_to_end_wall_s = monotonic_clock() - end_to_end_started
    if measured_wall_s is None:
        raise ContractError("measured JointAdvance phase did not complete")
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
        "workload_profile": workload_profile,
        "bootstrap_joint_advance_calls": len(bootstrap_validation_by_slot),
        "bootstrap_ticks_advanced_validated": len(bootstrap_validation_by_slot),
        "bootstrap_validation_by_slot": {
            str(slot): validation
            for slot, validation in sorted(bootstrap_validation_by_slot.items())
        },
        "validated_ticks_per_second": (len(advance_latencies) * ticks) / measured_wall_s,
        "canonical_hash_by_slot": hashes,
        "joint_advance_validation_by_slot": {
            str(slot): validation for slot, validation in sorted(validation_by_slot.items())
        },
        "teardown": teardown,
        "wall_seconds": measured_wall_s,
        "end_to_end_wall_seconds": end_to_end_wall_s,
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
    containment: RuntimeTaskContainment | None = None,
    workload_profile: str = "noop_control",
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
            "daemon_identity_lost": False,
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
                containment=containment,
                workload_profile=workload_profile,
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


def bind_post_cell_daemon_identity(
    terminal: str,
    payload: dict[str, Any],
    cell: dict[str, int],
    process_rss_bytes: dict[str, int | None],
    process_cpu_seconds: dict[str, int | float | None],
    *,
    identity_intact: bool,
) -> tuple[str, dict[str, Any]]:
    """Bind the post-cell listener check to one schema-valid terminal payload."""
    bound = {
        **payload,
        **cell,
        "process_rss_bytes": process_rss_bytes,
        "process_cpu_seconds": process_cpu_seconds,
    }
    if identity_intact:
        return terminal, bound

    cleanup_terminals = list(bound["cleanup_terminals"])
    if "daemon_retirement_required" not in cleanup_terminals:
        cleanup_terminals.append("daemon_retirement_required")
    if terminal == "success":
        prior_failure = None
    elif terminal == "timeout":
        prior_failure = {
            "terminal": terminal,
            "error_type": "TimeoutError",
            "error": bound["error"],
        }
    elif terminal == "rpc_error":
        prior_failure = {
            "terminal": terminal,
            "error_type": bound["error_type"],
            "error": bound["error"],
        }
    elif terminal == "teardown_error":
        prior_failure = {
            "terminal": terminal,
            "error_type": "TeardownError",
            "error": ";".join(bound["teardown_failures"])
            or "session teardown requires disposable-daemon containment",
        }
    else:
        raise ContractError(f"unsupported pre-identity-loss cell terminal: {terminal}")
    failure = {
        **cell,
        "process_rss_bytes": process_rss_bytes,
        "process_cpu_seconds": process_cpu_seconds,
        "teardown_failures": bound["teardown_failures"],
        "teardown_latency": bound["teardown_latency"],
        "teardown_attempted_session_ids": bound["teardown_attempted_session_ids"],
        "teardown_destroyed_session_ids": bound["teardown_destroyed_session_ids"],
        "teardown_unretired_session_ids": bound["teardown_unretired_session_ids"],
        "create_commit_response_ambiguous": bound["create_commit_response_ambiguous"],
        "cleanup_after_work_cancellation": bound["cleanup_after_work_cancellation"],
        "daemon_identity_lost": True,
        "containment_required": True,
        "cleanup_terminals": cleanup_terminals,
        "error_type": "DaemonIdentityError",
        "error": "spawned daemon/listener ownership lost during cell",
        "prior_cell_terminal": terminal,
        "prior_cell_failure": prior_failure,
        "completed_repetitions": bound.get(
            "completed_repetitions",
            len(bound.get("repetitions", [])),
        ),
    }
    return "rpc_error", failure


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
            "process_cpu_seconds": None,
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
    containment = RuntimeTaskContainment()
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
            cpu_before = process_cpu_sample(daemon.pid)
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
                containment=containment,
                workload_profile=args.workload_profile,
            )
            cpu_after = process_cpu_sample(daemon.pid)
            terminal, payload = bind_post_cell_daemon_identity(
                terminal,
                payload,
                cell,
                sampler.end_cell(),
                process_cpu_interval(cpu_before, cpu_after),
                identity_intact=(
                    daemon.poll() is None
                    and process_listener_identity(daemon.pid, args.port) == listener_identity
                ),
            )
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
        containment_required = containment.required or any(
            bool(cell.payload.get("containment_required"))
            for cell in ledger.values()
        )
        if channel is not None:
            try:
                close_failure = await close_channel_with_total_deadline(channel, 5.0)
                if close_failure is not None:
                    cleanup_failures.append(f"channel:{close_failure}")
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
        remaining_contained_tasks = await retire_contained_tasks(containment, 5.0)
        if remaining_contained_tasks:
            cleanup_failures.append(
                f"owned_phase_tasks_unretired_after_containment:{remaining_contained_tasks}"
            )
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
    result.add_argument(
        "--workload-profile",
        choices=WORKLOAD_PROFILES,
        default="noop_control",
        help=(
            "experiment contract: noop_control sends no player commands and measures "
            "JointAdvance control traffic; stop_owned_unit submits one STOP per player "
            "and proves aggregate order-pressure only, not action-specific application "
            "or representative tactical training (default: noop_control)"
        ),
    )
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
    if args.seed + max(concurrency) - 1 > 2_147_483_647:
        raise ContractError("seed/slot range exceeds the runtime integer domain")
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
        "workload_profile": args.workload_profile,
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
            # A pre-positioned report is not designated-host authority.  Refuse
            # it before runtime contact and preserve it for explicit review.
            reservation = reserve_evidence_namespace(Path(args.output))
            try:
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
                    publication = publish_evidence_create_only(
                        Path(args.output), payload, reservation=reservation,
                    )
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
                    # The same retained inode that held the attempted completed
                    # report must carry the process's authoritative failure
                    # terminal. Otherwise explicit reconciliation could count a
                    # durable `completed` artifact after canonical publication
                    # failed and stdout truthfully reported `output_error`.
                    try:
                        _write_reserved_payload(
                            reservation,
                            stable_json(report).encode("utf-8"),
                        )
                    except (OSError, ContractError) as persistence_error:
                        report["run"]["publication_terminal_persistence_error"] = (
                            f"{type(persistence_error).__name__}:{persistence_error}"
                        )
                        report = json.loads(json.dumps(report, allow_nan=False))
            finally:
                reservation.close()
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
