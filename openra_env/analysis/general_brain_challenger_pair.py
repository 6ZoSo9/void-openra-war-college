from __future__ import annotations

import copy
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from openra_env.learning.general_brain_generation import manifest_sha256

from ._spar_contract import ContractError
from .general_brain_g1_runtime_evidence import validate_general_brain_g1_evidence
from .spar_pair_binding import warm_start_identity

PAIR_SCHEMA = "void.general-brain-incumbent-challenger-pair.v1"
ATTACK_MOVE_FRACTION_MAXIMUM = 0.75
PREFERENCE_FOLLOW_FRACTION_MINIMUM = 0.80
PAIR_FIELDS = (
    "curriculum_id",
    "generation_id",
    "runtime_image_id",
    "engine_commit",
    "war_college_commit",
    "joint_training_attestation_sha256",
    "apollyon_model",
    "abaddon_controller_sha256",
    "abaddon_doctrine",
    "seed",
    "round_limit",
    "ticks_per_round",
)


class ChallengerPairError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ChallengerPairError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _clean_report(report: Mapping[str, Any], label: str) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    report = _obj(report, label)
    provenance = _obj(report.get("provenance"), f"{label}.provenance")
    integrity = _obj(report.get("integrity"), f"{label}.integrity")
    authority = _obj(report.get("authority"), f"{label}.authority")
    _require(authority.get("candidate_only") is True, f"{label} must remain candidate-only")
    _require(authority.get("review_required") is True, f"{label} review boundary drift")
    for key in (
        "automatic_corpus_admission",
        "automatic_apollyon_weight_mutation",
        "automatic_abaddon_policy_promotion",
    ):
        _require(authority.get(key) is False, f"{label} authority drift: {key}")
    for key in (
        "trajectory_verified",
        "summary_verified",
        "world_clock_contiguous",
        "perspective_accounting_consistent",
    ):
        _require(integrity.get(key) is True, f"{label} integrity missing: {key}")
    sides = _obj(report.get("sides"), f"{label}.sides")
    return provenance, integrity, sides


def _reviewed_v22(report: Mapping[str, Any], label: str) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    v22 = _obj(report.get("conditional_engagement_v2_2"), f"{label}.V2.2")
    conversion = _obj(
        report.get("conditional_engagement_v2_2_conversion_utility"),
        f"{label}.conversion",
    )
    _require(v22.get("present") is True, f"{label} is not V2.2")
    _require(v22.get("reviewed_identity_verified") is True, f"{label} V2.2 identity unreviewed")
    _require(v22.get("all_round_receipts_verified") is True, f"{label} V2.2 receipts incomplete")
    _require(v22.get("tool_surface_bound") is True, f"{label} V2.2 tool surface unbound")
    _require(v22.get("accepted_tool_bound") is True, f"{label} V2.2 accepted tool unbound")
    _require(v22.get("runtime_seed_branching") is False, f"{label} seed branching detected")
    _require(conversion.get("present") is True, f"{label} conversion utility missing")
    return v22, conversion


def _tool_fraction(side: Mapping[str, Any], tool: str, rounds: int) -> float:
    tools = _obj(side.get("tools"), "side.tools")
    count = tools.get(tool, 0)
    _require(type(count) is int and 0 <= count <= rounds, f"tool count malformed: {tool}")
    return count / rounds


def compare_incumbent_challenger(
    incumbent_report: Mapping[str, Any],
    challenger_report: Mapping[str, Any],
    *,
    incumbent_trajectory_path: Path,
    challenger_trajectory_path: Path,
    incumbent_warm_start_path: Path,
    challenger_warm_start_path: Path,
    incumbent_manifest: Mapping[str, Any],
    challenger_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    ip, ii, isides = _clean_report(incumbent_report, "incumbent")
    cp, ci, csides = _clean_report(challenger_report, "challenger")
    _reviewed_v22(incumbent_report, "incumbent")
    _, challenger_conversion = _reviewed_v22(challenger_report, "challenger")

    for field in PAIR_FIELDS:
        _require(ip.get(field) == cp.get(field), f"incumbent/challenger identity mismatch: {field}")

    incumbent_binding = warm_start_identity(incumbent_warm_start_path)
    challenger_binding = warm_start_identity(challenger_warm_start_path)
    _require(
        ip.get("warm_start_sha256") == incumbent_binding["raw_sha256"],
        "incumbent report is not bound to supplied warm start",
    )
    _require(
        cp.get("warm_start_sha256") == challenger_binding["raw_sha256"],
        "challenger report is not bound to supplied warm start",
    )
    _require(
        incumbent_binding["normalized_sha256"] == challenger_binding["normalized_sha256"],
        "incumbent/challenger warm starts are not semantically identical",
    )

    incumbent_brain = validate_general_brain_g1_evidence(
        incumbent_trajectory_path,
        expected_trajectory_sha256=str(ip["trajectory_sha256"]),
    )
    challenger_brain = validate_general_brain_g1_evidence(
        challenger_trajectory_path,
        expected_trajectory_sha256=str(cp["trajectory_sha256"]),
    )
    _require(incumbent_brain.get("present") is False, "incumbent unexpectedly contains Generation 1 adapter evidence")
    _require(challenger_brain.get("present") is True, "challenger is missing Generation 1 adapter evidence")
    _require(challenger_brain.get("all_round_receipts_verified") is True, "challenger General Brain receipts incomplete")
    _require(challenger_brain.get("reviewed_v2_2_identity_verified") is True, "challenger not layered over reviewed V2.2")

    from openra_env.learning.general_brain_generation import validate_brain_manifest
    validate_brain_manifest(incumbent_manifest)
    validate_brain_manifest(challenger_manifest)
    _require(incumbent_manifest.get("general_id") == "apollyon", "incumbent manifest must be Apollyon")
    _require(challenger_manifest.get("general_id") == "apollyon", "challenger manifest must be Apollyon")
    _require(incumbent_manifest.get("generation") == 0, "incumbent must be Generation 0")
    _require(challenger_manifest.get("generation") == 1, "challenger must be Generation 1")
    _require(challenger_manifest.get("competence_adapter", {}).get("state") == "challenger", "Generation 1 must remain challenger")
    _require(
        challenger_brain.get("challenger_manifest_sha256") == manifest_sha256(challenger_manifest),
        "runtime challenger manifest binding mismatch",
    )
    _require(
        incumbent_manifest.get("authority_envelope") == challenger_manifest.get("authority_envelope"),
        "authority envelope changed between incumbent and challenger",
    )

    incumbent_ap = _obj(isides.get("apollyon"), "incumbent.apollyon")
    challenger_ap = _obj(csides.get("apollyon"), "challenger.apollyon")
    incumbent_ab = _obj(isides.get("abaddon"), "incumbent.abaddon")
    challenger_ab = _obj(csides.get("abaddon"), "challenger.abaddon")
    incumbent_rounds = ii.get("rounds_completed")
    challenger_rounds = ci.get("rounds_completed")
    _require(type(incumbent_rounds) is int and incumbent_rounds >= 1, "incumbent rounds invalid")
    _require(type(challenger_rounds) is int and challenger_rounds >= 1, "challenger rounds invalid")

    incumbent_net = float(incumbent_ap["net_kill_cost"])
    challenger_net = float(challenger_ap["net_kill_cost"])
    net_delta = challenger_net - incumbent_net
    final_combat_delta = int(challenger_ap["final_combat_capable_units"]) - int(incumbent_ap["final_combat_capable_units"])
    verdict = "BETTER" if net_delta > 0 else "WORSE" if net_delta < 0 else "TIE"

    retry_lists = (
        incumbent_ap.get("retried_rounds"),
        incumbent_ab.get("retried_rounds"),
        challenger_ap.get("retried_rounds"),
        challenger_ab.get("retried_rounds"),
    )
    _require(all(isinstance(value, list) for value in retry_lists), "retry evidence malformed")
    protocol_clean = not any(retry_lists)

    challenger_contacts = challenger_ap.get("contact_rounds")
    _require(isinstance(challenger_contacts, list), "challenger contact rounds malformed")
    overall_contact = bool(challenger_contacts) and challenger_ap.get("first_damage_inflicted") is not None
    post_conversion = challenger_conversion.get("post_conversion_productivity_pass") is True
    productive_contact_pass = overall_contact and post_conversion
    attack_move_fraction = _tool_fraction(challenger_ap, "attack_move", challenger_rounds)
    attack_move_gate = attack_move_fraction <= ATTACK_MOVE_FRACTION_MAXIMUM
    force_gate = final_combat_delta >= 0
    preference_follow = float(challenger_brain["preference_follow_fraction"])
    preference_gate = preference_follow >= PREFERENCE_FOLLOW_FRACTION_MINIMUM
    behavioral_gates_pass = (
        force_gate
        and productive_contact_pass
        and attack_move_gate
        and preference_gate
    )

    return {
        "schema": PAIR_SCHEMA,
        "general_id": "apollyon",
        "incumbent_generation": 0,
        "challenger_generation": 1,
        "incumbent_manifest_sha256": manifest_sha256(incumbent_manifest),
        "challenger_manifest_sha256": manifest_sha256(challenger_manifest),
        "adapter_sha256": challenger_brain["adapter_sha256"],
        "pair_identity": {
            **{field: ip[field] for field in PAIR_FIELDS},
            "warm_start_normalized_sha256": incumbent_binding["normalized_sha256"],
        },
        "incumbent": {
            "trajectory_sha256": ip["trajectory_sha256"],
            "summary_sha256": ip["summary_sha256"],
            "apollyon_net_kill_cost": incumbent_net,
            "apollyon_final_combat": incumbent_ap["final_combat_capable_units"],
        },
        "challenger": {
            "trajectory_sha256": cp["trajectory_sha256"],
            "summary_sha256": cp["summary_sha256"],
            "apollyon_net_kill_cost": challenger_net,
            "apollyon_final_combat": challenger_ap["final_combat_capable_units"],
            "attack_move_fraction": attack_move_fraction,
            "general_brain": copy.deepcopy(challenger_brain),
        },
        "comparison": {
            "primary_metric": "challenger_minus_incumbent_apollyon_net_kill_cost",
            "verdict": verdict,
            "net_kill_cost_delta": net_delta,
            "final_combat_delta": final_combat_delta,
            "force_preservation_pass": force_gate,
            "productive_contact_pass": productive_contact_pass,
            "attack_move_fraction_maximum": ATTACK_MOVE_FRACTION_MAXIMUM,
            "attack_move_reduction_pass": attack_move_gate,
            "preference_follow_fraction": preference_follow,
            "preference_follow_fraction_minimum": PREFERENCE_FOLLOW_FRACTION_MINIMUM,
            "preference_follow_pass": preference_gate,
            "protocol_clean": protocol_clean,
            "behavioral_gates_pass": behavioral_gates_pass,
        },
        "warm_start_binding": {
            "semantic_match": True,
            "normalized_sha256": incumbent_binding["normalized_sha256"],
            "incumbent_raw_sha256": incumbent_binding["raw_sha256"],
            "challenger_raw_sha256": challenger_binding["raw_sha256"],
        },
        "authority_envelope_match": True,
        "automatic_weight_install": False,
        "automatic_promotion": False,
        "review_required": True,
    }


__all__ = ["PAIR_SCHEMA", "ChallengerPairError", "compare_incumbent_challenger"]
