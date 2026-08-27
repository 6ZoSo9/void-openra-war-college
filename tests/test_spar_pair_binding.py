from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis import spar_pair_binding as binding
from openra_env.analysis import spar_pair_comparison as pair
from openra_env.analysis._spar_conditional_v2_reviewed_identity import (
    REVIEWED_V2_CANDIDATE_SHA256,
    REVIEWED_V2_POLICY_SHA256,
    REVIEWED_V2_SESSION_SHA256,
    REVIEWED_V2_SOURCE_COMMIT,
    REVIEWED_V2_WRAPPER_SHA256,
)


def warm_start(path: Path, *, run_id: str, final_combat: int = 4) -> str:
    rows = [
        {
            "event": "warm_start_header",
            "run_id": run_id,
            "curriculum_id": "symmetric-contact-warm-start-v1",
            "generation_id": "ad1926569b12466c",
            "runner_sha256": "1" * 64,
            "base_runner_sha256": "2" * 64,
            "joint_training_attestation_sha256": "3" * 64,
            "seed": 2060,
            "controller_authored": False,
            "training_candidate": False,
        },
        {
            "event": "warm_start_step",
            "curriculum_id": "symmetric-contact-warm-start-v1",
            "label": "stage_advance",
            "start_tick": 2626,
            "end_tick": 2651,
            "commands": {"Multi0": [], "Multi1": []},
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


def report(*, warm_sha: str, v2: bool, net: int = 0, final_combat: int = 0) -> dict:
    provenance = {
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "generation_id": "ad1926569b12466c",
        "runtime_image_id": "sha256:" + "4" * 64,
        "engine_commit": "5" * 40,
        "war_college_commit": "6" * 40,
        "joint_training_attestation_sha256": "3" * 64,
        "warm_start_sha256": warm_sha,
        "warm_start_handoff": {"tick": 2651, "contact_achieved": False},
        "warm_start_handoff_tick": 2651,
        "apollyon_model": "apollyon",
        "abaddon_controller_sha256": "7" * 64,
        "abaddon_doctrine": "RUSHER",
        "seed": 2060,
        "round_limit": 72,
        "ticks_per_round": 25,
        "trajectory_sha256": hashlib.sha256(("candidate" if v2 else "baseline").encode()).hexdigest(),
        "summary_sha256": hashlib.sha256(("candidate-summary" if v2 else "baseline-summary").encode()).hexdigest(),
    }
    conditional = {"present": False, "rounds_verified": 0, "mode_counts": {}}
    if v2:
        conditional = {
            "present": True,
            "rounds_verified": 72,
            "mode_counts": {"REBUILD_FORCE": 10, "BALANCED_SEARCH": 62},
            "source_commit": REVIEWED_V2_SOURCE_COMMIT,
            "candidate_sha256": REVIEWED_V2_CANDIDATE_SHA256,
            "policy_sha256": REVIEWED_V2_POLICY_SHA256,
            "session_sha256": REVIEWED_V2_SESSION_SHA256,
            "wrapper_sha256": REVIEWED_V2_WRAPPER_SHA256,
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
                "retried_rounds": [],
            },
            "abaddon": {
                "final_combat_capable_units": 5,
                "net_kill_cost": -net,
                "tools": {"attack_move": 30},
                "retried_rounds": [],
            },
        },
        "authority": {
            "candidate_only": True,
            "review_required": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
        "conditional_engagement_v2": conditional,
    }


def test_run_id_only_changes_raw_hash_but_not_normalized_identity(tmp_path):
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"
    warm_start(first, run_id="run-20260827T185345Z")
    warm_start(second, run_id="run-20260827T201320Z")
    a = binding.warm_start_identity(first)
    b = binding.warm_start_identity(second)
    assert a["raw_sha256"] != b["raw_sha256"]
    assert a["normalized_sha256"] == b["normalized_sha256"]


def test_semantic_warm_start_change_still_fails_pair_binding(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="baseline", final_combat=4)
    candidate_sha = warm_start(candidate_warm, run_id="candidate", final_combat=3)
    with pytest.raises(pair.PairContractError, match="normalized warm-start mismatch"):
        binding.compare_reports_with_warm_starts(
            report(warm_sha=baseline_sha, v2=False),
            report(warm_sha=candidate_sha, v2=True),
            baseline_warm_start_path=baseline_warm,
            candidate_warm_start_path=candidate_warm,
        )


def test_report_must_bind_exact_supplied_raw_warm_start(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    warm_start(baseline_warm, run_id="baseline")
    candidate_sha = warm_start(candidate_warm, run_id="candidate")
    with pytest.raises(pair.PairContractError, match="baseline report is not bound"):
        binding.compare_reports_with_warm_starts(
            report(warm_sha="f" * 64, v2=False),
            report(warm_sha=candidate_sha, v2=True),
            baseline_warm_start_path=baseline_warm,
            candidate_warm_start_path=candidate_warm,
        )


def test_normalized_binding_admits_timestamp_only_rerun_and_preserves_primary_verdict(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="baseline-older")
    candidate_sha = warm_start(candidate_warm, run_id="candidate-newer")
    out = binding.compare_reports_with_warm_starts(
        report(warm_sha=baseline_sha, v2=False, net=0, final_combat=0),
        report(warm_sha=candidate_sha, v2=True, net=-200, final_combat=12),
        baseline_warm_start_path=baseline_warm,
        candidate_warm_start_path=candidate_warm,
        expected_v2_candidate_sha256=REVIEWED_V2_CANDIDATE_SHA256,
        expected_v2_source_commit=REVIEWED_V2_SOURCE_COMMIT,
    )
    assert out["comparison"]["verdict"] == "WORSE"
    assert out["comparison"]["net_kill_cost_delta"] == -200
    assert out["comparison"]["final_combat_delta"] == 12
    assert out["warm_start_binding"]["semantic_match"] is True
    assert "warm_start_sha256" not in out["pair_identity"]
    assert len(out["pair_identity"]["warm_start_normalized_sha256"]) == 64


def test_normalized_pair_remains_accepted_by_matrix_without_claiming_completion(tmp_path):
    baseline_warm = tmp_path / "baseline.jsonl"
    candidate_warm = tmp_path / "candidate.jsonl"
    baseline_sha = warm_start(baseline_warm, run_id="baseline")
    candidate_sha = warm_start(candidate_warm, run_id="candidate")
    paired = binding.compare_reports_with_warm_starts(
        report(warm_sha=baseline_sha, v2=False),
        report(warm_sha=candidate_sha, v2=True, net=-200, final_combat=12),
        baseline_warm_start_path=baseline_warm,
        candidate_warm_start_path=candidate_warm,
    )
    matrix = pair.evaluate_matrix([paired])
    assert matrix["status"] == "PENDING"
    assert matrix["by_seed"]["2060"]["pair_count"] == 1
    assert matrix["by_seed"]["2060"]["worse"] == 1
