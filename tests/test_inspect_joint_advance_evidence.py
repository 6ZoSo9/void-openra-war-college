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


def startup_error_payload() -> bytes:
    report = json.loads(valid_report_payload())
    report["cells"] = []
    report["run"] = {
        "terminal": "startup_error",
        "stage": "host_attestation",
        "error_type": "ContractError",
        "error": "designated hostname mismatch",
        "listener_identity": None,
        "runtime_provenance": None,
        "daemon_log": None,
        "cleanup": {"failures": []},
        "containment": {
            "required_by_cell": False,
            "boundary": "not_required",
            "daemon_retired": True,
        },
    }
    return bench.stable_json(report).encode("utf-8")


def impossible_startup_stage_payload() -> bytes:
    report = json.loads(startup_error_payload())
    report["run"]["stage"] = "matrix_complete"
    return bench.stable_json(report).encode("utf-8")


def impossible_pre_matrix_cells_payload() -> bytes:
    report = json.loads(startup_error_payload())
    report["cells"] = json.loads(valid_report_payload())["cells"]
    return bench.stable_json(report).encode("utf-8")


def channel_error_at_first_cell_payload(*, include_current_cell: bool) -> bytes:
    report = json.loads(valid_report_payload())
    if not include_current_cell:
        report["cells"] = []
    report["run"].update({
        "terminal": "channel_error",
        "stage": "cell:c1-t1",
        "error_type": "ContractError",
        "error": "synthetic channel failure",
    })
    return bench.stable_json(report).encode("utf-8")


def cleanup_error_payload(*, include_completed_matrix: bool) -> bytes:
    report = json.loads(valid_report_payload())
    if not include_completed_matrix:
        report["cells"] = []
    failure = "channel:RuntimeError:synthetic cleanup failure"
    report["run"].update({
        "terminal": "cleanup_error",
        "stage": "cleanup",
        "error_type": "CleanupError",
        "error": failure,
        "cleanup": {"failures": [failure]},
    })
    return bench.stable_json(report).encode("utf-8")


def output_error_payload(shape: str) -> bytes:
    if shape == "empty":
        report = json.loads(startup_error_payload())
    else:
        report = json.loads(
            benchmark_tests.EvidencePublicationTests.completed_failure_payload()
        )
        if shape == "partial_failure":
            report["cells"] = report["cells"][:1]
        elif shape != "complete":
            raise AssertionError(f"unsupported output-error shape: {shape}")
    report["run"].update({
        "terminal": "output_error",
        "stage": "evidence_publication",
        "error_type": "ContractError",
        "error": "synthetic evidence publication failure",
    })
    return bench.stable_json(report).encode("utf-8")


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
            self.assertEqual(report["final"]["report_run_stage"], "matrix_complete")
            self.assertIsNone(report["final"]["report_attempt_failure"])
            self.assertEqual(report["final"]["report_matrix_summary"], {
                "planned_cell_count": 1,
                "cell_count": 1,
                "executed_cell_count": 1,
                "missing_cell_count": 0,
                "first_missing": None,
                "first_incomplete": None,
                "success_count": 1,
                "non_success_count": 0,
                "failure_count": 0,
                "blocked_cell_count": 0,
                "first_non_success": None,
                "first_failure": None,
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
                "planned_cell_count": 2,
                "cell_count": 2,
                "executed_cell_count": 1,
                "missing_cell_count": 0,
                "first_missing": None,
                "first_incomplete": {
                    "key": "c1-t1",
                    "state": "present",
                    "terminal": "timeout",
                },
                "success_count": 0,
                "non_success_count": 2,
                "failure_count": 1,
                "blocked_cell_count": 1,
                "first_non_success": {"key": "c1-t1", "terminal": "timeout"},
                "first_failure": {"key": "c1-t1", "terminal": "timeout"},
            })
            self.assertEqual(report["final"]["report_run_stage"], "matrix_complete")
            self.assertEqual(report["final"]["report_attempt_failure"], {
                "scope": "matrix",
                "key": "c1-t1",
                "terminal": "timeout",
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_pre_matrix_run_failure_is_not_misreported_as_zero_failures(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = startup_error_payload()
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertEqual(final["report_terminal"], "startup_error")
            self.assertEqual(final["report_run_stage"], "host_attestation")
            self.assertEqual(final["report_cell_terminals"], [])
            self.assertEqual(final["report_matrix_summary"]["planned_cell_count"], 1)
            self.assertEqual(final["report_matrix_summary"]["cell_count"], 0)
            self.assertEqual(final["report_matrix_summary"]["failure_count"], 0)
            self.assertEqual(final["report_matrix_summary"]["missing_cell_count"], 1)
            self.assertEqual(final["report_attempt_failure"], {
                "scope": "run",
                "terminal": "startup_error",
                "stage": "host_attestation",
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])

    def test_impossible_run_terminal_stage_pair_is_explicit_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = impossible_startup_stage_payload()
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(final["report_schema_valid"])
            self.assertEqual(
                final["validation_error"],
                "ContractError:run terminal/stage mismatch: "
                "startup_error/matrix_complete",
            )
            self.assertIsNone(final["report_terminal"])
            self.assertIsNone(final["report_run_stage"])
            self.assertIsNone(final["report_attempt_failure"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_pre_matrix_terminal_with_executed_cell_is_explicit_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = impossible_pre_matrix_cells_payload()
            self.assertEqual(
                bench._validate_recoverable_evidence(payload)["cells"][0]["terminal"],
                "success",
            )
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(final["report_schema_valid"])
            self.assertEqual(
                final["validation_error"],
                "ContractError:pre-matrix run terminal carries matrix cells: "
                "startup_error/host_attestation",
            )
            self.assertIsNone(final["report_terminal"])
            self.assertIsNone(final["report_run_stage"])
            self.assertIsNone(final["report_attempt_failure"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_post_provenance_stages_require_runtime_provenance(self):
        cases = (
            ("readiness_timeout", "readiness"),
            ("channel_error", "readiness"),
            ("startup_error", "endpoint_preflight"),
        )
        for terminal, stage in cases:
            with self.subTest(terminal=terminal, stage=stage), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                report_body = json.loads(startup_error_payload())
                report_body["run"].update({
                    "terminal": terminal,
                    "stage": stage,
                    "error": "synthetic post-provenance failure",
                })
                payload = bench.stable_json(report_body).encode("utf-8")
                self.assertIsNone(
                    bench._validate_recoverable_evidence(payload)[
                        "run"
                    ]["runtime_provenance"],
                )
                write_0400(output, payload)
                receipt = bench._commit_receipt_path(output)
                write_0400(
                    receipt,
                    bench._commit_receipt_payload(output, payload),
                )

                report = INSPECT.inspect_namespace(output)

                final = report["final"]
                self.assertEqual(
                    report["classification"],
                    "CURRENT_SCHEMA_INVALID_HOLD",
                )
                self.assertFalse(final["report_schema_valid"])
                self.assertEqual(
                    final["validation_error"],
                    "ContractError:run stage lacks established runtime "
                    f"provenance: {terminal}/{stage}",
                )
                self.assertIsNone(final["report_terminal"])
                self.assertIsNone(final["report_run_stage"])
                self.assertIsNone(final["report_attempt_failure"])
                self.assertTrue(report["commit_receipt_binds_final"])
                self.assertFalse(report["countable"])
                self.assertFalse(report["automatic_recovery"])
                self.assertFalse(report["automatic_rewrite"])

    def test_pre_runtime_stages_reject_premature_identity(self):
        valid_run = json.loads(valid_report_payload())["run"]
        cases = (
            (
                "startup_error",
                "host_attestation",
                None,
                "runtime provenance",
            ),
            (
                "readiness_timeout",
                "readiness",
                valid_run["listener_identity"],
                "listener identity",
            ),
        )
        for terminal, stage, listener_identity, identity_name in cases:
            with self.subTest(
                terminal=terminal,
                stage=stage,
            ), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                report_body = json.loads(startup_error_payload())
                report_body["run"].update({
                    "terminal": terminal,
                    "stage": stage,
                    "error": "synthetic pre-runtime identity contradiction",
                    "runtime_provenance": valid_run["runtime_provenance"],
                    "listener_identity": listener_identity,
                })
                payload = bench.stable_json(report_body).encode("utf-8")
                validated = bench._validate_recoverable_evidence(payload)
                self.assertIsNotNone(validated["run"]["runtime_provenance"])
                if listener_identity is not None:
                    self.assertIsNotNone(validated["run"]["listener_identity"])
                write_0400(output, payload)
                receipt = bench._commit_receipt_path(output)
                write_0400(
                    receipt,
                    bench._commit_receipt_payload(output, payload),
                )

                report = INSPECT.inspect_namespace(output)

                final = report["final"]
                self.assertEqual(
                    report["classification"],
                    "CURRENT_SCHEMA_INVALID_HOLD",
                )
                self.assertFalse(final["report_schema_valid"])
                self.assertEqual(
                    final["validation_error"],
                    f"ContractError:run stage carries premature "
                    f"{identity_name}: {terminal}/{stage}",
                )
                self.assertIsNone(final["report_terminal"])
                self.assertIsNone(final["report_run_stage"])
                self.assertIsNone(final["report_attempt_failure"])
                self.assertTrue(report["commit_receipt_binds_final"])
                self.assertFalse(report["countable"])
                self.assertFalse(report["automatic_recovery"])
                self.assertFalse(report["automatic_rewrite"])

    def test_runtime_provenance_acquisition_failure_may_lack_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_body = json.loads(startup_error_payload())
            report_body["run"]["stage"] = "runtime_provenance"
            report_body["run"]["error"] = "synthetic provenance failure"
            payload = bench.stable_json(report_body).encode("utf-8")
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(
                receipt,
                bench._commit_receipt_payload(output, payload),
            )

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(
                report["classification"],
                "COMMITTED_LOCAL_UNTRUSTED",
            )
            self.assertTrue(final["report_schema_valid"])
            self.assertEqual(final["report_terminal"], "startup_error")
            self.assertEqual(
                final["report_run_stage"],
                "runtime_provenance",
            )
            self.assertIsNone(
                json.loads(payload)["run"]["runtime_provenance"],
            )
            self.assertEqual(final["report_attempt_failure"], {
                "scope": "run",
                "terminal": "startup_error",
                "stage": "runtime_provenance",
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])

    def test_channel_error_at_first_cell_accepts_exact_empty_predecessor_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = channel_error_at_first_cell_payload(
                include_current_cell=False,
            )
            validated = bench._validate_recoverable_evidence(payload)
            self.assertEqual(validated["cells"], [])
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertTrue(final["report_schema_valid"])
            self.assertEqual(final["report_terminal"], "channel_error")
            self.assertEqual(final["report_run_stage"], "cell:c1-t1")
            self.assertEqual(final["report_matrix_summary"]["cell_count"], 0)
            self.assertEqual(final["report_matrix_summary"]["missing_cell_count"], 1)
            self.assertEqual(final["report_attempt_failure"], {
                "scope": "run",
                "terminal": "channel_error",
                "stage": "cell:c1-t1",
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])

    def test_channel_error_at_cell_requires_established_runtime_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            report_body = json.loads(channel_error_at_first_cell_payload(
                include_current_cell=False,
            ))
            report_body["run"]["listener_identity"] = None
            report_body["run"]["runtime_provenance"] = None
            payload = bench.stable_json(report_body).encode("utf-8")
            self.assertEqual(
                bench._validate_recoverable_evidence(payload)["cells"],
                [],
            )
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(final["report_schema_valid"])
            self.assertEqual(
                final["validation_error"],
                "ContractError:cell-stage channel error lacks established "
                "runtime identity",
            )
            self.assertIsNone(final["report_terminal"])
            self.assertIsNone(final["report_run_stage"])
            self.assertIsNone(final["report_attempt_failure"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_channel_error_at_first_cell_cannot_carry_that_cell_as_completed(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = channel_error_at_first_cell_payload(
                include_current_cell=True,
            )
            self.assertEqual(
                bench._validate_recoverable_evidence(payload)["cells"][0]["terminal"],
                "success",
            )
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(final["report_schema_valid"])
            self.assertEqual(
                final["validation_error"],
                "ContractError:channel-error stage does not bind exact successful "
                "predecessor prefix: cell:c1-t1",
            )
            self.assertIsNone(final["report_terminal"])
            self.assertIsNone(final["report_run_stage"])
            self.assertIsNone(final["report_attempt_failure"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_cleanup_error_accepts_the_completed_matrix_it_follows(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = cleanup_error_payload(include_completed_matrix=True)
            validated = bench._validate_recoverable_evidence(payload)
            self.assertEqual(len(validated["cells"]), 1)
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "COMMITTED_LOCAL_UNTRUSTED")
            self.assertTrue(final["report_schema_valid"])
            self.assertEqual(final["report_terminal"], "cleanup_error")
            self.assertEqual(final["report_run_stage"], "cleanup")
            self.assertEqual(final["report_matrix_summary"]["cell_count"], 1)
            self.assertEqual(final["report_matrix_summary"]["missing_cell_count"], 0)
            self.assertEqual(final["report_attempt_failure"], {
                "scope": "run",
                "terminal": "cleanup_error",
                "stage": "cleanup",
            })
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])

    def test_cleanup_error_cannot_omit_the_completed_matrix(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = cleanup_error_payload(include_completed_matrix=False)
            self.assertEqual(
                bench._validate_recoverable_evidence(payload)["cells"],
                [],
            )
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(final["report_schema_valid"])
            self.assertEqual(
                final["validation_error"],
                "ContractError:cleanup-error evidence does not close the planned "
                "matrix",
            )
            self.assertIsNone(final["report_terminal"])
            self.assertIsNone(final["report_run_stage"])
            self.assertIsNone(final["report_attempt_failure"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_output_error_accepts_only_producible_matrix_shapes(self):
        cases = (
            ("empty", 0, 1),
            ("complete", 2, 0),
        )
        for shape, cell_count, missing_count in cases:
            with self.subTest(shape=shape), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                payload = output_error_payload(shape)
                validated = bench._validate_recoverable_evidence(payload)
                self.assertEqual(len(validated["cells"]), cell_count)
                write_0400(output, payload)
                receipt = bench._commit_receipt_path(output)
                write_0400(
                    receipt,
                    bench._commit_receipt_payload(output, payload),
                )

                report = INSPECT.inspect_namespace(output)

                final = report["final"]
                self.assertEqual(
                    report["classification"],
                    "COMMITTED_LOCAL_UNTRUSTED",
                )
                self.assertTrue(final["report_schema_valid"])
                self.assertEqual(final["report_terminal"], "output_error")
                self.assertEqual(
                    final["report_run_stage"],
                    "evidence_publication",
                )
                self.assertEqual(
                    final["report_matrix_summary"]["cell_count"],
                    cell_count,
                )
                self.assertEqual(
                    final["report_matrix_summary"]["missing_cell_count"],
                    missing_count,
                )
                self.assertTrue(report["commit_receipt_binds_final"])
                self.assertFalse(report["countable"])

    def test_output_error_cannot_carry_a_partial_failed_matrix(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = output_error_payload("partial_failure")
            validated = bench._validate_recoverable_evidence(payload)
            self.assertEqual(
                [cell["terminal"] for cell in validated["cells"]],
                ["timeout"],
            )
            write_0400(output, payload)
            receipt = bench._commit_receipt_path(output)
            write_0400(receipt, bench._commit_receipt_payload(output, payload))

            report = INSPECT.inspect_namespace(output)

            final = report["final"]
            self.assertEqual(report["classification"], "CURRENT_SCHEMA_INVALID_HOLD")
            self.assertFalse(final["report_schema_valid"])
            self.assertEqual(
                final["validation_error"],
                "ContractError:output-error evidence does not bind a valid "
                "pre-publication matrix state",
            )
            self.assertIsNone(final["report_terminal"])
            self.assertIsNone(final["report_run_stage"])
            self.assertIsNone(final["report_attempt_failure"])
            self.assertTrue(report["commit_receipt_binds_final"])
            self.assertFalse(report["countable"])
            self.assertFalse(report["automatic_recovery"])
            self.assertFalse(report["automatic_rewrite"])

    def test_matrix_summary_uses_planned_order_not_lexicographic_storage_order(self):
        report = {
            "parameters": {
                "concurrency": [8, 1],
                "tick_batches": [8, 1],
            },
            "cells": [
                {"key": "c1-t1", "terminal": "not_executed"},
                {"key": "c1-t8", "terminal": "not_executed"},
                {"key": "c8-t1", "terminal": "not_executed"},
                {"key": "c8-t8", "terminal": "timeout"},
            ],
        }

        terminals, summary = INSPECT._matrix_summary(report)

        self.assertEqual(
            terminals,
            ["timeout", "not_executed", "not_executed", "not_executed"],
        )
        self.assertEqual(summary, {
            "planned_cell_count": 4,
            "cell_count": 4,
            "executed_cell_count": 1,
            "missing_cell_count": 0,
            "first_missing": None,
            "first_incomplete": {
                "key": "c8-t8",
                "state": "present",
                "terminal": "timeout",
            },
            "success_count": 0,
            "non_success_count": 4,
            "failure_count": 1,
            "blocked_cell_count": 3,
            "first_non_success": {"key": "c8-t8", "terminal": "timeout"},
            "first_failure": {"key": "c8-t8", "terminal": "timeout"},
        })

    def test_matrix_summary_exposes_partial_and_empty_missing_cells(self):
        parameters = {
            "concurrency": [8, 1],
            "tick_batches": [8, 1],
        }
        partial = {
            "parameters": parameters,
            "cells": [
                {"key": "c8-t8", "terminal": "timeout"},
            ],
        }

        terminals, summary = INSPECT._matrix_summary(partial)

        self.assertEqual(terminals, ["timeout"])
        self.assertEqual(summary, {
            "planned_cell_count": 4,
            "cell_count": 1,
            "executed_cell_count": 1,
            "missing_cell_count": 3,
            "first_missing": "c8-t1",
            "first_incomplete": {
                "key": "c8-t8",
                "state": "present",
                "terminal": "timeout",
            },
            "success_count": 0,
            "non_success_count": 1,
            "failure_count": 1,
            "blocked_cell_count": 0,
            "first_non_success": {"key": "c8-t8", "terminal": "timeout"},
            "first_failure": {"key": "c8-t8", "terminal": "timeout"},
        })

        terminals, summary = INSPECT._matrix_summary({
            "parameters": parameters,
            "cells": [],
        })

        self.assertEqual(terminals, [])
        self.assertEqual(summary, {
            "planned_cell_count": 4,
            "cell_count": 0,
            "executed_cell_count": 0,
            "missing_cell_count": 4,
            "first_missing": "c8-t8",
            "first_incomplete": {"key": "c8-t8", "state": "missing"},
            "success_count": 0,
            "non_success_count": 0,
            "failure_count": 0,
            "blocked_cell_count": 0,
            "first_non_success": None,
            "first_failure": None,
        })

    def test_matrix_summary_missing_cell_precedes_later_present_failure(self):
        report = {
            "parameters": {
                "concurrency": [8, 1],
                "tick_batches": [8, 1],
            },
            "cells": [
                {"key": "c8-t1", "terminal": "timeout"},
            ],
        }

        terminals, summary = INSPECT._matrix_summary(report)

        self.assertEqual(terminals, ["timeout"])
        self.assertEqual(summary["first_missing"], "c8-t8")
        self.assertEqual(
            summary["first_non_success"],
            {"key": "c8-t1", "terminal": "timeout"},
        )
        self.assertEqual(
            summary["first_failure"],
            {"key": "c8-t1", "terminal": "timeout"},
        )
        self.assertEqual(
            summary["first_incomplete"],
            {"key": "c8-t8", "state": "missing"},
        )

    def test_matrix_summary_separates_blocked_cell_from_actual_failure(self):
        report = {
            "parameters": {
                "concurrency": [8, 1],
                "tick_batches": [8, 1],
            },
            "cells": [
                {"key": "c8-t8", "terminal": "not_executed"},
                {"key": "c8-t1", "terminal": "timeout"},
            ],
        }

        terminals, summary = INSPECT._matrix_summary(report)

        self.assertEqual(terminals, ["not_executed", "timeout"])
        self.assertEqual(
            summary["first_non_success"],
            {"key": "c8-t8", "terminal": "not_executed"},
        )
        self.assertEqual(
            summary["first_failure"],
            {"key": "c8-t1", "terminal": "timeout"},
        )
        self.assertEqual(
            summary["first_incomplete"],
            {
                "key": "c8-t8",
                "state": "present",
                "terminal": "not_executed",
            },
        )

    def test_matrix_summary_counts_execution_and_failure_separately_from_blocking(self):
        report = {
            "parameters": {
                "concurrency": [8, 1],
                "tick_batches": [8, 1],
            },
            "cells": [
                {"key": "c8-t8", "terminal": "success"},
                {"key": "c8-t1", "terminal": "timeout"},
                {"key": "c1-t8", "terminal": "not_executed"},
            ],
        }

        terminals, summary = INSPECT._matrix_summary(report)

        self.assertEqual(terminals, ["success", "timeout", "not_executed"])
        self.assertEqual(summary["planned_cell_count"], 4)
        self.assertEqual(summary["cell_count"], 3)
        self.assertEqual(summary["executed_cell_count"], 2)
        self.assertEqual(summary["missing_cell_count"], 1)
        self.assertEqual(summary["non_success_count"], 2)
        self.assertEqual(summary["failure_count"], 1)
        self.assertEqual(summary["blocked_cell_count"], 1)
        self.assertEqual(
            summary["first_failure"],
            {"key": "c8-t1", "terminal": "timeout"},
        )

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
