#!/usr/bin/env python3
"""Source-only contract tests for bench_joint_advance.py."""

import asyncio
import io
import json
import os
import socket
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

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

    def test_matrix_stops_after_any_non_success_terminal(self):
        self.assertTrue(bench.matrix_may_continue("success"))
        for terminal in ("timeout", "rpc_error", "teardown_error", "not_executed"):
            with self.subTest(terminal=terminal):
                self.assertFalse(bench.matrix_may_continue(terminal))
        with self.assertRaises(bench.ContractError):
            bench.matrix_may_continue("skipped")


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
        failed = bench.build_report(
            provenance=self.provenance,
            parameters=self.parameters,
            cells=[],
            executed_designated_host=True,
            generated_at_utc="2026-08-27T00:00:00Z",
            command=["unit-test"],
            run={"terminal": "startup_error"},
            host={"hostname": "fixture"},
        )
        self.assertEqual(failed["run"]["terminal"], "startup_error")
        with self.assertRaises(bench.ContractError):
            bench.build_report(
                provenance=self.provenance,
                parameters=self.parameters,
                cells=[],
                executed_designated_host=True,
                generated_at_utc="2026-08-27T00:00:00Z",
                command=["unit-test"],
                run={"terminal": "completed"},
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


class RuntimeBoundaryTests(unittest.TestCase):
    def test_joint_response_is_bound_to_session_ticks_and_perspectives(self):
        good = types.SimpleNamespace(
            session_id="session-a",
            start_tick=10,
            end_tick=18,
            player_observations=[
                types.SimpleNamespace(player="Multi0"),
                types.SimpleNamespace(player="Multi1"),
            ],
        )
        self.assertEqual(
            bench.validate_joint_response(good, "session-a", 8),
            {"start_tick": 10, "end_tick": 18, "players": ["Multi0", "Multi1"]},
        )
        for mutation in (
            {"session_id": "wrong"},
            {"end_tick": 19},
            {"player_observations": [types.SimpleNamespace(player="Multi0")]},
        ):
            candidate = types.SimpleNamespace(**good.__dict__)
            for key, value in mutation.items():
                setattr(candidate, key, value)
            with self.subTest(mutation=mutation), self.assertRaises(bench.ContractError):
                bench.validate_joint_response(candidate, "session-a", 8)

    def test_occupied_endpoint_fails_before_runtime_contact(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
        try:
            with self.assertRaises(bench.ContractError):
                bench.ensure_endpoint_unoccupied(port)
        finally:
            listener.close()

    def test_remaining_matrix_cells_are_explicitly_terminal(self):
        ledger = bench.CellLedger()
        ledger.finalize("c1-t1", "timeout", {})
        bench.finalize_unexecuted_cells(
            ledger,
            [
                {"concurrency": 1, "ticks_per_joint_advance": 8},
                {"concurrency": 2, "ticks_per_joint_advance": 1},
            ],
            blocked_by="c1-t1",
        )
        cells = ledger.values()
        self.assertEqual([cell.terminal for cell in cells], ["timeout", "not_executed", "not_executed"])
        self.assertTrue(all(cell.payload.get("blocked_by") == "c1-t1" for cell in cells[1:]))

    def test_daemon_log_capture_drains_and_bounds_tail(self):
        payload = (b"prefix\n" * 20_000) + b"terminal-tail"
        capture = bench.BoundedLogCapture(io.BytesIO(payload), max_tail_bytes=1024)
        capture.start()
        result = capture.finish()
        self.assertEqual(result["total_bytes"], len(payload))
        self.assertEqual(result["tail_bytes"], 1024)
        self.assertTrue(result["tail_utf8"].endswith("terminal-tail"))
        self.assertTrue(result["drain_thread_retired"])
        self.assertIsNone(result["drain_error"])

    def test_python_310_compatible_deadline_primitive(self):
        source = Path(bench.__file__).read_text(encoding="utf-8")
        self.assertNotIn("asyncio.timeout(", source)
        self.assertIn("asyncio.wait_for(", source)


class EvidencePublicationTests(unittest.TestCase):
    def test_create_only_publication_is_immutable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = b'{"terminal":"completed"}\n'
            result = bench.publish_evidence_create_only(output, payload)
            self.assertEqual(output.read_bytes(), payload)
            self.assertEqual(result["bytes"], len(payload))
            self.assertEqual(os.stat(output).st_mode & 0o777, 0o400)
            with self.assertRaises(FileExistsError):
                bench.publish_evidence_create_only(output, b"replacement")
            self.assertEqual(output.read_bytes(), payload)

    def test_interrupted_publication_leaves_recognizable_pending_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            with mock.patch("bench_joint_advance.os.link", side_effect=OSError("fixture crash")):
                with self.assertRaises(OSError):
                    bench.publish_evidence_create_only(output, b"payload")
            self.assertFalse(output.exists())
            pending = list(Path(directory).glob(".evidence.json.*.pending"))
            self.assertEqual(len(pending), 1)
            self.assertEqual(pending[0].read_bytes(), b"payload")


if __name__ == "__main__":
    unittest.main()
