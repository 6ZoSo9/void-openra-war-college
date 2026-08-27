#!/usr/bin/env python3
"""Bounded JointAdvance throughput and resource benchmark for VOID War College.

The module is deliberately importable without grpc or generated protobuf modules so
its source-only contracts can be tested on hosts without the OpenRA runtime. Runtime
imports occur only after ``run`` receives the explicit designated-host attestation.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import platform
import re
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Iterable


MARKER = "VOID_WAR_COLLEGE_JOINT_ADVANCE_BENCHMARK_V1"
SCHEMA_VERSION = 1
FROZEN_ENGINE_SHA = "1607a7a6501d42a47638393ecef8b22831064932"
FROZEN_WAR_COLLEGE_SHA = "973802ef0a614e5afa782ff20e231e18966ae3e5"
GENERATION = "ad1926569b12466c"
ALLOWED_CONCURRENCY = (1, 2, 4, 8)
ALLOWED_TERMINALS = {"success", "timeout", "rpc_error", "teardown_error"}
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


def validate_provenance(engine_sha: str, war_college_sha: str, generation: str) -> dict[str, str]:
    require_sha40(engine_sha, "engine SHA")
    require_sha40(war_college_sha, "War College SHA")
    if not GENERATION_RE.fullmatch(generation):
        raise ContractError("generation must be exactly 16 lowercase hex characters")
    return {
        "engine_sha": engine_sha,
        "war_college_sha": war_college_sha,
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
    host: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runtime_evidence = "EXECUTED" if executed_designated_host else "PENDING_DESIGNATED_HOST"
    if runtime_evidence == "EXECUTED" and not cells:
        raise ContractError("executed runtime evidence requires at least one terminal cell")
    if not executed_designated_host and cells:
        raise ContractError("source-only evidence must not contain measured runtime cells")
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
        "parameters": parameters,
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


def human_summary(report: dict[str, Any]) -> str:
    terminals = {terminal: 0 for terminal in sorted(ALLOWED_TERMINALS)}
    for cell in report["cells"]:
        terminals[cell["terminal"]] += 1
    counts = ", ".join(f"{key}={value}" for key, value in terminals.items())
    return (
        f"{MARKER} runtime_evidence={report['runtime_evidence']} "
        f"cells={len(report['cells'])} {counts}"
    )


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
        self._stop = asyncio.Event()

    async def run(self) -> None:
        while not self._stop.is_set():
            value = rss_bytes(self.pid)
            if value is not None and (self.peak is None or value > self.peak):
                self.peak = value
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=0.05)
            except TimeoutError:
                pass

    def stop(self) -> None:
        self.after = rss_bytes(self.pid)
        self._stop.set()


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


async def wait_ready(stub: Any, pb2: Any, timeout_s: float) -> None:
    deadline = time.monotonic() + timeout_s
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            await asyncio.wait_for(stub.GetState(pb2.StateRequest()), timeout=2.0)
            return
        except Exception as error:  # runtime boundary: grpc error subclasses vary
            last_error = error
            await asyncio.sleep(0.25)
    raise TimeoutError(f"daemon readiness exceeded {timeout_s}s: {last_error}")


async def destroy_sessions(stub: Any, pb2: Any, session_ids: list[str], timeout_s: float) -> list[str]:
    failures: list[str] = []
    for session_id in session_ids:
        try:
            await asyncio.wait_for(
                stub.DestroySession(pb2.DestroySessionRequest(session_id=session_id)),
                timeout=timeout_s,
            )
        except Exception as error:
            failures.append(f"{session_id}:{type(error).__name__}:{error}")
    return failures


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
) -> dict[str, Any]:
    session_ids: list[str] = []
    create_latencies: list[float] = []
    advance_latencies: list[float] = []
    hashes: dict[str, str] = {}
    teardown_failures: list[str] = []
    started = time.monotonic()
    try:
        async def create(slot: int) -> tuple[int, str, float]:
            t0 = time.monotonic()
            response = await asyncio.wait_for(
                stub.CreateSession(pb2.CreateSessionRequest(
                    map_name="singles.oramap",
                    bots="Multi1:rl-agent,Multi0:rl-agent",
                    seed=seed_base + slot,
                )),
                timeout=rpc_timeout_s,
            )
            return slot, response.session_id, (time.monotonic() - t0) * 1000

        created = await asyncio.gather(*(create(slot) for slot in range(concurrency)))
        created.sort(key=lambda item: item[0])
        session_ids.extend(item[1] for item in created)
        create_latencies.extend(item[2] for item in created)

        final_by_slot: dict[int, dict[str, Any]] = {}
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
                as_dict = message_to_dict(response, preserving_proto_field_name=True)
                return slot, elapsed_ms, as_dict

            advanced = await asyncio.gather(*(
                advance(slot, session_id) for slot, session_id in enumerate(session_ids)
            ))
            for slot, elapsed_ms, response in advanced:
                advance_latencies.append(elapsed_ms)
                final_by_slot[slot] = response

        for slot, response in sorted(final_by_slot.items()):
            hashes[str(slot)] = canonical_state_hash(response)
    finally:
        teardown_failures = await destroy_sessions(stub, pb2, session_ids, teardown_timeout_s)

    wall_s = time.monotonic() - started
    return {
        "repetition": repetition,
        "seed_by_slot": {str(slot): seed_base + slot for slot in range(concurrency)},
        "create_latency": latency_summary(create_latencies),
        "joint_advance_latency": latency_summary(advance_latencies),
        "joint_advance_calls": len(advance_latencies),
        "ticks_advanced_requested": len(advance_latencies) * ticks,
        "requested_ticks_per_second": (len(advance_latencies) * ticks) / wall_s if wall_s > 0 else 0,
        "canonical_hash_by_slot": hashes,
        "teardown_failures": teardown_failures,
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
    try:
        async with asyncio.timeout(cell_timeout_s):
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
                ))
    except TimeoutError as error:
        return "timeout", {"error": str(error), "completed_repetitions": len(repetition_results)}
    except Exception as error:
        return "rpc_error", {
            "error_type": type(error).__name__,
            "error": str(error),
            "completed_repetitions": len(repetition_results),
        }

    teardown_errors = [
        failure
        for repetition in repetition_results
        for failure in repetition["teardown_failures"]
    ]
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
        "teardown_failures": teardown_errors,
    }
    return ("teardown_error" if teardown_errors else "success"), payload


async def execute_runtime(args: argparse.Namespace, parameters: dict[str, Any]) -> list[dict[str, Any]]:
    grpc, message_to_dict, pb2, pb2_grpc = _runtime_modules()
    daemon = start_daemon(Path(args.openra_dir).resolve(), args.port)
    sampler = RssSampler(daemon.pid)
    sampler_task = asyncio.create_task(sampler.run())
    channel = grpc.aio.insecure_channel(
        f"127.0.0.1:{args.port}",
        options=[
            ("grpc.max_receive_message_length", 64 * 1024 * 1024),
            ("grpc.max_send_message_length", 16 * 1024 * 1024),
        ],
    )
    ledger = CellLedger()
    try:
        stub = pb2_grpc.RLBridgeStub(channel)
        await wait_ready(stub, pb2, args.ready_timeout_s)
        for cell in build_matrix(parameters["concurrency"], parameters["tick_batches"]):
            key = f"c{cell['concurrency']}-t{cell['ticks_per_joint_advance']}"
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
            ledger.finalize(key, terminal, payload)
            if not matrix_may_continue(terminal):
                break
    finally:
        await channel.close()
        sampler.stop()
        await sampler_task
        daemon.terminate()
        try:
            daemon.wait(timeout=5)
        except subprocess.TimeoutExpired:
            daemon.kill()
            daemon.wait(timeout=5)

    return [
        {
            "key": cell.key,
            "terminal": cell.terminal,
            **cell.payload,
            "process_rss_bytes": {
                "before": sampler.before,
                "peak": sampler.peak,
                "after": sampler.after,
            },
        }
        for cell in ledger.values()
    ]


def utc_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("mode", choices=("plan", "run"))
    result.add_argument("--engine-sha", required=True)
    result.add_argument("--war-college-sha", required=True)
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
    }


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        provenance = validate_provenance(args.engine_sha, args.war_college_sha, args.generation)
        parameters = normalized_args(args)
        if args.mode == "run":
            if not args.execute_designated_host:
                raise ContractError("run requires --execute-designated-host")
            if not args.openra_dir or not args.output:
                raise ContractError("run requires --openra-dir and --output")
            cells = asyncio.run(execute_runtime(args, parameters))
            report = build_report(
                provenance=provenance,
                parameters=parameters,
                cells=cells,
                executed_designated_host=True,
                generated_at_utc=utc_now(),
                command=sys.argv,
                host={
                    "hostname": socket.gethostname(),
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                    "cpu_count": os.cpu_count(),
                },
            )
            Path(args.output).write_text(stable_json(report), encoding="utf-8")
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
                command=sys.argv,
            )
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except ContractError as error:
        print(f"contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
