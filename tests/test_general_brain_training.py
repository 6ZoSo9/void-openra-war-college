from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning.general_brain_generation import (
    NONTRAINABLE_AUTHORITY_ENVELOPE,
    make_generation_zero,
    manifest_sha256,
)
from openra_env.learning.general_brain_training import (
    ADAPTER_SCHEMA,
    CORPUS_SNAPSHOT_SCHEMA,
    IMITATION_RECORD_SCHEMA,
    PREFERENCE_RECORD_SCHEMA,
    PROMOTION_EVALUATION_SCHEMA,
    GeneralBrainTrainingError,
    adapter_sha256,
    build_corpus_snapshot,
    corpus_snapshot_sha256,
    evaluate_promotion,
    extract_apollyon_training_records,
    make_challenger_from_training,
    make_training_receipt,
    train_tactical_preference_adapter,
    training_receipt_sha256,
)

CANDIDATE_SHA = "92f10e87f01a388882f621a09989783d561302cc46583a5344e8108c81d864ab"
SOURCE_COMMIT = "c7084294253793b101cc2826726a8cfa0b294c37"
POLICY_SHA = "fce4dfd00b0465e5545dd50d7fee1eadecf182577ba90f85b77b2987e8574f80"
SESSION_SHA = "7d11da6f5b485a20380485edd8c9d589f50be70b23f6bc4426a3c3d2e532d890"
WRAPPER_SHA = "72622f36a8374b277529a294f4bd42160f2690d69306f67ef4863d6bede71097"
PARENT_V21_SHA = "a0b08f7a7ea807de53416f589790059e2540404f680d6b470395bdbdc067f460"


def state(tick: int, *, combat: int = 5) -> dict:
    return {
        "tick": tick,
        "enemy_summary": [],
        "enemy_buildings_summary": [],
        "units_summary": [
            {"actor_id": index + 1, "can_attack": True}
            for index in range(combat)
        ],
        "military": {
            "units_killed": 0,
            "units_lost": 0,
            "buildings_killed": 0,
            "buildings_lost": 0,
            "kills_cost": 0,
            "deaths_cost": 0,
        },
    }


def header() -> dict:
    return {
        "event": "run_header",
        "run_id": "training-fixture-run",
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "generation_id": "ad1926569b12466c",
        "runtime_image_id": "sha256:" + "3" * 64,
        "engine_commit": "1" * 40,
        "war_college_commit": "2" * 40,
        "joint_training_attestation_sha256": "4" * 64,
        "warm_start_sha256": "5" * 64,
        "warm_start_handoff": {"tick": 100, "contact_achieved": False},
        "apollyon_model": "fixture-apollyon",
        "abaddon_controller_sha256": "6" * 64,
        "abaddon_doctrine": "RUSHER",
        "seed": 2051,
        "round_limit": 1,
        "ticks_per_round": 25,
        "candidate_only": True,
        "review_required": True,
        "agent_training_rows_begin_here": True,
        "conditional_engagement_v2_2": {
            "schema": "void.apollyon.conditional-engagement-run-binding.v2.2",
            "candidate_only": True,
            "source_commit": SOURCE_COMMIT,
            "candidate_sha256": CANDIDATE_SHA,
            "policy_sha256": POLICY_SHA,
            "session_sha256": SESSION_SHA,
            "wrapper_sha256": WRAPPER_SHA,
            "parent_v2_1_candidate_sha256": PARENT_V21_SHA,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
            "automatic_corpus_admission": False,
        },
    }


def coaching() -> str:
    return "\n".join(
        [
            "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_2",
            "MODE=FORCE_CONVERSION",
            "OBSERVED_REASONS=BLIND_ATTACK_MOVE_STREAK",
            "CURRENT_ALLOWED_TOOL_NAMES=attack_move,move_units",
            "BOUNDARY=Use exactly one function from CURRENT_ALLOWED_TOOL_NAMES; do not infer hidden state or invent actor IDs.",
            "TOOL_SURFACE_UNCHANGED=true",
            "FORCE_CONVERSION_ACTION_RULE=Do not choose attack_move this round; choose a currently offered alternative with a deliberate observable objective.",
            "PREFERRED_OFFERED_ALTERNATIVE=move_units",
            'PREFERRED_MOVE_UNITS_SELECTOR=unit_ids="all_combat"',
            'SELECTOR_INTEGRITY_RULE=When choosing move_units for FORCE_CONVERSION, use unit_ids="all_combat" exactly; do not enumerate, remember, or invent actor IDs.',
            "NON_ATTACK_MOVE_OFFERED_NAMES=move_units",
            "COACHING=convert force",
        ]
    )


def decision(*, selected: str = "attack_move", attempts: int = 1, selected_args: dict | None = None) -> dict:
    rows = []
    for index in range(attempts):
        tool = selected if index == attempts - 1 else "attack_move"
        row = {
            "tool": tool,
            "accepted": index == attempts - 1,
            "world_mutated_before_validation": False,
        }
        if index == attempts - 1 and selected_args is not None:
            row["arguments"] = copy.deepcopy(selected_args)
        rows.append(row)
    return {
        "event": "joint_decision",
        "run_id": "training-fixture-run",
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "round": 1,
        "start_tick": 100,
        "apollyon_state": state(100),
        "abaddon_state": state(100),
        "apollyon": {
            "tool": selected,
            "command_count": 1,
            "attempts": rows,
            "tool_contract": {"offered_tool_names": ["attack_move", "move_units"]},
        },
        "abaddon": {
            "accepted": True,
            "command_count": 1,
            "decision": {"action": {"tool": "attack_move"}},
        },
        "candidate_only": True,
        "training_candidate": True,
        "controller_authored": True,
        "conditional_engagement_v2_2": {
            "prepared": {
                "schema": "void.apollyon.conditional-engagement-prepared-round.v2.2",
                "round": 1,
                "candidate_sha256": CANDIDATE_SHA,
                "current_allowed_tool_names": ["attack_move", "move_units"],
                "decision": {
                    "schema": "void.apollyon.conditional-engagement-decision.v2.2",
                    "mode": "FORCE_CONVERSION",
                    "reasons": ["BLIND_ATTACK_MOVE_STREAK"],
                    "candidate_sha256": CANDIDATE_SHA,
                    "runtime_seed_branching": False,
                    "evidence": {"round": 1},
                    "instruction": "convert force",
                },
                "coaching": coaching(),
                "action_compliance": {
                    "schema": "void.apollyon.conditional-engagement-action-compliance.v2.2",
                    "mode": "FORCE_CONVERSION",
                    "tool_surface_unchanged": True,
                    "attack_move_discouraged": True,
                    "preferred_offered_alternative": "move_units",
                    "non_attack_move_offered_names": ["move_units"],
                },
                "history_committed": False,
            },
            "accepted": {
                "schema": "void.apollyon.conditional-engagement-accepted-round.v2.2",
                "round": 1,
                "candidate_sha256": CANDIDATE_SHA,
                "mode": "FORCE_CONVERSION",
                "reasons": ["BLIND_ATTACK_MOVE_STREAK"],
                "selected_tool": selected,
                "function_was_offered": True,
                "history_size": 1,
            },
        },
    }


def result() -> dict:
    return {
        "event": "joint_result",
        "run_id": "training-fixture-run",
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "round": 1,
        "start_tick": 100,
        "end_tick": 125,
        "apollyon_after": state(125),
        "abaddon_after": state(125),
        "phase": "playing",
        "winner": "",
        "candidate_only": True,
        "training_candidate": True,
        "controller_authored": True,
    }


def write_trajectory(path: Path, decision_row: dict) -> str:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in [header(), decision_row, result()]),
        encoding="utf-8",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_extracts_reviewed_counterfactual_preference(tmp_path: Path):
    trajectory = tmp_path / "trajectory.jsonl"
    digest = write_trajectory(trajectory, decision(selected="attack_move"))
    records = extract_apollyon_training_records(trajectory, expected_trajectory_sha256=digest)
    assert len(records) == 1
    record = records[0]
    assert record["schema"] == PREFERENCE_RECORD_SCHEMA
    assert record["chosen"] == {"tool": "move_units", "arguments": {"unit_ids": "all_combat"}}
    assert record["rejected"]["tool"] == "attack_move"
    assert record["authority_labels_included"] is False


def test_positive_imitation_requires_exact_reviewed_selector(tmp_path: Path):
    good = tmp_path / "good.jsonl"
    write_trajectory(good, decision(selected="move_units", selected_args={"unit_ids": "all_combat"}))
    records = extract_apollyon_training_records(good)
    assert len(records) == 1
    assert records[0]["schema"] == IMITATION_RECORD_SCHEMA

    unbound = tmp_path / "unbound.jsonl"
    write_trajectory(unbound, decision(selected="move_units", selected_args={"unit_ids": [1, 2, 3]}))
    assert extract_apollyon_training_records(unbound) == []


def test_retry_round_is_excluded_from_weight_training(tmp_path: Path):
    trajectory = tmp_path / "retry.jsonl"
    write_trajectory(trajectory, decision(selected="attack_move", attempts=2))
    assert extract_apollyon_training_records(trajectory) == []


def test_corpus_and_adapter_are_deterministic_and_authority_free(tmp_path: Path):
    bad = tmp_path / "bad-choice.jsonl"
    good = tmp_path / "good-choice.jsonl"
    bad_sha = write_trajectory(bad, decision(selected="attack_move"))
    good_sha = write_trajectory(good, decision(selected="move_units", selected_args={"unit_ids": "all_combat"}))

    snapshot = build_corpus_snapshot("apollyon", [(good, good_sha), (bad, bad_sha)])
    assert snapshot["schema"] == CORPUS_SNAPSHOT_SCHEMA
    assert snapshot["record_count"] == 2
    assert snapshot["preference_record_count"] == 1
    assert snapshot["positive_imitation_record_count"] == 1
    assert snapshot["authority_envelope_trainable"] is False

    parent = make_generation_zero("apollyon")
    adapter = train_tactical_preference_adapter(parent, snapshot)
    assert adapter["schema"] == ADAPTER_SCHEMA
    assert adapter["weights"]["FORCE_CONVERSION"]["move_units"] == pytest.approx(1.25)
    assert adapter["weights"]["FORCE_CONVERSION"]["attack_move"] == pytest.approx(-1.0)
    assert adapter["authority_envelope_embedded"] is False

    receipt = make_training_receipt(parent, snapshot, adapter)
    challenger = make_challenger_from_training(parent, snapshot, adapter, receipt)
    assert challenger["generation"] == 1
    assert challenger["competence_adapter"]["state"] == "challenger"
    assert challenger["competence_adapter"]["artifact_sha256"] == adapter_sha256(adapter)
    assert challenger["authority_envelope"] == parent["authority_envelope"] == NONTRAINABLE_AUTHORITY_ENVELOPE
    assert challenger["training_lineage"]["corpus_snapshot_sha256"] == corpus_snapshot_sha256(snapshot)
    assert challenger["training_lineage"]["training_receipt_sha256"] == training_receipt_sha256(receipt)


def test_empty_corpus_cannot_mutate_weights():
    parent = make_generation_zero("apollyon")
    snapshot = {
        "schema": CORPUS_SNAPSHOT_SCHEMA,
        "general_id": "apollyon",
        "scope": "tactical_competence_only",
        "records": [],
        "record_count": 0,
        "preference_record_count": 0,
        "positive_imitation_record_count": 0,
        "source_trajectory_sha256": [],
        "excluded_from_training": [
            "authority_envelope",
            "role_hierarchy",
            "sovereign_directives",
            "tool_authorization",
            "promotion_authority",
        ],
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }
    with pytest.raises(GeneralBrainTrainingError, match="no trainable tactical records"):
        train_tactical_preference_adapter(parent, snapshot)


def promotion_fixture(parent: dict, challenger: dict) -> dict:
    return {
        "schema": PROMOTION_EVALUATION_SCHEMA,
        "incumbent_manifest_sha256": manifest_sha256(parent),
        "challenger_manifest_sha256": manifest_sha256(challenger),
        "authority_envelope_match": True,
        "all_protocol_clean": True,
        "all_behavioral_gates_pass": True,
        "critical_seeds": {
            "2051": {"complete": True, "median_challenger_minus_incumbent": 0.0},
            "2055": {"complete": True, "median_challenger_minus_incumbent": 100.0},
        },
        "heldout_seeds": {
            "2052": {"complete": True, "worse_pairs": 0},
            "2053": {"complete": True, "worse_pairs": 1},
            "2054": {"complete": True, "worse_pairs": 0},
        },
    }


def test_promotion_gate_requires_evidence_and_never_auto_promotes():
    parent = make_generation_zero("apollyon")
    # Build a structurally valid challenger directly from synthetic digests.
    from openra_env.learning.general_brain_generation import make_challenger_generation

    challenger = make_challenger_generation(
        parent,
        adapter_artifact_sha256="a" * 64,
        corpus_snapshot_sha256="b" * 64,
        training_receipt_sha256="c" * 64,
    )
    passing = evaluate_promotion(parent, challenger, promotion_fixture(parent, challenger))
    assert passing["eligible_for_promotion"] is True
    assert passing["automatic_promotion"] is False
    assert passing["review_required"] is True

    failed_eval = promotion_fixture(parent, challenger)
    failed_eval["all_behavioral_gates_pass"] = False
    failed = evaluate_promotion(parent, challenger, failed_eval)
    assert failed["eligible_for_promotion"] is False
    assert "BEHAVIORAL_GATE_FAILED" in failed["reasons"]

    drifted = copy.deepcopy(challenger)
    drifted["authority_envelope"]["sovereign_directives_trainable"] = True
    with pytest.raises(Exception):
        evaluate_promotion(parent, drifted, promotion_fixture(parent, challenger))
