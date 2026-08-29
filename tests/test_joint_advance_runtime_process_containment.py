#!/usr/bin/env python3
"""Source-only proofs for finite JointAdvance runtime process containment."""

import asyncio
import multiprocessing
import os
import time
import unittest
from unittest import mock

import bench_joint_advance as bench


def _shutdown_resistant_child(sender):
    os.setsid()
    sender.send(("STARTED", os.getpid(), os.getpgrp()))

    async def fail():
        raise RuntimeError("fixture failure")

    async def resist_cancellation():
        gate = asyncio.Event()
        while True:
            try:
                await gate.wait()
            except asyncio.CancelledError:
                continue

    async def scenario():
        try:
            await bench.run_owned_phase(
                {
                    "fail": fail(),
                    "resistant": resist_cancellation(),
                },
                deadline_s=0.03,
            )
        except bench.ContractError:
            sender.send(("OUTCOME", "LOGICAL_TERMINAL"))
        else:
            sender.send(("OUTCOME", "UNEXPECTED_SUCCESS"))

    asyncio.run(scenario())
    sender.send(("PROCESS_TERMINAL",))
    sender.close()


class RuntimeProcessContainmentTests(unittest.TestCase):
    def test_outer_deadline_is_finite_and_covers_all_planned_cells(self):
        parameters = {
            "concurrency": [1, 2],
            "tick_batches": [1, 8],
            "rpc_timeout_s": 4,
            "cell_timeout_s": 5,
            "teardown_timeout_s": 2,
            "ready_timeout_s": 3,
        }
        self.assertEqual(bench._runtime_process_deadline_s(parameters), 91.0)

    def test_main_runtime_dispatch_uses_process_containment_for_reviewed_core(self):
        args = object()
        parameters = {"sentinel": "parameters"}
        provenance = {"sentinel": "provenance"}
        expected = {"sentinel": "outcome"}
        with mock.patch.object(
            bench, "_execute_runtime_contained", return_value=expected,
        ) as contained:
            actual = bench._run_runtime_from_main(args, parameters, provenance)
        self.assertEqual(actual, expected)
        contained.assert_called_once_with(args, parameters, provenance)

    def test_process_owner_retires_asyncio_shutdown_hang(self):
        context = multiprocessing.get_context("fork")
        receiver, sender = context.Pipe(duplex=False)
        process = context.Process(
            target=_shutdown_resistant_child,
            args=(sender,),
            name="void-war-college-containment-fixture",
        )
        process.start()
        sender.close()

        pgid = None
        try:
            self.assertTrue(receiver.poll(1.0))
            started = receiver.recv()
            self.assertEqual(started, ("STARTED", process.pid, process.pid))
            pgid = process.pid

            self.assertTrue(receiver.poll(1.0))
            outcome = receiver.recv()
            self.assertEqual(outcome, ("OUTCOME", "LOGICAL_TERMINAL"))

            process.join(0.05)
            self.assertTrue(
                process.is_alive(),
                "fixture must still be hung in asyncio.run shutdown before containment",
            )

            bounded_started = time.monotonic()
            bench._retire_runtime_process_group(
                process,
                pgid,
                natural_grace_s=0.01,
                signal_grace_s=0.5,
            )
            self.assertLess(time.monotonic() - bounded_started, 1.1)
            self.assertFalse(process.is_alive())
            self.assertFalse(bench._process_group_exists(pgid))

            drained = []
            while receiver.poll(0.0):
                drained.append(receiver.recv())
            self.assertNotIn(("PROCESS_TERMINAL",), drained)
        finally:
            receiver.close()
            if process.is_alive():
                process.kill()
                process.join(1.0)


if __name__ == "__main__":
    unittest.main()
