from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_canary_opponent_v1 as opponent


def state(*, combat=4, visible=(), base_x=15):
    return {
        "map": {"width": 112, "height": 54},
        "units_summary": [
            {"id": 100 + i, "type": "e1", "can_attack": True, "cell_x": base_x, "cell_y": 27}
            for i in range(combat)
        ],
        "buildings_summary": [
            {"id": 10, "type": "fact", "cell_x": base_x, "cell_y": 27},
            {"id": 11, "type": "barr", "cell_x": base_x + 1, "cell_y": 27},
        ],
        "enemy_summary": [
            {"id": uid, "type": "e1", "cell_x": 70, "cell_y": 27}
            for uid in visible
        ],
        "enemy_buildings_summary": [],
    }


def tools(*names):
    return list(names)


def test_visible_contact_attacks_lowest_observed_enemy_id():
    out = opponent.propose_deterministic_pressure_action(
        state(visible=(900, 700, 800)),
        offered_tool_names=tools("advance", "attack_move", "attack_target", "train_unit_e1"),
    )
    assert out["tool"] == "attack_target"
    assert out["arguments"] == {"unit_ids": "all_combat", "target_actor_id": 700}


def test_no_contact_pressures_opposite_half_from_left_base():
    out = opponent.propose_deterministic_pressure_action(
        state(base_x=15), offered_tool_names=tools("advance", "attack_move", "attack_target", "train_unit_e1"))
    assert out["tool"] == "attack_move"
    assert out["arguments"] == {"unit_ids": "all_combat", "target_x": 101, "target_y": 27, "queued": False}


def test_no_contact_pressures_opposite_half_from_right_base():
    out = opponent.propose_deterministic_pressure_action(
        state(base_x=90), offered_tool_names=tools("advance", "attack_move"))
    assert out["arguments"]["target_x"] == 10


def test_critical_force_replenishes_before_pressure_when_exact_tool_is_offered():
    out = opponent.propose_deterministic_pressure_action(
        state(combat=1), offered_tool_names=tools("advance", "attack_move", "train_unit_e1"))
    assert out["tool"] == "train_unit_e1"
    assert out["arguments"] == {"count": 1}


def test_no_force_rebuilds_or_advances_without_inventing_tool():
    out = opponent.propose_deterministic_pressure_action(
        state(combat=0), offered_tool_names=tools("advance", "train_unit_e1"))
    assert out["tool"] == "train_unit_e1"
    fallback = opponent.propose_deterministic_pressure_action(
        state(combat=0), offered_tool_names=tools("advance"))
    assert fallback["tool"] == "advance" and fallback["arguments"] == {}


def test_output_is_deterministic_and_non_authorizing():
    s = state(combat=3)
    names = tools("advance", "attack_move", "attack_target", "train_unit_e1")
    a = opponent.propose_deterministic_pressure_action(deepcopy(s), offered_tool_names=names)
    b = opponent.propose_deterministic_pressure_action(deepcopy(s), offered_tool_names=names)
    assert a == b
    assert a["deterministic"] is True
    assert a["model_backed"] is False
    assert a["learning_performed"] is False
    assert a["host_validation_required"] is True
    assert a["world_mutated_before_validation"] is False
    assert a["execution_authority"] is False
    assert a["training_use_approved"] is False
    assert a["automatic_promotion"] is False


def test_malformed_or_unsupported_input_holds():
    cases = [
        ({}, ["advance"]),
        (state(), []),
        (state(), ["advance", "advance"]),
        ({**state(), "enemy_summary": None}, ["advance"]),
        ({**state(), "buildings_summary": []}, ["attack_move", "advance"]),
    ]
    for raw, names in cases:
        with pytest.raises(opponent.DeterministicOpponentHold):
            opponent.propose_deterministic_pressure_action(raw, offered_tool_names=names)
    with pytest.raises(opponent.DeterministicOpponentHold, match="no_supported_offered_action"):
        opponent.propose_deterministic_pressure_action(state(combat=0), offered_tool_names=["attack_target"])


def test_execution_entrypoint_always_holds():
    with pytest.raises(opponent.DeterministicOpponentHold, match="HOST_VALIDATION"):
        opponent.authorize_or_execute(authorized=True)


def test_source_imports_only_pure_standard_library_modules():
    tree = ast.parse(Path(opponent.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "copy", "typing"}
