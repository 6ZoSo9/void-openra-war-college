#!/usr/bin/env python3
"""Real-spawn containment proof retained from historical Dijkstra Draft #24.

This file deliberately starts only disposable Python child processes. It does
not start OpenRA, a game, a model, or the promoted Apollyon service.
"""

from __future__ import annotations

import argparse
import asyncio
import multiprocessing
import os
import socket
import time
import unittest

import bench_joint_advance as bench


PHASE_DEADLINE_S = 0.10
PARENT_OBSERVATION_S = 3.0
PRECONTAINMENT_OBSERVATION_S = 0.05
CONTAINMENT_GRACE_S = 0.50


def _parameters() -> dict[str, object]:
    return {
        "concurrency": [1],
        "tick_batches": [1],
        "rpc_timeout_s": 0.1,
        "cell_timeout_s": 0.1,
        "teardown_timeout_s": 0.1,
        "ready_timeout_s": 0.1,
    }


def _host_rejection_args() -> argparse.Namespace:
    return argparse.Namespace(
        mode="run",
        execute_designated_host=True,
        designated_hostname=f"not-{socket.gethostname()}",
        openra_dir="/tmp/void-openra-not-contacted",
    )


def _shutdown_falsifier_child(connection: object) -> None:
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
            connection.send("OUTCOME_TRANSFERRED")  # type: ignore[attr-defined]
            return
        raise AssertionError("owned phase unexpectedly succeeded")

    asyncio.run(scenario())
    connection.send("NATURAL_PROCESS_TERMINAL")  # type: ignore[attr-defined]


@unittest.skipUnless(os.name == "posix", "POSIX process groups required")
class RuntimeChildSpawnContainmentTests(unittest.TestCase):
    def test_spawned_production_child_entry_transfers_host_rejection(self) -> None:
        """Exercise the actual production child entry in a fresh interpreter."""
        context = multiprocessing.get_context("spawn")
        self.assertEqual(context.get_start_method(), "spawn")
        receiver, sender = context.Pipe(duplex=False)
        args = _host_rejection_args()
        process = context.Process(
            target=bench._runtime_child_entry,
            args=(sender, args, _parameters(), {}),
            name="void-war-college-runtime-test",
        )
        process.start()
        sender.close()

        messages: list[object] = []
        outcome: dict[str, object] | None = None
        deadline = time.monotonic() + PARENT_OBSERVATION_S

        try:
            started_pgid: int | None = None
            while time.monotonic() < deadline:
                if receiver.poll(0.05):
                    try:
                        message = receiver.recv()
                    except EOFError:
                        break
                    messages.append(message)
                    if not isinstance(message, tuple) or not message:
                        self.fail(
                            f"production child emitted invalid message: {message!r}"
                        )
                    kind = message[0]
                    if kind == "STARTED":
                        self.assertEqual(len(message), 3)
                        self.assertEqual(message[1], process.pid)
                        self.assertEqual(message[2], process.pid)
                        started_pgid = message[2]
                    elif kind == "OUTCOME":
                        self.assertEqual(len(message), 2)
                        self.assertIsInstance(message[1], dict)
                        outcome = message[1]
                        break
                    elif kind == "ERROR":
                        self.fail(f"production child error terminal: {message!r}")
                    else:
                        self.fail(
                            f"production child unsupported message: {message!r}"
                        )
                elif not process.is_alive():
                    break

            process.join(0.25)
            if process.is_alive():
                bench._retire_runtime_process_group(
                    process,
                    process.pid,
                    natural_grace_s=0.01,
                    signal_grace_s=CONTAINMENT_GRACE_S,
                )

            if outcome is None:
                outcome = next(
                    (
                        item
                        for item in messages
                        if isinstance(item, dict)
                        and isinstance(item.get("run"), dict)
                        and "cells" in item
                    ),
                    None,
                )
            self.assertIsNotNone(
                outcome,
                f"production child emitted no structured outcome: {messages!r}",
            )
            assert outcome is not None

            run = outcome["run"]
            self.assertIsInstance(run, dict)
            assert isinstance(run, dict)
            self.assertEqual(outcome["cells"], [])
            self.assertEqual(run["terminal"], "startup_error")
            self.assertEqual(run["stage"], "host_attestation")
            self.assertEqual(run["error_type"], "ContractError")
            self.assertIn("designated hostname", str(run["error"]))
            self.assertFalse(process.is_alive())
        finally:
            if process.is_alive():
                process.kill()
                process.join(CONTAINMENT_GRACE_S)
            receiver.close()

    def test_detached_task_shutdown_hang_is_force_retired_by_outer_process_owner(
        self,
    ) -> None:
        """Preserve #24's real spawn/process-group containment falsifier."""
        context = multiprocessing.get_context("spawn")
        self.assertEqual(context.get_start_method(), "spawn")
        parent, child = context.Pipe(duplex=False)
        process = context.Process(
            target=_shutdown_falsifier_child,
            args=(child,),
        )
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

            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_2")
            self.assertTrue(parent.poll(PARENT_OBSERVATION_S))
            self.assertEqual(parent.recv(), "TASK_CANCEL_IGNORED_3")

            process.join(PRECONTAINMENT_OBSERVATION_S)
            self.assertTrue(
                process.is_alive(),
                "fixture must demonstrate the raw asyncio.run shutdown hang",
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
                try:
                    terminal_message = parent.recv()
                except EOFError:
                    break
                self.assertNotEqual(
                    terminal_message,
                    "NATURAL_PROCESS_TERMINAL",
                    "fixture retired naturally instead of by containment",
                )
        finally:
            if process.is_alive():
                process.kill()
                process.join(CONTAINMENT_GRACE_S)
            parent.close()

        self.assertFalse(process.is_alive())


if __name__ == "__main__":
    unittest.main()
