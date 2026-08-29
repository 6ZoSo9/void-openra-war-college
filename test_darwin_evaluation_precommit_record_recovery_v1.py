#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import darwin_evaluation_precommit_record_recovery_v1 as recovery
import darwin_evaluation_precommit_record_v1 as record_contract
import darwin_heldout_evaluation_split_v1 as split
import darwin_precommitted_evaluation_plan_v1 as plan_contract


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
