from __future__ import annotations

import contextlib
import hashlib
import importlib.util
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

import bench_joint_advance as bench
import test_bench_joint_advance as benchmark_tests


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


def valid_report_payload() -> bytes:
    return benchmark_tests.EvidencePublicationTests.payload()


class ReadOnlyInspectionTests(unittest.TestCase):
    def assert_inspection_failure_terminal(self, report, reason_code):
        self.assertEqual(report, {
            "marker": INSPECT.INSPECTION_MARKER,
            "schema_version": INSPECT.INSPECTION_SCHEMA_VERSION,
            "output_path": report["output_path"],
            "classification": "INSPECTION_ERROR_HOLD",
            "reason_code": reason_code,
            "error_type": report["error_type"],
            "artifacts_inspected": False,
            "artifact_authority": "NONE",
            "countable": False,
            "producer_authentication": "ABSENT",
            "inspection_read_only": True,
            "automatic_recovery": False,
            "automatic_delete": False,
            "automatic_link": False,
            "automatic_rewrite": False,
            "namespace_generation_stable": False,
        })

    def test_cli_missing_parent_emits_one_machine_readable_failure_terminal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "missing" / "evidence.json"
            before = list(root.iterdir())
            result = subprocess.run(
                [sys.executable, str(SOURCE), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            after = list(root.iterdir())
            self.assertEqual(result.returncode, 2)
            self.assertEqual(len(result.stdout.strip().splitlines()), 1)
            report = json.loads(result.stdout)
            self.assert_inspection_failure_terminal(report, "OUTPUT_PARENT_NOT_FOUND")
            self.assertEqual(report["output_path"], str(output))
            self.assertIn("OUTPUT_PARENT_NOT_FOUND", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(before, after)

    def test_cli_namespace_instability_emits_stable_nonmutating_failure_terminal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "evidence.json"
            before = list(root.iterdir())
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(
                INSPECT,
                "_require_retained_namespace_stable",
                side_effect=INSPECT.InspectionFailure(
                    "NAMESPACE_GENERATION_UNSTABLE",
                    "injected retained-namespace instability",
                ),
            ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                returncode = INSPECT.main(["--output", str(output)])
            after = list(root.iterdir())
            self.assertEqual(returncode, 2)
            self.assertEqual(len(stdout.getvalue().strip().splitlines()), 1)
            report = json.loads(stdout.getvalue())
            self.assert_inspection_failure_terminal(
                report, "NAMESPACE_GENERATION_UNSTABLE",
            )
            self.assertEqual(report["output_path"], str(output))
            self.assertIn("NAMESPACE_GENERATION_UNSTABLE", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertEqual(before, after)

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
            payload = valid_report_payload()
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, receipt)}
            report = INSPECT.inspect_namespace(output)
            after = {str(p): generation(p) for p in (output, receipt)}
            self.assertEqual(before, after)
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertTrue(report["final"]["report_schema_valid"])
            self.assertEqual(report["final"]["report_cell_terminals"], ["success"])
            self.assertEqual(report["final"]["report_matrix_summary"], {
                "cell_count": 1,
                "success_count": 1,
                "non_success_count": 0,
                "blocked_cell_count": 0,
                "first_non_success": None,
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")

    def test_receipt_bound_completed_failure_reports_matrix_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = benchmark_tests.EvidencePublicationTests.completed_failure_payload()
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, receipt)}

            report = INSPECT.inspect_namespace(output)

            self.assertEqual(before, {str(p): generation(p) for p in (output, receipt)})
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertTrue(report["final"]["report_schema_valid"])
            self.assertEqual(
                report["final"]["report_cell_terminals"],
                ["timeout", "not_executed"],
            )
            self.assertEqual(report["final"]["report_matrix_summary"], {
                "cell_count": 2,
                "success_count": 0,
                "non_success_count": 2,
                "blocked_cell_count": 1,
                "first_non_success": {"key": "c1-t1", "terminal": "timeout"},
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_receipt_bound_current_schema_invalid_report_is_explicit_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_payload = json.loads(
                benchmark_tests.EvidencePublicationTests.completed_failure_payload()
            )
            self.assertEqual(report_payload["schema_version"], 9)
            report_payload["cells"][1]["blocked_by"] = "c1-t8"
            payload = bench.stable_json(report_payload).encode("utf-8")
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, receipt)}

            report = INSPECT.inspect_namespace(output)

            self.assertEqual(before, {str(p): generation(p) for p in (output, receipt)})
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(report["final"]["report_schema_valid"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_prior_schema_eight_unbound_blocker_is_preserved_as_incompatible_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_payload = json.loads(
                benchmark_tests.EvidencePublicationTests.completed_failure_payload()
            )
            self.assertEqual(report_payload["schema_version"], 9)
            report_payload["schema_version"] = 8
            report_payload["cells"][1]["blocked_by"] = "c1-t8"
            payload = bench.stable_json(report_payload).encode("utf-8")
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, receipt)}

            report = INSPECT.inspect_namespace(output)

            self.assertEqual(before, {str(p): generation(p) for p in (output, receipt)})
            self.assertEqual(report["classification"], "INCOMPATIBLE_SCHEMA_HOLD")
            self.assertFalse(report["final"]["report_schema_valid"])
            self.assertFalse(report["final"]["report_schema_compatible"])
            self.assertEqual(report["final"]["report_schema_version"], 8)
            self.assertTrue(
                report["final"]["validation_error"].startswith("INCOMPATIBLE_SCHEMA_HOLD:")
            )
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_delete"])
            self.assertFalse(report["automatic_link"])
            self.assertFalse(report["automatic_rewrite"])

    def test_committed_final_with_hard_link_pending_is_exact_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = bench._pending_path(output)
            receipt = bench._commit_receipt_path(output)
            payload = valid_report_payload()
            write_0400(output, payload)
            os.link(output, pending)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, pending, receipt)}
            report = INSPECT.inspect_namespace(output)
            after = {str(p): generation(p) for p in (output, pending, receipt)}
            self.assertEqual(before, after)
            self.assertEqual(
                report["classification"],
                "COMMITTED_LOCAL_UNTRUSTED_WITH_PENDING_ALIAS",
            )
            self.assertTrue(report["pending_aliases_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_delete"])

    def test_committed_final_with_foreign_pending_generation_is_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = bench._pending_path(output)
            receipt = bench._commit_receipt_path(output)
            payload = valid_report_payload()
            write_0400(output, payload)
            write_0400(pending, payload)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(p): generation(p) for p in (output, pending, receipt)}
            report = INSPECT.inspect_namespace(output)
            after = {str(p): generation(p) for p in (output, pending, receipt)}
            self.assertEqual(before, after)
            self.assertEqual(
                report["classification"],
                "COMMITTED_LOCAL_UNTRUSTED_WITH_FOREIGN_PENDING_HOLD",
            )
            self.assertFalse(report["pending_aliases_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_delete"])
            self.assertFalse(report["automatic_link"])
            self.assertFalse(report["automatic_rewrite"])

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

    def test_parent_aba_cannot_mix_foreign_payload_and_receipt_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical_parent = root / "canonical"
            foreign_parent = root / "foreign"
            held_parent = root / "held"
            canonical_parent.mkdir()
            foreign_parent.mkdir()

            output = canonical_parent / "evidence.json"
            payload_a = b"retained-parent-final-a\n"
            write_0400(output, payload_a)

            foreign_output = foreign_parent / output.name
            payload_b = b"foreign-parent-final-b\n"
            write_0400(foreign_output, payload_b)
            write_0400(
                bench._commit_receipt_path(foreign_output),
                bench._commit_receipt_payload(foreign_output, payload_b),
            )

            original_read = INSPECT._read_descriptor
            swapped = False

            def read_during_parent_aba(descriptor):
                nonlocal swapped
                if swapped:
                    return original_read(descriptor)
                swapped = True
                canonical_parent.rename(held_parent)
                foreign_parent.rename(canonical_parent)
                try:
                    return original_read(descriptor)
                finally:
                    canonical_parent.rename(foreign_parent)
                    held_parent.rename(canonical_parent)

            with mock.patch.object(
                INSPECT, "_read_descriptor", side_effect=read_during_parent_aba,
            ):
                report = INSPECT.inspect_namespace(output)

            self.assertTrue(swapped)
            self.assertEqual(report["classification"], "FINAL_WITHOUT_RECEIPT")
            self.assertEqual(
                report["final"]["payload_sha256"],
                hashlib.sha256(payload_a).hexdigest(),
            )
            self.assertFalse(report["commit_receipt"]["present"])
            self.assertFalse(report["commit_receipt_binds_final"])
            self.assertTrue(report["namespace_generation_stable"])
            self.assertFalse(report["countable"])
            self.assertEqual(output.read_bytes(), payload_a)
            self.assertEqual(foreign_output.read_bytes(), payload_b)


if __name__ == "__main__":
    unittest.main()
