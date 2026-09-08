#!/usr/bin/env python3
"""Source-only falsifiers for JointAdvance parent-owned supervisor schema v10."""

import copy
import json
import unittest

import bench_joint_advance as bench
import test_bench_joint_advance as fixtures


class ParentSupervisorSchemaV10Tests(unittest.TestCase):
    @staticmethod
    def report():
        return json.loads(fixtures.EvidencePublicationTests.payload())

    @staticmethod
    def validate(report):
        return bench._validate_recoverable_evidence(
            bench.stable_json(report).encode("utf-8")
        )

    def test_current_schema_admits_exact_parent_owned_supervisor(self):
        report = self.report()
        self.assertEqual(report["schema_version"], 10)
        admitted = self.validate(report)
        supervisor = admitted["supervisor"]
        self.assertEqual(supervisor["schema"], bench.SUPERVISOR_SCHEMA)
        self.assertEqual(supervisor["owner"], "parent_process")
        self.assertEqual(supervisor["child_pid"], supervisor["child_pgid"])
        self.assertNotEqual(supervisor["parent_pid"], supervisor["child_pid"])
        self.assertTrue(supervisor["authorization_boundary"]["execute_designated_host"])
        self.assertEqual(supervisor["terminal_source"], "child_outcome")
        self.assertIn(
            supervisor["containment"]["retirement_terminal"],
            bench.SUPERVISOR_RETIREMENT_TERMINALS,
        )

    def test_schema_nine_without_supervisor_is_incompatible_before_field_checks(self):
        report = self.report()
        report["schema_version"] = 9
        report.pop("supervisor")
        with self.assertRaises(bench.IncompatibleEvidenceSchemaError) as raised:
            self.validate(report)
        self.assertEqual(raised.exception.actual, 9)
        self.assertEqual(raised.exception.expected, 10)

    def test_supervisor_record_is_required_for_current_schema(self):
        report = self.report()
        report["supervisor"] = None
        with self.assertRaisesRegex(bench.ContractError, "parent supervisor fields"):
            self.validate(report)

    def test_pid_pgid_binding_is_exact(self):
        report = self.report()
        report["supervisor"]["child_pgid"] += 1
        with self.assertRaisesRegex(bench.ContractError, "child PID/PGID identity"):
            self.validate(report)

    def test_parent_and_child_pid_are_distinct(self):
        report = self.report()
        report["supervisor"]["parent_pid"] = report["supervisor"]["child_pid"]
        with self.assertRaisesRegex(bench.ContractError, "child PID/PGID identity"):
            self.validate(report)

    def test_authorization_boundary_is_operation_bound(self):
        for field, value in (
            ("designated_hostname", "other"),
            ("operation_sha256", "0" * 64),
            ("execute_designated_host", False),
        ):
            report = self.report()
            report["supervisor"]["authorization_boundary"][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(
                bench.ContractError, "authorization boundary",
            ):
                self.validate(report)

    def test_outer_timeout_is_parameter_derived(self):
        report = self.report()
        report["supervisor"]["outer_execution_timeout_s"] += 1.0
        with self.assertRaisesRegex(bench.ContractError, "outer timeout"):
            self.validate(report)

    def test_terminal_source_is_closed_child_outcome(self):
        report = self.report()
        report["supervisor"]["terminal_source"] = "child_error"
        with self.assertRaisesRegex(bench.ContractError, "terminal source"):
            self.validate(report)

    def test_retirement_terminal_is_enumerated(self):
        report = self.report()
        report["supervisor"]["containment"]["retirement_terminal"] = "unknown"
        with self.assertRaisesRegex(bench.ContractError, "retirement terminal"):
            self.validate(report)

    def test_commit_receipt_digest_changes_with_supervisor_terminal(self):
        report = self.report()
        payload = bench.stable_json(report).encode("utf-8")
        mutated = copy.deepcopy(report)
        mutated["supervisor"]["containment"]["retirement_terminal"] = "sigkill_retired"
        mutated_payload = bench.stable_json(mutated).encode("utf-8")
        self.assertNotEqual(
            bench.hashlib.sha256(payload).hexdigest(),
            bench.hashlib.sha256(mutated_payload).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
