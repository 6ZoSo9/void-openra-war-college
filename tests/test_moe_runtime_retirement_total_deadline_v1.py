#!/usr/bin/env python3
"""Moe source-only falsifiers for bounded runtime process-group retirement."""

import types
import unittest
from unittest import mock

import bench_joint_advance as bench


class _Clock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, duration):
        self.now += duration


class _Process:
    def __init__(self, clock):
        self.pid = 4242
        self._clock = clock
        self._alive = True
        self.join_timeouts = []

    def join(self, timeout):
        self.join_timeouts.append(timeout)
        if len(self.join_timeouts) == 1:
            self._clock.now += timeout
        elif len(self.join_timeouts) == 2:
            self._clock.now += min(timeout, 0.04)
            self._alive = False

    def is_alive(self):
        return self._alive


class _UnboundProcess:
    def __init__(self, clock):
        self.pid = 4343
        self._clock = clock
        self._alive = True
        self.join_timeouts = []
        self.terminated = False
        self.killed = False

    def join(self, timeout):
        self.join_timeouts.append(timeout)
        if len(self.join_timeouts) == 2:
            self._clock.now += timeout + 0.04
        elif len(self.join_timeouts) == 3:
            self._clock.now += timeout
            self._alive = False

    def is_alive(self):
        return self._alive

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True


class _PipeEnd:
    def __init__(self, messages=None):
        self.messages = list(messages or [])
        self.closed = False
        self.poll_timeouts = []

    def poll(self, timeout):
        self.poll_timeouts.append(timeout)
        return bool(self.messages)

    def recv(self):
        return self.messages.pop(0)

    def close(self):
        self.closed = True


class _ContainedProcess:
    def __init__(self, target, args, name):
        self.target = target
        self.args = args
        self.name = name
        self.pid = 5151
        self.exitcode = None
        self.started = False

    def start(self):
        self.started = True

    def is_alive(self):
        return True


class _SpawnContext:
    def __init__(self, messages):
        self.receiver = _PipeEnd(messages)
        self.sender = _PipeEnd()
        self.pipe_duplex = None
        self.process = None

    def Pipe(self, duplex):
        self.pipe_duplex = duplex
        return self.receiver, self.sender

    def Process(self, *, target, args, name):
        self.process = _ContainedProcess(target, args, name)
        return self.process


class RuntimeRetirementTotalDeadlineTests(unittest.TestCase):
    def test_unbound_child_term_overrun_is_charged_to_kill_budget(self):
        clock = _Clock()
        process = _UnboundProcess(clock)

        with mock.patch.object(
            bench.time, "monotonic", side_effect=clock.monotonic
        ):
            bench._retire_unbound_runtime_child(
                process,
                signal_grace_s=0.1,
            )

        self.assertTrue(process.terminated)
        self.assertTrue(process.killed)
        self.assertEqual(len(process.join_timeouts), 3)
        self.assertEqual(process.join_timeouts[0], 0)
        self.assertAlmostEqual(process.join_timeouts[1], 0.1)
        self.assertAlmostEqual(process.join_timeouts[2], 0.06)
        self.assertLessEqual(clock.now, 0.200001)

    def test_unbound_child_invalid_grace_fails_before_process_contact(self):
        for value in (-0.1, float("nan"), float("inf"), float("-inf"), True, "0.1"):
            process = mock.Mock()

            with self.subTest(value=value), self.assertRaisesRegex(
                bench.ContractError,
                "unbound runtime child signal grace must be finite nonnegative seconds",
            ):
                bench._retire_unbound_runtime_child(
                    process,
                    signal_grace_s=value,
                )

            process.join.assert_not_called()
            process.is_alive.assert_not_called()
            process.terminate.assert_not_called()
            process.kill.assert_not_called()

    def test_unbound_child_deadline_overflow_fails_before_process_contact(self):
        process = mock.Mock()

        with mock.patch.object(
            bench.time, "monotonic", return_value=0.0
        ), self.assertRaisesRegex(
            bench.ContractError,
            "derived unbound runtime child retirement deadlines must be finite",
        ):
            bench._retire_unbound_runtime_child(
                process,
                signal_grace_s=1e308,
            )

        process.join.assert_not_called()
        process.is_alive.assert_not_called()
        process.terminate.assert_not_called()
        process.kill.assert_not_called()

    def test_join_and_group_polling_share_one_total_deadline(self):
        clock = _Clock()
        process = _Process(clock)
        signals = []
        killed_at = [None]

        def signal_group(_pgid, signal_number):
            signals.append(signal_number)
            if signal_number == bench._BootstrapSignal.SIGKILL:
                killed_at[0] = clock.now

        def group_exists(_pgid):
            if killed_at[0] is None:
                return True
            return clock.now < killed_at[0] + 0.1

        with mock.patch.object(
            bench.time, "monotonic", side_effect=clock.monotonic
        ), mock.patch.object(
            bench.time, "sleep", side_effect=clock.sleep
        ), mock.patch.object(
            bench, "_signal_process_group", side_effect=signal_group
        ), mock.patch.object(
            bench, "_process_group_exists", side_effect=group_exists
        ):
            retirement_terminal = bench._retire_runtime_process_group(
                process,
                process.pid,
                natural_grace_s=0.1,
                signal_grace_s=0.1,
            )

        self.assertEqual(
            signals,
            [bench._BootstrapSignal.SIGTERM, bench._BootstrapSignal.SIGKILL],
        )
        self.assertEqual(retirement_terminal, "sigkill_retired")
        self.assertEqual(len(process.join_timeouts), 3)
        self.assertTrue(all(timeout >= 0 for timeout in process.join_timeouts))
        self.assertLessEqual(clock.now, 0.300001)

    def test_group_poll_sleep_never_exceeds_remaining_budget(self):
        clock = _Clock()

        with mock.patch.object(
            bench.time, "monotonic", side_effect=clock.monotonic
        ), mock.patch.object(
            bench.time, "sleep", side_effect=clock.sleep
        ), mock.patch.object(
            bench, "_process_group_exists", return_value=True
        ):
            retired = bench._wait_process_group_absent(4242, 0.005)

        self.assertFalse(retired)
        self.assertLessEqual(clock.now, 0.005001)

    def test_finite_grace_that_overflows_derived_deadline_fails_before_contact(self):
        process = mock.Mock()
        process.pid = 4242

        with self.assertRaisesRegex(
            bench.ContractError, "derived runtime retirement deadlines must be finite"
        ):
            bench._retire_runtime_process_group(
                process,
                process.pid,
                natural_grace_s=1e308,
                signal_grace_s=1e308,
            )

        process.join.assert_not_called()
        process.is_alive.assert_not_called()

    def test_nonfinite_or_invalid_grace_fails_before_process_contact(self):
        for value in (-0.1, float("nan"), float("inf"), float("-inf"), True, "0.1"):
            process = mock.Mock()
            process.pid = 4242

            with self.subTest(value=value), self.assertRaisesRegex(
                bench.ContractError, "must be finite nonnegative seconds"
            ):
                bench._retire_runtime_process_group(
                    process,
                    process.pid,
                    natural_grace_s=value,
                    signal_grace_s=0.1,
                )

            process.join.assert_not_called()


    def test_production_containment_uses_spawn_and_parent_owned_supervisor(self):
        outcome = {"cells": [], "run": {}, "host": {}}
        context = _SpawnContext([
            ("STARTED", 5151, 5151),
            ("OUTCOME", outcome),
        ])
        args = types.SimpleNamespace(
            mode="run",
            execute_designated_host=True,
            designated_hostname="fixture",
            openra_dir="/tmp/frozen-openra",
        )
        parameters = {"samples": 1}
        provenance = {"generation": "test"}

        with mock.patch.object(
            bench._BootstrapMultiprocessing, "get_context", return_value=context,
        ) as get_context, mock.patch.object(
            bench, "_runtime_process_deadline_s", return_value=1.0,
        ), mock.patch.object(
            bench.time, "monotonic", return_value=0.0,
        ), mock.patch.object(
            bench, "_retire_runtime_process_group", return_value="natural_exit",
        ) as retire:
            result = bench._execute_runtime_contained(args, parameters, provenance)

        self.assertEqual(result["cells"], outcome["cells"])
        self.assertEqual(result["run"], outcome["run"])
        self.assertEqual(result["host"], outcome["host"])
        supervisor = result["supervisor"]
        self.assertEqual(supervisor["schema"], bench.SUPERVISOR_SCHEMA)
        self.assertEqual(supervisor["owner"], "parent_process")
        self.assertEqual(supervisor["child_pid"], context.process.pid)
        self.assertEqual(supervisor["child_pgid"], context.process.pid)
        self.assertEqual(supervisor["outer_execution_timeout_s"], 1.0)
        self.assertEqual(supervisor["terminal_source"], "child_outcome")
        self.assertEqual(
            supervisor["containment"]["retirement_terminal"], "natural_exit"
        )
        self.assertTrue(supervisor["authorization_boundary"]["execute_designated_host"])
        self.assertEqual(
            supervisor["authorization_boundary"]["designated_hostname"], "fixture"
        )
        self.assertRegex(
            supervisor["authorization_boundary"]["operation_sha256"],
            r"^[0-9a-f]{64}$",
        )
        get_context.assert_called_once_with("spawn")
        self.assertFalse(context.pipe_duplex)
        self.assertTrue(context.process.started)
        self.assertIs(context.process.target, bench._runtime_child_entry)
        self.assertEqual(
            context.process.args, (context.sender, args, parameters, provenance)
        )
        self.assertEqual(context.process.name, "void-war-college-runtime")
        self.assertTrue(context.sender.closed)
        self.assertTrue(context.receiver.closed)
        retire.assert_called_once_with(context.process, context.process.pid)

    def test_production_containment_rejects_outcome_before_started_binding(self):
        context = _SpawnContext([("OUTCOME", {"cells": []})])
        args = types.SimpleNamespace(
            mode="run",
            execute_designated_host=True,
            designated_hostname="fixture",
            openra_dir="/tmp/frozen-openra",
        )

        with mock.patch.object(
            bench._BootstrapMultiprocessing, "get_context", return_value=context,
        ), mock.patch.object(
            bench.time, "monotonic", return_value=0.0,
        ), mock.patch.object(
            bench, "_retire_unbound_runtime_child",
        ) as retire, self.assertRaisesRegex(
            bench.ContractError,
            "runtime child outcome arrived before process-group binding",
        ):
            bench._execute_runtime_contained(args, {}, {})

        self.assertTrue(context.sender.closed)
        self.assertTrue(context.receiver.closed)
        retire.assert_called_once_with(context.process)


    def test_containment_requires_explicit_designated_host_authorization(self):
        args = types.SimpleNamespace(
            mode="run",
            execute_designated_host=False,
            designated_hostname="fixture",
            openra_dir="/tmp/frozen-openra",
        )
        with mock.patch.object(
            bench._BootstrapMultiprocessing, "get_context",
        ) as get_context, self.assertRaisesRegex(
            bench.ContractError, "explicit designated-host run authorization",
        ):
            bench._execute_runtime_contained(args, {}, {})
        get_context.assert_not_called()

    def test_child_cannot_inject_parent_supervisor_record(self):
        context = _SpawnContext([
            ("STARTED", 5151, 5151),
            ("OUTCOME", {
                "cells": [], "run": {}, "host": {},
                "supervisor": {"owner": "child"},
            }),
        ])
        args = types.SimpleNamespace(
            mode="run",
            execute_designated_host=True,
            designated_hostname="fixture",
            openra_dir="/tmp/frozen-openra",
        )
        with mock.patch.object(
            bench._BootstrapMultiprocessing, "get_context", return_value=context,
        ), mock.patch.object(
            bench, "_runtime_process_deadline_s", return_value=1.0,
        ), mock.patch.object(
            bench.time, "monotonic", return_value=0.0,
        ), mock.patch.object(
            bench, "_retire_runtime_process_group", return_value="natural_exit",
        ), self.assertRaisesRegex(
            bench.ContractError, "runtime child outcome fields are not exact",
        ):
            bench._execute_runtime_contained(args, {}, {})


if __name__ == "__main__":
    unittest.main()
