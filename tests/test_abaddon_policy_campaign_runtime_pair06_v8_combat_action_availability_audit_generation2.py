from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_availability_audit_generation2
    as audit,
)


def _row(
    round_no: int,
    *,
    combat_count: int,
    visible_enemy_count: int,
    offered: list[str],
    legal_units: list[str],
    accepted: str = "advance",
):
    units = [
        {"id": index + 1, "type": "e1", "can_attack": True}
        for index in range(combat_count)
    ]
    enemies = [
        {"id": 100 + index, "type": "e1"}
        for index in range(visible_enemy_count)
    ]
    return {
        "event": "joint_decision",
        "run_id": audit.RUN_ID,
        "round": round_no,
        "apollyon_state": {
            "units_summary": units,
            "enemy_summary": enemies,
            "enemy_buildings_summary": [],
        },
        "apollyon": {
            "tool": accepted,
            "attempts": [{
                "attempt": 1,
                "tool": accepted,
                "accepted": True,
                "function_was_offered": True,
            }],
            "tool_contract": {
                "offered_tool_names": offered,
                "legal_units": legal_units,
                "legal_buildings": [],
            },
        },
    }


def test_contract_binds_exact_sources_and_trajectory():
    out = audit.pair06_v8_combat_action_availability_audit_contract()
    assert out["hypothesis_main_head"] == (
        "6eb6c9912be8877ed8b2c22c477101b9cccb3bac"
    )
    assert out["hypothesis_git_blob"] == (
        "2d60d5c5e963746c7ce04d993c18e36472cff9ab"
    )
    assert out["warm_start_runner_fixture_git_blob"] == (
        "132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51"
    )
    assert out["joint_host_fixture_git_blob"] == (
        "6e751b855da1d9425c4fd2bd5a997ae1c742ae11"
    )
    assert out["trajectory_sha256"] == (
        "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
    )


def test_row_audit_distinguishes_recovery_and_engagement_availability():
    rows = [
        _row(
            1,
            combat_count=2,
            visible_enemy_count=1,
            offered=["advance", "attack_target", "move_units"],
            legal_units=[],
            accepted="move_units",
        ),
        _row(
            2,
            combat_count=0,
            visible_enemy_count=1,
            offered=["advance", "train_unit_e1"],
            legal_units=["e1"],
        ),
        _row(
            3,
            combat_count=0,
            visible_enemy_count=0,
            offered=["advance"],
            legal_units=[],
        ),
    ]
    out = audit._audit_rows(rows)
    assert out["engagement_relevant_rounds"] == [1]
    assert out["engagement_available_rounds"] == [1]
    assert out["combat_recovery_relevant_rounds"] == [2, 3]
    assert out["combat_recovery_available_rounds"] == [2]
    assert out["combat_recovery_unavailable_rounds"] == [3]
    assert out["ranking_cause_supported_by_availability"] is False


def test_recovery_requires_typed_train_unit_function():
    rows = [
        _row(
            1,
            combat_count=0,
            visible_enemy_count=0,
            offered=["advance", "build_structure_tent"],
            legal_units=[],
        ),
    ]
    out = audit._audit_rows(rows)
    assert out["combat_recovery_relevant_rounds"] == [1]
    assert out["combat_recovery_available_rounds"] == []
    assert out["combat_recovery_unavailable_rounds"] == [1]


def test_engagement_relevance_requires_units_and_visibility():
    rows = [
        _row(
            1,
            combat_count=2,
            visible_enemy_count=0,
            offered=["advance", "move_units", "attack_move"],
            legal_units=[],
        ),
        _row(
            2,
            combat_count=0,
            visible_enemy_count=2,
            offered=["advance"],
            legal_units=[],
        ),
    ]
    out = audit._audit_rows(rows)
    assert out["engagement_relevant_rounds"] == []


def test_contract_grants_no_runtime_or_policy_authority():
    out = audit.pair06_v8_combat_action_availability_audit_contract()
    assert out["host_file_read_implemented"] is False
    assert out["host_file_read_performed"] is False
    assert out["trajectory_audited_by_contract_inspection"] is False
    assert out["ranking_cause_supported_by_current_contract_inspection"] is False
    for field in (
        "policy_change_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_contract_advances_only_to_readonly_precision_observation():
    out = audit.pair06_v8_combat_action_availability_audit_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_PRECISION_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_PRECISION_OBSERVATION_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        audit.Pair06V8CombatActionAvailabilityAuditHold,
        match="COMBAT_ACTION_AVAILABILITY_PRECISION_OBSERVATION_REQUIRED",
    ):
        audit.observe_or_change_policy()
