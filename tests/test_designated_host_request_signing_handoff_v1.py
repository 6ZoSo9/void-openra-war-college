#!/usr/bin/env python3
from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import json
import os
import sqlite3
import stat
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "scripts" / "prepare_designated_host_request_signing_handoff_v1.py"
SPEC = importlib.util.spec_from_file_location("handoff_tool", TOOL_PATH)
assert SPEC is not None and SPEC.loader is not None
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

from scripts import controller_attempt_admission_store_v1 as store
from scripts import verify_controller_evidence_isolation_v1 as structural
from scripts import verify_controller_evidence_producer_auth_v1 as producer_auth
from scripts import war_college_designated_host_verify_request_v1 as wrapper
from scripts import war_college_designated_producer_trust_root_v1 as designated_root


def modules():
    return structural, producer_auth, designated_root, store, wrapper


def make_record(player_id, controller_id, world_tick, attempt_id, generation):
    if player_id == "player-1":
        own_units, own_buildings, enemies = [101], [1101], [201, 1201]
    else:
        own_units, own_buildings, enemies = [201], [1201], [101, 1101]
    observation_payload = {
        "attempt_id": attempt_id,
        "controller_session_generation": generation,
        "player_id": player_id,
        "owned_unit_actor_ids": own_units,
        "owned_building_actor_ids": own_buildings,
        "visible_enemy_actor_ids": enemies,
        "available_production_items": ["e1", "powr"],
        "active_production_items": ["powr"],
        "world_tick": world_tick,
    }
    observation_sha = structural.sha256_hex(observation_payload)
    observation_binding = structural.observation_binding(
        attempt_id=attempt_id,
        controller_session_generation=generation,
        player_id=player_id,
        controller_id=controller_id,
        world_tick=world_tick,
        observation_sha256=observation_sha,
    )
    request_id = f"decision-{attempt_id}-{generation}-{world_tick}-{player_id}"
    action_payload = {
        "attempt_id": attempt_id,
        "controller_session_generation": generation,
        "commands": [{
            "action": "move",
            "actor_id": own_units[0],
            "target_actor_id": 0,
            "target_x": 5,
            "target_y": 5,
            "item_type": "",
            "queued": False,
        }],
        "controller_id": controller_id,
        "decision_observation_binding_sha256": observation_binding,
        "player_id": player_id,
        "request_id": request_id,
        "world_tick": world_tick,
    }
    action_sha = structural.sha256_hex(action_payload)
    return {
        "action_actor_player_id": player_id,
        "action_binding_sha256": structural.action_binding(
            attempt_id=attempt_id,
            controller_session_generation=generation,
            player_id=player_id,
            controller_id=controller_id,
            world_tick=world_tick,
            action_request_id=request_id,
            action_sha256=action_sha,
            decision_observation_binding_sha256=observation_binding,
        ),
        "action_payload": action_payload,
        "action_request_id": request_id,
        "action_sha256": action_sha,
        "controller_id": controller_id,
        "observation_binding_sha256": observation_binding,
        "observation_payload": observation_payload,
        "observation_sha256": observation_sha,
        "observation_subject_player_id": player_id,
        "player_id": player_id,
        "visibility_owner_player_id": player_id,
    }


def make_evidence(attempt_id="attempt-001", generation=1):
    tick = 420
    controllers = [
        make_record("player-1", "controller-a", tick, attempt_id, generation),
        make_record("player-2", "controller-b", tick, attempt_id, generation),
    ]
    bindings = [{
        "action_binding_sha256": record["action_binding_sha256"],
        "controller_id": record["controller_id"],
        "observation_binding_sha256": record["observation_binding_sha256"],
        "player_id": record["player_id"],
    } for record in controllers]
    joint = structural.joint_evidence_binding(
        attempt_id=attempt_id,
        controller_session_generation=generation,
        world_tick=tick,
        bindings=bindings,
    )
    return {
        "attempt_id": attempt_id,
        "controller_session_generation": generation,
        "controllers": controllers,
        "engine_frozen_commit": structural.ENGINE_FROZEN_COMMIT,
        "generation": structural.GENERATION,
        "joint_evidence_sha256": joint,
        "marker": structural.MARKER,
        "schema_version": structural.SCHEMA_VERSION,
        "war_college_frozen_commit": structural.WAR_COLLEGE_FROZEN_COMMIT,
        "world_tick": tick,
    }


def test_root(public_pem):
    derived = producer_auth.derive_void_node_identity_from_public_pem(public_pem)
    assert derived is not None
    node_id, _pem_sha, _key = derived
    fingerprint = designated_root.public_key_der_fingerprint_sha256_v1(public_pem)
    root = designated_root.DesignatedProducerTrustRootV1(
        marker=designated_root.MARKER,
        version=designated_root.VERSION,
        authority_scope=designated_root.AUTHORITY_SCOPE,
        designated_host_label="precision",
        source_repository="6ZoSo9/void-node",
        source_commit="1" * 40,
        trust_profile_path="config/void-tor-agent-access-client-v1.json",
        trust_profile_blob_sha1="2" * 40,
        trust_profile_marker="VOID_TOR_AGENT_ACCESS_CLIENT_PROFILE_V1",
        identity_confirmation_path="docs/public/local-multibox-nimo-rejoin-operator-runbook-v1.md",
        identity_confirmation_blob_sha1="3" * 40,
        producer_node_id=node_id,
        public_key_fingerprint_sha256=fingerprint,
        binding_sha256="4" * 64,
        expires_at_utc="2099-01-01T00:00:00.000Z",
        root_id="voidwcdptr1_" + "0" * 64,
    )
    return dataclasses.replace(root, root_id=designated_root.derive_trust_root_id_v1(root))


class SigningHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store_path = self.root / "store.sqlite3"
        self.private_key = Ed25519PrivateKey.generate()
        public_key = self.private_key.public_key()
        self.public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("ascii")
        derived = producer_auth.derive_void_node_identity_from_public_pem(self.public_pem)
        assert derived is not None
        node_id, pem_sha, _ = derived
        self.identity = store.AttemptIdentity(
            attempt_id="attempt-001",
            producer_id=node_id,
            producer_public_key_sha256=pem_sha,
            controller_a_id="controller-a",
            controller_a_player_id="player-1",
            controller_b_id="controller-b",
            controller_b_player_id="player-2",
            source_generation=structural.GENERATION,
            war_college_commit="f57c561f3a4c742e34d820933be40dd7d4253951",
            engine_commit=structural.ENGINE_FROZEN_COMMIT,
        )
        store.create_attempt(self.store_path, self.identity)
        self.evidence = make_evidence()
        self.evidence_raw = json.dumps(
            self.evidence, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        self.contract = {
            "request_id_derivation_domain": "VOID_WAR_COLLEGE_REQUEST_ID_V1",
            "store_path": str(self.store_path),
        }
        self.trust_root = test_root(self.public_pem)

    def tearDown(self):
        self.temp.cleanup()

    def consumption_count(self):
        connection = sqlite3.connect(f"file:{self.store_path}?mode=ro", uri=True)
        try:
            return connection.execute("SELECT COUNT(*) FROM consumptions").fetchone()[0]
        finally:
            connection.close()

    def test_prepare_emits_unsigned_handoff_without_consumption(self):
        evidence_path = self.root / "input-evidence.json"
        public_path = self.root / "public.pem"
        evidence_path.write_bytes(self.evidence_raw)
        public_path.write_text(self.public_pem, encoding="ascii")
        output = self.root / "handoff"

        before = self.consumption_count()
        report = tool.prepare_handoff(
            evidence_path=evidence_path,
            public_pem_path=public_path,
            output_dir=output,
            contract=self.contract,
            modules=modules(),
            store_path=self.store_path,
            root_override=self.trust_root,
        )
        after = self.consumption_count()

        self.assertEqual(before, 0)
        self.assertEqual(after, 0)
        self.assertTrue(report["signature_required"])
        self.assertFalse(report["private_key_access"])
        self.assertFalse(report["store_mutation_performed"])
        self.assertFalse((output / tool.AUTH_FILE).exists())
        self.assertFalse((output / tool.REQUEST_FILE).exists())
        self.assertTrue((output / tool.TRANSCRIPT_FILE).is_file())

    def test_finalize_verifies_signature_and_stages_exact_bundle_without_consumption(self):
        evidence_path = self.root / "input-evidence.json"
        public_path = self.root / "public.pem"
        evidence_path.write_bytes(self.evidence_raw)
        public_path.write_text(self.public_pem, encoding="ascii")
        output = self.root / "handoff"
        tool.prepare_handoff(
            evidence_path=evidence_path,
            public_pem_path=public_path,
            output_dir=output,
            contract=self.contract,
            modules=modules(),
            store_path=self.store_path,
            root_override=self.trust_root,
        )
        transcript = (output / tool.TRANSCRIPT_FILE).read_bytes()
        signature_hex = self.private_key.sign(transcript).hex()

        before = self.consumption_count()
        report = tool.finalize_handoff(
            handoff_dir=output,
            signature_hex=signature_hex,
            contract=self.contract,
            modules=modules(),
            store_path=self.store_path,
            root_override=self.trust_root,
        )
        after = self.consumption_count()

        self.assertEqual(before, 0)
        self.assertEqual(after, 0)
        self.assertTrue(report["signature_verified"])
        self.assertFalse(report["live_bundle_materialization_authorized"])
        self.assertFalse(report["service_start_authorized"])
        bundle = Path(report["bundle_dir"])
        self.assertEqual(
            {p.name for p in bundle.iterdir()},
            {tool.REQUEST_FILE, tool.EVIDENCE_FILE, tool.AUTH_FILE},
        )
        for name in (tool.REQUEST_FILE, tool.EVIDENCE_FILE, tool.AUTH_FILE):
            self.assertEqual(stat.S_IMODE((bundle / name).stat().st_mode), 0o400)

    def test_wrong_signature_fails_before_bundle_creation(self):
        evidence_path = self.root / "input-evidence.json"
        public_path = self.root / "public.pem"
        evidence_path.write_bytes(self.evidence_raw)
        public_path.write_text(self.public_pem, encoding="ascii")
        output = self.root / "handoff"
        tool.prepare_handoff(
            evidence_path=evidence_path,
            public_pem_path=public_path,
            output_dir=output,
            contract=self.contract,
            modules=modules(),
            store_path=self.store_path,
            root_override=self.trust_root,
        )
        with self.assertRaises(tool.HandoffHold):
            tool.finalize_handoff(
                handoff_dir=output,
                signature_hex="0" * 128,
                contract=self.contract,
                modules=modules(),
                store_path=self.store_path,
                root_override=self.trust_root,
            )
        self.assertFalse((output / tool.BUNDLE_DIR).exists())
        self.assertEqual(self.consumption_count(), 0)


if __name__ == "__main__":
    unittest.main()
