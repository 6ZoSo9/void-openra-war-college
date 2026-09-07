#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import unittest
from dataclasses import replace
from datetime import datetime, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from scripts import verify_controller_evidence_producer_auth_v1 as producer_auth
from scripts import war_college_designated_producer_trust_root_v1 as trust
from scripts.controller_attempt_admission_store_v1 import AttemptIdentity


def pem(private_key: Ed25519PrivateKey) -> str:
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def synthetic_root_and_identity() -> tuple[
    trust.DesignatedProducerTrustRootV1,
    AttemptIdentity,
    dict[str, object],
]:
    key = Ed25519PrivateKey.generate()
    public_pem = pem(key)
    derived = producer_auth.derive_void_node_identity_from_public_pem(public_pem)
    assert derived is not None
    node_id, pem_sha256, public_key = derived
    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    der_sha256 = hashlib.sha256(der).hexdigest()

    base = replace(
        trust.PRODUCTION_TRUST_ROOT,
        producer_node_id=node_id,
        public_key_fingerprint_sha256=der_sha256,
        expires_at_utc="2027-12-31T23:59:59.000Z",
        root_id="voidwcdptr1_" + "0" * 64,
    )
    root = replace(base, root_id=trust.derive_trust_root_id_v1(base))
    identity = AttemptIdentity(
        attempt_id="attempt-001",
        producer_id=node_id,
        producer_public_key_sha256=pem_sha256,
        controller_a_id="controller-a",
        controller_a_player_id="player-1",
        controller_b_id="controller-b",
        controller_b_player_id="player-2",
        source_generation="ad1926569b12466c",
        war_college_commit="f57c561f3a4c742e34d820933be40dd7d4253951",
        engine_commit="1607a7a6501d42a47638393ecef8b22831064932",
    )
    auth = {"producer_public_key_pem": public_pem}
    return root, identity, auth


class DesignatedProducerTrustRootTests(unittest.TestCase):
    def assert_hold(self, report: dict[str, object], code: str) -> None:
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_production_root_is_exact_and_self_consistent(self) -> None:
        root = trust.PRODUCTION_TRUST_ROOT
        trust.validate_trust_root_v1(root)
        self.assertEqual(
            root.root_id,
            "voidwcdptr1_"
            "6f5e9ea9e192cae9166c5be293e94437748e5d21d72bd8f27681a61979a29ba9",
        )
        self.assertEqual(
            root.producer_node_id,
            "9d89483769e469e0473b489dc50dba96",
        )
        self.assertEqual(
            root.public_key_fingerprint_sha256,
            "2f52b928cb00bf309510d1edef299554277fba6d52bfd1ddb52b9b015397c50b",
        )
        self.assertEqual(
            root.trust_profile_blob_sha1,
            "c181e5872650b2a1c29d0d3cc958676db34043b0",
        )
        self.assertEqual(
            root.identity_confirmation_blob_sha1,
            "34f88de65129010a2090303028809002981061c8",
        )

    def test_generic_verifier_accepts_matching_synthetic_root(self) -> None:
        root, identity, auth = synthetic_root_and_identity()
        report = trust.verify_designated_producer_trust_v1(
            identity=identity,
            producer_auth_record=auth,
            root=root,
            now_utc=datetime(2026, 9, 7, tzinfo=timezone.utc),
        )
        self.assertEqual(report["contract"], "GREEN")

    def test_production_root_rejects_unrelated_synthetic_node(self) -> None:
        _root, identity, auth = synthetic_root_and_identity()
        report = trust.verify_designated_producer_trust_v1(
            identity=identity,
            producer_auth_record=auth,
            now_utc=datetime(2026, 9, 7, tzinfo=timezone.utc),
        )
        self.assert_hold(report, "HOLD_DESIGNATED_PRODUCER_NODE_ID_MISMATCH")
        self.assert_hold(
            report,
            "HOLD_DESIGNATED_PRODUCER_PUBLIC_KEY_FINGERPRINT_MISMATCH",
        )

    def test_fingerprint_substitution_fails_closed(self) -> None:
        root, identity, auth = synthetic_root_and_identity()
        bad = replace(
            root,
            public_key_fingerprint_sha256="f" * 64,
            root_id="voidwcdptr1_" + "0" * 64,
        )
        bad = replace(bad, root_id=trust.derive_trust_root_id_v1(bad))
        report = trust.verify_designated_producer_trust_v1(
            identity=identity,
            producer_auth_record=auth,
            root=bad,
            now_utc=datetime(2026, 9, 7, tzinfo=timezone.utc),
        )
        self.assert_hold(
            report,
            "HOLD_DESIGNATED_PRODUCER_PUBLIC_KEY_FINGERPRINT_MISMATCH",
        )

    def test_store_public_key_hash_substitution_fails_closed(self) -> None:
        root, identity, auth = synthetic_root_and_identity()
        bad_identity = replace(identity, producer_public_key_sha256="e" * 64)
        report = trust.verify_designated_producer_trust_v1(
            identity=bad_identity,
            producer_auth_record=auth,
            root=root,
            now_utc=datetime(2026, 9, 7, tzinfo=timezone.utc),
        )
        self.assert_hold(
            report,
            "HOLD_DESIGNATED_PRODUCER_STORE_PUBLIC_KEY_MISMATCH",
        )

    def test_expired_root_fails_closed(self) -> None:
        root, identity, auth = synthetic_root_and_identity()
        report = trust.verify_designated_producer_trust_v1(
            identity=identity,
            producer_auth_record=auth,
            root=root,
            now_utc=datetime(2028, 1, 1, tzinfo=timezone.utc),
        )
        self.assert_hold(report, "HOLD_DESIGNATED_PRODUCER_TRUST_ROOT_EXPIRED")

    def test_root_identity_drift_fails_self_validation(self) -> None:
        root = replace(
            trust.PRODUCTION_TRUST_ROOT,
            source_commit="1" * 40,
        )
        with self.assertRaisesRegex(ValueError, "trust-root id mismatch"):
            trust.validate_trust_root_v1(root)


if __name__ == "__main__":
    unittest.main()
