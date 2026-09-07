#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from scripts import controller_attempt_admission_store_v1 as store
from scripts import verify_controller_evidence_producer_auth_v1 as producer_auth
from scripts import verify_controller_evidence_with_durable_currentness_v1 as integration
from tests.test_verify_controller_evidence_isolation_v1 import make_evidence


def public_pem(private_key: Ed25519PrivateKey) -> str:
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


class DurableCurrentnessIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_data_dir = os.environ.get("VOID_DATA_DIR")
        self._temp = tempfile.TemporaryDirectory()
        os.environ["VOID_DATA_DIR"] = self._temp.name
        self.store_path = integration.canonical_store_path()
        self.key = Ed25519PrivateKey.generate()

    def tearDown(self) -> None:
        if self._old_data_dir is None:
            os.environ.pop("VOID_DATA_DIR", None)
        else:
            os.environ["VOID_DATA_DIR"] = self._old_data_dir
        self._temp.cleanup()

    def identity(
        self,
        *,
        attempt_id: str = "attempt-001",
        source_generation: str = "ad1926569b12466c",
        war_college_commit: str = integration.STORE_WAR_COLLEGE_SOURCE_BASE,
        swapped_mapping: bool = False,
    ) -> store.AttemptIdentity:
        pem = public_pem(self.key)
        derived = producer_auth.derive_void_node_identity_from_public_pem(pem)
        assert derived is not None
        node_id, full_sha, _ = derived
        if swapped_mapping:
            a_player, b_player = "player-2", "player-1"
        else:
            a_player, b_player = "player-1", "player-2"
        return store.AttemptIdentity(
            attempt_id=attempt_id,
            producer_id=node_id,
            producer_public_key_sha256=full_sha,
            controller_a_id="controller-a",
            controller_a_player_id=a_player,
            controller_b_id="controller-b",
            controller_b_player_id=b_player,
            source_generation=source_generation,
            war_college_commit=war_college_commit,
            engine_commit=integration.structural.ENGINE_FROZEN_COMMIT,
        )

    def create_attempt(
        self,
        attempt_identity: store.AttemptIdentity | None = None,
    ) -> store.AttemptIdentity:
        value = attempt_identity or self.identity()
        store.create_attempt(self.store_path, value)
        return value

    def auth_for(
        self,
        evidence: dict[str, object],
        identity: store.AttemptIdentity,
        *,
        session_generation: int | None = None,
        signing_key: Ed25519PrivateKey | None = None,
    ) -> dict[str, object]:
        generation = (
            int(evidence["controller_session_generation"])
            if session_generation is None
            else session_generation
        )
        joint = str(evidence["joint_evidence_sha256"])
        transcript = producer_auth.producer_auth_transcript_bytes(
            identity,
            session_generation=generation,
            joint_evidence_sha256=joint,
            evidence_generation=integration.structural.GENERATION,
            war_college_frozen_commit=integration.structural.WAR_COLLEGE_FROZEN_COMMIT,
            engine_frozen_commit=integration.structural.ENGINE_FROZEN_COMMIT,
        )
        key = signing_key or self.key
        return {
            "attempt_id": identity.attempt_id,
            "joint_evidence_sha256": joint,
            "marker": producer_auth.MARKER,
            "producer_node_id": identity.producer_id,
            "producer_public_key_pem": public_pem(self.key),
            "producer_public_key_sha256": identity.producer_public_key_sha256,
            "schema_version": producer_auth.SCHEMA_VERSION,
            "session_generation": generation,
            "signature_hex": key.sign(transcript).hex(),
            "transcript_sha256": hashlib.sha256(transcript).hexdigest(),
        }

    def assert_hold(self, report: dict[str, object], code: str) -> None:
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_green_requires_store_currentness_and_valid_node_signature(self) -> None:
        identity = self.create_attempt()
        evidence = make_evidence()
        report = integration.verify_and_consume_evidence(
            evidence,
            self.auth_for(evidence, identity),
        )
        self.assertEqual(report["contract"], "GREEN")
        self.assertTrue(report["producer_signature_authentication_green"])
        self.assertEqual(report["session_generation"], 1)

    def test_identical_full_bundle_replay_is_rejected(self) -> None:
        identity = self.create_attempt()
        evidence = make_evidence()
        auth = self.auth_for(evidence, identity)
        self.assertEqual(
            integration.verify_and_consume_evidence(evidence, auth)["contract"],
            "GREEN",
        )
        replay = integration.verify_and_consume_evidence(evidence, auth)
        self.assert_hold(replay, "HOLD_EVIDENCE_ALREADY_CONSUMED")

    def test_structural_green_without_authentication_does_not_consume(self) -> None:
        identity = self.create_attempt()
        evidence = make_evidence()
        report = integration.verify_and_consume_evidence(evidence, {})
        self.assertEqual(report["phase"], "producer_authentication")
        self.assertEqual(report["contract"], "HOLD")

        clean = integration.verify_and_consume_evidence(
            evidence,
            self.auth_for(evidence, identity),
        )
        self.assertEqual(clean["contract"], "GREEN")

    def test_wrong_signing_key_does_not_consume(self) -> None:
        identity = self.create_attempt()
        evidence = make_evidence()
        wrong_key = Ed25519PrivateKey.generate()
        bad = self.auth_for(evidence, identity, signing_key=wrong_key)
        report = integration.verify_and_consume_evidence(evidence, bad)
        self.assert_hold(
            report,
            "HOLD_PRODUCER_AUTH_SIGNATURE_VERIFICATION_FAILED",
        )

        good = integration.verify_and_consume_evidence(
            evidence,
            self.auth_for(evidence, identity),
        )
        self.assertEqual(good["contract"], "GREEN")

    def test_stale_predecessor_after_reconnect_is_rejected(self) -> None:
        identity = self.create_attempt()
        store.advance_session(
            self.store_path,
            identity,
            expected_current_generation=1,
        )
        stale_evidence = make_evidence(controller_session_generation=1)
        stale = integration.verify_and_consume_evidence(
            stale_evidence,
            self.auth_for(stale_evidence, identity),
        )
        self.assert_hold(
            stale,
            "HOLD_EXPECTED_CONTROLLER_SESSION_GENERATION_MISMATCH",
        )

        fresh_evidence = make_evidence(controller_session_generation=2)
        fresh = integration.verify_and_consume_evidence(
            fresh_evidence,
            self.auth_for(fresh_evidence, identity),
        )
        self.assertEqual(fresh["contract"], "GREEN")

    def test_controller_player_mapping_is_store_authoritative(self) -> None:
        identity = self.create_attempt(self.identity(swapped_mapping=True))
        evidence = make_evidence()
        report = integration.verify_and_consume_evidence(
            evidence,
            self.auth_for(evidence, identity),
        )
        self.assert_hold(
            report,
            "HOLD_DURABLE_CONTROLLER_PLAYER_MAPPING_MISMATCH",
        )

    def test_structural_hold_does_not_consume_evidence(self) -> None:
        identity = self.create_attempt()
        invalid = make_evidence()
        invalid["controllers"][0]["action_payload"]["commands"][0]["actor_id"] = 201
        first = integration.verify_and_consume_evidence(
            invalid,
            self.auth_for(invalid, identity),
        )
        self.assertEqual(first["contract"], "HOLD")
        self.assertEqual(first["phase"], "structural_verification")

        clean_evidence = make_evidence()
        clean = integration.verify_and_consume_evidence(
            clean_evidence,
            self.auth_for(clean_evidence, identity),
        )
        self.assertEqual(clean["contract"], "GREEN")

    def test_store_source_generation_mismatch_fails_closed(self) -> None:
        identity = self.create_attempt(self.identity(source_generation="other-generation"))
        evidence = make_evidence()
        report = integration.verify_and_consume_evidence(
            evidence,
            self.auth_for(evidence, identity),
        )
        self.assert_hold(report, "HOLD_STORE_SOURCE_GENERATION_MISMATCH")

    def test_store_source_base_mismatch_fails_closed(self) -> None:
        identity = self.create_attempt(self.identity(war_college_commit="1" * 40))
        evidence = make_evidence()
        report = integration.verify_and_consume_evidence(
            evidence,
            self.auth_for(evidence, identity),
        )
        self.assert_hold(
            report,
            "HOLD_STORE_WAR_COLLEGE_SOURCE_BASE_MISMATCH",
        )

    def test_missing_store_is_not_created_by_verification(self) -> None:
        self.assertFalse(self.store_path.exists())
        report = integration.verify_and_consume_evidence(make_evidence(), {})
        self.assert_hold(report, "HOLD_STORE_NOT_FOUND")
        self.assertFalse(self.store_path.exists())

    def test_reconnect_race_after_auth_green_fails_at_consume(self) -> None:
        identity = self.create_attempt()
        evidence = make_evidence()
        auth = self.auth_for(evidence, identity)
        original_consume = integration.consume_joint_evidence

        def raced_consume(
            path: Path,
            loaded_identity: store.AttemptIdentity,
            *,
            session_generation: int,
            joint_evidence_sha256: str,
        ):
            store.advance_session(
                path,
                loaded_identity,
                expected_current_generation=session_generation,
            )
            return original_consume(
                path,
                loaded_identity,
                session_generation=session_generation,
                joint_evidence_sha256=joint_evidence_sha256,
            )

        integration.consume_joint_evidence = raced_consume
        try:
            raced = integration.verify_and_consume_evidence(evidence, auth)
        finally:
            integration.consume_joint_evidence = original_consume

        self.assert_hold(raced, "HOLD_SESSION_NOT_CURRENT")

        fresh_evidence = make_evidence(controller_session_generation=2)
        fresh = integration.verify_and_consume_evidence(
            fresh_evidence,
            self.auth_for(fresh_evidence, identity),
        )
        self.assertEqual(fresh["contract"], "GREEN")

    def test_cli_is_one_line_and_requires_auth_file(self) -> None:
        identity = self.create_attempt()
        evidence = make_evidence()
        auth = self.auth_for(evidence, identity)

        evidence_path = Path(self._temp.name) / "evidence.json"
        auth_path = Path(self._temp.name) / "producer-auth.json"
        evidence_path.write_text(
            json.dumps(evidence, sort_keys=True),
            encoding="utf-8",
        )
        auth_path.write_text(
            json.dumps(auth, sort_keys=True),
            encoding="utf-8",
        )

        script = (
            Path(__file__).resolve().parents[1]
            / "scripts"
            / "verify_controller_evidence_with_durable_currentness_v1.py"
        )
        cp = subprocess.run(
            [sys.executable, str(script), str(evidence_path), str(auth_path)],
            capture_output=True,
            text=True,
            check=False,
            env=dict(os.environ),
        )
        self.assertEqual(cp.returncode, 0)
        self.assertEqual(cp.stderr, "")
        self.assertEqual(len(cp.stdout.splitlines()), 1)
        report = json.loads(cp.stdout)
        self.assertEqual(report["contract"], "GREEN")
        self.assertTrue(report["producer_signature_authentication_green"])


if __name__ == "__main__":
    unittest.main()
