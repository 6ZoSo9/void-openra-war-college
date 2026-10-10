from __future__ import annotations

import pytest

from openra_env.learning import (
    apollyon_xiphos_candidate_training_runtime_admission_generation2 as admission,
)


def clean_observation() -> dict:
    return {
        "schema": admission.OBSERVATION_SCHEMA,
        "host": "Xiphos",
        "source_head": "f" * 40,
        "source_main_branch": True,
        "source_tracked_clean": True,
        "qualified_main_ancestor_verified": True,
        "candidate_training_host_qualified": True,
        "holds": [],
        "gpu_name": "NVIDIA GeForce RTX 5070",
        "gpu_total_mib": 12227,
        "gpu_free_mib": 11741,
        "gpu_compute_process_count": 0,
        "external_service_control_available": True,
        "model_root_present": True,
        "venv_python_present": True,
        "runtime_manifest_sha256": admission.RUNTIME_MANIFEST_SHA256,
        "pip_freeze_sha256": admission.PIP_FREEZE_SHA256,
        "runtime_asset_sha256": dict(admission.EXPECTED_RUNTIME_ASSETS),
        "candidate_output_preexisting": False,
        "observation_read_only": True,
        "model_load_performed": False,
        "model_inference_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "incumbent_weight_mutation_performed": False,
        "service_mutation_performed": False,
        "network_access_performed": False,
        "scheduler_mutation_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "secrets_access_performed": False,
    }


def test_clean_runtime_observation_is_admissible_but_not_authorized_to_train():
    out = admission.evaluate_xiphos_candidate_training_runtime_observation(
        clean_observation()
    )
    assert out["xiphos_candidate_training_runtime_admitted"] is True
    assert out["source_head"] == "f" * 40
    assert out["qualified_main_head"] == admission.QUALIFIED_MAIN_HEAD
    assert out["source_main_branch"] is True
    assert out["source_tracked_clean"] is True
    assert out["qualified_main_ancestor_verified"] is True
    assert out["training_execution_authorized"] is False
    assert out["candidate_weight_mutation_authorized_now"] is False
    assert out["incumbent_weight_mutation_authorized"] is False
    assert out["one_shot_training_authorization_required"] is True
    assert out["gpu_recheck_immediately_before_execution_required"] is True
    assert out[
        "external_revocation_check_immediately_before_execution_required"
    ] is True





@pytest.mark.parametrize(
    "field",
    (
        "source_main_branch",
        "source_tracked_clean",
        "qualified_main_ancestor_verified",
    ),
)
def test_source_lineage_must_remain_clean_main_descendant(field):
    evidence = clean_observation()
    evidence[field] = False
    with pytest.raises(
        admission.ApollyonXiphosCandidateTrainingRuntimeAdmissionHold,
        match="SOURCE_LINEAGE_HOLD",
    ):
        admission.evaluate_xiphos_candidate_training_runtime_observation(evidence)


def test_runtime_asset_hash_drift_fails_closed():
    evidence = clean_observation()
    evidence["runtime_asset_sha256"]["adapter_v8"] = "0" * 64
    with pytest.raises(
        admission.ApollyonXiphosCandidateTrainingRuntimeAdmissionHold,
        match="ASSET_HASH_MISMATCH:adapter_v8",
    ):
        admission.evaluate_xiphos_candidate_training_runtime_observation(evidence)


def test_busy_gpu_fails_closed():
    evidence = clean_observation()
    evidence["gpu_compute_process_count"] = 1
    with pytest.raises(
        admission.ApollyonXiphosCandidateTrainingRuntimeAdmissionHold,
        match="GPU_COMPUTE_PROCESS_HOLD",
    ):
        admission.evaluate_xiphos_candidate_training_runtime_observation(evidence)


def test_preexisting_candidate_output_fails_create_only_admission():
    evidence = clean_observation()
    evidence["candidate_output_preexisting"] = True
    with pytest.raises(
        admission.ApollyonXiphosCandidateTrainingRuntimeAdmissionHold,
        match="QUARANTINE_CREATE_ONLY_HOLD",
    ):
        admission.evaluate_xiphos_candidate_training_runtime_observation(evidence)


@pytest.mark.parametrize(
    "field",
    (
        "model_load_performed",
        "model_inference_performed",
        "training_performed",
        "weights_updated",
        "incumbent_weight_mutation_performed",
        "service_mutation_performed",
        "network_access_performed",
        "scheduler_mutation_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "secrets_access_performed",
    ),
)
def test_observation_must_precede_training_or_external_mutation(field):
    evidence = clean_observation()
    evidence[field] = True
    with pytest.raises(
        admission.ApollyonXiphosCandidateTrainingRuntimeAdmissionHold,
        match="TOO_LATE_OR_MUTATED_HOLD",
    ):
        admission.evaluate_xiphos_candidate_training_runtime_observation(evidence)


def test_contract_preserves_training_and_external_authority_boundaries():
    out = admission.apollyon_xiphos_candidate_training_runtime_admission_contract()
    assert out["candidate_training_runtime_admission_reviewed"] is False
    assert out["candidate_output_create_only_required"] is True
    assert out["fresh_readonly_observation_required"] is True
    assert out["host_qualification_required"] is True
    assert out["cuda0_idle_required"] is True
    assert out["external_service_control_required"] is True
    assert out["one_shot_training_authorization_required"] is True

    for field in (
        "training_execution_authorized",
        "candidate_weight_mutation_authorized_now",
        "incumbent_weight_mutation_authorized",
        "held_out_evidence_training_use_authorized",
        "authority_or_control_text_training_use_authorized",
        "credentials_or_secrets_training_use_authorized",
        "automatic_promotion_authorized",
        "deployment_authorized",
        "network_access_authorized",
        "external_api_access_authorized",
        "scheduler_mutation_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "secrets_access_authorized",
        "host_io_performed_by_contract_inspection",
        "model_load_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "training_performed_by_contract_inspection",
        "weights_updated_by_contract_inspection",
        "service_mutation_performed_by_contract_inspection",
    ):
        assert out[field] is False


def test_contract_binds_exact_v14_runtime_surface():
    out = admission.apollyon_xiphos_candidate_training_runtime_admission_contract()
    assert out["qualified_main_head"] == (
        "426cd18aa1d66df0658cd38f88feb7f7ea25cfed"
    )
    assert out["current_source_must_descend_from_qualified_main"] is True
    assert out["current_source_main_branch_required"] is True
    assert out["current_source_tracked_clean_required"] is True
    assert out["runtime_manifest_sha256"] == (
        "13914628fb815d81e5d2cb005868f1c04f55c70e604d59a388a729723c2152a7"
    )
    assert out["pip_freeze_sha256"] == (
        "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
    )
    assert out["expected_runtime_assets"]["adapter_v8"] == (
        "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6"
    )


def test_contract_advances_only_to_source_binding_review():
    out = admission.apollyon_xiphos_candidate_training_runtime_admission_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "APOLLYON_XIPHOS_CANDIDATE_TRAINING_RUNTIME_ADMISSION_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_operational_entrypoint_holds():
    with pytest.raises(
        admission.ApollyonXiphosCandidateTrainingRuntimeAdmissionHold,
        match="RUNTIME_ADMISSION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        admission.observe_train_execute_or_promote()
