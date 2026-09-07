#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
import tempfile
import unittest
from pathlib import Path

from scripts.controller_attempt_admission_store_v1 import (
    AdmissionHold,
    AttemptIdentity,
    advance_session,
    consume_joint_evidence,
    create_attempt,
    inspect_attempt,
)

WAR_COLLEGE_COMMIT = "f57c561f3a4c742e34d820933be40dd7d4253951"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
JOINT_A = "a" * 64
JOINT_B = "b" * 64


def identity(attempt_id: str = "attempt-001") -> AttemptIdentity:
    return AttemptIdentity(
        attempt_id=attempt_id,
        producer_id="designated-host-1",
        controller_a_id="controller-a",
        controller_b_id="controller-b",
        source_generation="ad1926569b12466c",
        war_college_commit=WAR_COLLEGE_COMMIT,
        engine_commit=ENGINE_COMMIT,
    )


class ControllerAttemptAdmissionStoreTests(unittest.TestCase):
    def test_create_attempt_is_durable_and_create_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            receipt = create_attempt(path, identity())
            self.assertEqual(receipt["contract"], "GREEN")
            self.assertEqual(receipt["session_generation"], 1)

            reopened = inspect_attempt(path, identity())
            self.assertEqual(reopened["session_generation"], 1)

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_ATTEMPT_ALREADY_EXISTS",
            ):
                create_attempt(path, identity())

    def test_reconnect_advances_monotonically_and_stales_predecessor(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity())

            successor = advance_session(
                path,
                identity(),
                expected_current_generation=1,
            )
            self.assertEqual(successor["session_generation"], 2)

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_SESSION_NOT_CURRENT",
            ):
                consume_joint_evidence(
                    path,
                    identity(),
                    session_generation=1,
                    joint_evidence_sha256=JOINT_A,
                )

            current = consume_joint_evidence(
                path,
                identity(),
                session_generation=2,
                joint_evidence_sha256=JOINT_A,
            )
            self.assertEqual(current["contract"], "GREEN")

    def test_competing_successors_only_one_can_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity())

            def contender() -> str:
                try:
                    result = advance_session(
                        path,
                        identity(),
                        expected_current_generation=1,
                    )
                    return f"GREEN:{result['session_generation']}"
                except AdmissionHold as error:
                    return str(error)

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(lambda _value: contender(), range(2)))

            self.assertEqual(results.count("GREEN:2"), 1)
            self.assertEqual(
                sum(
                    value in {
                        "HOLD_SESSION_PREDECESSOR_NOT_CURRENT",
                        "HOLD_COMPETING_SESSION_SUCCESSOR",
                    }
                    for value in results
                ),
                1,
            )
            self.assertEqual(
                inspect_attempt(path, identity())["session_generation"],
                2,
            )

    def test_joint_evidence_consumption_is_exactly_once_across_restart(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity())

            first = consume_joint_evidence(
                path,
                identity(),
                session_generation=1,
                joint_evidence_sha256=JOINT_A,
            )
            self.assertEqual(first["contract"], "GREEN")

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_EVIDENCE_ALREADY_CONSUMED",
            ):
                consume_joint_evidence(
                    path,
                    identity(),
                    session_generation=1,
                    joint_evidence_sha256=JOINT_A,
                )

    def test_joint_digest_cannot_be_reused_under_other_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity("attempt-001"))
            create_attempt(path, identity("attempt-002"))

            consume_joint_evidence(
                path,
                identity("attempt-001"),
                session_generation=1,
                joint_evidence_sha256=JOINT_A,
            )

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_JOINT_DIGEST_ALREADY_CONSUMED",
            ):
                consume_joint_evidence(
                    path,
                    identity("attempt-002"),
                    session_generation=1,
                    joint_evidence_sha256=JOINT_A,
                )

    def test_identity_binding_cannot_change_on_reconnect_or_consume(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            original = identity()
            create_attempt(path, original)

            wrong = AttemptIdentity(
                attempt_id=original.attempt_id,
                producer_id="other-producer",
                controller_a_id=original.controller_a_id,
                controller_b_id=original.controller_b_id,
                source_generation=original.source_generation,
                war_college_commit=original.war_college_commit,
                engine_commit=original.engine_commit,
            )

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_ATTEMPT_IDENTITY_MISMATCH",
            ):
                advance_session(
                    path,
                    wrong,
                    expected_current_generation=1,
                )

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_ATTEMPT_IDENTITY_MISMATCH",
            ):
                consume_joint_evidence(
                    path,
                    wrong,
                    session_generation=1,
                    joint_evidence_sha256=JOINT_A,
                )

    def test_stale_predecessor_cannot_reappear_after_multiple_successors(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity())
            advance_session(path, identity(), expected_current_generation=1)
            advance_session(path, identity(), expected_current_generation=2)

            self.assertEqual(
                inspect_attempt(path, identity())["session_generation"],
                3,
            )

            for stale in (1, 2):
                with self.subTest(stale=stale):
                    with self.assertRaisesRegex(
                        AdmissionHold,
                        "HOLD_SESSION_NOT_CURRENT",
                    ):
                        consume_joint_evidence(
                            path,
                            identity(),
                            session_generation=stale,
                            joint_evidence_sha256=JOINT_B,
                        )

    def test_restart_with_reused_predecessor_generation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity())
            advance_session(path, identity(), expected_current_generation=1)

            with self.assertRaisesRegex(
                AdmissionHold,
                "HOLD_SESSION_PREDECESSOR_NOT_CURRENT",
            ):
                advance_session(
                    path,
                    identity(),
                    expected_current_generation=1,
                )

    def test_valid_fresh_successor_can_consume_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "ledger.sqlite3"
            create_attempt(path, identity())
            next_session = advance_session(
                path,
                identity(),
                expected_current_generation=1,
            )
            self.assertEqual(next_session["session_generation"], 2)

            receipt = consume_joint_evidence(
                path,
                identity(),
                session_generation=2,
                joint_evidence_sha256=JOINT_B,
            )
            self.assertEqual(receipt["contract"], "GREEN")
            self.assertEqual(receipt["session_generation"], 2)
            self.assertEqual(receipt["joint_evidence_sha256"], JOINT_B)


if __name__ == "__main__":
    unittest.main()
