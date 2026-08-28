#!/usr/bin/env python3
"""Source-only contract tests for bench_joint_advance.py."""

import asyncio
import base64
import hashlib
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import bench_joint_advance as bench


BENCHMARK_SOURCE_SHA = "a" * 40


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

    def test_seed_slot_range_stays_within_runtime_integer_domain(self):
        base = [
            "plan",
            "--engine-sha", bench.FROZEN_ENGINE_SHA,
            "--war-college-sha", bench.FROZEN_WAR_COLLEGE_SHA,
            "--benchmark-source-sha", BENCHMARK_SOURCE_SHA,
        ]
        accepted = bench.parser().parse_args(
            base + ["--seed", "2147483647", "--concurrency", "1"],
        )
        self.assertEqual(bench.normalized_args(accepted)["seed"], 2_147_483_647)

        rejected = bench.parser().parse_args(
            base + ["--seed", "2147483647", "--concurrency", "1,8"],
        )
        with self.assertRaisesRegex(bench.ContractError, "runtime integer domain"):
            bench.normalized_args(rejected)


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
            bench.FROZEN_WAR_COLLEGE_SHA,
            BENCHMARK_SOURCE_SHA,
            bench.GENERATION,
        )
        self.parameters = {"concurrency": (1,), "tick_batches": (8,)}
        self.operation = bench.operation_descriptor(
            self.provenance,
            self.parameters,
            designated_hostname="fixture",
            openra_dir=Path("/tmp/frozen-openra"),
        )

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
                operation=self.operation,
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
            operation=self.operation,
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
                operation=self.operation,
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

    def test_only_reviewed_frozen_provenance_is_admitted(self):
        for engine_sha, war_college_sha, benchmark_source_sha, generation in (
            ("7" * 40, bench.FROZEN_WAR_COLLEGE_SHA, BENCHMARK_SOURCE_SHA, bench.GENERATION),
            (bench.FROZEN_ENGINE_SHA, "7" * 40, BENCHMARK_SOURCE_SHA, bench.GENERATION),
            (bench.FROZEN_ENGINE_SHA, bench.FROZEN_WAR_COLLEGE_SHA, "7" * 39, bench.GENERATION),
            (bench.FROZEN_ENGINE_SHA, bench.FROZEN_WAR_COLLEGE_SHA, BENCHMARK_SOURCE_SHA, "7" * 16),
        ):
            with self.subTest(
                engine_sha=engine_sha,
                war_college_sha=war_college_sha,
                generation=generation,
            ), self.assertRaises(bench.ContractError):
                bench.validate_provenance(
                    engine_sha, war_college_sha, benchmark_source_sha, generation,
                )


class RuntimeBoundaryTests(unittest.TestCase):
    def test_runtime_provenance_separates_benchmark_and_frozen_comparison(self):
        with tempfile.TemporaryDirectory() as directory:
            openra_dir = Path(directory)
            (openra_dir / "bin").mkdir()
            (openra_dir / "bin" / "OpenRA.dll").write_bytes(b"engine")
            expected = bench.validate_provenance(
                bench.FROZEN_ENGINE_SHA,
                bench.FROZEN_WAR_COLLEGE_SHA,
                BENCHMARK_SOURCE_SHA,
                bench.GENERATION,
            )
            source = Path(bench.__file__).read_bytes()
            with mock.patch(
                "bench_joint_advance.git_head",
                side_effect=[BENCHMARK_SOURCE_SHA, bench.FROZEN_ENGINE_SHA],
            ), mock.patch(
                "bench_joint_advance.committed_file_bytes", return_value=source,
            ), mock.patch(
                "bench_joint_advance.subprocess.check_output", return_value="8.0.0\n",
            ):
                report = bench.runtime_provenance(openra_dir, expected)
            self.assertEqual(report["benchmark_source_git_head"], BENCHMARK_SOURCE_SHA)
            self.assertEqual(
                report["frozen_war_college_comparison_sha"],
                bench.FROZEN_WAR_COLLEGE_SHA,
            )
            self.assertEqual(
                report["benchmark_source_sha256"],
                hashlib.sha256(source).hexdigest(),
            )

    def test_runtime_provenance_rejects_wrong_or_uncommitted_benchmark(self):
        with tempfile.TemporaryDirectory() as directory:
            openra_dir = Path(directory)
            (openra_dir / "bin").mkdir()
            (openra_dir / "bin" / "OpenRA.dll").write_bytes(b"engine")
            expected = bench.validate_provenance(
                bench.FROZEN_ENGINE_SHA,
                bench.FROZEN_WAR_COLLEGE_SHA,
                BENCHMARK_SOURCE_SHA,
                bench.GENERATION,
            )
            with mock.patch(
                "bench_joint_advance.git_head",
                side_effect=["b" * 40, bench.FROZEN_ENGINE_SHA],
            ), self.assertRaisesRegex(bench.ContractError, "benchmark source Git HEAD"):
                bench.runtime_provenance(openra_dir, expected)

            with mock.patch(
                "bench_joint_advance.git_head",
                side_effect=[BENCHMARK_SOURCE_SHA, bench.FROZEN_ENGINE_SHA],
            ), mock.patch(
                "bench_joint_advance.committed_file_bytes", return_value=b"copied-or-modified",
            ), self.assertRaisesRegex(bench.ContractError, "running benchmark bytes"):
                bench.runtime_provenance(openra_dir, expected)

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
    @staticmethod
    def payload():
        provenance = bench.validate_provenance(
                bench.FROZEN_ENGINE_SHA,
                bench.FROZEN_WAR_COLLEGE_SHA,
                BENCHMARK_SOURCE_SHA,
                bench.GENERATION,
            )
        parameters = {
            "concurrency": [1], "tick_batches": [1], "samples": 1,
            "repetitions": 2, "seed": 2050, "rpc_timeout_s": 60,
            "cell_timeout_s": 900, "teardown_timeout_s": 10,
            "ready_timeout_s": 30, "port": 9999,
            "map_name": bench.MAP_NAME, "bots": bench.BOTS,
        }
        operation = bench.operation_descriptor(
            provenance,
            parameters,
            designated_hostname="fixture",
            openra_dir=Path("/tmp/frozen-openra"),
        )
        digest = "b" * 64

        def repetition(index):
            session_id = f"session-{index}"
            latency = {"count": 1, "min_ms": 1.0, "p50_ms": 1.0,
                       "p95_ms": 1.0, "max_ms": 1.0}
            return {
                "repetition": index,
                "seed_by_slot": {"0": 2050},
                "session_id_by_slot": {"0": session_id},
                "create_latency": latency,
                "joint_advance_latency": latency,
                "joint_advance_calls": 1,
                "ticks_advanced_validated": 1,
                "validated_ticks_per_second": 1.0,
                "canonical_hash_by_slot": {"0": digest},
                "joint_advance_validation_by_slot": {
                    "0": [{"start_tick": 10, "end_tick": 11,
                           "players": ["Multi0", "Multi1"]}],
                },
                "teardown": {
                    "failures": [], "latency": latency,
                    "latency_samples_ms": [1.0],
                    "attempted_session_ids": [session_id],
                    "destroyed_session_ids": [session_id],
                    "unretired_session_ids": [],
                    "teardown_total_deadline_s": 10,
                    "cleanup_terminal": "complete",
                    "create_commit_response_ambiguous": False,
                    "cleanup_after_work_cancellation": False,
                    "containment_required": False,
                },
                "wall_seconds": 1.0,
            }

        repetitions = [repetition(0), repetition(1)]
        cell = {
            "key": "c1-t1", "terminal": "success", "concurrency": 1,
            "ticks_per_joint_advance": 1, "process_rss_bytes": {
                "before": 1024, "peak": 2048, "after": 1536,
            },
            "repetitions": repetitions, "same_seed_deterministic": True,
            "hashes_by_slot": {"0": [digest, digest]}, "cell_wall_seconds": 2.0,
            "teardown_failures": [],
            "teardown_latency": {"count": 2, "min_ms": 1.0, "p50_ms": 1.0,
                                  "p95_ms": 1.0, "max_ms": 1.0},
            "teardown_attempted_session_ids": ["session-0", "session-1"],
            "teardown_destroyed_session_ids": ["session-0", "session-1"],
            "teardown_unretired_session_ids": [],
            "create_commit_response_ambiguous": False,
            "cleanup_after_work_cancellation": False,
            "daemon_identity_lost": False,
            "containment_required": False,
            "cleanup_terminals": ["complete", "complete"],
        }
        report = bench.build_report(
            provenance=provenance,
            parameters=parameters,
            cells=[cell],
            executed_designated_host=True,
            generated_at_utc="2026-08-27T00:00:00Z",
            command=["unit-test"],
            run={
                "terminal": "completed", "stage": "matrix_complete",
                "error_type": None, "error": None,
                "listener_identity": {"pid": 123, "port": 9999,
                                      "socket_inode": "456", "proc_table": "tcp"},
                "runtime_provenance": {
                    "benchmark_source_git_head": BENCHMARK_SOURCE_SHA,
                    "benchmark_source_sha256": "c" * 64,
                    "frozen_war_college_comparison_sha": bench.FROZEN_WAR_COLLEGE_SHA,
                    "engine_git_head": bench.FROZEN_ENGINE_SHA,
                    "openra_binary_sha256": "d" * 64,
                    "dotnet_version": "10.0.0",
                    "dotnet_version_sha256": "e" * 64,
                },
                "daemon_log": {"total_bytes": 0, "sha256": hashlib.sha256(b"").hexdigest(),
                               "tail_utf8": "", "tail_bytes": 0, "drain_error": None,
                               "drain_thread_retired": True},
                "cleanup": {"failures": []},
                "containment": {"required_by_cell": False, "boundary": "not_required",
                                "daemon_retired": True},
                "daemon_returncode": 0,
            },
            host={"hostname": "fixture", "designated_hostname": "fixture",
                  "platform": "fixture-platform", "python": "3.10.0", "cpu_count": 2},
            operation=operation,
        )
        return bench.stable_json(report).encode("utf-8")

    @staticmethod
    def operation(payload):
        return json.loads(payload)["operation"]

    def test_post_cell_daemon_identity_loss_is_publishable_and_requires_retirement(self):
        report = json.loads(self.payload())
        success = report["cells"][0]
        cell = {
            "concurrency": success["concurrency"],
            "ticks_per_joint_advance": success["ticks_per_joint_advance"],
        }
        process_rss = success["process_rss_bytes"]
        payload = {
            key: value
            for key, value in success.items()
            if key not in {
                "key", "terminal", "concurrency", "ticks_per_joint_advance",
                "process_rss_bytes",
            }
        }

        terminal, failure = bench.bind_post_cell_daemon_identity(
            "success",
            payload,
            cell,
            process_rss,
            identity_intact=False,
        )

        self.assertEqual(terminal, "rpc_error")
        self.assertEqual(failure["completed_repetitions"], 2)
        self.assertTrue(failure["daemon_identity_lost"])
        self.assertTrue(failure["containment_required"])
        self.assertIn("daemon_retirement_required", failure["cleanup_terminals"])
        for success_only in (
            "repetitions", "same_seed_deterministic", "hashes_by_slot",
            "cell_wall_seconds",
        ):
            self.assertNotIn(success_only, failure)
        bench._validate_cell_evidence(
            {"key": "c1-t1", "terminal": terminal, **failure},
            report["parameters"],
        )

    def test_post_cell_identity_loss_preserves_partial_failure_progress(self):
        report = json.loads(self.payload())
        success = report["cells"][0]
        partial_failure = {
            key: value
            for key, value in success.items()
            if key in {
                "teardown_failures", "teardown_latency",
                "teardown_attempted_session_ids", "teardown_destroyed_session_ids",
                "teardown_unretired_session_ids", "create_commit_response_ambiguous",
                "cleanup_after_work_cancellation", "daemon_identity_lost",
                "containment_required", "cleanup_terminals",
            }
        }
        partial_failure.update({
            "error_type": "TimeoutError",
            "error": "cell deadline expired",
            "completed_repetitions": 1,
        })

        terminal, failure = bench.bind_post_cell_daemon_identity(
            "rpc_error",
            partial_failure,
            {
                "concurrency": success["concurrency"],
                "ticks_per_joint_advance": success["ticks_per_joint_advance"],
            },
            success["process_rss_bytes"],
            identity_intact=False,
        )

        self.assertEqual(terminal, "rpc_error")
        self.assertEqual(failure["completed_repetitions"], 1)
        self.assertEqual(failure["error_type"], "DaemonIdentityError")
        self.assertTrue(failure["containment_required"])
        bench._validate_cell_evidence(
            {"key": "c1-t1", "terminal": terminal, **failure},
            report["parameters"],
        )

    def test_create_only_publication_is_immutable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            result = bench.publish_evidence_create_only(output, payload)
            self.assertEqual(output.read_bytes(), payload)
            self.assertEqual(result["bytes"], len(payload))
            self.assertEqual(os.stat(output).st_mode & 0o777, 0o400)
            receipt = bench._commit_receipt_path(output)
            self.assertTrue(receipt.exists())
            self.assertEqual(receipt.stat().st_mode & 0o777, 0o400)
            self.assertEqual(result["commit_receipt"]["path"], str(receipt))
            local = bench.load_locally_committed_evidence(
                output, self.operation(payload),
            )
            self.assertEqual(local["marker"], bench.LOCAL_EVIDENCE_MARKER)
            self.assertEqual(local["schema_version"], 1)
            self.assertIs(local["countable"], False)
            self.assertEqual(local["producer_authentication"], "ABSENT")
            self.assertEqual(local["report"], json.loads(payload))
            self.assertEqual(
                local["commit_receipt"]["evidence_sha256"],
                hashlib.sha256(payload).hexdigest(),
            )
            with self.assertRaises(FileExistsError):
                bench.publish_evidence_create_only(output, b"replacement")
            self.assertEqual(output.read_bytes(), payload)

    def test_locally_self_issued_receipt_is_not_producer_authentication(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            bench.publish_evidence_create_only(output, payload)
            with self.assertRaisesRegex(
                bench.ContractError, "externally bound immutable trust root",
            ):
                bench.load_committed_evidence(output, self.operation(payload))
            with self.assertRaisesRegex(TypeError, "trusted_producer_validator"):
                bench.load_committed_evidence(
                    output,
                    self.operation(payload),
                    trusted_producer_validator=lambda _report, _receipt: False,
                )

    def test_claimant_callback_cannot_promote_publicly_constructible_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            bench.publish_evidence_create_only(output, payload)

            local = bench.load_locally_committed_evidence(
                output, self.operation(payload),
            )
            self.assertEqual(local["report"]["runtime_evidence"], "EXECUTED")
            self.assertEqual(local["report"]["run"]["terminal"], "completed")
            self.assertIs(local["countable"], False)

            claimant_validator = lambda _report, _receipt: True
            with self.assertRaisesRegex(TypeError, "trusted_producer_validator"):
                bench.load_committed_evidence(
                    output,
                    self.operation(payload),
                    trusted_producer_validator=claimant_validator,
                )
            with self.assertRaisesRegex(
                bench.ContractError, "not countable",
            ):
                bench.load_committed_evidence(output, self.operation(payload))

    def test_first_publication_rejects_skeletal_and_cross_field_evidence(self):
        payload = self.payload()
        report = json.loads(payload)
        variants = {}

        candidate = json.loads(payload)
        candidate["host"] = {"hostname": "fixture"}
        variants["skeletal-host"] = candidate

        candidate = json.loads(payload)
        candidate["run"] = {"terminal": "completed"}
        variants["skeletal-run"] = candidate

        candidate = json.loads(payload)
        candidate["cells"][0] = {"key": "c1-t1", "terminal": "success"}
        variants["skeletal-cell"] = candidate

        candidate = json.loads(payload)
        candidate["cells"][0]["same_seed_deterministic"] = False
        variants["success-not-deterministic"] = candidate

        candidate = json.loads(payload)
        candidate["cells"][0]["repetitions"][0]["seed_by_slot"]["0"] = 2051
        variants["seed-not-bound-to-operation"] = candidate

        candidate = json.loads(payload)
        candidate["cells"][0]["repetitions"][0]["validated_ticks_per_second"] = 1.0000000000000002
        variants["throughput-not-bound-to-validated-ticks-and-wall-time"] = candidate

        candidate = json.loads(payload)
        candidate["cells"][0]["repetitions"][0]["wall_seconds"] = 0.0
        candidate["cells"][0]["repetitions"][0]["validated_ticks_per_second"] = 0.0
        variants["positive-validated-work-with-zero-wall-time"] = candidate

        candidate = json.loads(payload)
        candidate["cells"][0]["repetitions"][0]["wall_seconds"] = 1
        candidate["cells"][0]["repetitions"][0]["validated_ticks_per_second"] = 1
        variants["throughput-operands-not-canonical-floats"] = candidate

        candidate = json.loads(payload)
        candidate["run"]["containment"]["daemon_retired"] = False
        variants["completed-daemon-not-retired"] = candidate

        for label, candidate in variants.items():
            with self.subTest(label=label):
                candidate_payload = bench.stable_json(candidate).encode("utf-8")
                with self.assertRaises(bench.ContractError):
                    bench._validate_recoverable_evidence(candidate_payload)
                with tempfile.TemporaryDirectory() as directory:
                    output = Path(directory) / "evidence.json"
                    with self.assertRaises(bench.ContractError):
                        bench.publish_evidence_create_only(output, candidate_payload)

    def test_commit_receipt_is_required_and_content_binds_final_report(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            bench.publish_evidence_create_only(output, payload)
            receipt = bench._commit_receipt_path(output)

            receipt.unlink()
            with self.assertRaises(FileNotFoundError):
                bench.load_committed_evidence(output, self.operation(payload))

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            bench.publish_evidence_create_only(output, payload)
            output.chmod(0o600)
            output.write_bytes(payload + b"\n")
            output.chmod(0o400)
            with self.assertRaises(bench.ContractError):
                bench.load_committed_evidence(output, self.operation(payload))

        for field, value in (
            ("schema_version", True),
            ("evidence_bytes", str(len(payload))),
            ("state", ["COMMITTED"]),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                bench.publish_evidence_create_only(output, payload)
                receipt = bench._commit_receipt_path(output)
                candidate = json.loads(receipt.read_bytes())
                candidate[field] = value
                receipt.chmod(0o600)
                receipt.write_bytes(bench.stable_json(candidate).encode("utf-8"))
                receipt.chmod(0o400)
                with self.assertRaisesRegex(bench.ContractError, "scalar types"):
                    bench.load_committed_evidence(output, self.operation(payload))

    def test_abrupt_termination_before_commit_receipt_is_not_countable(self):
        payload = self.payload()
        script = """
import base64
import os
import sys
from pathlib import Path
import bench_joint_advance as bench

output = Path(sys.argv[1])
payload = base64.b64decode(sys.argv[2])
mode = sys.argv[3]
reservation = bench.reserve_evidence_namespace(output)

def crash(*_args, **_kwargs):
    os._exit(91)

if mode == "before-final-link":
    bench._link_open_inode_create_only = crash
elif mode == "after-final-link-before-receipt":
    bench._publish_commit_receipt_create_only = crash
else:
    raise AssertionError(mode)

bench.publish_evidence_create_only(output, payload, reservation=reservation)
"""
        for mode, final_exists in (
            ("before-final-link", False),
            ("after-final-link-before-receipt", True),
        ):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-c",
                        script,
                        str(output),
                        base64.b64encode(payload).decode("ascii"),
                        mode,
                    ],
                    cwd=Path(__file__).parent,
                    check=False,
                )
                self.assertEqual(completed.returncode, 91)
                pending = Path(directory) / ".evidence.json.pending"
                self.assertEqual(pending.read_bytes(), payload)
                self.assertEqual(output.exists(), final_exists)
                self.assertFalse(bench._commit_receipt_path(output).exists())
                # The report schema may be closed, but no consumer may treat it
                # as committed completion without the independent receipt.
                self.assertEqual(
                    bench._validate_recoverable_evidence(pending.read_bytes()),
                    json.loads(payload),
                )
                with self.assertRaises(FileNotFoundError):
                    bench.load_committed_evidence(output, self.operation(payload))

    def test_interrupted_publication_requires_explicit_reconciliation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            with mock.patch(
                "bench_joint_advance._link_open_inode_create_only",
                side_effect=OSError("fixture crash"),
            ):
                with self.assertRaises(OSError):
                    bench.publish_evidence_create_only(output, payload)
            self.assertFalse(output.exists())
            pending = list(Path(directory).glob(".evidence.json.pending"))
            self.assertEqual(len(pending), 1)
            self.assertEqual(pending[0].read_bytes(), payload)
            with self.assertRaisesRegex(bench.ContractError, "automatic recovery"):
                bench.require_unused_evidence_namespace(output)
            self.assertFalse(output.exists())
            self.assertEqual(pending[0].read_bytes(), payload)

    def test_preexisting_pending_is_never_automatic_authority(self):
        payload = self.payload()
        report = json.loads(payload)
        variants = {}

        for field in ("cells", "host"):
            candidate = dict(report)
            candidate.pop(field)
            variants[f"missing-{field}"] = bench.stable_json(candidate).encode("utf-8")

        candidate = dict(report)
        candidate["unexpected"] = True
        variants["extra-field"] = bench.stable_json(candidate).encode("utf-8")

        candidate = dict(report)
        candidate["cells"] = []
        variants["incomplete-completed-matrix"] = bench.stable_json(candidate).encode("utf-8")
        variants["noncanonical-json"] = json.dumps(report, indent=2).encode("utf-8")

        for label, candidate_payload in variants.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / "evidence.json"
                pending = Path(directory) / ".evidence.json.pending"
                pending.write_bytes(candidate_payload)
                pending.chmod(0o400)
                with self.assertRaisesRegex(bench.ContractError, "automatic recovery"):
                    bench.require_unused_evidence_namespace(output)
                self.assertFalse(output.exists())
                self.assertEqual(pending.read_bytes(), candidate_payload)

    def test_post_link_directory_fsync_failure_requires_reconciliation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            real_fsync_directory = bench._fsync_directory
            calls = 0

            def fail_second(path):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("fixture parent fsync failure")
                return real_fsync_directory(path)

            with mock.patch("bench_joint_advance._fsync_directory", side_effect=fail_second):
                with self.assertRaises(OSError):
                    bench.publish_evidence_create_only(output, payload)
                self.assertTrue(output.exists())
                self.assertTrue((Path(directory) / ".evidence.json.pending").exists())
                with self.assertRaises(FileExistsError):
                    bench.require_unused_evidence_namespace(output)
            self.assertTrue((Path(directory) / ".evidence.json.pending").exists())
            self.assertEqual(output.read_bytes(), payload)

    def test_pending_name_is_fenced_before_final_link(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            order = []
            real_fsync_directory = bench._fsync_directory
            real_link = bench._link_open_inode_create_only

            def record_directory_fsync(path):
                order.append("directory_fsync")
                return real_fsync_directory(path)

            def record_link(descriptor, parent_descriptor, destination_name):
                order.append("link")
                return real_link(descriptor, parent_descriptor, destination_name)

            with mock.patch(
                "bench_joint_advance._fsync_directory", side_effect=record_directory_fsync,
            ), mock.patch(
                "bench_joint_advance._link_open_inode_create_only",
                side_effect=record_link,
            ):
                bench.publish_evidence_create_only(output, payload)
            self.assertEqual(order[:3], ["directory_fsync", "link", "directory_fsync"])

    def test_pending_name_fsync_failure_cannot_publish_final(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            with mock.patch(
                "bench_joint_advance._fsync_directory",
                side_effect=OSError("fixture pending-name fsync failure"),
            ), mock.patch(
                "bench_joint_advance._link_open_inode_create_only",
            ) as link:
                with self.assertRaises(OSError):
                    bench.publish_evidence_create_only(output, payload)
            link.assert_not_called()
            self.assertFalse(output.exists())
            self.assertTrue((Path(directory) / ".evidence.json.pending").exists())

    def test_pending_replacement_after_fsync_cannot_cross_commit_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            payload = self.payload()
            foreign = b"foreign-generation"
            real_assert = bench._assert_entry_generation
            replaced = False

            def replace_then_assert(parent_descriptor, name, descriptor, label):
                nonlocal replaced
                if not replaced:
                    replaced = True
                    pending.unlink()
                    pending.write_bytes(foreign)
                    pending.chmod(0o400)
                return real_assert(parent_descriptor, name, descriptor, label)

            with mock.patch(
                "bench_joint_advance._assert_entry_generation",
                side_effect=replace_then_assert,
            ):
                with self.assertRaisesRegex(bench.ContractError, "changed generation"):
                    bench.publish_evidence_create_only(output, payload)
            self.assertFalse(output.exists())
            self.assertEqual(pending.read_bytes(), foreign)

    def test_parent_replacement_before_link_cannot_redirect_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / "current"
            moved = root / "owned-attempt"
            parent.mkdir()
            output = parent / "evidence.json"
            payload = self.payload()
            real_link = bench._link_open_inode_create_only
            replaced = False

            def replace_parent_then_link(descriptor, parent_descriptor, destination_name):
                nonlocal replaced
                if not replaced:
                    replaced = True
                    parent.rename(moved)
                    parent.mkdir()
                return real_link(descriptor, parent_descriptor, destination_name)

            with mock.patch(
                "bench_joint_advance._link_open_inode_create_only",
                side_effect=replace_parent_then_link,
            ):
                with self.assertRaisesRegex(
                    bench.ContractError, "parent namespace changed generation",
                ):
                    bench.publish_evidence_create_only(output, payload)

            self.assertTrue(parent.is_dir())
            self.assertEqual(list(parent.iterdir()), [])
            self.assertEqual((moved / "evidence.json").read_bytes(), payload)
            self.assertEqual((moved / ".evidence.json.pending").read_bytes(), payload)

    def test_parent_replacement_after_link_before_fsync_cannot_return_success(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / "current"
            moved = root / "owned-attempt"
            parent.mkdir()
            output = parent / "evidence.json"
            payload = self.payload()
            real_fsync_directory = bench._fsync_directory
            calls = 0

            def replace_parent_before_second_fsync(path_or_descriptor):
                nonlocal calls
                calls += 1
                if calls == 2:
                    parent.rename(moved)
                    parent.mkdir()
                return real_fsync_directory(path_or_descriptor)

            with mock.patch(
                "bench_joint_advance._fsync_directory",
                side_effect=replace_parent_before_second_fsync,
            ):
                with self.assertRaisesRegex(
                    bench.ContractError, "parent namespace changed generation",
                ):
                    bench.publish_evidence_create_only(output, payload)

            self.assertTrue(parent.is_dir())
            self.assertEqual(list(parent.iterdir()), [])
            self.assertEqual((moved / "evidence.json").read_bytes(), payload)
            self.assertEqual((moved / ".evidence.json.pending").read_bytes(), payload)

    def test_preexisting_valid_pending_is_preserved_without_validation_or_adoption(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            payload = self.payload()
            pending.write_bytes(payload)
            pending.chmod(0o400)
            with mock.patch(
                "bench_joint_advance._validate_recoverable_evidence",
            ) as validate:
                with self.assertRaisesRegex(bench.ContractError, "automatic recovery"):
                    bench.require_unused_evidence_namespace(output)
            validate.assert_not_called()
            self.assertFalse(output.exists())
            self.assertEqual(pending.read_bytes(), payload)

    def test_retry_does_not_open_or_refence_pending_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            pending = Path(directory) / ".evidence.json.pending"
            pending.write_bytes(payload)
            pending.chmod(0o400)
            with mock.patch(
                "bench_joint_advance._fsync_directory",
            ) as directory_fsync, mock.patch(
                "bench_joint_advance._open_regular_read_only",
            ) as open_pending:
                with self.assertRaisesRegex(bench.ContractError, "automatic recovery"):
                    bench.require_unused_evidence_namespace(output)
            directory_fsync.assert_not_called()
            open_pending.assert_not_called()
            self.assertEqual(pending.read_bytes(), payload)

    def test_repetition_admission_rejects_reused_tick_interval(self):
        report = json.loads(self.payload())
        repetition = report["cells"][0]["repetitions"][0]
        repetition["joint_advance_calls"] = 2
        repetition["ticks_advanced_validated"] = 2
        repetition["validated_ticks_per_second"] = 2.0
        repetition["joint_advance_latency"]["count"] = 2
        repetition["joint_advance_validation_by_slot"]["0"] = [
            {"start_tick": 10, "end_tick": 11, "players": ["Multi0", "Multi1"]},
            {"start_tick": 11, "end_tick": 12, "players": ["Multi0", "Multi1"]},
        ]
        bench._validate_repetition_evidence(repetition, "fixture")

        repetition["joint_advance_validation_by_slot"]["0"][1]["start_tick"] = 10
        with self.assertRaisesRegex(bench.ContractError, "not continuous"):
            bench._validate_repetition_evidence(repetition, "fixture")

    def test_committed_final_is_not_downgraded_by_pending_cleanup_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            with mock.patch(
                "bench_joint_advance._retire_pending",
                return_value=(False, "fixture cleanup failure"),
            ):
                result = bench.publish_evidence_create_only(output, payload)
            self.assertEqual(output.read_bytes(), payload)
            self.assertFalse(result["pending_retired"])
            self.assertEqual(result["pending_retirement_error"], "fixture cleanup failure")

    def test_parent_must_preexist_and_mode_precedes_inode_fsync(self):
        with tempfile.TemporaryDirectory() as directory:
            missing_output = Path(directory) / "missing" / "evidence.json"
            with self.assertRaises(FileNotFoundError):
                bench.publish_evidence_create_only(missing_output, self.payload())
            self.assertFalse(missing_output.parent.exists())

            output = Path(directory) / "evidence.json"
            order = []
            real_fchmod = os.fchmod
            real_fsync = os.fsync

            def record_fchmod(fd, mode):
                order.append("fchmod")
                return real_fchmod(fd, mode)

            def record_fsync(fd):
                order.append("fsync")
                return real_fsync(fd)

            with mock.patch("bench_joint_advance.os.fchmod", side_effect=record_fchmod), mock.patch(
                "bench_joint_advance.os.fsync", side_effect=record_fsync,
            ):
                bench.publish_evidence_create_only(output, self.payload())
            self.assertLess(order.index("fchmod"), order.index("fsync"))


class RunRepetitionOwnershipTests(unittest.IsolatedAsyncioTestCase):
    class Pb2:
        @staticmethod
        def CreateSessionRequest(**kwargs):
            return types.SimpleNamespace(**kwargs)

        @staticmethod
        def StateRequest(**kwargs):
            return types.SimpleNamespace(**kwargs)

        @staticmethod
        def PlayerCommandBatch(**kwargs):
            return types.SimpleNamespace(**kwargs)

        @staticmethod
        def JointAdvanceRequest(**kwargs):
            return types.SimpleNamespace(**kwargs)

        @staticmethod
        def DestroySessionRequest(**kwargs):
            return types.SimpleNamespace(**kwargs)

    class Stub:
        def __init__(
            self, *, fail_advance=False, fail_create=False, stall_destroy=False,
            repeat_interval=False,
        ):
            self.destroyed = []
            self.server_created = []
            self.fail_advance = fail_advance
            self.fail_create = fail_create
            self.stall_destroy = stall_destroy
            self.repeat_interval = repeat_interval
            self.next_tick_by_session = {}
            self.blocked_create_cancelled = False
            self.blocked_advance_cancelled = False
            self.teardown_started = False
            self.mutation_after_teardown = False

        async def CreateSession(self, request):
            if self.fail_create and request.seed == 2050:
                raise RuntimeError("fixture create failure")
            if self.fail_create:
                # Model server-side commit before the response is withheld.
                self.server_created.append(f"session-{request.seed}")
                try:
                    await asyncio.sleep(60)
                finally:
                    self.blocked_create_cancelled = True
                    if self.teardown_started:
                        self.mutation_after_teardown = True
            await asyncio.sleep(0.02 if request.seed % 2 == 0 else 0)
            return types.SimpleNamespace(session_id=f"session-{request.seed}")

        async def GetState(self, request):
            return types.SimpleNamespace(phase="playing")

        async def JointAdvance(self, request):
            if self.fail_advance and request.session_id.endswith("2050"):
                raise RuntimeError("fixture advance failure")
            if self.fail_advance:
                try:
                    await asyncio.sleep(60)
                finally:
                    self.blocked_advance_cancelled = True
                    if self.teardown_started:
                        self.mutation_after_teardown = True
            seed = int(request.session_id.rsplit("-", 1)[1])
            start_tick = 10 if self.repeat_interval else self.next_tick_by_session.get(
                request.session_id, 10,
            )
            end_tick = start_tick + request.ticks
            if not self.repeat_interval:
                self.next_tick_by_session[request.session_id] = end_tick
            return types.SimpleNamespace(
                session_id=request.session_id,
                start_tick=start_tick,
                end_tick=end_tick,
                seed=seed,
                player_observations=[
                    types.SimpleNamespace(player="Multi0"),
                    types.SimpleNamespace(player="Multi1"),
                ],
            )

        async def DestroySession(self, request):
            self.teardown_started = True
            if self.stall_destroy and request.session_id.endswith("2050"):
                await asyncio.sleep(60)
            self.destroyed.append(request.session_id)
            return types.SimpleNamespace()

    @staticmethod
    def as_dict(response, preserving_proto_field_name=True):
        del preserving_proto_field_name
        return {
            "session_id": response.session_id,
            "start_tick": response.start_tick,
            "end_tick": response.end_tick,
            "state": {"seed": response.seed},
            "player_observations": [
                {"player": item.player} for item in response.player_observations
            ],
        }

    async def run_fixture(self, stub):
        teardown_records = []
        result = await bench.run_repetition(
            stub=stub,
            pb2=self.Pb2,
            message_to_dict=self.as_dict,
            concurrency=2,
            ticks=8,
            samples=1,
            seed_base=2050,
            repetition=0,
            rpc_timeout_s=1,
            teardown_timeout_s=1,
            teardown_records=teardown_records,
        )
        return result, teardown_records

    async def test_out_of_order_creation_preserves_slot_seed_session_hash_binding(self):
        stub = self.Stub()
        result, teardown_records = await self.run_fixture(stub)
        self.assertEqual(
            result["session_id_by_slot"],
            {"0": "session-2050", "1": "session-2051"},
        )
        self.assertEqual(result["seed_by_slot"], {"0": 2050, "1": 2051})
        self.assertNotEqual(
            result["canonical_hash_by_slot"]["0"],
            result["canonical_hash_by_slot"]["1"],
        )
        self.assertEqual(stub.destroyed, ["session-2050", "session-2051"])
        self.assertEqual(len(teardown_records), 1)

    async def test_repeated_samples_require_continuous_tick_intervals(self):
        teardown_records = []
        result = await bench.run_repetition(
            stub=self.Stub(),
            pb2=self.Pb2,
            message_to_dict=self.as_dict,
            concurrency=1,
            ticks=8,
            samples=2,
            seed_base=2050,
            repetition=0,
            rpc_timeout_s=1,
            teardown_timeout_s=1,
            teardown_records=teardown_records,
        )
        self.assertEqual(
            result["joint_advance_validation_by_slot"]["0"],
            [
                {"start_tick": 10, "end_tick": 18, "players": ["Multi0", "Multi1"]},
                {"start_tick": 18, "end_tick": 26, "players": ["Multi0", "Multi1"]},
            ],
        )
        self.assertEqual(result["joint_advance_calls"], 2)
        self.assertEqual(result["ticks_advanced_validated"], 16)

        repeated = self.Stub(repeat_interval=True)
        with self.assertRaisesRegex(bench.ContractError, "continuous tick advancement"):
            await bench.run_repetition(
                stub=repeated,
                pb2=self.Pb2,
                message_to_dict=self.as_dict,
                concurrency=1,
                ticks=8,
                samples=2,
                seed_base=2050,
                repetition=0,
                rpc_timeout_s=1,
                teardown_timeout_s=1,
                teardown_records=[],
            )
        self.assertEqual(repeated.destroyed, ["session-2050"])

    async def test_failed_advance_retires_sibling_before_teardown(self):
        stub = self.Stub(fail_advance=True)
        teardown_records = []
        with self.assertRaises(RuntimeError):
            await bench.run_repetition(
                stub=stub,
                pb2=self.Pb2,
                message_to_dict=self.as_dict,
                concurrency=2,
                ticks=8,
                samples=1,
                seed_base=2050,
                repetition=0,
                rpc_timeout_s=1,
                teardown_timeout_s=1,
                teardown_records=teardown_records,
            )
        self.assertTrue(stub.blocked_advance_cancelled)
        self.assertFalse(stub.mutation_after_teardown)
        self.assertEqual(stub.destroyed, ["session-2050", "session-2051"])
        self.assertEqual(len(teardown_records), 1)

    async def test_failed_create_retires_sibling_before_teardown(self):
        stub = self.Stub(fail_create=True)
        teardown_records = []
        with self.assertRaises(RuntimeError):
            await bench.run_repetition(
                stub=stub,
                pb2=self.Pb2,
                message_to_dict=self.as_dict,
                concurrency=2,
                ticks=8,
                samples=1,
                seed_base=2050,
                repetition=0,
                rpc_timeout_s=1,
                teardown_timeout_s=1,
                teardown_records=teardown_records,
            )
        self.assertTrue(stub.blocked_create_cancelled)
        self.assertFalse(stub.mutation_after_teardown)
        self.assertEqual(stub.destroyed, [])
        self.assertEqual(len(teardown_records), 1)
        self.assertEqual(stub.server_created, ["session-2051"])
        self.assertTrue(teardown_records[0]["create_commit_response_ambiguous"])
        self.assertTrue(teardown_records[0]["containment_required"])
        self.assertEqual(
            teardown_records[0]["cleanup_terminal"],
            "daemon_retirement_required",
        )

    async def test_cell_deadline_cannot_cancel_known_session_cleanup(self):
        stub = self.Stub(stall_destroy=True)
        terminal, payload = await bench.run_cell(
            stub=stub,
            pb2=self.Pb2,
            message_to_dict=self.as_dict,
            concurrency=2,
            ticks=8,
            samples=1,
            repetitions=2,
            seed_base=2050,
            rpc_timeout_s=1,
            cell_timeout_s=0.04,
            teardown_timeout_s=0.05,
        )
        self.assertEqual(terminal, "timeout")
        self.assertTrue(payload["cleanup_after_work_cancellation"])
        self.assertEqual(
            payload["teardown_attempted_session_ids"],
            ["session-2050", "session-2051"],
        )
        self.assertEqual(payload["teardown_destroyed_session_ids"], ["session-2051"])
        self.assertEqual(payload["teardown_unretired_session_ids"], ["session-2050"])
        self.assertTrue(payload["containment_required"])
        self.assertIn("daemon_retirement_required", payload["cleanup_terminals"])


class RetryRecoveryTests(unittest.TestCase):
    @staticmethod
    def invocation(directory, output, *, seed="2050", hostname="fixture"):
        argv = [
                "run",
                "--engine-sha", bench.FROZEN_ENGINE_SHA,
                "--war-college-sha", bench.FROZEN_WAR_COLLEGE_SHA,
                "--benchmark-source-sha", BENCHMARK_SOURCE_SHA,
                "--generation", bench.GENERATION,
                "--concurrency", "1",
                "--tick-batches", "1",
                "--samples", "1",
                "--repetitions", "2",
                "--execute-designated-host",
                "--openra-dir", directory,
                "--output", str(output),
                "--designated-hostname", hostname,
                "--seed", seed,
            ]
        parsed = bench.parser().parse_args(argv)
        provenance = bench.validate_provenance(
            parsed.engine_sha,
            parsed.war_college_sha,
            parsed.benchmark_source_sha,
            parsed.generation,
        )
        parameters = bench.normalized_args(parsed)
        operation = bench.operation_descriptor(
            provenance,
            parameters,
            designated_hostname=hostname,
            openra_dir=Path(directory),
        )
        del provenance, parameters, operation
        return argv, EvidencePublicationTests.payload()

    @staticmethod
    def completed_outcome(payload):
        report = json.loads(payload)
        return {
            "cells": report["cells"],
            "run": report["run"],
            "host": report["host"],
        }

    def test_main_durably_reserves_exact_pending_inode_before_runtime_contact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            argv, payload = self.invocation(directory, output)

            async def execute_runtime(*_args, **_kwargs):
                self.assertTrue(pending.exists())
                self.assertEqual(pending.stat().st_mode & 0o777, 0o400)
                self.assertEqual(pending.stat().st_size, 0)
                with self.assertRaisesRegex(bench.ContractError, "automatic recovery"):
                    bench.reserve_evidence_namespace(output)
                return self.completed_outcome(payload)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "bench_joint_advance.execute_runtime", side_effect=execute_runtime,
            ) as runtime, mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
                self.assertEqual(bench.main(argv), 0)
            runtime.assert_called_once()
            self.assertTrue(output.exists())
            self.assertFalse(pending.exists())
            self.assertEqual(output.stat().st_mode & 0o777, 0o400)
            self.assertEqual(json.loads(stdout.getvalue())["run"]["terminal"], "completed")

    def test_final_name_race_preserves_foreign_final_and_exact_pending_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            argv, payload = self.invocation(directory, output)
            foreign = b"foreign-final-generation"

            async def execute_runtime(*_args, **_kwargs):
                self.assertTrue(pending.exists())
                output.write_bytes(foreign)
                return self.completed_outcome(payload)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "bench_joint_advance.execute_runtime", side_effect=execute_runtime,
            ) as runtime, mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
                self.assertEqual(bench.main(argv), 1)
            runtime.assert_called_once()
            self.assertEqual(output.read_bytes(), foreign)
            self.assertTrue(pending.exists())
            self.assertEqual(pending.stat().st_mode & 0o777, 0o400)
            pending_report = json.loads(pending.read_bytes())
            stdout_report = json.loads(stdout.getvalue())
            self.assertEqual(pending_report["run"]["terminal"], "output_error")
            self.assertEqual(stdout_report["run"]["terminal"], "output_error")
            self.assertEqual(pending_report, stdout_report)

    def test_parent_generation_failure_persists_one_output_error_terminal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent = root / "current"
            moved = root / "owned-attempt"
            parent.mkdir()
            output = parent / "evidence.json"
            argv, payload = self.invocation(str(parent), output)
            real_link = bench._link_open_inode_create_only

            async def execute_runtime(*_args, **_kwargs):
                return self.completed_outcome(payload)

            def replace_parent_then_link(descriptor, parent_descriptor, destination_name):
                parent.rename(moved)
                parent.mkdir()
                return real_link(descriptor, parent_descriptor, destination_name)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch(
                "bench_joint_advance.execute_runtime", side_effect=execute_runtime,
            ) as runtime, mock.patch(
                "bench_joint_advance._link_open_inode_create_only",
                side_effect=replace_parent_then_link,
            ), mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
                self.assertEqual(bench.main(argv), 1)

            runtime.assert_called_once()
            self.assertEqual(list(parent.iterdir()), [])
            stdout_report = json.loads(stdout.getvalue())
            pending_report = json.loads((moved / ".evidence.json.pending").read_bytes())
            final_report = json.loads((moved / "evidence.json").read_bytes())
            self.assertEqual(stdout_report["run"]["terminal"], "output_error")
            self.assertEqual(pending_report, stdout_report)
            self.assertEqual(final_report, stdout_report)

    def test_pending_retry_fails_closed_before_runtime_contact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            argv, payload = self.invocation(directory, output)
            pending.write_bytes(payload)
            pending.chmod(0o400)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch("bench_joint_advance.execute_runtime") as execute_runtime, mock.patch(
                "sys.stdout", stdout,
            ), mock.patch("sys.stderr", stderr):
                self.assertEqual(bench.main(argv), 2)
            execute_runtime.assert_not_called()
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("automatic recovery is disabled", stderr.getvalue())
            self.assertTrue(pending.exists())
            self.assertEqual(pending.read_bytes(), payload)
            self.assertEqual(pending.stat().st_mode & 0o777, 0o400)
            self.assertFalse(output.exists())

    def test_changed_invocation_cannot_publish_pending_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            _, old_payload = self.invocation(directory, output, seed="2050")
            changed_argv, _ = self.invocation(directory, output, seed="2051")
            pending.write_bytes(old_payload)
            pending.chmod(0o400)
            with mock.patch("bench_joint_advance.execute_runtime") as execute_runtime:
                self.assertEqual(bench.main(changed_argv), 2)
            execute_runtime.assert_not_called()
            self.assertTrue(pending.exists())
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
