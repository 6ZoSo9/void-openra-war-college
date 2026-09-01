#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import darwin_evaluation_precommit_record_recovery_v1 as recovery
import darwin_evaluation_precommit_record_v1 as record_contract
import darwin_heldout_evaluation_split_v1 as split
import darwin_precommitted_evaluation_plan_v1 as plan_contract

CLI = Path(__file__).with_name(
    "darwin_evaluation_precommit_record_recovery_v1.py"
)
BASE_CLI = Path(__file__).with_name("darwin_evaluation_precommit_record_v1.py")


class EvaluationPrecommitRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / "precommit.json"
        self.manifest = split.build_manifest(
            "singles.oramap",
            tuple(range(1000, 1008)),
            tuple(range(2000, 2008)),
        )
        self.plan = plan_contract.build_precommitted_evaluation_plan(
            self.manifest,
            "b" * 40,
            1000,
            2000,
            (1, 4),
            (1, 8),
            2,
            2,
            "noop_control",
        )
        self.record = record_contract.build_record("eval-recovery-001", self.manifest, self.plan)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def record_args(self) -> list[str]:
        return [
            "record",
            "--manifest",
            str(self.root / "split.json"),
            "--record",
            str(self.path),
            "--record-id",
            "eval-recovery-001",
            "--benchmark-source-sha",
            "b" * 40,
            "--calibration-base-seed",
            "1000",
            "--held-out-base-seed",
            "2000",
            "--concurrency",
            "1,4",
            "--tick-batches",
            "1,8",
            "--samples",
            "2",
            "--repetitions",
            "2",
            "--workload-profile",
            "noop_control",
        ]

    def assert_duplicate_rejected_before_io(self, argv: list[str], option: str) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(recovery, "_load_manifest") as load_manifest:
            with mock.patch.object(recovery.os, "open") as open_file:
                with mock.patch.object(recovery.os, "fsync") as fsync_file:
                    with mock.patch.object(record_contract, "_fsync_parent") as fsync_parent:
                        with contextlib.redirect_stdout(stdout):
                            with contextlib.redirect_stderr(stderr):
                                return_code = recovery.main(argv)

        self.assertEqual(return_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        lines = stderr.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        terminal = json.loads(lines[0])
        self.assertEqual(terminal["marker"], recovery.HANDOFF_MARKER)
        self.assertEqual(terminal["status"], "HOLD")
        self.assertEqual(terminal["reason_code"], "ARGUMENT_ERROR")
        self.assertIn(
            f"argument {option}: may not be repeated",
            terminal["reason"],
        )
        load_manifest.assert_not_called()
        open_file.assert_not_called()
        fsync_file.assert_not_called()
        fsync_parent.assert_not_called()
        self.assertFalse(self.path.exists())

    def test_duplicate_options_fail_before_manifest_open_or_fsync(self) -> None:
        record_cases = (
            ("--manifest", str(self.root / "other-split.json")),
            ("--record", str(self.root / "other-record.json")),
            ("--record-id", "eval-recovery-002"),
            ("--benchmark-source-sha", "c" * 40),
            ("--samples", "3"),
        )
        for option, value in record_cases:
            with self.subTest(command="record", option=option):
                self.assert_duplicate_rejected_before_io(
                    [*self.record_args(), option, value],
                    option,
                )

        for command in ("validate", "recover"):
            for option, value in (
                ("--manifest", str(self.root / "other-split.json")),
                ("--record", str(self.root / "other-record.json")),
            ):
                with self.subTest(command=command, option=option):
                    self.assert_duplicate_rejected_before_io(
                        [
                            command,
                            "--manifest",
                            str(self.root / "split.json"),
                            "--record",
                            str(self.path),
                            option,
                            value,
                        ],
                        option,
                    )

    def test_duplicate_equals_form_is_one_machine_hold_terminal(self) -> None:
        attempt = subprocess.run(
            [
                sys.executable,
                str(CLI),
                *self.record_args(),
                "--record-id=eval-recovery-002",
            ],
            cwd=Path(__file__).parent,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )
        self.assertEqual(attempt.returncode, 2)
        self.assertEqual(attempt.stdout, "")
        self.assertNotIn("usage:", attempt.stderr.lower())
        self.assertNotIn("traceback", attempt.stderr.lower())
        lines = attempt.stderr.splitlines()
        self.assertEqual(len(lines), 1)
        terminal = json.loads(lines[0])
        self.assertEqual(terminal["marker"], recovery.HANDOFF_MARKER)
        self.assertEqual(terminal["status"], "HOLD")
        self.assertEqual(terminal["reason_code"], "ARGUMENT_ERROR")
        self.assertIn(
            "argument --record-id: may not be repeated",
            terminal["reason"],
        )
        self.assertFalse(self.path.exists())

    def test_long_option_abbreviations_fail_before_manifest_open_or_fsync(self) -> None:
        shadow_manifest = self.root / "shadow-split.json"
        cases = (
            [
                "recover",
                "--mani",
                str(shadow_manifest),
                "--manifest",
                str(self.root / "split.json"),
                "--record",
                str(self.path),
            ],
            [
                "recover",
                "--manifest",
                str(self.root / "split.json"),
                "--mani",
                str(shadow_manifest),
                "--record",
                str(self.path),
            ],
            [
                "recover",
                f"--man={shadow_manifest}",
                f"--manifest={self.root / 'split.json'}",
                f"--record={self.path}",
            ],
        )
        for argv in cases:
            with self.subTest(argv=argv):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with mock.patch.object(recovery, "_load_manifest") as load_manifest:
                    with mock.patch.object(recovery.os, "open") as open_file:
                        with mock.patch.object(recovery.os, "fsync") as fsync_file:
                            with mock.patch.object(
                                record_contract,
                                "_fsync_parent",
                            ) as fsync_parent:
                                with contextlib.redirect_stdout(stdout):
                                    with contextlib.redirect_stderr(stderr):
                                        return_code = recovery.main(argv)

                self.assertEqual(return_code, 2)
                self.assertEqual(stdout.getvalue(), "")
                lines = stderr.getvalue().splitlines()
                self.assertEqual(len(lines), 1)
                terminal = json.loads(lines[0])
                self.assertEqual(terminal["marker"], recovery.HANDOFF_MARKER)
                self.assertEqual(terminal["status"], "HOLD")
                self.assertEqual(terminal["reason_code"], "ARGUMENT_ERROR")
                self.assertIn("unrecognized arguments:", terminal["reason"])
                load_manifest.assert_not_called()
                open_file.assert_not_called()
                fsync_file.assert_not_called()
                fsync_parent.assert_not_called()
                self.assertFalse(self.path.exists())
                self.assertFalse(shadow_manifest.exists())

        subprocess_cases = (
            cases[0],
            cases[1],
            cases[2],
        )
        for argv in subprocess_cases:
            with self.subTest(subprocess_argv=argv):
                attempt = subprocess.run(
                    [sys.executable, str(CLI), *argv],
                    cwd=Path(__file__).parent,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=10,
                )
                self.assertEqual(attempt.returncode, 2)
                self.assertEqual(attempt.stdout, "")
                self.assertNotIn("usage:", attempt.stderr.lower())
                self.assertNotIn("traceback", attempt.stderr.lower())
                lines = attempt.stderr.splitlines()
                self.assertEqual(len(lines), 1)
                terminal = json.loads(lines[0])
                self.assertEqual(terminal["marker"], recovery.HANDOFF_MARKER)
                self.assertEqual(terminal["status"], "HOLD")
                self.assertEqual(terminal["reason_code"], "ARGUMENT_ERROR")
                self.assertIn("unrecognized arguments:", terminal["reason"])
                self.assertFalse(self.path.exists())
                self.assertFalse(shadow_manifest.exists())

        base_cases = (
            [
                "record",
                "--mani",
                str(shadow_manifest),
                *self.record_args()[1:],
            ],
            [
                *self.record_args(),
                "--mani",
                str(shadow_manifest),
            ],
            [
                "record",
                f"--man={shadow_manifest}",
                *self.record_args()[1:],
            ],
        )
        for argv in base_cases:
            with self.subTest(base_subprocess_argv=argv):
                attempt = subprocess.run(
                    [sys.executable, str(BASE_CLI), *argv],
                    cwd=Path(__file__).parent,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=10,
                )
                self.assertEqual(attempt.returncode, 2)
                self.assertEqual(attempt.stdout, "")
                self.assertNotIn("usage:", attempt.stderr.lower())
                self.assertNotIn("traceback", attempt.stderr.lower())
                lines = attempt.stderr.splitlines()
                self.assertEqual(len(lines), 1)
                terminal = json.loads(lines[0])
                self.assertEqual(terminal["marker"], record_contract.HANDOFF_MARKER)
                self.assertEqual(terminal["status"], "HOLD")
                self.assertEqual(terminal["reason_code"], "ARGUMENT_ERROR")
                self.assertIn("unrecognized arguments:", terminal["reason"])
                self.assertFalse(self.path.exists())
                self.assertFalse(shadow_manifest.exists())

    def test_parent_fsync_failure_is_machine_recoverable_without_replacement(self) -> None:
        with mock.patch.object(
            record_contract,
            "_fsync_parent",
            side_effect=record_contract.RecordError("synthetic parent fsync failure"),
        ):
            with self.assertRaises(recovery.PublicationDurabilityUncertain):
                recovery.write_record_create_only_with_terminal(self.path, self.record)

        before = self.path.read_bytes()
        before_stat = self.path.stat()
        self.assertEqual(stat.S_IMODE(before_stat.st_mode), 0o600)
        self.assertEqual(before_stat.st_nlink, 1)

        recovered = recovery.recover_existing_record(self.path, self.manifest)
        after_stat = self.path.stat()
        self.assertEqual(recovered["record_digest"], self.record["record_digest"])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual((after_stat.st_dev, after_stat.st_ino), (before_stat.st_dev, before_stat.st_ino))

        terminal = json.loads(
            recovery._summary(
                "PRECOMMIT_RECOVERED",
                recovered,
                "RECOVERY_PARENT_DIRECTORY_FSYNC_CONFIRMED",
                "RESTART_CALIBRATION_AFTER_THIS_RECOVERY_TERMINAL",
            )
        )
        self.assertEqual(terminal["prior_calibration_evidence_authority"], "NONE")
        self.assertEqual(terminal["retroactive_precalibration_time_authority"], "NONE")
        self.assertEqual(terminal["runtime_execution_authority"], "NONE")
        self.assertEqual(terminal["automatic_promotion_authority"], "NONE")

    def test_recovery_reestablishes_file_fsync_before_parent_terminal(self) -> None:
        payload = (record_contract.canonical_json(self.record) + "\n").encode("utf-8")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(self.path, flags, 0o600)
        try:
            os.write(fd, payload)
        finally:
            os.close(fd)

        events: list[str] = []
        original_fsync = os.fsync
        original_parent_fsync = record_contract._fsync_parent

        def observe_fsync(fd: int) -> None:
            events.append("file_fsync")
            original_fsync(fd)

        def observe_parent(path: Path) -> None:
            events.append("parent_fsync")
            original_parent_fsync(path)

        with mock.patch.object(recovery.os, "fsync", side_effect=observe_fsync):
            with mock.patch.object(record_contract, "_fsync_parent", side_effect=observe_parent):
                recovered = recovery.recover_existing_record(self.path, self.manifest)

        self.assertEqual(recovered["record_digest"], self.record["record_digest"])
        self.assertGreaterEqual(len(events), 2)
        self.assertEqual(events[:2], ["file_fsync", "parent_fsync"])

    def test_terminal_loss_after_parent_fsync_converges_without_byte_or_inode_change(self) -> None:
        recovery.write_record_create_only_with_terminal(self.path, self.record)
        before = self.path.read_bytes()
        before_stat = self.path.stat()

        recovered = recovery.recover_existing_record(self.path, self.manifest)
        after_stat = self.path.stat()

        self.assertEqual(recovered["record_digest"], self.record["record_digest"])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual((after_stat.st_dev, after_stat.st_ino), (before_stat.st_dev, before_stat.st_ino))

    def test_recovery_detects_same_path_replacement_and_does_not_delete_foreign(self) -> None:
        recovery.write_record_create_only_with_terminal(self.path, self.record)
        original_parent_fsync = record_contract._fsync_parent
        foreign_bytes = b"foreign replacement\n"

        def replace_then_sync(path: Path) -> None:
            held = self.root / "held-original.json"
            os.replace(self.path, held)
            self.path.write_bytes(foreign_bytes)
            os.chmod(self.path, 0o600)
            original_parent_fsync(path)

        with mock.patch.object(record_contract, "_fsync_parent", side_effect=replace_then_sync):
            with self.assertRaises(recovery.RecoveryError):
                recovery.recover_existing_record(self.path, self.manifest)

        self.assertEqual(self.path.read_bytes(), foreign_bytes)

    def test_record_success_terminal_reports_exact_published_generation_not_later_pathname(self) -> None:
        manifest_path = self.root / "split.json"
        manifest_path.write_text(
            record_contract.canonical_json(self.manifest) + "\n",
            encoding="utf-8",
        )
        foreign_record = record_contract.build_record(
            "foreign-valid-001",
            self.manifest,
            self.plan,
        )
        expected_foreign_bytes = (
            record_contract.canonical_json(foreign_record) + "\n"
        ).encode("utf-8")

        args = argparse.Namespace(
            manifest=str(manifest_path),
            record=str(self.path),
            record_id="eval-recovery-001",
            benchmark_source_sha="b" * 40,
            calibration_base_seed="1000",
            held_out_base_seed="2000",
            concurrency="1,4",
            tick_batches="1,8",
            samples="2",
            repetitions="2",
            workload_profile="noop_control",
        )

        original_writer = recovery.write_record_create_only_with_terminal

        def publish_then_substitute(path: Path, record: dict[str, object]) -> None:
            original_writer(path, record)
            held = self.root / "published-a.json"
            os.replace(path, held)
            original_writer(path, foreign_record)

        with mock.patch.object(
            recovery,
            "write_record_create_only_with_terminal",
            side_effect=publish_then_substitute,
        ):
            published = recovery._record_command(args)

        terminal = json.loads(
            recovery._summary(
                "PRECOMMIT_RECORDED",
                published,
                "PARENT_DIRECTORY_FSYNC_CONFIRMED",
                "CALIBRATION_MAY_START_FROM_THIS_TERMINAL",
            )
        )
        visible = record_contract.load_and_validate_record(self.path, self.manifest)

        self.assertEqual(published["record_id"], self.record["record_id"])
        self.assertEqual(published["record_digest"], self.record["record_digest"])
        self.assertEqual(terminal["record_id"], self.record["record_id"])
        self.assertEqual(terminal["record_digest"], self.record["record_digest"])
        self.assertEqual(visible["record_id"], foreign_record["record_id"])
        self.assertEqual(visible["record_digest"], foreign_record["record_digest"])
        self.assertEqual(self.path.read_bytes(), expected_foreign_bytes)
        self.assertNotEqual(terminal["record_digest"], visible["record_digest"])
        self.assertEqual(terminal["prior_calibration_evidence_authority"], "NONE")
        self.assertEqual(terminal["runtime_execution_authority"], "NONE")

    def test_validate_terminal_is_content_only_not_durability_authority(self) -> None:
        recovery.write_record_create_only_with_terminal(self.path, self.record)
        validated = record_contract.load_and_validate_record(self.path, self.manifest)
        terminal = json.loads(
            recovery._summary(
                "PRECOMMIT_CONTENT_REVALIDATED",
                validated,
                "CONTENT_ONLY_NOT_PUBLICATION_TERMINAL",
                "USE_RECOVER_IF_PUBLICATION_TERMINAL_WAS_LOST_OR_UNCERTAIN",
            )
        )
        self.assertEqual(terminal["publication_terminal"], "CONTENT_ONLY_NOT_PUBLICATION_TERMINAL")
        self.assertEqual(terminal["prior_calibration_evidence_authority"], "NONE")
        self.assertEqual(terminal["runtime_evidence"], "PENDING_DESIGNATED_HOST")


if __name__ == "__main__":
    unittest.main()
