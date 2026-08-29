from __future__ import annotations

import copy
import unittest

import darwin_benchmark_evaluation_partition_binding_v1 as benchmark_binding
import darwin_heldout_evaluation_split_v1 as split


class BenchmarkEvaluationPartitionBindingTests(unittest.TestCase):
    def manifest(self):
        return split.build_manifest(
            "singles.oramap",
            tuple(range(2050, 2058)),
            tuple(range(12050, 12058)),
        )

    def test_held_out_concurrency_eight_binds_complete_slot_window(self):
        manifest = self.manifest()
        binding = benchmark_binding.bind_benchmark_seed_window(
            manifest, "held_out", 12050, 8
        )
        self.assertEqual(binding["split_digest"], manifest["split_digest"])
        self.assertEqual(binding["partition"], "held_out")
        self.assertEqual(binding["benchmark_seed_rule"], "parameters.seed + slot")
        self.assertEqual(binding["base_seed"], 12050)
        self.assertEqual(binding["concurrency"], 8)
        self.assertEqual(
            binding["slot_bindings"],
            [{"slot": slot, "seed": 12050 + slot} for slot in range(8)],
        )
        self.assertEqual(
            binding["generalization_claim_authority"], "HELD_OUT_EVIDENCE_ONLY"
        )
        self.assertEqual(binding["runtime_evidence"], "PENDING_DESIGNATED_HOST")

    def test_calibration_window_grants_no_generalization_claim(self):
        binding = benchmark_binding.bind_benchmark_seed_window(
            self.manifest(), "calibration", 2050, 4
        )
        self.assertEqual(binding["generalization_claim_authority"], "NONE")
        self.assertEqual(binding["slot_bindings"][-1]["seed"], 2053)

    def test_base_seed_only_is_not_enough_for_held_out_claim(self):
        manifest = split.build_manifest(
            "singles.oramap",
            (2050, 2051, 2052, 2053),
            (12050, 12051, 12052),
        )
        with self.assertRaisesRegex(
            split.SplitError, "escapes held_out at slot 3 seed 12053"
        ):
            benchmark_binding.bind_benchmark_seed_window(
                manifest, "held_out", 12050, 4
            )

    def test_calibration_seed_cannot_be_relabelled_by_window_binding(self):
        with self.assertRaisesRegex(
            split.SplitError, "escapes held_out at slot 0 seed 2050"
        ):
            benchmark_binding.bind_benchmark_seed_window(
                self.manifest(), "held_out", 2050, 1
            )

    def test_random_seed_sentinel_cannot_bind_held_out_benchmark_window(self):
        with self.assertRaisesRegex(split.SplitError, "reserved"):
            benchmark_binding.bind_benchmark_seed_window(
                self.manifest(), "held_out", 0, 1
            )

    def test_concurrency_must_match_live_joint_advance_matrix_domain(self):
        for bad in (True, 0, 3, 16, 1.0, "8"):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(split.SplitError, "concurrency"):
                    benchmark_binding.bind_benchmark_seed_window(
                        self.manifest(), "held_out", 12050, bad
                    )

    def test_seed_window_overflow_fails_before_partition_attribution(self):
        manifest = split.build_manifest(
            "singles.oramap",
            (1, 2, 3, 4),
            (split.MAX_RUNTIME_SEED - 1, split.MAX_RUNTIME_SEED),
        )
        with self.assertRaisesRegex(split.SplitError, "exceeds"):
            benchmark_binding.bind_benchmark_seed_window(
                manifest, "held_out", split.MAX_RUNTIME_SEED - 1, 4
            )

    def test_tampered_split_manifest_cannot_bind_benchmark_window(self):
        manifest = self.manifest()
        tampered = copy.deepcopy(manifest)
        tampered["partitions"]["held_out"][-1] = 12099
        with self.assertRaisesRegex(split.SplitError, "canonical"):
            benchmark_binding.bind_benchmark_seed_window(
                tampered, "held_out", 12050, 8
            )

    def test_binding_preserves_protected_comparison_points_and_no_authority(self):
        binding = benchmark_binding.bind_benchmark_seed_window(
            self.manifest(), "held_out", 12050, 2
        )
        self.assertEqual(
            binding["engine_frozen_commit"],
            "1607a7a6501d42a47638393ecef8b22831064932",
        )
        self.assertEqual(
            binding["war_college_comparison_point"],
            "973802ef0a614e5afa782ff20e231e18966ae3e5",
        )
        self.assertEqual(binding["generation"], "ad1926569b12466c")
        self.assertEqual(binding["runtime_execution_authority"], "NONE")
        self.assertEqual(binding["model_weight_mutation_authority"], "NONE")
        self.assertEqual(binding["automatic_promotion_authority"], "NONE")


if __name__ == "__main__":
    unittest.main()
