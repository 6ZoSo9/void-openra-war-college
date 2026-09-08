#!/usr/bin/env python3
"""Read-only designated-host installed execution-path preflight."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import verify_designated_host_execution_binding_v1 as execution

CONTRACT_PATH = ROOT / "config/war-college/designated-host-runtime-preflight-v1.json"
MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_RUNTIME_PREFLIGHT_V1"
SCHEMA_VERSION = 1
SYSTEMCTL = "/usr/bin/systemctl"
GIT = "/usr/bin/git"
SYSTEMD_PROBE_REQUEST_ID = "wcrq1_00000000000000000000000000000000"
SYSTEMD_PROBE_REQUEST_RE = re.compile(r"wcrq1_[0-9a-f]{32}\Z")


class RuntimePreflightError(ValueError):
    pass


def _git_dependency_identity(relative: Path) -> str:
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimePreflightError("dependency path is not repository-relative")
    rel = relative.as_posix()
    committed = subprocess.run(
        [GIT, "-C", str(ROOT), "rev-parse", f"HEAD:{rel}"],
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
    if committed.returncode != 0:
        raise RuntimePreflightError("dependency committed blob query failed")
    blob = committed.stdout.strip()
    if re.fullmatch(r"[0-9a-f]{40}", blob) is None:
        raise RuntimePreflightError("dependency committed blob identity invalid")
    clean = subprocess.run(
        [GIT, "-C", str(ROOT), "diff", "--quiet", "HEAD", "--", rel],
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
    if clean.returncode == 1:
        raise RuntimePreflightError("dependency working tree differs from HEAD")
    if clean.returncode != 0:
        raise RuntimePreflightError("dependency working-tree identity query failed")
    return blob


def load_preflight_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimePreflightError("preflight contract unreadable") from error
    if type(value) is not dict:
        raise RuntimePreflightError("preflight contract is not an object")
    if value.get("marker") != MARKER or value.get("version") != 1:
        raise RuntimePreflightError("preflight contract marker/version mismatch")
    for field in (
        "execution_binding_path",
        "execution_binding_git_blob",
        "execution_verifier_path",
        "execution_verifier_git_blob",
        "semantic_parent_head",
        "service_template_name",
    ):
        if type(value.get(field)) is not str or not value[field]:
            raise RuntimePreflightError(f"{field} invalid")
    for field in (
        "read_only",
        "private_key_access",
        "service_install_authorized",
        "daemon_reload_authorized",
        "service_start_authorized",
        "runtime_execution_authorized",
    ):
        if type(value.get(field)) is not bool:
            raise RuntimePreflightError(f"{field} must be boolean")
    if value["read_only"] is not True:
        raise RuntimePreflightError("preflight must be read-only")
    if any(
        value[field] is not False
        for field in (
            "private_key_access",
            "service_install_authorized",
            "daemon_reload_authorized",
            "service_start_authorized",
            "runtime_execution_authorized",
        )
    ):
        raise RuntimePreflightError("preflight contract accidentally grants authority")

    for path_field, blob_field in (
        ("execution_binding_path", "execution_binding_git_blob"),
        ("execution_verifier_path", "execution_verifier_git_blob"),
    ):
        relative = Path(value[path_field])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimePreflightError(f"{path_field} is not repository-relative")
        source = ROOT / relative
        if not source.is_file():
            raise RuntimePreflightError(f"{path_field} source file missing")
        if _git_dependency_identity(relative) != value[blob_field]:
            raise RuntimePreflightError(f"{path_field} Git blob mismatch")
    return value


def _sha256_descriptor(fd: int, maximum_bytes: int = 2 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    os.lseek(fd, 0, os.SEEK_SET)
    total = 0
    while True:
        chunk = os.read(fd, min(65536, maximum_bytes + 1 - total))
        if not chunk:
            break
        total += len(chunk)
        if total > maximum_bytes:
            raise RuntimePreflightError("installed artifact exceeds read bound")
        digest.update(chunk)
    return digest.hexdigest()


def artifact_record(path: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "path": str(path),
        "exists": False,
        "is_regular": False,
        "is_symlink": False,
        "uid": None,
        "gid": None,
        "mode": None,
        "group_or_other_writable": None,
        "sha256": None,
    }
    try:
        named = path.lstat()
    except FileNotFoundError:
        return record
    except OSError as error:
        record["read_error"] = f"{type(error).__name__}:{error}"
        return record

    record["exists"] = True
    record["is_symlink"] = stat.S_ISLNK(named.st_mode)
    record["uid"] = named.st_uid
    record["gid"] = named.st_gid
    record["mode"] = oct(stat.S_IMODE(named.st_mode))
    record["group_or_other_writable"] = bool(stat.S_IMODE(named.st_mode) & 0o022)
    if record["is_symlink"] or not stat.S_ISREG(named.st_mode):
        return record

    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except OSError as error:
        record["read_error"] = f"{type(error).__name__}:{error}"
        return record
    try:
        opened = os.fstat(fd)
        if not os.path.samestat(named, opened):
            record["read_error"] = "artifact_generation_changed"
            return record
        record["is_regular"] = stat.S_ISREG(opened.st_mode)
        record["sha256"] = _sha256_descriptor(fd) if record["is_regular"] else None
    except (OSError, RuntimePreflightError) as error:
        record["read_error"] = f"{type(error).__name__}:{error}"
    finally:
        os.close(fd)
    return record


def _systemd_probe_unit_name(service_template_name: str) -> str:
    if type(service_template_name) is not str or service_template_name.count("@.") != 1:
        raise RuntimePreflightError("service template name is not instantiable")
    if SYSTEMD_PROBE_REQUEST_RE.fullmatch(SYSTEMD_PROBE_REQUEST_ID) is None:
        raise RuntimePreflightError("systemd probe request id is invalid")
    return service_template_name.replace(
        "@.", f"@{SYSTEMD_PROBE_REQUEST_ID}.", 1
    )

def _systemd_user_bus_environment() -> dict[str, str]:
    uid = os.getuid()
    runtime_dir = Path("/run/user") / str(uid)
    return {
        "HOME": str(Path.home()),
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin",
        "XDG_RUNTIME_DIR": str(runtime_dir),
        "DBUS_SESSION_BUS_ADDRESS": f"unix:path={runtime_dir / 'bus'}",
    }


def _run_systemctl(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [SYSTEMCTL, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=_systemd_user_bus_environment(),
    )



def systemd_snapshot(
    service_template_name: str,
    *,
    run_command: Callable[[list[str]], subprocess.CompletedProcess[str]] = _run_systemctl,
) -> dict[str, Any]:
    probe_unit_name = _systemd_probe_unit_name(service_template_name)
    args = [
        "--user",
        "show",
        probe_unit_name,
        "--property=LoadState",
        "--property=FragmentPath",
        "--property=DropInPaths",
        "--property=NeedDaemonReload",
        "--no-pager",
    ]
    completed = run_command(args)
    if completed.returncode != 0:
        return {
            "probe_unit_name": probe_unit_name,
            "load_state": None,
            "fragment_path": None,
            "dropin_paths": None,
            "need_daemon_reload": None,
            "query_error": (
                f"systemctl_show_failed:{completed.returncode}:"
                f"{completed.stderr.strip()[:512]}"
            ),
        }

    properties: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            properties[key] = value
    raw_dropins = properties.get("DropInPaths", "")
    try:
        dropins = shlex.split(raw_dropins) if raw_dropins else []
    except ValueError:
        dropins = None
    raw_reload = properties.get("NeedDaemonReload")
    need_reload = False if raw_reload == "no" else True if raw_reload == "yes" else None
    return {
        "probe_unit_name": probe_unit_name,
        "load_state": properties.get("LoadState"),
        "fragment_path": properties.get("FragmentPath") or None,
        "dropin_paths": dropins,
        "need_daemon_reload": need_reload,
        "query_error": None,
    }



def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [GIT, "-C", str(repo), *args],
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


def runtime_snapshot(
    binding: dict[str, Any],
    *,
    run_git: Callable[..., subprocess.CompletedProcess[str]] = _run_git,
) -> dict[str, Any]:
    repo = Path(binding["working_directory"])
    result = {
        "runtime_source_commit": None,
        "runtime_worktree_dirty": True,
        "runtime_artifact_git_blobs": {},
        "runtime_query_error": None,
    }
    try:
        resolved = repo.resolve(strict=True)
    except OSError as error:
        result["runtime_query_error"] = f"runtime_repository_unavailable:{type(error).__name__}"
        return result
    if resolved != repo:
        result["runtime_query_error"] = "runtime_repository_symlinked"
        return result

    head = run_git(repo, "rev-parse", "HEAD")
    status_result = run_git(repo, "status", "--porcelain", "--untracked-files=all")
    if head.returncode != 0 or status_result.returncode != 0:
        result["runtime_query_error"] = "runtime_git_query_failed"
        return result

    blobs: dict[str, str] = {}
    for relative in sorted(binding["runtime_artifact_git_blobs"]):
        queried = run_git(repo, "rev-parse", f"HEAD:{relative}")
        if queried.returncode != 0:
            result["runtime_query_error"] = "runtime_blob_query_failed"
            return result
        blobs[relative] = queried.stdout.strip()

    result.update(
        {
            "runtime_source_commit": head.stdout.strip(),
            "runtime_worktree_dirty": bool(status_result.stdout.strip()),
            "runtime_artifact_git_blobs": blobs,
            "runtime_query_error": None,
        }
    )
    return result


def collect_discovery(
    binding: dict[str, Any],
    *,
    systemd_override: dict[str, Any] | None = None,
    runtime_override: dict[str, Any] | None = None,
    artifact_overrides: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    systemd = systemd_override if systemd_override is not None else systemd_snapshot(
        binding["service_template_name"]
    )
    runtime = runtime_override if runtime_override is not None else runtime_snapshot(binding)
    overrides = artifact_overrides or {}

    def artifact(label: str, path_key: str) -> dict[str, Any]:
        return overrides.get(label) or artifact_record(Path(binding[path_key]))

    return {
        "marker": execution.DISCOVERY_MARKER,
        "schema_version": 1,
        "service_template_name": binding["service_template_name"],
        "systemd_probe_unit_name": systemd.get("probe_unit_name"),
        "systemd_load_state": systemd.get("load_state"),
        "systemd_fragment_path": systemd.get("fragment_path"),
        "systemd_query_error": systemd.get("query_error"),
        "dropin_paths": systemd.get("dropin_paths"),
        "need_daemon_reload": systemd.get("need_daemon_reload"),
        "unit_artifact": artifact("unit_artifact", "installed_unit_path"),
        "environment_artifact": artifact(
            "environment_artifact", "installed_environment_path"
        ),
        "wrapper_artifact": artifact("wrapper_artifact", "installed_wrapper_path"),
        "working_directory": binding["working_directory"],
        "void_data_dir": binding["void_data_dir"],
        "runtime_source_commit": runtime.get("runtime_source_commit"),
        "runtime_worktree_dirty": runtime.get("runtime_worktree_dirty"),
        "runtime_artifact_git_blobs": runtime.get("runtime_artifact_git_blobs"),
        "runtime_query_error": runtime.get("runtime_query_error"),
        "private_key_read": False,
        "mutation_performed": False,
        "service_started": False,
    }


def run_preflight(
    binding: dict[str, Any],
    *,
    systemd_override: dict[str, Any] | None = None,
    runtime_override: dict[str, Any] | None = None,
    artifact_overrides: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    discovery = collect_discovery(
        binding,
        systemd_override=systemd_override,
        runtime_override=runtime_override,
        artifact_overrides=artifact_overrides,
    )
    verification = execution.verify_installed_binding(discovery, binding=binding)
    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "discovery": discovery,
        "verification": verification,
        "read_only": True,
        "private_key_access": False,
        "service_install_authorized": False,
        "daemon_reload_authorized": False,
        "service_start_authorized": False,
        "runtime_execution_authorized": False,
    }


def main(argv: list[str] | None = None) -> int:
    if argv:
        raise RuntimePreflightError("runtime preflight accepts no arguments")
    try:
        contract = load_preflight_contract()
        binding = execution.load_binding()
        if binding["service_template_name"] != contract["service_template_name"]:
            raise RuntimePreflightError("preflight/execution service template mismatch")
        report = run_preflight(binding)
    except (OSError, ValueError, RuntimePreflightError, execution.ExecutionBindingError) as error:
        report = {
            "marker": MARKER,
            "schema_version": SCHEMA_VERSION,
            "verification": {
                "contract": "HOLD",
                "holds": [f"HOLD_RUNTIME_PREFLIGHT_FAILURE:{type(error).__name__}"],
                "execution_path_bound": False,
            },
            "read_only": True,
            "private_key_access": False,
            "service_install_authorized": False,
            "daemon_reload_authorized": False,
            "service_start_authorized": False,
            "runtime_execution_authorized": False,
        }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report.get("verification", {}).get("contract") == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
