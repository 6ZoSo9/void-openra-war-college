#!/usr/bin/env python3
"""Source-only falsifier for detached owned-phase event-loop shutdown.

This test deliberately proves the current HOLD rather than claiming closure. A
cancellation-resistant operation can outlive ``run_owned_phase``'s logical
terminal while remaining an owned live task, then keep ``asyncio.run`` in its
pending-task shutdown gather forever. The parent process owns the destructive
containment boundary so the test itself always retires the child without
contacting the OpenRA runtime.
"""

from __future__ import annotations

import asyncio
import multiprocessing
import unittest

from bench_joint_advance_core import run_owned_phase


PHASE_DEADLINE_S = 0.10
PARENT_OBSERVATION_S = 2.0
CHILD_RETIREMENT_S = 1.0


def _shutdown_falsifier_child(connection: object) -> None:
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
                # Model an RPC awaitable that does not retire merely because
                # its owning phase, finalizer, or asyncio.run shutdown cancelled it.
                continue

    async def scenario() -> None:
        try:
            await run_owned_phase(
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
            # The falsifier is only meaningful if run_owned_phase has already
            # returned authority to its caller while the stubborn operation is
            # still live and owned by this event loop.
            if len(pending_owned) != 1:
                raise AssertionError(
                    "expected exactly one live detached owned task at logical terminal"
                )
            connection.send("LOGICAL_TERMINAL")  # type: ignore[attr-defined]
            return
        raise AssertionError("owned phase unexpectedly succeeded")

    asyncio.run(scenario())
    # Reaching this line would mean top-level loop shutdown retired the detached
    # task and the current Dijkstra HOLD no longer reproduces.
    connection.send("PROCESS_TERMINAL")  # type: ignore[attr-defined]


class OwnedPhaseShutdownFalsifierTests(unittest.TestCase):
    def test_detached_cancellation_resistant_task_rehangs_asyncio_run_shutdown(self) -> None:
        context = multiprocessing.get_context("fork")
        parent, child = context.Pipe(duplex=False)
        process = context.Process(target=_shutdown_falsifier_child, args=(child,))
        process.start()
        child.close()
        try:
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S), "child never started owned operation")
            self.assertEqual(parent.recv(), "TASK_STARTED")

            # The phase deadline issues cancellation #1. The operation
            # deliberately survives it, so run_owned_phase must detach it and
            # reach its logical timeout terminal.
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S), "phase cancellation was never observed")
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_1")
            self.assertTrue(
                parent.poll(PARENT_OBSERVATION_S),
                "live-task ownership at logical terminal was never observed",
            )
            self.assertEqual(
                parent.recv(),
                "PENDING_OWNED_TASKS_AT_LOGICAL_TERMINAL=1",
            )
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S), "owned phase never reached logical terminal")
            self.assertEqual(parent.recv(), "LOGICAL_TERMINAL")

            # run_owned_phase's finally block issues cancellation #2 to the same
            # still-unfinished task after the timeout path has already detached it.
            self.assertTrue(
                parent.poll(PARENT_OBSERVATION_S),
                "run_owned_phase finalizer cancellation was never observed",
            )
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_2")

            # Only after scenario() returns does asyncio.run enter loop shutdown
            # and issue cancellation #3 to pending tasks.
            self.assertTrue(
                parent.poll(PARENT_OBSERVATION_S),
                "asyncio.run shutdown cancellation was never observed",
            )
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_3")

            # The logical phase terminal has already been published and the real
            # shutdown cancellation has fired. The process must still remain
            # alive because asyncio.run is waiting for the detached task to retire.
            process.join(CHILD_RETIREMENT_S)
            self.assertTrue(
                process.is_alive(),
                "falsifier no longer reproduces: top-level loop shutdown retired boundedly",
            )

            # Drain by message identity. A queued cancellation diagnostic is not
            # process termination evidence.
            while parent.poll(0.0):
                message = parent.recv()
                self.assertNotEqual(
                    message,
                    "PROCESS_TERMINAL",
                    "process terminal was published despite live child",
                )
                self.assertTrue(
                    str(message).startswith("TASK_CANCEL_IGNORED_"),
                    f"unexpected child message while process remains live: {message}",
                )
        finally:
            if process.is_alive():
                process.terminate()
                process.join(CHILD_RETIREMENT_S)
            if process.is_alive():
                process.kill()
                process.join(CHILD_RETIREMENT_S)
            parent.close()
        self.assertFalse(process.is_alive(), "parent containment failed to retire falsifier child")


if __name__ == "__main__":
    unittest.main()
