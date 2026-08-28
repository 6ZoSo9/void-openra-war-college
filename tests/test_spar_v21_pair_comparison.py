from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis import spar_v21_pair_binding as binding
from openra_env.analysis import spar_v21_pair_comparison as pair
from openra_env.analysis._spar_conditional_v2_1_reviewed_identity import REVIEWED_V21_IDENTITY


def absent() -> dict:
    return {"present": False, "rounds_verified": 0, "mode_counts": {}}


def report(
    *,
    v21: bool,
    net: int = 0,
    final_combat: int = 0,
    warm_sha: str = "8" * 64,
    seed: int = 2060,
    ap_retries=None,
    ab_retries=None,
    run: int = 0,
) -> dict:
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
        "trajectory_sha256": hashlib.sha256(
            f"trajectory:{v21}:{seed}:{run}".encode()
        ).hexdigest(),
        "summary_sha256": hashlib.sha256(
            f"summary:{v21}:{seed}:{run}".encode()
        ).hexdigest(),
    }
    v21_evidence = absent()
    if v21:
        v21_evidence = {
            "present": True,
            "rounds_verified": 72,
            "mode_counts": {"FORCE_CONVERSION": 8, "BALANCED_SEARCH": 64},
            **REVIEWED_V21_IDENTITY,
            "reviewed_identity_verified": True,
            "all_round_receipts_verified": True,
            "tool_surface_bound": True,
            "accepted_tool_bound": True,
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
        "sides": {
            "apollyon": {
                "final_combat_capable_units": final_combat,
                "net_kill_cost": net,
                "tools": {"attack_move": 20, "attack_target": 4},
                "retried_rounds": ap_retries,
            },
            "abaddon": {
                "final_combat_capable_units": 5,
                "net_kill_cost": -net,
                "tools": {"attack_move": 30},
                "retried_rounds": ab_retries,
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
        "conditional_engagement_v2_1": v21_evidence,
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
    raw = "".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    )
    path.write_text(raw, encoding="utf-8")
    return hashlib.sha256(raw.encode()).hexdigest()


def test_better_pair_with_force_preservation_passes_minimum_seed_2060_gate():
    out = pair.compare_reports(
        report(v21=False, net=0, final_combat=0),
        report(v21=True, net=100, final_combat=8),
    )
    assert out["comparison"]["verdict"] == "BETTER"
    assert out["comparison"]["net_kill_cost_delta"] == 100
    assert out["comparison"]["final_combat_delta"] == 8
    assert out["comparison"]["force_preservation_pass"] is True
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is True
    assert out["candidate"]["v2_1_wrapper_sha256"] == REVIEWED_V21_IDENTITY["wrapper_sha256"]


def test_worse_pair_cannot_be_rescued_by_large_surviving_force():
    out = pair.compare_reports(
        report(v21=False, net=0, final_combat=0),
        report(v21=True, net=-200, final_combat=12),
    )
    assert out["comparison"]["verdict"] == "WORSE"
    assert out["comparison"]["force_preservation_pass"] is True
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False


def test_tie_with_nonnegative_force_and_clean_protocol_meets_minimum_gate():
    out = pair.compare_reports(
        report(v21=False, net=0, final_combat=4),
        report(v21=True, net=0, final_combat=4),
    )
    assert out["comparison"]["verdict"] == "TIE"
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is True


def test_force_regression_fails_preservation_even_with_better_net_delta():
    out = pair.compare_reports(
        report(v21=False, net=0, final_combat=4),
        report(v21=True, net=300, final_combat=3),
    )
    assert out["comparison"]["verdict"] == "BETTER"
    assert out["comparison"]["force_preservation_pass"] is False
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False


def test_abaddon_retry_makes_pair_protocol_unclean():
    out = pair.compare_reports(
        report(v21=False),
        report(v21=True, net=100, final_combat=6, ab_retries=[9]),
    )
    assert out["comparison"]["protocol_clean"] is False
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is False


def test_apollyon_retry_makes_pair_protocol_unclean():
    out = pair.compare_reports(
        report(v21=False),
        report(v21=True, net=100, final_combat=6, ap_retries=[3]),
    )
    assert out["comparison"]["protocol_clean"] is False


def test_candidate_cannot_claim_v2_and_v21_generations_together():
    candidate = report(v21=True)
    candidate["conditional_engagement_v2"] = {"present": True}
    with pytest.raises(pair.PairContractError, match="unexpectedly contains conditional_engagement_v2"):
        pair.compare_reports(report(v21=False), candidate)


def test_baseline_must_be_generation_free():
    baseline = report(v21=False)
    baseline["conditional_engagement_v2_1"] = copy.deepcopy(
        report(v21=True)["conditional_engagement_v2_1"]
    )
    with pytest.raises(pair.PairContractError, match="baseline unexpectedly"):
        pair.compare_reports(baseline, report(v21=True))


def test_reviewed_v21_identity_drift_fails_closed():
    candidate = report(v21=True)
    candidate["conditional_engagement_v2_1"]["wrapper_sha256"] = "f" * 64
    with pytest.raises(pair.PairContractError, match="reviewed V2.1 identity mismatch"):
        pair.compare_reports(report(v21=False), candidate)


def test_pair_identity_drift_fails_closed():
    candidate = report(v21=True)
    candidate["provenance"]["seed"] = 9999
    with pytest.raises(pair.PairContractError, match="pair identity mismatch: seed"):
        pair.compare_reports(report(v21=False), candidate)


def test_timestamp_only_warm_start_difference_is_admitted(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="run-old")
    candidate_sha = warm_start(candidate_warm, run_id="run-new")
    out = binding.compare_reports_with_warm_starts(
        report(v21=False, warm_sha=baseline_sha),
        report(v21=True, warm_sha=candidate_sha, net=100, final_combat=8),
        baseline_warm_start_path=baseline_warm,
        candidate_warm_start_path=candidate_warm,
    )
    assert out["warm_start_binding"]["semantic_match"] is True
    assert out["comparison"]["minimum_seed_2060_gate_pass"] is True
    assert "warm_start_sha256" not in out["pair_identity"]
    assert len(out["pair_identity"]["warm_start_normalized_sha256"]) == 64


def test_substantive_warm_start_change_still_holds(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="old", final_combat=4)
    candidate_sha = warm_start(candidate_warm, run_id="new", final_combat=3)
    with pytest.raises(pair.PairContractError, match="normalized warm-start mismatch"):
        binding.compare_reports_with_warm_starts(
            report(v21=False, warm_sha=baseline_sha),
            report(v21=True, warm_sha=candidate_sha),
            baseline_warm_start_path=baseline_warm,
            candidate_warm_start_path=candidate_warm,
        )


def test_report_must_bind_exact_supplied_raw_warm_start(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    warm_start(baseline_warm, run_id="old")
    candidate_sha = warm_start(candidate_warm, run_id="new")
    with pytest.raises(pair.PairContractError, match="baseline report is not bound"):
        binding.compare_reports_with_warm_starts(
            report(v21=False, warm_sha="f" * 64),
            report(v21=True, warm_sha=candidate_sha),
            baseline_warm_start_path=baseline_warm,
            candidate_warm_start_path=candidate_warm,
        )
