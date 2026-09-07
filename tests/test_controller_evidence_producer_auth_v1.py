#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from scripts.controller_attempt_admission_store_v1 import AttemptIdentity
from scripts import verify_controller_evidence_producer_auth_v1 as auth

JOINT = "a" * 64
ENGINE = "1607a7a6501d42a47638393ecef8b22831064932"
STORE_BASE = "f57c561f3a4c742e34d820933be40dd7d4253951"
FROZEN_WC = "973802ef0a614e5afa782ff20e231e18966ae3e5"
GENERATION = "ad1926569b12466c"


def public_pem(private_key: Ed25519PrivateKey) -> str:
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def identity_for(private_key: Ed25519PrivateKey) -> AttemptIdentity:
    pem = public_pem(private_key)
    derived = auth.derive_void_node_identity_from_public_pem(pem)
    assert derived is not None
    node_id, full_sha, _ = derived
    return AttemptIdentity(
        attempt_id="attempt-001",
        producer_id=node_id,
        producer_public_key_sha256=full_sha,
        controller_a_id="controller-a",
        controller_a_player_id="player-1",
        controller_b_id="controller-b",
        controller_b_player_id="player-2",
        source_generation=GENERATION,
        war_college_commit=STORE_BASE,
        engine_commit=ENGINE,
    )


def envelope(
    private_key: Ed25519PrivateKey,
    identity: AttemptIdentity,
    *,
    session_generation: int = 1,
    joint: str = JOINT,
) -> dict[str, object]:
    pem = public_pem(private_key)
    transcript = auth.producer_auth_transcript_bytes(
        identity,
        session_generation=session_generation,
        joint_evidence_sha256=joint,
        evidence_generation=GENERATION,
        war_college_frozen_commit=FROZEN_WC,
        engine_frozen_commit=ENGINE,
    )
    return {
        "attempt_id": identity.attempt_id,
        "joint_evidence_sha256": joint,
        "marker": auth.MARKER,
        "producer_node_id": identity.producer_id,
        "producer_public_key_pem": pem,
        "producer_public_key_sha256": identity.producer_public_key_sha256,
        "schema_version": auth.SCHEMA_VERSION,
        "session_generation": session_generation,
        "signature_hex": private_key.sign(transcript).hex(),
        "transcript_sha256": hashlib.sha256(transcript).hexdigest(),
    }


class ProducerAuthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.key = Ed25519PrivateKey.generate()
        self.identity = identity_for(self.key)

    def verify(self, value: object, *, identity: AttemptIdentity | None = None) -> dict[str, object]:
        return auth.verify_producer_auth(
            value,
            identity=identity or self.identity,
            session_generation=1,
            joint_evidence_sha256=JOINT,
            evidence_generation=GENERATION,
            war_college_frozen_commit=FROZEN_WC,
            engine_frozen_commit=ENGINE,
        )

    def assert_hold(self, report: dict[str, object], code: str) -> None:
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_valid_existing_void_node_identity_signature_is_green(self) -> None:
        report = self.verify(envelope(self.key, self.identity))
        self.assertEqual(report["contract"], "GREEN")

    def test_wrong_private_key_fails_signature_verification(self) -> None:
        wrong = Ed25519PrivateKey.generate()
        value = envelope(self.key, self.identity)
        transcript = auth.producer_auth_transcript_bytes(
            self.identity,
            session_generation=1,
            joint_evidence_sha256=JOINT,
            evidence_generation=GENERATION,
            war_college_frozen_commit=FROZEN_WC,
            engine_frozen_commit=ENGINE,
        )
        value["signature_hex"] = wrong.sign(transcript).hex()
        self.assert_hold(
            self.verify(value),
            "HOLD_PRODUCER_AUTH_SIGNATURE_VERIFICATION_FAILED",
        )

    def test_public_key_must_match_durably_pinned_full_sha(self) -> None:
        wrong = Ed25519PrivateKey.generate()
        value = envelope(wrong, identity_for(wrong))
        value["attempt_id"] = self.identity.attempt_id
        self.assert_hold(
            self.verify(value),
            "HOLD_PRODUCER_NODE_ID_NOT_DURABLY_PINNED",
        )
        self.assert_hold(
            self.verify(value),
            "HOLD_PRODUCER_PUBLIC_KEY_NOT_DURABLY_PINNED",
        )

    def test_transcript_replay_under_different_session_fails(self) -> None:
        value = envelope(self.key, self.identity)
        value["session_generation"] = 2
        self.assert_hold(self.verify(value), "HOLD_PRODUCER_AUTH_SESSION_MISMATCH")

    def test_joint_digest_mutation_fails_before_signature_use(self) -> None:
        value = envelope(self.key, self.identity)
        value["joint_evidence_sha256"] = "b" * 64
        self.assert_hold(
            self.verify(value),
            "HOLD_PRODUCER_AUTH_JOINT_DIGEST_MISMATCH",
        )

    def test_schema_extension_fails_closed(self) -> None:
        value = envelope(self.key, self.identity)
        value["extra"] = True
        self.assert_hold(self.verify(value), "HOLD_PRODUCER_AUTH_SCHEMA_DRIFT")

    def test_noncanonical_pem_fails_closed(self) -> None:
        value = envelope(self.key, self.identity)
        value["producer_public_key_pem"] = str(value["producer_public_key_pem"]) + "\n"
        self.assert_hold(
            self.verify(value),
            "HOLD_PRODUCER_PUBLIC_KEY_NOT_CANONICAL_ED25519",
        )

    def test_bounded_file_reader_rejects_oversized_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "auth.json"
            path.write_bytes(b"{" + b"x" * auth.MAX_AUTH_BYTES + b"}")
            with self.assertRaisesRegex(
                auth.ProducerAuthAdmissionError,
                "HOLD_PRODUCER_AUTH_FILE_TOO_LARGE",
            ):
                auth.read_producer_auth_file(path)

    def test_bounded_file_reader_accepts_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "auth.json"
            value = envelope(self.key, self.identity)
            path.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")
            self.assertEqual(auth.read_producer_auth_file(path), value)


if __name__ == "__main__":
    unittest.main()
