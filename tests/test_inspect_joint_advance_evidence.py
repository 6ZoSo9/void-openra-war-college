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
            "classification_scope": "ARTIFACT_ONLY",
            "overall_status": "HOLD",
            "artifact_state": "INSPECTION_ERROR_HOLD",
            "schema_state": "SCHEMA_NOT_INSPECTED",
            "evidence_state": "EVIDENCE_NOT_INSPECTED",
            "operator_guidance": {
                "artifact_action": "RETRY_READ_ONLY_INSPECTION_AFTER_OPERATOR_FIX",
                "schema_action": "RETRY_READ_ONLY_INSPECTION",
                "evidence_action": "RETRY_READ_ONLY_INSPECTION",
                "countability_action": "AUTHENTICATE_PRODUCER_AND_REVIEW_BEFORE_ADMISSION",
                "automatic_action_allowed": False,
            },
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
            self.assertEqual(report["classification_scope"], "ARTIFACT_ONLY")
            self.assertEqual(report["overall_status"], "NO_EVIDENCE")
            self.assertEqual(report["evidence_state"], "EVIDENCE_NOT_AVAILABLE")
            self.assertTrue(report["inspection_read_only"])
            self.assertFalse(report["countable"])
            self.assertEqual(
                report["operator_guidance"],
                {
                    "artifact_action": "NONE",
                    "schema_action": "NONE",
                    "evidence_action": "NONE",
                    "countability_action": "AUTHENTICATE_PRODUCER_AND_REVIEW_BEFORE_ADMISSION",
                    "automatic_action_allowed": False,
                },
            )
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
            self.assertEqual(report["overall_status"], "REVIEW_REQUIRED")
            self.assertEqual(
                report["evidence_state"], "COMPLETED_RUNTIME_REVIEW_REQUIRED",
            )
            self.assertTrue(report["final"]["report_schema_valid"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")
            self.assertEqual(
                report["operator_guidance"]["artifact_action"],
                "PRESERVE_AND_AUTHENTICATE_PRODUCER",
            )
            self.assertEqual(
                report["operator_guidance"]["schema_action"],
                "PRESERVE_CURRENT_SCHEMA",
            )
            self.assertFalse(report["operator_guidance"]["automatic_action_allowed"])

    def test_receipt_bound_failed_runtime_is_top_level_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_payload = json.loads(valid_report_payload())
            report_payload["run"].update({
                "terminal": "startup_error",
                "stage": "runtime_supervisor",
                "error_type": "ContractError",
                "error": "runtime supervisor could not prove descendant retirement",
            })
            payload = bench.stable_json(report_payload).encode("utf-8")
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))
            before = {str(path): generation(path) for path in (output, receipt)}

            report = INSPECT.inspect_namespace(output)

            self.assertEqual(
                before, {str(path): generation(path) for path in (output, receipt)}
            )
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["schema_state"], "CURRENT_SCHEMA_VALID")
            self.assertEqual(report["final"]["report_terminal"], "startup_error")
            self.assertEqual(report["evidence_state"], "FAILED_RUNTIME_HOLD")
            self.assertEqual(report["overall_status"], "HOLD")
            self.assertEqual(
                report["operator_guidance"]["evidence_action"],
                "PRESERVE_AND_REVIEW_RUNTIME_FAILURE_BEFORE_RETRY",
            )
            self.assertFalse(report["operator_guidance"]["automatic_action_allowed"])

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
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["classification_scope"], "ARTIFACT_ONLY")
            self.assertEqual(report["overall_status"], "HOLD")
            self.assertEqual(report["artifact_state"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["schema_state"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(report["final"]["report_schema_valid"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")
            self.assertEqual(
                report["operator_guidance"]["artifact_action"],
                "PRESERVE_AND_AUTHENTICATE_PRODUCER",
            )
            self.assertEqual(
                report["operator_guidance"]["schema_action"],
                "PRESERVE_AND_REVIEW_CURRENT_SCHEMA_INVALID",
            )
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
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["classification_scope"], "ARTIFACT_ONLY")
            self.assertEqual(report["overall_status"], "HOLD")
            self.assertEqual(report["artifact_state"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["schema_state"], "INCOMPATIBLE_SCHEMA_HOLD")
            self.assertFalse(report["final"]["report_schema_valid"])
            self.assertFalse(report["final"]["report_schema_compatible"])
            self.assertEqual(report["final"]["report_schema_version"], 8)
            self.assertTrue(
                report["final"]["validation_error"].startswith("INCOMPATIBLE_SCHEMA_HOLD:")
            )
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertEqual(report["producer_authentication"], "ABSENT")
            self.assertEqual(
                report["operator_guidance"]["artifact_action"],
                "PRESERVE_AND_AUTHENTICATE_PRODUCER",
            )
            self.assertEqual(
                report["operator_guidance"]["schema_action"],
                "PRESERVE_AND_USE_MATCHING_HISTORICAL_VALIDATOR",
            )
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_delete"])
            self.assertFalse(report["automatic_link"])
            self.assertFalse(report["automatic_rewrite"])

    def test_cli_current_schema_invalid_emits_top_level_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_payload = json.loads(
                benchmark_tests.EvidencePublicationTests.completed_failure_payload()
            )
            report_payload["cells"][1]["blocked_by"] = "c1-t8"
            payload = bench.stable_json(report_payload).encode("utf-8")
            write_0400(output, payload)
            write_0400(
                bench._commit_receipt_path(output),
                bench._commit_receipt_payload(output, payload),
            )

            result = subprocess.run(
                [sys.executable, str(SOURCE), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            report = json.loads(result.stdout)
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["classification_scope"], "ARTIFACT_ONLY")
            self.assertEqual(report["schema_state"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertEqual(report["overall_status"], "HOLD")

    def test_cli_incompatible_schema_emits_top_level_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_payload = json.loads(
                benchmark_tests.EvidencePublicationTests.completed_failure_payload()
            )
            report_payload["schema_version"] = 8
            report_payload["cells"][1]["blocked_by"] = "c1-t8"
            payload = bench.stable_json(report_payload).encode("utf-8")
            write_0400(output, payload)
            write_0400(
                bench._commit_receipt_path(output),
                bench._commit_receipt_payload(output, payload),
            )

            result = subprocess.run(
                [sys.executable, str(SOURCE), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            report = json.loads(result.stdout)
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(report["classification_scope"], "ARTIFACT_ONLY")
            self.assertEqual(report["schema_state"], "INCOMPATIBLE_SCHEMA_HOLD")
            self.assertEqual(report["overall_status"], "HOLD")

    def test_prior_schema_preserves_artifact_authority_across_topologies(self):
        report_payload = json.loads(
            benchmark_tests.EvidencePublicationTests.completed_failure_payload()
        )
        self.assertEqual(report_payload["schema_version"], 9)
        report_payload["schema_version"] = 8
        payload = bench.stable_json(report_payload).encode("utf-8")
        cases = (
            (
                "committed",
                "COMMITTED_LOCAL_UNTRUSTED",
                "PRESERVE_AND_AUTHENTICATE_PRODUCER",
            ),
            (
                "final_without_receipt",
                "FINAL_WITHOUT_RECEIPT",
                "PRESERVE_AND_RECONCILE_UNCOMMITTED_FINAL",
            ),
            (
                "receipt_mismatch",
                "FINAL_RECEIPT_BINDING_MISMATCH_HOLD",
                "PRESERVE_AND_INVESTIGATE_RECEIPT_MISMATCH",
            ),
            (
                "pending_only",
                "PENDING_REPORT_ONLY",
                "PRESERVE_AND_RECONCILE_INTERRUPTED_PUBLICATION",
            ),
            (
                "foreign_pending",
                "COMMITTED_LOCAL_UNTRUSTED_WITH_FOREIGN_PENDING_HOLD",
                "PRESERVE_AND_RECONCILE_FOREIGN_PENDING",
            ),
        )

        for topology, expected_artifact_state, expected_artifact_action in cases:
            with self.subTest(topology=topology), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                pending = bench._pending_path(output)
                receipt = bench._commit_receipt_path(output)

                if topology != "pending_only":
                    write_0400(output, payload)
                if topology == "pending_only":
                    write_0400(pending, payload)
                elif topology == "foreign_pending":
                    write_0400(pending, payload)
                    write_0400(receipt, bench._commit_receipt_payload(output, payload))
                elif topology == "committed":
                    write_0400(receipt, bench._commit_receipt_payload(output, payload))
                elif topology == "receipt_mismatch":
                    write_0400(receipt, bench._commit_receipt_payload(output, b"foreign"))

                paths = tuple(path for path in (output, pending, receipt) if path.exists())
                before = {str(path): generation(path) for path in paths}
                report = INSPECT.inspect_namespace(output)

                self.assertEqual(before, {str(path): generation(path) for path in paths})
                self.assertEqual(report["classification"], expected_artifact_state)
                self.assertEqual(report["artifact_state"], expected_artifact_state)
                self.assertEqual(report["schema_state"], "INCOMPATIBLE_SCHEMA_HOLD")
                self.assertEqual(
                    report["operator_guidance"]["artifact_action"],
                    expected_artifact_action,
                )
                self.assertEqual(
                    report["operator_guidance"]["schema_action"],
                    "PRESERVE_AND_USE_MATCHING_HISTORICAL_VALIDATOR",
                )
                self.assertFalse(
                    report["operator_guidance"]["automatic_action_allowed"]
                )
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

    def test_operator_guidance_rejects_unknown_state(self):
        with self.assertRaisesRegex(
            bench.ContractError,
            "inspector state has no closed operator guidance",
        ):
            INSPECT._operator_guidance(
                "FOREIGN_STATE",
                "CURRENT_SCHEMA_VALID",
                "COMPLETED_RUNTIME_REVIEW_REQUIRED",
            )


if __name__ == "__main__":
    unittest.main()
