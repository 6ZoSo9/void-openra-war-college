#!/usr/bin/env python3
"""Moe source-only falsifiers for bounded runtime process-group retirement."""

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
            bench._retire_runtime_process_group(
                process,
                process.pid,
                natural_grace_s=0.1,
                signal_grace_s=0.1,
            )

        self.assertEqual(
            signals,
            [bench._BootstrapSignal.SIGTERM, bench._BootstrapSignal.SIGKILL],
        )
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


if __name__ == "__main__":
    unittest.main()
