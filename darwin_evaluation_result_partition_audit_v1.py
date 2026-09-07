#!/usr/bin/env python3
"""Audit evaluation-result coverage against one exact Darwin precommit record.

The precommit lane already binds the split and symmetric benchmark parameters. This
source-only companion prevents later result bundles from silently omitting, duplicating,
or relabeling partition rows. It does not authenticate a runtime producer and grants no
runtime, model-weight, corpus, or automatic-promotion authority.
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Mapping

import darwin_evaluation_precommit_record_v1 as record_contract
import darwin_heldout_evaluation_split_v1 as split


MARKER = "VOID_WAR_COLLEGE_EVALUATION_RESULT_PARTITION_AUDIT_V1"
BUNDLE_MARKER = "VOID_WAR_COLLEGE_EVALUATION_RESULT_BUNDLE_V1"
SCHEMA_VERSION = 1
SHA64_RE = re.compile(r"[0-9a-f]{64}\Z")
ROW_KEYS = {
    "record_digest",
    "evaluation_attempt_id",
    "producer_session_generation",
    "partition",
    "concurrency",
    "tick_batches",
    "sample_index",
    "repetition_index",
    "slot",
    "seed",
    "outcome_digest",
    "result_binding_sha256",
}


class ResultAuditError(ValueError):
    """Raised when result evidence is not exact for its precommitted generation."""


def canonical_json(value: object) -> str:
    return record_contract.canonical_json(value)


def _sha256_json(value: object) -> str:
    """Hash canonical JSON incrementally without allocating one full bundle string."""
    digest = hashlib.sha256()
    encoder = json.JSONEncoder(
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    for chunk in encoder.iterencode(value):
        digest.update(chunk.encode("utf-8"))
    return digest.hexdigest()


def _exact_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise ResultAuditError(f"{label} must be an exact integer")
    return value


def result_binding_sha256(
    *,
    record_digest: str,
    evaluation_attempt_id: str,
    producer_session_generation: int,
    partition: str,
    concurrency: int,
    tick_batches: int,
    sample_index: int,
    repetition_index: int,
    slot: int,
    seed: int,
    outcome_digest: str,
) -> str:
    if type(record_digest) is not str or not SHA64_RE.fullmatch(record_digest):
        raise ResultAuditError(
            "record_digest must be exactly 64 lowercase hex characters"
        )
    return _sha256_json(
        {
            "concurrency": concurrency,
            "evaluation_attempt_id": evaluation_attempt_id,
            "outcome_digest": outcome_digest,
            "partition": partition,
            "producer_session_generation": producer_session_generation,
            "record_digest": record_digest,
            "repetition_index": repetition_index,
            "sample_index": sample_index,
            "seed": seed,
            "slot": slot,
            "tick_batches": tick_batches,
        }
    )


def _run_layout(
    verified_record: Mapping[str, object], partition: str
) -> tuple[int, int, int, dict[tuple[int, int], int]]:
    plan = verified_record["plan"]
    assert isinstance(plan, Mapping)
    shared = plan["shared_parameters"]
    partition_runs = plan["partition_runs"]
    assert isinstance(shared, Mapping) and isinstance(partition_runs, Mapping)
    run = partition_runs[partition]
    assert isinstance(run, Mapping)
    base_seed = _exact_int(run["base_seed"], "base_seed")
    concurrency_values = shared["concurrency"]
    tick_values = shared["tick_batches"]
    samples = _exact_int(shared["samples"], "samples")
    repetitions = _exact_int(shared["repetitions"], "repetitions")
    assert isinstance(concurrency_values, list) and isinstance(tick_values, list)

    offsets: dict[tuple[int, int], int] = {}
    expected_count = 0
    for concurrency in concurrency_values:
        c = _exact_int(concurrency, "concurrency")
        for tick_batches in tick_values:
            ticks = _exact_int(tick_batches, "tick_batches")
            offsets[(c, ticks)] = expected_count
            expected_count += samples * repetitions * c
    return base_seed, samples, repetitions, offsets


def expected_result_row_count(
    precommit_record: Mapping[str, object],
    manifest: Mapping[str, object],
    partition: str,
) -> int:
    """Return exact expected rows without materializing the result identity space."""
    if partition not in split.PARTITIONS:
        raise ResultAuditError("partition must be calibration or held_out")
    verified_record = record_contract.validate_record(precommit_record, manifest)
    _, samples, repetitions, offsets = _run_layout(verified_record, partition)
    return sum(
        samples * repetitions * concurrency for concurrency, _ in offsets
    )


def _preflight_partition_rows(
    verified_record: Mapping[str, object],
    partition: str,
    rows: object,
) -> None:
    """Reject impossible partition containers before any result-row traversal."""
    if type(rows) is not list:
        raise ResultAuditError(f"{partition} rows must be an exact list")
    _, samples, repetitions, offsets = _run_layout(verified_record, partition)
    expected_count = sum(samples * repetitions * concurrency for concurrency, _ in offsets)
    if len(rows) != expected_count:
        raise ResultAuditError(
            f"{partition} row cardinality {len(rows)} does not equal precommit {expected_count}"
        )


def _validate_partition_rows(
    verified_record: Mapping[str, object],
    partition: str,
    rows: object,
) -> list[dict[str, object]]:
    _preflight_partition_rows(verified_record, partition, rows)
    assert type(rows) is list
    base_seed, samples, repetitions, offsets = _run_layout(
        verified_record, partition
    )
    record_digest = verified_record["record_digest"]
    evaluation_attempt_id = verified_record["evaluation_attempt_id"]
    producer_session_generation = verified_record["producer_session_generation"]
    assert isinstance(record_digest, str)
    assert isinstance(evaluation_attempt_id, str)
    assert type(producer_session_generation) is int

    # The precommit already defines one exact total row order.  Requiring the
    # producer to emit that order lets coverage be proved in one pass with
    # constant auxiliary state: no 2.4-million-byte bitmap, duplicate row
    # copies, or O(n log n) normalization sort at the maximum valid plan.
    for row_index, row in enumerate(rows):
        if type(row) is not dict or set(row) != ROW_KEYS:
            raise ResultAuditError(f"{partition} row keys are not schema-exact")
        if row["partition"] != partition:
            raise ResultAuditError(f"{partition} container includes a cross-partition row")
        if (
            type(row["record_digest"]) is not str
            or row["record_digest"] != record_digest
            or type(row["evaluation_attempt_id"]) is not str
            or row["evaluation_attempt_id"] != evaluation_attempt_id
            or type(row["producer_session_generation"]) is not int
            or row["producer_session_generation"] != producer_session_generation
        ):
            raise ResultAuditError(
                f"{partition} row belongs to a different execution attempt/session "
                "generation or a different precommit record"
            )
        concurrency = _exact_int(row["concurrency"], "concurrency")
        tick_batches = _exact_int(row["tick_batches"], "tick_batches")
        sample_index = _exact_int(row["sample_index"], "sample_index")
        repetition_index = _exact_int(row["repetition_index"], "repetition_index")
        slot = _exact_int(row["slot"], "slot")
        seed = _exact_int(row["seed"], "seed")
        offset = offsets.get((concurrency, tick_batches))
        if (
            offset is None
            or sample_index < 0
            or sample_index >= samples
            or repetition_index < 0
            or repetition_index >= repetitions
            or slot < 0
            or slot >= concurrency
            or seed != base_seed + slot
        ):
            raise ResultAuditError(
                f"{partition} row is outside the exact precommitted matrix/seed window"
            )
        ordinal = (
            offset
            + (sample_index * repetitions + repetition_index) * concurrency
            + slot
        )
        if ordinal != row_index:
            raise ResultAuditError(
                f"{partition} contains a duplicate, missing, or noncanonical result row order"
            )

        outcome_digest = row["outcome_digest"]
        binding = row["result_binding_sha256"]
        if not isinstance(outcome_digest, str) or not SHA64_RE.fullmatch(outcome_digest):
            raise ResultAuditError("outcome_digest must be exactly 64 lowercase hex characters")
        if not isinstance(binding, str) or not SHA64_RE.fullmatch(binding):
            raise ResultAuditError(
                "result_binding_sha256 must be exactly 64 lowercase hex characters"
            )
        expected_binding = result_binding_sha256(
            record_digest=record_digest,
            evaluation_attempt_id=evaluation_attempt_id,
            producer_session_generation=producer_session_generation,
            partition=partition,
            concurrency=concurrency,
            tick_batches=tick_batches,
            sample_index=sample_index,
            repetition_index=repetition_index,
            slot=slot,
            seed=seed,
            outcome_digest=outcome_digest,
        )
        if binding != expected_binding:
            raise ResultAuditError(
                f"{partition} outcome is not bound to its exact row identity"
            )
    return rows


def _bundle_provenance(
    verified_record: Mapping[str, object],
) -> dict[str, object]:
    return {
        "marker": BUNDLE_MARKER,
        "schema_version": SCHEMA_VERSION,
        "record_digest": verified_record["record_digest"],
        "evaluation_attempt_id": verified_record["evaluation_attempt_id"],
        "producer_session_generation": verified_record["producer_session_generation"],
        "plan_digest": verified_record["plan_digest"],
        "split_digest": verified_record["split_digest"],
        "benchmark_source_sha": verified_record["benchmark_source_sha"],
        "engine_frozen_commit": verified_record["engine_frozen_commit"],
        "war_college_comparison_point": verified_record["war_college_comparison_point"],
        "generation": verified_record["generation"],
    }


def _bundle_core_from_verified(
    verified_record: Mapping[str, object],
    runs: Mapping[str, object],
) -> dict[str, object]:
    if not isinstance(runs, Mapping) or set(runs) != set(split.PARTITIONS):
        raise ResultAuditError("result runs must contain exact calibration and held_out keys")
    # Check every partition container and exact cardinality before traversing the
    # first row. A malformed held-out container must not force a scan of up to
    # 2.4 million otherwise valid calibration rows.
    for partition in split.PARTITIONS:
        _preflight_partition_rows(verified_record, partition, runs[partition])
    normalized_runs = {
        partition: _validate_partition_rows(verified_record, partition, runs[partition])
        for partition in split.PARTITIONS
    }
    return {
        **_bundle_provenance(verified_record),
        "runs": normalized_runs,
    }


def _bundle_core(
    precommit_record: Mapping[str, object],
    manifest: Mapping[str, object],
    runs: Mapping[str, object],
) -> dict[str, object]:
    verified_record = record_contract.validate_record(precommit_record, manifest)
    return _bundle_core_from_verified(verified_record, runs)


def build_result_bundle(
    precommit_record: Mapping[str, object],
    manifest: Mapping[str, object],
    runs: Mapping[str, object],
) -> dict[str, object]:
    core = _bundle_core(precommit_record, manifest, runs)
    return {**core, "result_digest": _sha256_json(core)}


def audit_result_bundle(
    bundle: Mapping[str, object],
    precommit_record: Mapping[str, object],
    manifest: Mapping[str, object],
) -> dict[str, object]:
    if not isinstance(bundle, Mapping):
        raise ResultAuditError("result bundle must be an object")
    expected_keys = {
        "marker",
        "schema_version",
        "record_digest",
        "evaluation_attempt_id",
        "producer_session_generation",
        "plan_digest",
        "split_digest",
        "benchmark_source_sha",
        "engine_frozen_commit",
        "war_college_comparison_point",
        "generation",
        "runs",
        "result_digest",
    }
    if set(bundle) != expected_keys:
        raise ResultAuditError("result bundle keys are not schema-exact")
    if bundle["marker"] != BUNDLE_MARKER or bundle["schema_version"] != SCHEMA_VERSION:
        raise ResultAuditError("result bundle marker/schema mismatch")
    if not isinstance(bundle["result_digest"], str) or not SHA64_RE.fullmatch(
        bundle["result_digest"]
    ):
        raise ResultAuditError("result_digest must be exactly 64 lowercase hex characters")
    verified_record = record_contract.validate_record(precommit_record, manifest)
    expected_provenance = _bundle_provenance(verified_record)
    # Reject immutable provenance before traversing up to 4.8 million supplied
    # rows. Exact types preserve canonical JSON identity (for example, Python's
    # True == 1 must not admit a boolean schema version).
    for field, expected_value in expected_provenance.items():
        if (
            type(bundle[field]) is not type(expected_value)
            or bundle[field] != expected_value
        ):
            raise ResultAuditError(
                "result bundle identity, provenance, coverage, or digest differs from precommit"
            )
    core = _bundle_core_from_verified(verified_record, bundle["runs"])
    # Row validation proves exact schema, order, cardinality, identity, and
    # per-outcome binding in place before the one canonical core-digest pass.
    expected_result_digest = _sha256_json(core)
    if bundle["result_digest"] != expected_result_digest:
        raise ResultAuditError(
            "result bundle identity, provenance, coverage, or digest differs from precommit"
        )
    runs = core["runs"]
    assert isinstance(runs, Mapping)
    return {
        "marker": MARKER,
        "schema_version": SCHEMA_VERSION,
        "status": "GREEN",
        "record_digest": core["record_digest"],
        "evaluation_attempt_id": core["evaluation_attempt_id"],
        "producer_session_generation": core["producer_session_generation"],
        "result_digest": expected_result_digest,
        "calibration_rows": len(runs["calibration"]),
        "held_out_rows": len(runs["held_out"]),
        "calibration_generalization_claim_authority": "NONE",
        "held_out_generalization_claim_authority": "HELD_OUT_EVIDENCE_ONLY",
        "trusted_runtime_producer_authentication": "UNPROVEN",
        "bundle_replay_protection": "PENDING_CREATE_ONLY_ADMISSION_RECORD",
        "runtime_evidence": "PENDING_DESIGNATED_HOST",
        "runtime_execution_authority": "NONE",
        "model_weight_mutation_authority": "NONE",
        "corpus_admission_authority": "NONE",
        "automatic_promotion_authority": "NONE",
    }
