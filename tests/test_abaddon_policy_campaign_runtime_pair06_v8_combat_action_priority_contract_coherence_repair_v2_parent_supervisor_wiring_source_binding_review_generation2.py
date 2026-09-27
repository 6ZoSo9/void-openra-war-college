from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_parent_supervisor_wiring_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_process_boundary_sources():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract()
    )
    assert out["merged_main_head"] == (
        "3865459c9829a18593b6e3eea431abd0877941a8"
    )
    assert out["child_entry_git_blob"] == (
        "0078db895accd35a0f7f64e5cb16bab31998bd71"
    )
    assert out["child_entry_source_sha256"] == (
        "14d5b4cbe52aa493d07ac8f9d8e3b7d0a00cbead9f4147ecdefa55e868767d35"
    )
    assert out["child_entry_test_git_blob"] == (
        "d5c0f68c1a883124b640f2f0c15a361cfafcdb22"
    )
    assert out["child_entry_test_sha256"] == (
        "6fb942a43d6271b16c856dfaaafc49c002ba6f2306c02283bbf302da9ab5959b"
    )
    assert out["parent_wiring_git_blob"] == (
        "2541ea0de84ede2bb3a0effcca19cca61204d3a7"
    )
    assert out["parent_wiring_source_sha256"] == (
        "9aea4ce2abac908cee658fda4f2f2e2d8cf22bf05d73299d741b2dbf8d52ce9e"
    )
    assert out["parent_wiring_test_git_blob"] == (
        "6d2dc05122bc59c3a079d68ec715d4db13319ddf"
    )
    assert out["parent_wiring_test_sha256"] == (
        "7af07fb2031b9d8edf90b6e62efc6042aafb9d2e3510e40e99c376dfa6764049"
    )


def test_review_confirms_v2_process_boundary_and_legality_coherence():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract()
    )
    assert out["pair06_v8_combat_priority_coherent_v2_parent_wiring_reviewed"] is True
    assert out["canonical_invocation_lane"] == (
        "receipt_bound_no_offload_fresh_preclaim_gpu"
    )
    assert out["production_functions_filtered_to_offered_surface_by_v1"] is True
    assert out["legal_buildings_reconstructed_from_remaining_production"] is True
    assert out["legal_units_reconstructed_from_remaining_production"] is True
    assert out["translator_legal_building_mapping_coherent"] is True
    assert out["translator_legal_unit_mapping_coherent"] is True


def test_review_seals_latest_consumed_attempt_and_requires_fresh_authority():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract()
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
    assert out["fresh_evidence_namespace_required"] is True
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True


def test_review_preserves_one_shot_preclaim_gpu_boundary():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract()
    )
    assert out["maximum_attempts_per_fresh_authorization"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_must_precede_attempt_marker"] is True
    assert out["durable_create_only_attempt_marker_required"] is True
    assert out["attempt_marker_must_precede_model_load_and_child_spawn"] is True


def test_review_grants_no_claim_retry_or_runtime_authority():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract()
    )
    for field in (
        "attempt_retry_authorized",
        "attempt_marker_creation_authorized",
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


def test_review_advances_only_to_fresh_v2_invocation_source():
    out = (
        review
        .pair06_v8_combat_priority_coherent_v2_parent_wiring_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED",
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentV2ParentWiringReviewHold,
        match="REPAIR_V2_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED",
    ):
        review.implement_invocation_or_execute()
