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


if __name__ == "__main__":
    unittest.main()
