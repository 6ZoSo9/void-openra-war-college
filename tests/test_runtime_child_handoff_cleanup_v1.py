#!/usr/bin/env python3
"""Fail-closed tests for runtime-child construction/start/sender handoff cleanup."""

from __future__ import annotations

import argparse
import unittest
from unittest import mock

import bench_joint_advance as bench


def _authorized_args() -> argparse.Namespace:
    return argparse.Namespace(
        mode="run",
        execute_designated_host=True,
        designated_hostname="precision-test",
        openra_dir="/tmp/void-openra-not-contacted",
    )


def _parameters() -> dict[str, object]:
    return {
        "concurrency": [1],
        "tick_batches": [1],
        "rpc_timeout_s": 0.1,
        "cell_timeout_s": 0.1,
        "teardown_timeout_s": 0.1,
        "ready_timeout_s": 0.1,
    }


class RuntimeChildHandoffCleanupTests(unittest.TestCase):
    def _invoke(self) -> dict[str, object]:
        return bench._execute_runtime_contained(
            _authorized_args(),
            _parameters(),
            {},
        )

    def test_process_construction_failure_closes_both_pipe_endpoints(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        context.Pipe.return_value = (receiver, sender)
        context.Process.side_effect = RuntimeError("process construction refused")

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(bench, "_retire_unbound_runtime_child") as retire,
        ):
            with self.assertRaisesRegex(
                RuntimeError, "process construction refused"
            ):
                self._invoke()

        context.Pipe.assert_called_once_with(duplex=False)
        receiver.close.assert_called_once_with()
        sender.close.assert_called_once_with()
        retire.assert_not_called()

    def test_spawn_failure_closes_both_unstarted_pipe_endpoints(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        process.start.side_effect = OSError("spawn refused")
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(bench, "_retire_unbound_runtime_child") as retire,
        ):
            with self.assertRaisesRegex(OSError, "spawn refused"):
                self._invoke()

        process.start.assert_called_once_with()
        receiver.close.assert_called_once_with()
        sender.close.assert_called_once_with()
        retire.assert_not_called()
        process.terminate.assert_not_called()
        process.kill.assert_not_called()

    def test_parent_sender_handoff_failure_retires_started_child(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = OSError("sender handoff close refused")
        sender.close.side_effect = primary
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench, "_retire_unbound_runtime_child", return_value=None
            ) as retire,
        ):
            with self.assertRaises(OSError) as raised:
                self._invoke()

        self.assertIs(raised.exception, primary)
        process.start.assert_called_once_with()
        receiver.close.assert_called_once_with()
        retire.assert_called_once_with(process)

    def test_sender_handoff_receiver_cleanup_failure_preserves_primary(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = OSError("sender handoff close refused")
        receiver_failure = OSError("receiver close refused")
        sender.close.side_effect = primary
        receiver.close.side_effect = receiver_failure
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench, "_retire_unbound_runtime_child", return_value=None
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildHandoffError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIsNone(error.retirement_error)
        self.assertIs(error.__cause__, primary)
        self.assertEqual(
            error.details["cleanup"],
            {
                "receiver_close": {
                    "status": "error",
                    "error_type": "OSError",
                    "error": "receiver close refused",
                },
                "child_retirement": {"status": "ok"},
            },
        )
        retire.assert_called_once_with(process)

    def test_sender_handoff_retirement_failure_preserves_primary(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = OSError("sender handoff close refused")
        retirement_failure = bench.ContractError("child retirement failed")
        sender.close.side_effect = primary
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench,
                "_retire_unbound_runtime_child",
                side_effect=retirement_failure,
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildHandoffError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIsNone(error.receiver_close_error)
        self.assertIs(error.retirement_error, retirement_failure)
        self.assertIs(error.__cause__, primary)
        receiver.close.assert_called_once_with()
        retire.assert_called_once_with(process)

    def test_sender_handoff_dual_cleanup_failure_preserves_all_causes(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = OSError("sender handoff close refused")
        receiver_failure = OSError("receiver close refused")
        retirement_failure = bench.ContractError("child retirement failed")
        sender.close.side_effect = primary
        receiver.close.side_effect = receiver_failure
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench,
                "_retire_unbound_runtime_child",
                side_effect=retirement_failure,
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildHandoffError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIs(error.retirement_error, retirement_failure)
        self.assertIn('"error":"sender handoff close refused"', str(error))
        self.assertIn('"error":"receiver close refused"', str(error))
        self.assertIn('"error":"child retirement failed"', str(error))
        retire.assert_called_once_with(process)

    def test_sender_handoff_baseexception_primary_is_reraised_after_clean_cleanup(
        self,
    ) -> None:
        class HandoffAbort(BaseException):
            pass

        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = HandoffAbort("sender handoff aborted")
        sender.close.side_effect = primary
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench, "_retire_unbound_runtime_child", return_value=None
            ) as retire,
        ):
            with self.assertRaises(HandoffAbort) as raised:
                self._invoke()

        self.assertIs(raised.exception, primary)
        receiver.close.assert_called_once_with()
        retire.assert_called_once_with(process)


    def test_process_construction_receiver_close_failure_still_closes_sender(
        self,
    ) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        primary = RuntimeError("process construction refused")
        receiver_failure = OSError("receiver close refused")
        context.Pipe.return_value = (receiver, sender)
        context.Process.side_effect = primary
        receiver.close.side_effect = receiver_failure

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaises(bench.RuntimeChildStartCleanupError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIsNone(error.sender_close_error)
        self.assertIs(error.__cause__, primary)
        receiver.close.assert_called_once_with()
        sender.close.assert_called_once_with()

    def test_spawn_failure_dual_endpoint_cleanup_preserves_all_causes(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = OSError("spawn refused")
        receiver_failure = OSError("receiver close refused")
        sender_failure = OSError("sender close refused")
        process.start.side_effect = primary
        receiver.close.side_effect = receiver_failure
        sender.close.side_effect = sender_failure
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaises(bench.RuntimeChildStartCleanupError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIs(error.sender_close_error, sender_failure)
        self.assertIs(error.__cause__, primary)
        self.assertIn('"error":"spawn refused"', str(error))
        self.assertIn('"error":"receiver close refused"', str(error))
        self.assertIn('"error":"sender close refused"', str(error))
        receiver.close.assert_called_once_with()
        sender.close.assert_called_once_with()

    def test_unbound_parent_receiver_close_failure_still_retires_child(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        receiver.poll.return_value = False
        process.is_alive.return_value = False
        receiver_failure = OSError("receiver close refused")
        receiver.close.side_effect = receiver_failure
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench,
                "_retire_unbound_runtime_child",
                return_value=None,
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildParentCleanupError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIsNone(error.primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIsNone(error.retirement_error)
        retire.assert_called_once_with(process)

    def test_bound_parent_receiver_close_failure_still_retires_group(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        process.pid = 4242
        receiver.poll.side_effect = (True, True)
        receiver.recv.side_effect = (
            ("STARTED", 4242, 4242),
            ("OUTCOME", {"cells": [], "run": {}, "host": {}}),
        )
        receiver_failure = OSError("receiver close refused")
        receiver.close.side_effect = receiver_failure
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench,
                "_runtime_process_deadline_s",
                return_value=0.1,
            ),
            mock.patch.object(
                bench,
                "_retire_runtime_process_group",
                return_value="natural_exit",
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildParentCleanupError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIsNone(error.primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIsNone(error.retirement_error)
        retire.assert_called_once_with(process, 4242)

    def test_bound_parent_dual_cleanup_failure_preserves_both(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        process.pid = 4242
        receiver.poll.side_effect = (True, True)
        receiver.recv.side_effect = (
            ("STARTED", 4242, 4242),
            ("OUTCOME", {"cells": [], "run": {}, "host": {}}),
        )
        receiver_failure = OSError("receiver close refused")
        retirement_failure = bench.ContractError("process group retirement failed")
        receiver.close.side_effect = receiver_failure
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench,
                "_runtime_process_deadline_s",
                return_value=0.1,
            ),
            mock.patch.object(
                bench,
                "_retire_runtime_process_group",
                side_effect=retirement_failure,
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildParentCleanupError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIsNone(error.primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIs(error.retirement_error, retirement_failure)
        self.assertIn('"error":"receiver close refused"', str(error))
        self.assertIn('"error":"process group retirement failed"', str(error))
        retire.assert_called_once_with(process, 4242)

    def test_parent_loop_primary_is_preserved_when_retirement_also_fails(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = RuntimeError("receiver poll refused")
        retirement_failure = bench.ContractError("child retirement failed")
        receiver.poll.side_effect = primary
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with (
            mock.patch.object(
                bench._BootstrapMultiprocessing,
                "get_context",
                return_value=context,
            ),
            mock.patch.object(
                bench,
                "_retire_unbound_runtime_child",
                side_effect=retirement_failure,
            ) as retire,
        ):
            with self.assertRaises(bench.RuntimeChildParentCleanupError) as raised:
                self._invoke()

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIsNone(error.receiver_close_error)
        self.assertIs(error.retirement_error, retirement_failure)
        self.assertIs(error.__cause__, primary)
        retire.assert_called_once_with(process)



    def test_unbound_terminate_failure_still_attempts_kill(self) -> None:
        process = mock.Mock()
        process.is_alive.side_effect = (True, False)
        terminate_failure = OSError("terminate refused")
        process.terminate.side_effect = terminate_failure

        with self.assertRaises(
            bench.RuntimeChildUnboundRetirementError
        ) as raised:
            bench._retire_unbound_runtime_child(
                process,
                signal_grace_s=0.1,
            )

        error = raised.exception
        self.assertIs(error.terminate_error, terminate_failure)
        self.assertIsNone(error.kill_error)
        self.assertFalse(error.child_alive)
        self.assertIs(error.__cause__, terminate_failure)
        process.join.assert_any_call(0)
        process.terminate.assert_called_once_with()
        process.kill.assert_called_once_with()
        self.assertEqual(process.join.call_count, 2)

    def test_unbound_terminate_and_kill_failure_preserve_both(self) -> None:
        process = mock.Mock()
        process.is_alive.side_effect = (True, True)
        terminate_failure = OSError("terminate refused")
        kill_failure = OSError("kill refused")
        process.terminate.side_effect = terminate_failure
        process.kill.side_effect = kill_failure

        with self.assertRaises(
            bench.RuntimeChildUnboundRetirementError
        ) as raised:
            bench._retire_unbound_runtime_child(
                process,
                signal_grace_s=0.1,
            )

        error = raised.exception
        self.assertIs(error.terminate_error, terminate_failure)
        self.assertIs(error.kill_error, kill_failure)
        self.assertTrue(error.child_alive)
        self.assertIs(error.__cause__, terminate_failure)
        self.assertIn('"error":"terminate refused"', str(error))
        self.assertIn('"error":"kill refused"', str(error))
        process.terminate.assert_called_once_with()
        process.kill.assert_called_once_with()

    def test_unbound_kill_failure_after_successful_term_preserves_failure(
        self,
    ) -> None:
        process = mock.Mock()
        process.is_alive.side_effect = (True, True, True)
        kill_failure = OSError("kill refused")
        process.kill.side_effect = kill_failure

        with mock.patch.object(
            bench.time,
            "monotonic",
            side_effect=(0.0, 0.0),
        ):
            with self.assertRaises(
                bench.RuntimeChildUnboundRetirementError
            ) as raised:
                bench._retire_unbound_runtime_child(
                    process,
                    signal_grace_s=0.1,
                )

        error = raised.exception
        self.assertIsNone(error.terminate_error)
        self.assertIs(error.kill_error, kill_failure)
        self.assertTrue(error.child_alive)
        self.assertIs(error.__cause__, kill_failure)
        process.terminate.assert_called_once_with()
        process.kill.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
