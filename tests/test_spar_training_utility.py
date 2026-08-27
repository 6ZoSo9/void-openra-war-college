from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis import spar_training_utility as utility

ENGINE_COMMIT = "1" * 40
WAR_COLLEGE_COMMIT = "2" * 40
GENERATION = "ad1926569b12466c"
IMAGE_ID = "sha256:" + ("3" * 64)
ATTESTATION_SHA = "4" * 64
WARM_START_SHA = "5" * 64
ABADDON_SHA = "6" * 64


def header(*, handoff_tick: int = 100, ticks_per_round: int = 25):
    return {
        "event": "run_header",
        "run_id": "fixture-run",
        "curriculum_id": "fixture-curriculum",
        "generation_id": GENERATION,
        "runtime_image_id": IMAGE_ID,
        "engine_commit": ENGINE_COMMIT,
        "war_collee_commit": WAR_COLLEGE_COMMIT,
        "joint_training_attestation_sha256": ATTESTATION_SHA,
        "warm_start_sha256": WARM_START_SHA,
        "warm_start_handoff": {
            "tick": handoff_tick,
            "contact_achieved": True,
        },
        "apollyon_model": "fixture-apollyon",
        "abaddon_controller_sha256": ABADDON_SHA,
        "abaddon_doctrine": "RUSHER",
        "seed": 2050,
        "round_limit": 36,
        "ticks_per_round": ticks_per_round,
        "candidate_only": True,
        "review_required": True,
        "agent_training_rows_begin_here": True,
    }


def state(*, tick: int, visible=0, combat=2, kills=0, deaths=0):
    return {
        "tick": tick,
        "enemy_summary": [{"actor_id": 99}] * visible,
        "enemy_buildings_summary": [],
        "units_summary": [
            {"actor_id": index + 1, "can_attack": True}
            for index in range(combat)
        ],
        "military": {
            "units_killed": kills // 100,
            "units_lost": deaths // 100,
            "buildings_killed": 0,
            "buildings_lost": 0,
            "kills_cost": kills,
            "deaths_cost": deaths,
        },
    }


def decision(
    round_number,
    tick,
    *,
    ap_tool="advance",
    ap_commands=0,
    ab_tool="advance",
    ab_commands=0,
    before_ap=None,
    before_ab=None,
):
    return {
        "event": "joint_decision",
        "run_id": "fixture-run",
        "curriculum_id": "fixture-curriculum",
        "round": round_number,
        "start_tick": tick,
        "apollyon_state": before_ap or state(tick=tick),
        "abaddon_state": before_ab or state(tick=tick),
        "apollyon": {
            "tool": ap_tool,
            "command_count": ap_commands,
            "attempts": [
                {
                    "tool": ap_tool,
                    "accepted": True,
                    "world_mutated_before_validation": False,
                }
            ],
            "tool_contract": {"offered_tool_names": [ap_tool]},
        },
        "abaddon": {
            "accepted": True,
            "command_count": ab_commands,
            "decision": {"action": {"tool": ab_tool}},
        },
        "candidate_only": True,
        "training_candidate": True,
        "controller_authored": True,
    }


def result(
    round_number,
    start,
    end,
    *,
    after_ap=None,
    after_ab=None,
    phase="playing",
    winner="",
):
    return {
        "event": "joint_result",
        "run_id": "fixture-run",
        "curriculum_id": "fixture-curriculum",
        "round": round_number,
        "start_tick": start,
        "end_tick": end,
        "apollyon_after": after_ap or state(tick=end),
        "abaddon_after": after_ab or state(tick=end),
        "phase": phase,
        "winner": winner,
        "candidate_only": True,
        "training_candidate": True,
        "controller_authored": True,
    }


def write_jsonl(path: Path, rows):
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_summary(path: Path, trajectory: Path, *, final_ap, final_ab):
    obj = {
        "schema": "void.apollyon-abaddon.warm-start-combat-spar-summary.v1",
        "run_id": "fixture-run",
        "curriculum_id": "fixture-curriculum",
        "generation_id": GENERATION,
        "runtime_image_id": IMAGE_ID,
        "warm_start_sha256": WARM_START_SHA,
        "warm_start_handoff": {"tick": 100, "contact_achieved": True},
        "trajectory_sha256": hashlib.sha256(trajectory.read_bytes()).hexdigest(),
        "seed": 2050,
        "abaddon_doctrine": "RUSHER",
        "rounds_completed": 3,
        "ticks_per_round": 25,
        "final_tick": 175,
        "status": "round_limit",
        "winner": "",
        "outcome": "DRAW_OR_UNFINISHED",
        "apollyon_final": final_ap,
        "abaddon_final": final_ab,
        "candidate_only": True,
        "warm_start_rows_training_candidate": False,
        "controller_rows_training_candidate": True,
        "automatic_corpus_admission": False,
        "automatic_apollyon_weight_mutation": False,
        "automatic_abaddon_policy_promotion": False,
    }
    path.write_text(json.dumps(obj, sort_keys=True) + "\n", encoding="utf-8")


def good_rows():
    ap_100 = state(tick=100)
    ab_100 = state(tick=100)
    ap_125 = state(tick=125)
    ab_125 = state(tick=125)
    ap_150 = state(tick=150, visible=1, kills=100)
    ab_150 = state(tick=150, visible=1, deaths=100)
    ap_175 = state(tick=175, combat=3, kills=100)
    ab_175 = state(tick=175, deaths=100)
    return [
        header(),
        decision(
            1,
            100,
            ap_tool="advance",
            ap_commands=0,
            ab_tool="attack_move",
            ab_commands=1,
            before_ap=ap_100,
            before_ab=ab_100,
        ),
        result(1, 100, 125, after_ap=ap_125, after_ab=ab_125),
        decision(
            2,
            125,
            ap_tool="attack_move",
            ap_commands=1,
            ab_tool="attack_target",
            ab_commands=1,
            before_ap=ap_125,
            before_ab=ab_125,
        ),
        result(2, 125, 150, after_ap=ap_150, after_ab=ab_150),
        decision(
            3,
            150,
            ap_tool="train_unit_e1",
            ap_commands=1,
            ab_tool="advance",
            ab_commands=0,
            before_ap=ap_150,
            before_ab=ab_150,
       ),
        result(3, 150, 175, after_ap=ap_175, after_ab=ab_175),
    ]


def test_analyzer_derives_contact_damage_idle_and_production(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    summary = tmp_path / "summary.json"
    rows = good_rows()
    write_jsonl(trajectory, rows)
    final = rows[-1]
    write_summary(
        summary,
        trajectory,
        final_ap=final["apollyon_after"],
        final_ab=final["abaddon_after"],
    )

    report = utility.analyze_trajectory(trajectory, summary_path=summary)

    assert report["training_utility"]["classification"] == "TACTICAL_DAMAGE_PRESENT"
    assert report["training_utility"]["first_damage_tick"] == 150
    assert report["training_utility"]["contact_distribution_rounds"] == {
        "none": 2,
        "apollyon_only": 0,
        "abaddon_only": 0,
        "mutual": 1,
    }
    apollyon = report["sides"]["apollyon"]
    assert apollyon["first_enemy_visible"]["tick"] == 150
    assert apollyon["first_hostile_order"]["tick"] == 125
    assert apollyon["first_damage_inflicted"]["kills_cost_delta"] == 100
    assert apollyon["first_combat_capable_production"]["completion_tick"] == 175
    assert apollyon["first_combat_capable_production"]["ticks_from_handoff"] == 75
    assert apollyon["no_command_rounds"] == [1]
    assert apollyon["no_command_fraction"] == pytest.approx(1 / 3)
    assert report["integrity"]["summary_verified"] is True
    assert report["authority"]["automatic_corpus_admission"] is False


def test_delayed_production_completion_binds_latest_prior_order(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    ap_100 = state(tick=100)
    ab_100 = state(tick=100)
    ap_125 = state(tick=125)
    ab_125 = state(tick=125)
    ap_150 = state(tick=150, combat=3)
    ab_150 = state(tick=150)
    rows = [
        header(),
        decision(
            1,
            100,
            ap_tool="train_unit_e1",
            ap_commands=1,
            before_ap=ap_100,
            before_ab=ab_100,
        ),
        result(1, 100, 125, after_ap=ap_125, after_ab=ab_125),
        decision(2, 125, before_ap=ap_125, before_ab=ab_125),
        result(2, 125, 150, after_ap=ap_150, after_ab=ab_150),
    ]
    write_jsonl(trajectory, rows)
    report = utility.analyze_trajectory(trajectory)
    production = report["sides"]["apollyon"][
        "first_combat_capable_production"
    ]
    assert production["order"] == {
        "round": 1,
        "tick": 100,
        "tool": "train_unit_e1",
    }
    assert production["completion_round"] == 2
    assert production["completion_tick"] == 150
    assert production["attribution"] == "latest_prior_controller_production_order"

def test_requires_header_and_exact_alternation(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    write_jsonl(trajectory, [decision(1, 100), result(1, 100, 125)])
    with pytest.raises(utility.ContractError, match="run_header"):
        utility.analyze_trajectory(trajectory)

    write_jsonl(
        trajectory,
        [header(), decision(1, 100), decision(2, 125)],
    )
    with pytest.raises(utility.ContractError, match="before the previous"):
        utility.analyze_trajectory(trajectory)

    write_jsonl(
        trajectory,
        [
            header(),
            decision(1, 100),
            result(1, 100, 125),
            decision(3, 125),
            result(3, 125, 150),
        ],
    )
    with pytest.raises(utility.ContractError, match="expected decision round 2"):
        utility.analyze_trajectory(trajectory)


def test_rejects_tick_gap_counter_regression_and_state_discontinuity(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    write_jsonl(
        trajectory,
        [
            header(),
            decision(1, 100),
            result(1, 100, 125),
            decision(2, 126),
            result(2, 126, 151),
        ],
    )
    with pytest.raises(utility.ContractError, match="does not continue"):
        utility.analyze_trajectory(trajectory)

    write_jsonl(
        trajectory,
        [
            header(),
            decision(
                1,
                100,
                before_ap=state(tick=100, kills=100),
                before_ab=state(tick=100, deaths=100),
            ),
            result(
                1,
                100,
                125,
                after_ap=state(tick=125, kills=0),
                after_ab=state(tick=125, deaths=0),
            ),
        ],
    )
    with pytest.raises(utility.ContractError, match="regressed"):
        utility.analyze_trajectory(trajectory)

    write_jsonl(
        trajectory,
        [
            header(),
            decision(1, 100),
            result(1, 100, 125),
            decision(
                2,
                125,
                before_ap=state(tick=125, combat=3),
                before_ab=state(tick=125),
            ),
            result(2, 125, 150),
        ],
    )
    with pytest.raises(utility.ContractError, match="does not continue"):
        utility.analyze_trajectory(trajectory)


def test_rejects_rejected_attempt_without_zero_mutation_attestation(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    row = decision(1, 100, ap_tool="attack_move", ap_commands=1)
    row["apollyon"]["attempts"] = [
        {"tool": "bogus", "accepted": False},
        {
            "tool": "attack_move",
            "accepted": True,
            "world_mutated_before_validation": False,
        },
    ]
    write_jsonl(trajectory, [header(), row, result(1, 100, 125)])
    with pytest.raises(utility.ContractError, match="must be false"):
        utility.analyze_trajectory(trajectory)


def test_rejects_summary_hash_authority_or_final_state_drift(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    summary = tmp_path / "summary.json"
    rows = good_rows()
    write_jsonl(trajectory, rows)
    final = rows[-1]
    write_summary(
        summary,
        trajectory,
        final_ap=final["apollyon_after"],
        final_ab=final["abaddon_after"],
    )

    with pytest.raises(utility.ContractError, match="trajectory SHA-256 mismatch"):
        utility.analyze_trajectory(
            trajectory,
            expected_trajectory_sha256="0" * 64,
        )

    obj = json.loads(summary.read_text())
    obj["automatic_corpus_admission"] = True
    summary.write_text(json.dumps(obj) + "\n")
    with pytest.raises(utility.ContractError, match="must be false"):
        utility.analyze_trajectory(trajectory, summary_path=summary)

    write_summary(
        summary,
        trajectory,
        final_ap=state(tick=175, combat=99, kills=100),
        final_ab=final["abaddon_after"],
    )
    with pytest.raises(utility.ContractError, match="apollyon_final"):
        utility.analyze_trajectory(trajectory, summary_path=summary)


def test_requires_summary_when_summary_digest_is_supplied(tmp_path):
    trajectory = tmp_path / "trajectory.jsonl"
    write_jsonl(trajectory, good_rows())
    with pytest.raises(utility.ContractError, match="requires --summary"):
        utility.analyze_trajectory(
            trajectory,
            expected_summary_sha256="0" * 64,
        )


def test_visibility_fallback_contact_episodes_and_trade_ratio():
    assert utility.visible_count(
        {"visible_enemy_units": 2, "visible_enemy_buildings": 1}
    ) == 3
    assert utility.contact_episodes([1, 2, 5, 8, 9]) == [
        {"start_round": 1, "end_round": 2, "rounds": [1, 2]},
        {"start_round": 5, "end_round": 5, "rounds": [5]},
        {"start_round": 8, "end_round": 9, "rounds": [8, 9]},
    ]
    ratio = utility.trade_ratio(
        {
            "kills_cost": 100,
            "deaths_cost": 0,
            "units_killed": 1,
            "units_lost": 0,
            "buildings_killed": 0,
            "buildings_lost": 0,
        }
    )
    assert ratio == {
        "kills_cost": 100,
        "deaths_cost": 0,
        "value": None,
        "infinite": True,
    }


def test_stable_json_and_atomic_output(tmp_path):
    value = {"b": 2, "a": 1}
    encoded = utility.stable_json(value)
    assert encoded == '{"a":1,"b":2}\n'
    output = tmp_path / "nested" / "report.json"
    utility.atomic_write(output, encoded)
    assert output.read_text() == encoded
