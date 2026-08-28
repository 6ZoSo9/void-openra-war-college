from __future__ import annotations

import json
import statistics
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from openra_env.learning.general_brain_generation import manifest_sha256, validate_brain_manifest
from openra_env.learning.general_brain_training import (
    PROMOTION_EVALUATION_SCHEMA,
    evaluate_promotion,
)

from .general_brain_challenger_pair import PAIR_SCHEMA

CAMPAIGN_SCHEMA = "void.general-brain-challenger-campaign.v1"
SEED_ORDER = (2051, 2055, 2052, 2053, 2054)
REQUIRED_PER_SEED = 3
REQUIRED_PAIR_COUNT = len(SEED_ORDER) * REQUIRED_PER_SEED


class ChallengerCampaignError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ChallengerCampaignError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _seed_report(seed: int, rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    deltas = [float(_obj(row.get("comparison"), "pair comparison")["net_kill_cost_delta"]) for row in rows]
    worse = sum(float(value) < 0 for value in deltas)
    better = sum(float(value) > 0 for value in deltas)
    tie = sum(float(value) == 0 for value in deltas)
    complete = len(rows) == REQUIRED_PER_SEED
    median = statistics.median(deltas) if deltas else None
    return {
        "seed": seed,
        "pair_count": len(rows),
        "complete": complete,
        "median_challenger_minus_incumbent": median,
        "better_pairs": better,
        "worse_pairs": worse,
        "tie_pairs": tie,
        "all_protocol_clean": all(
            _obj(row.get("comparison"), "pair comparison").get("protocol_clean") is True
            for row in rows
        ),
        "all_behavioral_gates_pass": all(
            _obj(row.get("comparison"), "pair comparison").get("behavioral_gates_pass") is True
            for row in rows
        ),
    }


def build_challenger_campaign(
    pair_reports: Sequence[Mapping[str, Any]],
    *,
    incumbent_manifest: Mapping[str, Any],
    challenger_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    validate_brain_manifest(incumbent_manifest)
    validate_brain_manifest(challenger_manifest)
    incumbent_sha = manifest_sha256(incumbent_manifest)
    challenger_sha = manifest_sha256(challenger_manifest)
    _require(incumbent_manifest.get("general_id") == "apollyon", "incumbent must be Apollyon")
    _require(challenger_manifest.get("general_id") == "apollyon", "challenger must be Apollyon")
    _require(incumbent_manifest.get("generation") == 0, "incumbent generation must be 0")
    _require(challenger_manifest.get("generation") == 1, "challenger generation must be 1")

    by_seed: dict[int, list[Mapping[str, Any]]] = {seed: [] for seed in SEED_ORDER}
    seen_incumbent: set[str] = set()
    seen_challenger: set[str] = set()
    adapter_sha: str | None = None

    for index, raw in enumerate(pair_reports):
        row = _obj(raw, f"pair report {index}")
        _require(row.get("schema") == PAIR_SCHEMA, "pair report schema drift")
        _require(row.get("general_id") == "apollyon", "pair general_id drift")
        _require(row.get("incumbent_manifest_sha256") == incumbent_sha, "pair incumbent manifest drift")
        _require(row.get("challenger_manifest_sha256") == challenger_sha, "pair challenger manifest drift")
        current_adapter = row.get("adapter_sha256")
        _require(isinstance(current_adapter, str) and len(current_adapter) == 64, "pair adapter SHA malformed")
        if adapter_sha is None:
            adapter_sha = current_adapter
        _require(current_adapter == adapter_sha, "campaign mixes challenger adapter artifacts")
        identity = _obj(row.get("pair_identity"), "pair identity")
        seed = identity.get("seed")
        _require(seed in by_seed, f"unreviewed promotion seed: {seed}")
        incumbent = _obj(row.get("incumbent"), "pair incumbent")
        challenger = _obj(row.get("challenger"), "pair challenger")
        inc_traj = incumbent.get("trajectory_sha256")
        chal_traj = challenger.get("trajectory_sha256")
        _require(isinstance(inc_traj, str) and len(inc_traj) == 64, "incumbent trajectory SHA malformed")
        _require(isinstance(chal_traj, str) and len(chal_traj) == 64, "challenger trajectory SHA malformed")
        _require(inc_traj not in seen_incumbent, "duplicate incumbent trajectory evidence")
        _require(chal_traj not in seen_challenger, "duplicate challenger trajectory evidence")
        seen_incumbent.add(inc_traj)
        seen_challenger.add(chal_traj)
        by_seed[int(seed)].append(row)
        _require(len(by_seed[int(seed)]) <= REQUIRED_PER_SEED, f"too many pairs for seed {seed}")

    seed_reports = {seed: _seed_report(seed, by_seed[seed]) for seed in SEED_ORDER}
    all_protocol_clean = all(
        report["all_protocol_clean"] for report in seed_reports.values() if report["pair_count"]
    )
    all_behavioral = all(
        report["all_behavioral_gates_pass"] for report in seed_reports.values() if report["pair_count"]
    )

    regression = seed_reports[2051]
    gain = seed_reports[2055]
    heldouts = {str(seed): seed_reports[seed] for seed in (2052, 2053, 2054)}

    terminal_reject = False
    if regression["complete"] and (
        regression["median_challenger_minus_incumbent"] < 0
        or regression["worse_pairs"] > 1
        or not regression["all_protocol_clean"]
        or not regression["all_behavioral_gates_pass"]
    ):
        terminal_reject = True
    if gain["complete"] and (
        gain["median_challenger_minus_incumbent"] <= 0
        or gain["better_pairs"] < 2
        or not gain["all_protocol_clean"]
        or not gain["all_behavioral_gates_pass"]
    ):
        terminal_reject = True
    for report in heldouts.values():
        if report["complete"] and (
            report["worse_pairs"] > 1
            or not report["all_protocol_clean"]
            or not report["all_behavioral_gates_pass"]
        ):
            terminal_reject = True

    complete = len(pair_reports) == REQUIRED_PAIR_COUNT and all(
        report["complete"] for report in seed_reports.values()
    )
    if terminal_reject:
        status = "REJECT"
    elif complete:
        status = "PASS"
    else:
        status = "PENDING"

    evaluation = {
        "schema": PROMOTION_EVALUATION_SCHEMA,
        "incumbent_manifest_sha256": incumbent_sha,
        "challenger_manifest_sha256": challenger_sha,
        "authority_envelope_match": incumbent_manifest.get("authority_envelope") == challenger_manifest.get("authority_envelope"),
        "all_protocol_clean": complete and all_protocol_clean,
        "all_behavioral_gates_pass": complete and all_behavioral,
        "critical_seeds": {
            "2051": regression,
            "2055": gain,
        },
        "heldout_seeds": heldouts,
    }
    promotion = evaluate_promotion(incumbent_manifest, challenger_manifest, evaluation)

    return {
        "schema": CAMPAIGN_SCHEMA,
        "general_id": "apollyon",
        "incumbent_generation": 0,
        "challenger_generation": 1,
        "adapter_sha256": adapter_sha,
        "status": status,
        "observed_pair_count": len(pair_reports),
        "required_pair_count": REQUIRED_PAIR_COUNT,
        "remaining_pair_count": REQUIRED_PAIR_COUNT - len(pair_reports),
        "seed_order": list(SEED_ORDER),
        "required_pairs_per_seed": REQUIRED_PER_SEED,
        "by_seed": {str(seed): seed_reports[seed] for seed in SEED_ORDER},
        "promotion_evaluation": evaluation,
        "promotion_decision": promotion,
        "automatic_weight_install": False,
        "automatic_promotion": False,
        "review_required": True,
    }


def _read_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, Mapping), f"{path} must contain an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Aggregate General Brain incumbent/challenger pair reports")
    parser.add_argument("--incumbent-manifest", required=True)
    parser.add_argument("--challenger-manifest", required=True)
    parser.add_argument("--pair-report", action="append", default=[])
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        report = build_challenger_campaign(
            [_read_json(Path(path)) for path in args.pair_report],
            incumbent_manifest=_read_json(Path(args.incumbent_manifest)),
            challenger_manifest=_read_json(Path(args.challenger_manifest)),
        )
        sys.stdout.write(json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ChallengerCampaignError, ValueError) as error:
        print(f"General Brain challenger campaign error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
