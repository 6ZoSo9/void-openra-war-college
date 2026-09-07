#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_verify_controller_evidence_isolation_v1 import (
    ATTEMPT_ID,
    SESSION_GENERATION,
    SCRIPT,
    contract,
    make_evidence,
    verify,
)


class ControllerEvidenceInputBoundsTests(unittest.TestCase):
    def run_cli(
        self,
        evidence_path: Path,
        *,
        attempt_id: str = ATTEMPT_ID,
        session_generation: str = str(SESSION_GENERATION),
    ) -> dict[str, object]:
        cp = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(evidence_path),
                "--expected-attempt-id",
                attempt_id,
                "--expected-controller-session-generation",
                session_generation,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(cp.stderr, "")
        self.assertEqual(len(cp.stdout.splitlines()), 1)
        report = json.loads(cp.stdout)
        self.assertEqual(cp.returncode, 0 if report["contract"] == "GREEN" else 1)
        return report

    def test_exact_file_byte_ceiling_is_admitted_and_max_plus_one_holds(self) -> None:
        payload = json.dumps(make_evidence(), separators=(",", ":")).encode()
        self.assertLess(len(payload), contract.MAX_EVIDENCE_BYTES)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "evidence.json"
            exact = payload + b" " * (contract.MAX_EVIDENCE_BYTES - len(payload))
            self.assertEqual(len(exact), contract.MAX_EVIDENCE_BYTES)
            path.write_bytes(exact)
            self.assertEqual(self.run_cli(path)["contract"], "GREEN")

            path.write_bytes(exact + b" ")
            report = self.run_cli(path)
            self.assertEqual(report["contract"], "HOLD")
            self.assertIn("HOLD_EVIDENCE_FILE_TOO_LARGE", report["holds"])

    def test_symlink_and_fifo_fail_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "target.json"
            target.write_text(json.dumps(make_evidence()), encoding="utf-8")

            link = root / "evidence-link.json"
            link.symlink_to(target)
            report = self.run_cli(link)
            self.assertIn("HOLD_EVIDENCE_PATH_NOT_REGULAR", report["holds"])

            fifo = root / "evidence.fifo"
            os.mkfifo(fifo)
            report = self.run_cli(fifo)
            self.assertIn("HOLD_EVIDENCE_PATH_NOT_REGULAR", report["holds"])

    def test_json_depth_is_rejected_before_json_load(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "deep.json"
            depth = contract.MAX_JSON_DEPTH + 1
            raw = b"[" * depth + b"0" + b"]" * depth
            path.write_bytes(raw)
            report = self.run_cli(path)
            self.assertIn("HOLD_JSON_DEPTH_EXCEEDED", report["holds"])

    def test_identifier_max_and_max_plus_one(self) -> None:
        maximum = "a" * contract.MAX_IDENTIFIER_BYTES
        evidence = make_evidence(attempt_id=maximum)
        report = verify(
            evidence,
            expected_attempt_id=maximum,
            expected_controller_session_generation=SESSION_GENERATION,
        )
        self.assertEqual(report["contract"], "GREEN")

        too_wide = "a" * (contract.MAX_IDENTIFIER_BYTES + 1)
        evidence = make_evidence()
        evidence["attempt_id"] = too_wide
        report = verify(evidence)
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn("HOLD_ATTEMPT_ID_INPUT_INVALID", report["holds"])

    def test_uint32_bound_is_fail_closed(self) -> None:
        evidence = make_evidence()
        evidence["world_tick"] = contract.MAX_UINT32 + 1
        report = verify(evidence)
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn("HOLD_WORLD_TICK_INPUT_INVALID", report["holds"])

        evidence = make_evidence()
        evidence["controller_session_generation"] = contract.MAX_UINT32 + 1
        report = verify(evidence)
        self.assertIn(
            "HOLD_CONTROLLER_SESSION_GENERATION_INPUT_INVALID",
            report["holds"],
        )

    def test_noncanonical_digest_rejected_before_hash(self) -> None:
        evidence = make_evidence()
        evidence["controllers"][0]["observation_sha256"] = (
            str(evidence["controllers"][0]["observation_sha256"]).upper()
        )

        original = contract.sha256_hex
        def bomb(_value):
            raise AssertionError("hashing occurred before digest admission")
        contract.sha256_hex = bomb
        try:
            report = verify(evidence)
        finally:
            contract.sha256_hex = original

        self.assertEqual(report["contract"], "HOLD")
        self.assertIn("HOLD_OBSERVATION_SHA256_NONCANONICAL", report["holds"])

    def test_oversized_command_list_rejected_before_hash(self) -> None:
        evidence = make_evidence()
        command = dict(evidence["controllers"][0]["action_payload"]["commands"][0])
        evidence["controllers"][0]["action_payload"]["commands"] = [
            dict(command) for _ in range(contract.MAX_COMMANDS + 1)
        ]

        original = contract.sha256_hex
        def bomb(_value):
            raise AssertionError("hashing occurred before command admission")
        contract.sha256_hex = bomb
        try:
            report = verify(evidence)
        finally:
            contract.sha256_hex = original

        self.assertEqual(report["contract"], "HOLD")
        self.assertIn("HOLD_ACTION_COMMANDS_CARDINALITY", report["holds"])

    def test_nested_command_value_rejected_before_hash(self) -> None:
        evidence = make_evidence()
        command = dict(evidence["controllers"][0]["action_payload"]["commands"][0])
        command["item_type"] = {"nested": "hold"}
        evidence["controllers"][0]["action_payload"]["commands"] = [command]

        original = contract.sha256_hex
        def bomb(_value):
            raise AssertionError("hashing occurred before flat-shape admission")
        contract.sha256_hex = bomb
        try:
            report = verify(evidence)
        finally:
            contract.sha256_hex = original

        self.assertIn("HOLD_ACTION_COMMAND_ITEM_TYPE_INVALID", report["holds"])

    def test_expected_generation_5000_digits_is_one_line_hold(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "evidence.json"
            path.write_text(json.dumps(make_evidence()), encoding="utf-8")
            report = self.run_cli(path, session_generation="9" * 5000)
            self.assertIn(
                "HOLD_EXPECTED_CONTROLLER_SESSION_GENERATION_INVALID",
                report["holds"],
            )

    def test_oversized_expected_attempt_id_is_one_line_hold(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "evidence.json"
            path.write_text(json.dumps(make_evidence()), encoding="utf-8")
            report = self.run_cli(
                path,
                attempt_id="a" * (contract.MAX_IDENTIFIER_BYTES + 1),
            )
            self.assertIn("HOLD_EXPECTED_ATTEMPT_ID_INVALID", report["holds"])


if __name__ == "__main__":
    unittest.main()
