from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bench_joint_advance as bench
from test_bench_joint_advance import EvidencePublicationTests


class PostCommitImmutabilityTests(unittest.TestCase):
    def test_pending_retirement_exception_after_receipt_cannot_rewrite_final(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = EvidencePublicationTests.payload()
            with mock.patch(
                "bench_joint_advance._retire_pending",
                side_effect=OSError("fixture post-commit retirement failure"),
            ):
                publication = bench.publish_evidence_create_only(output, payload)

            self.assertEqual(output.read_bytes(), payload)
            self.assertEqual(
                hashlib.sha256(output.read_bytes()).hexdigest(),
                hashlib.sha256(payload).hexdigest(),
            )
            self.assertTrue(publication["commit_receipt"])
            self.assertTrue(publication["post_commit_verification_errors"])
            local = bench.load_locally_committed_evidence(
                output, EvidencePublicationTests.operation(payload),
            )
            self.assertEqual(local["report"]["run"]["terminal"], "completed")
            self.assertFalse(local["countable"])

    def test_replacement_after_pending_generation_check_is_never_deleted(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = bench._pending_path(output)
            payload = EvidencePublicationTests.payload()
            replacement = b"foreign-pending-generation\n"
            real_assert = bench._assert_entry_generation
            pending_checks = 0

            def replace_after_second_pending_check(
                parent_descriptor, name, descriptor, label,
            ):
                nonlocal pending_checks
                result = real_assert(parent_descriptor, name, descriptor, label)
                if label == "pending":
                    pending_checks += 1
                    if pending_checks == 2:
                        os.unlink(name, dir_fd=parent_descriptor)
                        flags = (
                            os.O_CREAT
                            | os.O_EXCL
                            | os.O_WRONLY
                            | getattr(os, "O_NOFOLLOW", 0)
                        )
                        replacement_descriptor = os.open(
                            name, flags, 0o400, dir_fd=parent_descriptor,
                        )
                        try:
                            os.write(replacement_descriptor, replacement)
                            os.fchmod(replacement_descriptor, 0o400)
                            os.fsync(replacement_descriptor)
                        finally:
                            os.close(replacement_descriptor)
                        bench._fsync_directory(parent_descriptor)
                return result

            with mock.patch(
                "bench_joint_advance._assert_entry_generation",
                side_effect=replace_after_second_pending_check,
            ):
                publication = bench.publish_evidence_create_only(output, payload)

            self.assertEqual(pending_checks, 2)
            self.assertTrue(pending.exists())
            self.assertEqual(pending.read_bytes(), replacement)
            self.assertFalse(publication["pending_retired"])
            self.assertIsNone(publication["pending_retirement_error"])
            self.assertEqual(output.read_bytes(), payload)
            self.assertTrue(publication["commit_receipt"])

    def test_commit_receipt_post_fsync_verification_failure_is_warning_not_rewrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = EvidencePublicationTests.payload()
            real_assert = bench._assert_entry_generation

            def fail_commit_receipt(parent_descriptor, name, descriptor, label):
                if label == "commit receipt":
                    raise bench.ContractError("fixture post-commit receipt verification failure")
                return real_assert(parent_descriptor, name, descriptor, label)

            with mock.patch(
                "bench_joint_advance._assert_entry_generation",
                side_effect=fail_commit_receipt,
            ):
                publication = bench.publish_evidence_create_only(output, payload)

            self.assertEqual(output.read_bytes(), payload)
            self.assertTrue(publication["commit_receipt"])
            self.assertTrue(
                any("commit receipt" in error for error in publication["post_commit_verification_errors"])
            )
            local = bench.load_locally_committed_evidence(
                output, EvidencePublicationTests.operation(payload),
            )
            self.assertEqual(local["report"]["run"]["terminal"], "completed")

    def test_precommit_failure_still_raises_and_preserves_pending_failure_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = EvidencePublicationTests.payload()
            with mock.patch(
                "bench_joint_advance._link_open_inode_create_only",
                side_effect=OSError("fixture precommit link failure"),
            ):
                with self.assertRaises(OSError):
                    bench.publish_evidence_create_only(output, payload)
            self.assertFalse(output.exists())
            pending = bench._pending_path(output)
            self.assertTrue(pending.exists())
            self.assertEqual(pending.read_bytes(), payload)
            self.assertFalse(bench._commit_receipt_path(output).exists())


if __name__ == "__main__":
    unittest.main()
