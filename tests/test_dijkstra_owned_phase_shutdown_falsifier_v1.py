#!/usr/bin/env python3
"""Source-only proof that detached owned work cannot hang runtime process retirement.

The reviewed core still permits a cancellation-resistant operation to outlive
``run_owned_phase``'s logical terminal. The canonical facade now owns that
residual lifetime in a private process group and may force-retire it after the
closed runtime outcome has been transferred to the parent. This proof uses the
same ``spawn`` process-start contract as production, so import, pickle, and
fresh-interpreter startup are inside the tested state machine.
"""

from __future__ import annotations

import argparse
import asyncio
import multiprocessing
import socket
import time
import unittest
from unittest import mock

import bench_joint_advance as bench


PHASE_DEADLINE_S = 0.10
PARENT_OBSERVATION_S = 2.0
PRECONTAINMENT_OBSERVATION_S = 0.05
CONTAINMENT_GRACE_S = 0.50


def _shutdown_falsifier_child(connection: object) -> None:
    # Match the canonical runtime-child ownership boundary: this process is the
    # leader of a private session/process group before any owned async work.
    import os

    os.setsid()
    connection.send(  # type: ignore[attr-defined]
        f"PROCESS_GROUP={os.getpid()}:{os.getpgrp()}"
    )

    async def cancellation_resistant_operation() -> None:
        gate = asyncio.Event()
        cancellation_count = 0
        connection.send("TASK_STARTED")  # type: ignore[attr-defined]
        while True:
            try:
                await gate.wait()
            except asyncio.CancelledError:
                cancellation_count += 1
                connection.send(  # type: ignore[attr-defined]
                    f"TASK_CANCEL_IGNORED_{cancellation_count}"
                )
                continue

    async def scenario() -> None:
        try:
            await bench.run_owned_phase(
                {"stubborn": cancellation_resistant_operation()},
                deadline_s=PHASE_DEADLINE_S,
            )
        except asyncio.TimeoutError:
            current = asyncio.current_task()
            pending_owned = tuple(
                task
                for task in asyncio.all_tasks()
                if task is not current and not task.done()
            )
            connection.send(  # type: ignore[attr-defined]
                f"PENDING_OWNED_TASKS_AT_LOGICAL_TERMINAL={len(pending_owned)}"
            )
            if len(pending_owned) != 1:
                raise AssertionError(
                    "expected exactly one live detached owned task at logical terminal"
                )
            # Canonical runtime-child entry transfers its structured outcome at
            # this point, before asyncio.run begins pending-task shutdown.
            connection.send("OUTCOME_TRANSFERRED")  # type: ignore[attr-defined]
            return
        raise AssertionError("owned phase unexpectedly succeeded")

    asyncio.run(scenario())
    connection.send("NATURAL_PROCESS_TERMINAL")  # type: ignore[attr-defined]


class OwnedPhaseShutdownContainmentTests(unittest.TestCase):
    def test_process_construction_failure_closes_both_pipe_endpoints(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        context.Pipe.return_value = (receiver, sender)
        context.Process.side_effect = RuntimeError("process construction refused")

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaisesRegex(
                RuntimeError, "process construction refused",
            ):
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        context.Pipe.assert_called_once_with(duplex=False)
        context.Process.assert_called_once_with(
            target=bench._runtime_child_entry,
            args=(sender, mock.ANY, mock.ANY, {}),
            name="void-war-college-runtime",
        )
        receiver.close.assert_called_once_with()
        sender.close.assert_called_once_with()

    def test_spawn_failure_closes_both_unstarted_pipe_endpoints(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        process.start.side_effect = OSError("spawn refused")
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaisesRegex(OSError, "spawn refused"):
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        context.Pipe.assert_called_once_with(duplex=False)
        process.start.assert_called_once_with()
        receiver.close.assert_called_once_with()
        sender.close.assert_called_once_with()
        process.terminate.assert_not_called()
        process.kill.assert_not_called()

    def test_parent_sender_handoff_failure_retires_started_child(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        sender.close.side_effect = OSError("sender handoff close refused")
        process.is_alive.side_effect = (True, False)
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaisesRegex(
                OSError, "sender handoff close refused",
            ):
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        process.start.assert_called_once_with()
        sender.close.assert_called_once_with()
        receiver.close.assert_called_once_with()
        self.assertEqual(
            process.join.call_args_list,
            [
                mock.call(0),
                mock.call(bench._RUNTIME_CHILD_SIGNAL_GRACE_S),
            ],
        )
        process.terminate.assert_called_once_with()
        process.kill.assert_not_called()

    def test_sender_handoff_receiver_cleanup_failure_preserves_primary(self) -> None:
        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = OSError("sender handoff close refused")
        receiver_failure = OSError("receiver close refused")
        sender.close.side_effect = primary
        receiver.close.side_effect = receiver_failure
        process.is_alive.return_value = False
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaises(bench.RuntimeChildHandoffError) as raised:
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIsNone(error.retirement_error)
        self.assertEqual(
            error.details,
            {
                "primary": {
                    "status": "error",
                    "error_type": "OSError",
                    "error": "sender handoff close refused",
                },
                "cleanup": {
                    "receiver_close": {
                        "status": "error",
                        "error_type": "OSError",
                        "error": "receiver close refused",
                    },
                    "child_retirement": {"status": "ok"},
                },
            },
        )
        receiver.close.assert_called_once_with()
        process.join.assert_called_once_with(0)

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
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIsNone(error.receiver_close_error)
        self.assertIs(error.retirement_error, retirement_failure)
        self.assertEqual(
            error.details["cleanup"],
            {
                "receiver_close": {"status": "ok"},
                "child_retirement": {
                    "status": "error",
                    "error_type": "ContractError",
                    "error": "child retirement failed",
                },
            },
        )
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
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        error = raised.exception
        self.assertIs(error.primary, primary)
        self.assertIs(error.receiver_close_error, receiver_failure)
        self.assertIs(error.retirement_error, retirement_failure)
        self.assertIn('"error":"sender handoff close refused"', str(error))
        self.assertIn('"error":"receiver close refused"', str(error))
        self.assertIn('"error":"child retirement failed"', str(error))
        receiver.close.assert_called_once_with()
        retire.assert_called_once_with(process)

    def test_sender_handoff_baseexception_primary_is_reraised_after_clean_cleanup(self) -> None:
        class HandoffAbort(BaseException):
            pass

        context = mock.Mock()
        receiver = mock.Mock()
        sender = mock.Mock()
        process = mock.Mock()
        primary = HandoffAbort("sender handoff aborted")
        sender.close.side_effect = primary
        process.is_alive.return_value = False
        context.Pipe.return_value = (receiver, sender)
        context.Process.return_value = process

        with mock.patch.object(
            bench._BootstrapMultiprocessing,
            "get_context",
            return_value=context,
        ):
            with self.assertRaises(HandoffAbort) as raised:
                bench._execute_runtime_contained(
                    argparse.Namespace(),
                    {
                        "concurrency": [1],
                        "tick_batches": [1],
                        "rpc_timeout_s": 0.1,
                        "cell_timeout_s": 0.1,
                        "teardown_timeout_s": 0.1,
                        "ready_timeout_s": 0.1,
                    },
                    {},
                )

        self.assertIs(raised.exception, primary)
        receiver.close.assert_called_once_with()
        process.join.assert_called_once_with(0)
        process.terminate.assert_not_called()
        process.kill.assert_not_called()

    def test_production_spawn_entrypoint_transfers_pre_runtime_host_rejection(self) -> None:
        designated_hostname = f"not-{socket.gethostname()}"
        args = argparse.Namespace(designated_hostname=designated_hostname)
        parameters = {
            "concurrency": [1],
            "tick_batches": [1],
            "rpc_timeout_s": 0.1,
            "cell_timeout_s": 0.1,
            "teardown_timeout_s": 0.1,
            "ready_timeout_s": 0.1,
        }

        outcome = bench._execute_runtime_contained(args, parameters, {})

        self.assertEqual(outcome["cells"], [])
        self.assertEqual(outcome["host"]["designated_hostname"], designated_hostname)
        self.assertEqual(outcome["run"]["terminal"], "startup_error")
        self.assertEqual(outcome["run"]["stage"], "host_attestation")
        self.assertEqual(outcome["run"]["error_type"], "ContractError")
        self.assertEqual(
            outcome["run"]["error"],
            "designated hostname does not match this host",
        )
        self.assertEqual(outcome["run"]["cleanup"], {"failures": []})
        self.assertEqual(
            outcome["run"]["containment"],
            {
                "required_by_cell": False,
                "boundary": "not_required",
                "daemon_retired": False,
            },
        )

    def test_detached_task_shutdown_hang_is_force_retired_by_outer_process_owner(self) -> None:
        context = multiprocessing.get_context("spawn")
        self.assertEqual(context.get_start_method(), "spawn")
        parent, child = context.Pipe(duplex=False)
        process = context.Process(target=_shutdown_falsifier_child, args=(child,))
        process.start()
        child.close()
        try:
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(
                parent.recv(),
                f"PROCESS_GROUP={process.pid}:{process.pid}",
            )
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "TASK_STARTED")

            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_1")
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(
                parent.recv(),
                "PENDING_OWNED_TASKS_AT_LOGICAL_TERMINAL=1",
            )
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "OUTCOME_TRANSFERRED")

            # run_owned_phase's finally issues cancellation #2 after the logical
            # terminal, then asyncio.run shutdown issues cancellation #3.
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_2")
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_3")

            process.join(PRECONTAINMENT_OBSERVATION_S)
            self.assertTrue(
                process.is_alive(),
                "fixture must still demonstrate the raw asyncio.run shutdown hang",
            )

            started = time.monotonic()
            bench._retire_runtime_process_group(
                process,
                process.pid,
                natural_grace_s=0.01,
                signal_grace_s=CONTAINMENT_GRACE_S,
            )
            elapsed = time.monotonic() - started

            self.assertLess(elapsed, 1.1)
            self.assertFalse(process.is_alive())
            self.assertFalse(bench._process_group_exists(process.pid))

            while parent.poll(0.0):
                self.assertNotEqual(
                    parent.recv(),
                    "NATURAL_PROCESS_TERMINAL",
                    "fixture unexpectedly retired naturally instead of by containment",
                )
        finally:
            if process.is_alive():
                process.kill()
                process.join(CONTAINMENT_GRACE_S)
            parent.close()

        self.assertFalse(process.is_alive())


if __name__ == "__main__":
    unittest.main()
