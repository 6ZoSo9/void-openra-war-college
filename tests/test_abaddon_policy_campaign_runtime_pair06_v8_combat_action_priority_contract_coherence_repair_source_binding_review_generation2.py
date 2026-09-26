from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_repair_source_and_tests():
    out = review.pair06_v8_combat_action_priority_contract_coherence_repair_review_contract()
    assert out["repair_main_head"] == (
        "72104294537bc8450a1505b643914dc503b83845"
    )
    assert out["repair_git_blob"] == (
        "fee7f07791d01594bf7f31b8cd8e24c8eb6fbed3"
    )
    assert out["repair_source_sha256"] == (
        "cd951c4cbfe6014e1dc2412b1f52b5beda552cf89e77846a5af176b2278b81f6"
    )
    assert out["repair_test_git_blob"] == (
        "d107a944897a461abb479ba47bed88155d3bedae"
    )
    assert out["repair_test_sha256"] == (
        "1d910f6cfd88c72ca362251f47bbb848bb7a159773d1a42874b2e84c5a46f8ac"
    )


def test_review_confirms_contract_coherence_invariants():
    out = review.pair06_v8_combat_action_priority_contract_coherence_repair_review_contract()
    assert out["production_functions_filtered_to_offered_surface"] is True
    assert out["legal_units_preserved"] is True
    assert out["legal_buildings_preserved"] is True
    assert out["normal_mode_production_mapping_identity_required"] is True


def test_review_grants_no_retry_or_runtime_authority():
    out = review.pair06_v8_combat_action_priority_contract_coherence_repair_review_contract()
    for field in (
        "attempt_retry_authorized",
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


def test_review_advances_only_to_proto_child_repair_wiring():
    out = review.pair06_v8_combat_action_priority_contract_coherence_repair_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_PROTO_CHILD_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_PROTO_CHILD_WIRING_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityContractCoherenceReviewHold,
        match="CONTRACT_COHERENCE_REPAIR_PROTO_CHILD_WIRING_REQUIRED",
    ):
        review.wire_or_execute()
