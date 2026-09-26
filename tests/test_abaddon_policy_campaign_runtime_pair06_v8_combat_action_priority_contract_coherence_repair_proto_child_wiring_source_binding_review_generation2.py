from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_wiring_source_and_tests():
    out = review.pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    assert out["wiring_main_head"] == (
        "721bb382cc07abbd26111bfdc605504d5961886c"
    )
    assert out["wiring_git_blob"] == (
        "75d4442b2b86a54343dc546b59f58f90e3e9afc4"
    )
    assert out["wiring_source_sha256"] == (
        "e904bd345b07ec25c061da710a625e9aafc51424dba5708408b46c07afed3306"
    )
    assert out["wiring_test_git_blob"] == (
        "e41123b2f46091359a3099766d152ce4418666b5"
    )
    assert out["wiring_test_sha256"] == (
        "d2559b04b0b854dd24477bb96a1dbc2ef4743b22d20d70d66c9a9d38a136e86f"
    )


def test_review_confirms_repaired_child_boundary():
    out = review.pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    assert out["repaired_decision_hook_bound"] is True
    assert out["production_functions_filtered_to_offered_surface"] is True
    assert out["existing_child_execution_authorization_gate_preserved"] is True
    assert out["existing_policy_activation_authorization_gate_preserved"] is True


def test_review_seals_consumed_attempt():
    out = review.pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    assert out["consumed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert out["failed_run_reusable_as_authority"] is False


def test_review_grants_no_retry_or_runtime_authority():
    out = review.pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    for field in (
        "attempt_retry_authorized",
        "parent_supervisor_repair_wiring_implemented",
        "operator_invocation_repair_implemented",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_parent_supervisor_wiring():
    out = review.pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_PARENT_SUPERVISOR_WIRING_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentProtoChildWiringReviewHold,
        match="REPAIR_PARENT_SUPERVISOR_WIRING_REQUIRED",
    ):
        review.wire_parent_or_execute()
