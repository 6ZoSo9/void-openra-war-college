#!/usr/bin/env python3
"""Generation-2 reconnect/controller-evidence capture wrapper.

This source-only child reuses the accepted PR #38 capture implementation while
binding a distinct generation-2 contract. It does not advance the durable
controller session itself. A future capture is valid only after session 2 is
already the current admitted successor of consumed session 1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import capture_designated_host_controller_evidence_v1 as base

CONTRACT_PATH = (
    ROOT
    / "config/war-college/"
    "designated-host-controller-evidence-capture-generation2-v1.json"
)
MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_CONTROLLER_EVIDENCE_CAPTURE_GENERATION2_TOOL_V1"
CHILD_MARKER = "VOID_WAR_COLLEGE_CONTROLLER_EVIDENCE_CAPTURE_GENERATION2_CHILD_V1"

EXPECTED_UID = 1000
EXPECTED_GID = 1000
EXPECTED_PARENT_HEAD = "eadc0b15876fdfe6cf021860f1d4b7b8697fb64e"
EXPECTED_PARENT_CAPTURE_BLOB = "99aa213459652959f2c1f5852659aa3a63b7cb59"
EXPECTED_PYPROJECT_BLOB = "6a32df4cab3e4198cee6ca426bea1e6ccb36533f"
EXPECTED_PREDECESSOR_GENERATION = 1
EXPECTED_GENERATION = 2
EXPECTED_PREDECESSOR_JOINT_SHA256 = (
    "486cb7e5ba1fe0718f1d418802f7c8a39540d36f233aa88c6b21da66bdd45d4a"
)
EXPECTED_PREDECESSOR_CONSUMPTION_SHA256 = (
    "a36298e79acc689fcbea3bbf9bd4626c5bf3c0ee270b36caa3809bda56130e16"
)
EXPECTED_GENERATION2_ADMISSION_SHA256 = (
    "5159b314633903133d82c2a21720108ec80e1a1c3d8d482675cac4e6a030e7d7"
)

_BASE_READ_ATTEMPT_RO = base._read_attempt_ro


class Generation2CaptureHold(base.CaptureHold):
    pass


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    return hashlib.sha256(raw).hexdigest()



def verify_capture_python(contract: dict[str, Any]) -> dict[str, str]:
    path = Path(contract["capture_python_path"])
    prefix = Path(contract["capture_python_prefix"])
    if (
        not path.exists()
        or not path.is_file()
        or not os.access(path, os.X_OK)
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CAPTURE_PYTHON_UNAVAILABLE")
    if path.parent.parent != prefix:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CAPTURE_PYTHON_PREFIX_PATH")

    cp = subprocess.run(
        [
            str(path),
            "-I",
            "-B",
            "-c",
            (
                "import json,sys;"
                f"sys.path.insert(0,{str(ROOT)!r});"
                "import grpc,google.protobuf;"
                "from openra_env.generated import rl_bridge_pb2,rl_bridge_pb2_grpc;"
                "import bench_joint_advance_core as bench;"
                "bench._runtime_modules();"
                "print(json.dumps({"
                "'python':sys.executable,"
                "'prefix':sys.prefix,"
                "'grpc':grpc.__version__,"
                "'protobuf':google.protobuf.__version__"
                "},sort_keys=True))"
            ),
        ],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": f"{path.parent}:/usr/bin:/bin",
        },
    )
    if cp.returncode != 0:
        raise Generation2CaptureHold(
            "HOLD_CAPTURE_G2_CAPTURE_PYTHON_RUNTIME_IMPORTS:"
            + cp.stderr.strip()
        )
    try:
        payload = json.loads(cp.stdout)
    except json.JSONDecodeError as error:
        raise Generation2CaptureHold(
            "HOLD_CAPTURE_G2_CAPTURE_PYTHON_PROBE_JSON"
        ) from error

    expected = {
        "python": str(path),
        "prefix": str(prefix),
        "grpc": contract["capture_grpc_version"],
        "protobuf": contract["capture_protobuf_version"],
    }
    if payload != expected:
        raise Generation2CaptureHold(
            "HOLD_CAPTURE_G2_CAPTURE_PYTHON_IDENTITY:"
            + json.dumps(payload, sort_keys=True)
        )
    return payload


def load_contract() -> dict[str, Any]:
    value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if value.get("marker") != (
        "VOID_WAR_COLLEGE_DESIGNATED_HOST_CONTROLLER_EVIDENCE_CAPTURE_GENERATION2_V1"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CONTRACT_MARKER")
    if value.get("version") != 1:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CONTRACT_VERSION")
    if (
        value.get("semantic_parent_pr") != 38
        or value.get("semantic_parent_head") != EXPECTED_PARENT_HEAD
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PARENT")
    if value.get("parent_capture_source_git_blob") != EXPECTED_PARENT_CAPTURE_BLOB:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PARENT_CAPTURE_BLOB")
    if value.get("predecessor_session_generation") != EXPECTED_PREDECESSOR_GENERATION:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PREDECESSOR_GENERATION")
    if value.get("controller_session_generation") != EXPECTED_GENERATION:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_SESSION_GENERATION")
    if (
        value.get("predecessor_joint_evidence_sha256")
        != EXPECTED_PREDECESSOR_JOINT_SHA256
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PREDECESSOR_JOINT_SHA")
    if (
        value.get("predecessor_consumption_sha256")
        != EXPECTED_PREDECESSOR_CONSUMPTION_SHA256
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PREDECESSOR_CONSUMPTION_SHA")
    if (
        value.get("expected_session_advance_receipt_sha256")
        != EXPECTED_GENERATION2_ADMISSION_SHA256
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_ADVANCE_RECEIPT_SHA")
    if value.get("evidence_filename") != (
        "war-college-ad1926569b12466c-001-s2-evidence.json"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_EVIDENCE_FILENAME")
    if value.get("explicit_capture_confirmation") != (
        "CAPTURE_GENERATION2_CONTROLLER_EVIDENCE"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CONFIRMATION")
    if value.get("source_import_strategy") != (
        "generation2_wrapper_parent_capture_reuse_v1"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_IMPORT_STRATEGY")
    if value.get("source_branch") != (
        "ren/designated-host-controller-evidence-capture-generation2-v1-20260908"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_SOURCE_BRANCH")
    if value.get("parent_capture_source_path") != (
        "scripts/capture_designated_host_controller_evidence_v1.py"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PARENT_CAPTURE_PATH")
    if value.get("store_schema_version") != 3:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_STORE_SCHEMA")
    if value.get("controller_player_bindings") != [
        {"controller_id": "apollyon", "player_id": "Multi0"},
        {"controller_id": "abaddon", "player_id": "Multi1"},
    ]:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CONTROLLER_BINDINGS")
    if value.get("controller_decision_provenance") != (
        "operator_bound_empty_action_profile_v1"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_DECISION_PROVENANCE")
    if value.get("controller_model_execution") is not False:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_MODEL_EXECUTION")
    if value.get("runtime_containment_strategy") != (
        "spawned_capture_child_private_process_group_v1"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CONTAINMENT")
    if value.get("private_publish_strategy") != (
        "retained_output_directory_fd_o_excl_v1"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PRIVATE_PUBLISH")
    if value.get("action_profile") != "empty_joint_batches":
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_ACTION_PROFILE")
    if value.get("bootstrap_ticks") != 1 or value.get("action_ticks") != 1:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_TICK_SHAPE")
    if value.get("dotnet_version") != "8.0.424":
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_DOTNET_VERSION")
    if value.get("capture_python_strategy") != "dedicated_capture_runtime_v1":
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CAPTURE_PYTHON_STRATEGY")
    if value.get("capture_python_path") != (
        "/home/zoso/Downloads/void-war-college-capture-runtime-v1/bin/python"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CAPTURE_PYTHON_PATH")
    if value.get("capture_python_prefix") != (
        "/home/zoso/Downloads/void-war-college-capture-runtime-v1"
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CAPTURE_PYTHON_PREFIX")
    if value.get("capture_grpc_version") != "1.75.1":
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_GRPC_VERSION")
    if value.get("capture_protobuf_version") != "6.31.1":
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PROTOBUF_VERSION")
    for field in (
        "ready_timeout_s",
        "rpc_timeout_s",
        "teardown_timeout_s",
        "capture_outer_timeout_s",
        "runtime_retirement_signal_grace_s",
    ):
        if type(value.get(field)) is not int or value[field] <= 0:
            raise Generation2CaptureHold(f"HOLD_CAPTURE_G2_TIMEOUT:{field}")
    bound = value.get("bound_source_git_blobs")
    if type(bound) is not dict:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_BOUND_SOURCE_BLOBS")
    if (
        bound.get("scripts/capture_designated_host_controller_evidence_v1.py")
        != EXPECTED_PARENT_CAPTURE_BLOB
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_BOUND_PARENT_CAPTURE_BLOB")
    if bound.get("pyproject.toml") != EXPECTED_PYPROJECT_BLOB:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_BOUND_PYPROJECT_BLOB")

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
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_SOURCE_AUTHORITY")
    operation = value.get("capture_operation")
    if type(operation) is not dict:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_OPERATION")
    for field in (
        "requires_separate_runtime_authorization",
        "requires_exact_confirmation",
        "requires_generation2_current",
        "requires_predecessor_consumed_exactly_once",
        "creates_private_evidence_only",
        "canonical_store_read_only",
    ):
        if operation.get(field) is not True:
            raise Generation2CaptureHold(f"HOLD_CAPTURE_G2_OPERATION:{field}")
    for field in (
        "controller_model_execution",
        "signing",
        "evidence_consumption",
        "session_advance",
        "service_action",
        "live_request_materialization",
    ):
        if operation.get(field) is not False:
            raise Generation2CaptureHold(f"HOLD_CAPTURE_G2_OPERATION:{field}")

    receipt_payload = {
        "attempt_id": value["attempt_id"],
        "controller_a_id": value["controller_player_bindings"][0]["controller_id"],
        "controller_a_player_id": value["controller_player_bindings"][0]["player_id"],
        "controller_b_id": value["controller_player_bindings"][1]["controller_id"],
        "controller_b_player_id": value["controller_player_bindings"][1]["player_id"],
        "engine_commit": value["engine_commit"],
        "producer_id": value["producer_node_id"],
        "producer_public_key_sha256": value["producer_public_key_sha256"],
        "schema_version": value["store_schema_version"],
        "session_generation": EXPECTED_GENERATION,
        "source_generation": value["source_generation"],
        "war_college_commit": value["store_war_college_source_base"],
    }
    if canonical_sha256(receipt_payload) != EXPECTED_GENERATION2_ADMISSION_SHA256:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_ADVANCE_RECEIPT_REDERIVATION")
    return value


def _read_attempt_generation2_ro(contract: dict[str, Any]) -> dict[str, Any]:
    current = _BASE_READ_ATTEMPT_RO(contract)
    path = Path(contract["store_path"])
    before = path.lstat()
    try:
        db = sqlite3.connect(
            f"file:{path}?mode=ro",
            uri=True,
            timeout=5.0,
            isolation_level=None,
        )
    except sqlite3.Error as error:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_STORE_OPEN_RO") from error
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA query_only=ON")
        predecessor = db.execute(
            """
            SELECT session_generation, predecessor_generation
            FROM sessions
            WHERE attempt_id=? AND session_generation=?
            """,
            (
                contract["attempt_id"],
                contract["predecessor_session_generation"],
            ),
        ).fetchone()
        current_session = db.execute(
            """
            SELECT session_generation, predecessor_generation
            FROM sessions
            WHERE attempt_id=? AND session_generation=?
            """,
            (
                contract["attempt_id"],
                contract["controller_session_generation"],
            ),
        ).fetchone()
        predecessor_consumptions = db.execute(
            """
            SELECT *
            FROM consumptions
            WHERE attempt_id=? AND session_generation=?
            ORDER BY joint_evidence_sha256
            """,
            (
                contract["attempt_id"],
                contract["predecessor_session_generation"],
            ),
        ).fetchall()
    finally:
        db.close()

    after = path.lstat()
    identity = lambda st: (
        st.st_dev,
        st.st_ino,
        st.st_size,
        st.st_mtime_ns,
        st.st_ctime_ns,
        stat.S_IMODE(st.st_mode),
        st.st_uid,
        st.st_gid,
    )
    if identity(before) != identity(after):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_STORE_CHANGED_DURING_RO_READ")
    if predecessor is None:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PREDECESSOR_SESSION_MISSING")
    if (
        int(predecessor["session_generation"]) != EXPECTED_PREDECESSOR_GENERATION
        or predecessor["predecessor_generation"] is not None
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PREDECESSOR_SESSION_DRIFT")
    if current_session is None:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_CURRENT_SESSION_MISSING")
    if (
        int(current_session["session_generation"]) != EXPECTED_GENERATION
        or int(current_session["predecessor_generation"])
        != EXPECTED_PREDECESSOR_GENERATION
    ):
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_SUCCESSOR_LINK_DRIFT")
    if len(predecessor_consumptions) != 1:
        raise Generation2CaptureHold("HOLD_CAPTURE_G2_PREDECESSOR_CONSUMPTION_COUNT")

    consumed = dict(predecessor_consumptions[0])
    expected = {
        "attempt_id": contract["attempt_id"],
        "session_generation": EXPECTED_PREDECESSOR_GENERATION,
        "joint_evidence_sha256": EXPECTED_PREDECESSOR_JOINT_SHA256,
        "producer_id": contract["producer_node_id"],
        "producer_public_key_sha256": contract["producer_public_key_sha256"],
        "controller_a_id": contract["controller_player_bindings"][0]["controller_id"],
        "controller_a_player_id": contract["controller_player_bindings"][0]["player_id"],
        "controller_b_id": contract["controller_player_bindings"][1]["controller_id"],
        "controller_b_player_id": contract["controller_player_bindings"][1]["player_id"],
        "consumption_sha256": EXPECTED_PREDECESSOR_CONSUMPTION_SHA256,
    }
    for key, expected_value in expected.items():
        if consumed.get(key) != expected_value:
            raise Generation2CaptureHold(
                f"HOLD_CAPTURE_G2_PREDECESSOR_CONSUMPTION_DRIFT:{key}"
            )
    return {
        **current,
        "predecessor_session_generation": EXPECTED_PREDECESSOR_GENERATION,
        "predecessor_consumption_count": 1,
        "predecessor_joint_evidence_sha256": EXPECTED_PREDECESSOR_JOINT_SHA256,
        "predecessor_consumption_sha256": EXPECTED_PREDECESSOR_CONSUMPTION_SHA256,
        "successor_predecessor_generation": EXPECTED_PREDECESSOR_GENERATION,
        "expected_session_advance_receipt_sha256":
            EXPECTED_GENERATION2_ADMISSION_SHA256,
    }


def _generation2_runtime_child_command(
    contract: dict[str, Any],
    confirmation: str,
) -> list[str]:
    return [
        contract["capture_python_path"],
        "-I",
        "-B",
        str(Path(__file__).resolve()),
        "_capture-child",
        "--confirm-capture",
        confirmation,
    ]


base.MARKER = MARKER
base.CHILD_MARKER = CHILD_MARKER
base._read_attempt_ro = _read_attempt_generation2_ro
base._runtime_child_command = _generation2_runtime_child_command


def plan_capture(contract: dict[str, Any]) -> dict[str, Any]:
    report = base.plan_capture(contract)
    return {
        **report,
        "marker": MARKER,
        "capture_generation": EXPECTED_GENERATION,
        "capture_python_path": contract["capture_python_path"],
        "capture_grpc_version": contract["capture_grpc_version"],
        "capture_protobuf_version": contract["capture_protobuf_version"],
        "predecessor_session_generation": EXPECTED_PREDECESSOR_GENERATION,
        "predecessor_consumption_bound": True,
        "expected_session_advance_receipt_sha256":
            EXPECTED_GENERATION2_ADMISSION_SHA256,
    }


def capture_child(
    contract: dict[str, Any],
    *,
    confirmation: str,
) -> dict[str, Any]:
    if confirmation != contract["explicit_capture_confirmation"]:
        return base.capture_child(contract, confirmation=confirmation)
    verify_capture_python(contract)
    return base.capture_child(contract, confirmation=confirmation)


def capture_runtime(
    contract: dict[str, Any],
    *,
    confirmation: str,
) -> dict[str, Any]:
    if confirmation != contract["explicit_capture_confirmation"]:
        return base.capture_runtime(contract, confirmation=confirmation)
    verify_capture_python(contract)
    return base.capture_runtime(contract, confirmation=confirmation)


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
    except base.CaptureOperationHold as error:
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
    except base.CaptureHold as error:
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
