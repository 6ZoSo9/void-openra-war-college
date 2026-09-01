#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import darwin_evaluation_precommit_record_v1 as record_contract
import darwin_heldout_evaluation_split_v1 as split

CLI = Path(__file__).with_name("darwin_evaluation_precommit_record_v1.py")


class EvaluationPrecommitRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manifest = split.build_manifest(
            "singles.oramap",
            tuple(range(1000, 1008)),
            tuple(range(2000, 2008)),
        )
        self.manifest_path = self.root / "split.json"
        self.manifest_path.write_text(
            record_contract.canonical_json(self.manifest) + "\n",
            encoding="utf-8",
        )
        self.record_path = self.root / "precommit.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=Path(__file__).parent,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def record_args(self, **overrides: str) -> list[str]:
        values = {
            "record_id": "eval-001",
            "benchmark_source_sha": "a" * 40,
            "calibration_base_seed": "1000",
            "held_out_base_seed": "2000",
            "concurrency": "1,4",
            "tick_batches": "1,8",
            "samples": "2",
            "repetitions": "2",
            "workload_profile": "noop_control",
        }
        values.update(overrides)
        return [
            "record",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
            "--record-id",
            values["record_id"],
            "--benchmark-source-sha",
            values["benchmark_source_sha"],
            "--calibration-base-seed",
            values["calibration_base_seed"],
            "--held-out-base-seed",
            values["held_out_base_seed"],
            "--concurrency",
            values["concurrency"],
            "--tick-batches",
            values["tick_batches"],
            "--samples",
            values["samples"],
            "--repetitions",
            values["repetitions"],
            "--workload-profile",
            values["workload_profile"],
        ]

    def assert_json_hold(
        self,
        result: subprocess.CompletedProcess[str],
        reason_code: str,
    ) -> dict[str, object]:
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("usage:", result.stderr.lower())
        self.assertNotIn("traceback", result.stderr.lower())
        lines = result.stderr.splitlines()
        self.assertEqual(len(lines), 1, result.stderr)
        terminal = json.loads(lines[0])
        self.assertEqual(terminal["marker"], record_contract.HANDOFF_MARKER)
        self.assertEqual(terminal["status"], "HOLD")
        self.assertEqual(terminal["reason_code"], reason_code)
        self.assertEqual(terminal["runtime_evidence"], "PENDING_DESIGNATED_HOST")
        self.assertEqual(terminal["runtime_execution_authority"], "NONE")
        self.assertEqual(terminal["model_weight_mutation_authority"], "NONE")
        self.assertEqual(terminal["corpus_admission_authority"], "NONE")
        self.assertEqual(terminal["automatic_promotion_authority"], "NONE")
        return terminal

    def test_fresh_process_record_then_restart_resume_validation(self) -> None:
        created = self.run_cli(*self.record_args())
        self.assertEqual(created.returncode, 0, created.stderr)
        created_summary = json.loads(created.stdout)
        self.assertEqual(created_summary["status"], "PRECOMMIT_RECORDED")
        self.assertEqual(created_summary["runtime_execution_authority"], "NONE")
        self.assertEqual(created_summary["automatic_promotion_authority"], "NONE")

        info = self.record_path.stat()
        self.assertEqual(stat.S_IMODE(info.st_mode), 0o600)
        self.assertEqual(info.st_nlink, 1)
        before = self.record_path.read_bytes()

        resumed = self.run_cli(
            "validate",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
        )
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        resumed_summary = json.loads(resumed.stdout)
        self.assertEqual(resumed_summary["status"], "PRECOMMIT_REVALIDATED")
        self.assertEqual(resumed_summary["record_digest"], created_summary["record_digest"])
        self.assertEqual(resumed_summary["plan_digest"], created_summary["plan_digest"])
        self.assertEqual(self.record_path.read_bytes(), before)

    def test_existing_record_collision_cannot_be_overwritten_by_posthoc_plan(self) -> None:
        created = self.run_cli(*self.record_args())
        self.assertEqual(created.returncode, 0, created.stderr)
        before = self.record_path.read_bytes()

        posthoc = self.run_cli(*self.record_args(tick_batches="1,16"))
        self.assertEqual(posthoc.returncode, 2)
        self.assertIn("create-only precommit refused", posthoc.stderr)
        self.assertEqual(self.record_path.read_bytes(), before)

    def test_record_byte_tamper_fails_fresh_process_validation(self) -> None:
        created = self.run_cli(*self.record_args())
        self.assertEqual(created.returncode, 0, created.stderr)
        obj = json.loads(self.record_path.read_text(encoding="utf-8"))
        obj["plan"]["shared_parameters"]["tick_batches"] = [1, 16]
        self.record_path.write_text(
            record_contract.canonical_json(obj) + "\n",
            encoding="utf-8",
        )
        os.chmod(self.record_path, 0o600)

        resumed = self.run_cli(
            "validate",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
        )
        self.assertEqual(resumed.returncode, 2)
        self.assertIn("HOLD", resumed.stderr)

    def test_changed_split_manifest_cannot_resume_record(self) -> None:
        created = self.run_cli(*self.record_args())
        self.assertEqual(created.returncode, 0, created.stderr)

        changed_manifest = split.build_manifest(
            "singles.oramap",
            tuple(range(1000, 1008)),
            tuple(range(3000, 3008)),
        )
        self.manifest_path.write_text(
            record_contract.canonical_json(changed_manifest) + "\n",
            encoding="utf-8",
        )

        resumed = self.run_cli(
            "validate",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
        )
        self.assertEqual(resumed.returncode, 2)
        self.assertIn("HOLD", resumed.stderr)

    def test_noncanonical_cli_seed_and_overdomain_counts_fail_before_record(self) -> None:
        leading_zero = self.run_cli(*self.record_args(held_out_base_seed="02000"))
        self.assertEqual(leading_zero.returncode, 2)
        self.assertFalse(self.record_path.exists())

        samples_over = self.run_cli(*self.record_args(samples="1001"))
        self.assertEqual(samples_over.returncode, 2)
        self.assertFalse(self.record_path.exists())

        repetitions_over = self.run_cli(*self.record_args(repetitions="11"))
        self.assertEqual(repetitions_over.returncode, 2)
        self.assertFalse(self.record_path.exists())

    def test_overlong_numeric_tokens_fail_inside_json_hold_before_int_conversion(self) -> None:
        scalar = self.run_cli(*self.record_args(samples="9" * 5000))
        scalar_terminal = self.assert_json_hold(scalar, "NUMERIC_ARGUMENT_ERROR")
        self.assertIn("samples must be in 1..1000", scalar_terminal["reason"])
        self.assertFalse(self.record_path.exists())

        csv_token = self.run_cli(*self.record_args(tick_batches="1," + ("9" * 5000)))
        csv_terminal = self.assert_json_hold(csv_token, "NUMERIC_ARGUMENT_ERROR")
        self.assertIn("tick_batches must be in 1..10000", csv_terminal["reason"])
        self.assertFalse(self.record_path.exists())

    def test_exact_numeric_upper_bound_controls_remain_admissible(self) -> None:
        created = self.run_cli(
            *self.record_args(
                concurrency="1",
                tick_batches="1,10000",
                samples="1000",
                repetitions="10",
            )
        )
        self.assertEqual(created.returncode, 0, created.stderr)
        summary = json.loads(created.stdout)
        self.assertEqual(summary["status"], "PRECOMMIT_RECORDED")

    def test_argument_errors_use_one_machine_readable_hold_terminal(self) -> None:
        missing_args = self.record_args()
        index = missing_args.index("--samples")
        del missing_args[index:index + 2]
        missing = self.run_cli(*missing_args)
        missing_terminal = self.assert_json_hold(missing, "ARGUMENT_ERROR")
        self.assertIn("required", missing_terminal["reason"])
        self.assertFalse(self.record_path.exists())

        unknown = self.run_cli(
            "validate",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
            "--unknown-option",
        )
        unknown_terminal = self.assert_json_hold(unknown, "ARGUMENT_ERROR")
        self.assertIn("unrecognized arguments", unknown_terminal["reason"])
        self.assertFalse(self.record_path.exists())

        invalid_choice = self.run_cli(*self.record_args(workload_profile="not-a-profile"))
        invalid_terminal = self.assert_json_hold(invalid_choice, "ARGUMENT_ERROR")
        self.assertIn("invalid choice", invalid_terminal["reason"])
        self.assertFalse(self.record_path.exists())

        help_result = self.run_cli("--help")
        self.assertEqual(help_result.returncode, 0)
        self.assertEqual(help_result.stderr, "")
        self.assertIn("record", help_result.stdout)
        self.assertIn("validate", help_result.stdout)

    def test_duplicate_single_value_options_fail_before_any_publication(self) -> None:
        duplicate_cases = (
            ("--record-id", "eval-002"),
            ("--benchmark-source-sha", "b" * 40),
            ("--manifest", str(self.manifest_path)),
            ("--record", str(self.root / "shadow.json")),
            ("--samples", "3"),
        )
        for option, value in duplicate_cases:
            with self.subTest(option=option):
                attempt = self.run_cli(*self.record_args(), option, value)
                terminal = self.assert_json_hold(attempt, "ARGUMENT_ERROR")
                self.assertIn(
                    f"argument {option}: may not be repeated",
                    terminal["reason"],
                )
                self.assertFalse(self.record_path.exists())
                self.assertFalse((self.root / "shadow.json").exists())

        equals_form = self.run_cli(
            *self.record_args(),
            "--record-id=eval-002",
        )
        equals_terminal = self.assert_json_hold(equals_form, "ARGUMENT_ERROR")
        self.assertIn(
            "argument --record-id: may not be repeated",
            equals_terminal["reason"],
        )
        self.assertFalse(self.record_path.exists())

        validate_duplicate = self.run_cli(
            "validate",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
            "--manifest",
            str(self.manifest_path),
        )
        validate_terminal = self.assert_json_hold(
            validate_duplicate,
            "ARGUMENT_ERROR",
        )
        self.assertIn(
            "argument --manifest: may not be repeated",
            validate_terminal["reason"],
        )
        self.assertFalse(self.record_path.exists())

    def test_hardlink_or_symlink_record_authority_fails_closed(self) -> None:
        created = self.run_cli(*self.record_args())
        self.assertEqual(created.returncode, 0, created.stderr)

        alias = self.root / "alias.json"
        os.link(self.record_path, alias)
        resumed = self.run_cli(
            "validate",
            "--manifest",
            str(self.manifest_path),
            "--record",
            str(self.record_path),
        )
        self.assertEqual(resumed.returncode, 2)
        self.assertIn("exactly one hard link", resumed.stderr)
        alias.unlink()

        foreign = self.root / "foreign.json"
        foreign.write_text("foreign\n", encoding="utf-8")
        symlink_record = self.root / "symlink-record.json"
        symlink_record.symlink_to(foreign)
        original = foreign.read_bytes()
        attempt = self.run_cli(
            *[
                arg if arg != str(self.record_path) else str(symlink_record)
                for arg in self.record_args(record_id="eval-002")
            ]
        )
        self.assertEqual(attempt.returncode, 2)
        self.assertEqual(foreign.read_bytes(), original)

    def test_record_schema_keeps_all_execution_and_promotion_authority_none(self) -> None:
        created = self.run_cli(*self.record_args())
        self.assertEqual(created.returncode, 0, created.stderr)
        record = json.loads(self.record_path.read_text(encoding="utf-8"))
        policy = record["record_policy"]
        self.assertIs(policy["recorded_before_calibration_required"], True)
        self.assertIs(policy["create_only_publication"], True)
        self.assertEqual(policy["external_timestamp_authority"], "NONE")
        self.assertEqual(policy["signature_authority"], "NONE")
        for field in (
            "overwrite_authority",
            "delete_replace_authority",
            "runtime_execution_authority",
            "model_weight_mutation_authority",
            "corpus_admission_authority",
            "automatic_promotion_authority",
        ):
            self.assertEqual(policy[field], "NONE")


if __name__ == "__main__":
    unittest.main()
