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

ATTEMPT_ID = "attempt-001"
SESSION_GENERATION = 1


def make_record(
    player_id: str,
    controller_id: str,
    world_tick: int,
    attempt_id: str,
    controller_session_generation: int,
) -> dict[str, object]:
    observation_payload = {
        "attempt_id": attempt_id,
        "controller_session_generation": controller_session_generation,
        "player_id": player_id,
        "visible_actor_ids": [f"{player_id}-actor"],
        "world_tick": world_tick,
    }
    observation_sha = contract.sha256_hex(observation_payload)
    observation_binding_sha = contract.observation_binding(
        attempt_id=attempt_id,
        controller_session_generation=controller_session_generation,
        player_id=player_id,
        controller_id=controller_id,
        world_tick=world_tick,
        observation_sha256=observation_sha,
    )
    action_request_id = (
        f"decision-{attempt_id}-{controller_session_generation}-"
        f"{world_tick}-{player_id}"
    )
    action_payload = {
        "attempt_id": attempt_id,
        "controller_session_generation": controller_session_generation,
        "commands": [{"actor_id": f"{player_id}-actor", "command": "hold"}],
        "controller_id": controller_id,
        "decision_observation_binding_sha256": observation_binding_sha,
        "player_id": player_id,
        "request_id": action_request_id,
        "world_tick": world_tick,
    }
    action_sha = contract.sha256_hex(action_payload)
    return {
        "action_actor_player_id": player_id,
        "action_binding_sha256": contract.action_binding(
            attempt_id=attempt_id,
            controller_session_generation=controller_session_generation,
            player_id=player_id,
            controller_id=controller_id,
            world_tick=world_tick,
            action_request_id=action_request_id,
            action_sha256=action_sha,
            decision_observation_binding_sha256=observation_binding_sha,
        ),
        "action_payload": action_payload,
        "action_request_id": action_request_id,
        "action_sha256": action_sha,
        "controller_id": controller_id,
        "observation_binding_sha256": observation_binding_sha,
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
        attempt_id=str(evidence["attempt_id"]),
        controller_session_generation=int(
            evidence["controller_session_generation"]
        ),
        world_tick=int(evidence["world_tick"]),
        bindings=bindings,
    )
    return evidence


def make_evidence(
    attempt_id: str = ATTEMPT_ID,
    controller_session_generation: int = SESSION_GENERATION,
) -> dict[str, object]:
    tick = 420
    return finalize(
        {
            "attempt_id": attempt_id,
            "controller_session_generation": controller_session_generation,
            "controllers": [
                make_record(
                    "player-1",
                    "controller-a",
                    tick,
                    attempt_id,
                    controller_session_generation,
                ),
                make_record(
                    "player-2",
                    "controller-b",
                    tick,
                    attempt_id,
                    controller_session_generation,
                ),
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


def refresh_action(record: dict[str, object], world_tick: int) -> None:
    payload = record["action_payload"]
    assert isinstance(payload, dict)
    record["action_sha256"] = contract.sha256_hex(payload)
    record["action_binding_sha256"] = contract.action_binding(
        attempt_id=payload["attempt_id"],
        controller_session_generation=payload[
            "controller_session_generation"
        ],
        player_id=record["player_id"],
        controller_id=record["controller_id"],
        world_tick=world_tick,
        action_request_id=record["action_request_id"],
        action_sha256=record["action_sha256"],
        decision_observation_binding_sha256=payload[
            "decision_observation_binding_sha256"
        ],
    )



def verify(
    evidence: dict[str, object],
    *,
    expected_attempt_id: str = ATTEMPT_ID,
    expected_controller_session_generation: int = SESSION_GENERATION,
) -> dict[str, object]:
    return contract.verify_evidence(
        evidence,
        expected_attempt_id=expected_attempt_id,
        expected_controller_session_generation=(
            expected_controller_session_generation
        ),
    )


class ControllerEvidenceIsolationTests(unittest.TestCase):
    def assert_hold(self, evidence: dict[str, object], code: str) -> None:
        report = verify(evidence)
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])
        self.assertEqual(report["runtime_evidence"], "PENDING_DESIGNATED_HOST")

    def test_accepts_exact_two_controller_binding(self) -> None:
        report = verify(make_evidence())
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
        first, second = evidence["controllers"]
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

    def test_rejects_action_from_different_admitted_observation(self) -> None:
        evidence = make_evidence()
        record = evidence["controllers"][0]
        record["observation_payload"]["visible_actor_ids"] = ["alternate-visible-actor"]
        record["observation_sha256"] = contract.sha256_hex(record["observation_payload"])
        record["observation_binding_sha256"] = contract.observation_binding(
            attempt_id=evidence["attempt_id"],
            controller_session_generation=evidence[
                "controller_session_generation"
            ],
            player_id=record["player_id"],
            controller_id=record["controller_id"],
            world_tick=evidence["world_tick"],
            observation_sha256=record["observation_sha256"],
        )
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_ACTION_DECISION_OBSERVATION_BINDING")

    def test_rejects_decision_observation_claim_mutation(self) -> None:
        evidence = make_evidence()
        record = evidence["controllers"][0]
        record["action_payload"]["decision_observation_binding_sha256"] = "0" * 64
        refresh_action(record, evidence["world_tick"])
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_ACTION_DECISION_OBSERVATION_BINDING")

    def test_rejects_swapped_action_payload_and_digest(self) -> None:
        evidence = make_evidence()
        first, second = evidence["controllers"]
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
        first, second = evidence["controllers"]
        second["action_request_id"] = first["action_request_id"]
        second["action_payload"]["request_id"] = first["action_request_id"]
        refresh_action(second, evidence["world_tick"])
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_DUPLICATE_ACTION_REQUEST_ID")

    def test_rejects_action_replay_across_tick(self) -> None:
        evidence = make_evidence()
        record = evidence["controllers"][0]
        record["action_payload"]["world_tick"] = 419
        refresh_action(record, evidence["world_tick"])
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
            attempt_id=evidence["attempt_id"],
            controller_session_generation=evidence[
                "controller_session_generation"
            ],
            world_tick=evidence["world_tick"],
            bindings=bindings,
        )
        self.assert_hold(evidence, "HOLD_JOINT_EVIDENCE_DIGEST_MISMATCH")

    def test_rejects_prior_schema_without_decision_input_binding(self) -> None:
        evidence = make_evidence()
        evidence["schema_version"] = 1
        record = evidence["controllers"][0]
        del record["action_payload"]["decision_observation_binding_sha256"]
        record["action_sha256"] = contract.sha256_hex(record["action_payload"])
        self.assert_hold(evidence, "HOLD_SCHEMA_VERSION_MISMATCH")
        self.assert_hold(evidence, "HOLD_ACTION_PAYLOAD_SCHEMA_DRIFT")

    def test_green_report_returns_admitted_attempt_session_and_joint_digest(self) -> None:
        evidence = make_evidence()
        report = verify(evidence)
        self.assertEqual(report["admitted_attempt_id"], ATTEMPT_ID)
        self.assertEqual(
            report["admitted_controller_session_generation"],
            SESSION_GENERATION,
        )
        self.assertEqual(
            report["admitted_joint_evidence_sha256"],
            evidence["joint_evidence_sha256"],
        )

    def test_identical_bundle_replay_under_other_attempt_fails_closed(self) -> None:
        evidence = make_evidence()
        report = verify(evidence, expected_attempt_id="attempt-002")
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn("HOLD_EXPECTED_ATTEMPT_ID_MISMATCH", report["holds"])

    def test_stale_session_after_reconnect_fails_closed(self) -> None:
        evidence = make_evidence()
        report = verify(
            evidence,
            expected_controller_session_generation=2,
        )
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(
            "HOLD_EXPECTED_CONTROLLER_SESSION_GENERATION_MISMATCH",
            report["holds"],
        )

    def test_cross_attempt_controller_record_swap_fails_closed(self) -> None:
        evidence = make_evidence()
        other = make_evidence(attempt_id="attempt-002")
        evidence["controllers"][0] = other["controllers"][0]
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_PAYLOAD_ATTEMPT_BINDING")

    def test_mixed_session_two_controller_bundle_fails_closed(self) -> None:
        evidence = make_evidence()
        other = make_evidence(controller_session_generation=2)
        evidence["controllers"][1] = other["controllers"][1]
        finalize(evidence)
        self.assert_hold(evidence, "HOLD_PAYLOAD_SESSION_BINDING")

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
                [
                    sys.executable,
                    str(SCRIPT),
                    str(evidence_path),
                    "--expected-attempt-id",
                    ATTEMPT_ID,
                    "--expected-controller-session-generation",
                    str(SESSION_GENERATION),
                ],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(green.returncode, 0, green.stderr)
            self.assertEqual(len(green.stdout.splitlines()), 1)
            self.assertEqual(json.loads(green.stdout)["contract"], "GREEN")

            evidence_path.write_text("{", encoding="utf-8")
            hold = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(evidence_path),
                    "--expected-attempt-id",
                    ATTEMPT_ID,
                    "--expected-controller-session-generation",
                    str(SESSION_GENERATION),
                ],
                check=False, capture_output=True, text=True,
            )
            self.assertEqual(hold.returncode, 1)
            self.assertEqual(len(hold.stdout.splitlines()), 1)
            self.assertEqual(json.loads(hold.stdout)["contract"], "HOLD")


if __name__ == "__main__":
    unittest.main()
