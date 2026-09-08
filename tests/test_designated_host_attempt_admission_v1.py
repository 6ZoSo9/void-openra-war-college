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
from unittest import mock

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
                "pathname_delete_authorized": False,
                "private_key_access": False,
                "runtime_execution_authorized": False,
                "service_action_authorized": False,
                "session_advance_authorized": False,
                "signing_authorized": False,
            },
        )
        self.assertEqual(self.contract["store_schema_version"], 3)
        self.assertEqual(self.contract["first_session_generation"], 1)
        self.assertEqual(
            self.contract["canonical_publish_strategy"],
            "linux_linkat_at_empty_path_descriptor_source_v1",
        )
        self.assertTrue(self.contract["retained_staging_alias_required"])
        self.assertEqual(self.contract["store_required_link_count_after_publish"], 2)

    def test_plan_binds_designated_public_identity_without_mutation(self):
        identity, trust = self.identity()
        report = tool.plan_admission(
            contract=self.contract,
            identity=identity,
            trust=trust,
        )
        self.assertEqual(report["phase"], "PLAN")
        self.assertFalse(report["mutation_performed"])
        self.assertFalse(report["canonical_store_created"])
        self.assertFalse(report["staging_alias_created"])
        self.assertEqual(
            report["producer_node_id"],
            "9d89483769e469e0473b489dc50dba96",
        )

    def test_wrong_public_key_cannot_be_designated_producer(self):
        key = Ed25519PrivateKey.generate()
        bad = key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii")
        with self.assertRaises(tool.AdmissionToolHold):
            self.identity(bad)

    def test_apply_descriptor_publishes_create_only_and_retains_alias(self):
        identity, _trust = self.identity()
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            os.chmod(data_dir, 0o700)
            wc = data_dir / "war_college"
            store_path = wc / "controller_attempt_admission_v3.sqlite3"
            staging_path = wc / ".controller_attempt_admission_v3.sqlite3.staging-v1"

            report = tool.apply_admission(
                contract=self.contract,
                modules=self.modules,
                identity=identity,
                confirmation=self.contract["explicit_apply_confirmation"],
                store_path=store_path,
                data_dir=data_dir,
                staging_path=staging_path,
                enforce_host=False,
            )
            self.assertTrue(report["mutation_performed"])
            self.assertTrue(report["canonical_store_created"])
            self.assertTrue(report["staging_alias_created"])
            self.assertTrue(report["staging_alias_retained"])
            self.assertTrue(store_path.is_file())
            self.assertTrue(staging_path.is_file())
            self.assertTrue(os.path.samestat(store_path.stat(), staging_path.stat()))
            self.assertEqual(store_path.stat().st_nlink, 2)
            self.assertEqual(stat.S_IMODE(store_path.stat().st_mode), 0o600)

            db = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
            try:
                self.assertEqual(
                    db.execute("SELECT COUNT(*) FROM attempts").fetchone()[0], 1
                )
                self.assertEqual(
                    db.execute("SELECT COUNT(*) FROM sessions").fetchone()[0], 1
                )
                self.assertEqual(
                    db.execute("SELECT COUNT(*) FROM consumptions").fetchone()[0], 0
                )
            finally:
                db.close()

    def test_apply_requires_exact_confirmation_without_mutation(self):
        identity, _trust = self.identity()
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            store_path = data_dir / "war_college/controller_attempt_admission_v3.sqlite3"
            staging_path = data_dir / "war_college/.controller_attempt_admission_v3.sqlite3.staging-v1"
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
                    staging_path=staging_path,
                    enforce_host=False,
                )
            self.assertFalse((data_dir / "war_college").exists())

    def test_linkat_create_only_preserves_preexisting_canonical(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            dir_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            source = root / "source"
            source_fd = os.open(source, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
            try:
                os.write(source_fd, b"source-bytes")
                canonical = root / "canonical"
                canonical.write_bytes(b"foreign")
                with self.assertRaisesRegex(
                    tool.AdmissionToolHold,
                    "HOLD_CANONICAL_STORE_ALREADY_EXISTS",
                ):
                    tool._link_fd_create_only(source_fd, dir_fd, canonical.name)
                self.assertEqual(canonical.read_bytes(), b"foreign")
            finally:
                os.close(source_fd)
                os.close(dir_fd)

    def test_descriptor_publication_ignores_staging_path_substitution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            dir_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            staging = root / "staging"
            source_fd = os.open(staging, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
            try:
                os.write(source_fd, b"descriptor-original")
                moved = root / "moved-original"
                os.rename(staging, moved)
                staging.write_bytes(b"foreign-replacement")
                tool._link_fd_create_only(source_fd, dir_fd, "canonical")
                self.assertEqual((root / "canonical").read_bytes(), b"descriptor-original")
                self.assertEqual(staging.read_bytes(), b"foreign-replacement")
            finally:
                os.close(source_fd)
                os.close(dir_fd)

    def test_failed_store_initialization_reports_partial_mutation_truthfully(self):
        identity, _trust = self.identity()

        class FailingStore:
            @staticmethod
            def create_attempt(path, identity):
                raise RuntimeError("synthetic failure")

        modules = (*self.modules[:3], FailingStore)
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            wc = data_dir / "war_college"
            store_path = wc / "controller_attempt_admission_v3.sqlite3"
            staging_path = wc / ".controller_attempt_admission_v3.sqlite3.staging-v1"
            with self.assertRaises(tool.ApplyAdmissionHold) as caught:
                tool.apply_admission(
                    contract=self.contract,
                    modules=modules,
                    identity=identity,
                    confirmation=self.contract["explicit_apply_confirmation"],
                    store_path=store_path,
                    data_dir=data_dir,
                    staging_path=staging_path,
                    enforce_host=False,
                )
            hold = caught.exception
            self.assertTrue(hold.mutation_performed)
            self.assertTrue(hold.war_college_directory_created)
            self.assertTrue(hold.staging_alias_created)
            self.assertFalse(hold.canonical_store_created)
            self.assertTrue(staging_path.is_file())
            self.assertFalse(store_path.exists())

    def test_directory_helper_failure_keeps_created_state_truthful(self):
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            data_fd = os.open(data_dir, os.O_RDONLY | os.O_DIRECTORY)
            mutation = tool.MutationState()
            try:
                with mock.patch.object(
                    tool,
                    "_require_fd_directory",
                    side_effect=tool.AdmissionToolHold("synthetic directory validation"),
                ):
                    with self.assertRaises(tool.AdmissionToolHold):
                        tool._open_or_create_wc_directory(
                            data_fd,
                            uid=os.getuid(),
                            gid=os.getgid(),
                            mutation=mutation,
                        )
                self.assertTrue(mutation.war_college_directory_created)
                self.assertTrue((data_dir / "war_college").is_dir())
            finally:
                os.close(data_fd)

    def test_staging_helper_failure_keeps_created_state_truthful(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            dir_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
            mutation = tool.MutationState()
            try:
                with mock.patch.object(
                    tool,
                    "_require_staging_descriptor",
                    side_effect=tool.AdmissionToolHold("synthetic staging validation"),
                ):
                    with self.assertRaises(tool.AdmissionToolHold):
                        tool._open_staging_descriptor(
                            dir_fd,
                            "staging",
                            uid=os.getuid(),
                            gid=os.getgid(),
                            mutation=mutation,
                        )
                self.assertTrue(mutation.staging_alias_created)
                self.assertTrue((root / "staging").is_file())
            finally:
                os.close(dir_fd)

    def test_second_apply_never_reuses_existing_staging_or_canonical(self):
        identity, _trust = self.identity()
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data_a"
            data_dir.mkdir(mode=0o700)
            wc = data_dir / "war_college"
            store_path = wc / "controller_attempt_admission_v3.sqlite3"
            staging_path = wc / ".controller_attempt_admission_v3.sqlite3.staging-v1"

            tool.apply_admission(
                contract=self.contract,
                modules=self.modules,
                identity=identity,
                confirmation=self.contract["explicit_apply_confirmation"],
                store_path=store_path,
                data_dir=data_dir,
                staging_path=staging_path,
                enforce_host=False,
            )
            before = store_path.read_bytes()
            with self.assertRaises(tool.ApplyAdmissionHold):
                tool.apply_admission(
                    contract=self.contract,
                    modules=self.modules,
                    identity=identity,
                    confirmation=self.contract["explicit_apply_confirmation"],
                    store_path=store_path,
                    data_dir=data_dir,
                    staging_path=staging_path,
                    enforce_host=False,
                )
            self.assertEqual(store_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
