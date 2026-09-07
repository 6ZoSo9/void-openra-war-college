#!/usr/bin/env python3
"""Durable attempt/session admission store for controller evidence.

Source-only authority primitive. This module does not authenticate producers and
does not execute the game. It provides durable, monotonic attempt/session state
and exactly-once joint-evidence consumption.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2
MAX_IDENTIFIER_BYTES = 128
MAX_UINT32 = (1 << 32) - 1

_IDENTIFIER_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]*\Z")
_LOWER_HEX_64_RE = re.compile(r"[0-9a-f]{64}\Z")
_LOWER_HEX_40_RE = re.compile(r"[0-9a-f]{40}\Z")


class AdmissionHold(RuntimeError):
    """Stable fail-closed admission terminal."""


@dataclass(frozen=True)
class AttemptIdentity:
    attempt_id: str
    producer_id: str
    controller_a_id: str
    controller_a_player_id: str
    controller_b_id: str
    controller_b_player_id: str
    source_generation: str
    war_college_commit: str
    engine_commit: str


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _bounded_identifier(value: Any) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        encoded = value.encode("ascii", "strict")
    except UnicodeError:
        return False
    return len(encoded) <= MAX_IDENTIFIER_BYTES and _IDENTIFIER_RE.fullmatch(value) is not None


def _canonical_sha256(value: Any) -> bool:
    return type(value) is str and _LOWER_HEX_64_RE.fullmatch(value) is not None


def _canonical_git_commit(value: Any) -> bool:
    return type(value) is str and _LOWER_HEX_40_RE.fullmatch(value) is not None


def _uint32(value: Any, *, positive: bool = False) -> bool:
    if type(value) is not int:
        return False
    minimum = 1 if positive else 0
    return minimum <= value <= MAX_UINT32


def _validate_identity(identity: AttemptIdentity) -> None:
    for field_name in (
        "attempt_id",
        "producer_id",
        "controller_a_id",
        "controller_a_player_id",
        "controller_b_id",
        "controller_b_player_id",
        "source_generation",
    ):
        if not _bounded_identifier(getattr(identity, field_name)):
            raise AdmissionHold(f"HOLD_{field_name.upper()}_INVALID")
    if identity.controller_a_id == identity.controller_b_id:
        raise AdmissionHold("HOLD_DUPLICATE_CONTROLLER_ID")
    if identity.controller_a_player_id == identity.controller_b_player_id:
        raise AdmissionHold("HOLD_DUPLICATE_CONTROLLER_PLAYER_ID")
    if not _canonical_git_commit(identity.war_college_commit):
        raise AdmissionHold("HOLD_WAR_COLLEGE_COMMIT_INVALID")
    if not _canonical_git_commit(identity.engine_commit):
        raise AdmissionHold("HOLD_ENGINE_COMMIT_INVALID")


def _connect(path: Path) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=5.0, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA busy_timeout=5000")
    connection.execute("PRAGMA synchronous=FULL")
    return connection


def _connect_existing(path: Path) -> sqlite3.Connection:
    path = Path(path)
    try:
        visible = path.lstat()
    except FileNotFoundError as error:
        raise AdmissionHold("HOLD_STORE_NOT_FOUND") from error
    except OSError as error:
        raise AdmissionHold(
            f"HOLD_STORE_PATH_STAT_FAILURE:{type(error).__name__}"
        ) from error
    if not stat.S_ISREG(visible.st_mode):
        raise AdmissionHold("HOLD_STORE_PATH_NOT_REGULAR")

    try:
        connection = sqlite3.connect(
            f"file:{path}?mode=rw",
            uri=True,
            timeout=5.0,
            isolation_level=None,
        )
    except sqlite3.Error as error:
        raise AdmissionHold("HOLD_STORE_OPEN_FAILURE") from error
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA busy_timeout=5000")
    connection.execute("PRAGMA synchronous=FULL")
    _require_store_schema(connection)
    return connection


def _require_store_schema(connection: sqlite3.Connection) -> None:
    try:
        row = connection.execute(
            "SELECT value FROM metadata WHERE key='schema_version'"
        ).fetchone()
    except sqlite3.Error as error:
        raise AdmissionHold("HOLD_STORE_SCHEMA_INVALID") from error
    if row is None or row["value"] != str(SCHEMA_VERSION):
        raise AdmissionHold("HOLD_STORE_SCHEMA_VERSION_MISMATCH")


def initialize_store(path: Path) -> None:
    connection = _connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS attempts (
                attempt_id TEXT PRIMARY KEY,
                producer_id TEXT NOT NULL,
                controller_a_id TEXT NOT NULL,
                controller_a_player_id TEXT NOT NULL,
                controller_b_id TEXT NOT NULL,
                controller_b_player_id TEXT NOT NULL,
                source_generation TEXT NOT NULL,
                war_college_commit TEXT NOT NULL,
                engine_commit TEXT NOT NULL,
                current_session_generation INTEGER NOT NULL
                    CHECK(current_session_generation >= 1)
            );

            CREATE TABLE IF NOT EXISTS sessions (
                attempt_id TEXT NOT NULL,
                session_generation INTEGER NOT NULL
                    CHECK(session_generation >= 1),
                predecessor_generation INTEGER,
                PRIMARY KEY(attempt_id, session_generation),
                FOREIGN KEY(attempt_id) REFERENCES attempts(attempt_id)
                    ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS consumptions (
                attempt_id TEXT NOT NULL,
                session_generation INTEGER NOT NULL,
                joint_evidence_sha256 TEXT NOT NULL UNIQUE,
                producer_id TEXT NOT NULL,
                controller_a_id TEXT NOT NULL,
                controller_a_player_id TEXT NOT NULL,
                controller_b_id TEXT NOT NULL,
                controller_b_player_id TEXT NOT NULL,
                consumption_sha256 TEXT NOT NULL UNIQUE,
                PRIMARY KEY(
                    attempt_id,
                    session_generation,
                    joint_evidence_sha256
                ),
                FOREIGN KEY(attempt_id, session_generation)
                    REFERENCES sessions(attempt_id, session_generation)
                    ON DELETE RESTRICT
            );
            """
        )
        row = connection.execute(
            "SELECT value FROM metadata WHERE key='schema_version'"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
        elif row["value"] != str(SCHEMA_VERSION):
            raise AdmissionHold("HOLD_STORE_SCHEMA_VERSION_MISMATCH")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _identity_from_row(row: sqlite3.Row) -> AttemptIdentity:
    return AttemptIdentity(
        attempt_id=row["attempt_id"],
        producer_id=row["producer_id"],
        controller_a_id=row["controller_a_id"],
        controller_a_player_id=row["controller_a_player_id"],
        controller_b_id=row["controller_b_id"],
        controller_b_player_id=row["controller_b_player_id"],
        source_generation=row["source_generation"],
        war_college_commit=row["war_college_commit"],
        engine_commit=row["engine_commit"],
    )


def _require_identity(row: sqlite3.Row, expected: AttemptIdentity) -> None:
    actual = _identity_from_row(row)
    if actual != expected:
        raise AdmissionHold("HOLD_ATTEMPT_IDENTITY_MISMATCH")


def _attempt_receipt(identity: AttemptIdentity, session_generation: int) -> dict[str, Any]:
    payload = {
        "attempt_id": identity.attempt_id,
        "controller_a_id": identity.controller_a_id,
        "controller_a_player_id": identity.controller_a_player_id,
        "controller_b_id": identity.controller_b_id,
        "controller_b_player_id": identity.controller_b_player_id,
        "engine_commit": identity.engine_commit,
        "producer_id": identity.producer_id,
        "schema_version": SCHEMA_VERSION,
        "session_generation": session_generation,
        "source_generation": identity.source_generation,
        "war_college_commit": identity.war_college_commit,
    }
    return {
        **payload,
        "attempt_admission_sha256": sha256_hex(payload),
        "contract": "GREEN",
    }


def create_attempt(path: Path, identity: AttemptIdentity) -> dict[str, Any]:
    _validate_identity(identity)
    initialize_store(path)
    connection = _connect(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        existing = connection.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (identity.attempt_id,),
        ).fetchone()
        if existing is not None:
            raise AdmissionHold("HOLD_ATTEMPT_ALREADY_EXISTS")

        connection.execute(
            """
            INSERT INTO attempts(
                attempt_id,
                producer_id,
                controller_a_id,
                controller_a_player_id,
                controller_b_id,
                controller_b_player_id,
                source_generation,
                war_college_commit,
                engine_commit,
                current_session_generation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (
                identity.attempt_id,
                identity.producer_id,
                identity.controller_a_id,
                identity.controller_a_player_id,
                identity.controller_b_id,
                identity.controller_b_player_id,
                identity.source_generation,
                identity.war_college_commit,
                identity.engine_commit,
            ),
        )
        connection.execute(
            """
            INSERT INTO sessions(
                attempt_id,
                session_generation,
                predecessor_generation
            ) VALUES (?, 1, NULL)
            """,
            (identity.attempt_id,),
        )
        connection.commit()
        return _attempt_receipt(identity, 1)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def inspect_attempt(path: Path, identity: AttemptIdentity) -> dict[str, Any]:
    _validate_identity(identity)
    connection = _connect_existing(path)
    try:
        row = connection.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (identity.attempt_id,),
        ).fetchone()
        if row is None:
            raise AdmissionHold("HOLD_ATTEMPT_NOT_FOUND")
        _require_identity(row, identity)
        return _attempt_receipt(identity, int(row["current_session_generation"]))
    finally:
        connection.close()


def load_attempt(path: Path, attempt_id: str) -> tuple[AttemptIdentity, int]:
    if not _bounded_identifier(attempt_id):
        raise AdmissionHold("HOLD_ATTEMPT_ID_INVALID")
    connection = _connect_existing(path)
    try:
        row = connection.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (attempt_id,),
        ).fetchone()
        if row is None:
            raise AdmissionHold("HOLD_ATTEMPT_NOT_FOUND")
        identity = _identity_from_row(row)
        generation = int(row["current_session_generation"])
        if not _uint32(generation, positive=True):
            raise AdmissionHold("HOLD_STORED_SESSION_GENERATION_INVALID")
        return identity, generation
    finally:
        connection.close()


def advance_session(
    path: Path,
    identity: AttemptIdentity,
    *,
    expected_current_generation: int,
) -> dict[str, Any]:
    _validate_identity(identity)
    if not _uint32(expected_current_generation, positive=True):
        raise AdmissionHold("HOLD_EXPECTED_SESSION_GENERATION_INVALID")
    if expected_current_generation >= MAX_UINT32:
        raise AdmissionHold("HOLD_SESSION_GENERATION_EXHAUSTED")

    connection = _connect_existing(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (identity.attempt_id,),
        ).fetchone()
        if row is None:
            raise AdmissionHold("HOLD_ATTEMPT_NOT_FOUND")
        _require_identity(row, identity)

        current = int(row["current_session_generation"])
        if current != expected_current_generation:
            raise AdmissionHold("HOLD_SESSION_PREDECESSOR_NOT_CURRENT")

        successor = current + 1
        updated = connection.execute(
            """
            UPDATE attempts
            SET current_session_generation=?
            WHERE attempt_id=? AND current_session_generation=?
            """,
            (successor, identity.attempt_id, current),
        )
        if updated.rowcount != 1:
            raise AdmissionHold("HOLD_COMPETING_SESSION_SUCCESSOR")

        connection.execute(
            """
            INSERT INTO sessions(
                attempt_id,
                session_generation,
                predecessor_generation
            ) VALUES (?, ?, ?)
            """,
            (identity.attempt_id, successor, current),
        )
        connection.commit()
        return _attempt_receipt(identity, successor)
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def consume_joint_evidence(
    path: Path,
    identity: AttemptIdentity,
    *,
    session_generation: int,
    joint_evidence_sha256: str,
) -> dict[str, Any]:
    _validate_identity(identity)
    if not _uint32(session_generation, positive=True):
        raise AdmissionHold("HOLD_SESSION_GENERATION_INVALID")
    if not _canonical_sha256(joint_evidence_sha256):
        raise AdmissionHold("HOLD_JOINT_EVIDENCE_DIGEST_INVALID")

    connection = _connect_existing(path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (identity.attempt_id,),
        ).fetchone()
        if row is None:
            raise AdmissionHold("HOLD_ATTEMPT_NOT_FOUND")
        _require_identity(row, identity)

        current = int(row["current_session_generation"])
        if session_generation != current:
            raise AdmissionHold("HOLD_SESSION_NOT_CURRENT")

        session = connection.execute(
            """
            SELECT 1 FROM sessions
            WHERE attempt_id=? AND session_generation=?
            """,
            (identity.attempt_id, session_generation),
        ).fetchone()
        if session is None:
            raise AdmissionHold("HOLD_SESSION_NOT_ADMITTED")

        prior = connection.execute(
            """
            SELECT attempt_id, session_generation
            FROM consumptions
            WHERE joint_evidence_sha256=?
            """,
            (joint_evidence_sha256,),
        ).fetchone()
        if prior is not None:
            if (
                prior["attempt_id"] == identity.attempt_id
                and int(prior["session_generation"]) == session_generation
            ):
                raise AdmissionHold("HOLD_EVIDENCE_ALREADY_CONSUMED")
            raise AdmissionHold("HOLD_JOINT_DIGEST_ALREADY_CONSUMED")

        receipt_payload = {
            "attempt_id": identity.attempt_id,
            "controller_a_id": identity.controller_a_id,
            "controller_a_player_id": identity.controller_a_player_id,
            "controller_b_id": identity.controller_b_id,
            "controller_b_player_id": identity.controller_b_player_id,
            "joint_evidence_sha256": joint_evidence_sha256,
            "producer_id": identity.producer_id,
            "schema_version": SCHEMA_VERSION,
            "session_generation": session_generation,
        }
        consumption_sha256 = sha256_hex(receipt_payload)

        connection.execute(
            """
            INSERT INTO consumptions(
                attempt_id,
                session_generation,
                joint_evidence_sha256,
                producer_id,
                controller_a_id,
                controller_a_player_id,
                controller_b_id,
                controller_b_player_id,
                consumption_sha256
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                identity.attempt_id,
                session_generation,
                joint_evidence_sha256,
                identity.producer_id,
                identity.controller_a_id,
                identity.controller_a_player_id,
                identity.controller_b_id,
                identity.controller_b_player_id,
                consumption_sha256,
            ),
        )
        connection.commit()
        return {
            **receipt_payload,
            "consumption_sha256": consumption_sha256,
            "contract": "GREEN",
        }
    except sqlite3.IntegrityError as error:
        connection.rollback()
        raise AdmissionHold("HOLD_STORE_INTEGRITY_CONFLICT") from error
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
