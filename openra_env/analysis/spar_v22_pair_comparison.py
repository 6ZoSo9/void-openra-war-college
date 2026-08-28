from __future__ import annotations

import json
import math
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from ._spar_conditional_v2_2_reviewed_identity import REVIEWED_V22_IDENTITY

PAIR_SCHEMA = "void.apollyon.conditional-engagement-v2-2-pair-comparison.v2"
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
    "source_commit": "v2_2_source_commit",
    "candidate_sha256": "v2_2_candidate_sha256",
    "policy_sha256": "v2_2_policy_sha256",
    "session_sha256": "v2_2_session_sha256",
    "wrapper_sha256": "v2_2_wrapper_sha256",
}
ATTACK_MOVE_FRACTION_MAXIMUM = 0.75


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
        _arr(side_report.get("contact_rounds"), f"{label}.{side}.contact_rounds")
    return provenance, integrity, sides


def _tool_fraction(side: Mapping[str, Any], tool: str, rounds: int) -> float:
    tools = _obj(side.get("tools"), "tools")
    count = tools.get(tool, 0)
    _require(type(count) is int and 0 <= count <= rounds, f"tool count malformed: {tool}")
    return count / rounds


def _require_absent_generation(report: Mapping[str, Any], key: str, label: str) -> None:
    generation = _obj(report.get(key), f"{label}.{key}")
    _require(generation.get("present") is False, f"{label} unexpectedly contains {key}")


def _require_reviewed_v22_identity(v22: Mapping[str, Any]) -> None:
    _require(v22.get("reviewed_identity_verified") is True, "candidate reviewed V2.2 identity is not verified")
    for key, expected in REVIEWED_V22_IDENTITY.items():
        _require(v22.get(key) == expected, f"candidate reviewed V2.2 identity mismatch: {key}")


def _conversion_utility(report: Mapping[str, Any], *, present: bool, label: str) -> Mapping[str, Any]:
    utility = _obj(
        report.get("conditional_engagement_v2_2_conversion_utility"),
        f"{label}.conditional_engagement_v2_2_conversion_utility",
    )
    _require(utility.get("present") is present, f"{label} V2.2 conversion utility presence mismatch")
    return utility


def compare_reports(baseline: Mapping[str, Any], candidate: Mapping[str, Any]) -> dict[str, Any]:
    bp, bi, bs = _clean_report(baseline, "baseline")
    cp, ci, cs = _clean_report(candidate, "candidate")

    for field in PAIR_FIELDS:
        _require(bp.get(field) == cp.get(field), f"pair identity mismatch: {field}")

    baseline_trajectory_sha = _sha256(bp.get("trajectory_sha256"), "baseline trajectory SHA-256")
    candidate_trajectory_sha = _sha256(cp.get("trajectory_sha256"), "candidate trajectory SHA-256")
    baseline_summary_sha = _sha256(bp.get("summary_sha256"), "baseline summary SHA-256")
    candidate_summary_sha = _sha256(cp.get("summary_sha256"), "candidate summary SHA-256")
    _require(baseline_trajectory_sha != candidate_trajectory_sha, "baseline and candidate trajectory SHA-256 must differ")

    for key in ("conditional_engagement_v2", "conditional_engagement_v2_1", "conditional_engagement_v2_2"):
        _require_absent_generation(baseline, key, "baseline")
    _conversion_utility(baseline, present=False, label="baseline")

    for key in ("conditional_engagement_v2", "conditional_engagement_v2_1"):
        _require_absent_generation(candidate, key, "candidate")
    cv22 = _obj(candidate.get("conditional_engagement_v2_2"), "candidate.conditional_engagement_v2_2")
    _require(cv22.get("present") is True, "candidate is missing Conditional Engagement V2.2")
    _require_reviewed_v22_identity(cv22)
    for key in ("all_round_receipts_verified", "tool_surface_bound", "accepted_tool_bound", "action_compliance_bound"):
        _require(cv22.get(key) is True, f"candidate V2.2 evidence not proven: {key}")
    _require(cv22.get("runtime_seed_branching") is False, "candidate V2.2 runtime seed branching detected")
    _require(cv22.get("rounds_verified") == ci.get("rounds_completed"), "candidate V2.2 verified-round count mismatch")

    conversion = _conversion_utility(candidate, present=True, label="candidate")
    _require(conversion.get("reviewed_identity_verified") is True, "candidate conversion utility lacks reviewed identity")
    _require(
        conversion.get("trajectory_sha256") == candidate_trajectory_sha,
        "candidate conversion utility trajectory binding mismatch",
    )
    _require(
        conversion.get("v2_2_candidate_sha256") == cv22.get("candidate_sha256"),
        "candidate conversion utility candidate identity mismatch",
    )
    _require(
        conversion.get("rounds_verified") == ci.get("rounds_completed"),
        "candidate conversion utility verified-round count mismatch",
    )
    conversion_applicable = conversion.get("conversion_productivity_applicable")
    _require(type(conversion_applicable) is bool, "candidate conversion applicability must be bool")
    post_conversion_productivity_pass = conversion.get("post_conversion_productivity_pass")
    _require(type(post_conversion_productivity_pass) is bool, "candidate post-conversion productivity must be bool")
    first_conversion_round = conversion.get("first_conversion_round")
    if conversion_applicable:
        _require(type(first_conversion_round) is int and first_conversion_round >= 1, "candidate first conversion round malformed")
    else:
        _require(first_conversion_round is None, "candidate first conversion round present while not applicable")

    b_ap = _obj(bs["apollyon"], "baseline.apollyon")
    c_ap = _obj(cs["apollyon"], "candidate.apollyon")
    b_ab = _obj(bs["abaddon"], "baseline.abaddon")
    c_ab = _obj(cs["abaddon"], "candidate.abaddon")
    b_rounds = _int(bi["rounds_completed"], "baseline.rounds_completed", 1)
    c_rounds = _int(ci["rounds_completed"], "candidate.rounds_completed", 1)

    b_net = _num(b_ap["net_kill_cost"], "baseline.apollyon.net_kill_cost")
    c_net = _num(c_ap["net_kill_cost"], "candidate.apollyon.net_kill_cost")
    net_delta = c_net - b_net
    final_combat_delta = c_ap["final_combat_capable_units"] - b_ap["final_combat_capable_units"]
    verdict = "BETTER" if net_delta > 0 else "WORSE" if net_delta < 0 else "TIE"

    b_ap_retries = list(_arr(b_ap["retried_rounds"], "baseline.apollyon.retried_rounds"))
    c_ap_retries = list(_arr(c_ap["retried_rounds"], "candidate.apollyon.retried_rounds"))
    b_ab_retries = list(_arr(b_ab["retried_rounds"], "baseline.abaddon.retried_rounds"))
    c_ab_retries = list(_arr(c_ab["retried_rounds"], "candidate.abaddon.retried_rounds"))
    protocol_clean = not any((b_ap_retries, c_ap_retries, b_ab_retries, c_ab_retries))

    candidate_contact_rounds = list(_arr(c_ap["contact_rounds"], "candidate.apollyon.contact_rounds"))
    damage_inflicted = c_ap.get("first_damage_inflicted") is not None
    overall_productive_contact_pass = len(candidate_contact_rounds) >= 1 and damage_inflicted
    productive_contact_pass = overall_productive_contact_pass and post_conversion_productivity_pass
    attack_move_fraction = _tool_fraction(c_ap, "attack_move", c_rounds)
    attack_move_reduction_pass = attack_move_fraction <= ATTACK_MOVE_FRACTION_MAXIMUM
    force_preservation_pass = final_combat_delta >= 0
    minimum_seed_2060_gate_pass = (
        net_delta >= 0
        and force_preservation_pass
        and protocol_clean
        and productive_contact_pass
        and attack_move_reduction_pass
    )

    candidate_identity = {IDENTITY_OUTPUT_KEYS[key]: cv22[key] for key in REVIEWED_V22_IDENTITY}
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
            "apollyon_contact_round_count": len(_arr(b_ap["contact_rounds"], "baseline.apollyon.contact_rounds")),
            "apollyon_retried_rounds": b_ap_retries,
            "abaddon_retried_rounds": b_ab_retries,
        },
        "candidate": {
            "trajectory_sha256": candidate_trajectory_sha,
            "summary_sha256": candidate_summary_sha,
            "rounds_completed": c_rounds,
            "reviewed_identity_verified": True,
            **candidate_identity,
            "v2_2_mode_counts": dict(sorted(_obj(cv22.get("mode_counts"), "candidate V2.2 mode counts").items())),
            "attack_move_discouraged_rounds": _int(cv22.get("attack_move_discouraged_rounds"), "candidate attack_move_discouraged_rounds"),
            "followed_non_attack_move_rounds": _int(cv22.get("followed_non_attack_move_rounds"), "candidate followed_non_attack_move_rounds"),
            "ignored_attack_move_discouragement_rounds": _int(cv22.get("ignored_attack_move_discouragement_rounds"), "candidate ignored_attack_move_discouragement_rounds"),
            "preferred_move_units_offered_rounds": _int(cv22.get("preferred_move_units_offered_rounds"), "candidate preferred_move_units_offered_rounds"),
            "preferred_move_units_selected_rounds": _int(cv22.get("preferred_move_units_selected_rounds"), "candidate preferred_move_units_selected_rounds"),
            "apollyon_net_kill_cost": c_net,
            "apollyon_final_combat": c_ap["final_combat_capable_units"],
            "abaddon_final_combat": c_ab["final_combat_capable_units"],
            "apollyon_attack_move_fraction": attack_move_fraction,
            "apollyon_attack_target_fraction": _tool_fraction(c_ap, "attack_target", c_rounds),
            "apollyon_contact_round_count": len(candidate_contact_rounds),
            "apollyon_damage_inflicted": damage_inflicted,
            "conversion_productivity_applicable": conversion_applicable,
            "post_conversion_productivity_pass": post_conversion_productivity_pass,
            "first_conversion_round": first_conversion_round,
            "first_contact_round_after_conversion": conversion.get("first_contact_round_after_conversion"),
            "first_damage_round_after_conversion": conversion.get("first_damage_round_after_conversion"),
            "post_conversion_contact_round_count": len(_arr(conversion.get("post_conversion_contact_rounds"), "candidate post_conversion_contact_rounds")),
            "post_conversion_damage_round_count": len(_arr(conversion.get("post_conversion_damage_rounds"), "candidate post_conversion_damage_rounds")),
            "post_conversion_attack_move_fraction": _num(conversion.get("post_conversion_attack_move_fraction"), "candidate post_conversion_attack_move_fraction"),
            "apollyon_retried_rounds": c_ap_retries,
            "abaddon_retried_rounds": c_ab_retries,
        },
        "comparison": {
            "primary_metric": "apollyon_net_kill_cost_delta",
            "verdict": verdict,
            "net_kill_cost_delta": net_delta,
            "final_combat_delta": final_combat_delta,
            "force_preservation_pass": force_preservation_pass,
            "overall_productive_contact_pass": overall_productive_contact_pass,
            "post_conversion_productivity_pass": post_conversion_productivity_pass,
            "productive_contact_pass": productive_contact_pass,
            "attack_move_fraction_maximum": ATTACK_MOVE_FRACTION_MAXIMUM,
            "attack_move_reduction_pass": attack_move_reduction_pass,
            "minimum_seed_2060_gate_pass": minimum_seed_2060_gate_pass,
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
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n"


def _read_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return _obj(value, str(path))


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Fail-closed Conditional Engagement V2.2 pair comparison")
    parser.add_argument("--baseline-report", required=True)
    parser.add_argument("--candidate-report", required=True)
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        sys.stdout.write(stable_json(compare_reports(_read_json(Path(args.baseline_report)), _read_json(Path(args.candidate_report)))))
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, PairContractError) as error:
        print(f"V2.2 pair contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
