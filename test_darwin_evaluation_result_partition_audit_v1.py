#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import unittest

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
