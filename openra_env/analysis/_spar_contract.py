"""Strict evidence parsing and identity contracts for spar analysis."""

from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path
from typing import Any

MARKER = "VOID_WAR_COLLEGE_SPAR_TRAINING_UTILITY_V1"
MAX_TRAJECTORY_BYTES = 64 * 1024 * 1024
MAX_SUMMARY_BYTES = 4 * 1024 * 1024
MAX_ROUNDS = 10_000
SHA256 = re.compile(r"[0-9a-f]{64}")
SHA40 = re.compile(r"[0-9a-f]{40}")
GENERATION = re.compile(r"[0-9a-f]{16}")
IMAGE = re.compile(r"sha256:[0-9a-f]{64}")
DAMAGE = (
    "units_killed", "units_lost", "buildings_killed",
    "buildings_lost", "kills_cost", "deaths_cost",
)
SIDES = {
    "apollyon": ("apollyon_state", "apollyon_after"),
    "abaddon": ("abaddon_state", "abaddon_after"),
}
HOSTILE = {"attack_move", "attack_target"}
PASSIVE = {"advance", "no_op"}


class ContractError(ValueError):
    """The supplied evidence does not satisfy the analysis contract."""


def _obj(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be an object")
    return value


def _arr(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{label} must be an array")
    return value


def _int(value: Any, label: str, low: int = 0, high: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < low:
        raise ContractError(f"{label} must be an integer >= {low}")
    if high is not None and value > high:
        raise ContractError(f"{label} must be <= {high}")
    return value


def _str(value: Any, label: str, empty: bool = False) -> str:
    if not isinstance(value, str) or (not empty and not value):
        raise ContractError(f"{label} must be text")
    return value


def _bool(value: Any, label: str, expected: bool | None = None) -> bool:
    if expected is not None and value is not expected:
        raise ContractError(f"{label} must be {str(expected).lower()}")
    if not isinstance(value, bool):
        raise ContractError(f"{label} must be boolean")
    return value


def _pattern(value: Any, label: str, pattern: re.Pattern[str]) -> str:
    value = _str(value, label)
    if pattern.fullmatch(value) is None:
        raise ContractError(f"{label} has invalid format")
    return value


def _read(path: Path, label: str, ceiling: int) -> bytes:
    """Read one no-follow, unchanged regular-file generation."""
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as error:
        raise ContractError(f"cannot open {label}: {error}") from error
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= ceiling:
            raise ContractError(f"{label} is not a bounded regular file")
        with os.fdopen(fd, "rb", closefd=False) as handle:
            raw = handle.read(ceiling + 1)
        after = os.fstat(fd)
        def identity(value: os.stat_result) -> tuple[int, int, int, int]:
            return (
                value.st_dev,
                value.st_ino,
                value.st_size,
                value.st_mtime_ns,
            )
        if identity(before) != identity(after) or len(raw) != before.st_size:
            raise ContractError(f"{label} changed while being read")
        return raw
    finally:
        os.close(fd)


def _json_object(raw: bytes, label: str) -> dict[str, Any]:
    if not raw.endswith(b"\n"):
        raise ContractError(f"{label} must end with newline")
    try:
        return _obj(json.loads(raw.decode("utf-8", "strict")), label)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError(f"{label} is not strict UTF-8 JSON: {error}") from error


def _jsonl(raw: bytes) -> list[dict[str, Any]]:
    if not raw.endswith(b"\n"):
        raise ContractError("trajectory must end with newline")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise ContractError("trajectory is not valid UTF-8") from error
    rows = []
    for line_no, line in enumerate(text.splitlines(keepends=True), 1):
        if line == "\n" or not line.endswith("\n"):
            raise ContractError(f"trajectory line {line_no} is blank or unterminated")
        try:
            row = _obj(json.loads(line), f"trajectory line {line_no}")
        except json.JSONDecodeError as error:
            raise ContractError(f"trajectory line {line_no} invalid JSON") from error
        rows.append({**row, "_line": line_no})
        if len(rows) > 1 + 2 * MAX_ROUNDS:
            raise ContractError("trajectory exceeds row ceiling")
    return rows


def _header(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("event") != "run_header":
        raise ContractError("trajectory must begin with exactly one run_header")
    handoff = _obj(row.get("warm_start_handoff"), "warm_start_handoff")
    tick = _int(handoff.get("tick"), "warm_start_handoff.tick")
    if "contact_achieved" in handoff:
        _bool(handoff["contact_achieved"], "handoff.contact_achieved")
    fields = {
        "run_id": _str(row.get("run_id"), "run_header.run_id"),
        "curriculum_id": _str(row.get("curriculum_id"), "run_header.curriculum_id"),
        "generation_id": _pattern(row.get("generation_id"), "generation_id", GENERATION),
        "runtime_image_id": _pattern(row.get("runtime_image_id"), "runtime_image_id", IMAGE),
        "engine_commit": _pattern(row.get("engine_commit"), "engine_commit", SHA40),
        "war_college_commit": _pattern(row.get("war_college_commit"), "war_college_commit", SHA40),
        "joint_training_attestation_sha256": _pattern(
            row.get("joint_training_attestation_sha256"), "training attestation", SHA256,
        ),
        "warm_start_sha256": _pattern(row.get("warm_start_sha256"), "warm start SHA", SHA256),
        "warm_start_handoff": handoff,
        "warm_start_handoff_tick": tick,
        "apollyon_model": _str(row.get("apollyon_model"), "apollyon_model"),
        "abaddon_controller_sha256": _pattern(
            row.get("abaddon_controller_sha256"), "Abaddon controller SHA", SHA256,
        ),
        "abaddon_doctrine": _str(row.get("abaddon_doctrine"), "abaddon_doctrine"),
        "seed": _int(row.get("seed"), "seed"),
        "round_limit": _int(row.get("round_limit"), "round_limit", 1, MAX_ROUNDS),
        "ticks_per_round": _int(row.get("ticks_per_round"), "ticks_per_round", 1, 10_000),
    }
    for key in ("candidate_only", "review_required", "agent_training_rows_begin_here"):
        _bool(row.get(key), f"run_header.{key}", True)
    return fields


def _pairs(rows: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    pairs, pending, expected = [], None, 1
    for row in rows:
        event = _str(row.get("event"), f"line {row['_line']} event")
        number = _int(row.get("round"), "round", 1)
        if event == "joint_decision":
            if pending is not None:
                raise ContractError("joint_decision arrived before the previous joint_result")
            if number != expected:
                raise ContractError(f"expected decision round {expected}, got {number}")
            pending = row
        elif event == "joint_result":
            if pending is None:
                raise ContractError("joint_result arrived without joint_decision")
            if number != expected:
                raise ContractError(f"expected result round {expected}, got {number}")
            pairs.append((pending, row))
            pending, expected = None, expected + 1
        else:
            raise ContractError(f"unsupported trajectory event {event!r}")
    if pending is not None or not pairs:
        raise ContractError("trajectory has an incomplete or empty round sequence")
    return pairs


