#!/usr/bin/env python3
"""Source-only contract tests for bench_joint_advance.py."""

import asyncio
import json
import unittest

import bench_joint_advance as bench


class InputContractTests(unittest.TestCase):
    def test_canonical_integer_list(self):
        self.assertEqual(
            bench.parse_int_csv("1,2,4,8", label="c", minimum=1, maximum=8, allowed=(1, 2, 4, 8)),
            (1, 2, 4, 8),
        )
        for raw in ("", "01", "1,", "1,1", "1,3", "1, 2", "0", "-1", "1e1"):
            with self.subTest(raw=raw), self.assertRaises(bench.ContractError):
                bench.parse_int_csv(raw, label="c", minimum=1, maximum=8, allowed=(1, 2, 4, 8))

    def test_matrix_is_stable_and_bounded(self):
        self.assertEqual(
            bench.build_matrix((1, 2), (8, 32)),
            [
                {"concurrency": 1, "ticks_per_joint_advance": 8},
                {"concurrency": 1, "ticks_per_joint_advance": 32},
                {"concurrency": 2, "ticks_per_joint_advance": 8},
                {"concurrency": 2, "ticks_per_joint_advance": 32},
            ],
        )
        with self.assertRaises(bench.ContractError):
            bench.build_matrix(tuple(range(1, 10)), tuple(range(1, 10)))


class StatisticsTests(unittest.TestCase):
    def test_nearest_rank(self):
        values = [50, 10, 40, 20, 30]
        self.assertEqual(bench.percentile_nearest_rank(values, 0), 10)
        self.assertEqual(bench.percentile_nearest_rank(values, 50), 30)
        self.assertEqual(bench.percentile_nearest_rank(values, 95), 50)

    def test_latency_summary_rejects_invalid_samples(self):
        self.assertEqual(bench.latency_summary([]), {"count": 0})
        with self.assertRaises(bench.ContractError):
            bench.latency_summary([1, -1])
        with self.assertRaises(bench.ContractError):
            bench.latency_summary([float("nan")])


class CanonicalStateTests(unittest.TestCase):
    def test_transport_identifiers_do_not_change_hash(self):
        left = {
            "session_id": "one",
            "player_observations": [
                {"player": "Multi0", "observation": {"episode_id": "a", "tick": 50, "units": []}},
                {"player": "Multi1", "observation": {"episode_id": "b", "tick": 50, "units": []}},
            ],
        }
        right = {
            "session_id": "two",
            "player_observations": [
                {"player": "Multi0", "observation": {"episode_id": "c", "tick": 50, "units": []}},
                {"player": "Multi1", "observation": {"episode_id": "d", "tick": 50, "units": []}},
            ],
        }
        self.assertEqual(bench.canonical_state_hash(left), bench.canonical_state_hash(right))
        right["player_observations"][1]["observation"]["tick"] = 51
        self.assertNotEqual(bench.canonical_state_hash(left), bench.canonical_state_hash(right))

    def test_nonfinite_state_is_rejected(self):
        with self.assertRaises(bench.ContractError):
            bench.canonical_state_hash({"reward": float("inf")})


class TerminalLedgerTests(unittest.TestCase):
    def test_cell_terminal_is_exactly_once_and_immutable(self):
        ledger = bench.CellLedger()
        payload = {"samples": [1]}
        terminal = ledger.finalize("c1-t8", "timeout", payload)
        payload["samples"].append(2)
        self.assertEqual(terminal.payload, {"samples": [1]})
        with self.assertRaises(bench.ContractError):
            ledger.finalize("c1-t8", "success", {})
        with self.assertRaises(bench.ContractError):
            ledger.finalize("c2-t8", "late_success", {})


class PhaseTerminalityTests(unittest.IsolatedAsyncioTestCase):
    async def test_slow_completion_cannot_rewrite_timeout_or_escape_phase(self):
        retired = asyncio.Event()

        async def fast():
            await asyncio.sleep(0)

        async def slow():
            try:
                await asyncio.sleep(60)
            finally:
                retired.set()

        ledger = await bench.retire_phase_tasks(
            {"fast": fast(), "slow": slow()},
            deadline_s=0.01,
        )
        terminals = {cell.key: cell.terminal for cell in ledger.values()}
        self.assertEqual(terminals, {"fast": "success", "slow": "timeout"})
        self.assertTrue(retired.is_set())
        with self.assertRaises(bench.ContractError):
            ledger.finalize("slow", "success", {})


class EvidenceContractTests(unittest.TestCase):
    def setUp(self):
        self.provenance = bench.validate_provenance(
            bench.FROZEN_ENGINE_SHA,
            "7" * 40,
            bench.GENERATION,
        )
        self.parameters = {"concurrency": (1,), "tick_batches": (8,)}

    def test_source_only_report_cannot_claim_runtime_measurements(self):
        report = bench.build_report(
            provenance=self.provenance,
            parameters=self.parameters,
            cells=[],
            executed_designated_host=False,
            generated_at_utc="2026-08-27T00:00:00Z",
            command=["bench_joint_advance.py", "plan"],
        )
        self.assertEqual(report["runtime_evidence"], "PENDING_DESIGNATED_HOST")
        self.assertIsNone(report["host"])
        with self.assertRaises(bench.ContractError):
            bench.build_report(
                provenance=self.provenance,
                parameters=self.parameters,
                cells=[{"terminal": "success"}],
                executed_designated_host=False,
                generated_at_utc="2026-08-27T00:00:00Z",
                command=["unit-test"],
            )

    def test_runtime_report_requires_terminal_cells(self):
        with self.assertRaises(bench.ContractError):
            bench.build_report(
                provenance=self.provenance,
                parameters=self.parameters,
                cells=[],
                executed_designated_host=True,
                generated_at_utc="2026-08-27T00:00:00Z",
                command=["unit-test"],
                host={"hostname": "fixture"},
            )

    def test_stable_json_is_machine_replayable(self):
        report = bench.build_report(
            provenance=self.provenance,
            parameters=self.parameters,
            cells=[],
            executed_designated_host=False,
            generated_at_utc="2026-08-27T00:00:00Z",
            command=["unit-test"],
        )
        encoded = bench.stable_json(report)
        self.assertTrue(encoded.endswith("\n"))
        self.assertEqual(json.loads(encoded), report)


if __name__ == "__main__":
    unittest.main()
