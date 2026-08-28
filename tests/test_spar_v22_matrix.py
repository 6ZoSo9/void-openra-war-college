from __future__ import annotations

import pytest

from openra_env.analysis._spar_conditional_v2_2_reviewed_identity import REVIEWED_V22_IDENTITY
from openra_env.analysis.spar_v22_matrix import (
    MATRIX_SCHEMA,
    PairContractError,
    evaluate_matrix,
)
from openra_env.analysis.spar_v22_pair_comparison import PAIR_SCHEMA


def pair(
    seed: int,
    run: int,
    *,
    verdict: str = "TIE",
    delta: float = 0.0,
    protocol_clean: bool = True,
    force: bool = True,
    overall_contact: bool = True,
    post_conversion: bool = True,
    contact: bool = True,
    attack_move: bool = True,
) -> dict:
    return {
        "schema": PAIR_SCHEMA,
        "candidate_only": True,
        "pair_identity": {"seed": seed},
        "baseline": {
            "trajectory_sha256": f"{seed:04x}{run:060x}"[-64:],
        },
        "candidate": {
            "trajectory_sha256": f"{seed + 1:04x}{run + 1000:060x}"[-64:],
            "reviewed_identity_verified": True,
            **{f"v2_2_{key}": value for key, value in REVIEWED_V22_IDENTITY.items()},
        },
        "comparison": {
            "verdict": verdict,
            "net_kill_cost_delta": delta,
            "protocol_clean": protocol_clean,
            "force_preservation_pass": force,
            "overall_productive_contact_pass": overall_contact,
            "post_conversion_productivity_pass": post_conversion,
            "productive_contact_pass": contact,
            "attack_move_reduction_pass": attack_move,
        },
        "authority": {
            "candidate_only": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }


def three(seed: int, specs: list[tuple[str, float]], **kwargs) -> list[dict]:
    return [pair(seed, index + 1, verdict=verdict, delta=delta, **kwargs) for index, (verdict, delta) in enumerate(specs)]


def test_empty_matrix_is_pending():
    report = evaluate_matrix([])
    assert report["schema"] == MATRIX_SCHEMA
    assert report["schema"].endswith("pair-matrix.v2")
    assert report["status"] == "PENDING"
    assert report["pair_count"] == 0


def test_single_seed_2060_pair_is_pending_not_pass():
    report = evaluate_matrix([pair(2060, 1)])
    assert report["status"] == "PENDING"
    assert report["by_seed"]["2060"]["pair_count"] == 1
    assert report["by_seed"]["2060"]["gate_pass"] is None


def test_duplicate_baseline_trajectory_is_rejected():
    first = pair(2051, 1)
    second = pair(2051, 2)
    second["baseline"]["trajectory_sha256"] = first["baseline"]["trajectory_sha256"]
    with pytest.raises(PairContractError, match="duplicate baseline trajectory"):
        evaluate_matrix([first, second])


def test_duplicate_candidate_trajectory_is_rejected():
    first = pair(2051, 1)
    second = pair(2051, 2)
    second["candidate"]["trajectory_sha256"] = first["candidate"]["trajectory_sha256"]
    with pytest.raises(PairContractError, match="duplicate candidate trajectory"):
        evaluate_matrix([first, second])


def test_reviewed_identity_drift_is_rejected():
    row = pair(2051, 1)
    row["candidate"]["v2_2_wrapper_sha256"] = "f" * 64
    with pytest.raises(PairContractError, match="reviewed V2.2 identity mismatch"):
        evaluate_matrix([row])


def test_old_pair_schema_is_rejected():
    row = pair(2051, 1)
    row["schema"] = "void.apollyon.conditional-engagement-v2-2-pair-comparison.v1"
    with pytest.raises(PairContractError, match="schema drift"):
        evaluate_matrix([row])


def test_missing_post_conversion_field_is_rejected():
    row = pair(2051, 1)
    row["comparison"].pop("post_conversion_productivity_pass")
    with pytest.raises(PairContractError, match="post_conversion_productivity_pass"):
        evaluate_matrix([row])


def test_regression_seed_allows_one_worse_with_nonnegative_median():
    rows = three(2051, [("WORSE", -100), ("TIE", 0), ("BETTER", 100)])
    report = evaluate_matrix(rows)
    seed = report["by_seed"]["2051"]
    assert seed["complete"] is True
    assert seed["median_net_delta"] == 0
    assert seed["worse"] == 1
    assert seed["gate_pass"] is True
    assert report["status"] == "PENDING"


def test_regression_seed_rejects_negative_median():
    rows = three(2051, [("WORSE", -200), ("WORSE", -100), ("BETTER", 300)])
    report = evaluate_matrix(rows)
    assert report["by_seed"]["2051"]["gate_pass"] is False
    assert report["status"] == "REJECT"


def test_gain_seed_requires_positive_median_and_two_better():
    passing = three(2055, [("BETTER", 100), ("BETTER", 200), ("TIE", 0)])
    report = evaluate_matrix(passing)
    assert report["by_seed"]["2055"]["gate_pass"] is True

    failing = three(2055, [("BETTER", 100), ("TIE", 0), ("TIE", 0)])
    report = evaluate_matrix(failing)
    assert report["by_seed"]["2055"]["gate_pass"] is False
    assert report["status"] == "REJECT"


def test_post_conversion_failure_rejects_complete_seed_even_if_old_behavior_fields_pass():
    rows = three(2051, [("BETTER", 100), ("BETTER", 100), ("BETTER", 100)])
    rows[1]["comparison"]["post_conversion_productivity_pass"] = False
    report = evaluate_matrix(rows)
    assert report["by_seed"]["2051"]["all_behavioral_gates_pass"] is False
    assert report["by_seed"]["2051"]["gate_pass"] is False
    assert report["status"] == "REJECT"


def test_behavioral_failure_rejects_complete_seed_even_if_net_metric_wins():
    rows = three(2051, [("BETTER", 100), ("BETTER", 100), ("BETTER", 100)])
    rows[1]["comparison"]["productive_contact_pass"] = False
    report = evaluate_matrix(rows)
    assert report["by_seed"]["2051"]["all_behavioral_gates_pass"] is False
    assert report["by_seed"]["2051"]["gate_pass"] is False
    assert report["status"] == "REJECT"


def test_protocol_failure_rejects_complete_seed():
    rows = three(2051, [("TIE", 0), ("BETTER", 100), ("TIE", 0)])
    rows[2]["comparison"]["protocol_clean"] = False
    report = evaluate_matrix(rows)
    assert report["by_seed"]["2051"]["gate_pass"] is False
    assert report["status"] == "REJECT"


def test_three_complete_held_out_seeds_required():
    rows = []
    rows += three(2051, [("TIE", 0), ("BETTER", 100), ("TIE", 0)])
    rows += three(2055, [("BETTER", 100), ("BETTER", 200), ("TIE", 0)])
    rows += three(2052, [("TIE", 0), ("BETTER", 100), ("TIE", 0)])
    rows += three(2053, [("BETTER", 100), ("TIE", 0), ("TIE", 0)])
    report = evaluate_matrix(rows)
    assert report["complete_held_out_seed_count"] == 2
    assert report["status"] == "PENDING"


def test_full_reviewed_matrix_passes_only_when_every_complete_gate_passes():
    rows = []
    rows += three(2051, [("WORSE", -100), ("TIE", 0), ("BETTER", 100)])
    rows += three(2055, [("BETTER", 100), ("BETTER", 200), ("TIE", 0)])
    rows += three(2052, [("TIE", 0), ("BETTER", 100), ("TIE", 0)])
    rows += three(2053, [("BETTER", 100), ("TIE", 0), ("TIE", 0)])
    rows += three(2054, [("TIE", 0), ("TIE", 0), ("BETTER", 100)])
    report = evaluate_matrix(rows)
    assert report["pair_count"] == 15
    assert report["complete_held_out_seed_count"] == 3
    assert report["all_protocol_clean"] is True
    assert report["all_behavioral_gates_pass"] is True
    assert report["status"] == "PASS"


def test_held_out_seed_rejects_two_of_three_worse():
    rows = []
    rows += three(2051, [("TIE", 0), ("BETTER", 100), ("TIE", 0)])
    rows += three(2055, [("BETTER", 100), ("BETTER", 200), ("TIE", 0)])
    rows += three(2052, [("WORSE", -100), ("WORSE", -100), ("BETTER", 100)])
    report = evaluate_matrix(rows)
    assert report["by_seed"]["2052"]["gate_pass"] is False
    assert report["status"] == "REJECT"


def test_repeat_ceiling_is_fail_closed():
    rows = [pair(2051, index + 1) for index in range(4)]
    with pytest.raises(PairContractError, match="exceeds repeat ceiling"):
        evaluate_matrix(rows)
