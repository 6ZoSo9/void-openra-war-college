from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_child_wiring_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_v2_proto_child_wiring():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    assert out["wiring_main_head"] == (
        "b7815dee5408e860ef71784b8617f9a2b89f4e80"
    )
    assert out["wiring_git_blob"] == (
        "7d55059d17d8679c9e2883c0ee2e6d7951883a22"
    )
    assert out["wiring_source_sha256"] == (
        "3e0c8d7f15b997786b0436dc5a3165b8028b29adca84e41bdd668c32d49b6e3e"
    )
    assert out["wiring_test_git_blob"] == (
        "63e543b7ff9d37f6d6b1cd160360dd69bc981dd0"
    )
    assert out["wiring_test_sha256"] == (
        "c2ec27056ce25192504b1d7af42b3d1b562171d4f7b8e2a29e326131569ed182"
    )


def test_review_confirms_v2_legality_coherent_child():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    assert out["v2_repaired_decision_hook_bound"] is True
    assert out["production_functions_filtered_to_offered_surface_by_v1"] is True
    assert out["legal_buildings_reconstructed_from_remaining_production"] is True
    assert out["legal_units_reconstructed_from_remaining_production"] is True
    assert out["translator_legal_building_mapping_coherent"] is True
    assert out["translator_legal_unit_mapping_coherent"] is True
    assert out["existing_child_execution_authorization_gate_preserved"] is True
    assert out["existing_policy_activation_authorization_gate_preserved"] is True
    assert out["existing_ipc_decider_reused"] is True
    assert out["existing_legacy_runner_reused"] is True


def test_review_seals_consumed_precursor():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    assert out["consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["failed_run_reusable_as_authority"] is False
    assert out["prior_authorization_reusable"] is False


def test_review_grants_no_retry_or_runtime_authority():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    for field in (
        "attempt_retry_authorized",
        "parent_supervisor_v2_wiring_implemented",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_v2_parent_wiring():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_PARENT_SUPERVISOR_WIRING_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentV2ProtoChildWiringReviewHold,
        match="REPAIR_V2_PARENT_SUPERVISOR_WIRING_REQUIRED",
    ):
        review.wire_parent_or_execute()
