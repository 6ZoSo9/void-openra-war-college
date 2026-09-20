#!/usr/bin/env python3
"""Read-only operator admission for local OpenBW/Brood War game data.

The tool hashes only explicitly named files beneath an explicitly named game
root. It never scans for installations, copies assets, writes a receipt, starts
OpenBW/BWAPI, creates a socket, or grants runtime authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any

from openra_env.learning import openbw_neutral_duel_harness_v1 as harness

SCHEMA = harness.RUNTIME_ADMISSION_SCHEMA
CONFIRMATION = "VOID_OPENBW_LOCAL_GAME_DATA_RIGHTS_REVIEWED"
REQUIRED = ("Stardat.mpq", "Broodat.mpq", "Patch_rt.mpq")
MAX_MPQ_BYTES = 4 * 1024 * 1024 * 1024
MAX_MAP_BYTES = 256 * 1024 * 1024
READ_CHUNK_BYTES = 1024 * 1024


class OpenBWGameDataAdmissionHold(RuntimeError):
    pass


def _require(value: bool, code: str) -> None:
    if not value:
        raise OpenBWGameDataAdmissionHold(code)


def _split_relative(value: str) -> tuple[str, ...]:
    _require(type(value) is str and value != "", "relative_path_required")
    path = Path(value)
    _require(not path.is_absolute(), "absolute_relative_path_forbidden")
    parts = tuple(path.parts)
    _require(bool(parts), "relative_path_required")
    _require(all(part not in ("", ".", "..") for part in parts), "path_traversal_forbidden")
    return parts


def _open_directory_no_follow(parent_fd: int, name: str) -> int:
    flags = os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(name, flags, dir_fd=parent_fd)
    except OSError as exc:
        raise OpenBWGameDataAdmissionHold("directory_open_hold:" + name) from exc
    st = os.fstat(fd)
    if not stat.S_ISDIR(st.st_mode):
        os.close(fd)
        raise OpenBWGameDataAdmissionHold("directory_type_hold:" + name)
    return fd


def _open_file_beneath(root_fd: int, relative: str) -> tuple[int, tuple[int, ...]]:
    parts = _split_relative(relative)
    owned_dirs: list[int] = []
    current_fd = root_fd
    try:
        for part in parts[:-1]:
            next_fd = _open_directory_no_follow(current_fd, part)
            owned_dirs.append(next_fd)
            current_fd = next_fd
        flags = os.O_RDONLY | os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            file_fd = os.open(parts[-1], flags, dir_fd=current_fd)
        except OSError as exc:
            raise OpenBWGameDataAdmissionHold("file_open_hold:" + relative) from exc
        st = os.fstat(file_fd)
        if not stat.S_ISREG(st.st_mode):
            os.close(file_fd)
            raise OpenBWGameDataAdmissionHold("regular_file_required:" + relative)
        identity = (
            st.st_dev,
            st.st_ino,
            st.st_mode,
            st.st_nlink,
            st.st_uid,
            st.st_gid,
            st.st_size,
            st.st_mtime_ns,
            st.st_ctime_ns,
        )
        return file_fd, identity
    finally:
        for fd in reversed(owned_dirs):
            try:
                os.close(fd)
            except OSError:
                pass


def _hash_fd(fd: int, identity: tuple[int, ...], *, max_bytes: int, label: str) -> dict[str, Any]:
    size = identity[6]
    _require(0 < size <= max_bytes, "file_size_bound:" + label)
    digest = hashlib.sha256()
    read_total = 0
    while True:
        chunk = os.read(fd, READ_CHUNK_BYTES)
        if not chunk:
            break
        read_total += len(chunk)
        _require(read_total <= max_bytes, "read_size_bound:" + label)
        digest.update(chunk)
    _require(read_total == size, "short_or_changed_read:" + label)
    after = os.fstat(fd)
    after_identity = (
        after.st_dev,
        after.st_ino,
        after.st_mode,
        after.st_nlink,
        after.st_uid,
        after.st_gid,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    )
    _require(after_identity == identity, "file_identity_changed:" + label)
    return {"sha256": digest.hexdigest(), "bytes": size}


def admit_game_data(*, game_root: Path, map_relative: str, confirm: str) -> dict[str, Any]:
    _require(confirm == CONFIRMATION, "operator_rights_review_confirmation_required")
    _require(os.name == "posix" and hasattr(os, "O_CLOEXEC"), "posix_required")

    try:
        root_lstat = game_root.lstat()
    except OSError as exc:
        raise OpenBWGameDataAdmissionHold("game_root_missing") from exc
    _require(stat.S_ISDIR(root_lstat.st_mode), "game_root_directory_required")
    _require(not stat.S_ISLNK(root_lstat.st_mode), "game_root_symlink_forbidden")

    root_flags = os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY
    if hasattr(os, "O_NOFOLLOW"):
        root_flags |= os.O_NOFOLLOW
    try:
        root_fd = os.open(str(game_root), root_flags)
    except OSError as exc:
        raise OpenBWGameDataAdmissionHold("game_root_open_hold") from exc

    game_data: dict[str, str] = {}
    game_sizes: dict[str, int] = {}
    map_record: dict[str, Any] | None = None
    try:
        for name in REQUIRED:
            fd = None
            try:
                fd, identity = _open_file_beneath(root_fd, name)
                record = _hash_fd(fd, identity, max_bytes=MAX_MPQ_BYTES, label=name)
                game_data[name] = record["sha256"]
                game_sizes[name] = record["bytes"]
            finally:
                if fd is not None:
                    os.close(fd)

        map_fd = None
        try:
            map_fd, map_identity = _open_file_beneath(root_fd, map_relative)
            map_record = _hash_fd(
                map_fd,
                map_identity,
                max_bytes=MAX_MAP_BYTES,
                label="map",
            )
        finally:
            if map_fd is not None:
                os.close(map_fd)
    finally:
        os.close(root_fd)

    assert map_record is not None
    receipt = {
        "schema": SCHEMA,
        "record_kind": "read_only_local_asset_identity_not_execution_authority",
        "game_data_sha256": game_data,
        "game_data_bytes": game_sizes,
        "map_relative_path": map_relative,
        "map_sha256": map_record["sha256"],
        "map_bytes": map_record["bytes"],
        "license_or_ownership_reviewed_by_operator": True,
        "files_copied": False,
        "files_modified": False,
        "game_launched": False,
        "game_session_created": False,
        "runtime_authorized": False,
        "game_execution_authorized": False,
        "model_execution_authorized": False,
        "training_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "next_gate": "OPENBW_NEUTRAL_DUEL_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED",
    }
    admitted = harness.validate_future_runtime_admission(receipt)
    _require(admitted["runtime_authorized"] is False, "validator_runtime_authority_drift")
    _require(admitted["game_execution_authorized"] is False, "validator_game_authority_drift")
    return receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game-root", required=True)
    parser.add_argument("--map", required=True, dest="map_relative")
    parser.add_argument("--confirm", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = admit_game_data(
            game_root=Path(args.game_root),
            map_relative=args.map_relative,
            confirm=args.confirm,
        )
    except OpenBWGameDataAdmissionHold as exc:
        print(
            json.dumps(
                {
                    "schema": "void.war-college.openbw-game-data-admission-hold.v1",
                    "terminal": "HOLD",
                    "reason": str(exc),
                    "game_launched": False,
                    "runtime_authorized": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
