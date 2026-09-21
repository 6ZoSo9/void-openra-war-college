from __future__ import annotations

import errno

import pytest

from openra_env.learning.openbw_s1_vx4_compatibility_v1 import (
    AssetOpenResult,
    CANONICAL_VX4_RECORD_BYTES,
    CLASSIC_VX4_RECORD_BYTES,
    Vx4FormatError,
    Vx4OpenError,
    canonicalize_classic_vx4,
    canonicalize_vx4ex,
    decode_canonical_words,
    modern_vx4ex_name,
    reference_metrics,
    resolve_asset,
)


def _u32_record(values: list[int]) -> bytes:
    assert len(values) == 16
    return b"".join(value.to_bytes(4, "little") for value in values)


def _u16_record(values: list[int]) -> bytes:
    assert len(values) == 16
    return b"".join(value.to_bytes(2, "little") for value in values)


def test_modern_name_preserves_request_and_adds_ex_suffix():
    assert modern_vx4ex_name("Tileset/badlands.vx4") == "Tileset/badlands.vx4ex"
    assert modern_vx4ex_name("TileSet/Ice.VX4") == "TileSet/Ice.VX4ex"


def test_modern_vx4ex_is_already_canonical_u32():
    values = [0, 1, 2, 3, 65534, 65535, 65536, 94988] + list(range(8))
    payload = _u32_record(values)
    assert len(payload) == CANONICAL_VX4_RECORD_BYTES
    assert canonicalize_vx4ex(payload) == payload
    assert decode_canonical_words(payload) == tuple(values)


def test_classic_vx4_expands_each_little_endian_u16_to_u32():
    values = [0, 1, 2, 3, 32767, 32768, 65534, 65535] + list(range(8))
    classic = _u16_record(values)
    canonical = canonicalize_classic_vx4(classic)
    assert len(classic) == CLASSIC_VX4_RECORD_BYTES
    assert len(canonical) == CANONICAL_VX4_RECORD_BYTES
    assert decode_canonical_words(canonical) == tuple(values)


def test_modern_badlands_high_value_is_not_truncated_to_u16():
    payload = _u32_record([94988] + [0] * 15)
    words = decode_canonical_words(canonicalize_vx4ex(payload))
    assert words[0] == 94988
    assert words[0] > 65535
    assert words[0] // 2 == 47494


def test_low_bit_flip_and_divide_by_two_index_semantics_are_preserved():
    payload = _u32_record([0, 1, 2, 3, 94988, 94989] + [0] * 10)
    metrics = reference_metrics(payload, vr4_record_count=47495)
    assert metrics["max_raw_entry"] == 94989
    assert metrics["max_vr4_id"] == 47494
    assert metrics["flip_entry_count"] == 3
    assert metrics["invalid_vr4_reference_count"] == 0
    assert metrics["all_references_valid"] is True


def test_reference_range_rejects_one_past_final_vr4_record():
    payload = _u32_record([94990] + [0] * 15)
    metrics = reference_metrics(payload, vr4_record_count=47495)
    assert metrics["max_vr4_id"] == 47495
    assert metrics["invalid_vr4_reference_count"] == 1
    assert metrics["all_references_valid"] is False


def test_modern_vx4ex_malformed_length_is_rejected():
    with pytest.raises(Vx4FormatError):
        canonicalize_vx4ex(b"\0" * (CANONICAL_VX4_RECORD_BYTES - 1))


def test_classic_vx4_malformed_length_is_rejected():
    with pytest.raises(Vx4FormatError):
        canonicalize_classic_vx4(b"\0" * (CLASSIC_VX4_RECORD_BYTES - 1))


def test_resolver_prefers_modern_vx4ex_without_touching_classic():
    calls: list[str] = []
    modern_payload = _u32_record([94988] + [0] * 15)

    def opener(name: str) -> AssetOpenResult:
        calls.append(name)
        if name.endswith(".vx4ex"):
            return AssetOpenResult(modern_payload)
        raise AssertionError("classic fallback must not be attempted")

    resolved = resolve_asset("Tileset/badlands.vx4", opener)
    assert calls == ["Tileset/badlands.vx4ex"]
    assert resolved.opened_name == "Tileset/badlands.vx4ex"
    assert resolved.source_format == "vx4ex"
    assert resolved.payload == modern_payload


def test_resolver_falls_back_to_classic_only_on_exact_enoent():
    calls: list[str] = []
    classic_payload = _u16_record([65535] + [0] * 15)

    def opener(name: str) -> AssetOpenResult:
        calls.append(name)
        if name.endswith(".vx4ex"):
            return AssetOpenResult(None, errno.ENOENT)
        return AssetOpenResult(classic_payload)

    resolved = resolve_asset("Tileset/badlands.vx4", opener)
    assert calls == ["Tileset/badlands.vx4ex", "Tileset/badlands.vx4"]
    assert resolved.source_format == "vx4"
    assert decode_canonical_words(resolved.payload)[0] == 65535


def test_resolver_does_not_mask_non_enoent_modern_open_failure():
    calls: list[str] = []

    def opener(name: str) -> AssetOpenResult:
        calls.append(name)
        return AssetOpenResult(None, errno.EIO)

    with pytest.raises(Vx4OpenError) as excinfo:
        resolve_asset("Tileset/badlands.vx4", opener)
    assert calls == ["Tileset/badlands.vx4ex"]
    assert excinfo.value.error_code == errno.EIO


def test_resolver_reports_classic_open_error_after_valid_fallback_decision():
    calls: list[str] = []

    def opener(name: str) -> AssetOpenResult:
        calls.append(name)
        if name.endswith(".vx4ex"):
            return AssetOpenResult(None, errno.ENOENT)
        return AssetOpenResult(None, errno.EACCES)

    with pytest.raises(Vx4OpenError) as excinfo:
        resolve_asset("Tileset/badlands.vx4", opener)
    assert calls == ["Tileset/badlands.vx4ex", "Tileset/badlands.vx4"]
    assert excinfo.value.name == "Tileset/badlands.vx4"
    assert excinfo.value.error_code == errno.EACCES


def test_non_vx4_assets_pass_through_byte_for_byte_and_exact_name():
    calls: list[str] = []
    payload = b"opaque-wpe"

    def opener(name: str) -> AssetOpenResult:
        calls.append(name)
        return AssetOpenResult(payload)

    resolved = resolve_asset("Tileset/badlands.wpe", opener)
    assert calls == ["Tileset/badlands.wpe"]
    assert resolved.source_format == "opaque"
    assert resolved.opened_name == "Tileset/badlands.wpe"
    assert resolved.payload == payload
