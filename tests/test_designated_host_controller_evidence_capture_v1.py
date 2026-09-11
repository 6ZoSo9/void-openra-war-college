#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/capture_designated_host_controller_evidence_v1.py"
SPEC = importlib.util.spec_from_file_location("controller_capture_tool", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

STRUCTURAL_SPEC = importlib.util.spec_from_file_location(
    "controller_structural",
    ROOT / "scripts/verify_controller_evidence_isolation_v1.py",
)
assert STRUCTURAL_SPEC is not None and STRUCTURAL_SPEC.loader is not None
structural = importlib.util.module_from_spec(STRUCTURAL_SPEC)
STRUCTURAL_SPEC.loader.exec_module(structural)


def actor(actor_id: int, owner: str):
    return SimpleNamespace(actor_id=actor_id, owner=owner)


def observation(player: str, tick: int, offset: int):
    enemy = "Multi1" if player == "Multi0" else "Multi0"
    return SimpleNamespace(
        tick=tick,
        units=[actor(offset + 1, player), actor(offset + 2, player)],
        buildings=[actor(offset + 100, player)],
        visible_enemies=[actor(offset + 1000, enemy)],
        visible_enemy_buildings=[actor(offset + 1100, enemy)],
        available_production=["e1", "powr"],
        production=[SimpleNamespace(item="powr")],
    )


def response(session_id: str, start: int, end: int):
    return SimpleNamespace(
        session_id=session_id,
        start_tick=start,
        end_tick=end,
        player_observations=[
            SimpleNamespace(
                player="Multi0",
                observation=observation("Multi0", end, 10000),
            ),
            SimpleNamespace(
                player="Multi1",
                observation=observation("Multi1", end, 20000),
            ),
        ],
    )


class ControllerEvidenceCaptureTests(unittest.TestCase):
    def setUp(self):
        self.contract = tool.load_contract()

    def test_source_lane_authority_is_non_runtime_and_non_model(self):
        self.assertEqual(
            self.contract["source_lane_authority"],
            {
                "canonical_store_mutation": False,
                "controller_model_execution": False,
                "evidence_consumption": False,
                "live_request_materialization": False,
                "private_key_access": False,
                "runtime_execution": False,
                "service_action": False,
                "session_advance": False,
                "signing": False,
            },
        )
        self.assertEqual(
            self.contract["controller_decision_provenance"],
            "operator_bound_empty_action_profile_v1",
        )
        self.assertFalse(self.contract["controller_model_execution"])

    def test_builds_structurally_green_causal_evidence(self):
        evidence = tool.build_causal_evidence(
            bootstrap_response=response("session-a", 40, 41),
            action_response=response("session-a", 41, 42),
            expected_session_id="session-a",
            contract=self.contract,
            structural=structural,
        )
        report = structural.verify_evidence(
            evidence,
            expected_attempt_id=self.contract["attempt_id"],
            expected_controller_session_generation=1,
        )
        self.assertEqual(report["contract"], "GREEN")
        self.assertEqual(report["checked_players"], ["Multi0", "Multi1"])
        self.assertEqual(evidence["world_tick"], 41)
        for record in evidence["controllers"]:
            self.assertEqual(record["action_payload"]["commands"], [])
            self.assertEqual(
                record["action_payload"]["decision_observation_binding_sha256"],
                record["observation_binding_sha256"],
            )

    def test_rejects_retroactive_action_tick(self):
        with self.assertRaisesRegex(
            tool.CaptureHold,
            "HOLD_CAPTURE_CAUSAL_ACTION_START_TICK",
        ):
            tool.build_causal_evidence(
                bootstrap_response=response("session-a", 40, 41),
                action_response=response("session-a", 42, 43),
                expected_session_id="session-a",
                contract=self.contract,
                structural=structural,
            )

    def test_rejects_observation_not_at_bootstrap_end_tick(self):
        bootstrap = response("session-a", 40, 41)
        bootstrap.player_observations[0].observation.tick = 40
        with self.assertRaisesRegex(
            tool.CaptureHold,
            "HOLD_CAPTURE_OBSERVATION_TICK_MISMATCH",
        ):
            tool.build_causal_evidence(
                bootstrap_response=bootstrap,
                action_response=response("session-a", 41, 42),
                expected_session_id="session-a",
                contract=self.contract,
                structural=structural,
            )

    def test_rejects_wrong_own_actor_owner(self):
        bootstrap = response("session-a", 40, 41)
        bootstrap.player_observations[0].observation.units[0].owner = "Multi1"
        with self.assertRaisesRegex(
            tool.CaptureHold,
            "HOLD_CAPTURE_OWN_ACTOR_OWNER_MISMATCH",
        ):
            tool.build_causal_evidence(
                bootstrap_response=bootstrap,
                action_response=response("session-a", 41, 42),
                expected_session_id="session-a",
                contract=self.contract,
                structural=structural,
            )

    def test_private_publication_is_descriptor_bound_create_only_0400(self):
        evidence = tool.build_causal_evidence(
            bootstrap_response=response("session-a", 40, 41),
            action_response=response("session-a", 41, 42),
            expected_session_id="session-a",
            contract=self.contract,
            structural=structural,
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            state = tool._new_state()
            try:
                receipt = tool.publish_private_create_only(
                    root_fd=root_fd,
                    root_path=root,
                    filename="evidence.json",
                    evidence=evidence,
                    state=state,
                )
                self.assertTrue(receipt["descriptor_bound_parent"])
                self.assertTrue(state["private_evidence_created"])
                path = root / "evidence.json"
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o400)
                before = path.read_bytes()
                with self.assertRaisesRegex(
                    tool.CaptureHold,
                    "HOLD_CAPTURE_EVIDENCE_ALREADY_EXISTS",
                ):
                    tool.publish_private_create_only(
                        root_fd=root_fd,
                        root_path=root,
                        filename="evidence.json",
                        evidence=evidence,
                        state=state,
                    )
                self.assertEqual(path.read_bytes(), before)
            finally:
                os.close(root_fd)

    def test_private_directory_substitution_is_detected_without_retargeting(self):
        evidence = tool.build_causal_evidence(
            bootstrap_response=response("session-a", 40, 41),
            action_response=response("session-a", 41, 42),
            expected_session_id="session-a",
            contract=self.contract,
            structural=structural,
        )
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "root"
            moved = parent / "moved"
            root.mkdir()
            root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            state = tool._new_state()
            real_fsync = os.fsync
            calls = {"n": 0}

            def substituting_fsync(fd):
                calls["n"] += 1
                if calls["n"] == 1:
                    os.rename(root, moved)
                    root.mkdir()
                return real_fsync(fd)

            try:
                with mock.patch.object(tool.os, "fsync", side_effect=substituting_fsync):
                    with self.assertRaisesRegex(
                        tool.CaptureHold,
                        "HOLD_CAPTURE_PRIVATE_OUTPUT_ROOT_PATH_IDENTITY",
                    ):
                        tool.publish_private_create_only(
                            root_fd=root_fd,
                            root_path=root,
                            filename="evidence.json",
                            evidence=evidence,
                            state=state,
                        )
                self.assertTrue(state["private_evidence_created"])
                self.assertFalse((root / "evidence.json").exists())
                self.assertTrue((moved / "evidence.json").is_file())
            finally:
                os.close(root_fd)

    def test_read_attempt_ro_does_not_change_store(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "store.sqlite3"
            db = sqlite3.connect(path)
            try:
                db.executescript(
                    """
                    CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    INSERT INTO metadata VALUES('schema_version','3');
                    CREATE TABLE attempts(
                      attempt_id TEXT PRIMARY KEY,
                      producer_id TEXT NOT NULL,
                      producer_public_key_sha256 TEXT NOT NULL,
                      controller_a_id TEXT NOT NULL,
                      controller_a_player_id TEXT NOT NULL,
                      controller_b_id TEXT NOT NULL,
                      controller_b_player_id TEXT NOT NULL,
                      source_generation TEXT NOT NULL,
                      war_college_commit TEXT NOT NULL,
                      engine_commit TEXT NOT NULL,
                      current_session_generation INTEGER NOT NULL
                    );
                    CREATE TABLE sessions(
                      attempt_id TEXT NOT NULL,
                      session_generation INTEGER NOT NULL,
                      predecessor_generation INTEGER
                    );
                    CREATE TABLE consumptions(
                      attempt_id TEXT NOT NULL,
                      session_generation INTEGER NOT NULL
                    );
                    """
                )
                db.execute(
                    "INSERT INTO attempts VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.contract["attempt_id"],
                        self.contract["producer_node_id"],
                        self.contract["producer_public_key_sha256"],
                        "apollyon",
                        "Multi0",
                        "abaddon",
                        "Multi1",
                        self.contract["source_generation"],
                        self.contract["store_war_college_source_base"],
                        self.contract["engine_commit"],
                        1,
                    ),
                )
                db.execute(
                    "INSERT INTO sessions VALUES(?,?,NULL)",
                    (self.contract["attempt_id"], 1),
                )
                db.commit()
            finally:
                db.close()
            os.chmod(path, 0o600)
            before = path.stat()
            contract = dict(self.contract)
            contract["store_path"] = str(path)
            with mock.patch.object(tool, "EXPECTED_UID", os.getuid()), mock.patch.object(
                tool, "EXPECTED_GID", os.getgid()
            ):
                result = tool._read_attempt_ro(contract)
            after = path.stat()
            self.assertEqual(result["consumption_count"], 0)
            self.assertEqual(
                (before.st_size, before.st_mtime_ns),
                (after.st_size, after.st_mtime_ns),
            )

    def test_capture_confirmation_fails_before_runtime_verification(self):
        with mock.patch.object(
            tool,
            "verify_source_generation",
            side_effect=AssertionError("must not run"),
        ):
            with self.assertRaises(tool.CaptureOperationHold) as caught:
                tool.capture_runtime(
                    self.contract,
                    confirmation="WRONG",
                )
            self.assertIn("HOLD_CAPTURE_EXPLICIT_CONFIRMATION", str(caught.exception))
            self.assertFalse(caught.exception.state["runtime_child_started"])

    def test_repo_root_is_inserted_for_isolated_runtime_imports(self):
        code = (
            "import runpy;"
            f"ns=runpy.run_path({str(SCRIPT)!r},run_name='pr38_probe');"
            "m=ns['load_structural_verifier']();"
            "b=ns['load_benchmark_core']();"
            "print(m.MARKER,b.MARKER)"
        )
        cp = subprocess.run(
            [sys.executable, "-I", "-B", "-c", code],
            cwd="/tmp",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertIn("VOID_WAR_COLLEGE_CONTROLLER_EVIDENCE_ISOLATION_V1", cp.stdout)
        self.assertIn("VOID_WAR_COLLEGE_JOINT_ADVANCE_BENCHMARK_V1", cp.stdout)

    def test_process_group_retirement_is_bounded(self):
        process = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(60)"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        pgid = os.getpgid(process.pid)
        terminal = tool.force_retire_process_group(
            process,
            pgid,
            signal_grace_s=0.2,
        )
        self.assertIn(terminal, {"sigterm_retired", "sigkill_retired"})
        self.assertFalse(tool._process_group_exists(pgid))

    def test_parent_rejects_child_source_head_drift_before_publication(self):
        head = "a" * 40
        wrong = "b" * 40
        attempt = {"attempt_id": self.contract["attempt_id"]}

        with mock.patch.object(
            tool.socket,
            "gethostname",
            return_value=self.contract["designated_hostname"],
        ), mock.patch.object(
            tool,
            "EXPECTED_UID",
            os.getuid(),
        ), mock.patch.object(
            tool,
            "EXPECTED_GID",
            os.getgid(),
        ), mock.patch.object(
            tool,
            "verify_source_generation",
            return_value=head,
        ), mock.patch.object(
            tool,
            "verify_runtime_generation",
            return_value=Path(self.contract["openra_directory"]),
        ), mock.patch.object(
            tool,
            "verify_dotnet",
            return_value=Path(self.contract["dotnet_path"]),
        ), mock.patch.object(
            tool,
            "_read_attempt_ro",
            return_value=attempt,
        ), mock.patch.object(
            tool,
            "inspect_private_output_namespace",
            return_value={"root_exists": False, "evidence_exists": False},
        ), mock.patch.object(
            tool,
            "_run_runtime_child",
            return_value=({}, {}, wrong),
        ), mock.patch.object(
            tool,
            "_open_or_create_private_output_root",
            side_effect=AssertionError("must not publish"),
        ):
            with self.assertRaises(tool.CaptureOperationHold) as caught:
                tool.capture_runtime(
                    self.contract,
                    confirmation=self.contract["explicit_capture_confirmation"],
                )

        self.assertIn(
            "HOLD_CAPTURE_PARENT_CHILD_SOURCE_HEAD_MISMATCH",
            str(caught.exception),
        )
        self.assertFalse(caught.exception.state["private_evidence_created"])

    def test_child_rejects_source_drift_after_runtime(self):
        head = "a" * 40
        wrong = "b" * 40
        attempt = {"attempt_id": self.contract["attempt_id"]}
        fake_evidence = {
            "marker": structural.MARKER,
            "schema_version": structural.SCHEMA_VERSION,
        }

        with mock.patch.object(
            tool.socket,
            "gethostname",
            return_value=self.contract["designated_hostname"],
        ), mock.patch.object(
            tool,
            "EXPECTED_UID",
            os.getuid(),
        ), mock.patch.object(
            tool,
            "EXPECTED_GID",
            os.getgid(),
        ), mock.patch.object(
            tool,
            "verify_source_generation",
            side_effect=[head, wrong],
        ), mock.patch.object(
            tool,
            "verify_runtime_generation",
            return_value=Path(self.contract["openra_directory"]),
        ), mock.patch.object(
            tool,
            "verify_dotnet",
            return_value=Path(self.contract["dotnet_path"]),
        ), mock.patch.object(
            tool,
            "_read_attempt_ro",
            return_value=attempt,
        ), mock.patch.object(
            tool,
            "_capture_async",
            new=mock.AsyncMock(return_value=(fake_evidence, {})),
        ):
            with self.assertRaisesRegex(
                tool.CaptureHold,
                "HOLD_CAPTURE_CHILD_SOURCE_HEAD_DRIFT",
            ):
                tool.capture_child(
                    self.contract,
                    confirmation=self.contract["explicit_capture_confirmation"],
                )

    def test_runtime_child_command_is_isolated_and_confirmation_bound(self):
        command = tool._runtime_child_command(
            self.contract,
            self.contract["explicit_capture_confirmation"],
        )
        self.assertEqual(command[1:3], ["-I", "-B"])
        self.assertIn("_capture-child", command)
        self.assertIn("--confirm-capture", command)
        self.assertIn(
            self.contract["explicit_capture_confirmation"],
            command,
        )

    def test_contract_binds_dotnet_and_containment(self):
        self.assertEqual(self.contract["dotnet_version"], "8.0.424")
        self.assertEqual(
            self.contract["runtime_containment_strategy"],
            "spawned_capture_child_private_process_group_v1",
        )
        self.assertEqual(
            self.contract["private_publish_strategy"],
            "retained_output_directory_fd_o_excl_v1",
        )


if __name__ == "__main__":
    unittest.main()
