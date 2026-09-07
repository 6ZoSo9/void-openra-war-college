#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import controller_attempt_admission_store_v1 as store
from scripts import verify_controller_evidence_with_durable_currentness_v1 as integration
from tests.test_verify_controller_evidence_isolation_v1 import make_evidence


def identity(
    *,
    attempt_id: str = "attempt-001",
    source_generation: str = "ad1926569b12466c",
    war_college_commit: str = integration.STORE_WAR_COLLEGE_SOURCE_BASE,
    swapped_mapping: bool = False,
) -> store.AttemptIdentity:
    if swapped_mapping:
        a_player, b_player = "player-2", "player-1"
    else:
        a_player, b_player = "player-1", "player-2"
    return store.AttemptIdentity(
        attempt_id=attempt_id,
        producer_id="designated-host-1",
        controller_a_id="controller-a",
        controller_a_player_id=a_player,
        controller_b_id="controller-b",
        controller_b_player_id=b_player,
        source_generation=source_generation,
        war_college_commit=war_college_commit,
        engine_commit=integration.structural.ENGINE_FROZEN_COMMIT,
    )


class DurableCurrentnessIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_data_dir = os.environ.get("VOID_DATA_DIR")
        self._temp = tempfile.TemporaryDirectory()
        os.environ["VOID_DATA_DIR"] = self._temp.name
        self.store_path = integration.canonical_store_path()

    def tearDown(self) -> None:
        if self._old_data_dir is None:
            os.environ.pop("VOID_DATA_DIR", None)
        else:
            os.environ["VOID_DATA_DIR"] = self._old_data_dir
        self._temp.cleanup()

    def create_attempt(
        self,
        attempt_identity: store.AttemptIdentity | None = None,
    ) -> store.AttemptIdentity:
        value = attempt_identity or identity()
        store.create_attempt(self.store_path, value)
        return value

    def assert_hold(self, report: dict[str, object], code: str) -> None:
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_green_derives_store_currentness_and_consumes_once(self) -> None:
        self.create_attempt()
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assertEqual(report["contract"], "GREEN")
        self.assertEqual(report["session_generation"], 1)
        self.assertEqual(report["structural_contract"], "GREEN")
        self.assertIsNotNone(report["consumption_sha256"])

    def test_identical_full_bundle_replay_is_rejected(self) -> None:
        self.create_attempt()
        evidence = make_evidence()
        self.assertEqual(
            integration.verify_and_consume_evidence(evidence)["contract"],
            "GREEN",
        )
        replay = integration.verify_and_consume_evidence(evidence)
        self.assert_hold(replay, "HOLD_EVIDENCE_ALREADY_CONSUMED")

    def test_stale_predecessor_after_reconnect_is_rejected(self) -> None:
        attempt_identity = self.create_attempt()
        store.advance_session(
            self.store_path,
            attempt_identity,
            expected_current_generation=1,
        )
        stale = integration.verify_and_consume_evidence(
            make_evidence(controller_session_generation=1)
        )
        self.assert_hold(
            stale,
            "HOLD_EXPECTED_CONTROLLER_SESSION_GENERATION_MISMATCH",
        )
        fresh = integration.verify_and_consume_evidence(
            make_evidence(controller_session_generation=2)
        )
        self.assertEqual(fresh["contract"], "GREEN")

    def test_controller_player_mapping_is_store_authoritative(self) -> None:
        self.create_attempt(identity(swapped_mapping=True))
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assert_hold(
            report,
            "HOLD_DURABLE_CONTROLLER_PLAYER_MAPPING_MISMATCH",
        )

    def test_structural_hold_does_not_consume_evidence(self) -> None:
        self.create_attempt()
        invalid = make_evidence()
        invalid["controllers"][0]["action_payload"]["commands"][0]["actor_id"] = 201
        first = integration.verify_and_consume_evidence(invalid)
        self.assertEqual(first["contract"], "HOLD")
        self.assertEqual(first["phase"], "structural_verification")
        clean = integration.verify_and_consume_evidence(make_evidence())
        self.assertEqual(clean["contract"], "GREEN")

    def test_store_source_generation_mismatch_fails_closed(self) -> None:
        self.create_attempt(identity(source_generation="other-generation"))
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assert_hold(report, "HOLD_STORE_SOURCE_GENERATION_MISMATCH")

    def test_store_source_base_mismatch_fails_closed(self) -> None:
        self.create_attempt(identity(war_college_commit="1" * 40))
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assert_hold(
            report,
            "HOLD_STORE_WAR_COLLEGE_SOURCE_BASE_MISMATCH",
        )

    def test_missing_store_is_not_created_by_verification(self) -> None:
        self.assertFalse(self.store_path.exists())
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assert_hold(report, "HOLD_STORE_NOT_FOUND")
        self.assertFalse(self.store_path.exists())

    def test_void_data_dir_must_be_absolute(self) -> None:
        os.environ["VOID_DATA_DIR"] = "relative-data"
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assert_hold(report, "HOLD_VOID_DATA_DIR_NOT_ABSOLUTE")

    def test_void_data_dir_is_required(self) -> None:
        os.environ.pop("VOID_DATA_DIR", None)
        report = integration.verify_and_consume_evidence(make_evidence())
        self.assert_hold(report, "HOLD_VOID_DATA_DIR_REQUIRED")

    def test_reconnect_race_after_structural_green_fails_at_consume(self) -> None:
        attempt_identity = self.create_attempt()
        original_consume = integration.consume_joint_evidence

        def raced_consume(
            path: Path,
            loaded_identity: store.AttemptIdentity,
            *,
            session_generation: int,
            joint_evidence_sha256: str,
        ):
            store.advance_session(
                path,
                loaded_identity,
                expected_current_generation=session_generation,
            )
            return original_consume(
                path,
                loaded_identity,
                session_generation=session_generation,
                joint_evidence_sha256=joint_evidence_sha256,
            )

        integration.consume_joint_evidence = raced_consume
        try:
            raced = integration.verify_and_consume_evidence(make_evidence())
        finally:
            integration.consume_joint_evidence = original_consume

        self.assert_hold(raced, "HOLD_SESSION_NOT_CURRENT")
        fresh = integration.verify_and_consume_evidence(
            make_evidence(controller_session_generation=2)
        )
        self.assertEqual(fresh["contract"], "GREEN")
        self.assertEqual(
            store.inspect_attempt(self.store_path, attempt_identity)[
                "session_generation"
            ],
            2,
        )

    def test_cli_is_one_line_and_has_no_store_path_argument(self) -> None:
        self.create_attempt()
        evidence_path = Path(self._temp.name) / "evidence.json"
        evidence_path.write_text(
            json.dumps(make_evidence(), sort_keys=True),
            encoding="utf-8",
        )
        script = (
            Path(__file__).resolve().parents[1]
            / "scripts"
            / "verify_controller_evidence_with_durable_currentness_v1.py"
        )
        cp = subprocess.run(
            [sys.executable, str(script), str(evidence_path)],
            capture_output=True,
            text=True,
            check=False,
            env=dict(os.environ),
        )
        self.assertEqual(cp.returncode, 0)
        self.assertEqual(cp.stderr, "")
        self.assertEqual(len(cp.stdout.splitlines()), 1)
        report = json.loads(cp.stdout)
        self.assertEqual(report["contract"], "GREEN")


if __name__ == "__main__":
    unittest.main()
