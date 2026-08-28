from __future__ import annotations

import json
import math
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from ._spar_conditional_v2_1_reviewed_identity import REVIEWED_V21_IDENTITY

PAIR_SCHEMA = "void.apollyon.conditional-engagement-v2-1-pair-comparison.v1"
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
IDENTITY_OUTPUT_KEYS = {
    "source_commit": "v2_1_source_commit",
    "candidate_sha256": "v2_1_candidate_sha256",
    "policy_sha256": "v2_1_policy_sha256",
    "session_sha256": "v2_1_session_sha256",
    "wrapper_sha256": "v2_1_wrapper_sha256",
}


class PairContractError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PairContractError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _arr(value: Any, label: str) -> Sequence[Any]:
    _require(
        isinstance(value, Sequence) and not isinstance(value, (str, bytes)),
        f"{label} must be an array",
    )
    return value


def _int(value: Any, label: str, minimum: int = 0) -> int:
    _require(type(value) is int and value >= minimum, f"{label} must be integer >= {minimum}")
    return value


def _num(value: Any, label: str) -> float:
    _require(
        type(value) in (int, float) and math.isfinite(float(value)),
        f"{label} must be finite number",
    )
    return float(value)


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _clean_report(
    report: Mapping[str, Any], label: str
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    report = _obj(report, label)
    _require(
        report.get("marker") == ANALYZER_MARKER and report.get("version") == 1,
        f"{label} analyzer identity drift",
    )
    provenance = _obj(report.get("provenance"), f"{label}.provenance")
    integrity = _obj(report.get("integrity"), f"{label}.integrity")
    authority = _obj(report.get("authority"), f"{label}.authority")
    _require(
        authority.get("candidate_only") is True
        and authority.get("review_required") is True,
        f"{label} authority wall drift",
    )
    for key in AUTHORITY_FALSE:
        _require(authority.get(key) is False, f"{label} authority drift: {key}")
    for key in (
        "trajectory_verified",
        "summary_verified",
        "world_clock_contiguous",
        "perspective_accounting_consistent",
    ):
        _require(integrity.get(key) is True, f"{label} integrity not proven: {key}")
    _int(integrity.get("rounds_completed"), f"{label}.rounds_completed", 1)
    sides = _obj(report.get("sides"), f"{label}.sides")
    for side in ("apollyon", "abaddon"):
        side_report = _obj(sides.get(side), f"{label}.sides.{side}")
        _int(
            side_report.get("final_combat_capable_units"),
            f"{label}.{side}.final_combat_capable_units",
        )
        _num(side_report.get("net_kill_cost"), f"{label}.{side}.net_kill_cost")
        _obj(side_report.get("tools"), f"{label}.{side}.tools")
        _arr(side_report.get("retried_rounds"), f"{label}.{side}.retried_rounds")
    return provenance, integrity, sides


def _tool_fraction(side: Mapping[str, Any], tool: str, rounds: int) -> float:
    tools = _obj(side.get("tools"), "tools")
    count = tools.get(tool, 0)
    _require(type(count) is int and 0 <= count <= rounds, f"tool count malformed: {tool}")
    return count / rounds


def _require_absent_generation(report: Mapping[str, Any], key: str, label: str) -> None:
    generation = _obj(report.get(key), f"{label}.{key}")
    _require(generation.get("present") is False, f"{label} unexpectedly contains {key}")


def _require_reviewed_v21_identity(v21: Mapping[str, Any]) -> None:
    _require(
        v21.get("reviewed_identity_verified") is True,
        "candidate reviewed V2.1 identity is not verified",
    )
    for key, expected in REVIEWED_V21_IDENTITY.items():
        _require(v21.get(key) == expected, f"candidate reviewed V2.1 identity mismatch: {key}")


def compare_reports(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    """Compare one original-baseline/V2.1 exact pair.

    The primary verdict remains Apollyon net-kill-cost delta. V2.1 additionally
    carries a force-preservation gate because V2's useful +force-survival effect
    must not be discarded by the refinement.
    """
    bp, bi, bs = _clean_report(baseline, "baseline")
    cp, ci, cs = _clean_report(candidate, "candidate")

    for field in PAIR_FIELDS:
        _require(bp.get(field) == cp.get(field), f"pair identity mismatch: {field}")

    baseline_trajectory_sha = _sha256(bp.get("trajectory_sha256"), "baseline trajectory SHA-256")
    candidate_trajectory_sha = _sha256(cp.get("trajectory_sha256"), "candidate trajectory SHA-256")
    baseline_summary_sha = _sha256(bp.get("summary_sha256"), "baseline summary SHA-256")
    candidate_summary_sha = _sha256(cp.get("summary_sha256"), "candidate summary SHA-256")
    _require(
        baseline_trajectory_sha != candidate_trajectory_sha,
        "baseline and candidate trajectory SHA-256 must differ",
    )

    _require_absent_generation(baseline, "conditional_engagement_v2", "baseline")
    _require_absent_generation(baseline, "conditional_engagement_v2_1", "baseline")
    _require_absent_generation(candidate, "conditional_engagement_v2", "candidate")
    cv21 = _obj(
        candidate.get("conditional_engagement_v2_1"),
        "candidate.conditional_engagement_v2_1",
    )
    _require(cv21.get("present") is True, "candidate is missing Conditional Engagement V2.1")
    _require_reviewed_v21_identity(cv21)
    _require(
        cv21.get("all_round_receipts_verified") is True,
        "candidate V2.1 round receipts are not verified",
    )
    _require(
        cv21.get("tool_surface_bound") is True,
        "candidate V2.1 tool surface is not bound",
    )
    _require(
        cv21.get("accepted_tool_bound") is True,
        "candidate V2.1 accepted tool is not bound",
    )
    _require(
        cv21.get("runtime_seed_branching") is False,
        "candidate V2.1 runtime seed branching detected",
    )
    _require(
        cv21.get("rounds_verified") == ci.get("rounds_completed"),
        "candidate V2.1 verified-round count mismatch",
    )

    b_ap = _obj(bs["apollyon"], "baseline.apollyon")
    c_ap = _obj(cs["apollyon"], "candidate.apollyon")
    b_ab = _obj(bs["abaddon"], "baseline.abaddon")
    c_ab = _obj(cs["abaddon"], "candidate.abaddon")
    b_rounds = _int(bi["rounds_completed"], "baseline.rounds_completed", 1)
    c_rounds = _int(ci["rounds_completed"], "candidate.rounds_completed", 1)

    b_net = _num(b_ap["net_kill_cost"], "baseline.apollyon.net_kill_cost")
    c_net = _num(c_ap["net_kill_cost"], "candidate.apollyon.net_kill_cost")
    net_delta = c_net - b_net
    final_combat_delta = (
        c_ap["final_combat_capable_units"] - b_ap["final_combat_capable_units"]
    )
    verdict = "BETTER" if net_delta > 0 else "WORSE" if net_delta < 0 else "TIE"

    b_ap_retries = list(_arr(b_ap["retried_rounds"], "baseline.apollyon.retried_rounds"))
    c_ap_retries = list(_arr(c_ap["retried_rounds"], "candidate.apollyon.retried_rounds"))
    b_ab_retries = list(_arr(b_ab["retried_rounds"], "baseline.abaddon.retried_rounds"))
    c_ab_retries = list(_arr(c_ab["retried_rounds"], "candidate.abaddon.retried_rounds"))
    protocol_clean = not any((b_ap_retries, c_ap_retries, b_ab_retries, c_ab_retries))
    force_preservation_pass = final_combat_delta >= 0
    minimum_seed_2060_gate_pass = (
        net_delta >= 0 and force_preservation_pass and protocol_clean
    )

    candidate_identity = {
        IDENTITY_OUTPUT_KEYS[key]: cv21[key] for key in REVIEWED_V21_IDENTITY
    }
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
            "apollyon_retried_rounds": b_ap_retries,
            "abaddon_retried_rounds": b_ab_retries,
        },
        "candidate": {
            "trajectory_sha256": candidate_trajectory_sha,
            "summary_sha256": candidate_summary_sha,
            "rounds_completed": c_rounds,
            "reviewed_identity_verified": True,
            **candidate_identity,
            "v2_1_mode_counts": dict(
                sorted(_obj(cv21.get("mode_counts"), "candidate V2.1 mode_counts").items())
            ),
            "apollyon_net_kill_cost": c_net,
            "apollyon_final_combat": c_ap["final_combat_capable_units"],
            "abaddon_final_combat": c_ab["final_combat_capable_units"],
            "apollyon_attack_move_fraction": _tool_fraction(c_ap, "attack_move", c_rounds),
            "apollyon_attack_target_fraction": _tool_fraction(c_ap, "attack_target", c_rounds),
            "apollyon_retried_rounds": c_ap_retries,
            "abaddon_retried_rounds": c_ab_retries,
        },
        "comparison": {
            "primary_metric": "apollyon_net_kill_cost_delta",
            "verdict": verdict,
            "net_kill_cost_delta": net_delta,
            "final_combat_delta": final_combat_delta,
            "force_preservation_pass": force_preservation_pass,
            "minimum_seed_2060_gate_pass": minimum_seed_2060_gate_pass,
            "attack_move_fraction_delta": (
                _tool_fraction(c_ap, "attack_move", c_rounds)
                - _tool_fraction(b_ap, "attack_move", b_rounds)
            ),
            "attack_target_fraction_delta": (
                _tool_fraction(c_ap, "attack_target", c_rounds)
                - _tool_fraction(b_ap, "attack_target", b_rounds)
            ),
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
    import argparse

    parser = argparse.ArgumentParser(description="Fail-closed Conditional Engagement V2.1 pair comparison")
    parser.add_argument("--baseline-report", required=True)
    parser.add_argument("--candidate-report", required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        sys.stdout.write(
            stable_json(
                compare_reports(
                    _read_json(Path(args.baseline_report)),
                    _read_json(Path(args.candidate_report)),
                )
            )
        )
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, PairContractError) as error:
        print(f"V2.1 pair contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
