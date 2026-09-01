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
    observation_payload = {
        "player_id": player_id,
        "visible_actor_ids": [f"{player_id}-actor"],
        "world_tick": world_tick,
    }
    observation_sha = contract.sha256_hex(observation_payload)
    action_request_id = f"decision-{world_tick}-{player_id}"
    action_payload = {
        "commands": [{"actor_id": f"{player_id}-actor", "command": "hold"}],
        "controller_id": controller_id,
        "player_id": player_id,
        "request_id": action_request_id,
        "world_tick": world_tick,
    }
    action_sha = contract.sha256_hex(action_payload)
    return {
        "action_actor_player_id": player_id,
        "action_binding_sha256": contract.action_binding(
            player_id=player_id,
            controller_id=controller_id,
            world_tick=world_tick,
            action_request_id=action_request_id,
            action_sha256=action_sha,
        ),
        "action_payload": action_payload,
        "action_request_id": action_request_id,
        "action_sha256": action_sha,
        "controller_id": controller_id,
        "observation_binding_sha256": contract.observation_binding(
            player_id=player_id,
            controller_id=controller_id,
            world_tick=world_tick,
            observation_sha256=observation_sha,
        ),
        "observation_payload": observation_payload,
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
            "action_binding_sha256": str(record["action_binding_sha256"]),
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

    def test_rejects_swapped_action_payload_and_digest(self) -> None:
        evidence = make_evidence()
        first = evidence["controllers"][0]
        second = evidence["controllers"][1]
        second["action_payload"] = first["action_payload"]
        second["action_sha256"] = first["action_sha256"]
        self.assert_hold(evidence, "HOLD_ACTION_PAYLOAD_PLAYER_BINDING")
        self.assert_hold(evidence, "HOLD_ACTION_PAYLOAD_CONTROLLER_BINDING")
        self.assert_hold(evidence, "HOLD_ACTION_BINDING_MISMATCH")

    def test_rejects_action_byte_mutation(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][0]["action_payload"]["commands"][0]["command"] = "attack"
        self.assert_hold(evidence, "HOLD_ACTION_DIGEST_MISMATCH")

    def test_rejects_action_replay_across_controller(self) -> None:
        evidence = make_evidence()
        first = evidence["controllers"][0]
        second = evidence["controllers"][1]
        second["action_request_id"] = first["action_request_id"]
        second["action_payload"]["request_id"] = first["action_request_id"]
        second["action_sha256"] = contract.sha256_hex(second["action_payload"])
        second["action_binding_sha256"] = contract.action_binding(
            player_id=second["player_id"],
            controller_id=second["controller_id"],
            world_tick=evidence["world_tick"],
            action_request_id=second["action_request_id"],
            action_sha256=second["action_sha256"],
        )
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_DUPLICATE_ACTION_REQUEST_ID")

    def test_rejects_action_replay_across_tick(self) -> None:
        evidence = make_evidence()
        record = evidence["controllers"][0]
        record["action_payload"]["world_tick"] = 419
        record["action_sha256"] = contract.sha256_hex(record["action_payload"])
        record["action_binding_sha256"] = contract.action_binding(
            player_id=record["player_id"],
            controller_id=record["controller_id"],
            world_tick=evidence["world_tick"],
            action_request_id=record["action_request_id"],
            action_sha256=record["action_sha256"],
        )
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_ACTION_PAYLOAD_TICK_BINDING")

    def test_rejects_joint_digest_omitting_action_binding(self) -> None:
        evidence = make_evidence()
        bindings = [
            {
                "controller_id": record["controller_id"],
                "observation_binding_sha256": record["observation_binding_sha256"],
                "player_id": record["player_id"],
            }
            for record in evidence["controllers"]
        ]
        evidence["joint_evidence_sha256"] = contract.joint_evidence_binding(
            world_tick=evidence["world_tick"],
            bindings=bindings,
        )
        self.assert_hold(evidence, "HOLD_JOINT_EVIDENCE_DIGEST_MISMATCH")

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
