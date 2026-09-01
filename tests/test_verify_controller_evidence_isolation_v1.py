#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_controller_evidence_isolation_v1.py"
SPEC = importlib.util.spec_from_file_location("controller_evidence_isolation", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


def make_record(player_id: str, controller_id: str, world_tick: int) -> dict[str, object]:
    payload = {
        "player_id": player_id,
        "visible_actor_ids": [f"{player_id}-actor"],
        "world_tick": world_tick,
    }
    observation_sha = contract.sha256_hex(payload)
    return {
        "action_actor_player_id": player_id,
        "controller_id": controller_id,
        "observation_binding_sha256": contract.observation_binding(
            player_id=player_id,
            controller_id=controller_id,
            world_tick=world_tick,
            observation_sha256=observation_sha,
        ),
        "observation_payload": payload,
        "observation_sha256": observation_sha,
        "observation_subject_player_id": player_id,
        "player_id": player_id,
        "visibility_owner_player_id": player_id,
    }


def finalize(evidence: dict[str, object]) -> dict[str, object]:
    controllers = evidence["controllers"]
    assert isinstance(controllers, list)
    bindings = [
        {
            "controller_id": str(record["controller_id"]),
            "observation_binding_sha256": str(record["observation_binding_sha256"]),
            "player_id": str(record["player_id"]),
        }
        for record in controllers
    ]
    evidence["joint_evidence_sha256"] = contract.joint_evidence_binding(
        world_tick=int(evidence["world_tick"]),
        bindings=bindings,
    )
    return evidence


def make_evidence() -> dict[str, object]:
    tick = 420
    return finalize(
        {
            "controllers": [
                make_record("player-1", "controller-a", tick),
                make_record("player-2", "controller-b", tick),
            ],
            "engine_frozen_commit": contract.ENGINE_FROZEN_COMMIT,
            "generation": contract.GENERATION,
            "joint_evidence_sha256": "pending",
            "marker": contract.MARKER,
            "schema_version": contract.SCHEMA_VERSION,
            "war_college_frozen_commit": contract.WAR_COLLEGE_FROZEN_COMMIT,
            "world_tick": tick,
        }
    )


class ControllerEvidenceIsolationTests(unittest.TestCase):
    def assert_hold(self, evidence: dict[str, object], code: str) -> None:
        report = contract.verify_evidence(evidence)
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])
        self.assertEqual(report["runtime_evidence"], "PENDING_DESIGNATED_HOST")

    def test_accepts_exact_two_controller_binding(self) -> None:
        report = contract.verify_evidence(make_evidence())
        self.assertEqual(report["contract"], "GREEN")
        self.assertEqual(report["holds"], [])
        self.assertEqual(report["checked_players"], ["player-1", "player-2"])

    def test_rejects_cross_player_observation_subject(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][1]["observation_subject_player_id"] = "player-1"
        self.assert_hold(evidence, "HOLD_CROSS_PLAYER_OBSERVATION")

    def test_rejects_cross_player_action_actor(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][0]["action_actor_player_id"] = "player-2"
        self.assert_hold(evidence, "HOLD_CROSS_PLAYER_ACTION")

    def test_rejects_duplicate_controller_identity(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][1]["controller_id"] = "controller-a"
        self.assert_hold(evidence, "HOLD_DUPLICATE_CONTROLLER_ID")

    def test_rejects_swapped_observation_payload(self) -> None:
        evidence = make_evidence()
        first = evidence["controllers"][0]
        second = evidence["controllers"][1]
        second["observation_payload"] = first["observation_payload"]
        second["observation_sha256"] = first["observation_sha256"]
        self.assert_hold(evidence, "HOLD_PAYLOAD_PLAYER_BINDING")
        self.assert_hold(evidence, "HOLD_OBSERVATION_BINDING_MISMATCH")

    def test_rejects_observation_byte_mutation(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][0]["observation_payload"]["visible_actor_ids"].append("injected")
        self.assert_hold(evidence, "HOLD_OBSERVATION_DIGEST_MISMATCH")

    def test_rejects_split_tick_payload(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][1]["observation_payload"]["world_tick"] = 421
        self.assert_hold(evidence, "HOLD_PAYLOAD_TICK_BINDING")

    def test_rejects_frozen_baseline_drift(self) -> None:
        evidence = make_evidence()
        evidence["engine_frozen_commit"] = "0" * 40
        self.assert_hold(evidence, "HOLD_ENGINE_BASE_MISMATCH")

    def test_rejects_schema_extension(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][0]["unreviewed_authority"] = True
        self.assert_hold(evidence, "HOLD_CONTROLLER_SCHEMA_DRIFT")

    def test_cli_is_one_line_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            evidence_path = Path(temp_dir) / "evidence.json"
            evidence_path.write_text(json.dumps(make_evidence()), encoding="utf-8")
            green = subprocess.run(
                [sys.executable, str(SCRIPT), str(evidence_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(green.returncode, 0, green.stderr)
            self.assertEqual(len(green.stdout.splitlines()), 1)
            self.assertEqual(json.loads(green.stdout)["contract"], "GREEN")

            evidence_path.write_text("{", encoding="utf-8")
            hold = subprocess.run(
                [sys.executable, str(SCRIPT), str(evidence_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(hold.returncode, 1)
            self.assertEqual(len(hold.stdout.splitlines()), 1)
            self.assertEqual(json.loads(hold.stdout)["contract"], "HOLD")


if __name__ == "__main__":
    unittest.main()
