from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from ._spar_conditional_v2_2_reviewed_identity import REVIEWED_V22_IDENTITY
from .spar_v22_pair_comparison import PAIR_SCHEMA, PairContractError

MATRIX_SCHEMA = "void.apollyon.conditional-engagement-v2-2-pair-matrix.v1"
REVIEWED_REGRESSION_SEED = 2051
REVIEWED_GAIN_SEED = 2055
MINIMUM_HELD_OUT_SEED_COUNT = 3
REPEATS_PER_SEED = 3


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PairContractError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _num(value: Any, label: str) -> float:
    _require(type(value) in (int, float), f"{label} must be numeric")
    return float(value)


def _sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _bool(value: Any, label: str) -> bool:
    _require(type(value) is bool, f"{label} must be bool")
    return value


def evaluate_matrix(
    pairs: Sequence[Mapping[str, Any]],
    *,
    regression_seed: int = REVIEWED_REGRESSION_SEED,
    gain_seed: int = REVIEWED_GAIN_SEED,
    minimum_held_out_seed_count: int = MINIMUM_HELD_OUT_SEED_COUNT,
    repeats_per_seed: int = REPEATS_PER_SEED,
) -> dict[str, Any]:
    _require(type(regression_seed) is int and regression_seed >= 0, "regression seed malformed")
    _require(type(gain_seed) is int and gain_seed >= 0 and gain_seed != regression_seed, "gain seed malformed")
    _require(type(minimum_held_out_seed_count) is int and minimum_held_out_seed_count >= 1, "held-out seed count malformed")
    _require(type(repeats_per_seed) is int and repeats_per_seed >= 1, "repeat count malformed")

    grouped: dict[int, list[Mapping[str, Any]]] = {}
    seen_baseline: set[str] = set()
    seen_candidate: set[str] = set()
    all_protocol_clean = True
    all_behavioral_gates = True

    for index, raw in enumerate(pairs):
        pair = _obj(raw, f"pairs[{index}]")
        _require(pair.get("schema") == PAIR_SCHEMA, f"pairs[{index}] schema drift")
        _require(pair.get("candidate_only") is True, f"pairs[{index}] candidate_only drift")
        identity = _obj(pair.get("pair_identity"), f"pairs[{index}].pair_identity")
        seed = identity.get("seed")
        _require(type(seed) is int and seed >= 0, f"pairs[{index}] seed malformed")

        baseline = _obj(pair.get("baseline"), f"pairs[{index}].baseline")
        candidate = _obj(pair.get("candidate"), f"pairs[{index}].candidate")
        comparison = _obj(pair.get("comparison"), f"pairs[{index}].comparison")

        baseline_sha = _sha(baseline.get("trajectory_sha256"), f"pairs[{index}] baseline trajectory")
        candidate_sha = _sha(candidate.get("trajectory_sha256"), f"pairs[{index}] candidate trajectory")
        _require(baseline_sha not in seen_baseline, "duplicate baseline trajectory evidence")
        _require(candidate_sha not in seen_candidate, "duplicate candidate trajectory evidence")
        seen_baseline.add(baseline_sha)
        seen_candidate.add(candidate_sha)

        _require(candidate.get("reviewed_identity_verified") is True, "pair reviewed V2.2 identity is not verified")
        for key, expected in REVIEWED_V22_IDENTITY.items():
            output_key = f"v2_2_{key}"
            _require(candidate.get(output_key) == expected, f"pair reviewed V2.2 identity mismatch: {key}")

        _require(comparison.get("verdict") in {"BETTER", "WORSE", "TIE"}, "pair verdict malformed")
        _num(comparison.get("net_kill_cost_delta"), "net_kill_cost_delta")
        all_protocol_clean = all_protocol_clean and _bool(comparison.get("protocol_clean"), "protocol_clean")
        behavioral = (
            _bool(comparison.get("force_preservation_pass"), "force_preservation_pass")
            and _bool(comparison.get("productive_contact_pass"), "productive_contact_pass")
            and _bool(comparison.get("attack_move_reduction_pass"), "attack_move_reduction_pass")
        )
        all_behavioral_gates = all_behavioral_gates and behavioral
        grouped.setdefault(seed, []).append(pair)

    summaries: dict[str, Any] = {}
    complete_held_out = 0
    any_complete_failure = False

    for seed, rows in sorted(grouped.items()):
        _require(len(rows) <= repeats_per_seed, f"seed {seed} exceeds repeat ceiling")
        comparisons = [_obj(row["comparison"], f"seed {seed} comparison") for row in rows]
        deltas = [_num(row.get("net_kill_cost_delta"), "net_kill_cost_delta") for row in comparisons]
        verdicts = [row.get("verdict") for row in comparisons]
        complete = len(rows) == repeats_per_seed
        better = verdicts.count("BETTER")
        worse = verdicts.count("WORSE")
        tie = verdicts.count("TIE")
        protocol_clean = all(row.get("protocol_clean") is True for row in comparisons)
        behavior_clean = all(
            row.get("force_preservation_pass") is True
            and row.get("productive_contact_pass") is True
            and row.get("attack_move_reduction_pass") is True
            for row in comparisons
        )
        median_delta = statistics.median(deltas)
        mean_delta = statistics.mean(deltas)

        gate_pass: bool | None = None
        if complete:
            if seed == regression_seed:
                gate_pass = median_delta >= 0 and worse <= 1 and protocol_clean and behavior_clean
            elif seed == gain_seed:
                gate_pass = median_delta > 0 and better >= 2 and protocol_clean and behavior_clean
            else:
                gate_pass = worse <= 1 and protocol_clean and behavior_clean
                complete_held_out += 1
            if gate_pass is False:
                any_complete_failure = True

        summaries[str(seed)] = {
            "pair_count": len(rows),
            "complete": complete,
            "better": better,
            "worse": worse,
            "tie": tie,
            "mean_net_delta": mean_delta,
            "median_net_delta": median_delta,
            "all_protocol_clean": protocol_clean,
            "all_behavioral_gates_pass": behavior_clean,
            "gate_pass": gate_pass,
        }

    regression_complete = str(regression_seed) in summaries and summaries[str(regression_seed)]["complete"]
    gain_complete = str(gain_seed) in summaries and summaries[str(gain_seed)]["complete"]
    enough_held_out = complete_held_out >= minimum_held_out_seed_count
    required_complete = regression_complete and gain_complete and enough_held_out

    if any_complete_failure:
        status = "REJECT"
    elif required_complete:
        required_rows = [
            value
            for seed, value in summaries.items()
            if int(seed) in {regression_seed, gain_seed}
            or (int(seed) not in {regression_seed, gain_seed} and value["complete"])
        ]
        status = "PASS" if all(row["gate_pass"] is True for row in required_rows) else "REJECT"
    else:
        status = "PENDING"

    return {
        "schema": MATRIX_SCHEMA,
        "candidate_only": True,
        "status": status,
        "reviewed_v2_2_identity": dict(REVIEWED_V22_IDENTITY),
        "requirements": {
            "regression_seed": regression_seed,
            "regression_seed_rule": "median net delta >= 0; <=1/3 worse; all protocol and behavioral gates pass",
            "gain_seed": gain_seed,
            "gain_seed_rule": "median net delta > 0; >=2/3 better; all protocol and behavioral gates pass",
            "minimum_held_out_seed_count": minimum_held_out_seed_count,
            "held_out_rule": "<=1/3 worse per complete seed; all protocol and behavioral gates pass",
            "repeats_per_seed": repeats_per_seed,
            "behavioral_gate": "force preserved; productive contact+damage; attack_move fraction <= 0.75",
        },
        "pair_count": len(pairs),
        "complete_held_out_seed_count": complete_held_out,
        "all_protocol_clean": all_protocol_clean,
        "all_behavioral_gates_pass": all_behavioral_gates,
        "by_seed": summaries,
        "authority": {
            "candidate_only": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }


def stable_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n"


def _read_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return _obj(value, str(path))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate reviewed Conditional Engagement V2.2 paired acceptance matrix")
    parser.add_argument("--pair-report", action="append", default=[])
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        reports = [_read_json(Path(path)) for path in args.pair_report]
        sys.stdout.write(stable_json(evaluate_matrix(reports)))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, PairContractError) as error:
        print(f"V2.2 matrix contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
