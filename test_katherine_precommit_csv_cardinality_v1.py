#!/usr/bin/env python3
from __future__ import annotations

import unittest
from unittest import mock

import darwin_evaluation_precommit_record_v1 as record_contract


class SplitTrap(str):
    """Fail if a rejected vector reaches token materialization."""

    def count(self, *args: object, **kwargs: object) -> int:
        raise AssertionError("over-bound CSV reached count()")

    def split(self, *args: object, **kwargs: object) -> list[str]:
        raise AssertionError("over-bound CSV reached split()")


class RegexTrap:
    """Fail if an over-domain scalar reaches regular-expression scanning."""

    def fullmatch(self, value: object) -> object:
        raise AssertionError(f"over-domain scalar reached regex: {type(value).__name__}")


class PrecommitCsvCardinalityTests(unittest.TestCase):
    def test_concurrency_fifth_item_rejects_before_split(self) -> None:
        value = "1,2,4,8,1"
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"concurrency must be in 1..8, contain at most 4 values, "
            r"and contain at most 7 characters",
        ):
            record_contract._parse_csv_positive_decimals(value, "concurrency", 8)

    def test_tick_batches_sixty_fifth_item_rejects_before_split(self) -> None:
        value = ",".join(str(index) for index in range(1, 66))
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"tick_batches must contain at most 64 values",
        ):
            record_contract._parse_csv_positive_decimals(value, "tick_batches", 10_000)

    def test_overlength_concurrency_rejects_before_count_or_split(self) -> None:
        value = SplitTrap("1" * 8)
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"concurrency must be in 1..8, contain at most 4 values, "
            r"and contain at most 7 characters",
        ):
            record_contract._parse_csv_positive_decimals(value, "concurrency", 8)

    def test_overlength_tick_batches_rejects_before_count_or_split(self) -> None:
        value = SplitTrap("1" * 384)
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"tick_batches must be in 1..10000, contain at most 64 values, "
            r"and contain at most 383 characters",
        ):
            record_contract._parse_csv_positive_decimals(value, "tick_batches", 10_000)

    def test_every_scalar_field_binds_its_exact_numeric_boundary(self) -> None:
        cases = (
            ("calibration_base_seed", record_contract.split.MAX_RUNTIME_SEED),
            ("held_out_base_seed", record_contract.split.MAX_RUNTIME_SEED),
            ("samples", record_contract.plan_contract.MAX_SAMPLES),
            ("repetitions", record_contract.plan_contract.MAX_REPETITIONS),
        )
        for label, maximum in cases:
            with self.subTest(label=label, boundary="maximum"):
                self.assertEqual(
                    record_contract._parse_positive_decimal(
                        str(maximum),
                        label,
                        maximum,
                    ),
                    maximum,
                )
            with self.subTest(label=label, boundary="maximum_plus_one"):
                with self.assertRaisesRegex(
                    record_contract.NumericArgumentError,
                    rf"{label} must be in 1\.\.{maximum}",
                ):
                    record_contract._parse_positive_decimal(
                        str(maximum + 1),
                        label,
                        maximum,
                    )

    def test_every_overlength_scalar_rejects_before_regex(self) -> None:
        cases = (
            ("calibration_base_seed", record_contract.split.MAX_RUNTIME_SEED),
            ("held_out_base_seed", record_contract.split.MAX_RUNTIME_SEED),
            ("samples", record_contract.plan_contract.MAX_SAMPLES),
            ("repetitions", record_contract.plan_contract.MAX_REPETITIONS),
        )
        with mock.patch.object(record_contract, "POSITIVE_DECIMAL_RE", RegexTrap()):
            for label, maximum in cases:
                with self.subTest(label=label):
                    with self.assertRaisesRegex(
                        record_contract.NumericArgumentError,
                        rf"{label} must be in 1\.\.{maximum}",
                    ):
                        record_contract._parse_positive_decimal(
                            "9" * (len(str(maximum)) + 1),
                            label,
                            maximum,
                        )

    def test_exact_cardinality_and_character_boundaries_remain_parseable(self) -> None:
        self.assertEqual(
            record_contract._parse_csv_positive_decimals(
                "1,2,4,8", "concurrency", 8
            ),
            (1, 2, 4, 8),
        )
        tick_boundary = ",".join(["10000"] * 64)
        self.assertEqual(len(tick_boundary), 383)
        self.assertEqual(
            record_contract._parse_csv_positive_decimals(
                tick_boundary,
                "tick_batches",
                10_000,
            ),
            (10_000,) * 64,
        )
        self.assertEqual(
            record_contract._parse_positive_decimal(
                "4294967295",
                "seed",
                4_294_967_295,
            ),
            4_294_967_295,
        )

    def test_unknown_csv_label_rejects_before_count_or_split(self) -> None:
        value = SplitTrap("1")
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"future has no bounded CSV cardinality contract",
        ):
            record_contract._parse_csv_positive_decimals(value, "future", 8)


if __name__ == "__main__":
    unittest.main()
