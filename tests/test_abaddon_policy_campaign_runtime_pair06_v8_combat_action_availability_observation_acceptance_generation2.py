from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_availability_observation_acceptance_generation2
    as acceptance,
)


def test_acceptance_pins_exact_audit_and_observation_identity():
    out = (
        acceptance
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
    assert out["audit_main_head"] == (
        "e6f95851026dfdbca4bfa60572f086bdc9d65ba1"
    )
    assert out["audit_git_blob"] == (
        "4f5a9797e8aea5c4aa960d63d524eac2237603d4"
    )
    assert out["audit_source_sha256"] == (
        "a4fa1aff1666bc7d566cad8f31ac24817aee36e7cc2deb8f43ad8ee5b3f03a34"
    )
    assert out["trajectory_sha256"] == (
        "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
    )
    assert out["trajectory_bytes"] == 386881
    assert out["observation_terminal_sha256"] == (
        "79841b3174bab1b8b4a5eccc764c470237736c8c759a04bc362d086b749b3f47"
    )
    assert out["observation_terminal_bytes"] == 25319


def test_recovery_was_available_for_every_zero_combat_round():
    out = (
        acceptance
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
    expected = tuple(range(8, 37))
    assert out["combat_recovery_relevant_rounds"] == expected
    assert out["combat_recovery_available_rounds"] == expected
    assert out["combat_recovery_unavailable_rounds"] == ()
    assert out["all_recovery_relevant_rounds_had_recovery_tool"] is True


def test_engagement_was_available_for_every_contact_round():
    out = (
        acceptance
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
    assert out["engagement_relevant_rounds"] == (3, 4, 5, 6, 7)
    assert out["engagement_available_rounds"] == (3, 4, 5, 6, 7)
    assert out["engagement_unavailable_rounds"] == ()
    assert out["all_engagement_relevant_rounds_had_engagement_tool"] is True


def test_available_but_not_chosen_is_proven_without_overclaiming_upstream_cause():
    out = (
        acceptance
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
    assert out["ranking_cause_supported_by_availability"] is True
    assert out["action_selection_layer_available_but_not_chosen_proven"] is True
    for field in (
        "upstream_model_preference_cause_proven",
        "prompt_framing_cause_proven",
        "learned_policy_cause_proven",
        "reward_shaping_cause_proven",
    ):
        assert out[field] is False


def test_acceptance_grants_no_execution_or_mutation_authority():
    out = (
        acceptance
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
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


def test_acceptance_advances_only_to_source_policy_proposal():
    out = (
        acceptance
        .pair06_v8_combat_action_availability_observation_acceptance_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8CombatActionAvailabilityObservationAcceptanceHold,
        match="COMBAT_ACTION_PRIORITY_POLICY_PROPOSAL_REQUIRED",
    ):
        acceptance.change_policy_or_execute()
