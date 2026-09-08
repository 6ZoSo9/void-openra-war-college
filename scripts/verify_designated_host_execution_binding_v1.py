#!/usr/bin/env python3
"""Verify exact installed systemd execution-path artifacts without starting them."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BINDING_PATH = ROOT / "config/war-college/designated-host-execution-binding-v1.json"
MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_EXECUTION_BINDING_V1"
DISCOVERY_MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_EXECUTION_BINDING_DISCOVERY_V1"


class ExecutionBindingError(ValueError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob_sha1(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def load_binding(path: Path = BINDING_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ExecutionBindingError("binding is not an object")
    if value.get("marker") != MARKER or value.get("version") != 1:
        raise ExecutionBindingError("binding marker/version mismatch")
    for key in (
        "source_unit_path",
        "source_environment_path",
        "source_wrapper_path",
        "supervisor_contract_path",
        "supervisor_contract_git_blob",
        "installed_unit_path",
        "installed_environment_path",
        "installed_wrapper_path",
        "working_directory",
        "void_data_dir",
    ):
        raw = value.get(key)
        if type(raw) is not str or not raw:
            raise ExecutionBindingError(f"{key} invalid")
    for key in (
        "installed_unit_path",
        "installed_environment_path",
        "installed_wrapper_path",
        "working_directory",
        "void_data_dir",
    ):
        if not Path(value[key]).is_absolute():
            raise ExecutionBindingError(f"{key} is not absolute")
    if value.get("dropins_allowed") != []:
        raise ExecutionBindingError("drop-ins are not closed")
    if value.get("need_daemon_reload_required") is not False:
        raise ExecutionBindingError("daemon-reload requirement invalid")
    if any(
        value.get(key) is not False
        for key in (
            "service_install_authorized",
            "service_start_authorized",
            "runtime_execution_authorized",
        )
    ):
        raise ExecutionBindingError("source binding accidentally grants runtime authority")

    supervisor_relative = Path(value["supervisor_contract_path"])
    if supervisor_relative.is_absolute() or ".." in supervisor_relative.parts:
        raise ExecutionBindingError("supervisor contract path is not repository-relative")
    source_supervisor = ROOT / supervisor_relative
    if _git_blob_sha1(source_supervisor) != value.get("supervisor_contract_git_blob"):
        raise ExecutionBindingError("supervisor contract Git blob mismatch")
    try:
        supervisor_contract = json.loads(
            source_supervisor.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as error:
        raise ExecutionBindingError("supervisor contract unreadable") from error
    if supervisor_contract.get("service_name") != value.get("service_template_name"):
        raise ExecutionBindingError("supervisor/execution service template mismatch")
    if (
        supervisor_contract.get("service_instance_id_regex")
        != value.get("request_id_regex")
    ):
        raise ExecutionBindingError("supervisor/execution request id mismatch")

    source_unit = ROOT / value["source_unit_path"]
    source_env = ROOT / value["source_environment_path"]
    source_wrapper = ROOT / value["source_wrapper_path"]
    if _sha256(source_unit) != value.get("unit_sha256"):
        raise ExecutionBindingError("source unit SHA mismatch")
    if _sha256(source_env) != value.get("environment_sha256"):
        raise ExecutionBindingError("source environment SHA mismatch")
    if _sha256(source_wrapper) != value.get("wrapper_sha256"):
        raise ExecutionBindingError("source wrapper SHA mismatch")

    unit_text = source_unit.read_text(encoding="utf-8")
    unit_lines = unit_text.splitlines()
    exact_exec = value.get("exec_start_line")
    if type(exact_exec) is not str or unit_lines.count(exact_exec) != 1:
        raise ExecutionBindingError("exact ExecStart line mismatch")
    if "[Install]" in unit_text:
        raise ExecutionBindingError("source service unexpectedly has an Install section")

    # This verifier is a user-manager service. PrivateDevices= implicitly
    # rewrites the capability bounding set (including CAP_MKNOD/CAP_SYS_RAWIO)
    # and is not executable on the designated host's unprivileged user manager.
    # Keep the remaining sandbox contract explicit while forbidding that
    # incompatible capability mutation.
    if any(line.startswith("PrivateDevices=") for line in unit_lines):
        raise ExecutionBindingError(
            "source service uses unsupported PrivateDevices in user manager"
        )
    for hardening_line in (
        "UMask=0077",
        "NoNewPrivileges=true",
        "PrivateTmp=true",
        "ProtectSystem=strict",
        "ProtectHome=read-only",
        "ReadWritePaths=/home/zoso/dev/void-node/data_a/war_college",
        "LockPersonality=true",
        "MemoryDenyWriteExecute=true",
        "RestrictSUIDSGID=true",
        "RestrictAddressFamilies=AF_UNIX",
    ):
        if unit_lines.count(hardening_line) != 1:
            raise ExecutionBindingError(
                "required source service hardening line mismatch"
            )
    return value


def _artifact_holds(
    record: Any,
    *,
    prefix: str,
    expected_path: str,
    expected_sha256: str,
    expected_mode: str,
) -> list[str]:
    if type(record) is not dict:
        return [f"HOLD_{prefix}_INVALID"]
    holds: list[str] = []
    if record.get("path") != expected_path:
        holds.append(f"HOLD_{prefix}_PATH_MISMATCH")
    if record.get("exists") is not True:
        holds.append(f"HOLD_{prefix}_NOT_FOUND")
    if record.get("is_regular") is not True:
        holds.append(f"HOLD_{prefix}_NOT_REGULAR")
    if record.get("is_symlink") is not False:
        holds.append(f"HOLD_{prefix}_SYMLINK")
    if record.get("uid") != 1000 or record.get("gid") != 1000:
        holds.append(f"HOLD_{prefix}_OWNER_MISMATCH")
    if record.get("mode") != expected_mode:
        holds.append(f"HOLD_{prefix}_MODE_MISMATCH")
    if record.get("group_or_other_writable") is not False:
        holds.append(f"HOLD_{prefix}_GROUP_OR_OTHER_WRITABLE")
    if record.get("sha256") != expected_sha256:
        holds.append(f"HOLD_{prefix}_SHA256_MISMATCH")
    return holds


def verify_installed_binding(
    report: Any,
    *,
    binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    b = binding or load_binding()
    holds: list[str] = []
    if type(report) is not dict:
        return {
            "contract": "HOLD",
            "holds": ["HOLD_EXECUTION_BINDING_DISCOVERY_NOT_OBJECT"],
            "execution_path_bound": False,
        }
    if report.get("marker") != DISCOVERY_MARKER:
        holds.append("HOLD_EXECUTION_BINDING_DISCOVERY_MARKER_MISMATCH")
    if report.get("schema_version") != 1:
        holds.append("HOLD_EXECUTION_BINDING_DISCOVERY_SCHEMA_MISMATCH")
    if report.get("service_template_name") != b["service_template_name"]:
        holds.append("HOLD_SERVICE_TEMPLATE_NAME_MISMATCH")
    if report.get("systemd_query_error") is not None:
        holds.append("HOLD_SERVICE_QUERY_ERROR")
    if report.get("systemd_load_state") != "loaded":
        holds.append("HOLD_SERVICE_NOT_LOADED")
    if report.get("systemd_fragment_path") != b["installed_unit_path"]:
        holds.append("HOLD_SERVICE_FRAGMENT_PATH_MISMATCH")
    if report.get("dropin_paths") != []:
        holds.append("HOLD_SERVICE_DROPINS_PRESENT")
    if report.get("need_daemon_reload") is not False:
        holds.append("HOLD_SERVICE_DAEMON_RELOAD_REQUIRED")

    holds.extend(
        _artifact_holds(
            report.get("unit_artifact"),
            prefix="UNIT_ARTIFACT",
            expected_path=b["installed_unit_path"],
            expected_sha256=b["unit_sha256"],
            expected_mode=b["unit_required_mode"],
        )
    )
    holds.extend(
        _artifact_holds(
            report.get("environment_artifact"),
            prefix="ENVIRONMENT_ARTIFACT",
            expected_path=b["installed_environment_path"],
            expected_sha256=b["environment_sha256"],
            expected_mode=b["environment_required_mode"],
        )
    )
    holds.extend(
        _artifact_holds(
            report.get("wrapper_artifact"),
            prefix="WRAPPER_ARTIFACT",
            expected_path=b["installed_wrapper_path"],
            expected_sha256=b["wrapper_sha256"],
            expected_mode=b["wrapper_required_mode"],
        )
    )

    if report.get("working_directory") != b["working_directory"]:
        holds.append("HOLD_EXECUTION_WORKING_DIRECTORY_MISMATCH")
    if report.get("void_data_dir") != b["void_data_dir"]:
        holds.append("HOLD_EXECUTION_VOID_DATA_DIR_MISMATCH")
    if report.get("runtime_source_commit") != b["runtime_source_commit"]:
        holds.append("HOLD_EXECUTION_RUNTIME_SOURCE_COMMIT_MISMATCH")
    if report.get("runtime_worktree_dirty") is not False:
        holds.append("HOLD_EXECUTION_RUNTIME_WORKTREE_NOT_CLEAN")
    if report.get("runtime_artifact_git_blobs") != b["runtime_artifact_git_blobs"]:
        holds.append("HOLD_EXECUTION_RUNTIME_ARTIFACT_BLOB_MISMATCH")

    for field, hold in (
        ("private_key_read", "HOLD_EXECUTION_DISCOVERY_PRIVATE_KEY_READ"),
        ("mutation_performed", "HOLD_EXECUTION_DISCOVERY_MUTATION_PERFORMED"),
        ("service_started", "HOLD_EXECUTION_DISCOVERY_SERVICE_STARTED"),
    ):
        if report.get(field) is not False:
            holds.append(hold)

    green = not holds
    return {
        "contract": "GREEN" if green else "HOLD",
        "holds": sorted(set(holds)),
        "execution_path_bound": green,
        "service_template_name": b["service_template_name"],
        "exec_start_line": b["exec_start_line"],
        "runtime_execution_authorized": False,
        "runtime_evidence": "PENDING_DESIGNATED_HOST",
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("discovery_report", type=Path)
    args = parser.parse_args(argv)
    try:
        report = json.loads(args.discovery_report.read_text(encoding="utf-8"))
        result = verify_installed_binding(report)
    except (OSError, json.JSONDecodeError, ExecutionBindingError) as error:
        result = {
            "contract": "HOLD",
            "holds": [f"HOLD_EXECUTION_BINDING_FAILURE:{type(error).__name__}"],
            "execution_path_bound": False,
            "runtime_execution_authorized": False,
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
        }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["contract"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
