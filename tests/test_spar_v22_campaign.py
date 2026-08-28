from __future__ import annotations

import hashlib
import json

import pytest

from openra_env.analysis._spar_conditional_v2_2_reviewed_identity import REVIEWED_V22_IDENTITY
from openra_env.analysis.spar_v22_campaign import (
    REVIEWED_CAMPAIGN_SEEDS,
    REVIEWED_PAIR_COUNT,
    evaluate_campaign,
    reviewed_plan,
)
from openra_env.analysis.spar_v22_pair_comparison import PAIR_SCHEMA, PairContractError


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def pair(seed: int, trial: int, delta: float, *, behavior: bool = True, protocol: bool = True) -> dict:
    verdict = "BETTER" if delta > 0 else "WORSE" if delta < 0 else "TIE"
    return {
        "schema": PAIR_SCHEMA,
        "candidate_only": True,
        "pair_identity": {"seed": seed},
        "baseline": {"trajectory_sha256": digest(f"baseline:{seed}:{trial}")},
        "candidate": {
            "trajectory_sha256": digest(f"candidate:{seed}:{trial}"),
            "reviewed_identity_verified": True,
            **{f"v2_2_{key}": value for key, value in REVIEWED_V22_IDENTITY.items()},
        },
        "comparison": {
            "verdict": verdict,
            "net_kill_cost_delta": delta,
            "protocol_clean": protocol,
            "force_preservation_pass": behavior,
            "productive_contact_pass": behavior,
            "attack_move_reduction_pass": behavior,
        },
    }


def full_pass_pairs() -> list[dict]:
    rows: list[dict] = []
    for seed in REVIEWED_CAMPAIGN_SEEDS:
        if seed == 2051:
            deltas = (0, 100, -100)
        elif seed == 2055:
            deltas = (100, 100, 0)
        else:
            deltas = (0, 0, -100)
        rows.extend(pair(seed, trial, delta) for trial, delta in enumerate(deltas, 1))
    return rows


def test_reviewed_plan_is_exact_five_seed_fifteen_pair_campaign():
    plan = reviewed_plan()
    assert plan["required_pair_count"] == 15 == REVIEWED_PAIR_COUNT
    assert [row["seed"] for row in plan["seeds"]] == [2051, 2055, 2052, 2053, 2054]
    assert [row["role"] for row in plan["seeds"]] == [
        "regression", "gain", "held_out", "held_out", "held_out"
    ]
    assert all(row["required_pairs"] == 3 for row in plan["seeds"])


def test_empty_campaign_is_pending_with_all_pairs_remaining():
    out = evaluate_campaign([])
    assert out["status"] == "PENDING"
    assert out["observed_pair_count"] == 0
    assert out["remaining_pair_count"] == 15
    assert out["campaign_complete"] is False
    assert all(value == 3 for value in out["remaining_by_seed"].values())


def test_first_tranche_2051_2055_resumes_with_thirteen_pairs_remaining():
    out = evaluate_campaign([pair(2051, 1, 0), pair(2055, 1, 100)])
    assert out["status"] == "PENDING"
    assert out["observed_pair_count"] == 2
    assert out["remaining_pair_count"] == 13
    assert out["completed_by_seed"]["2051"] == 1
    assert out["completed_by_seed"]["2055"] == 1
    assert out["remaining_by_seed"]["2051"] == 2
    assert out["remaining_by_seed"]["2055"] == 2


def test_seed_2060_sanity_evidence_cannot_enter_acceptance_campaign():
    with pytest.raises(PairContractError, match="seed 2060 is not in reviewed V2.2 campaign"):
        evaluate_campaign([pair(2060, 1, 0)])


def test_fourth_repeat_fails_before_matrix_evaluation():
    rows = [pair(2051, trial, 0) for trial in range(1, 5)]
    with pytest.raises(PairContractError, match="seed 2051 exceeds reviewed repeat ceiling"):
        evaluate_campaign(rows)


def test_duplicate_trajectory_evidence_is_rejected_by_matrix_contract():
    first = pair(2051, 1, 0)
    duplicate = pair(2051, 2, 0)
    duplicate["candidate"]["trajectory_sha256"] = first["candidate"]["trajectory_sha256"]
    with pytest.raises(PairContractError, match="duplicate candidate trajectory evidence"):
        evaluate_campaign([first, duplicate])


def test_complete_reviewed_campaign_passes_only_with_matrix_pass():
    out = evaluate_campaign(full_pass_pairs())
    assert out["status"] == "PASS"
    assert out["campaign_complete"] is True
    assert out["remaining_pair_count"] == 0
    assert out["matrix"]["status"] == "PASS"
    assert out["matrix"]["complete_held_out_seed_count"] == 3


def test_complete_gain_seed_failure_rejects_campaign():
    rows = full_pass_pairs()
    for row in rows:
        if row["pair_identity"]["seed"] == 2055:
            row["comparison"]["net_kill_cost_delta"] = 0
            row["comparison"]["verdict"] = "TIE"
    out = evaluate_campaign(rows)
    assert out["status"] == "REJECT"
    assert out["matrix"]["by_seed"]["2055"]["gate_pass"] is False


def test_behavioral_failure_on_complete_seed_rejects_early():
    rows = [pair(2051, 1, 0), pair(2051, 2, 100), pair(2051, 3, -100, behavior=False)]
    out = evaluate_campaign(rows)
    assert out["status"] == "REJECT"
    assert out["campaign_complete"] is False
    assert out["matrix"]["by_seed"]["2051"]["gate_pass"] is False


def test_output_is_input_order_independent():
    rows = [pair(2051, 1, 0), pair(2055, 1, 100), pair(2052, 1, 0)]
    forward = evaluate_campaign(rows)
    reverse = evaluate_campaign(list(reversed(rows)))
    assert json.dumps(forward, sort_keys=True) == json.dumps(reverse, sort_keys=True)
