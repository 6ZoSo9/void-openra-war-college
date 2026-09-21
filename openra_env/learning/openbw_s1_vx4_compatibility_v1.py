"""Source-only compatibility contract for classic VX4 and modern StarCraft VX4EX.

This module does not open game data, start OpenBW, access CASC, or execute a game.
It models the byte-level compatibility rules proven by the Precision acceptance
lane so build/runtime adapters can share one deterministic contract.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import errno

VX4_WORDS_PER_RECORD = 16
CLASSIC_VX4_WORD_BYTES = 2
MODERN_VX4EX_WORD_BYTES = 4
CLASSIC_VX4_RECORD_BYTES = VX4_WORDS_PER_RECORD * CLASSIC_VX4_WORD_BYTES
CANONICAL_VX4_RECORD_BYTES = VX4_WORDS_PER_RECORD * MODERN_VX4EX_WORD_BYTES
CASC_FILE_NOT_FOUND = errno.ENOENT


class Vx4CompatibilityError(RuntimeError):
    """Base error for the source-only VX4 compatibility contract."""


class Vx4FormatError(Vx4CompatibilityError):
    """Raised when a VX4/VX4EX byte stream has an invalid record shape."""


class Vx4OpenError(Vx4CompatibilityError):
    """Raised when an asset open fails and fallback is not permitted."""

    def __init__(self, name: str, error_code: int) -> None:
        super().__init__(f"open failed for {name}: error={error_code}")
        self.name = name
        self.error_code = error_code


@dataclass(frozen=True)
class AssetOpenResult:
    payload: bytes | None
    error_code: int = 0

    @property
    def ok(self) -> bool:
        return self.payload is not None


@dataclass(frozen=True)
class CanonicalAsset:
    requested_name: str
    opened_name: str
    source_format: str
    payload: bytes

    @property
    def record_count(self) -> int:
        if self.source_format not in {"vx4", "vx4ex"}:
            return 0
        return len(self.payload) // CANONICAL_VX4_RECORD_BYTES


def is_classic_vx4_request(name: str) -> bool:
    return name.lower().endswith(".vx4")


def modern_vx4ex_name(classic_name: str) -> str:
    if not is_classic_vx4_request(classic_name):
        raise ValueError(f"not a .vx4 request: {classic_name}")
    return classic_name + "ex"


def canonicalize_vx4ex(payload: bytes) -> bytes:
    if len(payload) % CANONICAL_VX4_RECORD_BYTES != 0:
        raise Vx4FormatError(
            "VX4EX payload length must be a multiple of "
            f"{CANONICAL_VX4_RECORD_BYTES}, got {len(payload)}"
        )
    return bytes(payload)


def canonicalize_classic_vx4(payload: bytes) -> bytes:
    if len(payload) % CLASSIC_VX4_RECORD_BYTES != 0:
        raise Vx4FormatError(
            "classic VX4 payload length must be a multiple of "
            f"{CLASSIC_VX4_RECORD_BYTES}, got {len(payload)}"
        )

    canonical = bytearray(
        len(payload) // CLASSIC_VX4_RECORD_BYTES * CANONICAL_VX4_RECORD_BYTES
    )
    dst = 0
    for src in range(0, len(payload), CLASSIC_VX4_WORD_BYTES):
        value = int.from_bytes(payload[src : src + 2], "little", signed=False)
        canonical[dst : dst + 4] = value.to_bytes(4, "little", signed=False)
        dst += 4
    return bytes(canonical)


def resolve_asset(
    requested_name: str,
    opener: Callable[[str], AssetOpenResult],
) -> CanonicalAsset:
    """Resolve one asset with fail-closed VX4EX-to-VX4 fallback semantics.

    For a .vx4 request, the modern .vx4ex name is attempted first. Classic VX4
    fallback is permitted only when the modern open fails with exact ENOENT.
    Any other modern open error is terminal. Non-VX4 requests are opened exactly
    once under their requested name and are returned byte-for-byte.
    """

    if not is_classic_vx4_request(requested_name):
        result = opener(requested_name)
        if not result.ok:
            raise Vx4OpenError(requested_name, result.error_code)
        return CanonicalAsset(
            requested_name=requested_name,
            opened_name=requested_name,
            source_format="opaque",
            payload=bytes(result.payload or b""),
        )

    modern_name = modern_vx4ex_name(requested_name)
    modern = opener(modern_name)
    if modern.ok:
        return CanonicalAsset(
            requested_name=requested_name,
            opened_name=modern_name,
            source_format="vx4ex",
            payload=canonicalize_vx4ex(modern.payload or b""),
        )
    if modern.error_code != CASC_FILE_NOT_FOUND:
        raise Vx4OpenError(modern_name, modern.error_code)

    classic = opener(requested_name)
    if not classic.ok:
        raise Vx4OpenError(requested_name, classic.error_code)
    return CanonicalAsset(
        requested_name=requested_name,
        opened_name=requested_name,
        source_format="vx4",
        payload=canonicalize_classic_vx4(classic.payload or b""),
    )


def decode_canonical_words(payload: bytes) -> tuple[int, ...]:
    if len(payload) % CANONICAL_VX4_RECORD_BYTES != 0:
        raise Vx4FormatError(
            "canonical VX4 payload length must be a multiple of "
            f"{CANONICAL_VX4_RECORD_BYTES}, got {len(payload)}"
        )
    return tuple(
        int.from_bytes(payload[offset : offset + 4], "little", signed=False)
        for offset in range(0, len(payload), 4)
    )


def reference_metrics(payload: bytes, vr4_record_count: int) -> dict[str, int | bool]:
    if vr4_record_count < 0:
        raise ValueError("vr4_record_count must be non-negative")
    words = decode_canonical_words(payload)
    max_raw = max(words, default=0)
    max_vr4_id = max((value // 2 for value in words), default=0)
    flip_entries = sum(value & 1 for value in words)
    invalid = sum((value // 2) >= vr4_record_count for value in words)
    return {
        "entry_count": len(words),
        "record_count": len(words) // VX4_WORDS_PER_RECORD,
        "max_raw_entry": max_raw,
        "max_vr4_id": max_vr4_id,
        "flip_entry_count": flip_entries,
        "invalid_vr4_reference_count": invalid,
        "all_references_valid": invalid == 0,
    }
