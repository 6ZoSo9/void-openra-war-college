from __future__ import annotations

import copy
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from ._spar_contract import ContractError
from .spar_pair_binding import WARM_START_BINDING_SCHEMA, warm_start_identity
from .spar_v22_pair_comparison import PairContractError, compare_reports, stable_json


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PairContractError(message)


def compare_reports_with_warm_starts(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
    *,
    baseline_warm_start_path: Path,
    candidate_warm_start_path: Path,
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
    normalized = baseline_binding["normalized_sha256"]
    baseline_copy["provenance"]["warm_start_sha256"] = normalized
    candidate_copy["provenance"]["warm_start_sha256"] = normalized

    result = compare_reports(baseline_copy, candidate_copy)
    pair_identity = result["pair_identity"]
    internal = pair_identity.pop("warm_start_sha256")
    _require(internal == normalized, "internal normalized warm-start binding drift")
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

    parser = argparse.ArgumentParser(description="Bind semantically identical warm starts before V2.2 pair comparison")
    parser.add_argument("--baseline-report", required=True)
    parser.add_argument("--candidate-report", required=True)
    parser.add_argument("--baseline-warm-start", required=True)
    parser.add_argument("--candidate-warm-start", required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        result = compare_reports_with_warm_starts(
            _read_json(Path(args.baseline_report)),
            _read_json(Path(args.candidate_report)),
            baseline_warm_start_path=Path(args.baseline_warm_start),
            candidate_warm_start_path=Path(args.candidate_warm_start),
        )
        sys.stdout.write(stable_json(result))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ContractError, PairContractError) as error:
        print(f"V2.2 pair binding error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
