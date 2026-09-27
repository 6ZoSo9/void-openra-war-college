from __future__ import annotations

from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as base_invocation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as spent_v1,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as invocation,
)


def test_contract_binds_exact_v2_parent_review():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )

    assert out["parent_wiring_review_main_head"] == (
        "71afc3c5ca6887d376088bba8d687fd116b4b96b"
    )
    assert out["parent_wiring_review_git_blob"] == (
        "bc22e83cb56db2479f77147c84963c8420050899"
    )
    assert out["parent_wiring_review_source_sha256"] == (
        "51acdb78f7acca71b0bbdf14adbb558bae422eece6ea175433ab30569d62831d"
    )

    parent = out["dependencies"]["combat_priority_parent_wiring_review"]
    assert parent[
        "pair06_v8_combat_priority_coherent_v2_parent_wiring_reviewed"
    ] is True
    assert parent[
        "production_functions_filtered_to_offered_surface_by_v1"
    ] is True
    assert parent[
        "legal_buildings_reconstructed_from_remaining_production"
    ] is True
    assert parent["legal_units_reconstructed_from_remaining_production"] is True
    assert parent["translator_legal_building_mapping_coherent"] is True
    assert parent["translator_legal_unit_mapping_coherent"] is True


def test_v2_namespace_is_fresh_and_distinct():
    assert invocation.MARKER_NAME != base_invocation.MARKER_NAME
    assert invocation.RESULT_NAME != base_invocation.RESULT_NAME
    assert invocation.CLOSEOUT_NAME != base_invocation.CLOSEOUT_NAME
    assert invocation.RUNS_ROOT != Path(base_invocation.RUNS_ROOT)

    assert invocation.MARKER_NAME != spent_v1.MARKER_NAME
    assert invocation.RESULT_NAME != spent_v1.RESULT_NAME
    assert invocation.CLOSEOUT_NAME != spent_v1.CLOSEOUT_NAME
    assert invocation.RUNS_ROOT != Path(spent_v1.RUNS_ROOT)

    assert "coherent-v2" in invocation.MARKER_NAME
    assert "coherent-v2" in invocation.RESULT_NAME
    assert "coherent-v2" in invocation.CLOSEOUT_NAME
    assert invocation.RUNS_ROOT.name == "runs-combat-priority-coherent-v2-v1"


def test_contract_seals_consumed_v1_coherent_attempt():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )

    assert out["consumed_coherent_v1_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_coherent_v1_attempt_reusable"] is False
    assert out["failed_coherent_v1_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["failed_coherent_v1_run_reusable_as_authority"] is False
    assert out["failed_coherent_v1_run_preserved"] is True
    assert out["prior_authorization_reusable"] is False


def test_consumed_v1_lineage_requires_preserved_failed_run(
    monkeypatch,
    tmp_path,
):
    claims = tmp_path / "claims"
    claims.mkdir()

    marker = claims / spent_v1.MARKER_NAME
    marker.write_bytes(b"synthetic marker")

    runs_root = tmp_path / "spent-runs"
    run_dir = runs_root / invocation.FAILED_COHERENT_V1_RUN_ID
    run_dir.mkdir(parents=True)

    monkeypatch.setattr(invocation, "CLAIMS_ROOT", claims)
    monkeypatch.setattr(spent_v1, "RUNS_ROOT", runs_root)
    monkeypatch.setattr(
        base_invocation,
        "_file_sha256",
        lambda path: invocation.CONSUMED_COHERENT_V1_ATTEMPT_MARKER_SHA256,
    )

    out = invocation._verify_consumed_coherent_v1_lineage()

    assert out["attempt_marker_sha256"] == (
        invocation.CONSUMED_COHERENT_V1_ATTEMPT_MARKER_SHA256
    )
    assert out["attempt_marker_reusable"] is False
    assert out["failed_run_id"] == invocation.FAILED_COHERENT_V1_RUN_ID
    assert out["failed_run_preserved"] is True
    assert out["result_absent"] is True
    assert out["closeout_absent"] is True


def test_consumed_v1_lineage_holds_if_failed_run_missing(
    monkeypatch,
    tmp_path,
):
    claims = tmp_path / "claims"
    claims.mkdir()
    (claims / spent_v1.MARKER_NAME).write_bytes(b"synthetic marker")

    runs_root = tmp_path / "spent-runs"
    runs_root.mkdir()

    monkeypatch.setattr(invocation, "CLAIMS_ROOT", claims)
    monkeypatch.setattr(spent_v1, "RUNS_ROOT", runs_root)
    monkeypatch.setattr(
        base_invocation,
        "_file_sha256",
        lambda path: invocation.CONSUMED_COHERENT_V1_ATTEMPT_MARKER_SHA256,
    )

    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentV2InvocationHold,
        match="FAILED_V1_RUN_MISSING",
    ):
        invocation._verify_consumed_coherent_v1_lineage()


def test_contract_preserves_fresh_preclaim_gpu_one_shot_boundary():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )

    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["fresh_preclaim_gpu_observation_implemented"] is True
    assert out["fresh_preclaim_gpu_admission_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["durable_create_only_attempt_marker_implemented"] is True
    assert out["attempt_marker_precedes_model_load_and_child_spawn"] is True
    assert out["marker_sha256_is_attempt_id"] is True
    assert out["authority_rechecked_after_claim"] is True
    assert out["authority_rechecked_before_each_inference_by_supervisor"] is True


def test_contract_requires_fresh_dual_authorization_and_distinct_tokens():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )

    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True
    assert out["explicit_execution_authorization_boolean_required"] is True
    assert out["explicit_policy_activation_authorization_boolean_required"] is True
    assert out["explicit_execution_confirmation_token_required"] is True
    assert out["explicit_policy_confirmation_token_required"] is True
    assert out["execution_and_policy_confirmation_tokens_distinct"] is True
    assert invocation.EXECUTION_CONFIRM_TOKEN != invocation.POLICY_CONFIRM_TOKEN


def test_contract_grants_no_claim_or_runtime_authority():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )

    assert out[
        "pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_reviewed"
    ] is False

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        assert out[field] is False


def test_execute_requires_fresh_execution_authorization_before_host_io():
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentV2InvocationHold,
        match="EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_coherent_v2_baseline_game(
            expected_main_head="0" * 40,
            expected_invocation_source_sha256="0" * 64,
            execution_authorization_accepted=False,
            policy_activation_authorization_accepted=True,
            execution_confirm=invocation.EXECUTION_CONFIRM_TOKEN,
            policy_confirm=invocation.POLICY_CONFIRM_TOKEN,
        )


def test_execute_requires_fresh_policy_authorization_before_host_io():
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentV2InvocationHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        invocation.execute_pair06_v8_combat_priority_coherent_v2_baseline_game(
            expected_main_head="0" * 40,
            expected_invocation_source_sha256="0" * 64,
            execution_authorization_accepted=True,
            policy_activation_authorization_accepted=False,
            execution_confirm=invocation.EXECUTION_CONFIRM_TOKEN,
            policy_confirm=invocation.POLICY_CONFIRM_TOKEN,
        )


def test_next_gate_is_source_binding_review_only():
    out = (
        invocation
        .pair06_v8_combat_priority_coherent_v2_baseline_attempt_invocation_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_entrypoint_holds():
    with pytest.raises(
        invocation.Pair06V8CombatPriorityCoherentV2InvocationHold,
        match="REPAIR_V2_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        invocation.authorize_or_execute()
