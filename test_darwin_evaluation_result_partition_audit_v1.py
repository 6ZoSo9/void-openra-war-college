#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import unittest
from unittest import mock

import darwin_evaluation_precommit_record_v1 as record_contract
import darwin_evaluation_result_partition_audit_v1 as audit
import darwin_heldout_evaluation_split_v1 as split
import darwin_precommitted_evaluation_plan_v1 as plan_contract


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def fixture() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    manifest = split.build_manifest(
        "singles.oramap",
        [100, 101],
        [200, 201],
    )
    plan = plan_contract.build_precommitted_evaluation_plan(
        manifest,
        "a" * 40,
        100,
        200,
        [1, 2],
        [1, 8],
        2,
        2,
        "noop_control",
    )
    record = record_contract.build_record("darwin-audit-001", manifest, plan)
    runs: dict[str, object] = {}
    for partition, base_seed in (("calibration", 100), ("held_out", 200)):
        rows: list[dict[str, object]] = []
        for concurrency in (1, 2):
            for tick_batches in (1, 8):
                for sample_index in range(2):
                    for repetition_index in range(2):
                        for slot in range(concurrency):
                            seed = base_seed + slot
                            outcome_digest = sha256_text(
                                f"{partition}:{concurrency}:{tick_batches}:"
                                f"{sample_index}:{repetition_index}:{slot}:{seed}"
                            )
                            rows.append(
                                {
                                    "partition": partition,
                                    "concurrency": concurrency,
                                    "tick_batches": tick_batches,
                                    "sample_index": sample_index,
                                    "repetition_index": repetition_index,
                                    "slot": slot,
                                    "seed": seed,
                                    "outcome_digest": outcome_digest,
                                    "result_binding_sha256": audit.result_binding_sha256(
                                        partition=partition,
                                        concurrency=concurrency,
                                        tick_batches=tick_batches,
                                        sample_index=sample_index,
                                        repetition_index=repetition_index,
                                        slot=slot,
                                        seed=seed,
                                        outcome_digest=outcome_digest,
                                    ),
                                }
                            )
        runs[partition] = rows
    bundle = audit.build_result_bundle(record, manifest, runs)
    return manifest, record, bundle


class EvaluationResultPartitionAuditTests(unittest.TestCase):
    def assert_hold(
        self,
        bundle: dict[str, object],
        record: dict[str, object],
        manifest: dict[str, object],
        phrase: str,
    ) -> None:
        with self.assertRaisesRegex(audit.ResultAuditError, phrase):
            audit.audit_result_bundle(bundle, record, manifest)

    def test_exact_symmetric_result_bundle_is_green(self) -> None:
        manifest, record, bundle = fixture()
        result = audit.audit_result_bundle(bundle, record, manifest)
        self.assertEqual(result["status"], "GREEN")
        self.assertEqual(result["calibration_rows"], 24)
        self.assertEqual(result["held_out_rows"], 24)
        self.assertEqual(result["runtime_evidence"], "PENDING_DESIGNATED_HOST")
        self.assertEqual(result["trusted_runtime_producer_authentication"], "UNPROVEN")

    def test_missing_row_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        bundle["runs"]["held_out"].pop()
        self.assert_hold(bundle, record, manifest, "cardinality")

    def test_duplicate_row_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        rows = bundle["runs"]["calibration"]
        rows[-1] = copy.deepcopy(rows[0])
        self.assert_hold(bundle, record, manifest, "duplicate")

    def test_reordered_valid_rows_fail_closed_without_normalization(self) -> None:
        manifest, record, bundle = fixture()
        rows = bundle["runs"]["held_out"]
        rows[0], rows[1] = rows[1], rows[0]
        self.assert_hold(bundle, record, manifest, "noncanonical")

    def test_canonical_partition_validation_reuses_the_admitted_row_list(self) -> None:
        manifest, record, bundle = fixture()
        rows = bundle["runs"]["calibration"]
        verified_record = record_contract.validate_record(record, manifest)
        validated = audit._validate_partition_rows(
            verified_record, "calibration", rows
        )
        self.assertIs(validated, rows)

    def test_streaming_digest_matches_the_canonical_json_contract(self) -> None:
        value = {
            "ascii": ["z", "a", 7],
            "nested": {"unicode": "\u03bb", "flag": True},
        }
        expected = hashlib.sha256(
            record_contract.canonical_json(value).encode("utf-8")
        ).hexdigest()
        self.assertEqual(audit._sha256_json(value), expected)

    def test_full_bundle_audit_never_allocates_a_canonical_bundle_string(self) -> None:
        manifest, record, bundle = fixture()
        with mock.patch.object(
            audit,
            "canonical_json",
            side_effect=AssertionError("full canonical string allocation"),
        ):
            result = audit.audit_result_bundle(bundle, record, manifest)
        self.assertEqual(result["status"], "GREEN")
        self.assertEqual(result["calibration_rows"], 24)
        self.assertEqual(result["held_out_rows"], 24)

    def test_full_bundle_audit_hashes_the_validated_core_once(self) -> None:
        manifest, record, bundle = fixture()
        original_sha256_json = audit._sha256_json
        whole_bundle_inputs: list[dict[str, object]] = []

        def tracked_sha256_json(value: object) -> str:
            if type(value) is dict and "runs" in value:
                whole_bundle_inputs.append(value)
            return original_sha256_json(value)

        with mock.patch.object(
            audit,
            "_sha256_json",
            side_effect=tracked_sha256_json,
        ):
            result = audit.audit_result_bundle(bundle, record, manifest)
        self.assertEqual(result["status"], "GREEN")
        self.assertEqual(len(whole_bundle_inputs), 1)
        self.assertNotIn("result_digest", whole_bundle_inputs[0])

    def test_scalar_provenance_fails_before_result_row_traversal(self) -> None:
        manifest, record, bundle = fixture()
        bundle["engine_frozen_commit"] = "f" * 40
        with mock.patch.object(
            audit,
            "_validate_partition_rows",
            side_effect=AssertionError("invalid provenance reached result rows"),
        ):
            self.assert_hold(bundle, record, manifest, "differs from precommit")

    def test_late_partition_type_fails_before_any_row_traversal(self) -> None:
        manifest, record, bundle = fixture()
        bundle["runs"]["held_out"] = tuple(bundle["runs"]["held_out"])
        with mock.patch.object(
            audit,
            "_validate_partition_rows",
            side_effect=AssertionError("invalid container reached result rows"),
        ):
            self.assert_hold(bundle, record, manifest, "held_out rows must be an exact list")

    def test_late_partition_cardinality_fails_before_any_row_traversal(self) -> None:
        manifest, record, bundle = fixture()
        bundle["runs"]["held_out"].pop()
        with mock.patch.object(
            audit,
            "_validate_partition_rows",
            side_effect=AssertionError("invalid cardinality reached result rows"),
        ):
            self.assert_hold(bundle, record, manifest, "held_out row cardinality")

    def test_scalar_provenance_requires_exact_value_and_type(self) -> None:
        manifest, record, bundle = fixture()
        mutations: tuple[tuple[str, object], ...] = (
            ("schema_version", True),
            ("engine_frozen_commit", "f" * 40),
            ("generation", "darwin-audit-other-generation"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                mutated = copy.deepcopy(bundle)
                mutated[field] = value
                self.assert_hold(mutated, record, manifest, "differs from precommit")

    def test_cross_partition_relabel_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        row = bundle["runs"]["held_out"][0]
        row["partition"] = "calibration"
        self.assert_hold(bundle, record, manifest, "cross-partition")

    def test_cross_partition_outcome_swap_fails_binding(self) -> None:
        manifest, record, bundle = fixture()
        calibration = bundle["runs"]["calibration"][0]
        held_out = bundle["runs"]["held_out"][0]
        calibration["outcome_digest"], held_out["outcome_digest"] = (
            held_out["outcome_digest"],
            calibration["outcome_digest"],
        )
        self.assert_hold(bundle, record, manifest, "not bound")

    def test_seed_outside_precommitted_window_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        bundle["runs"]["held_out"][0]["seed"] = 100
        self.assert_hold(bundle, record, manifest, "outside")

    def test_result_schema_extension_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        bundle["runs"]["calibration"][0]["promotion"] = True
        self.assert_hold(bundle, record, manifest, "schema-exact")

    def test_precommit_record_substitution_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        other_plan = copy.deepcopy(record["plan"])
        other_plan["shared_parameters"]["workload_profile"] = "stop_owned_unit"
        other_plan_core = {
            key: value for key, value in other_plan.items() if key != "plan_digest"
        }
        other_plan["plan_digest"] = plan_contract._sha256_json(other_plan_core)
        other_record = record_contract.build_record("darwin-audit-002", manifest, other_plan)
        self.assert_hold(bundle, other_record, manifest, "differs from precommit")

    def test_bundle_digest_mutation_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        bundle["result_digest"] = "0" * 64
        self.assert_hold(bundle, record, manifest, "differs from precommit")

    def test_bundle_schema_extension_fails_closed(self) -> None:
        manifest, record, bundle = fixture()
        bundle["automatic_promotion"] = True
        self.assert_hold(bundle, record, manifest, "schema-exact")

    def test_maximum_plan_cardinality_is_counted_without_row_materialization(self) -> None:
        manifest = split.build_manifest(
            "singles.oramap",
            list(range(100, 108)),
            list(range(200, 208)),
        )
        plan = plan_contract.build_precommitted_evaluation_plan(
            manifest,
            "b" * 40,
            100,
            200,
            [1, 2, 4, 8],
            list(range(1, 17)),
            1_000,
            10,
            "noop_control",
        )
        record = record_contract.build_record("darwin-audit-max", manifest, plan)
        self.assertEqual(
            audit.expected_result_row_count(record, manifest, "held_out"),
            2_400_000,
        )


if __name__ == "__main__":
    unittest.main()
