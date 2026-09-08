#!/usr/bin/env python3
"""Prepare/finalize a non-custodial War College request signing handoff.

This tool never reads a producer private key, never consumes evidence, never
writes the live verifier request root, and never starts a service.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib
import json
import os
import re
import sqlite3
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config/war-college/designated-host-request-signing-handoff-v1.json"

MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_REQUEST_SIGNING_HANDOFF_TOOL_V1"
HANDOFF_MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_UNSIGNED_SIGNING_HANDOFF_V1"
FINAL_MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_STAGING_BUNDLE_V1"

EXPECTED_UID = 1000
EXPECTED_GID = 1000
REQUEST_FILE = "request.json"
EVIDENCE_FILE = "evidence.json"
AUTH_FILE = "producer-auth.json"
PUBLIC_PEM_FILE = "producer-public.pem"
AUTH_FIELDS_FILE = "producer-auth-fields.json"
TRANSCRIPT_FILE = "transcript.bin"
HANDOFF_FILE = "handoff.json"
SIGNATURE_FILE = "signature.hex"
BUNDLE_DIR = "bundle"

LOWER_HEX_64 = re.compile(r"[0-9a-f]{64}\Z")
LOWER_HEX_128 = re.compile(r"[0-9a-f]{128}\Z")
REQUEST_ID_RE = re.compile(r"wcrq1_[0-9a-f]{32}\Z")
GIT = "/usr/bin/git"


class HandoffHold(RuntimeError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _read_regular(path: Path, *, max_bytes: int) -> bytes:
    try:
        visible = path.lstat()
    except OSError as error:
        raise HandoffHold(f"HOLD_INPUT_STAT:{type(error).__name__}") from error
    if stat.S_ISLNK(visible.st_mode) or not stat.S_ISREG(visible.st_mode):
        raise HandoffHold("HOLD_INPUT_NOT_REGULAR")
    if visible.st_size > max_bytes:
        raise HandoffHold("HOLD_INPUT_TOO_LARGE")

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(fd, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        after = os.fstat(fd)
        identity = lambda st: (
            st.st_dev,
            st.st_ino,
            st.st_size,
            st.st_mtime_ns,
            stat.S_IMODE(st.st_mode),
        )
        if identity(before) != identity(after) or len(raw) != before.st_size:
            raise HandoffHold("HOLD_INPUT_CHANGED_DURING_READ")
        if len(raw) > max_bytes:
            raise HandoffHold("HOLD_INPUT_TOO_LARGE")
        return raw
    finally:
        os.close(fd)


def _json_no_duplicates(raw: bytes, hold: str) -> Any:
    def hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise HandoffHold(hold)
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=hook)
    except HandoffHold:
        raise
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise HandoffHold(hold) from error


def load_contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if value.get("marker") != "VOID_WAR_COLLEGE_DESIGNATED_HOST_REQUEST_SIGNING_HANDOFF_V1":
        raise HandoffHold("HOLD_HANDOFF_CONTRACT_MARKER")
    if value.get("version") != 1:
        raise HandoffHold("HOLD_HANDOFF_CONTRACT_VERSION")
    expected_authority = {
        "private_key_access": False,
        "store_mutation_authorized": False,
        "live_bundle_materialization_authorized": False,
        "service_start_authorized": False,
        "runtime_execution_authorized": False,
    }
    if value.get("authority") != expected_authority:
        raise HandoffHold("HOLD_HANDOFF_AUTHORITY_DRIFT")
    return value


def _git(repo: Path, *args: str) -> str:
    cp = subprocess.run(
        [GIT, "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={"HOME": str(Path.home()), "LANG": "C", "LC_ALL": "C", "PATH": "/usr/bin:/bin"},
    )
    if cp.returncode != 0:
        raise HandoffHold("HOLD_RUNTIME_GIT_QUERY")
    return cp.stdout.strip()


def verify_runtime(contract: dict[str, Any]) -> Path:
    repo = Path(contract["runtime_repository"])
    try:
        resolved = repo.resolve(strict=True)
    except OSError as error:
        raise HandoffHold("HOLD_RUNTIME_REPOSITORY_NOT_FOUND") from error
    if resolved != repo:
        raise HandoffHold("HOLD_RUNTIME_REPOSITORY_SYMLINKED")
    if _git(repo, "rev-parse", "HEAD") != contract["runtime_source_commit"]:
        raise HandoffHold("HOLD_RUNTIME_SOURCE_COMMIT")
    if _git(repo, "status", "--porcelain", "--untracked-files=all"):
        raise HandoffHold("HOLD_RUNTIME_WORKTREE_DIRTY")
    for rel, expected in sorted(contract["runtime_artifact_git_blobs"].items()):
        if _git(repo, "rev-parse", f"HEAD:{rel}") != expected:
            raise HandoffHold("HOLD_RUNTIME_ARTIFACT_BLOB")
    return repo


def load_runtime_modules(repo: Path):
    original = list(sys.path)
    try:
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        structural = importlib.import_module("scripts.verify_controller_evidence_isolation_v1")
        producer_auth = importlib.import_module("scripts.verify_controller_evidence_producer_auth_v1")
        designated_root = importlib.import_module("scripts.war_college_designated_producer_trust_root_v1")
        store = importlib.import_module("scripts.controller_attempt_admission_store_v1")
        wrapper = importlib.import_module("scripts.war_college_designated_host_verify_request_v1")
        return structural, producer_auth, designated_root, store, wrapper
    finally:
        sys.path[:] = original


def read_attempt_read_only(
    store_path: Path,
    attempt_id: str,
    *,
    store_module,
) -> tuple[Any, int]:
    try:
        visible = store_path.lstat()
    except OSError as error:
        raise HandoffHold("HOLD_STORE_NOT_FOUND") from error
    if stat.S_ISLNK(visible.st_mode) or not stat.S_ISREG(visible.st_mode):
        raise HandoffHold("HOLD_STORE_NOT_REGULAR")

    try:
        connection = sqlite3.connect(
            f"file:{store_path}?mode=ro",
            uri=True,
            timeout=5.0,
            isolation_level=None,
        )
    except sqlite3.Error as error:
        raise HandoffHold("HOLD_STORE_OPEN_READ_ONLY") from error
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA query_only=ON")
        meta = connection.execute(
            "SELECT value FROM metadata WHERE key='schema_version'"
        ).fetchone()
        if meta is None or meta["value"] != "3":
            raise HandoffHold("HOLD_STORE_SCHEMA_VERSION")
        row = connection.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (attempt_id,),
        ).fetchone()
        if row is None:
            raise HandoffHold("HOLD_ATTEMPT_NOT_FOUND")
        identity = store_module.AttemptIdentity(
            attempt_id=row["attempt_id"],
            producer_id=row["producer_id"],
            producer_public_key_sha256=row["producer_public_key_sha256"],
            controller_a_id=row["controller_a_id"],
            controller_a_player_id=row["controller_a_player_id"],
            controller_b_id=row["controller_b_id"],
            controller_b_player_id=row["controller_b_player_id"],
            source_generation=row["source_generation"],
            war_college_commit=row["war_college_commit"],
            engine_commit=row["engine_commit"],
        )
        generation = int(row["current_session_generation"])
        return identity, generation
    finally:
        connection.close()


def _controller_bindings(evidence: dict[str, Any]) -> set[tuple[str, str]]:
    controllers = evidence.get("controllers")
    if type(controllers) is not list:
        raise HandoffHold("HOLD_EVIDENCE_CONTROLLERS")
    result: set[tuple[str, str]] = set()
    for record in controllers:
        if type(record) is not dict:
            raise HandoffHold("HOLD_EVIDENCE_CONTROLLER_RECORD")
        controller_id = record.get("controller_id")
        player_id = record.get("player_id")
        if type(controller_id) is not str or type(player_id) is not str:
            raise HandoffHold("HOLD_EVIDENCE_CONTROLLER_BINDING")
        result.add((controller_id, player_id))
    return result


def _request_id(
    domain: str,
    evidence_sha256: str,
    transcript_sha256: str,
) -> str:
    material = (
        domain.encode("ascii")
        + b"\0"
        + evidence_sha256.encode("ascii")
        + b"\0"
        + transcript_sha256.encode("ascii")
    )
    return "wcrq1_" + hashlib.sha256(material).hexdigest()[:32]


def _validate_public_identity(
    *,
    public_pem: str,
    identity,
    producer_auth,
    designated_root,
    root_override=None,
) -> None:
    derived = producer_auth.derive_void_node_identity_from_public_pem(public_pem)
    if derived is None:
        raise HandoffHold("HOLD_PUBLIC_KEY_NOT_CANONICAL_ED25519")
    node_id, pem_sha256, _key = derived
    if node_id != identity.producer_id:
        raise HandoffHold("HOLD_PUBLIC_KEY_NODE_ID_NOT_PINNED")
    if pem_sha256 != identity.producer_public_key_sha256:
        raise HandoffHold("HOLD_PUBLIC_KEY_SHA256_NOT_PINNED")

    auth_stub = {"producer_public_key_pem": public_pem}
    kwargs = {"identity": identity, "producer_auth_record": auth_stub}
    if root_override is not None:
        kwargs["root"] = root_override
    report = designated_root.verify_designated_producer_trust_v1(**kwargs)
    if report.get("contract") != "GREEN":
        raise HandoffHold(
            "HOLD_DESIGNATED_TRUST_ROOT:" + ",".join(report.get("holds", []))
        )


def derive_state(
    *,
    evidence_raw: bytes,
    public_pem_raw: bytes,
    store_path: Path,
    contract: dict[str, Any],
    modules,
    root_override=None,
) -> dict[str, Any]:
    structural, producer_auth, designated_root, store, _wrapper = modules
    evidence = _json_no_duplicates(evidence_raw, "HOLD_EVIDENCE_JSON_INVALID")
    if type(evidence) is not dict:
        raise HandoffHold("HOLD_EVIDENCE_NOT_OBJECT")
    attempt_id = evidence.get("attempt_id")
    if type(attempt_id) is not str or not attempt_id:
        raise HandoffHold("HOLD_ATTEMPT_ID_INVALID")

    identity, session_generation = read_attempt_read_only(
        store_path, attempt_id, store_module=store
    )

    if identity.source_generation != structural.GENERATION:
        raise HandoffHold("HOLD_STORE_SOURCE_GENERATION")
    if identity.war_college_commit != "f57c561f3a4c742e34d820933be40dd7d4253951":
        raise HandoffHold("HOLD_STORE_WAR_COLLEGE_SOURCE_BASE")
    if identity.engine_commit != structural.ENGINE_FROZEN_COMMIT:
        raise HandoffHold("HOLD_STORE_ENGINE_COMMIT")

    report = structural.verify_evidence(
        evidence,
        expected_attempt_id=identity.attempt_id,
        expected_controller_session_generation=session_generation,
    )
    if report.get("contract") != "GREEN":
        raise HandoffHold(
            "HOLD_STRUCTURAL_EVIDENCE:" + ",".join(report.get("holds", []))
        )
    expected_bindings = {
        (identity.controller_a_id, identity.controller_a_player_id),
        (identity.controller_b_id, identity.controller_b_player_id),
    }
    if _controller_bindings(evidence) != expected_bindings:
        raise HandoffHold("HOLD_DURABLE_CONTROLLER_PLAYER_MAPPING")

    joint_digest = report.get("admitted_joint_evidence_sha256")
    if type(joint_digest) is not str or LOWER_HEX_64.fullmatch(joint_digest) is None:
        raise HandoffHold("HOLD_JOINT_EVIDENCE_DIGEST")

    try:
        public_pem = public_pem_raw.decode("ascii", "strict")
    except UnicodeError as error:
        raise HandoffHold("HOLD_PUBLIC_KEY_ASCII") from error
    _validate_public_identity(
        public_pem=public_pem,
        identity=identity,
        producer_auth=producer_auth,
        designated_root=designated_root,
        root_override=root_override,
    )

    transcript = producer_auth.producer_auth_transcript_bytes(
        identity,
        session_generation=session_generation,
        joint_evidence_sha256=joint_digest,
        evidence_generation=structural.GENERATION,
        war_college_frozen_commit=structural.WAR_COLLEGE_FROZEN_COMMIT,
        engine_frozen_commit=structural.ENGINE_FROZEN_COMMIT,
    )
    transcript_sha = _sha256(transcript)
    evidence_sha = _sha256(evidence_raw)
    request_id = _request_id(
        contract["request_id_derivation_domain"],
        evidence_sha,
        transcript_sha,
    )
    if REQUEST_ID_RE.fullmatch(request_id) is None:
        raise HandoffHold("HOLD_DERIVED_REQUEST_ID")

    auth_fields = {
        "attempt_id": identity.attempt_id,
        "joint_evidence_sha256": joint_digest,
        "marker": producer_auth.MARKER,
        "producer_node_id": identity.producer_id,
        "producer_public_key_pem": public_pem,
        "producer_public_key_sha256": identity.producer_public_key_sha256,
        "schema_version": producer_auth.SCHEMA_VERSION,
        "session_generation": session_generation,
        "transcript_sha256": transcript_sha,
    }
    return {
        "attempt_id": identity.attempt_id,
        "auth_fields": auth_fields,
        "evidence": evidence,
        "evidence_sha256": evidence_sha,
        "identity": identity,
        "joint_evidence_sha256": joint_digest,
        "public_pem": public_pem,
        "request_id": request_id,
        "session_generation": session_generation,
        "structural_report": report,
        "transcript": transcript,
        "transcript_sha256": transcript_sha,
    }


def _create_private_dir(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise HandoffHold("HOLD_OUTPUT_ALREADY_EXISTS")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir(mode=0o700)
    os.chmod(path, 0o700)


def _write_create_only(path: Path, raw: bytes, mode: int) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_CLOEXEC", 0)
    fd = os.open(path, flags, mode)
    try:
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(path, mode)


def prepare_handoff(
    *,
    evidence_path: Path,
    public_pem_path: Path,
    output_dir: Path,
    contract: dict[str, Any],
    modules,
    store_path: Path | None = None,
    root_override=None,
) -> dict[str, Any]:
    evidence_raw = _read_regular(evidence_path, max_bytes=128 * 1024)
    public_raw = _read_regular(public_pem_path, max_bytes=2048)
    store_path = store_path or Path(contract["store_path"])
    state = derive_state(
        evidence_raw=evidence_raw,
        public_pem_raw=public_raw,
        store_path=store_path,
        contract=contract,
        modules=modules,
        root_override=root_override,
    )

    _create_private_dir(output_dir)
    _write_create_only(output_dir / EVIDENCE_FILE, evidence_raw, 0o400)
    _write_create_only(
        output_dir / PUBLIC_PEM_FILE,
        state["public_pem"].encode("ascii"),
        0o400,
    )
    _write_create_only(
        output_dir / AUTH_FIELDS_FILE,
        canonical_json_bytes(state["auth_fields"]),
        0o400,
    )
    _write_create_only(output_dir / TRANSCRIPT_FILE, state["transcript"], 0o400)

    manifest = {
        "attempt_id": state["attempt_id"],
        "evidence_sha256": state["evidence_sha256"],
        "joint_evidence_sha256": state["joint_evidence_sha256"],
        "marker": HANDOFF_MARKER,
        "private_key_access": False,
        "request_id": state["request_id"],
        "session_generation": state["session_generation"],
        "signature_required": True,
        "store_mutation_performed": False,
        "transcript_sha256": state["transcript_sha256"],
        "version": 1,
    }
    _write_create_only(output_dir / HANDOFF_FILE, canonical_json_bytes(manifest), 0o400)
    return manifest


def _load_handoff_files(handoff_dir: Path) -> tuple[bytes, bytes, dict[str, Any]]:
    if handoff_dir.resolve(strict=True) != handoff_dir:
        raise HandoffHold("HOLD_HANDOFF_DIRECTORY_SYMLINKED")
    evidence_raw = _read_regular(handoff_dir / EVIDENCE_FILE, max_bytes=128 * 1024)
    public_raw = _read_regular(handoff_dir / PUBLIC_PEM_FILE, max_bytes=2048)
    handoff_raw = _read_regular(handoff_dir / HANDOFF_FILE, max_bytes=16 * 1024)
    handoff = _json_no_duplicates(handoff_raw, "HOLD_HANDOFF_JSON")
    if type(handoff) is not dict or handoff.get("marker") != HANDOFF_MARKER:
        raise HandoffHold("HOLD_HANDOFF_MANIFEST")
    return evidence_raw, public_raw, handoff


def finalize_handoff(
    *,
    handoff_dir: Path,
    signature_hex: str,
    contract: dict[str, Any],
    modules,
    store_path: Path | None = None,
    root_override=None,
) -> dict[str, Any]:
    structural, producer_auth, designated_root, _store, wrapper = modules
    signature_hex = signature_hex.strip()
    if LOWER_HEX_128.fullmatch(signature_hex) is None:
        raise HandoffHold("HOLD_SIGNATURE_HEX_INVALID")

    evidence_raw, public_raw, manifest = _load_handoff_files(handoff_dir)
    store_path = store_path or Path(contract["store_path"])
    state = derive_state(
        evidence_raw=evidence_raw,
        public_pem_raw=public_raw,
        store_path=store_path,
        contract=contract,
        modules=modules,
        root_override=root_override,
    )

    for key in (
        "attempt_id",
        "evidence_sha256",
        "joint_evidence_sha256",
        "request_id",
        "session_generation",
        "transcript_sha256",
    ):
        if manifest.get(key) != state[key]:
            raise HandoffHold("HOLD_HANDOFF_STATE_DRIFT")

    auth_record = dict(state["auth_fields"])
    auth_record["signature_hex"] = signature_hex

    auth_report = producer_auth.verify_producer_auth(
        auth_record,
        identity=state["identity"],
        session_generation=state["session_generation"],
        joint_evidence_sha256=state["joint_evidence_sha256"],
        evidence_generation=structural.GENERATION,
        war_college_frozen_commit=structural.WAR_COLLEGE_FROZEN_COMMIT,
        engine_frozen_commit=structural.ENGINE_FROZEN_COMMIT,
    )
    if auth_report.get("contract") != "GREEN":
        raise HandoffHold(
            "HOLD_SIGNATURE_VERIFICATION:" + ",".join(auth_report.get("holds", []))
        )

    root_kwargs = {
        "identity": state["identity"],
        "producer_auth_record": auth_record,
    }
    if root_override is not None:
        root_kwargs["root"] = root_override
    root_report = designated_root.verify_designated_producer_trust_v1(**root_kwargs)
    if root_report.get("contract") != "GREEN":
        raise HandoffHold(
            "HOLD_DESIGNATED_TRUST_ROOT:" + ",".join(root_report.get("holds", []))
        )

    auth_raw = canonical_json_bytes(auth_record)
    request = {
        "evidence_sha256": state["evidence_sha256"],
        "marker": wrapper.REQUEST_MARKER,
        "producer_auth_sha256": _sha256(auth_raw),
        "request_id": state["request_id"],
        "schema_version": wrapper.REQUEST_SCHEMA_VERSION,
    }
    request_raw = canonical_json_bytes(request)
    wrapper._validate_request(
        state["request_id"],
        request_raw,
        evidence_raw,
        auth_raw,
    )

    bundle_dir = handoff_dir / BUNDLE_DIR
    _create_private_dir(bundle_dir)
    _write_create_only(bundle_dir / REQUEST_FILE, request_raw, 0o400)
    _write_create_only(bundle_dir / EVIDENCE_FILE, evidence_raw, 0o400)
    _write_create_only(bundle_dir / AUTH_FILE, auth_raw, 0o400)

    return {
        "bundle_dir": str(bundle_dir),
        "live_bundle_materialization_authorized": False,
        "marker": FINAL_MARKER,
        "private_key_access": False,
        "request_id": state["request_id"],
        "service_start_authorized": False,
        "signature_verified": True,
        "store_mutation_performed": False,
        "version": 1,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--evidence", type=Path, required=True)
    prepare.add_argument("--producer-public-pem", type=Path, required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)

    finalize = sub.add_parser("finalize")
    finalize.add_argument("--handoff-dir", type=Path, required=True)
    finalize.add_argument("--signature-hex-file", type=Path, required=True)

    args = parser.parse_args(argv)
    try:
        if os.getuid() != EXPECTED_UID or os.getgid() != EXPECTED_GID:
            raise HandoffHold("HOLD_OPERATOR_UID_GID")
        contract = load_contract()
        repo = verify_runtime(contract)
        modules = load_runtime_modules(repo)
        if args.command == "prepare":
            report = prepare_handoff(
                evidence_path=args.evidence,
                public_pem_path=args.producer_public_pem,
                output_dir=args.output_dir,
                contract=contract,
                modules=modules,
            )
        else:
            signature_raw = _read_regular(args.signature_hex_file, max_bytes=256)
            try:
                signature_hex = signature_raw.decode("ascii", "strict").strip()
            except UnicodeError as error:
                raise HandoffHold("HOLD_SIGNATURE_ASCII") from error
            report = finalize_handoff(
                handoff_dir=args.handoff_dir,
                signature_hex=signature_hex,
                contract=contract,
                modules=modules,
            )
    except (HandoffHold, OSError, sqlite3.Error, ValueError, RecursionError) as error:
        print(
            json.dumps(
                {
                    "contract": "HOLD",
                    "hold": str(error),
                    "live_bundle_materialization_authorized": False,
                    "marker": MARKER,
                    "private_key_access": False,
                    "runtime_execution_authorized": False,
                    "service_start_authorized": False,
                    "store_mutation_performed": False,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 1

    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
