"""Exact-blob review of the Xiphos candidate-training runtime admission.

Pins the source-only runtime admission and focused tests.  The review confirms
that Xiphos/V14 runtime readiness may be recognized only from a fresh
read-only observation, while actual training still requires a separate
one-shot external authorization and all external authority remains denied.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    apollyon_xiphos_candidate_training_runtime_admission_generation2 as admission,
)


CONTRACT_SCHEMA = (
    "void.apollyon.generation2."
    "xiphos-candidate-training-runtime-admission-review.v1"
)
ACCEPTED_BASE_HEAD = "426cd18aa1d66df0658cd38f88feb7f7ea25cfed"

ADMISSION_PATH = (
    "openra_env/learning/"
    "apollyon_xiphos_candidate_training_runtime_admission_generation2.py"
)
ADMISSION_GIT_BLOB = "ec0bfd7d4d9452bbf2cd1f329050d8e800436831"

ADMISSION_TEST_PATH = (
    "tests/test_apollyon_xiphos_candidate_training_runtime_admission_generation2.py"
)
ADMISSION_TEST_GIT_BLOB = "6339c12b3a02765a4579d748624e7f937d5975c7"

NEXT_GATE = (
    "APOLLYON_XIPHOS_CANDIDATE_TRAINING_RUNTIME_READONLY_OBSERVATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "host_readonly_apollyon_xiphos_candidate_training_runtime_observation"
)


class ApollyonXiphosCandidateTrainingRuntimeAdmissionReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ApollyonXiphosCandidateTrainingRuntimeAdmissionReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = admission.apollyon_xiphos_candidate_training_runtime_admission_contract()

    _require(
        out.get("qualified_main_head")
        == "426cd18aa1d66df0658cd38f88feb7f7ea25cfed"
        and out.get("expected_host") == "Xiphos"
        and out.get("expected_gpu_name") == "NVIDIA GeForce RTX 5070",
        "Xiphos training runtime host/source identity drift",
    )
    _require(
        out.get("runtime_manifest_sha256")
        == "13914628fb815d81e5d2cb005868f1c04f55c70e604d59a388a729723c2152a7"
        and out.get("pip_freeze_sha256")
        == "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77",
        "Xiphos training runtime manifest/package-lock drift",
    )
    _require(
        out.get("expected_runtime_assets") == admission.EXPECTED_RUNTIME_ASSETS,
        "Xiphos training runtime asset binding drift",
    )
    _require(
        out.get("candidate_output_create_only_required") is True
        and out.get("fresh_readonly_observation_required") is True
        and out.get("host_qualification_required") is True
        and out.get("cuda0_idle_required") is True
        and out.get("external_service_control_required") is True
        and out.get("gpu_recheck_immediately_before_execution_required") is True
        and out.get(
            "external_revocation_check_immediately_before_execution_required"
        )
        is True
        and out.get("one_shot_training_authorization_required") is True,
        "Xiphos training runtime admission boundary drift",
    )

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
        _require(
            out.get(field) is False,
            "Xiphos training runtime authority drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (ADMISSION_PATH, ADMISSION_GIT_BLOB),
        (ADMISSION_TEST_PATH, ADMISSION_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def apollyon_xiphos_candidate_training_runtime_admission_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "admission_path": ADMISSION_PATH,
        "admission_git_blob": ADMISSION_GIT_BLOB,
        "admission_test_path": ADMISSION_TEST_PATH,
        "admission_test_git_blob": ADMISSION_TEST_GIT_BLOB,
        "apollyon_xiphos_candidate_training_runtime_admission_reviewed": True,
        "qualified_main_head": validated["qualified_main_head"],
        "expected_host": validated["expected_host"],
        "expected_gpu_name": validated["expected_gpu_name"],
        "runtime_manifest_sha256": validated["runtime_manifest_sha256"],
        "pip_freeze_sha256": validated["pip_freeze_sha256"],
        "candidate_output_create_only_required": True,
        "fresh_readonly_observation_required": True,
        "cuda0_idle_required": True,
        "external_service_control_required": True,
        "one_shot_training_authorization_required": True,
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
        "validated_admission": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_train_execute_or_promote(*args: Any, **kwargs: Any) -> None:
    raise ApollyonXiphosCandidateTrainingRuntimeAdmissionReviewHold(NEXT_GATE)
