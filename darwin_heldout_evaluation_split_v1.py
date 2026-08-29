#!/usr/bin/env python3
"""Deterministic held-out evaluation split contract for the VOID OpenRA War College.

This module creates an immutable, content-addressed split manifest that prevents
calibration/training seeds from being relabeled as held-out evaluation seeds.
It does not execute OpenRA and grants no runtime, training, or promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from typing import Iterable, Mapping, Sequence

MARKER = "VOID_WAR_COLLEGE_HELDOUT_EVALUATION_SPLIT_V1"
SCHEMA_VERSION = 1
ENGINE_FROZEN_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
WAR_COLLEGE_COMPARISON_POINT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
GENERATION = "ad1926569b12466c"
MAX_RUNTIME_SEED = 2_147_483_647
PARTITIONS = ("calibration", "held_out")
SEED_RE = re.compile(r"(?:0|[1-9][0-9]*)\Z")


class SplitError(ValueError):
    """Raised when an evaluation split cannot be proven unambiguous."""


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _validate_map_name(map_name: str) -> str:
    if not isinstance(map_name, str) or not map_name:
        raise SplitError("map_name must be a non-empty string")
    if len(map_name) > 128:
        raise SplitError("map_name exceeds 128 characters")
    if any(ord(ch) < 0x21 or ord(ch) > 0x7E for ch in map_name):
        raise SplitError("map_name must contain printable non-space ASCII only")
    return map_name


def _validate_seed(seed: object) -> int:
    if type(seed) is not int:
        raise SplitError("seed must be an integer")
    if seed < 0 or seed > MAX_RUNTIME_SEED:
        raise SplitError("seed is outside the signed runtime-integer range")
    return seed


def parse_seed_set(text: str) -> tuple[int, ...]:
    if not isinstance(text, str) or not text:
        raise SplitError("seed set must be a non-empty comma-separated string")
    tokens = text.split(",")
    if any(not SEED_RE.fullmatch(token) for token in tokens):
        raise SplitError("seed set contains a non-canonical decimal integer")
    seeds = tuple(_validate_seed(int(token, 10)) for token in tokens)
    return _validate_seed_set(seeds, "seed set")


def _validate_seed_set(seeds: Iterable[object], label: str) -> tuple[int, ...]:
    normalized = tuple(_validate_seed(seed) for seed in seeds)
    if not normalized:
        raise SplitError(f"{label} must not be empty")
    if len(normalized) > 4096:
        raise SplitError(f"{label} exceeds 4096 seeds")
    if tuple(sorted(normalized)) != normalized:
        raise SplitError(f"{label} must be strictly ascending")
    if len(set(normalized)) != len(normalized):
        raise SplitError(f"{label} contains duplicate seeds")
    return normalized


def _manifest_core(
    map_name: str,
    calibration_seeds: Iterable[object],
    held_out_seeds: Iterable[object],
) -> dict[str, object]:
    calibration = _validate_seed_set(calibration_seeds, "calibration_seeds")
    held_out = _validate_seed_set(held_out_seeds, "held_out_seeds")
    overlap = sorted(set(calibration).intersection(held_out))
    if overlap:
        raise SplitError(
            "calibration and held-out seed sets overlap: "
            + ",".join(str(seed) for seed in overlap)
        )
    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "engine_frozen_commit": ENGINE_FROZEN_COMMIT,
        "war_college_comparison_point": WAR_COLLEGE_COMPARISON_POINT,
        "generation": GENERATION,
        "map": _validate_map_name(map_name),
        "partitions": {
            "calibration": list(calibration),
            "held_out": list(held_out),
        },
        "split_policy": {
            "disjoint_seed_sets": True,
            "same_seed_cross_partition_reuse": False,
            "held_out_tuning_authority": "NONE",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        },
    }


def build_manifest(
    map_name: str,
    calibration_seeds: Iterable[object],
    held_out_seeds: Iterable[object],
) -> dict[str, object]:
    core = _manifest_core(map_name, calibration_seeds, held_out_seeds)
    return {**core, "split_digest": _sha256_json(core)}


def validate_manifest(manifest: Mapping[str, object]) -> dict[str, object]:
    if not isinstance(manifest, Mapping):
        raise SplitError("manifest must be an object")
    expected_keys = {
        "marker",
        "schema_version",
        "engine_frozen_commit",
        "war_college_comparison_point",
        "generation",
        "map",
        "partitions",
        "split_policy",
        "split_digest",
    }
    if set(manifest) != expected_keys:
        raise SplitError("manifest keys are not schema-exact")
    if manifest["marker"] != MARKER or manifest["schema_version"] != SCHEMA_VERSION:
        raise SplitError("manifest marker/schema mismatch")
    if manifest["engine_frozen_commit"] != ENGINE_FROZEN_COMMIT:
        raise SplitError("engine comparison point mismatch")
    if manifest["war_college_comparison_point"] != WAR_COLLEGE_COMPARISON_POINT:
        raise SplitError("War College comparison point mismatch")
    if manifest["generation"] != GENERATION:
        raise SplitError("generation mismatch")
    partitions = manifest["partitions"]
    if not isinstance(partitions, Mapping) or set(partitions) != set(PARTITIONS):
        raise SplitError("partition object is not schema-exact")
    rebuilt = build_manifest(
        str(manifest["map"]),
        partitions["calibration"],
        partitions["held_out"],
    )
    if canonical_json(rebuilt) != canonical_json(dict(manifest)):
        raise SplitError("manifest content or split digest is not canonical")
    return rebuilt


def bind_evaluation_seed(
    manifest: Mapping[str, object], partition: str, seed: object
) -> dict[str, object]:
    verified = validate_manifest(manifest)
    if partition not in PARTITIONS:
        raise SplitError("partition must be calibration or held_out")
    normalized_seed = _validate_seed(seed)
    seeds = verified["partitions"][partition]
    assert isinstance(seeds, list)
    if normalized_seed not in seeds:
        raise SplitError("seed is not admitted by the requested partition")
    other = "held_out" if partition == "calibration" else "calibration"
    other_seeds = verified["partitions"][other]
    assert isinstance(other_seeds, list)
    if normalized_seed in other_seeds:
        raise SplitError("seed is ambiguously admitted by both partitions")
    return {
        "marker": "VOID_WAR_COLLEGE_EVALUATION_SEED_BINDING_V1",
        "schema_version": 1,
        "split_digest": verified["split_digest"],
        "map": verified["map"],
        "partition": partition,
        "seed": normalized_seed,
        "generalization_claim_authority": (
            "HELD_OUT_EVIDENCE_ONLY" if partition == "held_out" else "NONE"
        ),
        "runtime_evidence": "PENDING_DESIGNATED_HOST",
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", required=True, dest="map_name")
    parser.add_argument("--calibration-seeds", required=True)
    parser.add_argument("--held-out-seeds", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        manifest = build_manifest(
            args.map_name,
            parse_seed_set(args.calibration_seeds),
            parse_seed_set(args.held_out_seeds),
        )
    except SplitError as error:
        print(
            canonical_json(
                {
                    "marker": MARKER,
                    "schema_version": SCHEMA_VERSION,
                    "classification": "HOLD",
                    "reason": str(error),
                    "runtime_evidence": "PENDING_DESIGNATED_HOST",
                }
            )
        )
        return 2
    print(canonical_json(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
