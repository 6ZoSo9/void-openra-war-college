#!/usr/bin/env python3
"""Plan or separately capture one causal controller-evidence canary.

The first capture is deliberately an operator-bound empty-action canary. It
proves the admitted controller/player isolation and evidence pipeline; it does
not claim that Apollyon or Abaddon's model executed.

`plan` is read-only and never contacts OpenRA.
`capture` requires an exact confirmation, then launches an isolated child
process group. The child obtains both player perspectives at a shared bootstrap
end tick T and performs a second atomic JointAdvance whose start tick must be T.
Only after the child, its OpenRA daemon, and its process group are fully retired
may the parent publish private schema-3 evidence.

This source never reads a private key, signs, consumes evidence, advances the
durable controller session, starts/reloads a service, or materializes a live
verifier request.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib
import json
import os
import signal
import socket
import sqlite3
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONTRACT_PATH = (
    ROOT / "config/war-college/designated-host-controller-evidence-capture-v1.json"
)
MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_CONTROLLER_EVIDENCE_CAPTURE_TOOL_V2"
EVIDENCE_MARKER = "VOID_WAR_COLLEGE_CONTROLLER_EVIDENCE_ISOLATION_V1"
CHILD_MARKER = "VOID_WAR_COLLEGE_CONTROLLER_EVIDENCE_CAPTURE_CHILD_V1"
EXPECTED_UID = 1000
EXPECTED_GID = 1000


class CaptureHold(RuntimeError):
    pass


class CaptureOperationHold(CaptureHold):
    def __init__(self, message: str, *, state: dict[str, Any]) -> None:
        super().__init__(message)
        self.state = dict(state)


def _new_state() -> dict[str, Any]:
    return {
        "runtime_child_started": False,
        "runtime_child_clean_exit": False,
        "runtime_child_group_retired": False,
        "private_output_root_created": False,
        "private_evidence_created": False,
    }


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd) if cwd is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        },
    )


def _git_scalar(repo: Path, *args: str) -> str:
    cp = _run("git", "-C", str(repo), *args)
    if cp.returncode != 0:
        raise CaptureHold(
            f"HOLD_GIT_COMMAND:{' '.join(args)}:{cp.stderr.strip()}"
        )
    return cp.stdout.strip()


def load_contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if value.get("marker") != (
        "VOID_WAR_COLLEGE_DESIGNATED_HOST_CONTROLLER_EVIDENCE_CAPTURE_V2"
    ):
        raise CaptureHold("HOLD_CAPTURE_CONTRACT_MARKER")
    if value.get("version") != 2:
        raise CaptureHold("HOLD_CAPTURE_CONTRACT_VERSION")
    expected_source_authority = {
        "canonical_store_mutation": False,
        "controller_model_execution": False,
        "evidence_consumption": False,
        "live_request_materialization": False,
        "private_key_access": False,
        "runtime_execution": False,
        "service_action": False,
        "session_advance": False,
        "signing": False,
    }
    if value.get("source_lane_authority") != expected_source_authority:
        raise CaptureHold("HOLD_CAPTURE_SOURCE_AUTHORITY_DRIFT")
    if value.get("store_schema_version") != 3:
        raise CaptureHold("HOLD_CAPTURE_STORE_SCHEMA")
    if value.get("controller_session_generation") != 1:
        raise CaptureHold("HOLD_CAPTURE_SESSION_GENERATION")
    if value.get("bootstrap_ticks") != 1 or value.get("action_ticks") != 1:
        raise CaptureHold("HOLD_CAPTURE_TICK_SHAPE")
    if value.get("action_profile") != "empty_joint_batches":
        raise CaptureHold("HOLD_CAPTURE_ACTION_PROFILE")
    if value.get("controller_decision_provenance") != (
        "operator_bound_empty_action_profile_v1"
    ):
        raise CaptureHold("HOLD_CAPTURE_CONTROLLER_DECISION_PROVENANCE")
    if value.get("controller_model_execution") is not False:
        raise CaptureHold("HOLD_CAPTURE_CONTROLLER_MODEL_EXECUTION")
    if value.get("runtime_containment_strategy") != (
        "spawned_capture_child_private_process_group_v1"
    ):
        raise CaptureHold("HOLD_CAPTURE_CONTAINMENT_STRATEGY")
    if value.get("private_publish_strategy") != (
        "retained_output_directory_fd_o_excl_v1"
    ):
        raise CaptureHold("HOLD_CAPTURE_PRIVATE_PUBLISH_STRATEGY")
    if value.get("source_import_strategy") != (
        "repo_root_insert_before_runtime_imports_v1"
    ):
        raise CaptureHold("HOLD_CAPTURE_IMPORT_STRATEGY")
    bindings = value.get("controller_player_bindings")
    if bindings != [
        {"controller_id": "apollyon", "player_id": "Multi0"},
        {"controller_id": "abaddon", "player_id": "Multi1"},
    ]:
        raise CaptureHold("HOLD_CAPTURE_CONTROLLER_BINDING_DRIFT")
    for field in (
        "ready_timeout_s",
        "rpc_timeout_s",
        "teardown_timeout_s",
        "capture_outer_timeout_s",
        "runtime_retirement_signal_grace_s",
    ):
        if type(value.get(field)) is not int or value[field] <= 0:
            raise CaptureHold(f"HOLD_CAPTURE_TIMEOUT:{field}")
    return value


def verify_source_generation(contract: dict[str, Any]) -> str:
    branch = _git_scalar(ROOT, "branch", "--show-current")
    if branch != contract["source_branch"]:
        raise CaptureHold("HOLD_CAPTURE_SOURCE_BRANCH")
    if _git_scalar(ROOT, "status", "--porcelain", "--untracked-files=all"):
        raise CaptureHold("HOLD_CAPTURE_SOURCE_WORKTREE_DIRTY")
    for rel, expected in sorted(contract["bound_source_git_blobs"].items()):
        actual = _git_scalar(ROOT, "rev-parse", f"HEAD:{rel}")
        if actual != expected:
            raise CaptureHold(f"HOLD_CAPTURE_BOUND_SOURCE_BLOB:{rel}")
    return _git_scalar(ROOT, "rev-parse", "HEAD")


def verify_runtime_generation(contract: dict[str, Any]) -> Path:
    repo = Path(contract["runtime_repository"])
    if repo.resolve(strict=True) != repo:
        raise CaptureHold("HOLD_CAPTURE_RUNTIME_REPOSITORY_IDENTITY")
    if _git_scalar(repo, "rev-parse", "HEAD") != contract["runtime_source_commit"]:
        raise CaptureHold("HOLD_CAPTURE_RUNTIME_SOURCE_HEAD")
    if _git_scalar(repo, "status", "--porcelain", "--untracked-files=all"):
        raise CaptureHold("HOLD_CAPTURE_RUNTIME_WORKTREE_DIRTY")

    openra = Path(contract["openra_directory"])
    if openra.resolve(strict=True) != openra:
        raise CaptureHold("HOLD_CAPTURE_OPENRA_DIRECTORY_IDENTITY")
    if _git_scalar(openra, "rev-parse", "HEAD") != contract["engine_commit"]:
        raise CaptureHold("HOLD_CAPTURE_ENGINE_HEAD")
    if _git_scalar(openra, "status", "--porcelain", "--untracked-files=all"):
        raise CaptureHold("HOLD_CAPTURE_ENGINE_WORKTREE_DIRTY")
    return openra


def verify_dotnet(contract: dict[str, Any]) -> Path:
    path = Path(contract["dotnet_path"])
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise CaptureHold("HOLD_CAPTURE_DOTNET_NOT_FOUND") from error
    if resolved != path or not path.is_file() or not os.access(path, os.X_OK):
        raise CaptureHold("HOLD_CAPTURE_DOTNET_IDENTITY")
    cp = subprocess.run(
        [str(path), "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": f"{path.parent}:/usr/bin:/bin",
            "DOTNET_ROOT": str(path.parent),
        },
    )
    if cp.returncode != 0 or cp.stdout.strip() != contract["dotnet_version"]:
        raise CaptureHold("HOLD_CAPTURE_DOTNET_VERSION")
    return path


def _read_attempt_ro(contract: dict[str, Any]) -> dict[str, Any]:
    path = Path(contract["store_path"])
    try:
        visible = path.lstat()
    except OSError as error:
        raise CaptureHold("HOLD_CAPTURE_STORE_NOT_FOUND") from error
    if stat.S_ISLNK(visible.st_mode) or not stat.S_ISREG(visible.st_mode):
        raise CaptureHold("HOLD_CAPTURE_STORE_NOT_REGULAR")
    if visible.st_uid != EXPECTED_UID or visible.st_gid != EXPECTED_GID:
        raise CaptureHold("HOLD_CAPTURE_STORE_OWNER")
    if stat.S_IMODE(visible.st_mode) != 0o600:
        raise CaptureHold("HOLD_CAPTURE_STORE_MODE")

    before = (
        visible.st_dev,
        visible.st_ino,
        visible.st_size,
        visible.st_mtime_ns,
        visible.st_ctime_ns,
    )
    try:
        db = sqlite3.connect(
            f"file:{path}?mode=ro",
            uri=True,
            timeout=5.0,
            isolation_level=None,
        )
    except sqlite3.Error as error:
        raise CaptureHold("HOLD_CAPTURE_STORE_OPEN_RO") from error
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA query_only=ON")
        schema = db.execute(
            "SELECT value FROM metadata WHERE key='schema_version'"
        ).fetchone()
        if schema is None or schema["value"] != "3":
            raise CaptureHold("HOLD_CAPTURE_STORE_SCHEMA_DRIFT")
        row = db.execute(
            "SELECT * FROM attempts WHERE attempt_id=?",
            (contract["attempt_id"],),
        ).fetchone()
        if row is None:
            raise CaptureHold("HOLD_CAPTURE_ATTEMPT_NOT_FOUND")
        consumptions = db.execute(
            """
            SELECT COUNT(*) AS n
            FROM consumptions
            WHERE attempt_id=? AND session_generation=?
            """,
            (
                contract["attempt_id"],
                contract["controller_session_generation"],
            ),
        ).fetchone()["n"]
        session = db.execute(
            """
            SELECT session_generation
            FROM sessions
            WHERE attempt_id=? AND session_generation=?
            """,
            (
                contract["attempt_id"],
                contract["controller_session_generation"],
            ),
        ).fetchone()
    finally:
        db.close()

    after_st = path.lstat()
    after = (
        after_st.st_dev,
        after_st.st_ino,
        after_st.st_size,
        after_st.st_mtime_ns,
        after_st.st_ctime_ns,
    )
    if before != after:
        raise CaptureHold("HOLD_CAPTURE_STORE_CHANGED_DURING_RO_READ")
    if session is None:
        raise CaptureHold("HOLD_CAPTURE_SESSION_NOT_FOUND")
    if int(row["current_session_generation"]) != contract[
        "controller_session_generation"
    ]:
        raise CaptureHold("HOLD_CAPTURE_SESSION_NOT_CURRENT")
    if int(consumptions) != 0:
        raise CaptureHold("HOLD_CAPTURE_SESSION_ALREADY_CONSUMED")

    expected = {
        "attempt_id": contract["attempt_id"],
        "producer_id": contract["producer_node_id"],
        "producer_public_key_sha256": contract["producer_public_key_sha256"],
        "controller_a_id": contract["controller_player_bindings"][0][
            "controller_id"
        ],
        "controller_a_player_id": contract["controller_player_bindings"][0][
            "player_id"
        ],
        "controller_b_id": contract["controller_player_bindings"][1][
            "controller_id"
        ],
        "controller_b_player_id": contract["controller_player_bindings"][1][
            "player_id"
        ],
        "source_generation": contract["source_generation"],
        "war_college_commit": contract["store_war_college_source_base"],
        "engine_commit": contract["engine_commit"],
    }
    actual = {key: row[key] for key in expected}
    if actual != expected:
        raise CaptureHold("HOLD_CAPTURE_ATTEMPT_IDENTITY_DRIFT")
    return {
        **actual,
        "current_session_generation": int(row["current_session_generation"]),
        "consumption_count": int(consumptions),
    }


def load_structural_verifier():
    return importlib.import_module("scripts.verify_controller_evidence_isolation_v1")


def load_benchmark_core():
    return importlib.import_module("bench_joint_advance_core")


def _player_observations(response: Any) -> dict[str, Any]:
    records = list(getattr(response, "player_observations", []))
    result: dict[str, Any] = {}
    for record in records:
        player = getattr(record, "player", None)
        observation = getattr(record, "observation", None)
        if not isinstance(player, str) or not player or observation is None:
            raise CaptureHold("HOLD_CAPTURE_PLAYER_OBSERVATION_SHAPE")
        if player in result:
            raise CaptureHold("HOLD_CAPTURE_DUPLICATE_PLAYER_OBSERVATION")
        result[player] = observation
    if set(result) != {"Multi0", "Multi1"}:
        raise CaptureHold("HOLD_CAPTURE_PLAYER_OBSERVATION_COVERAGE")
    return result


def _positive_unique_actor_ids(items: Any, player: str, *, enemy: bool) -> list[int]:
    result: list[int] = []
    for item in list(items):
        actor_id = getattr(item, "actor_id", None)
        owner = getattr(item, "owner", None)
        if type(actor_id) is not int or actor_id <= 0:
            raise CaptureHold("HOLD_CAPTURE_ACTOR_ID")
        if not isinstance(owner, str) or not owner:
            raise CaptureHold("HOLD_CAPTURE_ACTOR_OWNER")
        if enemy and owner == player:
            raise CaptureHold("HOLD_CAPTURE_VISIBLE_ENEMY_OWNED_BY_PLAYER")
        if not enemy and owner != player:
            raise CaptureHold("HOLD_CAPTURE_OWN_ACTOR_OWNER_MISMATCH")
        result.append(actor_id)
    if len(result) != len(set(result)):
        raise CaptureHold("HOLD_CAPTURE_DUPLICATE_ACTOR_ID")
    return sorted(result)


def observation_payload(
    *,
    observation: Any,
    player: str,
    world_tick: int,
    contract: dict[str, Any],
) -> dict[str, Any]:
    if getattr(observation, "tick", None) != world_tick:
        raise CaptureHold("HOLD_CAPTURE_OBSERVATION_TICK_MISMATCH")

    owned_units = _positive_unique_actor_ids(
        getattr(observation, "units", []), player, enemy=False
    )
    owned_buildings = _positive_unique_actor_ids(
        getattr(observation, "buildings", []), player, enemy=False
    )
    visible_enemy_units = _positive_unique_actor_ids(
        getattr(observation, "visible_enemies", []), player, enemy=True
    )
    visible_enemy_buildings = _positive_unique_actor_ids(
        getattr(observation, "visible_enemy_buildings", []),
        player,
        enemy=True,
    )
    visible_enemies = sorted(
        set(visible_enemy_units) | set(visible_enemy_buildings)
    )
    if set(owned_units) & set(owned_buildings):
        raise CaptureHold("HOLD_CAPTURE_OWN_ACTOR_CLASS_OVERLAP")
    if (set(owned_units) | set(owned_buildings)) & set(visible_enemies):
        raise CaptureHold("HOLD_CAPTURE_OWN_ENEMY_ACTOR_OVERLAP")

    available = sorted(
        {
            item
            for item in list(getattr(observation, "available_production", []))
            if isinstance(item, str) and item
        }
    )
    active = sorted(
        {
            getattr(item, "item", "")
            for item in list(getattr(observation, "production", []))
            if isinstance(getattr(item, "item", ""), str)
            and getattr(item, "item", "")
        }
    )
    return {
        "attempt_id": contract["attempt_id"],
        "controller_session_generation": contract[
            "controller_session_generation"
        ],
        "player_id": player,
        "owned_unit_actor_ids": owned_units,
        "owned_building_actor_ids": owned_buildings,
        "visible_enemy_actor_ids": visible_enemies,
        "available_production_items": available,
        "active_production_items": active,
        "world_tick": world_tick,
    }


def _action_request_id(
    *,
    contract: dict[str, Any],
    player: str,
    controller_id: str,
    world_tick: int,
    observation_binding_sha256: str,
) -> str:
    digest = sha256_hex(
        {
            "attempt_id": contract["attempt_id"],
            "controller_session_generation": contract[
                "controller_session_generation"
            ],
            "controller_id": controller_id,
            "observation_binding_sha256": observation_binding_sha256,
            "player_id": player,
            "world_tick": world_tick,
        }
    )
    return f"wca1-{digest}"


def build_causal_evidence(
    *,
    bootstrap_response: Any,
    action_response: Any,
    expected_session_id: str,
    contract: dict[str, Any],
    structural: Any,
) -> dict[str, Any]:
    if getattr(bootstrap_response, "session_id", None) != expected_session_id:
        raise CaptureHold("HOLD_CAPTURE_BOOTSTRAP_SESSION_BINDING")
    if getattr(action_response, "session_id", None) != expected_session_id:
        raise CaptureHold("HOLD_CAPTURE_ACTION_SESSION_BINDING")

    bootstrap_start = getattr(bootstrap_response, "start_tick", None)
    bootstrap_end = getattr(bootstrap_response, "end_tick", None)
    action_start = getattr(action_response, "start_tick", None)
    action_end = getattr(action_response, "end_tick", None)
    for value in (bootstrap_start, bootstrap_end, action_start, action_end):
        if type(value) is not int or value < 0:
            raise CaptureHold("HOLD_CAPTURE_TICK_SCALAR")
    if bootstrap_end - bootstrap_start != contract["bootstrap_ticks"]:
        raise CaptureHold("HOLD_CAPTURE_BOOTSTRAP_TICK_DELTA")
    if action_start != bootstrap_end:
        raise CaptureHold("HOLD_CAPTURE_CAUSAL_ACTION_START_TICK")
    if action_end - action_start != contract["action_ticks"]:
        raise CaptureHold("HOLD_CAPTURE_ACTION_TICK_DELTA")

    world_tick = bootstrap_end
    observations = _player_observations(bootstrap_response)
    records: list[dict[str, Any]] = []
    bindings: list[dict[str, str]] = []

    for binding in contract["controller_player_bindings"]:
        controller_id = binding["controller_id"]
        player = binding["player_id"]
        observation = observation_payload(
            observation=observations[player],
            player=player,
            world_tick=world_tick,
            contract=contract,
        )
        observation_sha = structural.sha256_hex(observation)
        observation_binding_sha = structural.observation_binding(
            attempt_id=contract["attempt_id"],
            controller_session_generation=contract[
                "controller_session_generation"
            ],
            player_id=player,
            controller_id=controller_id,
            world_tick=world_tick,
            observation_sha256=observation_sha,
        )
        request_id = _action_request_id(
            contract=contract,
            player=player,
            controller_id=controller_id,
            world_tick=world_tick,
            observation_binding_sha256=observation_binding_sha,
        )
        action = {
            "request_id": request_id,
            "attempt_id": contract["attempt_id"],
            "controller_session_generation": contract[
                "controller_session_generation"
            ],
            "player_id": player,
            "controller_id": controller_id,
            "world_tick": world_tick,
            "decision_observation_binding_sha256": observation_binding_sha,
            "commands": [],
        }
        action_sha = structural.sha256_hex(action)
        action_binding_sha = structural.action_binding(
            attempt_id=contract["attempt_id"],
            controller_session_generation=contract[
                "controller_session_generation"
            ],
            player_id=player,
            controller_id=controller_id,
            world_tick=world_tick,
            action_request_id=request_id,
            action_sha256=action_sha,
            decision_observation_binding_sha256=observation_binding_sha,
        )
        record = {
            "player_id": player,
            "controller_id": controller_id,
            "observation_subject_player_id": player,
            "visibility_owner_player_id": player,
            "action_actor_player_id": player,
            "observation_payload": observation,
            "observation_sha256": observation_sha,
            "observation_binding_sha256": observation_binding_sha,
            "action_request_id": request_id,
            "action_payload": action,
            "action_sha256": action_sha,
            "action_binding_sha256": action_binding_sha,
        }
        records.append(record)
        bindings.append(
            {
                "action_binding_sha256": action_binding_sha,
                "controller_id": controller_id,
                "observation_binding_sha256": observation_binding_sha,
                "player_id": player,
            }
        )

    evidence = {
        "marker": EVIDENCE_MARKER,
        "schema_version": 3,
        "generation": contract["source_generation"],
        "war_college_frozen_commit": contract[
            "war_college_frozen_comparison"
        ],
        "engine_frozen_commit": contract["engine_commit"],
        "attempt_id": contract["attempt_id"],
        "controller_session_generation": contract[
            "controller_session_generation"
        ],
        "world_tick": world_tick,
        "controllers": records,
        "joint_evidence_sha256": structural.joint_evidence_binding(
            attempt_id=contract["attempt_id"],
            controller_session_generation=contract[
                "controller_session_generation"
            ],
            world_tick=world_tick,
            bindings=bindings,
        ),
    }
    report = structural.verify_evidence(
        evidence,
        expected_attempt_id=contract["attempt_id"],
        expected_controller_session_generation=contract[
            "controller_session_generation"
        ],
    )
    if report.get("contract") != "GREEN":
        raise CaptureHold(
            "HOLD_CAPTURE_SELF_VERIFICATION:"
            + ",".join(report.get("holds", []))
        )
    return evidence


def _require_fd_path_identity(fd: int, expected: Path, *, label: str) -> None:
    try:
        resolved = Path(f"/proc/self/fd/{fd}").resolve(strict=True)
    except OSError as error:
        raise CaptureHold(f"HOLD_{label}_PATH_IDENTITY_UNAVAILABLE") from error
    if resolved != expected:
        raise CaptureHold(f"HOLD_{label}_PATH_IDENTITY")


def _open_downloads_fd() -> tuple[int, Path]:
    downloads = Path.home() / "Downloads"
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        fd = os.open(downloads, flags)
    except OSError as error:
        raise CaptureHold("HOLD_CAPTURE_DOWNLOADS_OPEN") from error
    try:
        st = os.fstat(fd)
        if not stat.S_ISDIR(st.st_mode):
            raise CaptureHold("HOLD_CAPTURE_DOWNLOADS_NOT_DIRECTORY")
        if st.st_uid != os.getuid() or st.st_gid != os.getgid():
            raise CaptureHold("HOLD_CAPTURE_DOWNLOADS_OWNER")
        _require_fd_path_identity(fd, downloads, label="CAPTURE_DOWNLOADS")
        return fd, downloads
    except Exception:
        os.close(fd)
        raise


def _private_output_path(contract: dict[str, Any]) -> Path:
    return Path(contract["private_output_root"]) / contract["evidence_filename"]


def inspect_private_output_namespace(contract: dict[str, Any]) -> dict[str, bool]:
    downloads_fd, _downloads = _open_downloads_fd()
    root = Path(contract["private_output_root"])
    try:
        if root.parent != Path.home() / "Downloads":
            raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_PARENT")
        flags = (
            os.O_RDONLY
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        try:
            root_fd = os.open(root.name, flags, dir_fd=downloads_fd)
        except FileNotFoundError:
            return {"root_exists": False, "evidence_exists": False}
        except OSError as error:
            raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_OPEN") from error
        try:
            st = os.fstat(root_fd)
            if not stat.S_ISDIR(st.st_mode):
                raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_NOT_DIRECTORY")
            if st.st_uid != os.getuid() or st.st_gid != os.getgid():
                raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_OWNER")
            if stat.S_IMODE(st.st_mode) != 0o700:
                raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_MODE")
            _require_fd_path_identity(
                root_fd, root, label="CAPTURE_PRIVATE_OUTPUT_ROOT"
            )
            try:
                os.stat(
                    contract["evidence_filename"],
                    dir_fd=root_fd,
                    follow_symlinks=False,
                )
                exists = True
            except FileNotFoundError:
                exists = False
            return {"root_exists": True, "evidence_exists": exists}
        finally:
            os.close(root_fd)
    finally:
        os.close(downloads_fd)


def _open_or_create_private_output_root(
    contract: dict[str, Any],
    *,
    state: dict[str, Any],
) -> tuple[int, int, Path]:
    downloads_fd, downloads = _open_downloads_fd()
    root = Path(contract["private_output_root"])
    if root.parent != downloads:
        os.close(downloads_fd)
        raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_PARENT")
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        try:
            root_fd = os.open(root.name, flags, dir_fd=downloads_fd)
        except FileNotFoundError:
            try:
                os.mkdir(root.name, 0o700, dir_fd=downloads_fd)
                state["private_output_root_created"] = True
            except FileExistsError:
                pass
            root_fd = os.open(root.name, flags, dir_fd=downloads_fd)
        st = os.fstat(root_fd)
        if not stat.S_ISDIR(st.st_mode):
            raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_NOT_DIRECTORY")
        if st.st_uid != os.getuid() or st.st_gid != os.getgid():
            raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_OWNER")
        if stat.S_IMODE(st.st_mode) != 0o700:
            raise CaptureHold("HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_MODE")
        _require_fd_path_identity(
            downloads_fd, downloads, label="CAPTURE_DOWNLOADS"
        )
        _require_fd_path_identity(
            root_fd, root, label="CAPTURE_PRIVATE_OUTPUT_ROOT"
        )
        return downloads_fd, root_fd, root
    except Exception:
        try:
            if "root_fd" in locals():
                os.close(root_fd)
        finally:
            os.close(downloads_fd)
        raise


def publish_private_create_only(
    *,
    root_fd: int,
    root_path: Path,
    filename: str,
    evidence: dict[str, Any],
    state: dict[str, Any],
) -> dict[str, Any]:
    payload = canonical_bytes(evidence) + b"\n"
    _require_fd_path_identity(
        root_fd, root_path, label="CAPTURE_PRIVATE_OUTPUT_ROOT"
    )
    try:
        os.stat(filename, dir_fd=root_fd, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise CaptureHold("HOLD_CAPTURE_EVIDENCE_ALREADY_EXISTS")

    flags = (
        os.O_CREAT
        | os.O_EXCL
        | os.O_WRONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        fd = os.open(filename, flags, 0o400, dir_fd=root_fd)
        state["private_evidence_created"] = True
    except FileExistsError as error:
        raise CaptureHold("HOLD_CAPTURE_EVIDENCE_ALREADY_EXISTS") from error
    try:
        os.fchmod(fd, 0o400)
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode):
            raise CaptureHold("HOLD_CAPTURE_PUBLISHED_EVIDENCE_NOT_REGULAR")
        if stat.S_IMODE(opened.st_mode) != 0o400:
            raise CaptureHold("HOLD_CAPTURE_PUBLISHED_EVIDENCE_MODE")
        with os.fdopen(fd, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.fsync(root_fd)
        _require_fd_path_identity(
            root_fd, root_path, label="CAPTURE_PRIVATE_OUTPUT_ROOT"
        )
        named = os.stat(filename, dir_fd=root_fd, follow_symlinks=False)
        current = os.fstat(fd)
        if not os.path.samestat(named, current):
            raise CaptureHold("HOLD_CAPTURE_PUBLISHED_EVIDENCE_IDENTITY")
        if current.st_uid != os.getuid() or current.st_gid != os.getgid():
            raise CaptureHold("HOLD_CAPTURE_PUBLISHED_EVIDENCE_OWNER")
        if stat.S_IMODE(current.st_mode) != 0o400:
            raise CaptureHold("HOLD_CAPTURE_PUBLISHED_EVIDENCE_MODE")
    finally:
        os.close(fd)

    read_fd = os.open(
        filename,
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
        dir_fd=root_fd,
    )
    try:
        readback = bytearray()
        while len(readback) <= len(payload):
            chunk = os.read(read_fd, min(65536, len(payload) + 1 - len(readback)))
            if not chunk:
                break
            readback.extend(chunk)
        if bytes(readback) != payload:
            raise CaptureHold("HOLD_CAPTURE_PUBLISHED_EVIDENCE_READBACK")
    finally:
        os.close(read_fd)

    _require_fd_path_identity(
        root_fd, root_path, label="CAPTURE_PRIVATE_OUTPUT_ROOT"
    )
    return {
        "path": str(root_path / filename),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "mode": "0o400",
        "descriptor_bound_parent": True,
    }


def _process_group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError as error:
        raise CaptureHold("HOLD_CAPTURE_PROCESS_GROUP_PERMISSION") from error
    return True


def _wait_group_absent(pgid: int, timeout_s: float) -> bool:
    deadline = time.monotonic() + timeout_s
    while True:
        if not _process_group_exists(pgid):
            return True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(0.01, remaining))


def force_retire_process_group(
    process: subprocess.Popen[str],
    pgid: int,
    *,
    signal_grace_s: float,
) -> str:
    if pgid != process.pid:
        raise CaptureHold("HOLD_CAPTURE_CHILD_PROCESS_GROUP_IDENTITY")
    if not _process_group_exists(pgid):
        if process.poll() is None:
            process.wait(timeout=signal_grace_s)
        return "already_absent"

    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=signal_grace_s)
    except subprocess.TimeoutExpired:
        pass
    if _wait_group_absent(pgid, signal_grace_s):
        return "sigterm_retired"

    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=signal_grace_s)
    except subprocess.TimeoutExpired as error:
        raise CaptureHold("HOLD_CAPTURE_CHILD_SIGKILL_WAIT") from error
    if not _wait_group_absent(pgid, signal_grace_s):
        raise CaptureHold("HOLD_CAPTURE_CHILD_GROUP_NOT_RETIRED")
    return "sigkill_retired"


def _child_env(contract: dict[str, Any]) -> dict[str, str]:
    dotnet = Path(contract["dotnet_path"])
    return {
        "HOME": str(Path.home()),
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": f"{dotnet.parent}:/usr/bin:/bin",
        "DOTNET_ROOT": str(dotnet.parent),
    }


def _runtime_child_command(
    contract: dict[str, Any],
    confirmation: str,
) -> list[str]:
    return [
        sys.executable,
        "-I",
        "-B",
        str(Path(__file__).resolve()),
        "_capture-child",
        "--confirm-capture",
        confirmation,
    ]


def _run_runtime_child(
    contract: dict[str, Any],
    *,
    confirmation: str,
    state: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], str]:
    command = _runtime_child_command(contract, confirmation)
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        env=_child_env(contract),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    state["runtime_child_started"] = True
    try:
        pgid = os.getpgid(process.pid)
    except ProcessLookupError as error:
        raise CaptureOperationHold(
            "HOLD_CAPTURE_CHILD_EXITED_BEFORE_PGID",
            state=state,
        ) from error
    if pgid != process.pid:
        raise CaptureOperationHold(
            "HOLD_CAPTURE_CHILD_PROCESS_GROUP_IDENTITY",
            state=state,
        )

    forced_terminal: str | None = None
    try:
        stdout, stderr = process.communicate(
            timeout=contract["capture_outer_timeout_s"]
        )
    except subprocess.TimeoutExpired:
        forced_terminal = force_retire_process_group(
            process,
            pgid,
            signal_grace_s=contract["runtime_retirement_signal_grace_s"],
        )
        state["runtime_child_group_retired"] = not _process_group_exists(pgid)
        stdout, stderr = process.communicate()
        raise CaptureOperationHold(
            f"HOLD_CAPTURE_CHILD_OUTER_TIMEOUT:{forced_terminal}",
            state=state,
        )

    group_was_absent = not _process_group_exists(pgid)
    if not group_was_absent:
        forced_terminal = force_retire_process_group(
            process,
            pgid,
            signal_grace_s=contract["runtime_retirement_signal_grace_s"],
        )
    state["runtime_child_group_retired"] = not _process_group_exists(pgid)
    state["runtime_child_clean_exit"] = (
        process.returncode == 0
        and group_was_absent
        and state["runtime_child_group_retired"]
    )
    if not state["runtime_child_clean_exit"]:
        raise CaptureOperationHold(
            "HOLD_CAPTURE_CHILD_NOT_CLEANLY_RETIRED:"
            f"rc={process.returncode}:forced={forced_terminal}:stderr={stderr.strip()}",
            state=state,
        )
    try:
        child = json.loads(stdout)
    except json.JSONDecodeError as error:
        raise CaptureOperationHold(
            "HOLD_CAPTURE_CHILD_OUTPUT_JSON",
            state=state,
        ) from error
    if (
        not isinstance(child, dict)
        or child.get("marker") != CHILD_MARKER
        or child.get("phase") != "CHILD_CAPTURE_GREEN"
    ):
        raise CaptureOperationHold(
            "HOLD_CAPTURE_CHILD_TERMINAL:"
            + json.dumps(child, sort_keys=True),
            state=state,
        )
    evidence = child.get("evidence")
    runtime = child.get("runtime")
    child_source_head = child.get("source_head")
    if (
        not isinstance(evidence, dict)
        or not isinstance(runtime, dict)
        or not isinstance(child_source_head, str)
        or len(child_source_head) != 40
        or any(char not in "0123456789abcdef" for char in child_source_head)
    ):
        raise CaptureOperationHold(
            "HOLD_CAPTURE_CHILD_PAYLOAD_SHAPE",
            state=state,
        )
    return evidence, runtime, child_source_head


def plan_capture(contract: dict[str, Any]) -> dict[str, Any]:
    attempt = _read_attempt_ro(contract)
    namespace = inspect_private_output_namespace(contract)
    return {
        "marker": MARKER,
        "phase": "PLAN",
        "attempt": attempt,
        "output_path": str(_private_output_path(contract)),
        "output_namespace": namespace,
        "controller_decision_provenance": contract[
            "controller_decision_provenance"
        ],
        "controller_model_execution": False,
        "bootstrap_ticks": contract["bootstrap_ticks"],
        "action_ticks": contract["action_ticks"],
        "runtime_containment_strategy": contract[
            "runtime_containment_strategy"
        ],
        "private_publish_strategy": contract["private_publish_strategy"],
        "causal_sequence": [
            "bootstrap JointAdvance with two empty batches -> perspectives at T",
            "bind operator-selected controller IDs to no-op actions at T",
            "action JointAdvance must prove start_tick == T",
            "structurally self-verify schema-3 evidence",
            "retire session, daemon, capture child, and process group",
            "re-prove current attempt/session and zero consumption",
            "publish private evidence through retained directory descriptor",
        ],
        "runtime_execution": False,
        "canonical_store_mutation": False,
        "private_key_access": False,
        "signing_action": False,
        "evidence_consumption": False,
        "session_advance": False,
        "service_action": False,
        "live_request_materialization": False,
    }


async def _capture_async(
    contract: dict[str, Any],
    openra: Path,
    source_head: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    bench = load_benchmark_core()
    grpc, _message_to_dict, pb2, pb2_grpc = bench._runtime_modules()
    expected_provenance = {
        "engine_sha": contract["engine_commit"],
        "war_college_sha": contract["war_college_frozen_comparison"],
        "benchmark_source_sha": source_head,
        "generation": contract["source_generation"],
    }
    runtime_provenance = bench.runtime_provenance(
        openra,
        expected_provenance,
    )
    bench.ensure_endpoint_unoccupied(contract["port"])

    daemon = None
    capture = None
    channel = None
    stub = None
    session_id = None
    cleanup: dict[str, Any] = {
        "session_destroyed": False,
        "channel_closed": False,
        "daemon_retired": False,
        "daemon_log_clean": False,
    }
    evidence: dict[str, Any] | None = None
    runtime_meta: dict[str, Any] = {
        "runtime_provenance": runtime_provenance,
    }
    try:
        daemon = bench.start_daemon(openra, contract["port"])
        if daemon.stdout is None:
            raise CaptureHold("HOLD_CAPTURE_DAEMON_STDOUT")
        capture = bench.BoundedLogCapture(daemon.stdout)
        capture.start()
        channel = grpc.aio.insecure_channel(
            f"127.0.0.1:{contract['port']}",
            options=[
                ("grpc.max_receive_message_length", 64 * 1024 * 1024),
                ("grpc.max_send_message_length", 16 * 1024 * 1024),
            ],
        )
        stub = pb2_grpc.RLBridgeStub(channel)
        listener = await bench.wait_ready(
            stub,
            pb2,
            daemon,
            contract["port"],
            contract["ready_timeout_s"],
        )
        create = await asyncio.wait_for(
            stub.CreateSession(
                pb2.CreateSessionRequest(
                    map_name=contract["map_name"],
                    bots=contract["bots"],
                    seed=contract["seed"],
                )
            ),
            timeout=contract["rpc_timeout_s"],
        )
        session_id = create.session_id
        if not isinstance(session_id, str) or not session_id:
            raise CaptureHold("HOLD_CAPTURE_SESSION_ID")
        await bench.wait_session_playing(
            stub, pb2, session_id, contract["rpc_timeout_s"]
        )

        def empty_batches():
            return [
                pb2.PlayerCommandBatch(player="Multi0"),
                pb2.PlayerCommandBatch(player="Multi1"),
            ]

        bootstrap = await asyncio.wait_for(
            stub.JointAdvance(
                pb2.JointAdvanceRequest(
                    session_id=session_id,
                    ticks=contract["bootstrap_ticks"],
                    player_actions=empty_batches(),
                )
            ),
            timeout=contract["rpc_timeout_s"],
        )
        bench.validate_joint_response(
            bootstrap,
            session_id,
            contract["bootstrap_ticks"],
        )

        action = await asyncio.wait_for(
            stub.JointAdvance(
                pb2.JointAdvanceRequest(
                    session_id=session_id,
                    ticks=contract["action_ticks"],
                    player_actions=empty_batches(),
                )
            ),
            timeout=contract["rpc_timeout_s"],
        )
        bench.validate_joint_response(
            action,
            session_id,
            contract["action_ticks"],
        )

        if (
            daemon.poll() is not None
            or bench.process_listener_identity(daemon.pid, contract["port"])
            != listener
        ):
            raise CaptureHold("HOLD_CAPTURE_DAEMON_IDENTITY_LOST")

        structural = load_structural_verifier()
        evidence = build_causal_evidence(
            bootstrap_response=bootstrap,
            action_response=action,
            expected_session_id=session_id,
            contract=contract,
            structural=structural,
        )
        runtime_meta.update(
            {
                "listener_identity": listener,
                "session_id": session_id,
                "bootstrap_start_tick": bootstrap.start_tick,
                "bootstrap_end_tick": bootstrap.end_tick,
                "action_start_tick": action.start_tick,
                "action_end_tick": action.end_tick,
            }
        )
    finally:
        if channel is not None and session_id is not None and stub is not None:
            try:
                teardown = await bench.destroy_sessions(
                    stub,
                    pb2,
                    [session_id],
                    contract["teardown_timeout_s"],
                )
                cleanup["session_destroyed"] = (
                    teardown.get("unretired_session_ids") == []
                    and teardown.get("failures") == []
                    and teardown.get("destroyed_session_ids") == [session_id]
                )
            except Exception:
                cleanup["session_destroyed"] = False
        if channel is not None:
            try:
                await channel.close()
                cleanup["channel_closed"] = True
            except Exception:
                cleanup["channel_closed"] = False
        if daemon is not None:
            try:
                if daemon.poll() is None:
                    daemon.terminate()
                    try:
                        daemon.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        daemon.kill()
                        daemon.wait(timeout=5)
                cleanup["daemon_retired"] = daemon.poll() is not None
            except Exception:
                cleanup["daemon_retired"] = False
        if capture is not None:
            try:
                log = capture.finish()
                cleanup["daemon_log_clean"] = (
                    not log.get("drain_error")
                    and log.get("drain_thread_retired") is True
                )
                runtime_meta["daemon_log_sha256"] = log.get("sha256")
                runtime_meta["daemon_log_bytes"] = log.get("total_bytes")
            except Exception:
                cleanup["daemon_log_clean"] = False

    if evidence is None:
        raise CaptureHold("HOLD_CAPTURE_NO_EVIDENCE")
    if cleanup != {
        "session_destroyed": True,
        "channel_closed": True,
        "daemon_retired": True,
        "daemon_log_clean": True,
    }:
        raise CaptureHold("HOLD_CAPTURE_CLEANUP_NOT_GREEN")
    return evidence, {**runtime_meta, "cleanup": cleanup}


def capture_child(
    contract: dict[str, Any],
    *,
    confirmation: str,
) -> dict[str, Any]:
    if confirmation != contract["explicit_capture_confirmation"]:
        raise CaptureHold("HOLD_CAPTURE_EXPLICIT_CONFIRMATION")
    if socket.gethostname() != contract["designated_hostname"]:
        raise CaptureHold("HOLD_CAPTURE_DESIGNATED_HOSTNAME")
    if os.getuid() != EXPECTED_UID or os.getgid() != EXPECTED_GID:
        raise CaptureHold("HOLD_CAPTURE_OPERATOR_UID_GID")

    source_head = verify_source_generation(contract)
    openra = verify_runtime_generation(contract)
    verify_dotnet(contract)
    attempt_before = _read_attempt_ro(contract)
    evidence, runtime = asyncio.run(
        _capture_async(contract, openra, source_head)
    )
    source_head_after = verify_source_generation(contract)
    if source_head_after != source_head:
        raise CaptureHold("HOLD_CAPTURE_CHILD_SOURCE_HEAD_DRIFT")
    verify_runtime_generation(contract)
    verify_dotnet(contract)
    attempt_after = _read_attempt_ro(contract)
    if attempt_after != attempt_before:
        raise CaptureHold("HOLD_CAPTURE_ATTEMPT_CHANGED_DURING_RUNTIME")
    return {
        "marker": CHILD_MARKER,
        "phase": "CHILD_CAPTURE_GREEN",
        "source_head": source_head,
        "attempt": attempt_after,
        "evidence": evidence,
        "runtime": runtime,
        "canonical_store_mutation": False,
        "controller_model_execution": False,
        "private_key_access": False,
        "signing_action": False,
        "evidence_consumption": False,
        "session_advance": False,
        "service_action": False,
        "live_request_materialization": False,
    }


def capture_runtime(
    contract: dict[str, Any],
    *,
    confirmation: str,
) -> dict[str, Any]:
    state = _new_state()
    try:
        if confirmation != contract["explicit_capture_confirmation"]:
            raise CaptureHold("HOLD_CAPTURE_EXPLICIT_CONFIRMATION")
        if socket.gethostname() != contract["designated_hostname"]:
            raise CaptureHold("HOLD_CAPTURE_DESIGNATED_HOSTNAME")
        if os.getuid() != EXPECTED_UID or os.getgid() != EXPECTED_GID:
            raise CaptureHold("HOLD_CAPTURE_OPERATOR_UID_GID")

        source_head = verify_source_generation(contract)
        verify_runtime_generation(contract)
        verify_dotnet(contract)
        attempt_before = _read_attempt_ro(contract)
        namespace = inspect_private_output_namespace(contract)
        if namespace["evidence_exists"]:
            raise CaptureHold("HOLD_CAPTURE_EVIDENCE_ALREADY_EXISTS")

        evidence, runtime, child_source_head = _run_runtime_child(
            contract,
            confirmation=confirmation,
            state=state,
        )
        if child_source_head != source_head:
            raise CaptureHold("HOLD_CAPTURE_PARENT_CHILD_SOURCE_HEAD_MISMATCH")

        source_head_after_child = verify_source_generation(contract)
        if source_head_after_child != source_head:
            raise CaptureHold("HOLD_CAPTURE_PARENT_SOURCE_HEAD_DRIFT_AFTER_CHILD")
        verify_runtime_generation(contract)
        verify_dotnet(contract)

        structural = load_structural_verifier()
        structural_report = structural.verify_evidence(
            evidence,
            expected_attempt_id=contract["attempt_id"],
            expected_controller_session_generation=contract[
                "controller_session_generation"
            ],
        )
        if structural_report.get("contract") != "GREEN":
            raise CaptureHold(
                "HOLD_CAPTURE_PARENT_STRUCTURAL_VERIFY:"
                + ",".join(structural_report.get("holds", []))
            )

        attempt_after = _read_attempt_ro(contract)
        if attempt_after != attempt_before:
            raise CaptureHold("HOLD_CAPTURE_ATTEMPT_CHANGED_AFTER_CHILD")

        source_head_before_publish = verify_source_generation(contract)
        if source_head_before_publish != source_head:
            raise CaptureHold("HOLD_CAPTURE_PARENT_SOURCE_HEAD_DRIFT_BEFORE_PUBLISH")
        verify_runtime_generation(contract)
        verify_dotnet(contract)

        downloads_fd, root_fd, root_path = _open_or_create_private_output_root(
            contract,
            state=state,
        )
        try:
            publication = publish_private_create_only(
                root_fd=root_fd,
                root_path=root_path,
                filename=contract["evidence_filename"],
                evidence=evidence,
                state=state,
            )
        finally:
            os.close(root_fd)
            os.close(downloads_fd)

        source_head_after_publish = verify_source_generation(contract)
        if source_head_after_publish != source_head:
            raise CaptureHold("HOLD_CAPTURE_PARENT_SOURCE_HEAD_DRIFT_AFTER_PUBLISH")
        verify_runtime_generation(contract)
        verify_dotnet(contract)
        final_attempt = _read_attempt_ro(contract)
        if final_attempt != attempt_before:
            raise CaptureHold("HOLD_CAPTURE_ATTEMPT_CHANGED_AFTER_PUBLISH")

        return {
            "marker": MARKER,
            "phase": "CAPTURED_PRIVATE_EVIDENCE",
            "source_head": source_head,
            "child_source_head": child_source_head,
            "source_head_revalidated_after_publish": source_head_after_publish,
            "attempt": final_attempt,
            "controller_decision_provenance": contract[
                "controller_decision_provenance"
            ],
            "controller_model_execution": False,
            "evidence": {
                "attempt_id": evidence["attempt_id"],
                "controller_session_generation": evidence[
                    "controller_session_generation"
                ],
                "world_tick": evidence["world_tick"],
                "joint_evidence_sha256": evidence["joint_evidence_sha256"],
            },
            "publication": publication,
            "runtime": runtime,
            "operation_state": state,
            "runtime_execution": True,
            "canonical_store_mutation": False,
            "private_key_access": False,
            "signing_action": False,
            "evidence_consumption": False,
            "session_advance": False,
            "service_action": False,
            "live_request_materialization": False,
        }
    except CaptureOperationHold:
        raise
    except CaptureHold as error:
        raise CaptureOperationHold(str(error), state=state) from error
    except Exception as error:
        raise CaptureOperationHold(
            f"HOLD_CAPTURE_UNEXPECTED:{type(error).__name__}",
            state=state,
        ) from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan")
    capture = sub.add_parser("capture")
    capture.add_argument("--confirm-capture", required=True)
    child = sub.add_parser("_capture-child")
    child.add_argument("--confirm-capture", required=True)
    args = parser.parse_args(argv)

    contract = load_contract()
    if args.command == "plan":
        report = plan_capture(contract)
    elif args.command == "_capture-child":
        report = capture_child(
            contract,
            confirmation=args.confirm_capture,
        )
    else:
        report = capture_runtime(
            contract,
            confirmation=args.confirm_capture,
        )
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CaptureOperationHold as error:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "phase": "HOLD",
                    "hold": str(error),
                    "operation_state": error.state,
                    "canonical_store_mutation": False,
                    "controller_model_execution": False,
                    "private_key_access": False,
                    "signing_action": False,
                    "evidence_consumption": False,
                    "session_advance": False,
                    "service_action": False,
                    "live_request_materialization": False,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        raise SystemExit(2)
    except CaptureHold as error:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "phase": "HOLD",
                    "hold": str(error),
                    "canonical_store_mutation": False,
                    "controller_model_execution": False,
                    "private_key_access": False,
                    "signing_action": False,
                    "evidence_consumption": False,
                    "session_advance": False,
                    "service_action": False,
                    "live_request_materialization": False,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        raise SystemExit(2)
