from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_wiring_source_and_tests():
    out = review.pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    assert out["wiring_main_head"] == (
        "d213f9805de2a0990c831b59ec8a5b73c8d1539a"
    )
    assert out["wiring_git_blob"] == (
        "7dd120dce2bc39a780ce40b9d167d39ea5cf9bfc"
    )
    assert out["wiring_source_sha256"] == (
        "3483056aab144c412be96ed8e90f27f07c8c0d0988419be64a844e10d870b2b1"
    )
    assert out["wiring_test_git_blob"] == (
        "6c58ab0d3692f6a8fc9feb6755e0a140228b9819"
    )
    assert out["wiring_test_sha256"] == (
        "a762c71c24ef38a9f1798163fdffcc68b9c7c5c3dcf160dbe92b9cfe354905e8"
    )


def test_review_confirms_scoped_child_wiring_only():
    out = review.pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    assert out[
        "pair06_v8_combat_action_priority_proto_child_wiring_reviewed"
    ] is True
    assert out["existing_proto_child_source_modified"] is False
    assert out["hook_factory_substitution_scoped_to_single_call"] is True
    assert out["hook_factory_restored_in_finally"] is True
    assert out["additional_policy_activation_gate_required"] is True
    assert out["parent_supervisor_wiring_implemented"] is False
    assert out["operator_entrypoint_wiring_implemented"] is False


def test_review_grants_no_runtime_or_training_authority():
    out = review.pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    for field in (
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_parent_supervisor_wiring():
    out = review.pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatActionPriorityProtoChildWiringReviewHold,
        match="COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED",
    ):
        review.wire_parent_or_execute()
