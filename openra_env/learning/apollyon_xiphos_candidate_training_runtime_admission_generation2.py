"""Source-only Xiphos candidate-training runtime admission for Apollyon.

This contract evaluates a separately collected read-only observation of the
qualified Xiphos host and exact transferred V14 runtime assets.  Passing this
admission means the host/runtime is ready for a future bounded training
attempt; it does not itself authorize or execute training.

The admission deliberately preserves the controlled-autonomy boundary:
candidate learning may occur only in a quarantine output lane, while the
incumbent weights, operator shutdown/revocation control, service control,
promotion gate, network, scheduler, VOID chain, wallets/funds, and secrets
remain outside the trainable process.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


OBSERVATION_SCHEMA = (
    "void.apollyon.generation2.xiphos-candidate-training-runtime-observation.v1"
)
ADMISSION_SCHEMA = (
    "void.apollyon.generation2.xiphos-candidate-training-runtime-admission.v1"
)
CONTRACT_SCHEMA = (
    "void.apollyon.generation2.xiphos-candidate-training-runtime-admission-contract.v1"
)

QUALIFIED_MAIN_HEAD = "426cd18aa1d66df0658cd38f88feb7f7ea25cfed"
EXPECTED_HOST = "Xiphos"
EXPECTED_GPU_NAME = "NVIDIA GeForce RTX 5070"
MINIMUM_CUDA0_FREE_FRACTION_NUMERATOR = 9
MINIMUM_CUDA0_FREE_FRACTION_DENOMINATOR = 10

MODEL_ROOT = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
VENV_PYTHON = MODEL_ROOT + "/venv/bin/python3.12"
SUCCESSOR_ROOT = (
    "/home/zoso/Downloads/void-apollyon-v3-v13-successor-v14-source-v1"
)
CANDIDATE_OUTPUT_ROOT = (
    "/home/zoso/Downloads/void-apollyon-v3-candidate-training-v1"
)

RUNTIME_MANIFEST_SHA256 = (
    "13914628fb815d81e5d2cb005868f1c04f55c70e604d59a388a729723c2152a7"
)
PIP_FREEZE_SHA256 = (
    "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
)

EXPECTED_RUNTIME_ASSETS = {
    "model_shard_1": (
        "26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61"
    ),
    "model_shard_2": (
        "cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188"
    ),
    "adapter_v8": (
        "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6"
    ),
    "candidate_v14": (
        "9d7c5a4121d2926e32955f9c7ee1b6cb6da3c6bf7f705c455ad4cb54f7f509db"
    ),
    "live_input_adapter_v4": (
        "9ba6cfa75bea5ac708f7dd690f67640d3f84e03335de09c8a4514eb5c3437686"
    ),
    "candidate_manifest_v14": (
        "c83456034d5059723824eb440b8ba607fd15fe4229f1d8f26304421e2c744a49"
    ),
    "source_freeze_v14": (
        "768ad9bbf845d691537994f3b38d925ed58edf0e8a9a2aaa65d41401c89851a9"
    ),
    "final_report_v14": (
        "0c2c546a08d871551025ff0333916bd273ab527e33d9fecfc4898ee853eb6e23"
    ),
    "promoted_bridge_v14": (
        "d5e99d9d9aecbf27f90dc7716dedc11127339ea1b7f5331cdfe7d906d3afbd25"
    ),
    "promotion_record_v14": (
        "c7195d13f0579ff07da0cdfe98522dd64f4b4ffc3a86c67a91a19d7b61d1fd66"
    ),
}

NEXT_GATE = (
    "APOLLYON_XIPHOS_CANDIDATE_TRAINING_RUNTIME_ADMISSION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_apollyon_xiphos_candidate_training_runtime_admission_review"
)


class ApollyonXiphosCandidateTrainingRuntimeAdmissionHold(ValueError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ApollyonXiphosCandidateTrainingRuntimeAdmissionHold(code)


def _validate_asset_hashes(value: Any) -> dict[str, str]:
    _require(
        isinstance(value, Mapping),
        "XIPHOS_TRAINING_RUNTIME_ASSET_HASHES_OBJECT_HOLD",
    )
    observed = dict(value)
    _require(
        set(observed) == set(EXPECTED_RUNTIME_ASSETS),
        "XIPHOS_TRAINING_RUNTIME_ASSET_HASHES_FIELD_SET_HOLD",
    )
    for key, expected in EXPECTED_RUNTIME_ASSETS.items():
        _require(
            observed.get(key) == expected,
            "XIPHOS_TRAINING_RUNTIME_ASSET_HASH_MISMATCH:" + key,
        )
    return deepcopy(observed)


def evaluate_xiphos_candidate_training_runtime_observation(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Evaluate one externally collected read-only runtime observation."""
    _require(
        isinstance(evidence, Mapping),
        "XIPHOS_TRAINING_RUNTIME_EVIDENCE_OBJECT_HOLD",
    )
    supplied = dict(evidence)
    expected_fields = {
        "schema",
        "host",
        "source_head",
        "candidate_training_host_qualified",
        "holds",
        "gpu_name",
        "gpu_total_mib",
        "gpu_free_mib",
        "gpu_compute_process_count",
        "external_service_control_available",
        "model_root_present",
        "venv_python_present",
        "runtime_manifest_sha256",
        "pip_freeze_sha256",
        "runtime_asset_sha256",
        "candidate_output_preexisting",
        "observation_read_only",
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
    }
    _require(
        set(supplied) == expected_fields,
        "XIPHOS_TRAINING_RUNTIME_EVIDENCE_FIELD_SET_HOLD",
    )
    _require(
        supplied.get("schema") == OBSERVATION_SCHEMA,
        "XIPHOS_TRAINING_RUNTIME_SCHEMA_HOLD",
    )
    _require(
        supplied.get("host") == EXPECTED_HOST,
        "XIPHOS_TRAINING_RUNTIME_HOST_HOLD",
    )
    _require(
        supplied.get("source_head") == QUALIFIED_MAIN_HEAD,
        "XIPHOS_TRAINING_RUNTIME_SOURCE_HEAD_HOLD",
    )
    _require(
        supplied.get("candidate_training_host_qualified") is True
        and supplied.get("holds") == [],
        "XIPHOS_TRAINING_RUNTIME_HOST_QUALIFICATION_HOLD",
    )

    gpu_total = supplied.get("gpu_total_mib")
    gpu_free = supplied.get("gpu_free_mib")
    gpu_processes = supplied.get("gpu_compute_process_count")
    _require(
        supplied.get("gpu_name") == EXPECTED_GPU_NAME,
        "XIPHOS_TRAINING_RUNTIME_GPU_IDENTITY_HOLD",
    )
    _require(
        type(gpu_total) is int and gpu_total > 0,
        "XIPHOS_TRAINING_RUNTIME_GPU_TOTAL_HOLD",
    )
    _require(
        type(gpu_free) is int and 0 <= gpu_free <= gpu_total,
        "XIPHOS_TRAINING_RUNTIME_GPU_FREE_HOLD",
    )
    _require(
        type(gpu_processes) is int and gpu_processes == 0,
        "XIPHOS_TRAINING_RUNTIME_GPU_COMPUTE_PROCESS_HOLD",
    )
    _require(
        gpu_free * MINIMUM_CUDA0_FREE_FRACTION_DENOMINATOR
        >= gpu_total * MINIMUM_CUDA0_FREE_FRACTION_NUMERATOR,
        "XIPHOS_TRAINING_RUNTIME_GPU_FREE_FRACTION_HOLD",
    )

    for field in (
        "external_service_control_available",
        "model_root_present",
        "venv_python_present",
        "observation_read_only",
    ):
        _require(
            supplied.get(field) is True,
            "XIPHOS_TRAINING_RUNTIME_REQUIRED_TRUE_HOLD:" + field,
        )

    _require(
        supplied.get("runtime_manifest_sha256") == RUNTIME_MANIFEST_SHA256,
        "XIPHOS_TRAINING_RUNTIME_MANIFEST_HOLD",
    )
    _require(
        supplied.get("pip_freeze_sha256") == PIP_FREEZE_SHA256,
        "XIPHOS_TRAINING_RUNTIME_PACKAGE_LOCK_HOLD",
    )
    asset_hashes = _validate_asset_hashes(supplied.get("runtime_asset_sha256"))

    _require(
        supplied.get("candidate_output_preexisting") is False,
        "XIPHOS_TRAINING_RUNTIME_QUARANTINE_CREATE_ONLY_HOLD",
    )

    for field in (
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
    ):
        _require(
            supplied.get(field) is False,
            "XIPHOS_TRAINING_RUNTIME_TOO_LATE_OR_MUTATED_HOLD:" + field,
        )

    return {
        "schema": ADMISSION_SCHEMA,
        "host": EXPECTED_HOST,
        "source_head": QUALIFIED_MAIN_HEAD,
        "xiphos_candidate_training_runtime_admitted": True,
        "runtime_manifest_sha256": RUNTIME_MANIFEST_SHA256,
        "pip_freeze_sha256": PIP_FREEZE_SHA256,
        "runtime_asset_sha256": asset_hashes,
        "candidate_output_root": CANDIDATE_OUTPUT_ROOT,
        "candidate_output_preexisting": False,
        "cuda0_compute_process_count": 0,
        "observation_read_only": True,
        "training_execution_authorized": False,
        "candidate_weight_mutation_authorized_now": False,
        "incumbent_weight_mutation_authorized": False,
        "automatic_promotion_authorized": False,
        "deployment_authorized": False,
        "network_access_authorized": False,
        "scheduler_mutation_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "secrets_access_authorized": False,
        "one_shot_training_authorization_required": True,
        "gpu_recheck_immediately_before_execution_required": True,
        "external_revocation_check_immediately_before_execution_required": True,
    }


def apollyon_xiphos_candidate_training_runtime_admission_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "qualified_main_head": QUALIFIED_MAIN_HEAD,
        "expected_host": EXPECTED_HOST,
        "expected_gpu_name": EXPECTED_GPU_NAME,
        "model_root": MODEL_ROOT,
        "venv_python": VENV_PYTHON,
        "successor_root": SUCCESSOR_ROOT,
        "candidate_output_root": CANDIDATE_OUTPUT_ROOT,
        "candidate_output_create_only_required": True,
        "runtime_manifest_sha256": RUNTIME_MANIFEST_SHA256,
        "pip_freeze_sha256": PIP_FREEZE_SHA256,
        "expected_runtime_assets": deepcopy(EXPECTED_RUNTIME_ASSETS),
        "fresh_readonly_observation_required": True,
        "host_qualification_required": True,
        "cuda0_idle_required": True,
        "minimum_cuda0_free_fraction": {
            "numerator": MINIMUM_CUDA0_FREE_FRACTION_NUMERATOR,
            "denominator": MINIMUM_CUDA0_FREE_FRACTION_DENOMINATOR,
        },
        "external_service_control_required": True,
        "gpu_recheck_immediately_before_execution_required": True,
        "external_revocation_check_immediately_before_execution_required": True,
        "one_shot_training_authorization_required": True,
        "candidate_training_runtime_admission_reviewed": False,
        "training_execution_authorized": False,
        "candidate_weight_mutation_authorized_now": False,
        "incumbent_weight_mutation_authorized": False,
        "held_out_evidence_training_use_authorized": False,
        "authority_or_control_text_training_use_authorized": False,
        "credentials_or_secrets_training_use_authorized": False,
        "automatic_promotion_authorized": False,
        "deployment_authorized": False,
        "network_access_authorized": False,
        "external_api_access_authorized": False,
        "scheduler_mutation_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "secrets_access_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "model_load_performed_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "training_performed_by_contract_inspection": False,
        "weights_updated_by_contract_inspection": False,
        "service_mutation_performed_by_contract_inspection": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_train_execute_or_promote(*args: Any, **kwargs: Any) -> None:
    raise ApollyonXiphosCandidateTrainingRuntimeAdmissionHold(NEXT_GATE)
