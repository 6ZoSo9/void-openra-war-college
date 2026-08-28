from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

import bench_joint_advance as bench


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "inspect_joint_advance_evidence.py"
SPEC = importlib.util.spec_from_file_location("inspect_joint_advance_evidence", SOURCE)
assert SPEC is not None and SPEC.loader is not None
INSPECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSPECT)


def write_0400(path: Path, payload: bytes) -> None:
    path.write_bytes(payload)
    path.chmod(0o400)


def generation(path: Path):
    if not path.exists():
        return None
    meta = path.lstat()
    return (
        meta.st_dev,
        meta.st_ino,
        stat.S_IMODE(meta.st_mode),
        meta.st_size,
        meta.st_mtime_ns,
        meta.st_ctime_ns,
        hashlib.sha256(path.read_bytes()).hexdigest(),
    )


class ReadOnlyInspectionTests(unittest.TestCase):
    def test_empty_namespace_is_classified_without_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report = INSPECT.inspect_namespace(output)
            self.assertEqual(report["classification"], "EMPTY")
            self.assertTrue(report["inspection_read_only"])
            self.assertFalse(report["countable"])
            self.assertFalse(output.exists())
            self.assertFalse(bench._pending_path(output).exists())
            self.assertFalse(bench._commit_receipt_path(output).exists())

    def test_empty_pending_reservation_is_preserved_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = bench._pending_path(output)
            write_0400(pending, b"")
            before = generation(pending)
            report = INSPECT.inspect_namespace(output)
            after = generation(pending)
            self.assertEqual(before, after)
            self.assertEqual(report["classification"], "PENDING_RESERVATION_ONLY")
            self.assertFalse(report["pending"]["report_schema_valid"])
            self.assertEqual(report["pending"]["validation_error"], "EMPTY_PENDING_RESERVATION")
            self.assertTrue(report["namespace_generation_stable"])

    def test_final_without_receipt_is_preserved_and_never_promoted(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            write_0400(output, b"not-authoritative\n")
            before = generation(output)
            report = INSPECT.inspect_namespace(output)
            self.assertEqual(before, generation(output))
            self.assertEqual(report["classification"], "FINAL_WITHOUT_RECEIPT")
            self.assertFalse(report["final"]["report_schema_valid"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_receipt_binding_is_reported_local_untrusted_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = b"opaque-final-bytes\n"
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, receipt)}
            report = INSPECT.inspect_namespace(output)
            after = {str(p): generation(p) for p in (output, receipt)}
            self.assertEqual(before, after)
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")

    def test_pending_and_final_without_receipt_remain_explicitly_ambiguous(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = bench._pending_path(output)
            write_0400(output, b"same-inode-not-required-for-inspection\n")
            write_0400(pending, b"pending-copy\n")
            before = {str(p): generation(p) for p in (output, pending)}
            report = INSPECT.inspect_namespace(output)
            self.assertEqual(before, {str(p): generation(p) for p in (output, pending)})
            self.assertEqual(report["classification"], "FINAL_AND_PENDING_WITHOUT_RECEIPT")
            self.assertFalse(report["automatic_link"])
            self.assertFalse(report["automatic_delete"])

    def test_receipt_without_final_is_hold_and_not_recovered(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, b"{}\n")
            before = generation(receipt)
            report = INSPECT.inspect_namespace(output)
            self.assertEqual(before, generation(receipt))
            self.assertEqual(report["classification"], "RECEIPT_WITHOUT_FINAL_HOLD")
            self.assertFalse(report["automatic_recovery"])

    def test_symlink_is_never_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "evidence.json"
            target = root / "foreign.txt"
            target.write_text("foreign\n", encoding="utf-8")
            output.symlink_to(target)
            target_before = target.read_bytes()
            report = INSPECT.inspect_namespace(output)
            self.assertEqual(report["final"]["validation_error"], "ARTIFACT_NOT_REGULAR_FILE")
            self.assertEqual(target.read_bytes(), target_before)
            self.assertFalse(report["countable"])


if __name__ == "__main__":
    unittest.main()
