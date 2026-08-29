#!/usr/bin/env python3
from __future__ import annotations

import unittest

import darwin_evaluation_precommit_record_v1 as record_contract


class SplitTrap(str):
    """Fail if an over-cardinality vector reaches list materialization."""

    def split(self, *args: object, **kwargs: object) -> list[str]:
        raise AssertionError("over-cardinality CSV reached split()")


class PrecommitCsvCardinalityTests(unittest.TestCase):
    def test_concurrency_fifth_item_rejects_before_split(self) -> None:
        value = SplitTrap("1,2,4,8,1")
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"concurrency must contain at most 4 values",
        ):
            record_contract._parse_csv_positive_decimals(value, "concurrency", 8)

    def test_tick_batches_sixty_fifth_item_rejects_before_split(self) -> None:
        value = SplitTrap(",".join(str(index) for index in range(1, 66)))
        with self.assertRaisesRegex(
            record_contract.NumericArgumentError,
            r"tick_batches must contain at most 64 values",
        ):
            record_contract._parse_csv_positive_decimals(value, "tick_batches", 10_000)

    def test_exact_cardinality_boundaries_remain_parseable(self) -> None:
        self.assertEqual(
            record_contract._parse_csv_positive_decimals(
                "1,2,4,8", "concurrency", 8
            ),
            (1, 2, 4, 8),
        )
        tick_batches = record_contract._parse_csv_positive_decimals(
            ",".join(str(index) for index in range(1, 65)),
            "tick_batches",
            10_000,
        )
        self.assertEqual(tick_batches, tuple(range(1, 65)))


if __name__ == "__main__":
    unittest.main()
