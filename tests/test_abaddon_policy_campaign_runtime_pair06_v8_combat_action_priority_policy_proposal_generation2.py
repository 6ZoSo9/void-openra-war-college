from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_proposal_generation2
    as proposal,
)


def test_proposal_pins_exact_availability_acceptance():
    out = proposal.pair06_v8_combat_action_priority_policy_proposal_contract()
    assert out["availability_acceptance_main_head"] == (
        "71df31c3369f833bdcc4392cfd6749df3eb35896"
    )
    assert out["availability_acceptance_git_blob"] == (
        "f4f535d039a7dc5c72c87713e8f78dd360b42fa0"
    )
    assert out["availability_acceptance_source_sha256"] == (
        "55a82e91b327590a3b2300abdcf698c251ea9b3980dc036d828a27a77636b7ab"
    )
    assert out["evidence_available_but_not_chosen"] is True


def test_recovery_mode_exposes_only_current_recovery_tools():
    out = proposal.proposed_priority_envelope(
        combat_count=0,
        visible_enemy_count=0,
        offered_tool_names=(
            "advance",
            "build_structure_tent",
            "train_unit_e1",
            "train_unit_e3",
        ),
    )
    assert out["mode"] == "RECOVERY"
    assert out["proposed_offered_tool_names"] == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert out["advance_suppressed"] is True
    assert out["structure_tools_suppressed"] == (
        "build_structure_tent",
    )


def test_visible_contact_mode_preserves_combat_reinforcement_and_controls():
    out = proposal.proposed_priority_envelope(
        combat_count=3,
        visible_enemy_count=2,
        offered_tool_names=(
            "advance",
            "build_structure_gun",
            "train_unit_e1",
            "move_units",
            "attack_move",
            "attack_target",
            "set_stance",
            "stop_units",
            "guard_target",
        ),
    )
    assert out["mode"] == "VISIBLE_CONTACT"
    assert out["proposed_offered_tool_names"] == (
        "train_unit_e1",
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    )
    assert out["advance_suppressed"] is True
    assert out["structure_tools_suppressed"] == (
        "build_structure_gun",
    )


def test_normal_mode_is_identity_transform():
    offered = (
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "move_units",
        "attack_move",
    )
    out = proposal.proposed_priority_envelope(
        combat_count=2,
        visible_enemy_count=0,
        offered_tool_names=offered,
    )
    assert out["mode"] == "NORMAL"
    assert out["proposed_offered_tool_names"] == offered
    assert out["advance_suppressed"] is False
    assert out["structure_tools_suppressed"] == ()


def test_proposal_never_invents_tools():
    offered = ("advance", "train_unit_e1")
    out = proposal.proposed_priority_envelope(
        combat_count=0,
        visible_enemy_count=5,
        offered_tool_names=offered,
    )
    assert set(out["proposed_offered_tool_names"]) <= set(offered)


def test_proposal_preserves_validation_and_grants_no_execution_authority():
    out = proposal.pair06_v8_combat_action_priority_policy_proposal_contract()
    assert out["host_validation_must_remain_unchanged"] is True
    assert out["six_attempt_fail_closed_retry_must_remain_unchanged"] is True
    assert (
        out["frozen_world_state_across_rejected_attempts_must_remain_unchanged"]
        is True
    )
    assert out["typed_production_legality_must_remain_unchanged"] is True
    assert out["normal_mode_surface_must_remain_unchanged"] is True
    assert out["implementation_present"] is False
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


def test_proposal_advances_only_to_source_binding_review():
    out = proposal.pair06_v8_combat_action_priority_policy_proposal_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        proposal.Pair06V8CombatActionPriorityPolicyProposalHold,
        match="POLICY_PROPOSAL_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        proposal.implement_or_execute()
