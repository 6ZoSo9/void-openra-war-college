from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from ._spar_contract import MAX_TRAJECTORY_BYTES, ContractError, _jsonl, _read
from .spar_pair_comparison import PairContractError, compare_reports, stable_json

WARM_START_BINDING_SCHEMA = "void.apollyon.warm-start-pair-binding.v1"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PairContractError(message)


def warm_start_identity(path: Path) -> dict[str, str]:
    """Bind one raw warm-start log and derive a run-id-independent digest.

    The warm-start runner includes a timestamp-bearing ``run_id`` in the first
    ``warm_start_header`` row. That makes the raw file SHA intentionally unique
    per execution even when every curriculum/world fact is identical. Pairing
    therefore removes only that one run-local field before stable hashing; all
    subsequent rows must remain byte-equivalent after JSON canonicalization.
    """
    raw = _read(path, "warm-start", MAX_TRAJECTORY_BYTES)
    raw_sha = hashlib.sha256(raw).hexdigest()
    rows = _jsonl(raw)
    _require(bool(rows), "warm-start log is empty")
    _require(rows[0].get("event") == "warm_start_header", "warm-start must begin with warm_start_header")
    run_id = rows[0].get("run_id")
    _require(isinstance(run_id, str) and bool(run_id), "warm-start header run_id missing")

    canonical_rows: list[dict[str, Any]] = []
    for index, source in enumerate(rows):
        row = {key: value for key, value in source.items() if key != "_line"}
        if index == 0:
            row.pop("run_id", None)
        canonical_rows.append(row)

    canonical = "".join(
        json.dumps(
            row,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
        for row in canonical_rows
    ).encode("utf-8")
    return {
        "raw_sha256": raw_sha,
        "normalized_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def compare_reports_with_warm_starts(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
    *,
    baseline_warm_start_path: Path,
    candidate_warm_start_path: Path,
    expected_v2_candidate_sha256: str | None = None,
    expected_v2_source_commit: str | None = None,
) -> dict[str, Any]:
    baseline_binding = warm_start_identity(baseline_warm_start_path)
    candidate_binding = warm_start_identity(candidate_warm_start_path)

    baseline_provenance = baseline.get("provenance")
    candidate_provenance = candidate.get("provenance")
    _require(isinstance(baseline_provenance, Mapping), "baseline provenance missing")
    _require(isinstance(candidate_provenance, Mapping), "candidate provenance missing")
    _require(
        baseline_provenance.get("warm_start_sha256") == baseline_binding["raw_sha256"],
        "baseline report is not bound to supplied warm-start log",
    )
    _require(
        candidate_provenance.get("warm_start_sha256") == candidate_binding["raw_sha256"],
        "candidate report is not bound to supplied warm-start log",
    )
    _require(
        baseline_binding["normalized_sha256"] == candidate_binding["normalized_sha256"],
        "normalized warm-start mismatch",
    )

    baseline_copy = copy.deepcopy(dict(baseline))
    candidate_copy = copy.deepcopy(dict(candidate))
    baseline_copy["provenance"]["warm_start_sha256"] = baseline_binding["normalized_sha256"]
    candidate_copy["provenance"]["warm_start_sha256"] = candidate_binding["normalized_sha256"]

    result = compare_reports(
        baseline_copy,
        candidate_copy,
        expected_v2_candidate_sha256=expected_v2_candidate_sha256,
        expected_v2_source_commit=expected_v2_source_commit,
    )
    pair_identity = result["pair_identity"]
    normalized = pair_identity.pop("warm_start_sha256")
    _require(
        normalized == baseline_binding["normalized_sha256"],
        "internal normalized warm-start binding drift",
    )
    pair_identity["warm_start_normalized_sha256"] = normalized
    result["warm_start_binding"] = {
        "schema": WARM_START_BINDING_SCHEMA,
        "normalization": "remove warm_start_header.run_id only; stable canonical JSONL",
        "baseline_raw_sha256": baseline_binding["raw_sha256"],
        "candidate_raw_sha256": candidate_binding["raw_sha256"],
        "normalized_sha256": normalized,
        "semantic_match": True,
    }
    return result


def _read_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, Mapping), f"{path} must contain a JSON object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Bind semantically identical warm starts before V2 pair comparison")
    parser.add_argument("--baseline-report", required=True)
    parser.add_argument("--candidate-report", required=True)
    parser.add_argument("--baseline-warm-start", required=True)
    parser.add_argument("--candidate-warm-start", required=True)
    parser.add_argument("--expected-v2-candidate-sha256", required=True)
    parser.add_argument("--expected-v2-source-commit", required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        result = compare_reports_with_warm_starts(
            _read_json(Path(args.baseline_report)),
            _read_json(Path(args.candidate_report)),
            baseline_warm_start_path=Path(args.baseline_warm_start),
            candidate_warm_start_path=Path(args.candidate_warm_start),
            expected_v2_candidate_sha256=args.expected_v2_candidate_sha256,
            expected_v2_source_commit=args.expected_v2_source_commit,
        )
        sys.stdout.write(stable_json(result))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ContractError, PairContractError) as error:
        print(f"pair binding error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
