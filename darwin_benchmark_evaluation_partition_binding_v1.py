#!/usr/bin/env python3
"""Bind War College benchmark seed windows to an immutable evaluation partition.

The JointAdvance benchmark derives each concurrent slot seed as ``base_seed + slot``.
A held-out claim therefore cannot safely bind only the base seed: every derived slot
seed used by the matrix must belong to the same immutable held-out partition.

This module is source-only. It validates evaluation-partition identity and grants no
runtime execution, model-weight, corpus, or automatic promotion authority.
"""

from __future__ import annotations

from typing import Mapping

import darwin_heldout_evaluation_split_v1 as split

MARKER = "VOID_WAR_COLLEGE_BENCHMARK_EVALUATION_PARTITION_BINDING_V1"
SCHEMA_VERSION = 1
ALLOWED_JOINT_ADVANCE_CONCURRENCY = (1, 2, 4, 8)
BENCHMARK_SEED_RULE = "parameters.seed + slot"


def bind_benchmark_seed_window(
    manifest: Mapping[str, object],
    partition: str,
    base_seed: object,
    concurrency: object,
) -> dict[str, object]:
    """Bind every derived benchmark slot seed to one immutable partition.

    The live JointAdvance benchmark's allowed concurrency values are 1, 2, 4, and 8,
    and each slot uses ``parameters.seed + slot``. This contract refuses a
    generalization label unless the complete derived seed window is admitted by the
    requested partition.
    """

    verified = split.validate_manifest(manifest)

    if partition not in split.PARTITIONS:
        raise split.SplitError("partition must be calibration or held_out")
    if type(base_seed) is not int:
        raise split.SplitError("benchmark base_seed must be an integer")
    if base_seed == split.RANDOM_RUNTIME_SEED_SENTINEL:
        raise split.SplitError(
            "benchmark base_seed 0 is reserved as the runtime random-seed sentinel"
        )
    if (
        base_seed < split.MIN_DETERMINISTIC_RUNTIME_SEED
        or base_seed > split.MAX_RUNTIME_SEED
    ):
        raise split.SplitError(
            "benchmark base_seed is outside the deterministic signed runtime-integer range"
        )
    if type(concurrency) is not int or concurrency not in ALLOWED_JOINT_ADVANCE_CONCURRENCY:
        raise split.SplitError("benchmark concurrency must be one of 1,2,4,8")
    last_seed = base_seed + concurrency - 1
    if last_seed > split.MAX_RUNTIME_SEED:
        raise split.SplitError(
            "benchmark seed window exceeds the signed runtime-integer range"
        )

    slot_bindings: list[dict[str, int]] = []
    for slot in range(concurrency):
        seed = base_seed + slot
        try:
            split.bind_evaluation_seed(verified, partition, seed)
        except split.SplitError as error:
            raise split.SplitError(
                f"benchmark seed window escapes {partition} at slot {slot} seed {seed}"
            ) from error
        slot_bindings.append({"slot": slot, "seed": seed})

    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "split_digest": verified["split_digest"],
        "engine_frozen_commit": verified["engine_frozen_commit"],
        "war_college_comparison_point": verified["war_college_comparison_point"],
        "generation": verified["generation"],
        "map": verified["map"],
        "partition": partition,
        "benchmark_seed_rule": BENCHMARK_SEED_RULE,
        "base_seed": base_seed,
        "concurrency": concurrency,
        "slot_bindings": slot_bindings,
        "generalization_claim_authority": (
            "HELD_OUT_EVIDENCE_ONLY" if partition == "held_out" else "NONE"
        ),
        "runtime_evidence": "PENDING_DESIGNATED_HOST",
        "runtime_execution_authority": "NONE",
        "model_weight_mutation_authority": "NONE",
        "automatic_promotion_authority": "NONE",
    }
