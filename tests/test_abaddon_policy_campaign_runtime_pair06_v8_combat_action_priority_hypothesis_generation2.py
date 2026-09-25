from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_hypothesis_generation2
    as hypothesis,
)


def test_hypothesis_pins_exact_diagnostic_source():
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
    assert out["diagnostic_main_head"] == (
        "f7d76da01e8bdd40f43aad91104252ecda4e97a7"
    )
    assert out["diagnostic_git_blob"] == (
        "1abb7add92d82a118f4357ce26e8af9bbfa20b1d"
    )
    assert out["diagnostic_source_sha256"] == (
        "5ea3d91f538ca7826d8a8c1765211d5d8488b20507326f53028fbce394b77603"
    )


def test_hypothesis_preserves_observed_trace_facts():
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
    assert out["observed_tool_rejection_or_retry_failure"] is False
    assert out["observed_controller_rounds"] == 36
    assert out["observed_apollyon_structure_build_actions"] == 11
    assert out["observed_apollyon_advance_actions"] == 25
    assert out["observed_apollyon_explicit_attack_target_actions"] == 0
    assert out["observed_apollyon_explicit_move_units_actions"] == 0
    assert out["observed_apollyon_explicit_unit_build_actions"] == 0
    assert out["observed_apollyon_combat_count_start"] == 4
    assert out["observed_apollyon_combat_count_zero_round"] == 7
    assert out["observed_apollyon_zero_combat_round_count"] == 30


def test_hypothesis_is_conditional_on_action_availability():
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
    assert out["hypothesis_kind"] == "conditional_action_priority_ranking"
    assert out["availability_must_be_proven_before_ranking_cause"] is True
    assert out["tool_availability_currently_proven"] is False
    assert out["policy_ranking_cause_currently_proven"] is False
    assert out["availability_audit_required_before_policy_proposal"] is True
    assert out["falsification_if_relevant_combat_actions_unavailable"] is True


def test_hypothesis_defines_recovery_and_engagement_priority_without_applying_it():
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
    assert out["combat_recovery_priority_hypothesis"] == (
        "prefer_legal_combat_capacity_recovery_over_nonessential_structure_or_bare_advance"
    )
    assert out["engagement_priority_hypothesis"] == (
        "prefer_legal_attack_or_contact_movement_over_nonessential_structure_or_bare_advance"
    )
    assert out["nonessential_structure_suppression_hypothesis"] == (
        "during_active_contact_or_combat_depletion_do_not_prioritize_nonessential_structure_growth"
    )


def test_hypothesis_grants_no_execution_or_policy_authority():
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
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


def test_hypothesis_advances_only_to_availability_audit():
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_AUDIT_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_AUDIT_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        hypothesis.Pair06V8CombatActionPriorityHypothesisHold,
        match="COMBAT_ACTION_AVAILABILITY_AUDIT_REQUIRED",
    ):
        hypothesis.audit_or_change_policy()
