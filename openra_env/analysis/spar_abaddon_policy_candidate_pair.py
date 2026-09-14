"""Symmetric pair comparison for reviewed Abaddon policy candidates."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

PAIR_SCHEMA = "void.abaddon.policy-candidate-pair-comparison.v1"
ANALYZER_MARKER = "VOID_WAR_COLLEGE_SPAR_TRAINING_UTILITY_V1"
ABADDON_EVIDENCE_KEY = "abaddon_policy_candidate_v1"
APOLLYON_GENERATION_KEYS = (
    "conditional_engagement_v2",
    "conditional_engagement_v2_1",
    "conditional_engagement_v2_2",
)
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
    report: Mapping[str, Any],
    label: str,
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
        _int(side_report.get("final_combat_capable_units"), f"{label}.{side}.final_combat_capable_units")
        _num(side_report.get("net_kill_cost"), f"{label}.{side}.net_kill_cost")
        _arr(side_report.get("retried_rounds"), f"{label}.{side}.retried_rounds")
        _arr(side_report.get("contact_rounds"), f"{label}.{side}.contact_rounds")
    return provenance, integrity, sides


def _require_apollyon_fixed(report: Mapping[str, Any], label: str) -> None:
    for key in APOLLYON_GENERATION_KEYS:
        generation = _obj(report.get(key), f"{label}.{key}")
        _require(
            generation.get("present") is False,
            f"{label} unexpectedly contains Apollyon candidate evidence: {key}",
        )


def compare_reports(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
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

    _require_apollyon_fixed(baseline, "baseline")
    _require_apollyon_fixed(candidate, "candidate")

    baseline_evidence = _obj(
        baseline.get(ABADDON_EVIDENCE_KEY),
        f"baseline.{ABADDON_EVIDENCE_KEY}",
    )
    candidate_evidence = _obj(
        candidate.get(ABADDON_EVIDENCE_KEY),
        f"candidate.{ABADDON_EVIDENCE_KEY}",
    )
    _require(
        baseline_evidence.get("present") is False,
        "baseline unexpectedly contains Abaddon candidate evidence",
    )
    _require(
        candidate_evidence.get("present") is True,
        "candidate is missing Abaddon candidate evidence",
    )
    for key, message in (
        ("reviewed_wrapper_identity_verified", "candidate reviewed wrapper identity is not verified"),
        ("all_round_receipts_verified", "candidate Abaddon round receipts are not verified"),
        ("host_acceptance_bound", "candidate Abaddon host acceptance is not bound"),
        ("host_validation_unchanged", "candidate Abaddon host validation changed"),
    ):
        _require(candidate_evidence.get(key) is True, message)
    _require(
        candidate_evidence.get("training_use_approved") is False,
        "candidate evidence crossed training-use approval boundary",
    )
    _require(
        candidate_evidence.get("training_performed") is False,
        "candidate evidence reports training",
    )
    _require(
        candidate_evidence.get("weights_updated") is False,
        "candidate evidence reports weight mutation",
    )

    rounds = _int(ci.get("rounds_completed"), "candidate.rounds_completed", 1)
    _require(
        candidate_evidence.get("rounds_verified") == rounds,
        "candidate Abaddon verified-round count mismatch",
    )

    identity = {
        key: _sha256(candidate_evidence.get(key), f"candidate {key}")
        for key in (
            "candidate_file_sha256",
            "candidate_genome_sha256",
            "wrapper_sha256",
            "legacy_runner_sha256",
            "abaddon_controller_sha256",
            "abaddon_refiner_sha256",
        )
    }

    b_ab = _obj(bs.get("abaddon"), "baseline.abaddon")
    c_ab = _obj(cs.get("abaddon"), "candidate.abaddon")
    b_ap = _obj(bs.get("apollyon"), "baseline.apollyon")
    c_ap = _obj(cs.get("apollyon"), "candidate.apollyon")

    baseline_net = _num(b_ab.get("net_kill_cost"), "baseline.abaddon.net_kill_cost")
    candidate_net = _num(c_ab.get("net_kill_cost"), "candidate.abaddon.net_kill_cost")
    net_delta = candidate_net - baseline_net
    verdict = "BETTER" if net_delta > 0 else "WORSE" if net_delta < 0 else "TIE"

    final_combat_delta = c_ab["final_combat_capable_units"] - b_ab["final_combat_capable_units"]
    force_preservation_pass = final_combat_delta >= 0

    retry_lists = (
        _arr(b_ab.get("retried_rounds"), "baseline.abaddon.retried_rounds"),
        _arr(c_ab.get("retried_rounds"), "candidate.abaddon.retried_rounds"),
        _arr(b_ap.get("retried_rounds"), "baseline.apollyon.retried_rounds"),
        _arr(c_ap.get("retried_rounds"), "candidate.apollyon.retried_rounds"),
    )
    protocol_clean = not any(retry_lists)

    contact_rounds = list(_arr(c_ab.get("contact_rounds"), "candidate.abaddon.contact_rounds"))
    damage_inflicted = c_ab.get("first_damage_inflicted") is not None
    productive_contact_pass = bool(contact_rounds) and damage_inflicted

    host_rejections = _int(
        candidate_evidence.get("host_rejection_count"),
        "candidate Abaddon host_rejection_count",
    )
    host_acceptance_pass = host_rejections == 0
    _int(candidate_evidence.get("host_accept_count"), "candidate Abaddon host_accept_count")

    review_candidate_pass = (
        verdict == "BETTER"
        and force_preservation_pass
        and protocol_clean
        and productive_contact_pass
        and host_acceptance_pass
    )

    return {
        "schema": PAIR_SCHEMA,
        "candidate_only": True,
        "review_required": True,
        "pair_identity": {field: bp[field] for field in PAIR_FIELDS},
        "baseline": {
            "trajectory_sha256": baseline_trajectory_sha,
            "summary_sha256": baseline_summary_sha,
            "rounds_completed": bi["rounds_completed"],
            "abaddon_net_kill_cost": baseline_net,
            "abaddon_final_combat": b_ab["final_combat_capable_units"],
            "apollyon_net_kill_cost": _num(
                b_ap.get("net_kill_cost"),
                "baseline.apollyon.net_kill_cost",
            ),
        },
        "candidate": {
            "trajectory_sha256": candidate_trajectory_sha,
            "summary_sha256": candidate_summary_sha,
            "rounds_completed": rounds,
            **identity,
            "abaddon_net_kill_cost": candidate_net,
            "abaddon_final_combat": c_ab["final_combat_capable_units"],
            "apollyon_net_kill_cost": _num(
                c_ap.get("net_kill_cost"),
                "candidate.apollyon.net_kill_cost",
            ),
            "abaddon_contact_round_count": len(contact_rounds),
            "abaddon_damage_inflicted": damage_inflicted,
            "host_accept_count": candidate_evidence["host_accept_count"],
            "host_rejection_count": host_rejections,
        },
        "comparison": {
            "primary_metric": "abaddon_net_kill_cost_delta",
            "verdict": verdict,
            "net_kill_cost_delta": net_delta,
            "final_combat_delta": final_combat_delta,
            "force_preservation_pass": force_preservation_pass,
            "protocol_clean": protocol_clean,
            "productive_contact_pass": productive_contact_pass,
            "host_acceptance_pass": host_acceptance_pass,
            "review_candidate_pass": review_candidate_pass,
        },
        "authority": {
            "training_performed": False,
            "weights_updated": False,
            "automatic_corpus_admission": False,
            "automatic_weight_mutation": False,
            "automatic_promotion": False,
        },
    }
