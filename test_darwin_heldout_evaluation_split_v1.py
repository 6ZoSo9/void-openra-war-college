from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

import darwin_heldout_evaluation_split_v1 as split


class HeldOutEvaluationSplitTests(unittest.TestCase):
    def manifest(self):
        return split.build_manifest(
            "singles.oramap",
            (2050, 2051, 2052),
            (12050, 12051, 12052),
        )

    def test_manifest_is_content_addressed_and_stable(self):
        manifest = self.manifest()
        core = dict(manifest)
        digest = core.pop("split_digest")
        expected = hashlib.sha256(split.canonical_json(core).encode("utf-8")).hexdigest()
        self.assertEqual(digest, expected)
        self.assertEqual(split.validate_manifest(manifest), manifest)

    def test_overlap_falsifier_rejects_relabelled_calibration_seed(self):
        with self.assertRaisesRegex(split.SplitError, "overlap"):
            split.build_manifest("singles.oramap", (2050, 2051), (2051, 12050))

    def test_binding_cannot_relabel_calibration_seed_as_held_out(self):
        manifest = self.manifest()
        with self.assertRaisesRegex(split.SplitError, "not admitted"):
            split.bind_evaluation_seed(manifest, "held_out", 2050)

    def test_held_out_binding_is_digest_and_partition_bound(self):
        manifest = self.manifest()
        binding = split.bind_evaluation_seed(manifest, "held_out", 12050)
        self.assertEqual(binding["split_digest"], manifest["split_digest"])
        self.assertEqual(binding["partition"], "held_out")
        self.assertEqual(binding["seed"], 12050)
        self.assertEqual(binding["generalization_claim_authority"], "HELD_OUT_EVIDENCE_ONLY")
        self.assertEqual(binding["runtime_evidence"], "PENDING_DESIGNATED_HOST")

    def test_calibration_binding_grants_no_generalization_claim(self):
        manifest = self.manifest()
        binding = split.bind_evaluation_seed(manifest, "calibration", 2050)
        self.assertEqual(binding["generalization_claim_authority"], "NONE")

    def test_tampered_manifest_is_rejected_even_with_original_digest(self):
        manifest = self.manifest()
        tampered = copy.deepcopy(manifest)
        tampered["partitions"]["held_out"][2] = 12053
        with self.assertRaisesRegex(split.SplitError, "canonical"):
            split.validate_manifest(tampered)

    def test_duplicate_unsorted_and_noncanonical_seed_inputs_fail_closed(self):
        with self.assertRaisesRegex(split.SplitError, "duplicate"):
            split.build_manifest("singles.oramap", (2050, 2050), (12050,))
        with self.assertRaisesRegex(split.SplitError, "ascending"):
            split.build_manifest("singles.oramap", (2051, 2050), (12050,))
        with self.assertRaisesRegex(split.SplitError, "non-canonical"):
            split.parse_seed_set("02050,12050")

    def test_runtime_random_seed_sentinel_cannot_enter_evaluation_partitions(self):
        with self.assertRaisesRegex(split.SplitError, "reserved"):
            split.build_manifest("singles.oramap", (0,), (12050,))
        with self.assertRaisesRegex(split.SplitError, "reserved"):
            split.build_manifest("singles.oramap", (2050,), (0,))
        with self.assertRaisesRegex(split.SplitError, "non-canonical deterministic"):
            split.parse_seed_set("0")

    def test_deterministic_seed_domain_preserves_signed_int32_upper_bound(self):
        manifest = split.build_manifest(
            "singles.oramap",
            (split.MIN_DETERMINISTIC_RUNTIME_SEED,),
            (split.MAX_RUNTIME_SEED,),
        )
        binding = split.bind_evaluation_seed(
            manifest, "held_out", split.MAX_RUNTIME_SEED
        )
        self.assertEqual(binding["seed"], split.MAX_RUNTIME_SEED)
        self.assertEqual(manifest["split_policy"]["runtime_random_seed_sentinel"], 0)
        self.assertEqual(manifest["split_policy"]["deterministic_runtime_seed_min"], 1)
        self.assertEqual(
            manifest["split_policy"]["deterministic_runtime_seed_max"],
            split.MAX_RUNTIME_SEED,
        )

    def test_split_change_changes_digest(self):
        left = self.manifest()
        right = split.build_manifest(
            "singles.oramap",
            (2050, 2051, 2052),
            (12050, 12051, 12053),
        )
        self.assertNotEqual(left["split_digest"], right["split_digest"])

    def test_comparison_points_and_generation_are_exact(self):
        manifest = self.manifest()
        self.assertEqual(
            manifest["engine_frozen_commit"],
            "1607a7a6501d42a47638393ecef8b22831064932",
        )
        self.assertEqual(
            manifest["war_college_comparison_point"],
            "973802ef0a614e5afa782ff20e231e18966ae3e5",
        )
        self.assertEqual(manifest["generation"], "ad1926569b12466c")

    def test_cli_emits_one_manifest_and_no_runtime_claim(self):
        source = Path(split.__file__).resolve()
        result = subprocess.run(
            [
                sys.executable,
                str(source),
                "--map",
                "singles.oramap",
                "--calibration-seeds",
                "2050,2051",
                "--held-out-seeds",
                "12050,12051",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(result.stdout.strip().splitlines()), 1)
        manifest = json.loads(result.stdout)
        self.assertEqual(split.validate_manifest(manifest), manifest)
        self.assertEqual(manifest["split_policy"]["runtime_execution_authority"], "NONE")
        self.assertEqual(
            manifest["split_policy"]["automatic_promotion_authority"], "NONE"
        )


if __name__ == "__main__":
    unittest.main()
