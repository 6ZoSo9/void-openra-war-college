#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/capture_designated_host_controller_evidence_generation2_v1.py"
SPEC = importlib.util.spec_from_file_location("controller_capture_generation2", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

STRUCTURAL_SPEC = importlib.util.spec_from_file_location(
    "controller_structural_g2",
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


def initialize_store(path: Path, contract: dict, *, predecessor_consumed: bool = True):
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
              session_generation INTEGER NOT NULL,
              joint_evidence_sha256 TEXT NOT NULL,
              producer_id TEXT NOT NULL,
              producer_public_key_sha256 TEXT NOT NULL,
              controller_a_id TEXT NOT NULL,
              controller_a_player_id TEXT NOT NULL,
              controller_b_id TEXT NOT NULL,
              controller_b_player_id TEXT NOT NULL,
              consumption_sha256 TEXT NOT NULL
            );
            """
        )
        db.execute(
            "INSERT INTO attempts VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (
                contract["attempt_id"],
                contract["producer_node_id"],
                contract["producer_public_key_sha256"],
                "apollyon",
                "Multi0",
                "abaddon",
                "Multi1",
                contract["source_generation"],
                contract["store_war_college_source_base"],
                contract["engine_commit"],
                2,
            ),
        )
        db.execute(
            "INSERT INTO sessions VALUES(?,?,NULL)",
            (contract["attempt_id"], 1),
        )
        db.execute(
            "INSERT INTO sessions VALUES(?,?,?)",
            (contract["attempt_id"], 2, 1),
        )
        if predecessor_consumed:
            db.execute(
                "INSERT INTO consumptions VALUES(?,?,?,?,?,?,?,?,?,?)",
                (
                    contract["attempt_id"],
                    1,
                    contract["predecessor_joint_evidence_sha256"],
                    contract["producer_node_id"],
                    contract["producer_public_key_sha256"],
                    "apollyon",
                    "Multi0",
                    "abaddon",
                    "Multi1",
                    contract["predecessor_consumption_sha256"],
                ),
            )
        db.commit()
    finally:
        db.close()
    os.chmod(path, 0o600)


class Generation2CaptureTests(unittest.TestCase):
    def setUp(self):
        self.contract = tool.load_contract()

    def test_contract_binds_exact_generation2_successor_and_no_authority(self):
        self.assertEqual(self.contract["semantic_parent_pr"], 38)
        self.assertEqual(
            self.contract["semantic_parent_head"],
            "eadc0b15876fdfe6cf021860f1d4b7b8697fb64e",
        )
        self.assertEqual(self.contract["predecessor_session_generation"], 1)
        self.assertEqual(self.contract["controller_session_generation"], 2)
        self.assertEqual(
            self.contract["expected_session_advance_receipt_sha256"],
            tool.EXPECTED_GENERATION2_ADMISSION_SHA256,
        )
        self.assertEqual(
            self.contract["evidence_filename"],
            "war-college-ad1926569b12466c-001-s2-evidence.json",
        )
        self.assertEqual(
            self.contract["explicit_capture_confirmation"],
            "CAPTURE_GENERATION2_CONTROLLER_EVIDENCE",
        )
        self.assertEqual(
            self.contract["capture_python_path"],
            "/home/zoso/Downloads/void-war-college-capture-runtime-v1/bin/python",
        )
        self.assertEqual(
            self.contract["capture_python_prefix"],
            "/home/zoso/Downloads/void-war-college-capture-runtime-v1",
        )
        self.assertEqual(self.contract["capture_grpc_version"], "1.75.1")
        self.assertEqual(self.contract["capture_protobuf_version"], "6.31.1")
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

    def test_generation2_admission_receipt_rederives_exactly(self):
        payload = {
            "attempt_id": self.contract["attempt_id"],
            "controller_a_id": "apollyon",
            "controller_a_player_id": "Multi0",
            "controller_b_id": "abaddon",
            "controller_b_player_id": "Multi1",
            "engine_commit": self.contract["engine_commit"],
            "producer_id": self.contract["producer_node_id"],
            "producer_public_key_sha256": self.contract[
                "producer_public_key_sha256"
            ],
            "schema_version": 3,
            "session_generation": 2,
            "source_generation": self.contract["source_generation"],
            "war_college_commit": self.contract["store_war_college_source_base"],
        }
        self.assertEqual(
            tool.canonical_sha256(payload),
            "5159b314633903133d82c2a21720108ec80e1a1c3d8d482675cac4e6a030e7d7",
        )

    def test_generation2_child_command_reenters_wrapper(self):
        command = tool._generation2_runtime_child_command(
            self.contract,
            self.contract["explicit_capture_confirmation"],
        )
        self.assertEqual(command[0], self.contract["capture_python_path"])
        self.assertEqual(command[1:3], ["-I", "-B"])
        self.assertEqual(Path(command[3]).resolve(), SCRIPT.resolve())
        self.assertEqual(command[4], "_capture-child")
        self.assertEqual(command[-1], "CAPTURE_GENERATION2_CONTROLLER_EVIDENCE")
        self.assertIs(tool.base._read_attempt_ro, tool._read_attempt_generation2_ro)

    def test_builds_structurally_green_generation2_evidence(self):
        evidence = tool.base.build_causal_evidence(
            bootstrap_response=response("session-g2", 80, 81),
            action_response=response("session-g2", 81, 82),
            expected_session_id="session-g2",
            contract=self.contract,
            structural=structural,
        )
        report = structural.verify_evidence(
            evidence,
            expected_attempt_id=self.contract["attempt_id"],
            expected_controller_session_generation=2,
        )
        self.assertEqual(report["contract"], "GREEN")
        self.assertEqual(evidence["controller_session_generation"], 2)
        for record in evidence["controllers"]:
            self.assertEqual(record["action_payload"]["commands"], [])

    def test_read_only_store_gate_accepts_exact_successor_and_predecessor_receipt(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "store.sqlite3"
            initialize_store(path, self.contract)
            contract = dict(self.contract)
            contract["store_path"] = str(path)
            before = path.stat()
            with mock.patch.object(tool.base, "EXPECTED_UID", os.getuid()), mock.patch.object(
                tool.base, "EXPECTED_GID", os.getgid()
            ):
                result = tool._read_attempt_generation2_ro(contract)
            after = path.stat()
            self.assertEqual(result["current_session_generation"], 2)
            self.assertEqual(result["consumption_count"], 0)
            self.assertEqual(result["predecessor_consumption_count"], 1)
            self.assertEqual(
                result["predecessor_consumption_sha256"],
                tool.EXPECTED_PREDECESSOR_CONSUMPTION_SHA256,
            )
            self.assertEqual(result["successor_predecessor_generation"], 1)
            self.assertEqual(
                (before.st_size, before.st_mtime_ns),
                (after.st_size, after.st_mtime_ns),
            )

    def test_read_only_store_gate_rejects_missing_predecessor_consumption(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "store.sqlite3"
            initialize_store(path, self.contract, predecessor_consumed=False)
            contract = dict(self.contract)
            contract["store_path"] = str(path)
            with mock.patch.object(tool.base, "EXPECTED_UID", os.getuid()), mock.patch.object(
                tool.base, "EXPECTED_GID", os.getgid()
            ):
                with self.assertRaisesRegex(
                    tool.Generation2CaptureHold,
                    "HOLD_CAPTURE_G2_PREDECESSOR_CONSUMPTION_COUNT",
                ):
                    tool._read_attempt_generation2_ro(contract)


    def test_capture_runtime_probes_dedicated_python_before_parent_runtime(self):
        with mock.patch.object(
            tool,
            "verify_capture_python",
            side_effect=tool.Generation2CaptureHold(
                "HOLD_CAPTURE_G2_CAPTURE_PYTHON_RUNTIME_IMPORTS"
            ),
        ), mock.patch.object(
            tool.base,
            "capture_runtime",
            side_effect=AssertionError("must not run parent capture"),
        ):
            with self.assertRaisesRegex(
                tool.Generation2CaptureHold,
                "HOLD_CAPTURE_G2_CAPTURE_PYTHON_RUNTIME_IMPORTS",
            ):
                tool.capture_runtime(
                    self.contract,
                    confirmation=self.contract["explicit_capture_confirmation"],
                )

    def test_wrong_capture_confirmation_fails_before_runtime_verification(self):
        with mock.patch.object(
            tool.base,
            "verify_source_generation",
            side_effect=AssertionError("must not run"),
        ):
            with self.assertRaises(tool.base.CaptureOperationHold) as caught:
                tool.capture_runtime(
                    self.contract,
                    confirmation="WRONG",
                )
        self.assertIn("HOLD_CAPTURE_EXPLICIT_CONFIRMATION", str(caught.exception))
        self.assertFalse(caught.exception.state["runtime_child_started"])

    def test_wrapper_contains_no_direct_mutation_or_secret_authority(self):
        source = SCRIPT.read_text(encoding="utf-8")
        for forbidden in (
            "BEGIN PRIVATE KEY",
            "consume_joint_evidence(",
            "advance_session(",
            "systemctl",
            ".sign(",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
