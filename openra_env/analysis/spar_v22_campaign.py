from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .spar_v22_matrix import (
    REVIEWED_GAIN_SEED,
    REVIEWED_REGRESSION_SEED,
    REPEATS_PER_SEED,
    evaluate_matrix,
)
from .spar_v22_pair_comparison import PAIR_SCHEMA, PairContractError

CAMPAIGN_SCHEMA = "void.apollyon.conditional-engagement-v2-2-validation-campaign.v1"
REVIEWED_HELD_OUT_SEEDS = (2052, 2053, 2054)
REVIEWED_CAMPAIGN_SEEDS = (
    REVIEWED_REGRESSION_SEED,
    REVIEWED_GAIN_SEED,
    *REVIEWED_HELD_OUT_SEEDS,
)
REVIEWED_PAIR_COUNT = len(REVIEWED_CAMPAIGN_SEEDS) * REPEATS_PER_SEED


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PairContractError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _seed_role(seed: int) -> str:
    if seed == REVIEWED_REGRESSION_SEED:
        return "regression"
    if seed == REVIEWED_GAIN_SEED:
        return "gain"
    _require(seed in REVIEWED_HELD_OUT_SEEDS, f"seed {seed} is not in reviewed V2.2 campaign")
    return "held_out"


def reviewed_plan() -> dict[str, Any]:
    return {
        "schema": CAMPAIGN_SCHEMA,
        "candidate_only": True,
        "seeds": [
            {
                "seed": seed,
                "role": _seed_role(seed),
                "required_pairs": REPEATS_PER_SEED,
            }
            for seed in REVIEWED_CAMPAIGN_SEEDS
        ],
        "required_pair_count": REVIEWED_PAIR_COUNT,
        "authority": {
            "candidate_only": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }


def evaluate_campaign(pairs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    counts = {seed: 0 for seed in REVIEWED_CAMPAIGN_SEEDS}

    for index, raw in enumerate(pairs):
        pair = _obj(raw, f"pairs[{index}]")
        _require(pair.get("schema") == PAIR_SCHEMA, f"pairs[{index}] schema drift")
        identity = _obj(pair.get("pair_identity"), f"pairs[{index}].pair_identity")
        seed = identity.get("seed")
        _require(type(seed) is int, f"pairs[{index}] seed malformed")
        _require(seed in counts, f"seed {seed} is not in reviewed V2.2 campaign")
        counts[seed] += 1
        _require(
            counts[seed] <= REPEATS_PER_SEED,
            f"seed {seed} exceeds reviewed repeat ceiling",
        )

    matrix = evaluate_matrix(
        pairs,
        regression_seed=REVIEWED_REGRESSION_SEED,
        gain_seed=REVIEWED_GAIN_SEED,
        minimum_held_out_seed_count=len(REVIEWED_HELD_OUT_SEEDS),
        repeats_per_seed=REPEATS_PER_SEED,
    )

    remaining_by_seed = {
        str(seed): REPEATS_PER_SEED - counts[seed]
        for seed in REVIEWED_CAMPAIGN_SEEDS
    }
    remaining_pair_count = sum(remaining_by_seed.values())
    complete = remaining_pair_count == 0

    if matrix["status"] == "REJECT":
        status = "REJECT"
    elif complete:
        _require(matrix["status"] == "PASS", "complete campaign did not produce terminal matrix verdict")
        status = "PASS"
    else:
        status = "PENDING"

    next_required_pairs = [
        {
            "seed": seed,
            "role": _seed_role(seed),
            "remaining_pairs": remaining_by_seed[str(seed)],
        }
        for seed in REVIEWED_CAMPAIGN_SEEDS
        if remaining_by_seed[str(seed)] > 0
    ]

    return {
        "schema": CAMPAIGN_SCHEMA,
        "candidate_only": True,
        "status": status,
        "campaign_complete": complete,
        "required_pair_count": REVIEWED_PAIR_COUNT,
        "observed_pair_count": len(pairs),
        "remaining_pair_count": remaining_pair_count,
        "completed_by_seed": {str(seed): counts[seed] for seed in REVIEWED_CAMPAIGN_SEEDS},
        "remaining_by_seed": remaining_by_seed,
        "next_required_pairs": next_required_pairs,
        "matrix": matrix,
        "authority": {
            "candidate_only": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }


def stable_json(value: Mapping[str, Any]) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"


def _read_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return _obj(value, str(path))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate and resume the frozen Conditional Engagement V2.2 acceptance campaign"
    )
    parser.add_argument("--pair-report", action="append", default=[])
    parser.add_argument("--print-plan", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.print_plan:
            _require(not args.pair_report, "--print-plan cannot be combined with pair evidence")
            sys.stdout.write(stable_json(reviewed_plan()))
            return 0
        reports = [_read_json(Path(path)) for path in args.pair_report]
        sys.stdout.write(stable_json(evaluate_campaign(reports)))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, PairContractError) as error:
        print(f"V2.2 campaign contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
