#!/usr/bin/env python3
"""Plan or explicitly apply the first canonical V3 War College attempt admission.

The default plan path is non-mutating. The apply path may create only the
canonical war_college directory and canonical V3 attempt store. It never reads
a private key, signs, consumes evidence, advances a session, starts/reloads a
service, materializes a verifier request, or executes the game/runtime.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import socket
import sqlite3
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config/war-college/designated-host-attempt-admission-v1.json"
MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_ATTEMPT_ADMISSION_TOOL_V1"
EXPECTED_UID = 1000
EXPECTED_GID = 1000
GIT = "/usr/bin/git"


class AdmissionToolHold(RuntimeError):
    pass


def load_contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if value.get("marker") != "VOID_WAR_COLLEGE_DESIGNATED_HOST_ATTEMPT_ADMISSION_V1":
        raise AdmissionToolHold("HOLD_ADMISSION_CONTRACT_MARKER")
    if value.get("version") != 1:
        raise AdmissionToolHold("HOLD_ADMISSION_CONTRACT_VERSION")
    if value.get("store_schema_version") != 3:
        raise AdmissionToolHold("HOLD_ADMISSION_STORE_SCHEMA")
    expected_authority = {
        "attempt_store_creation_authorized": True,
        "evidence_consumption_authorized": False,
        "live_request_materialization_authorized": False,
        "private_key_access": False,
        "runtime_execution_authorized": False,
        "service_action_authorized": False,
        "session_advance_authorized": False,
        "signing_authorized": False,
    }
    if value.get("authority") != expected_authority:
        raise AdmissionToolHold("HOLD_ADMISSION_AUTHORITY_DRIFT")
    data_dir = Path(value["void_data_dir"])
    store = Path(value["store_path"])
    if store != data_dir / value["store_relative_path"]:
        raise AdmissionToolHold("HOLD_ADMISSION_STORE_PATH_DRIFT")
    return value


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
        },
    )
    return cp


def verify_runtime(contract: dict[str, Any]) -> Path:
    repo = Path(contract["runtime_repository"])
    try:
        if repo.resolve(strict=True) != repo:
            raise AdmissionToolHold("HOLD_RUNTIME_REPOSITORY_SYMLINKED")
    except OSError as error:
        raise AdmissionToolHold("HOLD_RUNTIME_REPOSITORY_NOT_FOUND") from error

    head = _run(GIT, "-C", str(repo), "rev-parse", "HEAD")
    if head.returncode != 0 or head.stdout.strip() != contract["runtime_source_commit"]:
        raise AdmissionToolHold("HOLD_RUNTIME_SOURCE_COMMIT")

    status_result = _run(
        GIT, "-C", str(repo), "status", "--porcelain", "--untracked-files=all"
    )
    if status_result.returncode != 0 or status_result.stdout.strip():
        raise AdmissionToolHold("HOLD_RUNTIME_WORKTREE_DIRTY")

    for rel, expected in sorted(contract["runtime_artifact_git_blobs"].items()):
        blob = _run(GIT, "-C", str(repo), "rev-parse", f"HEAD:{rel}")
        if blob.returncode != 0 or blob.stdout.strip() != expected:
            raise AdmissionToolHold(f"HOLD_RUNTIME_ARTIFACT_BLOB:{rel}")
    return repo


def load_runtime_modules(repo: Path):
    original = list(sys.path)
    try:
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        structural = importlib.import_module("scripts.verify_controller_evidence_isolation_v1")
        producer_auth = importlib.import_module(
            "scripts.verify_controller_evidence_producer_auth_v1"
        )
        designated_root = importlib.import_module(
            "scripts.war_college_designated_producer_trust_root_v1"
        )
        store = importlib.import_module("scripts.controller_attempt_admission_store_v1")
        return structural, producer_auth, designated_root, store
    finally:
        sys.path[:] = original


def _read_public_pem(path: Path) -> str:
    try:
        visible = path.lstat()
    except OSError as error:
        raise AdmissionToolHold("HOLD_PUBLIC_PEM_NOT_FOUND") from error
    if stat.S_ISLNK(visible.st_mode) or not stat.S_ISREG(visible.st_mode):
        raise AdmissionToolHold("HOLD_PUBLIC_PEM_NOT_REGULAR")
    if visible.st_size > 4096:
        raise AdmissionToolHold("HOLD_PUBLIC_PEM_TOO_LARGE")
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as error:
        raise AdmissionToolHold("HOLD_PUBLIC_PEM_OPEN") from error
    try:
        before = os.fstat(fd)
        raw = os.read(fd, 4097)
        after = os.fstat(fd)
        if (
            before.st_dev != after.st_dev
            or before.st_ino != after.st_ino
            or before.st_size != after.st_size
            or len(raw) != before.st_size
            or len(raw) > 4096
        ):
            raise AdmissionToolHold("HOLD_PUBLIC_PEM_CHANGED_DURING_READ")
    finally:
        os.close(fd)
    try:
        return raw.decode("ascii", "strict")
    except UnicodeError as error:
        raise AdmissionToolHold("HOLD_PUBLIC_PEM_ASCII") from error


def build_identity(
    *,
    contract: dict[str, Any],
    modules,
    public_pem: str,
    attempt_id: str,
    controller_a_id: str,
    controller_a_player_id: str,
    controller_b_id: str,
    controller_b_player_id: str,
):
    structural, producer_auth, designated_root, store = modules

    if structural.GENERATION != contract["source_generation"]:
        raise AdmissionToolHold("HOLD_SOURCE_GENERATION_DRIFT")
    if structural.ENGINE_FROZEN_COMMIT != contract["engine_commit"]:
        raise AdmissionToolHold("HOLD_ENGINE_COMMIT_DRIFT")
    if (
        structural.WAR_COLLEGE_FROZEN_COMMIT
        != contract["war_college_frozen_comparison"]
    ):
        raise AdmissionToolHold("HOLD_WAR_COLLEGE_FROZEN_DRIFT")

    derived = producer_auth.derive_void_node_identity_from_public_pem(public_pem)
    if derived is None:
        raise AdmissionToolHold("HOLD_PUBLIC_KEY_NOT_CANONICAL_ED25519")
    node_id, pem_sha256, _key = derived
    if node_id != contract["producer_node_id"]:
        raise AdmissionToolHold("HOLD_PRODUCER_NODE_ID_NOT_DESIGNATED")

    identity = store.AttemptIdentity(
        attempt_id=attempt_id,
        producer_id=node_id,
        producer_public_key_sha256=pem_sha256,
        controller_a_id=controller_a_id,
        controller_a_player_id=controller_a_player_id,
        controller_b_id=controller_b_id,
        controller_b_player_id=controller_b_player_id,
        source_generation=contract["source_generation"],
        war_college_commit=contract["store_war_college_source_base"],
        engine_commit=contract["engine_commit"],
    )
    validator = getattr(store, "_validate_identity", None)
    if not callable(validator):
        raise AdmissionToolHold("HOLD_STORE_IDENTITY_VALIDATOR_UNAVAILABLE")
    try:
        validator(identity)
    except Exception as error:
        raise AdmissionToolHold(f"HOLD_ATTEMPT_IDENTITY:{type(error).__name__}") from error

    trust = designated_root.verify_designated_producer_trust_v1(
        identity=identity,
        producer_auth_record={"producer_public_key_pem": public_pem},
    )
    if trust.get("contract") != "GREEN":
        raise AdmissionToolHold(
            "HOLD_DESIGNATED_PRODUCER_TRUST:"
            + ",".join(trust.get("holds", []))
        )
    if trust.get("trust_root_id") != contract["designated_trust_root_id"]:
        raise AdmissionToolHold("HOLD_DESIGNATED_TRUST_ROOT_ID")
    if (
        trust.get("public_key_fingerprint_sha256")
        != contract["producer_public_key_der_sha256"]
    ):
        raise AdmissionToolHold("HOLD_DESIGNATED_PUBLIC_KEY_FINGERPRINT")
    return identity, trust


def plan_admission(
    *,
    contract: dict[str, Any],
    identity,
    trust: dict[str, Any],
) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "phase": "PLAN",
        "attempt_id": identity.attempt_id,
        "producer_node_id": identity.producer_id,
        "producer_public_key_sha256": identity.producer_public_key_sha256,
        "controller_player_bindings": [
            {
                "controller_id": identity.controller_a_id,
                "player_id": identity.controller_a_player_id,
            },
            {
                "controller_id": identity.controller_b_id,
                "player_id": identity.controller_b_player_id,
            },
        ],
        "source_generation": identity.source_generation,
        "store_war_college_source_base": identity.war_college_commit,
        "engine_commit": identity.engine_commit,
        "store_path": contract["store_path"],
        "store_schema_version": contract["store_schema_version"],
        "initial_session_generation": contract["first_session_generation"],
        "trust_root_id": trust["trust_root_id"],
        "controller_binding_authority": contract["controller_binding_authority"],
        "store_creation_performed": False,
        "private_key_access": False,
        "signing_action": False,
        "evidence_consumption": False,
        "session_advance": False,
        "service_action": False,
        "runtime_execution": False,
        "live_request_materialization": False,
    }


def _require_directory(path: Path, *, uid: int, gid: int, mode: int) -> None:
    try:
        st = path.lstat()
    except OSError as error:
        raise AdmissionToolHold(f"HOLD_DIRECTORY_NOT_FOUND:{path}") from error
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode):
        raise AdmissionToolHold(f"HOLD_DIRECTORY_NOT_PLAIN:{path}")
    if st.st_uid != uid or st.st_gid != gid:
        raise AdmissionToolHold(f"HOLD_DIRECTORY_OWNER:{path}")
    if stat.S_IMODE(st.st_mode) != mode:
        raise AdmissionToolHold(f"HOLD_DIRECTORY_MODE:{path}")


def _inspect_created_store(
    path: Path,
    attempt_id: str,
    *,
    expected_uid: int,
    expected_gid: int,
) -> dict[str, Any]:
    try:
        visible = path.lstat()
    except OSError as error:
        raise AdmissionToolHold("HOLD_CREATED_STORE_NOT_FOUND") from error
    if stat.S_ISLNK(visible.st_mode) or not stat.S_ISREG(visible.st_mode):
        raise AdmissionToolHold("HOLD_CREATED_STORE_NOT_REGULAR")
    if visible.st_uid != expected_uid or visible.st_gid != expected_gid:
        raise AdmissionToolHold("HOLD_CREATED_STORE_OWNER")
    if stat.S_IMODE(visible.st_mode) != 0o600:
        raise AdmissionToolHold("HOLD_CREATED_STORE_MODE")

    try:
        db = sqlite3.connect(
            f"file:{path}?mode=ro",
            uri=True,
            timeout=5.0,
            isolation_level=None,
        )
    except sqlite3.Error as error:
        raise AdmissionToolHold("HOLD_CREATED_STORE_READBACK_OPEN") from error
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA query_only=ON")
        schema = db.execute(
            "SELECT value FROM metadata WHERE key='schema_version'"
        ).fetchone()
        if schema is None or schema["value"] != "3":
            raise AdmissionToolHold("HOLD_CREATED_STORE_SCHEMA")
        row = db.execute(
            "SELECT attempt_id, current_session_generation FROM attempts WHERE attempt_id=?",
            (attempt_id,),
        ).fetchone()
        if row is None or int(row["current_session_generation"]) != 1:
            raise AdmissionToolHold("HOLD_CREATED_ATTEMPT_READBACK")
        sessions = db.execute(
            "SELECT COUNT(*) AS n FROM sessions WHERE attempt_id=?",
            (attempt_id,),
        ).fetchone()["n"]
        consumptions = db.execute(
            "SELECT COUNT(*) AS n FROM consumptions"
        ).fetchone()["n"]
        if sessions != 1 or consumptions != 0:
            raise AdmissionToolHold("HOLD_CREATED_STORE_CARDINALITY")
    finally:
        db.close()
    return {
        "schema_version": 3,
        "attempt_present": True,
        "session_generation": 1,
        "session_count": 1,
        "consumption_count": 0,
        "mode": "0o600",
    }


def apply_admission(
    *,
    contract: dict[str, Any],
    modules,
    identity,
    confirmation: str,
    store_path: Path | None = None,
    data_dir: Path | None = None,
    enforce_host: bool = True,
) -> dict[str, Any]:
    if confirmation != contract["explicit_apply_confirmation"]:
        raise AdmissionToolHold("HOLD_EXPLICIT_APPLY_CONFIRMATION")
    if enforce_host:
        if os.getuid() != EXPECTED_UID or os.getgid() != EXPECTED_GID:
            raise AdmissionToolHold("HOLD_OPERATOR_UID_GID")
        if socket.gethostname() != contract["designated_hostname"]:
            raise AdmissionToolHold("HOLD_DESIGNATED_HOSTNAME")

    store_path = store_path or Path(contract["store_path"])
    data_dir = data_dir or Path(contract["void_data_dir"])
    expected_uid = EXPECTED_UID if enforce_host else os.getuid()
    expected_gid = EXPECTED_GID if enforce_host else os.getgid()

    if enforce_host and store_path != Path(contract["store_path"]):
        raise AdmissionToolHold("HOLD_CANONICAL_STORE_PATH")
    _require_directory(data_dir, uid=expected_uid, gid=expected_gid, mode=0o700)

    wc_dir = store_path.parent
    if wc_dir.parent != data_dir:
        raise AdmissionToolHold("HOLD_WAR_COLLEGE_DIRECTORY_DERIVATION")

    if wc_dir.exists() or wc_dir.is_symlink():
        _require_directory(wc_dir, uid=expected_uid, gid=expected_gid, mode=0o700)
        wc_dir_created = False
    else:
        os.mkdir(wc_dir, 0o700)
        _require_directory(wc_dir, uid=expected_uid, gid=expected_gid, mode=0o700)
        wc_dir_created = True

    if store_path.exists() or store_path.is_symlink():
        raise AdmissionToolHold("HOLD_CANONICAL_STORE_ALREADY_EXISTS")

    store = modules[3]
    old_umask = os.umask(0o077)
    try:
        receipt = store.create_attempt(store_path, identity)
    finally:
        os.umask(old_umask)

    if receipt.get("contract") != "GREEN":
        raise AdmissionToolHold("HOLD_CREATE_ATTEMPT_RECEIPT")
    readback = _inspect_created_store(
        store_path,
        identity.attempt_id,
        expected_uid=expected_uid,
        expected_gid=expected_gid,
    )
    return {
        "marker": MARKER,
        "phase": "APPLIED_FIRST_ATTEMPT",
        "attempt_id": identity.attempt_id,
        "receipt": receipt,
        "store_path": str(store_path),
        "war_college_directory_created": wc_dir_created,
        "store_creation_performed": True,
        "readback": readback,
        "private_key_access": False,
        "signing_action": False,
        "evidence_consumption": False,
        "session_advance": False,
        "service_action": False,
        "runtime_execution": False,
        "live_request_materialization": False,
    }


def _add_identity_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--controller-a-id", required=True)
    parser.add_argument("--controller-a-player-id", required=True)
    parser.add_argument("--controller-b-id", required=True)
    parser.add_argument("--controller-b-player-id", required=True)
    parser.add_argument("--producer-public-pem", type=Path, required=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    _add_identity_args(plan)
    apply = sub.add_parser("apply")
    _add_identity_args(apply)
    apply.add_argument("--confirm-create-store", required=True)
    args = parser.parse_args(argv)

    contract = load_contract()
    runtime = verify_runtime(contract)
    modules = load_runtime_modules(runtime)
    public_pem = _read_public_pem(args.producer_public_pem)
    identity, trust = build_identity(
        contract=contract,
        modules=modules,
        public_pem=public_pem,
        attempt_id=args.attempt_id,
        controller_a_id=args.controller_a_id,
        controller_a_player_id=args.controller_a_player_id,
        controller_b_id=args.controller_b_id,
        controller_b_player_id=args.controller_b_player_id,
    )

    if args.command == "plan":
        report = plan_admission(contract=contract, identity=identity, trust=trust)
    else:
        report = apply_admission(
            contract=contract,
            modules=modules,
            identity=identity,
            confirmation=args.confirm_create_store,
        )
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AdmissionToolHold as error:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "phase": "HOLD",
                    "hold": str(error),
                    "store_creation_performed": False,
                    "private_key_access": False,
                    "signing_action": False,
                    "evidence_consumption": False,
                    "session_advance": False,
                    "service_action": False,
                    "runtime_execution": False,
                    "live_request_materialization": False,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        raise SystemExit(2)
