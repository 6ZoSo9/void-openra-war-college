#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

import darwin_heldout_evaluation_split_v1 as split
import darwin_precommitted_evaluation_plan_v1 as plan


class PrecommittedEvaluationPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = split.build_manifest(
            "singles.oramap",
            tuple(range(1000, 1008)),
            tuple(range(2000, 2008)),
        )
        self.source_sha = "a" * 40

    def build(self, **overrides: object) -> dict[str, object]:
        parameters: dict[str, object] = {
            "manifest": self.manifest,
            "benchmark_source_sha": self.source_sha,
            "calibration_base_seed": 1000,
            "held_out_base_seed": 2000,
            "concurrency": (1, 4),
            "tick_batches": (1, 8),
            "samples": 2,
            "repetitions": 2,
            "workload_profile": "noop_control",
        }
        parameters.update(overrides)
        return plan.build_precommitted_evaluation_plan(**parameters)

    def test_stable_plan_validates_against_precommitted_digest(self) -> None:
        candidate = self.build()
        validated = plan.validate_precommitted_evaluation_plan(
            candidate, self.manifest, candidate["plan_digest"]
        )
        self.assertEqual(validated, candidate)
        self.assertEqual(
            validated["shared_parameters"]["benchmark_schema_version"], 9
        )
        self.assertEqual(
            validated["shared_parameters"]["benchmark_seed_rule"],
            "parameters.seed + slot",
        )
        self.assertEqual(
            [row["concurrency"] for row in validated["partition_runs"]["held_out"]["window_bindings"]],
            [1, 4],
        )

    def test_incomplete_held_out_seed_window_fails_closed(self) -> None:
        incomplete = split.build_manifest(
            "singles.oramap",
            tuple(range(1000, 1008)),
            (2000, 2001, 2002),
        )
        with self.assertRaisesRegex(split.SplitError, r"slot 3 seed 2003"):
            self.build(
                manifest=incomplete,
                concurrency=(4,),
                held_out_base_seed=2000,
            )

    def test_posthoc_tick_batch_selection_changes_digest_and_is_rejected(self) -> None:
        committed = self.build()
        altered = self.build(tick_batches=(1, 16))
        self.assertNotEqual(committed["plan_digest"], altered["plan_digest"])
        with self.assertRaisesRegex(split.SplitError, "precommitted digest"):
            plan.validate_precommitted_evaluation_plan(
                altered, self.manifest, committed["plan_digest"]
            )

    def test_posthoc_benchmark_source_generation_changes_digest_and_is_rejected(self) -> None:
        committed = self.build()
        altered = self.build(benchmark_source_sha="b" * 40)
        self.assertNotEqual(committed["plan_digest"], altered["plan_digest"])
        with self.assertRaisesRegex(split.SplitError, "precommitted digest"):
            plan.validate_precommitted_evaluation_plan(
                altered, self.manifest, committed["plan_digest"]
            )

    def test_calibration_seed_cannot_be_relabelled_as_held_out(self) -> None:
        with self.assertRaisesRegex(split.SplitError, "escapes held_out"):
            self.build(held_out_base_seed=1000, concurrency=(1,))

    def test_random_runtime_seed_zero_cannot_obtain_plan_authority(self) -> None:
        with self.assertRaisesRegex(split.SplitError, "runtime random-seed sentinel"):
            self.build(held_out_base_seed=0, concurrency=(1,))

    def test_matrix_parameters_must_be_canonical(self) -> None:
        with self.assertRaisesRegex(split.SplitError, "strictly ascending"):
            self.build(concurrency=(4, 1))
        with self.assertRaisesRegex(split.SplitError, "strictly ascending"):
            self.build(tick_batches=(8, 1))

    def test_authority_policy_or_manifest_tamper_cannot_validate(self) -> None:
        committed = self.build()
        tampered = copy.deepcopy(committed)
        tampered["evaluation_policy"]["automatic_promotion_authority"] = "ALLOW"
        with self.assertRaises(split.SplitError):
            plan.validate_precommitted_evaluation_plan(
                tampered, self.manifest, committed["plan_digest"]
            )

        changed_manifest = split.build_manifest(
            "singles.oramap",
            tuple(range(1000, 1008)),
            tuple(range(3000, 3008)),
        )
        with self.assertRaises(split.SplitError):
            plan.validate_precommitted_evaluation_plan(
                committed, changed_manifest, committed["plan_digest"]
            )

        self.assertIs(
            committed["evaluation_policy"]["shared_parameters_across_partitions"], True
        )
        self.assertIs(
            committed["evaluation_policy"]["posthoc_heldout_parameter_selection"], False
        )
        for field in (
            "runtime_execution_authority",
            "model_weight_mutation_authority",
            "corpus_admission_authority",
            "automatic_promotion_authority",
        ):
            self.assertEqual(committed["evaluation_policy"][field], "NONE")


if __name__ == "__main__":
    unittest.main()
