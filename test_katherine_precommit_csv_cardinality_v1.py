#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import unittest
from unittest import mock

import darwin_evaluation_precommit_record_recovery_v1 as recovery
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
                    record_contract._parse_positive_decimal(str(maximum), label, maximum),
                    maximum,
                )
            with self.subTest(label=label, boundary="maximum_plus_one"):
                with self.assertRaisesRegex(
                    record_contract.NumericArgumentError,
                    rf"{label} must be in 1\.\.{maximum}",
                ):
                    record_contract._parse_positive_decimal(
                        str(maximum + 1), label, maximum
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
                            "9" * (len(str(maximum)) + 1), label, maximum
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
                tick_boundary, "tick_batches", 10_000
            ),
            (10_000,) * 64,
        )
        self.assertEqual(
            record_contract._parse_positive_decimal(
                "4294967295", "seed", 4_294_967_295
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


class HostileToken:
    """Fail if admission invokes any token behavior."""

    def __eq__(self, other: object) -> bool:
        raise AssertionError("hostile token equality executed")

    def __getattribute__(self, name: str) -> object:
        if name in {"startswith", "split", "encode", "__len__"}:
            raise AssertionError(f"hostile token behavior executed: {name}")
        return object.__getattribute__(self, name)


class OverflowThenTrap:
    """Yield forever, but fail loudly after the first over-bound token."""

    def __init__(self) -> None:
        self.consumed = 0

    def __iter__(self) -> "OverflowThenTrap":
        return self

    def __next__(self) -> str:
        self.consumed += 1
        if self.consumed > record_contract.MAX_ARGV_TOKENS + 1:
            raise AssertionError("argv collector consumed beyond the first overflow token")
        return f"--future-{self.consumed}"


class PrecommitArgvCardinalityTests(unittest.TestCase):
    @staticmethod
    def maximum_shape() -> list[str]:
        tokens = ["record"]
        for index in range(13):
            tokens.extend((f"--future-{index}", "value"))
        if len(tokens) != record_contract.MAX_ARGV_TOKENS:
            raise AssertionError("test fixture no longer matches the maximum CLI grammar")
        return tokens

    def run_cli(self, module: object, argv: object) -> dict[str, object]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(record_contract, "_bounded_read_json") as bounded_read:
            with mock.patch.object(recovery, "_load_manifest") as load_manifest:
                with mock.patch.object(record_contract.os, "open") as open_file:
                    with mock.patch.object(record_contract.os, "fsync") as fsync_file:
                        with contextlib.redirect_stdout(stdout):
                            with contextlib.redirect_stderr(stderr):
                                return_code = module.main(argv)

        self.assertEqual(return_code, 2)
        self.assertEqual(stdout.getvalue(), "")
        lines = stderr.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        terminal = json.loads(lines[0])
        self.assertEqual(terminal["status"], "HOLD")
        self.assertEqual(terminal["reason_code"], "ARGUMENT_ERROR")
        bounded_read.assert_not_called()
        load_manifest.assert_not_called()
        open_file.assert_not_called()
        fsync_file.assert_not_called()
        return terminal

    def test_exact_maximum_token_control_reaches_parser_in_both_clis(self) -> None:
        argv = self.maximum_shape()
        self.assertEqual(record_contract._bounded_argv_tokens(iter(argv)), argv)
        for module in (record_contract, recovery):
            with self.subTest(module=module.__name__):
                terminal = self.run_cli(module, iter(argv))
                self.assertNotIn(
                    f"at most {record_contract.MAX_ARGV_TOKENS} tokens",
                    terminal["reason"],
                )

    def test_first_overflow_token_rejects_before_parser_or_io_in_both_clis(self) -> None:
        argv = [*self.maximum_shape(), "--overflow"]
        self.assertEqual(len(argv), record_contract.MAX_ARGV_TOKENS + 1)
        for module in (record_contract, recovery):
            with self.subTest(module=module.__name__):
                terminal = self.run_cli(module, iter(argv))
                self.assertEqual(
                    terminal["reason"],
                    f"argv must contain at most {record_contract.MAX_ARGV_TOKENS} tokens",
                )

    def test_infinite_iterable_stops_at_first_overflow_in_both_clis(self) -> None:
        for module in (record_contract, recovery):
            with self.subTest(module=module.__name__):
                stream = OverflowThenTrap()
                terminal = self.run_cli(module, stream)
                self.assertEqual(
                    stream.consumed,
                    record_contract.MAX_ARGV_TOKENS + 1,
                )
                self.assertEqual(
                    terminal["reason"],
                    f"argv must contain at most {record_contract.MAX_ARGV_TOKENS} tokens",
                )


    def test_non_string_token_one_fails_closed_before_scanner_or_io(self) -> None:
        for token in (object(), b"--manifest", HostileToken()):
            for module in (record_contract, recovery):
                with self.subTest(
                    token_type=type(token).__name__,
                    module=module.__name__,
                ):
                    terminal = self.run_cli(module, [token])
                    self.assertEqual(
                        terminal["reason"],
                        "argv token 1 must be an exact built-in string",
                    )

    def test_hostile_first_overflow_token_is_never_inspected(self) -> None:
        argv: list[object] = [*self.maximum_shape(), HostileToken()]
        for module in (record_contract, recovery):
            with self.subTest(module=module.__name__):
                terminal = self.run_cli(module, argv)
                self.assertEqual(
                    terminal["reason"],
                    f"argv must contain at most {record_contract.MAX_ARGV_TOKENS} tokens",
                )

    def test_over_character_domain_rejects_every_token_role_before_io(self) -> None:
        over = "x" * (record_contract.MAX_ARGV_TOKEN_CHARS + 1)
        cases = {
            "option": [f"--{over}"],
            "positional": [over],
            "manifest_path": ["validate", "--manifest", over],
            "record_path": ["validate", "--record", over],
            "value": ["record", "--record-id", over],
        }
        for role, argv in cases.items():
            for module in (record_contract, recovery):
                with self.subTest(role=role, module=module.__name__):
                    terminal = self.run_cli(module, argv)
                    token_number = next(
                        index
                        for index, token in enumerate(argv, start=1)
                        if len(token) > record_contract.MAX_ARGV_TOKEN_CHARS
                    )
                    self.assertEqual(
                        terminal["reason"],
                        f"argv token {token_number} must contain at most "
                        f"{record_contract.MAX_ARGV_TOKEN_CHARS} characters",
                    )

    def test_multibyte_token_rejects_at_utf8_byte_wall(self) -> None:
        token = "é" * ((record_contract.MAX_ARGV_TOKEN_UTF8_BYTES // 2) + 1)
        self.assertLessEqual(len(token), record_contract.MAX_ARGV_TOKEN_CHARS)
        for module in (record_contract, recovery):
            with self.subTest(module=module.__name__):
                terminal = self.run_cli(module, [token])
                self.assertEqual(
                    terminal["reason"],
                    f"argv token 1 must contain at most "
                    f"{record_contract.MAX_ARGV_TOKEN_UTF8_BYTES} UTF-8 bytes",
                )

    def test_nul_and_non_utf8_text_fail_closed_before_io(self) -> None:
        cases = (
            ("nul", "validate\x00"),
            ("surrogate", "\ud800"),
        )
        for label, token in cases:
            for module in (record_contract, recovery):
                with self.subTest(label=label, module=module.__name__):
                    terminal = self.run_cli(module, [token])
                    if label == "nul":
                        self.assertEqual(
                            terminal["reason"],
                            "argv token 1 must not contain NUL",
                        )
                    else:
                        self.assertEqual(
                            terminal["reason"],
                            "argv token 1 must be valid UTF-8 text",
                        )

    def test_exact_character_and_utf8_byte_boundaries_are_admitted(self) -> None:
        ascii_boundary = "x" * record_contract.MAX_ARGV_TOKEN_CHARS
        utf8_boundary = "é" * (record_contract.MAX_ARGV_TOKEN_UTF8_BYTES // 2)
        self.assertEqual(
            record_contract._bounded_argv_tokens([ascii_boundary]),
            [ascii_boundary],
        )
        self.assertEqual(
            record_contract._bounded_argv_tokens([utf8_boundary]),
            [utf8_boundary],
        )


if __name__ == "__main__":
    unittest.main()
