from __future__ import annotations

import hashlib
import json
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from openra_env.learning.general_brain_generation import (
    classify_abaddon_from_apollyon_v22_pair,
)
from tools import abaddon_policy_candidate_duel_wrapper as wrapper


class FakeRefiner:
    SCHEMA = "void.abaddon.policy-genome.v1"

    @staticmethod
    def digest(value):
        return hashlib.sha256(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    @classmethod
    def validate_genome(cls, genome):
        if genome.get("schema") != cls.SCHEMA:
            raise ValueError("schema drift")
        if genome.get("identity") != "Abaddon":
            raise ValueError("identity drift")
        if "profiles" not in genome:
            raise ValueError("profiles missing")

    @staticmethod
    def policy_for(genome, doctrine):
        return dict(genome["profiles"][doctrine.upper()])


def genome():
    body = {
        "schema": FakeRefiner.SCHEMA,
        "identity": "Abaddon",
        "generation": 1,
        "controller_version": 1,
        "profiles": {
            "RUSHER": {
                "inf": 6,
                "veh": 1,
                "group": 4,
                "power_margin_min": 35,
                "weap_power_min": 50,
                "scout_current_min": 10,
                "scout_history_min": 16,
                "advance_ticks": 50,
            }
        },
        "source": "fixture",
    }
    body["genome_sha256"] = FakeRefiner.digest(body)
    return body


class FakeController:
    def __init__(self, doctrine, seed=2050, policy=None):
        self.doctrine = doctrine
        self.seed = seed
        self.policy = policy

    def decide(self, observation):
        return {
            "action": {
                "tool": "advance",
                "arguments": {"ticks": self.policy["advance_ticks"]},
            },
            "observation": observation,
        }


class FakeBase:
    ABADDON_CONTROLLER = wrapper.ABADDON_CONTROLLER
    ABADDON_CONTROLLER_SHA = wrapper.ABADDON_CONTROLLER_SHA256

    def __init__(self):
        self.load_calls = []

    def load_module(self, path, name):
        self.load_calls.append((Path(path), name))
        if Path(path).resolve() == wrapper.ABADDON_CONTROLLER.resolve():
            module = types.ModuleType("fake_abaddon_controller")
            module.AbaddonController = FakeController
            return module
        module = types.ModuleType(name)
        module.marker = "other"
        return module


class FakeLegacy:
    def __init__(self):
        self.base = FakeBase()
        self.rows = []
        self.load_base = lambda: self.base
        self.append_jsonl = lambda path, row: self.rows.append(dict(row))


class AbaddonPolicyCandidateWrapperTests(unittest.TestCase):
    def setUp(self):
        self.genome = genome()
        self.binding = {
            "candidate_file_sha256": "a" * 64,
            "candidate_genome_sha256": self.genome["genome_sha256"],
            "legacy_runner_sha256": wrapper.LEGACY_RUNNER_SHA256,
            "abaddon_controller_sha256": wrapper.ABADDON_CONTROLLER_SHA256,
            "abaddon_refiner_sha256": wrapper.ABADDON_REFINER_SHA256,
        }

    def test_candidate_controller_proxy_injects_policy_only_at_constructor(self):
        module = types.ModuleType("original")
        module.AbaddonController = FakeController
        proxy = wrapper._candidate_controller_module(
            module,
            FakeRefiner,
            self.genome,
            self.binding,
        )
        controller = proxy.AbaddonController("RUSHER", 2050)
        self.assertEqual(controller.policy["inf"], 6)
        self.assertEqual(controller.policy["advance_ticks"], 50)
        self.assertEqual(controller.seed, 2050)
        self.assertEqual(
            controller._void_candidate_binding["candidate_genome_sha256"],
            self.genome["genome_sha256"],
        )
        with self.assertRaisesRegex(
            wrapper.WrapperError,
            "override candidate policy",
        ):
            proxy.AbaddonController("RUSHER", policy={"advance_ticks": 25})

    def test_hooks_wrap_only_exact_abaddon_controller_load(self):
        legacy = FakeLegacy()
        original_load_base = legacy.load_base
        hooks = wrapper.AbaddonCandidateHooks(
            legacy,
            FakeRefiner,
            self.genome,
            self.binding,
        )
        hooks.install()
        try:
            with mock.patch.object(
                wrapper,
                "sha256_file",
                return_value=wrapper.ABADDON_CONTROLLER_SHA256,
            ):
                base = legacy.load_base()
                other = base.load_module(Path("/tmp/other.py"), "other")
                candidate_module = base.load_module(
                    wrapper.ABADDON_CONTROLLER,
                    "abaddon",
                )
        finally:
            hooks.restore()

        self.assertEqual(other.marker, "other")
        controller = candidate_module.AbaddonController("RUSHER", 2050)
        self.assertEqual(controller.policy["inf"], 6)
        self.assertIs(legacy.load_base, original_load_base)

    def test_run_header_records_abaddon_candidate_without_promotion_authority(self):
        legacy = FakeLegacy()
        hooks = wrapper.AbaddonCandidateHooks(
            legacy,
            FakeRefiner,
            self.genome,
            self.binding,
        )
        hooks.install()
        try:
            legacy.append_jsonl(
                Path("unused"),
                {
                    "event": "run_header",
                    "abaddon_controller_sha256":
                        wrapper.ABADDON_CONTROLLER_SHA256,
                    "candidate_only": True,
                },
            )
        finally:
            hooks.restore()

        evidence = legacy.rows[0][wrapper.EVIDENCE_KEY]
        self.assertEqual(evidence["schema"], wrapper.RUN_SCHEMA)
        self.assertEqual(evidence["candidate_general"], "abaddon")
        self.assertEqual(evidence["opponent_general"], "apollyon")
        self.assertTrue(evidence["host_validation_unchanged"])
        self.assertFalse(evidence["world_mutated_before_host_validation"])
        self.assertFalse(evidence["training_performed"])
        self.assertFalse(evidence["weights_updated"])
        self.assertFalse(evidence["automatic_corpus_admission"])
        self.assertFalse(evidence["automatic_abaddon_policy_promotion"])

    def test_joint_decision_binds_legacy_host_acceptance(self):
        legacy = FakeLegacy()
        hooks = wrapper.AbaddonCandidateHooks(
            legacy,
            FakeRefiner,
            self.genome,
            self.binding,
        )
        hooks.install()
        try:
            legacy.append_jsonl(
                Path("unused"),
                {
                    "event": "joint_decision",
                    "round": 7,
                    "abaddon": {
                        "decision": {"action": {"tool": "advance"}},
                        "accepted": False,
                        "host_reason": "fixture reject",
                    },
                },
            )
        finally:
            hooks.restore()

        evidence = legacy.rows[0][wrapper.EVIDENCE_KEY]
        self.assertEqual(evidence["schema"], wrapper.ROUND_SCHEMA)
        self.assertEqual(evidence["round"], 7)
        self.assertFalse(evidence["legacy_host_accepted"])
        self.assertEqual(evidence["legacy_host_reason"], "fixture reject")
        self.assertTrue(evidence["host_validation_unchanged"])

    def test_candidate_file_and_semantic_digests_are_both_required(self):
        candidate = genome()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            raw = (
                json.dumps(candidate, sort_keys=True, separators=(",", ":"))
                + "\n"
            ).encode()
            path.write_bytes(raw)
            file_sha = hashlib.sha256(raw).hexdigest()
            loaded, binding = wrapper.load_candidate_genome(
                path,
                expected_file_sha256=file_sha,
                refiner=FakeRefiner,
            )
            self.assertEqual(loaded, candidate)
            self.assertEqual(binding["candidate_file_sha256"], file_sha)
            self.assertEqual(
                binding["candidate_genome_sha256"],
                candidate["genome_sha256"],
            )

            tampered = dict(candidate)
            tampered["genome_sha256"] = "0" * 64
            tampered_raw = (
                json.dumps(tampered, sort_keys=True, separators=(",", ":"))
                + "\n"
            ).encode()
            path.write_bytes(tampered_raw)
            with self.assertRaisesRegex(
                wrapper.WrapperError,
                "semantic digest mismatch",
            ):
                wrapper.load_candidate_genome(
                    path,
                    expected_file_sha256=hashlib.sha256(
                        tampered_raw
                    ).hexdigest(),
                    refiner=FakeRefiner,
                )

    def test_wrapper_arg_partition_preserves_legacy_args(self):
        namespace, remaining = wrapper.parse_wrapper_args(
            [
                "--abaddon-candidate-genome",
                "/tmp/candidate.json",
                "--expected-candidate-file-sha256",
                "a" * 64,
                "--seed",
                "2060",
                "--rounds",
                "72",
            ]
        )
        self.assertEqual(
            namespace.abaddon_candidate_genome,
            "/tmp/candidate.json",
        )
        self.assertEqual(
            namespace.expected_candidate_file_sha256,
            "a" * 64,
        )
        self.assertEqual(
            remaining,
            ["--seed", "2060", "--rounds", "72"],
        )

    def test_existing_general_brain_abaddon_training_gate_stays_fail_closed(self):
        result = classify_abaddon_from_apollyon_v22_pair({})
        self.assertEqual(result["general_id"], "abaddon")
        self.assertFalse(result["eligible"])
        self.assertEqual(
            result["reasons"],
            ["ABADDON_REQUIRES_SYMMETRIC_REVIEWED_CHALLENGER_EVIDENCE"],
        )
        self.assertFalse(result["automatic_corpus_admission"])
        self.assertFalse(result["automatic_weight_mutation"])
        self.assertFalse(result["automatic_promotion"])


if __name__ == "__main__":
    unittest.main()
