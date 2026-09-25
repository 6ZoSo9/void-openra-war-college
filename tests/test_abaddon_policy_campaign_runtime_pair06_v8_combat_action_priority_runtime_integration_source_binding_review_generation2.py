from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_integration_source_and_tests():
    out = (
        review
        .pair06_v8_combat_action_priority_runtime_integration_review_contract()
    )
    assert out["integration_main_head"] == (
        "c70de88f564062fee6d5eb1d6cd575afffa2957b"
    )
    assert out["integration_git_blob"] == (
        "5f33527e1b6b7c1bf8912436d70ab406748c66bd"
    )
    assert out["integration_source_sha256"] == (
        "558be4263016a6e2e74df49ae0d0dbed27ef508389a83a428b09bf5d3387b36d"
    )
    assert out["integration_test_git_blob"] == (
        "5302aad6f50bcc2237e0b452f0d0a35ec189210d"
    )
    assert out["integration_test_sha256"] == (
        "d7b3ded580bb598ecba5d708db8781b7b87d1a90bf82649e6fe0a5e332e598d7"
    )


def test_review_confirms_decision_hook_only_integration():
    out = (
        review
        .pair06_v8_combat_action_priority_runtime_integration_review_contract()
    )
    assert out[
        "pair06_v8_combat_action_priority_runtime_integration_reviewed"
    ] is True
    assert out["decision_hook_runtime_integration_implemented"] is True
    assert out["proto_game_child_wiring_implemented"] is False
    assert out["parent_supervisor_wiring_implemented"] is False
    assert out["operator_invocation_implemented"] is False


def test_review_grants_no_runtime_or_training_authority():
    out = (
        review
        .pair06_v8_combat_action_priority_runtime_integration_review_contract()
    )
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


def test_review_advances_only_to_proto_child_wiring():
    out = (
        review
        .pair06_v8_combat_action_priority_runtime_integration_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatActionPriorityRuntimeIntegrationReviewHold,
        match="COMBAT_ACTION_PRIORITY_PROTO_CHILD_WIRING_REQUIRED",
    ):
        review.wire_or_execute()
