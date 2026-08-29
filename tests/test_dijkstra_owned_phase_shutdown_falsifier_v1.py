#!/usr/bin/env python3
"""Source-only falsifier for detached owned-phase event-loop shutdown.

This test deliberately proves the current HOLD rather than claiming closure.  A
cancellation-resistant operation can outlive ``run_owned_phase``'s logical
terminal, then keep ``asyncio.run`` in its pending-task shutdown gather forever.
The parent process owns the destructive containment boundary so the test itself
always retires the child without contacting the OpenRA runtime.
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
        connection.send("TASK_STARTED")  # type: ignore[attr-defined]
        while True:
            try:
                await gate.wait()
            except asyncio.CancelledError:
                # Model an RPC awaitable that does not retire merely because
                # its owning phase cancelled it.
                continue

    async def scenario() -> None:
        try:
            await run_owned_phase(
                {"stubborn": cancellation_resistant_operation()},
                deadline_s=PHASE_DEADLINE_S,
            )
        except asyncio.TimeoutError:
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
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S), "owned phase never reached logical terminal")
            self.assertEqual(parent.recv(), "LOGICAL_TERMINAL")

            # The logical phase terminal has already been published.  The
            # process must nevertheless remain alive because asyncio.run is
            # waiting for the detached task to honor cancellation.
            process.join(CHILD_RETIREMENT_S)
            self.assertTrue(
                process.is_alive(),
                "falsifier no longer reproduces: top-level loop shutdown retired boundedly",
            )
            self.assertFalse(parent.poll(0.0), "process terminal was published despite live child")
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
