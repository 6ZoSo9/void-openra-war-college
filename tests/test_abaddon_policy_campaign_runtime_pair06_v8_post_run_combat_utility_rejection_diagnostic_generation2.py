from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_post_run_combat_utility_rejection_diagnostic_generation2
    as diagnostic,
)


def test_diagnostic_binds_exact_run_terminal_and_result():
    out = diagnostic.pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    assert out["result_review_main_head"] == (
        "4d666f0157c09a002b3d9897d09f550dc55e3656"
    )
    assert out["result_review_git_blob"] == (
        "2ca3aa48919193ed57703a6446372cb4ae6414c7"
    )
    assert out["run_terminal_sha256"] == (
        "25378d215a7bd5cf8e3192030d8bb3b89b429dacda7bb61c2ff4c58090a2f5a8"
    )
    assert out["run_terminal_bytes"] == 23772
    assert out["attempt_marker_sha256"] == (
        "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
    )


def test_rejection_diagnostic_finds_no_retry_pressure():
    out = diagnostic.pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    assert out["controller_rounds"] == 36
    assert out["apollyon_tool_contract_accepted_rounds"] == 36
    assert out["apollyon_total_tool_attempts"] == 36
    assert out["apollyon_max_attempts_for_accepted_action"] == 1
    assert out["apollyon_rounds_requiring_tool_retry"] == 0
    assert out["tool_rejection_or_retry_failure_observed"] is False
    assert out["trace_supports_protocol_rejection_failure"] is False


def test_action_mix_and_combat_collapse_are_exact():
    out = diagnostic.pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    assert out["apollyon_structure_build_actions"] == 11
    assert out["apollyon_advance_actions"] == 25
    assert out["apollyon_explicit_attack_target_actions"] == 0
    assert out["apollyon_explicit_move_units_actions"] == 0
    assert out["apollyon_explicit_unit_build_actions"] == 0
    assert out["apollyon_combat_count_at_controller_start"] == 4
    assert out["apollyon_combat_count_zero_round"] == 7
    assert out["combat_counts_at_round_7"] == (0, 6)
    assert out["apollyon_zero_combat_rounds_7_through_36"] == 30
    assert out["combat_counts_at_round_36"] == (0, 6)


def test_diagnostic_classifies_observation_without_overclaiming_cause():
    out = diagnostic.pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    assert out["diagnostic_classification"] == (
        "combat_utility_action_mix_not_tool_rejection"
    )
    assert out["trace_supports_combat_utility_deficit"] is True
    for field in (
        "causal_root_cause_proven",
        "tool_availability_root_cause_proven",
        "policy_ranking_root_cause_proven",
        "reward_shaping_root_cause_proven",
        "state_interpretation_root_cause_proven",
    ):
        assert out[field] is False


def test_diagnostic_grants_no_change_or_execution_authority():
    out = diagnostic.pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    for field in (
        "policy_change_authorized",
        "new_runtime_execution_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_diagnostic_advances_only_to_source_hypothesis():
    out = diagnostic.pair06_v8_post_run_combat_utility_rejection_diagnostic_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_HYPOTHESIS_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_HYPOTHESIS_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        diagnostic.Pair06V8PostRunCombatUtilityRejectionDiagnosticHold,
        match="COMBAT_ACTION_PRIORITY_HYPOTHESIS_REQUIRED",
    ):
        diagnostic.change_policy_or_execute()
