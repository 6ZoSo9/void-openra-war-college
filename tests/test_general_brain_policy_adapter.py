from __future__ import annotations

from openra_env.learning.general_brain_direct_policy import propose_direct_policy_action
from openra_env.learning.general_brain_generation import (
    NONTRAINABLE_AUTHORITY_ENVELOPE,
    make_challenger_generation,
    make_generation_zero,
)
from openra_env.learning.general_brain_policy_adapter import (
    ALGORITHM_ID,
    POLICY_ADAPTER_SCHEMA,
    POLICY_RECORD_SCHEMA,
    POLICY_SNAPSHOT_SCHEMA,
    classify_force_conversion_move,
    policy_adapter_sha256,
    train_policy_adapter_revision_two,
)


def military(kills=0, deaths=0):
    return {
        "units_killed": kills // 100,
        "units_lost": deaths // 100,
        "buildings_killed": 0,
        "buildings_lost": 0,
        "kills_cost": kills,
        "deaths_cost": deaths,
    }


def state(*, kills=0, deaths=0, visible=False, width=100, height=80, combat=5):
    return {
        "map": {"width": width, "height": height},
        "military": military(kills, deaths),
        "units_summary": [
            {"id": index + 1, "can_attack": True}
            for index in range(combat)
        ],
        "enemy_summary": ([{"id": 9001}] if visible else []),
        "enemy_buildings_summary": [],
    }


def force_conversion_decision(*, target_x=50, target_y=40):
    return {
        "apollyon": {
            "tool": "move_units",
            "attempts": [
                {
                    "attempt": 1,
                    "tool": "move_units",
                    "arguments": {
                        "unit_ids": "all_combat",
                        "target_x": target_x,
                        "target_y": target_y,
                        "queued": False,
                    },
                    "accepted": True,
                    "world_mutated_before_validation": False,
                }
            ],
        },
        "apollyon_state": state(),
        "conditional_engagement_v2_2": {
            "prepared": {"decision": {"mode": "FORCE_CONVERSION"}},
            "accepted": {"selected_tool": "move_units"},
        },
    }


def result(after):
    return {"apollyon_after": after}


def test_valid_first_attempt_is_not_positive_without_utility():
    row = classify_force_conversion_move(
        force_conversion_decision(),
        [result(state()), result(state()), result(state())],
        source_trajectory_sha256="a" * 64,
        seed=2055,
        round_no=10,
    )
    assert row is None


def test_contact_without_loss_becomes_portable_policy_record():
    row = classify_force_conversion_move(
        force_conversion_decision(target_x=25, target_y=60),
        [result(state()), result(state(visible=True)), result(state(visible=True))],
        source_trajectory_sha256="a" * 64,
        seed=2055,
        round_no=10,
    )
    assert row is not None
    assert row["schema"] == POLICY_RECORD_SCHEMA
    assert row["utility"]["utility_positive"] is True
    assert row["unit_selector"] == "all_combat"
    assert row["target_policy"] == "normalized_map_fraction"
    assert 0 <= row["target_x_millis"] <= 1000
    assert 0 <= row["target_y_millis"] <= 1000
    assert row["authority_labels_included"] is False


def test_damage_with_worse_trade_is_not_positive():
    row = classify_force_conversion_move(
        force_conversion_decision(),
        [result(state(kills=100, deaths=300))],
        source_trajectory_sha256="a" * 64,
        seed=2055,
        round_no=10,
    )
    assert row is None


def snapshot(records):
    return {
        "schema": POLICY_SNAPSHOT_SCHEMA,
        "general_id": "apollyon",
        "scope": "tactical_competence_only",
        "record_count": len(records),
        "records": records,
        "source_trajectory_sha256": sorted({r["source_trajectory_sha256"] for r in records}),
        "utility_horizon_rounds": 3,
        "validity_only_examples_admitted": False,
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def policy_record(index, x, y):
    return {
        "schema": POLICY_RECORD_SCHEMA,
        "general_id": "apollyon",
        "source_trajectory_sha256": f"{index + 1:064x}",
        "source_round": index + 1,
        "seed": 2055,
        "mode": "FORCE_CONVERSION",
        "tool": "move_units",
        "unit_selector": "all_combat",
        "target_policy": "normalized_map_fraction",
        "target_x_millis": x,
        "target_y_millis": y,
        "utility_horizon_rounds": 3,
        "utility": {
            "contact_observed": True,
            "damage_inflicted": False,
            "kills_cost_delta": 0,
            "deaths_cost_delta": 0,
            "net_kill_cost_delta": 0,
            "utility_positive": True,
        },
        "authority_labels_included": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def make_r2_adapter():
    parent0 = make_generation_zero("apollyon")
    parent1 = make_challenger_generation(
        parent0,
        adapter_artifact_sha256="a" * 64,
        corpus_snapshot_sha256="b" * 64,
        training_receipt_sha256="c" * 64,
    )
    records = [
        policy_record(0, 480, 490),
        policy_record(1, 500, 500),
        policy_record(2, 520, 510),
    ]
    rejected = {
        "schema": "void.general-brain-incumbent-challenger-pair.v1",
        "general_id": "apollyon",
        "adapter_sha256": "a" * 64,
        "comparison": {
            "verdict": "WORSE",
            "protocol_clean": False,
            "behavioral_gates_pass": False,
        },
    }
    adapter, receipt, revised = train_policy_adapter_revision_two(
        parent1,
        snapshot(records),
        rejected_parent_pair=rejected,
        rejected_parent_pair_sha256="d" * 64,
    )
    return parent1, adapter, receipt, revised


def test_revision_two_rejects_flat_weight_and_preserves_authority():
    parent, adapter, receipt, revised = make_r2_adapter()
    assert adapter["schema"] == POLICY_ADAPTER_SCHEMA
    assert adapter["algorithm"] == ALGORITHM_ID
    assert adapter["candidate_revision"] == 2
    assert adapter["flat_tool_weight_retained"] is False
    assert adapter["policies"]["FORCE_CONVERSION"]["target_x_millis"] == 500
    assert adapter["policies"]["FORCE_CONVERSION"]["target_y_millis"] == 500
    assert revised["generation"] == 1
    assert revised["candidate_revision"] == 2
    assert revised["authority_envelope"] == parent["authority_envelope"] == NONTRAINABLE_AUTHORITY_ENVELOPE
    assert revised["competence_adapter"]["artifact_sha256"] == policy_adapter_sha256(adapter)
    assert receipt["automatic_promotion"] is False


def test_direct_policy_proposes_current_map_action_only_on_mode_entry():
    _, adapter, _, _ = make_r2_adapter()
    proposal = propose_direct_policy_action(
        adapter,
        state=state(width=101, height=81, combat=4),
        mode="FORCE_CONVERSION",
        previous_mode="BALANCED_SEARCH",
        offered_tool_names=["attack_move", "move_units", "train_unit_e1"],
    )
    assert proposal is not None
    assert proposal["tool"] == "move_units"
    assert proposal["arguments"] == {
        "unit_ids": "all_combat",
        "target_x": 50,
        "target_y": 40,
        "queued": False,
    }
    assert proposal["host_validation_required"] is True
    assert proposal["world_mutated_before_validation"] is False
    assert proposal["authority_envelope_trainable"] is False

    assert propose_direct_policy_action(
        adapter,
        state=state(),
        mode="FORCE_CONVERSION",
        previous_mode="FORCE_CONVERSION",
        offered_tool_names=["move_units"],
    ) is None


def test_direct_policy_backs_off_when_host_preconditions_are_not_grounded():
    _, adapter, _, _ = make_r2_adapter()
    assert propose_direct_policy_action(
        adapter,
        state=state(combat=0),
        mode="FORCE_CONVERSION",
        previous_mode="BALANCED_SEARCH",
        offered_tool_names=["move_units"],
    ) is None
    assert propose_direct_policy_action(
        adapter,
        state=state(),
        mode="FORCE_CONVERSION",
        previous_mode="BALANCED_SEARCH",
        offered_tool_names=["attack_move"],
    ) is None
    malformed = state()
    malformed["map"] = {"width": 0, "height": 0}
    assert propose_direct_policy_action(
        adapter,
        state=malformed,
        mode="FORCE_CONVERSION",
        previous_mode="BALANCED_SEARCH",
        offered_tool_names=["move_units"],
    ) is None
