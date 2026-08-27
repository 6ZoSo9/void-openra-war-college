from __future__ import annotations

import copy
import hashlib

import pytest

from openra_env.analysis import spar_pair_comparison as pair

CANDIDATE_SHA = "a" * 64
SOURCE_COMMIT = "b" * 40


def report(
    *,
    seed=2060,
    net=0,
    final_combat=0,
    attack_move=10,
    rounds=72,
    v2=False,
    retries=None,
    run=0,
):
    retries = [] if retries is None else retries
    provenance = {
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "generation_id": "ad1926569b12466c",
        "runtime_image_id": "sha256:" + "1" * 64,
        "engine_commit": "2" * 40,
        "war_college_commit": "3" * 40,
        "joint_training_attestation_sha256": "4" * 64,
        "warm_start_sha256": "5" * 64,
        "warm_start_handoff": {"tick": 2651, "contact_achieved": False},
        "warm_start_handoff_tick": 2651,
        "apollyon_model": "apollyon",
        "abaddon_controller_sha256": "6" * 64,
        "abaddon_doctrine": "RUSHER",
        "seed": seed,
        "round_limit": 72,
        "ticks_per_round": 25,
        "trajectory_sha256": hashlib.sha256(
            f"trajectory:{seed}:{v2}:{run}".encode()
        ).hexdigest(),
        "summary_sha256": hashlib.sha256(
            f"summary:{seed}:{v2}:{run}".encode()
        ).hexdigest(),
    }
    return {
        "marker": "VOID_WAR_COLLEGE_SPAR_TRAINING_UTILITY_V1",
        "version": 1,
        "provenance": provenance,
        "integrity": {
            "trajectory_verified": True,
            "summary_verified": True,
            "rounds_completed": rounds,
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
                "tools": {"attack_move": attack_move, "attack_target": 2},
                "retried_rounds": retries,
            },
            "abaddon": {
                "final_combat_capable_units": 5,
                "net_kill_cost": -net,
                "tools": {"attack_move": 20},
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
        "conditional_engagement_v2": (
            {"present": False, "rounds_verified": 0, "mode_counts": {}}
            if not v2
            else {
                "present": True,
                "rounds_verified": rounds,
                "mode_counts": {
                    "REBUILD_FORCE": 10,
                    "BALANCED_SEARCH": rounds - 10,
                },
                "source_commit": SOURCE_COMMIT,
                "candidate_sha256": CANDIDATE_SHA,
                "all_round_receipts_verified": True,
                "tool_surface_bound": True,
                "accepted_tool_bound": True,
                "runtime_seed_branching": False,
            }
        ),
    }


def test_compare_uses_net_delta_primary_and_preserves_diagnostics():
    out = pair.compare_reports(
        report(net=0, final_combat=0, attack_move=50),
        report(net=400, final_combat=4, attack_move=20, v2=True),
        expected_v2_candidate_sha256=CANDIDATE_SHA,
        expected_v2_source_commit=SOURCE_COMMIT,
    )
    assert out["comparison"]["verdict"] == "BETTER"
    assert out["comparison"]["net_kill_cost_delta"] == 400
    assert out["comparison"]["final_combat_delta"] == 4
    assert out["comparison"]["attack_move_fraction_delta"] < 0
    assert out["comparison"]["protocol_clean"] is True


@pytest.mark.parametrize(
    "field",
    [
        "seed",
        "abaddon_doctrine",
        "generation_id",
        "runtime_image_id",
        "engine_commit",
        "warm_start_sha256",
        "ticks_per_round",
    ],
)
def test_pair_identity_drift_fails_closed(field):
    baseline = report()
    candidate = report(v2=True)
    candidate["provenance"][field] = (
        999 if field in {"seed", "ticks_per_round"} else "drift"
    )
    with pytest.raises(pair.PairContractError, match="pair identity mismatch"):
        pair.compare_reports(baseline, candidate)


def test_baseline_v2_presence_and_candidate_identity_fail_closed():
    baseline = report()
    candidate = report(v2=True)
    baseline["conditional_engagement_v2"] = copy.deepcopy(
        candidate["conditional_engagement_v2"]
    )
    with pytest.raises(pair.PairContractError, match="baseline unexpectedly"):
        pair.compare_reports(baseline, candidate)

    baseline = report()
    with pytest.raises(pair.PairContractError, match="unexpected V2 candidate"):
        pair.compare_reports(
            baseline,
            candidate,
            expected_v2_candidate_sha256="f" * 64,
        )


def test_retries_make_pair_protocol_unclean_without_changing_primary_verdict():
    out = pair.compare_reports(
        report(),
        report(net=100, v2=True, retries=[7]),
    )
    assert out["comparison"]["verdict"] == "BETTER"
    assert out["comparison"]["protocol_clean"] is False
    assert out["comparison"]["invalid_attempt_count_zero"] is False


def mkpair(seed, delta, clean=True, run=0):
    baseline = report(seed=seed, net=0, run=run)
    candidate = report(
        seed=seed,
        net=delta,
        v2=True,
        retries=[] if clean else [1],
        run=run,
    )
    return pair.compare_reports(baseline, candidate)


def test_matrix_pending_with_single_held_out_pair():
    out = pair.evaluate_matrix([mkpair(2060, 400)])
    assert out["status"] == "PENDING"
    assert out["by_seed"]["2060"]["pair_count"] == 1
    assert out["by_seed"]["2060"]["gate_pass"] is None


def test_matrix_passes_exact_reviewed_and_three_held_out_seeds():
    rows = []
    for run, delta in enumerate((0, 100, -50), 1):
        rows.append(mkpair(2051, delta, run=run))
    for run, delta in enumerate((600, 500, -100), 1):
        rows.append(mkpair(2055, delta, run=run))
    for seed in (2060, 2061, 2062):
        for run, delta in enumerate((100, 0, -50), 1):
            rows.append(mkpair(seed, delta, run=run))

    out = pair.evaluate_matrix(rows)
    assert out["status"] == "PASS"
    assert out["by_seed"]["2051"]["gate_pass"] is True
    assert out["by_seed"]["2055"]["gate_pass"] is True
    assert out["complete_held_out_seeds"] == [2060, 2061, 2062]


def test_matrix_fails_completed_seed_gate_or_protocol():
    rows = [
        mkpair(2051, -100, run=1),
        mkpair(2051, -200, run=2),
        mkpair(2051, 100, run=3),
    ]
    out = pair.evaluate_matrix(rows)
    assert out["status"] == "FAIL"
    assert out["by_seed"]["2051"]["gate_pass"] is False

    out = pair.evaluate_matrix([mkpair(2060, 100, clean=False)])
    assert out["status"] == "FAIL"
    assert out["all_protocol_clean"] is False


def test_matrix_rejects_mixed_candidate_generation_and_repeat_overflow():
    first = mkpair(2060, 100)
    second = mkpair(2061, 100)
    second["candidate"]["v2_candidate_sha256"] = "f" * 64
    with pytest.raises(pair.PairContractError, match="mixed V2 candidate"):
        pair.evaluate_matrix([first, second])

    with pytest.raises(pair.PairContractError, match="repeat ceiling"):
        pair.evaluate_matrix(
            [
                mkpair(2060, delta, run=run)
                for run, delta in enumerate((1, 2, 3, 4), 1)
            ]
        )


def test_matrix_rejects_duplicate_trajectory_evidence():
    evidence = mkpair(2060, 100, run=1)
    with pytest.raises(pair.PairContractError, match="duplicate baseline trajectory"):
        pair.evaluate_matrix([evidence, copy.deepcopy(evidence)])


def test_stable_json_is_deterministic():
    assert pair.stable_json({"b": 2, "a": 1}) == '{"a":1,"b":2}\n'
