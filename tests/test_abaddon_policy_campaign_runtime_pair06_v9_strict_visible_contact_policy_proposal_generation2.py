from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_proposal_generation2
    as proposal,
)


def test_contract_is_hypothesis_only_and_preserves_spent_v8_lineage():
    out = proposal.pair06_v9_strict_visible_contact_policy_proposal_contract()

    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["baseline_policy_id"] == (
        "pair06-v8-combat-action-priority-envelope-v1"
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["evidence_basis"] == {
        "v8_policy_retains_reinforcement_tools_in_visible_contact": True,
        "v8_v2_coherent_run_completed": True,
        "v8_v2_coherent_rounds_completed": 36,
        "v8_v2_coherent_outcome": "DRAW_OR_UNFINISHED",
        "action_level_causal_attribution_available": False,
    }
    assert out["causal_claim_made"] is False
    assert out["new_execution_request_opened"] is False


def test_recovery_mode_is_unchanged_from_v8_recovery_shape():
    offered = (
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
        "attack_move",
    )
    out = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=0,
        visible_enemy_count=0,
        offered_tool_names=offered,
    )

    assert out["mode"] == "RECOVERY"
    assert out["proposed_offered_tool_names"] == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert out["reinforcement_tools_suppressed"] == ()


def test_strict_visible_contact_excludes_reinforcement_and_growth_choices():
    offered = (
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "train_unit_e3",
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    )
    out = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=4,
        visible_enemy_count=2,
        offered_tool_names=offered,
    )

    assert out["mode"] == "STRICT_VISIBLE_CONTACT"
    assert out["proposed_offered_tool_names"] == (
        "move_units",
        "attack_move",
        "attack_target",
        "set_stance",
        "stop_units",
        "guard_target",
    )
    assert out["reinforcement_tools_suppressed"] == (
        "train_unit_e1",
        "train_unit_e3",
    )
    assert out["advance_suppressed"] is True
    assert out["structure_tools_suppressed"] == ("build_structure_powr",)


def test_strict_visible_contact_preserves_relative_order_of_retained_tools():
    offered = (
        "guard_target",
        "train_unit_e1",
        "attack_target",
        "stop_units",
        "move_units",
        "set_stance",
        "attack_move",
    )
    out = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=1,
        visible_enemy_count=1,
        offered_tool_names=offered,
    )
    assert out["proposed_offered_tool_names"] == (
        "guard_target",
        "attack_target",
        "stop_units",
        "move_units",
        "set_stance",
        "attack_move",
    )


def test_normal_mode_is_exact_identity_surface():
    offered = (
        "advance",
        "build_structure_powr",
        "train_unit_e1",
        "move_units",
        "attack_move",
    )
    out = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=3,
        visible_enemy_count=0,
        offered_tool_names=offered,
    )

    assert out["mode"] == "NORMAL"
    assert out["proposed_offered_tool_names"] == offered
    assert out["reinforcement_tools_suppressed"] == ()
    assert out["advance_suppressed"] is False
    assert out["structure_tools_suppressed"] == ()


def test_visible_enemy_without_current_engagement_tool_does_not_force_empty_surface():
    offered = (
        "advance",
        "train_unit_e1",
        "set_stance",
    )
    out = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=2,
        visible_enemy_count=1,
        offered_tool_names=offered,
    )

    assert out["mode"] == "NORMAL"
    assert out["proposed_offered_tool_names"] == offered


def test_proposal_never_invents_tools_and_rejects_duplicates():
    offered = (
        "attack_target",
        "train_unit_e1",
        "set_stance",
    )
    out = proposal.proposed_v9_strict_visible_contact_envelope(
        combat_count=2,
        visible_enemy_count=1,
        offered_tool_names=offered,
    )
    assert set(out["proposed_offered_tool_names"]) <= set(offered)

    with pytest.raises(
        proposal.Pair06V9StrictVisibleContactProposalHold,
        match="duplicate offered tool name",
    ):
        proposal.proposed_v9_strict_visible_contact_envelope(
            combat_count=2,
            visible_enemy_count=1,
            offered_tool_names=("attack_target", "attack_target"),
        )


@pytest.mark.parametrize(
    "field",
    (
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ),
)
def test_proposal_grants_no_effect_authority(field):
    out = proposal.pair06_v9_strict_visible_contact_policy_proposal_contract()
    assert out[field] is False


def test_proposal_advances_only_to_source_review():
    out = proposal.pair06_v9_strict_visible_contact_policy_proposal_contract()

    assert out["implementation_present"] is False
    assert out["runtime_integration_present"] is False
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_PROPOSAL_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_PROPOSAL_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_implement_or_execute_holds():
    with pytest.raises(
        proposal.Pair06V9StrictVisibleContactProposalHold,
        match="SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        proposal.implement_or_execute()
