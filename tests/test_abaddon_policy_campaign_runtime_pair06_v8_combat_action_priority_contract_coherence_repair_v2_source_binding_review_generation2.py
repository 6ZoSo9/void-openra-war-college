from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_v2_source_and_tests():
    out = (
        review
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract()
    )
    assert out["repair_v2_main_head"] == (
        "d4d3e57d5025e0a37729440377d1d36be10fce71"
    )
    assert out["repair_v2_git_blob"] == (
        "bf9b5f0e5f8d1c61f1bc8f4ba42aa45b2d3278ae"
    )
    assert out["repair_v2_source_sha256"] == (
        "087245a4fea130ff25cec1c052370fa26fa4e31450b91b5277d9e5b63ad2cdab"
    )
    assert out["repair_v2_test_git_blob"] == (
        "8ec279e12294020876ebb38a9ef6f8f3481046a1"
    )
    assert out["repair_v2_test_sha256"] == (
        "c5c69956dea345dc01f6ef78bdd67df83487853fa1635b423ffbba4a7ad720a4"
    )


def test_review_confirms_both_translator_mapping_invariants():
    out = (
        review
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract()
    )
    assert out["production_functions_filtered_to_offered_surface_by_v1"] is True
    assert out[
        "legal_buildings_reconstructed_from_remaining_production"
    ] is True
    assert out["legal_units_reconstructed_from_remaining_production"] is True
    assert out["translator_legal_building_mapping_invariant_required"] is True
    assert out["translator_legal_unit_mapping_invariant_required"] is True
    assert out["normal_mode_identity_required"] is True


def test_review_seals_consumed_v2_precursor_attempt():
    out = (
        review
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract()
    )
    assert out["consumed_v2_precursor_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_v2_precursor_attempt_reusable"] is False
    assert out["consumed_v2_precursor_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["consumed_v2_precursor_run_reusable_as_authority"] is False
    assert out["consumed_v2_precursor_result_present"] is False
    assert out["consumed_v2_precursor_closeout_present"] is False
    assert out["prior_authorization_reusable"] is False


def test_review_grants_no_retry_or_runtime_authority():
    out = (
        review
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract()
    )
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


def test_review_advances_only_to_v2_proto_child_wiring():
    out = (
        review
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_PROTO_CHILD_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_PROTO_CHILD_WIRING_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityContractCoherenceV2ReviewHold,
        match="REPAIR_V2_PROTO_CHILD_WIRING_REQUIRED",
    ):
        review.wire_or_execute()
