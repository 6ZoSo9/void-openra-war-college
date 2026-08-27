from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

PAIR_SCHEMA = "void.apollyon.conditional-engagement-pair-comparison.v1"
MATRIX_SCHEMA = "void.apollyon.conditional-engagement-pair-matrix.v1"
ANALYZER_MARKER = "VOID_WAR_COLLEGE_SPAR_TRAINING_UTILITY_V1"
PAIR_FIELDS = (
    "curriculum_id",
    "generation_id",
    "runtime_image_id",
    "engine_commit",
    "war_college_commit",
    "joint_training_attestation_sha256",
    "warm_start_sha256",
    "warm_start_handoff",
    "apollyon_model",
    "abaddon_controller_sha256",
    "abaddon_doctrine",
    "seed",
    "round_limit",
    "ticks_per_round",
)
AUTHORITY_FALSE = (
    "automatic_corpus_admission",
    "automatic_apollyon_weight_mutation",
    "automatic_abaddon_policy_promotion",
)


class PairContractError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PairContractError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _arr(value: Any, label: str) -> Sequence[Any]:
    _require(isinstance(value, Sequence) and not isinstance(value, (str, bytes)), f"{label} must be an array")
    return value


def _int(value: Any, label: str, minimum: int = 0) -> int:
    _require(type(value) is int and value >= minimum, f"{label} must be integer >= {minimum}")
    return value


def _num(value: Any, label: str) -> float:
    _require(type(value) in (int, float) and math.isfinite(float(value)), f"{label} must be finite number")
    return float(value)


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _clean_report(report: Mapping[str, Any], label: str) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    report = _obj(report, label)
    _require(report.get("marker") == ANALYZER_MARKER and report.get("version") == 1, f"{label} analyzer identity drift")
    provenance = _obj(report.get("provenance"), f"{label}.provenance")
    integrity = _obj(report.get("integrity"), f"{label}.integrity")
    authority = _obj(report.get("authority"), f"{label}.authority")
    _require(authority.get("candidate_only") is True and authority.get("review_required") is True, f"{label} authority wall drift")
    for key in AUTHORITY_FALSE:
        _require(authority.get(key) is False, f"{label} authority drift: {key}")
    for key in ("trajectory_verified", "summary_verified", "world_clock_contiguous", "perspective_accounting_consistent"):
        _require(integrity.get(key) is True, f"{label} integrity not proven: {key}")
    _int(integrity.get("rounds_completed"), f"{label}.rounds_completed", 1)
    sides = _obj(report.get("sides"), f"{label}.sides")
    for side in ("apollyon", "abaddon"):
        side_report = _obj(sides.get(side), f"{label}.sides.{side}")
        _int(side_report.get("final_combat_capable_units"), f"{label}.{side}.final_combat_capable_units")
        _num(side_report.get("net_kill_cost"), f"{label}.{side}.net_kill_cost")
        _obj(side_report.get("tools"), f"{label}.{side}.tools")
        _arr(side_report.get("retried_rounds"), f"{label}.{side}.retried_rounds")
    return provenance, integrity, sides


def _tool_fraction(side: Mapping[str, Any], tool: str, rounds: int) -> float:
    tools = _obj(side.get("tools"), "tools")
    count = tools.get(tool, 0)
    _require(type(count) is int and 0 <= count <= rounds, f"tool count malformed: {tool}")
    return count / rounds


def compare_reports(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
    *,
    expected_v2_candidate_sha256: str | None = None,
    expected_v2_source_commit: str | None = None,
) -> dict[str, Any]:
    bp, bi, bs = _clean_report(baseline, "baseline")
    cp, ci, cs = _clean_report(candidate, "candidate")

    for field in PAIR_FIELDS:
        _require(bp.get(field) == cp.get(field), f"pair identity mismatch: {field}")

    baseline_trajectory_sha = _sha256(bp.get("trajectory_sha256"), "baseline trajectory SHA-256")
    candidate_trajectory_sha = _sha256(cp.get("trajectory_sha256"), "candidate trajectory SHA-256")
    baseline_summary_sha = _sha256(bp.get("summary_sha256"), "baseline summary SHA-256")
    candidate_summary_sha = _sha256(cp.get("summary_sha256"), "candidate summary SHA-256")
    _require(baseline_trajectory_sha != candidate_trajectory_sha, "baseline and candidate trajectory SHA-256 must differ")

    bv2 = _obj(baseline.get("conditional_engagement_v2"), "baseline.conditional_engagement_v2")
    cv2 = _obj(candidate.get("conditional_engagement_v2"), "candidate.conditional_engagement_v2")
    _require(bv2.get("present") is False, "baseline unexpectedly contains Conditional Engagement V2")
    _require(cv2.get("present") is True, "candidate is missing Conditional Engagement V2")
    _require(cv2.get("all_round_receipts_verified") is True, "candidate V2 round receipts are not verified")
    _require(cv2.get("tool_surface_bound") is True, "candidate V2 tool surface is not bound")
    _require(cv2.get("accepted_tool_bound") is True, "candidate V2 accepted tool is not bound")
    _require(cv2.get("runtime_seed_branching") is False, "candidate V2 runtime seed branching detected")
    _require(cv2.get("rounds_verified") == ci.get("rounds_completed"), "candidate V2 verified-round count mismatch")

    if expected_v2_candidate_sha256 is not None:
        _require(cv2.get("candidate_sha256") == expected_v2_candidate_sha256, "unexpected V2 candidate SHA-256")
    if expected_v2_source_commit is not None:
        _require(cv2.get("source_commit") == expected_v2_source_commit, "unexpected V2 source commit")

    b_ap = _obj(bs["apollyon"], "baseline.apollyon")
    c_ap = _obj(cs["apollyon"], "candidate.apollyon")
    b_ab = _obj(bs["abaddon"], "baseline.abaddon")
    c_ab = _obj(cs["abaddon"], "candidate.abaddon")
    b_rounds = _int(bi["rounds_completed"], "baseline.rounds_completed", 1)
    c_rounds = _int(ci["rounds_completed"], "candidate.rounds_completed", 1)

    b_net = _num(b_ap["net_kill_cost"], "baseline.apollyon.net_kill_cost")
    c_net = _num(c_ap["net_kill_cost"], "candidate.apollyon.net_kill_cost")
    net_delta = c_net - b_net
    verdict = "BETTER" if net_delta > 0 else "WORSE" if net_delta < 0 else "TIE"

    b_retries = list(_arr(b_ap["retried_rounds"], "baseline.apollyon.retried_rounds"))
    c_retries = list(_arr(c_ap["retried_rounds"], "candidate.apollyon.retried_rounds"))
    protocol_clean = not b_retries and not c_retries

    return {
        "schema": PAIR_SCHEMA,
        "candidate_only": True,
        "pair_identity": {field: bp[field] for field in PAIR_FIELDS},
        "baseline": {
            "trajectory_sha256": baseline_trajectory_sha,
            "summary_sha256": baseline_summary_sha,
            "rounds_completed": b_rounds,
            "apollyon_net_kill_cost": b_net,
            "apollyon_final_combat": b_ap["final_combat_capable_units"],
            "abaddon_final_combat": b_ab["final_combat_capable_units"],
            "apollyon_attack_move_fraction": _tool_fraction(b_ap, "attack_move", b_rounds),
            "apollyon_attack_target_fraction": _tool_fraction(b_ap, "attack_target", b_rounds),
            "apollyon_retried_rounds": b_retries,
        },
        "candidate": {
            "trajectory_sha256": candidate_trajectory_sha,
            "summary_sha256": candidate_summary_sha,
            "rounds_completed": c_rounds,
            "v2_source_commit": cv2.get("source_commit"),
            "v2_candidate_sha256": cv2.get("candidate_sha256"),
            "v2_mode_counts": dict(sorted(_obj(cv2.get("mode_counts"), "candidate V2 mode_counts").items())),
            "apollyon_net_kill_cost": c_net,
            "apollyon_final_combat": c_ap["final_combat_capable_units"],
            "abaddon_final_combat": c_ab["final_combat_capable_units"],
            "apollyon_attack_move_fraction": _tool_fraction(c_ap, "attack_move", c_rounds),
            "apollyon_attack_target_fraction": _tool_fraction(c_ap, "attack_target", c_rounds),
            "apollyon_retried_rounds": c_retries,
        },
        "comparison": {
            "primary_metric": "apollyon_net_kill_cost_delta",
            "verdict": verdict,
            "net_kill_cost_delta": net_delta,
            "final_combat_delta": c_ap["final_combat_capable_units"] - b_ap["final_combat_capable_units"],
            "attack_move_fraction_delta": _tool_fraction(c_ap, "attack_move", c_rounds) - _tool_fraction(b_ap, "attack_move", b_rounds),
            "attack_target_fraction_delta": _tool_fraction(c_ap, "attack_target", c_rounds) - _tool_fraction(b_ap, "attack_target", b_rounds),
            "protocol_clean": protocol_clean,
            "all_accepted_actions_first_attempt": protocol_clean,
            "invalid_attempt_count_zero": protocol_clean,
        },
        "authority": {
            "candidate_only": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }


def evaluate_matrix(
    pairs: Sequence[Mapping[str, Any]],
    *,
    regression_seed: int = 2051,
    gain_seed: int = 2055,
    minimum_held_out_seed_count: int = 3,
    repeats_per_seed: int = 3,
) -> dict[str, Any]:
    _require(type(regression_seed) is int and regression_seed >= 0, "regression_seed malformed")
    _require(type(gain_seed) is int and gain_seed >= 0 and gain_seed != regression_seed, "gain_seed malformed")
    _require(type(minimum_held_out_seed_count) is int and minimum_held_out_seed_count >= 1, "held-out seed count malformed")
    _require(type(repeats_per_seed) is int and repeats_per_seed >= 1, "repeats_per_seed malformed")

    grouped: dict[int, list[Mapping[str, Any]]] = {}
    expected_candidate_sha = None
    expected_source_commit = None
    all_protocol_clean = True
    seen_baseline_trajectories: set[str] = set()
    seen_candidate_trajectories: set[str] = set()

    for index, pair in enumerate(pairs):
        pair = _obj(pair, f"pairs[{index}]")
        _require(pair.get("schema") == PAIR_SCHEMA and pair.get("candidate_only") is True, f"pairs[{index}] identity drift")
        identity = _obj(pair.get("pair_identity"), f"pairs[{index}].pair_identity")
        seed = _int(identity.get("seed"), f"pairs[{index}].seed")
        baseline = _obj(pair.get("baseline"), f"pairs[{index}].baseline")
        candidate = _obj(pair.get("candidate"), f"pairs[{index}].candidate")
        comparison = _obj(pair.get("comparison"), f"pairs[{index}].comparison")
        baseline_trajectory_sha = _sha256(baseline.get("trajectory_sha256"), f"pairs[{index}] baseline trajectory SHA-256")
        candidate_trajectory_sha = _sha256(candidate.get("trajectory_sha256"), f"pairs[{index}] candidate trajectory SHA-256")
        _require(baseline_trajectory_sha not in seen_baseline_trajectories, "duplicate baseline trajectory evidence")
        _require(candidate_trajectory_sha not in seen_candidate_trajectories, "duplicate candidate trajectory evidence")
        seen_baseline_trajectories.add(baseline_trajectory_sha)
        seen_candidate_trajectories.add(candidate_trajectory_sha)
        candidate_sha = candidate.get("v2_candidate_sha256")
        source_commit = candidate.get("v2_source_commit")
        _require(isinstance(candidate_sha, str) and candidate_sha, "pair candidate SHA missing")
        _require(isinstance(source_commit, str) and source_commit, "pair source commit missing")
        if expected_candidate_sha is None:
            expected_candidate_sha = candidate_sha
            expected_source_commit = source_commit
        _require(candidate_sha == expected_candidate_sha, "mixed V2 candidate SHA-256 generations")
        _require(source_commit == expected_source_commit, "mixed V2 source commit generations")
        all_protocol_clean = all_protocol_clean and comparison.get("protocol_clean") is True
        grouped.setdefault(seed, []).append(pair)

    summaries: dict[str, Any] = {}
    any_complete_failure = False

    for seed, rows in sorted(grouped.items()):
        deltas = [_num(_obj(row["comparison"], "comparison").get("net_kill_cost_delta"), "net_kill_cost_delta") for row in rows]
        verdicts = [_obj(row["comparison"], "comparison").get("verdict") for row in rows]
        _require(all(v in {"BETTER", "WORSE", "TIE"} for v in verdicts), f"seed {seed} verdict malformed")
        complete = len(rows) == repeats_per_seed
        _require(len(rows) <= repeats_per_seed, f"seed {seed} exceeds repeat ceiling")
        better = verdicts.count("BETTER")
        worse = verdicts.count("WORSE")
        tie = verdicts.count("TIE")
        summary = {
            "pair_count": len(rows),
            "complete": complete,
            "better": better,
            "worse": worse,
            "tie": tie,
            "mean_net_delta": statistics.mean(deltas),
            "median_net_delta": statistics.median(deltas),
            "all_protocol_clean": all(_obj(row["comparison"], "comparison").get("protocol_clean") is True for row in rows),
        }
        if complete:
            if seed == regression_seed:
                gate = summary["median_net_delta"] >= 0 and worse <= 1
            elif seed == gain_seed:
                gate = summary["median_net_delta"] > 0 and better >= 2
            else:
                gate = worse <= 1
            summary["gate_pass"] = gate
            any_complete_failure = any_complete_failure or not gate
        else:
            summary["gate_pass"] = None
        summaries[str(seed)] = summary

    held_out_complete = [seed for seed, rows in grouped.items() if seed not in {regression_seed, gain_seed} and len(rows) == repeats_per_seed]
    reviewed_complete = all(len(grouped.get(seed, [])) == repeats_per_seed for seed in (regression_seed, gain_seed))
    complete = reviewed_complete and len(held_out_complete) >= minimum_held_out_seed_count

    if not all_protocol_clean or any_complete_failure:
        status = "FAIL"
    elif complete:
        status = "PASS"
    else:
        status = "PENDING"

    return {
        "schema": MATRIX_SCHEMA,
        "candidate_only": True,
        "status": status,
        "v2_candidate_sha256": expected_candidate_sha,
        "v2_source_commit": expected_source_commit,
        "repeats_per_seed": repeats_per_seed,
        "regression_seed": regression_seed,
        "gain_seed": gain_seed,
        "minimum_held_out_seed_count": minimum_held_out_seed_count,
        "complete_held_out_seeds": sorted(held_out_complete),
        "all_protocol_clean": all_protocol_clean,
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
    raw = path.read_text(encoding="utf-8")
    value = json.loads(raw)
    return _obj(value, str(path))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed Conditional Engagement V2 pair/matrix comparison")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pair = sub.add_parser("pair")
    p_pair.add_argument("--baseline-report", required=True)
    p_pair.add_argument("--candidate-report", required=True)
    p_pair.add_argument("--expected-v2-candidate-sha256", required=True)
    p_pair.add_argument("--expected-v2-source-commit", required=True)

    p_matrix = sub.add_parser("matrix")
    p_matrix.add_argument("--pair-report", action="append", required=True)
    p_matrix.add_argument("--regression-seed", type=int, default=2051)
    p_matrix.add_argument("--gain-seed", type=int, default=2055)
    p_matrix.add_argument("--minimum-held-out-seed-count", type=int, default=3)
    p_matrix.add_argument("--repeats-per-seed", type=int, default=3)

    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "pair":
            result = compare_reports(
                _read_json(Path(args.baseline_report)),
                _read_json(Path(args.candidate_report)),
                expected_v2_candidate_sha256=args.expected_v2_candidate_sha256,
                expected_v2_source_commit=args.expected_v2_source_commit,
            )
        else:
            result = evaluate_matrix(
                [_read_json(Path(path)) for path in args.pair_report],
                regression_seed=args.regression_seed,
                gain_seed=args.gain_seed,
                minimum_held_out_seed_count=args.minimum_held_out_seed_count,
                repeats_per_seed=args.repeats_per_seed,
            )
        sys.stdout.write(stable_json(result))
        return 0
    except (OSError, json.JSONDecodeError, PairContractError) as error:
        print(f"pair contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
