#!/usr/bin/env python3
"""Source-only contract tests for bench_joint_advance.py."""

import asyncio
import hashlib
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
        parameters = {"concurrency": [1], "tick_batches": [1]}
        operation = bench.operation_descriptor(
            provenance,
            parameters,
            designated_hostname="fixture",
            openra_dir=Path("/tmp/frozen-openra"),
        )
        report = bench.build_report(
            provenance=provenance,
            parameters=parameters,
            cells=[{"key": "c1-t1", "terminal": "success"}],
            executed_designated_host=True,
            generated_at_utc="2026-08-27T00:00:00Z",
            command=["unit-test"],
            run={"terminal": "completed"},
            host={"hostname": "fixture"},
            operation=operation,
        )
        return bench.stable_json(report).encode("utf-8")

    @staticmethod
    def operation(payload):
        return json.loads(payload)["operation"]

    def test_create_only_publication_is_immutable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
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
            recovered = bench.recover_owned_evidence(output, self.operation(payload))
            self.assertEqual(recovered, payload)
            self.assertEqual(output.read_bytes(), payload)
            self.assertFalse(pending[0].exists())

    def test_recovery_requires_closed_canonical_report_schema(self):
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
                with self.assertRaises(bench.ContractError):
                    bench.recover_owned_evidence(output, self.operation(payload))
                self.assertFalse(output.exists())
                self.assertEqual(pending.read_bytes(), candidate_payload)

    def test_post_link_directory_fsync_failure_is_recoverable(self):
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
                self.assertEqual(
                    bench.recover_owned_evidence(output, self.operation(payload)), payload
                )
            self.assertFalse((Path(directory) / ".evidence.json.pending").exists())

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

            def record_link(descriptor, destination):
                order.append("link")
                return real_link(descriptor, destination)

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
            real_assert = bench._assert_path_generation
            replaced = False

            def replace_then_assert(path, descriptor, label):
                nonlocal replaced
                if not replaced:
                    replaced = True
                    pending.unlink()
                    pending.write_bytes(foreign)
                    pending.chmod(0o400)
                return real_assert(path, descriptor, label)

            with mock.patch(
                "bench_joint_advance._assert_path_generation",
                side_effect=replace_then_assert,
            ):
                with self.assertRaisesRegex(bench.ContractError, "changed generation"):
                    bench.publish_evidence_create_only(output, payload)
            self.assertFalse(output.exists())
            self.assertEqual(pending.read_bytes(), foreign)

    def test_recovery_replacement_after_validation_cannot_be_adopted_or_deleted(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            pending = Path(directory) / ".evidence.json.pending"
            payload = self.payload()
            foreign = b"foreign-generation"
            pending.write_bytes(payload)
            pending.chmod(0o400)
            real_validate = bench._validate_recoverable_evidence

            def validate_then_replace(candidate, expected_operation=None):
                result = real_validate(candidate, expected_operation)
                pending.unlink()
                pending.write_bytes(foreign)
                pending.chmod(0o400)
                return result

            with mock.patch(
                "bench_joint_advance._validate_recoverable_evidence",
                side_effect=validate_then_replace,
            ):
                with self.assertRaisesRegex(bench.ContractError, "changed generation"):
                    bench.recover_owned_evidence(output, self.operation(payload))
            self.assertFalse(output.exists())
            self.assertEqual(pending.read_bytes(), foreign)

    def test_retry_refences_surviving_pending_name_before_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            payload = self.payload()
            pending = Path(directory) / ".evidence.json.pending"
            pending.write_bytes(payload)
            pending.chmod(0o400)
            order = []
            real_fsync_directory = bench._fsync_directory
            real_open = bench._open_regular_read_only

            def record_directory_fsync(path):
                order.append("directory_fsync")
                return real_fsync_directory(path)

            def record_open(path):
                order.append("open")
                return real_open(path)

            with mock.patch(
                "bench_joint_advance._fsync_directory", side_effect=record_directory_fsync,
            ), mock.patch(
                "bench_joint_advance._open_regular_read_only", side_effect=record_open,
            ):
                recovered = bench.recover_owned_evidence(
                    output, self.operation(payload),
                )
            self.assertEqual(recovered, payload)
            self.assertEqual(order[:2], ["directory_fsync", "open"])

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
        def __init__(self, *, fail_advance=False, fail_create=False, stall_destroy=False):
            self.destroyed = []
            self.server_created = []
            self.fail_advance = fail_advance
            self.fail_create = fail_create
            self.stall_destroy = stall_destroy
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
            return types.SimpleNamespace(
                session_id=request.session_id,
                start_tick=10,
                end_tick=10 + request.ticks,
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
        report = bench.build_report(
            provenance=provenance,
            parameters=parameters,
            cells=[{"key": "c1-t1", "terminal": "success"}],
            executed_designated_host=True,
            generated_at_utc="2026-08-27T00:00:00Z",
            command=argv,
            run={"terminal": "completed"},
            host={"hostname": hostname},
            operation=operation,
        )
        return argv, bench.stable_json(report).encode("utf-8")

    def test_pending_retry_recovers_before_runtime_contact(self):
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
                self.assertEqual(bench.main(argv), 0)
            execute_runtime.assert_not_called()
            self.assertEqual(json.loads(stdout.getvalue())["run"]["terminal"], "completed")
            self.assertFalse(pending.exists())
            self.assertTrue(output.exists())

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
