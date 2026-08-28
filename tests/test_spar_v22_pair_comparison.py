from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis import spar_v22_pair_binding as binding
from openra_env.analysis import spar_v22_pair_comparison as pair
from openra_env.analysis._spar_conditional_v2_2_reviewed_identity import REVIEWED_V22_IDENTITY


def absent() -> dict:
    return {"present": False, "rounds_verified": 0, "mode_counts": {}}


def report(
    *,
    v22: bool,
    net: int = 0,
    final_combat: int = 0,
    attack_move: int = 20,
    contact_rounds=None,
    damage: bool = False,
    warm_sha: str = "8" * 64,
    seed: int = 2060,
    ap_retries=None,
    ab_retries=None,
    run: int = 0,
) -> dict:
    contact_rounds = [] if contact_rounds is None else contact_rounds
    ap_retries = [] if ap_retries is None else ap_retries
    ab_retries = [] if ab_retries is None else ab_retries
    provenance = {
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "generation_id": "ad1926569b12466c",
        "runtime_image_id": "sha256:" + "1" * 64,
        "engine_commit": "2" * 40,
        "war_college_commit": "3" * 40,
        "joint_training_attestation_sha256": "4" * 64,
        "warm_start_sha256": warm_sha,
        "warm_start_handoff": {"tick": 2651, "contact_achieved": False},
        "warm_start_handoff_tick": 2651,
        "apollyon_model": "apollyon",
        "abaddon_controller_sha256": "5" * 64,
        "abaddon_doctrine": "RUSHER",
        "seed": seed,
        "round_limit": 72,
        "ticks_per_round": 25,
        "trajectory_sha256": hashlib.sha256(f"trajectory:{v22}:{seed}:{run}".encode()).hexdigest(),
        "summary_sha256": hashlib.sha256(f"summary:{v22}:{seed}:{run}".encode()).hexdigest(),
    }
    v22_evidence = absent()
    if v22:
        v22_evidence = {
            "present": True,
            "rounds_verified": 72,
            "mode_counts": {"FORCE_CONVERSION": 30, "BALANCED_SEARCH": 42},
            **REVIEWED_V22_IDENTITY,
            "reviewed_identity_verified": True,
            "all_round_receipts_verified": True,
            "tool_surface_bound": True,
            "accepted_tool_bound": True,
            "action_compliance_bound": True,
            "attack_move_discouraged_rounds": 30,
            "followed_non_attack_move_rounds": 24,
            "ignored_attack_move_discouragement_rounds": 6,
            "preferred_move_units_offered_rounds": 30,
            "preferred_move_units_selected_rounds": 20,
            "runtime_seed_branching": False,
        }
    return {
        "marker": "VOID_WAR_COLLEGE_SPAR_TRAINING_UTILITY_V1",
        "version": 1,
        "provenance": provenance,
        "integrity": {
            "trajectory_verified": True,
            "summary_verified": True,
            "rounds_completed": 72,
            "final_tick": 4451,
            "terminal_phase": "playing",
            "winner": "",
            "world_clock_contiguous": True,
            "perspective_accounting_consistent": True,
        },
        "training_utility": {"classification": "TACTICAL_DAMAGE_PRESENT" if damage else "NO_CONTACT"},
        "sides": {
            "apollyon": {
                "final_combat_capable_units": final_combat,
                "net_kill_cost": net,
                "tools": {"attack_move": attack_move, "attack_target": 4, "move_units": 72 - attack_move - 4},
                "retried_rounds": ap_retries,
                "contact_rounds": contact_rounds,
                "first_damage_inflicted": {"round": contact_rounds[0]} if damage and contact_rounds else None,
            },
            "abaddon": {
                "final_combat_capable_units": 5,
                "net_kill_cost": -net,
                "tools": {"attack_move": 30},
                "retried_rounds": ab_retries,
                "contact_rounds": contact_rounds,
                "first_damage_inflicted": None,
            },
        },
        "authority": {
            "candidate_only": True,
            "review_required": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
        "conditional_engagement_v2": absent(),
        "conditional_engagement_v2_1": absent(),
        "conditional_engagement_v2_2": v22_evidence,
    }


def warm_start(path: Path, *, run_id: str, final_combat: int = 4) -> str:
    rows = [
        {
            "event": "warm_start_header",
            "run_id": run_id,
            "curriculum_id": "symmetric-contact-warm-start-v1",
            "generation_id": "ad1926569b12466c",
            "runner_sha256": "1" * 64,
            "base_runner_sha256": "2" * 64,
            "joint_training_attestation_sha256": "4" * 64,
            "seed": 2060,
            "controller_authored": False,
            "training_candidate": False,
        },
        {
            "event": "warm_start_step",
            "label": "stage_advance",
            "start_tick": 2626,
            "end_tick": 2651,
            "state": {
                "Multi0": {"tick": 2651, "combat": final_combat},
                "Multi1": {"tick": 2651, "combat": 4},
            },
            "controller_authored": False,
            "training_candidate": False,
        },
    ]
    raw = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    path.write_text(raw, encoding="utf-8")
    return hashlib.sha256(raw.encode()).hexdigest()


def passing_candidate(**overrides):
    values = dict(v22=True, net=0, final_combat=4, attack_move=54, contact_rounds=[20], damage=True, run=1)
    values.update(overrides)
    return report(**values)


def test_tie_passes_only_with_force_contact_damage_attack_move_reduction_and_clean_protocol():
    out = pair.compare_reports(report(v22=False, net=0, final_combat=0), passing_candidate())
    assert out["comparison"]["verdict"] == "TIE"
    assert out["comparison"]["net_kill_cost_delta"] == 0
    assert out["comparison"]["final_combat_delta"] == 4
    assert out["comparison"]["force_preservation_pass"] is True
    assert out["comparison"]["productive_contact_pass"] is True
    assert out["comparison"]["attack_move_reduction_pass"] is True
    assert out["comparison"]["protocol_clean"] is True
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is True
    assert out["candidate"]["v2_2_wrapper_sha256"] == REVIEWED_V22_IDENTITY["wrapper_sha256"]


def test_contact_without_damage_is_not_productive():
    out = pair.compare_reports(report(v22=False), passing_candidate(damage=False))
    assert out["comparison"]["productive_contact_pass"] is False
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False


def test_damage_without_observed_contact_is_not_productive():
    out = pair.compare_reports(report(v22=False), passing_candidate(contact_rounds=[], damage=True))
    assert out["comparison"]["productive_contact_pass"] is False


def test_attack_move_fraction_above_frozen_ceiling_fails_gate():
    out = pair.compare_reports(report(v22=False), passing_candidate(attack_move=55))
    assert out["candidate"]["apollyon_attack_move_fraction"] > 0.75
    assert out["comparison"]["attack_move_reduction_pass"] is False
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False


def test_negative_net_or_force_regression_cannot_be_rescued():
    out = pair.compare_reports(report(v22=False), passing_candidate(net=-100))
    assert out["comparison"]["verdict"] == "WORSE"
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False

    out = pair.compare_reports(report(v22=False, final_combat=4), passing_candidate(net=100, final_combat=3))
    assert out["comparison"]["verdict"] == "BETTER"
    assert out["comparison"]["force_preservation_pass"] is False
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False


def test_either_side_retry_makes_pair_protocol_unclean():
    out = pair.compare_reports(report(v22=False), passing_candidate(ap_retries=[3]))
    assert out["comparison"]["protocol_clean"] is False
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False

    out = pair.compare_reports(report(v22=False), passing_candidate(ab_retries=[9]))
    assert out["comparison"]["protocol_clean"] is False


def test_generation_mixing_and_reviewed_identity_drift_fail_closed():
    candidate = passing_candidate()
    candidate["conditional_engagement_v2_1"] = {"present": True}
    with pytest.raises(pair.PairContractError, match="unexpectedly contains conditional_engagement_v2_1"):
        pair.compare_reports(report(v22=False), candidate)

    candidate = passing_candidate()
    candidate["conditional_engagement_v2_2"]["wrapper_sha256"] = "f" * 64
    with pytest.raises(pair.PairContractError, match="reviewed V2.2 identity mismatch"):
        pair.compare_reports(report(v22=False), candidate)


def test_baseline_must_be_generation_free_and_pair_identity_exact():
    baseline = report(v22=False)
    baseline["conditional_engagement_v2_2"] = copy.deepcopy(passing_candidate()["conditional_engagement_v2_2"])
    with pytest.raises(pair.PairContractError, match="baseline unexpectedly"):
        pair.compare_reports(baseline, passing_candidate())

    candidate = passing_candidate()
    candidate["provenance"]["seed"] = 9999
    with pytest.raises(pair.PairContractError, match="pair identity mismatch: seed"):
        pair.compare_reports(report(v22=False), candidate)


def test_timestamp_only_warm_start_difference_is_admitted(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="run-old")
    candidate_sha = warm_start(candidate_warm, run_id="run-new")
    out = binding.compare_reports_with_warm_starts(
        report(v22=False, warm_sha=baseline_sha),
        passing_candidate(warm_sha=candidate_sha),
        baseline_warm_start_path=baseline_warm,
        candidate_warm_start_path=candidate_warm,
    )
    assert out["warm_start_binding"]["semantic_match"] is True
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is True
    assert "warm_start_sha256" not in out["pair_identity"]
    assert len(out["pair_identity"]["warm_start_normalized_sha256"]) == 64


def test_substantive_or_unbound_warm_start_holds(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="old", final_combat=4)
    candidate_sha = warm_start(candidate_warm, run_id="new", final_combat=3)
    with pytest.raises(pair.PairContractError, match="normalized warm-start mismatch"):
        binding.compare_reports_with_warm_starts(
            report(v22=False, warm_sha=baseline_sha),
            passing_candidate(warm_sha=candidate_sha),
            baseline_warm_start_path=baseline_warm,
            candidate_warm_start_path=candidate_warm,
        )

    candidate_sha = warm_start(candidate_warm, run_id="new2", final_combat=4)
    with pytest.raises(pair.PairContractError, match="baseline report is not bound"):
        binding.compare_reports_with_warm_starts(
            report(v22=False, warm_sha="f" * 64),
            passing_candidate(warm_sha=candidate_sha),
            baseline_warm_start_path=baseline_warm,
            candidate_warm_start_path=candidate_warm,
        )
