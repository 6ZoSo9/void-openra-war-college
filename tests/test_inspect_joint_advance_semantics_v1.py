#!/usr/bin/env python3
"""Focused semantics for read-only JointAdvance evidence inspection."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bench_joint_advance as bench
import test_bench_joint_advance as benchmark_tests


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "inspect_joint_advance_evidence.py"
SPEC = importlib.util.spec_from_file_location(
    "inspect_joint_advance_evidence_semantics_v1",
    SOURCE,
)
assert SPEC is not None and SPEC.loader is not None
INSPECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSPECT)


def valid_report() -> dict:
    return json.loads(benchmark_tests.EvidencePublicationTests.payload())


def synthetic_report(
    *,
    terminal: str,
    stage: str,
    cells: list[dict],
    concurrency: list[int] | None = None,
    tick_batches: list[int] | None = None,
    runtime_provenance: object | None = None,
    listener_identity: object | None = None,
) -> dict:
    return {
        "schema_version": 10,
        "parameters": {
            "concurrency": concurrency or [1],
            "tick_batches": tick_batches or [1],
        },
        "cells": cells,
        "run": {
            "terminal": terminal,
            "stage": stage,
            "runtime_provenance": runtime_provenance,
            "listener_identity": listener_identity,
        },
    }


class EvidenceInspectorSemanticsV1Tests(unittest.TestCase):
    def test_matrix_summary_uses_declared_plan_order(self) -> None:
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
        self.assertEqual(
            summary["first_non_success"],
            {"key": "c8-t8", "terminal": "timeout"},
        )
        self.assertEqual(
            summary["first_failure"],
            {"key": "c8-t8", "terminal": "timeout"},
        )
        self.assertEqual(
            summary["first_incomplete"],
            {"key": "c8-t8", "state": "present", "terminal": "timeout"},
        )

    def test_matrix_summary_separates_execution_blocking_and_missing(self) -> None:
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
        self.assertEqual(summary["first_missing"], "c1-t1")
        self.assertEqual(summary["failure_count"], 1)
        self.assertEqual(summary["blocked_cell_count"], 1)

    def test_impossible_terminal_stage_pair_fails_closed(self) -> None:
        report = synthetic_report(
            terminal="startup_error",
            stage="matrix_complete",
            cells=[],
        )

        with self.assertRaisesRegex(
            bench.ContractError,
            "run terminal/stage mismatch: startup_error/matrix_complete",
        ):
            INSPECT._require_run_terminal_stage_consistent(report)

    def test_pre_matrix_terminal_cannot_carry_cells(self) -> None:
        report = synthetic_report(
            terminal="startup_error",
            stage="host_attestation",
            cells=[{"key": "c1-t1", "terminal": "success"}],
        )

        with self.assertRaisesRegex(
            bench.ContractError,
            "pre-matrix run terminal carries matrix cells",
        ):
            INSPECT._require_run_terminal_stage_consistent(report)

    def test_cell_channel_error_requires_exact_successful_predecessor_prefix(self) -> None:
        report = synthetic_report(
            terminal="channel_error",
            stage="cell:c1-t1",
            cells=[{"key": "c1-t1", "terminal": "success"}],
            runtime_provenance={"bound": True},
            listener_identity={"bound": True},
        )

        with self.assertRaisesRegex(
            bench.ContractError,
            "channel-error stage does not bind exact successful predecessor prefix",
        ):
            INSPECT._require_run_terminal_stage_consistent(report)

    def test_artifact_projects_run_failure_without_mutation(self) -> None:
        report = synthetic_report(
            terminal="startup_error",
            stage="host_attestation",
            cells=[],
        )
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            path = parent / "evidence.json"
            path.write_bytes(b"synthetic-current-schema-report\n")
            path.chmod(0o400)
            before = path.read_bytes()
            parent_fd = os.open(
                parent,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            try:
                with mock.patch.object(
                    bench,
                    "_validate_recoverable_evidence",
                    return_value=report,
                ):
                    row, payload, descriptor = INSPECT._artifact(
                        parent_fd,
                        path.name,
                        path,
                        validate_report=True,
                    )
                try:
                    self.assertEqual(payload, before)
                    self.assertTrue(row["report_schema_valid"])
                    self.assertEqual(row["report_terminal"], "startup_error")
                    self.assertEqual(row["report_run_stage"], "host_attestation")
                    self.assertEqual(row["report_cell_terminals"], [])
                    self.assertEqual(
                        row["report_attempt_failure"],
                        {
                            "scope": "run",
                            "terminal": "startup_error",
                            "stage": "host_attestation",
                        },
                    )
                    self.assertEqual(
                        row["report_matrix_summary"]["missing_cell_count"],
                        1,
                    )
                    self.assertEqual(path.read_bytes(), before)
                finally:
                    assert descriptor is not None
                    os.close(descriptor)
            finally:
                os.close(parent_fd)

    def test_artifact_projects_matrix_failure_in_planned_order(self) -> None:
        report = synthetic_report(
            terminal="completed",
            stage="matrix_complete",
            cells=[
                {"key": "c8-t8", "terminal": "success"},
                {"key": "c8-t1", "terminal": "timeout"},
                {"key": "c1-t8", "terminal": "not_executed"},
            ],
            concurrency=[8, 1],
            tick_batches=[8, 1],
            runtime_provenance={"bound": True},
            listener_identity={"bound": True},
        )
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            path = parent / "evidence.json"
            path.write_bytes(b"synthetic-current-schema-report\n")
            path.chmod(0o400)
            parent_fd = os.open(
                parent,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            try:
                with mock.patch.object(
                    bench,
                    "_validate_recoverable_evidence",
                    return_value=report,
                ):
                    row, _, descriptor = INSPECT._artifact(
                        parent_fd,
                        path.name,
                        path,
                        validate_report=True,
                    )
                try:
                    self.assertTrue(row["report_schema_valid"])
                    self.assertEqual(
                        row["report_cell_terminals"],
                        ["success", "timeout", "not_executed"],
                    )
                    self.assertEqual(
                        row["report_attempt_failure"],
                        {
                            "scope": "matrix",
                            "key": "c8-t1",
                            "terminal": "timeout",
                        },
                    )
                    self.assertEqual(
                        row["report_matrix_summary"]["first_incomplete"],
                        {
                            "key": "c8-t1",
                            "state": "present",
                            "terminal": "timeout",
                        },
                    )
                finally:
                    assert descriptor is not None
                    os.close(descriptor)
            finally:
                os.close(parent_fd)


if __name__ == "__main__":
    unittest.main()
