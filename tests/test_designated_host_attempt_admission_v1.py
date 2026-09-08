#!/usr/bin/env python3
from __future__ import annotations

import importlib
import importlib.util
import os
import sqlite3
import stat
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "scripts/prepare_designated_host_attempt_admission_v1.py"
SPEC = importlib.util.spec_from_file_location("attempt_admission_tool", TOOL_PATH)
assert SPEC is not None and SPEC.loader is not None
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

PUBLIC_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEAejYyFziUrf8A2eRhz9/LJMM2SsMFvrEqVN1iC7m/G4g=\n"
    "-----END PUBLIC KEY-----\n"
)


def local_modules():
    structural = importlib.import_module("scripts.verify_controller_evidence_isolation_v1")
    producer_auth = importlib.import_module(
        "scripts.verify_controller_evidence_producer_auth_v1"
    )
    designated_root = importlib.import_module(
        "scripts.war_college_designated_producer_trust_root_v1"
    )
    store = importlib.import_module("scripts.controller_attempt_admission_store_v1")
    return structural, producer_auth, designated_root, store


class AttemptAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.contract = tool.load_contract()
        self.modules = local_modules()

    def identity(self, public_pem=PUBLIC_PEM):
        return tool.build_identity(
            contract=self.contract,
            modules=self.modules,
            public_pem=public_pem,
            attempt_id="attempt-production-shape-001",
            controller_a_id="controller-alpha",
            controller_a_player_id="Multi0",
            controller_b_id="controller-bravo",
            controller_b_player_id="Multi1",
        )

    def test_contract_grants_only_explicit_first_store_creation(self):
        self.assertEqual(
            self.contract["authority"],
            {
                "attempt_store_creation_authorized": True,
                "evidence_consumption_authorized": False,
                "live_request_materialization_authorized": False,
                "private_key_access": False,
                "runtime_execution_authorized": False,
                "service_action_authorized": False,
                "session_advance_authorized": False,
                "signing_authorized": False,
            },
        )
        self.assertEqual(self.contract["store_schema_version"], 3)
        self.assertEqual(self.contract["first_session_generation"], 1)

    def test_plan_binds_designated_public_identity_without_mutation(self):
        identity, trust = self.identity()
        report = tool.plan_admission(
            contract=self.contract,
            identity=identity,
            trust=trust,
        )
        self.assertEqual(report["phase"], "PLAN")
        self.assertFalse(report["store_creation_performed"])
        self.assertEqual(
            report["producer_node_id"],
            "9d89483769e469e0473b489dc50dba96",
        )
        self.assertEqual(report["initial_session_generation"], 1)

    def test_wrong_public_key_cannot_be_designated_producer(self):
        key = Ed25519PrivateKey.generate()
        bad = key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii")
        with self.assertRaises(tool.AdmissionToolHold):
            self.identity(bad)

    def test_apply_is_create_only_and_leaves_zero_consumptions(self):
        identity, _trust = self.identity()
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            os.chmod(data_dir, 0o700)
            store_path = data_dir / "war_college/controller_attempt_admission_v3.sqlite3"

            report = tool.apply_admission(
                contract=self.contract,
                modules=self.modules,
                identity=identity,
                confirmation=self.contract["explicit_apply_confirmation"],
                store_path=store_path,
                data_dir=data_dir,
                enforce_host=False,
            )
            self.assertTrue(report["store_creation_performed"])
            self.assertEqual(report["readback"]["schema_version"], 3)
            self.assertEqual(report["readback"]["session_generation"], 1)
            self.assertEqual(report["readback"]["consumption_count"], 0)
            self.assertEqual(stat.S_IMODE(store_path.stat().st_mode), 0o600)

            db = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
            try:
                self.assertEqual(
                    db.execute("SELECT COUNT(*) FROM consumptions").fetchone()[0],
                    0,
                )
            finally:
                db.close()

            with self.assertRaisesRegex(
                tool.AdmissionToolHold,
                "HOLD_CANONICAL_STORE_ALREADY_EXISTS",
            ):
                tool.apply_admission(
                    contract=self.contract,
                    modules=self.modules,
                    identity=identity,
                    confirmation=self.contract["explicit_apply_confirmation"],
                    store_path=store_path,
                    data_dir=data_dir,
                    enforce_host=False,
                )

    def test_apply_requires_exact_confirmation(self):
        identity, _trust = self.identity()
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            os.chmod(data_dir, 0o700)
            store_path = data_dir / "war_college/controller_attempt_admission_v3.sqlite3"
            with self.assertRaisesRegex(
                tool.AdmissionToolHold,
                "HOLD_EXPLICIT_APPLY_CONFIRMATION",
            ):
                tool.apply_admission(
                    contract=self.contract,
                    modules=self.modules,
                    identity=identity,
                    confirmation="wrong",
                    store_path=store_path,
                    data_dir=data_dir,
                    enforce_host=False,
                )
            self.assertFalse(store_path.exists())


if __name__ == "__main__":
    unittest.main()
