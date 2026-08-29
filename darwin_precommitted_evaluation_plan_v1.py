#!/usr/bin/env python3
"""Precommit symmetric calibration/held-out JointAdvance evaluation plans.

This source-only contract removes a second evaluation shortcut after seed partitioning:
held-out results must not be produced with benchmark parameters chosen after calibration
results are known.  One content-addressed plan therefore binds the exact benchmark source
generation and the shared matrix/workload parameters for both calibration and held-out
windows before either partition is interpreted as generalization evidence.

The contract grants no runtime, model-weight, corpus, or automatic-promotion authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Iterable, Mapping

import darwin_benchmark_evaluation_partition_binding_v1 as window_binding
import darwin_heldout_evaluation_split_v1 as split

MARKER = "VOID_WAR_COLLEGE_PRECOMMITTED_EVALUATION_PLAN_V1"
SCHEMA_VERSION = 1
BENCHMARK_SCHEMA_VERSION = 9
BENCHMARK_MAP = "singles.oramap"
BENCHMARK_SEED_RULE = "parameters.seed + slot"
WORKLOAD_PROFILES = ("noop_control", "stop_owned_unit")
SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
PLAN_DIGEST_RE = re.compile(r"[0-9a-f]{64}\Z")
MAX_MATRIX_CELLS = 64
MAX_SAMPLES = 1_000
MAX_REPETITIONS = 10


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _validate_benchmark_source_sha(value: object) -> str:
    if not isinstance(value, str) or not SHA40_RE.fullmatch(value):
        raise split.SplitError("benchmark_source_sha must be exactly 40 lowercase hex characters")
    return value


def _validate_concurrency(values: Iterable[object]) -> tuple[int, ...]:
    result = tuple(values)
    if not result:
        raise split.SplitError("concurrency must not be empty")
    if any(type(value) is not int for value in result):
        raise split.SplitError("concurrency values must be exact integers")
    if result != tuple(sorted(result)) or len(result) != len(set(result)):
        raise split.SplitError("concurrency must be strictly ascending and unique")
    if any(value not in window_binding.ALLOWED_JOINT_ADVANCE_CONCURRENCY for value in result):
        raise split.SplitError("concurrency contains an unsupported JointAdvance value")
    return result


def _validate_tick_batches(values: Iterable[object]) -> tuple[int, ...]:
    result = tuple(values)
    if not result:
        raise split.SplitError("tick_batches must not be empty")
    if any(type(value) is not int or value <= 0 or value > 10_000 for value in result):
        raise split.SplitError("tick_batches must contain exact integers in 1..10000")
    if result != tuple(sorted(result)) or len(result) != len(set(result)):
        raise split.SplitError("tick_batches must be strictly ascending and unique")
    return result


def _validate_positive_count(
    value: object,
    label: str,
    *,
    minimum: int,
    maximum: int,
) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise split.SplitError(f"{label} must be an exact integer in {minimum}..{maximum}")
    return value


def _plan_core(
    manifest: Mapping[str, object],
    benchmark_source_sha: object,
    calibration_base_seed: object,
    held_out_base_seed: object,
    concurrency: Iterable[object],
    tick_batches: Iterable[object],
    samples: object,
    repetitions: object,
    workload_profile: object,
) -> dict[str, object]:
    verified = split.validate_manifest(manifest)
    if verified["map"] != BENCHMARK_MAP:
        raise split.SplitError(
            f"evaluation split map must equal the current JointAdvance benchmark map {BENCHMARK_MAP}"
        )

    source_sha = _validate_benchmark_source_sha(benchmark_source_sha)
    concurrency_values = _validate_concurrency(concurrency)
    tick_values = _validate_tick_batches(tick_batches)
    if len(concurrency_values) * len(tick_values) > MAX_MATRIX_CELLS:
        raise split.SplitError(f"benchmark matrix exceeds {MAX_MATRIX_CELLS} cells")
    sample_count = _validate_positive_count(
        samples,
        "samples",
        minimum=1,
        maximum=MAX_SAMPLES,
    )
    repetition_count = _validate_positive_count(
        repetitions,
        "repetitions",
        minimum=2,
        maximum=MAX_REPETITIONS,
    )
    if workload_profile not in WORKLOAD_PROFILES:
        raise split.SplitError("workload_profile is not supported by the current JointAdvance benchmark")

    calibration_windows = [
        window_binding.bind_benchmark_seed_window(
            verified, "calibration", calibration_base_seed, value
        )
        for value in concurrency_values
    ]
    held_out_windows = [
        window_binding.bind_benchmark_seed_window(
            verified, "held_out", held_out_base_seed, value
        )
        for value in concurrency_values
    ]

    shared_parameters = {
        "benchmark_source_sha": source_sha,
        "benchmark_schema_version": BENCHMARK_SCHEMA_VERSION,
        "map": BENCHMARK_MAP,
        "concurrency": list(concurrency_values),
        "tick_batches": list(tick_values),
        "samples": sample_count,
        "repetitions": repetition_count,
        "workload_profile": workload_profile,
        "benchmark_seed_rule": BENCHMARK_SEED_RULE,
    }

    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "engine_frozen_commit": verified["engine_frozen_commit"],
        "war_college_comparison_point": verified["war_college_comparison_point"],
        "generation": verified["generation"],
        "split_digest": verified["split_digest"],
        "shared_parameters": shared_parameters,
        "partition_runs": {
            "calibration": {
                "base_seed": calibration_base_seed,
                "window_bindings": calibration_windows,
                "generalization_claim_authority": "NONE",
            },
            "held_out": {
                "base_seed": held_out_base_seed,
                "window_bindings": held_out_windows,
                "generalization_claim_authority": "HELD_OUT_EVIDENCE_ONLY",
            },
        },
        "evaluation_policy": {
            "shared_parameters_across_partitions": True,
            "posthoc_heldout_parameter_selection": False,
            "held_out_tuning_authority": "NONE",
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "runtime_execution_authority": "NONE",
            "model_weight_mutation_authority": "NONE",
            "corpus_admission_authority": "NONE",
            "automatic_promotion_authority": "NONE",
        },
    }


def build_precommitted_evaluation_plan(
    manifest: Mapping[str, object],
    benchmark_source_sha: object,
    calibration_base_seed: object,
    held_out_base_seed: object,
    concurrency: Iterable[object],
    tick_batches: Iterable[object],
    samples: object,
    repetitions: object,
    workload_profile: object,
) -> dict[str, object]:
    core = _plan_core(
        manifest,
        benchmark_source_sha,
        calibration_base_seed,
        held_out_base_seed,
        concurrency,
        tick_batches,
        samples,
        repetitions,
        workload_profile,
    )
    return {**core, "plan_digest": _sha256_json(core)}


def validate_precommitted_evaluation_plan(
    plan: Mapping[str, object],
    manifest: Mapping[str, object],
    expected_plan_digest: object,
) -> dict[str, object]:
    """Validate one plan against the digest recorded before evaluation.

    Requiring the caller's previously recorded digest is what converts content
    addressing into a precommitment: rebuilding a different but internally valid plan
    after observing calibration changes the digest and therefore fails this boundary.
    """

    if not isinstance(plan, Mapping):
        raise split.SplitError("plan must be an object")
    if not isinstance(expected_plan_digest, str) or not PLAN_DIGEST_RE.fullmatch(
        expected_plan_digest
    ):
        raise split.SplitError("expected_plan_digest must be exactly 64 lowercase hex characters")
    expected_keys = {
        "marker",
        "schema_version",
        "engine_frozen_commit",
        "war_college_comparison_point",
        "generation",
        "split_digest",
        "shared_parameters",
        "partition_runs",
        "evaluation_policy",
        "plan_digest",
    }
    if set(plan) != expected_keys:
        raise split.SplitError("plan keys are not schema-exact")
    if plan["marker"] != MARKER or plan["schema_version"] != SCHEMA_VERSION:
        raise split.SplitError("plan marker/schema mismatch")
    if plan["plan_digest"] != expected_plan_digest:
        raise split.SplitError("plan digest differs from the precommitted digest")

    shared = plan["shared_parameters"]
    runs = plan["partition_runs"]
    if not isinstance(shared, Mapping) or not isinstance(runs, Mapping):
        raise split.SplitError("plan parameter/run objects are invalid")
    if set(runs) != set(split.PARTITIONS):
        raise split.SplitError("plan partition runs are not schema-exact")
    calibration = runs["calibration"]
    held_out = runs["held_out"]
    if not isinstance(calibration, Mapping) or not isinstance(held_out, Mapping):
        raise split.SplitError("plan partition run is invalid")

    rebuilt = build_precommitted_evaluation_plan(
        manifest,
        shared.get("benchmark_source_sha"),
        calibration.get("base_seed"),
        held_out.get("base_seed"),
        shared.get("concurrency", ()),
        shared.get("tick_batches", ()),
        shared.get("samples"),
        shared.get("repetitions"),
        shared.get("workload_profile"),
    )
    if canonical_json(rebuilt) != canonical_json(dict(plan)):
        raise split.SplitError("plan content is not canonical for the precommitted evaluation")
    return rebuilt
