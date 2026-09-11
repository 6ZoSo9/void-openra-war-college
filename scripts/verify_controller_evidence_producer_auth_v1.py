#!/usr/bin/env python3
"""Cryptographically bind War College evidence to an existing VOID node identity."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from scripts.controller_attempt_admission_store_v1 import AttemptIdentity

MARKER = "VOID_WAR_COLLEGE_PRODUCER_AUTH_V1"
SCHEMA_VERSION = 1
AUTH_DOMAIN = "VOID_WAR_COLLEGE_PRODUCER_EVIDENCE_AUTH_V1"
TRANSCRIPT_ENCODING = "utf8_json_array_v1"

MAX_AUTH_BYTES = 16 * 1024
MAX_JSON_DEPTH = 8
MAX_PUBLIC_PEM_BYTES = 2048
MAX_UINT32 = (1 << 32) - 1

NODE_ID_RE = re.compile(r"[0-9a-f]{32}\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
SIGNATURE_RE = re.compile(r"[0-9a-f]{128}\Z")

AUTH_KEYS = {
    "marker",
    "schema_version",
    "producer_node_id",
    "producer_public_key_pem",
    "producer_public_key_sha256",
    "attempt_id",
    "session_generation",
    "joint_evidence_sha256",
    "transcript_sha256",
    "signature_hex",
}


class ProducerAuthAdmissionError(ValueError):
    """Typed fail-closed producer-auth input terminal."""


def _uint32(value: Any, *, positive: bool = False) -> bool:
    if type(value) is not int:
        return False
    minimum = 1 if positive else 0
    return minimum <= value <= MAX_UINT32


def canonical_ed25519_public_pem(raw: Any) -> tuple[str, Ed25519PublicKey] | None:
    if type(raw) is not str or not raw:
        return None
    try:
        encoded = raw.encode("ascii", "strict")
    except UnicodeError:
        return None
    if len(encoded) > MAX_PUBLIC_PEM_BYTES:
        return None

    try:
        key = serialization.load_pem_public_key(encoded)
    except (TypeError, ValueError):
        return None
    if not isinstance(key, Ed25519PublicKey):
        return None

    canonical = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")
    if canonical != raw:
        return None
    return canonical, key


def derive_void_node_identity_from_public_pem(
    raw: Any,
) -> tuple[str, str, Ed25519PublicKey] | None:
    normalized = canonical_ed25519_public_pem(raw)
    if normalized is None:
        return None
    canonical, key = normalized
    digest = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    return digest[:32], digest, key


def _controller_player_bindings(identity: AttemptIdentity) -> list[list[str]]:
    return sorted(
        [
            [identity.controller_a_id, identity.controller_a_player_id],
            [identity.controller_b_id, identity.controller_b_player_id],
        ],
        key=lambda item: (item[0], item[1]),
    )


def producer_auth_transcript_bytes(
    identity: AttemptIdentity,
    *,
    session_generation: int,
    joint_evidence_sha256: str,
    evidence_generation: str,
    war_college_frozen_commit: str,
    engine_frozen_commit: str,
) -> bytes:
    if not _uint32(session_generation, positive=True):
        raise ValueError("session generation is invalid")
    if SHA256_RE.fullmatch(joint_evidence_sha256) is None:
        raise ValueError("joint evidence digest is invalid")

    payload = [
        AUTH_DOMAIN,
        TRANSCRIPT_ENCODING,
        SCHEMA_VERSION,
        identity.producer_id,
        identity.producer_public_key_sha256,
        identity.attempt_id,
        session_generation,
        joint_evidence_sha256,
        identity.source_generation,
        identity.war_college_commit,
        identity.engine_commit,
        evidence_generation,
        war_college_frozen_commit,
        engine_frozen_commit,
        _controller_player_bindings(identity),
    ]
    return json.dumps(
        payload,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("ascii")


def verify_producer_auth(
    raw: Any,
    *,
    identity: AttemptIdentity,
    session_generation: int,
    joint_evidence_sha256: str,
    evidence_generation: str,
    war_college_frozen_commit: str,
    engine_frozen_commit: str,
) -> dict[str, Any]:
    holds: list[str] = []

    if type(raw) is not dict:
        return {
            "contract": "HOLD",
            "holds": ["HOLD_PRODUCER_AUTH_NOT_OBJECT"],
            "producer_node_id": None,
            "transcript_sha256": None,
        }
    if set(raw) != AUTH_KEYS:
        holds.append("HOLD_PRODUCER_AUTH_SCHEMA_DRIFT")

    producer_node_id = raw.get("producer_node_id")
    producer_public_key_pem = raw.get("producer_public_key_pem")
    producer_public_key_sha256 = raw.get("producer_public_key_sha256")
    attempt_id = raw.get("attempt_id")
    envelope_session = raw.get("session_generation")
    envelope_joint = raw.get("joint_evidence_sha256")
    transcript_sha256 = raw.get("transcript_sha256")
    signature_hex = raw.get("signature_hex")

    if raw.get("marker") != MARKER:
        holds.append("HOLD_PRODUCER_AUTH_MARKER_MISMATCH")
    if raw.get("schema_version") != SCHEMA_VERSION:
        holds.append("HOLD_PRODUCER_AUTH_SCHEMA_VERSION_MISMATCH")

    if type(producer_node_id) is not str or NODE_ID_RE.fullmatch(producer_node_id) is None:
        holds.append("HOLD_PRODUCER_NODE_ID_INVALID")
    if (
        type(producer_public_key_sha256) is not str
        or SHA256_RE.fullmatch(producer_public_key_sha256) is None
    ):
        holds.append("HOLD_PRODUCER_PUBLIC_KEY_SHA256_INVALID")
    if type(attempt_id) is not str or attempt_id != identity.attempt_id:
        holds.append("HOLD_PRODUCER_AUTH_ATTEMPT_MISMATCH")
    if envelope_session != session_generation:
        holds.append("HOLD_PRODUCER_AUTH_SESSION_MISMATCH")
    if envelope_joint != joint_evidence_sha256:
        holds.append("HOLD_PRODUCER_AUTH_JOINT_DIGEST_MISMATCH")
    if type(transcript_sha256) is not str or SHA256_RE.fullmatch(transcript_sha256) is None:
        holds.append("HOLD_PRODUCER_AUTH_TRANSCRIPT_SHA256_INVALID")
    if type(signature_hex) is not str or SIGNATURE_RE.fullmatch(signature_hex) is None:
        holds.append("HOLD_PRODUCER_AUTH_SIGNATURE_INVALID")

    derived = derive_void_node_identity_from_public_pem(producer_public_key_pem)
    public_key: Ed25519PublicKey | None = None
    if derived is None:
        holds.append("HOLD_PRODUCER_PUBLIC_KEY_NOT_CANONICAL_ED25519")
    else:
        derived_node_id, derived_public_key_sha256, public_key = derived
        if producer_node_id != derived_node_id:
            holds.append("HOLD_PRODUCER_NODE_ID_PUBLIC_KEY_MISMATCH")
        if producer_public_key_sha256 != derived_public_key_sha256:
            holds.append("HOLD_PRODUCER_PUBLIC_KEY_SHA256_MISMATCH")

    if identity.producer_id != producer_node_id:
        holds.append("HOLD_PRODUCER_NODE_ID_NOT_DURABLY_PINNED")
    if identity.producer_public_key_sha256 != producer_public_key_sha256:
        holds.append("HOLD_PRODUCER_PUBLIC_KEY_NOT_DURABLY_PINNED")

    if holds:
        return {
            "contract": "HOLD",
            "holds": sorted(set(holds)),
            "producer_node_id": producer_node_id if isinstance(producer_node_id, str) else None,
            "transcript_sha256": transcript_sha256 if isinstance(transcript_sha256, str) else None,
        }

    transcript = producer_auth_transcript_bytes(
        identity,
        session_generation=session_generation,
        joint_evidence_sha256=joint_evidence_sha256,
        evidence_generation=evidence_generation,
        war_college_frozen_commit=war_college_frozen_commit,
        engine_frozen_commit=engine_frozen_commit,
    )
    expected_transcript_sha256 = hashlib.sha256(transcript).hexdigest()
    if transcript_sha256 != expected_transcript_sha256:
        return {
            "contract": "HOLD",
            "holds": ["HOLD_PRODUCER_AUTH_TRANSCRIPT_MISMATCH"],
            "producer_node_id": producer_node_id,
            "transcript_sha256": transcript_sha256,
        }

    assert public_key is not None
    try:
        public_key.verify(bytes.fromhex(signature_hex), transcript)
    except (InvalidSignature, ValueError):
        return {
            "contract": "HOLD",
            "holds": ["HOLD_PRODUCER_AUTH_SIGNATURE_VERIFICATION_FAILED"],
            "producer_node_id": producer_node_id,
            "transcript_sha256": transcript_sha256,
        }

    return {
        "contract": "GREEN",
        "holds": [],
        "producer_node_id": producer_node_id,
        "producer_public_key_sha256": producer_public_key_sha256,
        "transcript_sha256": transcript_sha256,
    }


def _json_depth_preflight(raw: bytes) -> None:
    depth = 0
    in_string = False
    escaped = False
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 0x5C:
                escaped = True
            elif byte == 0x22:
                in_string = False
            continue
        if byte == 0x22:
            in_string = True
        elif byte in (0x7B, 0x5B):
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_JSON_DEPTH_EXCEEDED")
        elif byte in (0x7D, 0x5D):
            depth = max(0, depth - 1)


def read_producer_auth_file(path: Path) -> Any:
    try:
        visible = path.lstat()
    except OSError as error:
        raise ProducerAuthAdmissionError(
            f"HOLD_PRODUCER_AUTH_PATH_STAT_FAILURE:{type(error).__name__}"
        ) from error

    if not stat.S_ISREG(visible.st_mode):
        raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_PATH_NOT_REGULAR")
    if visible.st_size > MAX_AUTH_BYTES:
        raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_FILE_TOO_LARGE")

    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)

    try:
        fd = os.open(path, flags)
    except OSError as error:
        raise ProducerAuthAdmissionError(
            f"HOLD_PRODUCER_AUTH_OPEN_FAILURE:{type(error).__name__}"
        ) from error

    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode):
            raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_PATH_NOT_REGULAR")
        if (before.st_dev, before.st_ino) != (visible.st_dev, visible.st_ino):
            raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_PATH_GENERATION_CHANGED")
        if before.st_size > MAX_AUTH_BYTES:
            raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_FILE_TOO_LARGE")

        chunks: list[bytes] = []
        remaining = MAX_AUTH_BYTES + 1
        while remaining:
            chunk = os.read(fd, min(16_384, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)

        after = os.fstat(fd)
        identity = lambda value: (
            value.st_dev,
            value.st_ino,
            value.st_size,
            value.st_mtime_ns,
        )
        if identity(before) != identity(after) or len(raw) != before.st_size:
            raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_FILE_CHANGED_DURING_READ")
        if len(raw) > MAX_AUTH_BYTES:
            raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_FILE_TOO_LARGE")
    finally:
        os.close(fd)

    _json_depth_preflight(raw)
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeError as error:
        raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_UTF8_INVALID") from error

    try:
        return json.loads(text)
    except (json.JSONDecodeError, RecursionError) as error:
        raise ProducerAuthAdmissionError("HOLD_PRODUCER_AUTH_JSON_INVALID") from error
