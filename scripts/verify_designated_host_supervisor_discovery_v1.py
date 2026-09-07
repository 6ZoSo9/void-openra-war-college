#!/usr/bin/env python3
"""Verify one read-only supervisor discovery report against the committed contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "war-college"
    / "designated-host-supervisor-v1.json"
)
DISCOVERY_MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_SUPERVISOR_DISCOVERY_V1"
CONTRACT_MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_SUPERVISOR_CONTRACT_V1"


class SupervisorContractError(ValueError):
    pass


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise SupervisorContractError("contract is not an object")
    required = {
        "marker",
        "version",
        "designated_host_label",
        "expected_node_id",
        "service_scope",
        "service_name",
        "runtime_uid",
        "runtime_gid",
        "runtime_repository",
        "runtime_source_commit",
        "runtime_artifact_git_blobs",
        "void_data_dir",
        "store_relative_path",
        "store_absolute_path",
        "artifact_policy",
        "authority",
        "observed_legacy_service_disposition",
    }
    if set(value) != required:
        raise SupervisorContractError("contract keys are not exact")
    if value["marker"] != CONTRACT_MARKER or value["version"] != 1:
        raise SupervisorContractError("contract marker/version mismatch")
    runtime_repository = Path(value["runtime_repository"])
    if not runtime_repository.is_absolute():
        raise SupervisorContractError("runtime repository is not absolute")
    if not Path(value["void_data_dir"]).is_absolute():
        raise SupervisorContractError("contract VOID_DATA_DIR is not absolute")
    if (
        str(Path(value["void_data_dir"]) / value["store_relative_path"])
        != value["store_absolute_path"]
    ):
        raise SupervisorContractError("contract store path is not derived from VOID_DATA_DIR")
    source_commit = value["runtime_source_commit"]
    if type(source_commit) is not str or len(source_commit) != 40:
        raise SupervisorContractError("runtime source commit is invalid")
    artifacts = value["runtime_artifact_git_blobs"]
    if type(artifacts) is not dict or not artifacts:
        raise SupervisorContractError("runtime artifact manifest is invalid")
    for path_text, blob in artifacts.items():
        if (
            type(path_text) is not str
            or not path_text
            or type(blob) is not str
            or len(blob) != 40
        ):
            raise SupervisorContractError("runtime artifact manifest entry is invalid")
    authority = value["authority"]
    if type(authority) is not dict or any(authority.values()):
        raise SupervisorContractError("contract accidentally grants authority")
    return value


def _artifact_holds(
    records: Any,
    *,
    label: str,
    expected_uid: int,
    expected_gid: int,
    require_mode: str | None = None,
) -> list[str]:
    holds: list[str] = []
    if type(records) is not list or not records:
        return [f"HOLD_{label}_MISSING"]
    for index, record in enumerate(records):
        prefix = f"{label}_{index}"
        if type(record) is not dict:
            holds.append(f"HOLD_{prefix}_INVALID")
            continue
        if record.get("exists") is not True:
            holds.append(f"HOLD_{prefix}_NOT_FOUND")
        if record.get("is_regular") is not True:
            holds.append(f"HOLD_{prefix}_NOT_REGULAR")
        if record.get("is_symlink") is not False:
            holds.append(f"HOLD_{prefix}_SYMLINK")
        if record.get("uid") != expected_uid or record.get("gid") != expected_gid:
            holds.append(f"HOLD_{prefix}_OWNER_MISMATCH")
        if record.get("group_or_other_writable") is not False:
            holds.append(f"HOLD_{prefix}_GROUP_OR_OTHER_WRITABLE")
        if require_mode is not None and record.get("mode") != require_mode:
            holds.append(f"HOLD_{prefix}_MODE_MISMATCH")
    return holds


def verify_discovery(
    report: Any,
    *,
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    c = contract or load_contract()
    holds: list[str] = []

    if type(report) is not dict:
        return {
            "contract": "HOLD",
            "holds": ["HOLD_DISCOVERY_NOT_OBJECT"],
            "supervisor_contract_green": False,
        }

    if report.get("marker") != DISCOVERY_MARKER:
        holds.append("HOLD_DISCOVERY_MARKER_MISMATCH")
    if report.get("schema_version") != 1:
        holds.append("HOLD_DISCOVERY_SCHEMA_MISMATCH")
    if report.get("service") != c["service_name"]:
        holds.append("HOLD_SUPERVISOR_SERVICE_NAME_MISMATCH")
    if report.get("active_state") != "active":
        holds.append("HOLD_SUPERVISOR_NOT_ACTIVE")
    sub_state = report.get("sub_state")
    if sub_state not in ("running", "exited"):
        holds.append("HOLD_SUPERVISOR_SUBSTATE_INVALID")

    main_pid = report.get("main_pid")
    process = report.get("process")
    if sub_state == "running":
        if type(main_pid) is not int or main_pid <= 0:
            holds.append("HOLD_SUPERVISOR_MAIN_PID_INVALID")
        if type(process) is not dict:
            holds.append("HOLD_SUPERVISOR_PROCESS_INVALID")
        else:
            if (
                process.get("uid") != c["runtime_uid"]
                or process.get("gid") != c["runtime_gid"]
            ):
                holds.append("HOLD_SUPERVISOR_PROCESS_OWNER_MISMATCH")
            if process.get("cwd") != c["runtime_repository"]:
                holds.append("HOLD_SUPERVISOR_RUNTIME_REPOSITORY_MISMATCH")
    elif sub_state == "exited":
        if main_pid != 0:
            holds.append("HOLD_SUPERVISOR_EXITED_MAIN_PID_NOT_ZERO")
        if process not in (None, {}):
            holds.append("HOLD_SUPERVISOR_EXITED_PROCESS_STILL_ASSERTED")

    if report.get("runtime_source_commit") != c["runtime_source_commit"]:
        holds.append("HOLD_RUNTIME_SOURCE_COMMIT_MISMATCH")
    if report.get("runtime_worktree_dirty") is not False:
        holds.append("HOLD_RUNTIME_WORKTREE_NOT_CLEAN")
    observed_blobs = report.get("runtime_artifact_git_blobs")
    if type(observed_blobs) is not dict:
        holds.append("HOLD_RUNTIME_ARTIFACT_MANIFEST_INVALID")
    elif observed_blobs != c["runtime_artifact_git_blobs"]:
        holds.append("HOLD_RUNTIME_ARTIFACT_BLOB_MISMATCH")

    runtime_data = report.get("runtime_void_data_dir")
    if type(runtime_data) is not dict:
        holds.append("HOLD_VOID_DATA_DIR_DISCOVERY_INVALID")
    else:
        if runtime_data.get("configured") is not True:
            holds.append("HOLD_VOID_DATA_DIR_NOT_CONFIGURED")
        if runtime_data.get("is_absolute") is not True:
            holds.append("HOLD_VOID_DATA_DIR_NOT_ABSOLUTE")
        if runtime_data.get("raw") != c["void_data_dir"]:
            holds.append("HOLD_VOID_DATA_DIR_RAW_MISMATCH")
        if runtime_data.get("resolved") != c["void_data_dir"]:
            holds.append("HOLD_VOID_DATA_DIR_RESOLVED_MISMATCH")

    data_artifact = report.get("resolved_void_data_dir_artifact")
    if type(data_artifact) is not dict:
        holds.append("HOLD_VOID_DATA_DIR_ARTIFACT_INVALID")
    else:
        if data_artifact.get("exists") is not True:
            holds.append("HOLD_VOID_DATA_DIR_NOT_FOUND")
        if data_artifact.get("is_directory") is not True:
            holds.append("HOLD_VOID_DATA_DIR_NOT_DIRECTORY")
        if data_artifact.get("is_symlink") is not False:
            holds.append("HOLD_VOID_DATA_DIR_SYMLINK")
        if data_artifact.get("uid") != c["runtime_uid"] or data_artifact.get("gid") != c["runtime_gid"]:
            holds.append("HOLD_VOID_DATA_DIR_OWNER_MISMATCH")
        if data_artifact.get("mode") != c["artifact_policy"]["data_dir_required_mode"]:
            holds.append("HOLD_VOID_DATA_DIR_MODE_MISMATCH")
        if data_artifact.get("group_or_other_writable") is not False:
            holds.append("HOLD_VOID_DATA_DIR_GROUP_OR_OTHER_WRITABLE")
        if data_artifact.get("path") != c["void_data_dir"]:
            holds.append("HOLD_VOID_DATA_DIR_PATH_MISMATCH")

    holds.extend(
        _artifact_holds(
            report.get("service_artifacts"),
            label="SERVICE_ARTIFACT",
            expected_uid=c["runtime_uid"],
            expected_gid=c["runtime_gid"],
        )
    )
    holds.extend(
        _artifact_holds(
            report.get("environment_file_artifacts"),
            label="ENVIRONMENT_ARTIFACT",
            expected_uid=c["runtime_uid"],
            expected_gid=c["runtime_gid"],
            require_mode=c["artifact_policy"]["environment_file_required_mode"],
        )
    )

    health = report.get("health_identity")
    if type(health) is not dict or health.get("matches_expected") is not True:
        holds.append("HOLD_DESIGNATED_NODE_HEALTH_IDENTITY_MISMATCH")
    elif health.get("node_id") != c["expected_node_id"]:
        holds.append("HOLD_DESIGNATED_NODE_ID_MISMATCH")

    for field, hold in (
        ("private_key_read", "HOLD_DISCOVERY_PRIVATE_KEY_READ"),
        ("full_process_environment_emitted", "HOLD_DISCOVERY_FULL_ENVIRONMENT_EMITTED"),
        ("environment_file_contents_emitted", "HOLD_DISCOVERY_ENVIRONMENT_CONTENTS_EMITTED"),
        ("mutation_performed", "HOLD_DISCOVERY_MUTATION_PERFORMED"),
        ("service_restart_performed", "HOLD_DISCOVERY_SERVICE_RESTART_PERFORMED"),
    ):
        if report.get(field) is not False:
            holds.append(hold)

    green = not holds
    return {
        "contract": "GREEN" if green else "HOLD",
        "holds": sorted(set(holds)),
        "supervisor_contract_green": green,
        "designated_host_label": c["designated_host_label"],
        "service_name": c["service_name"],
        "runtime_repository": c["runtime_repository"],
        "runtime_source_commit": c["runtime_source_commit"],
        "void_data_dir": c["void_data_dir"],
        "store_absolute_path": c["store_absolute_path"],
        "expected_node_id": c["expected_node_id"],
        "runtime_execution_authorized": False,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("discovery_report", type=Path)
    args = parser.parse_args(argv)
    try:
        report = json.loads(args.discovery_report.read_text(encoding="utf-8"))
        result = verify_discovery(report)
    except (OSError, json.JSONDecodeError, SupervisorContractError) as error:
        result = {
            "contract": "HOLD",
            "holds": [f"HOLD_SUPERVISOR_CONTRACT_FAILURE:{type(error).__name__}"],
            "supervisor_contract_green": False,
            "runtime_execution_authorized": False,
        }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["contract"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
