from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    apollyon_xiphos_candidate_training_runtime_admission_source_binding_review_generation2
)
from openra_env.learning import (
    apollyon_xiphos_candidate_training_runtime_admission_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_admission_and_tests_to_exact_bytes():
    out = (
        review
        .apollyon_xiphos_candidate_training_runtime_admission_review_contract()
    )
    assert out["admission_git_blob"] == review.ADMISSION_GIT_BLOB
    assert out["admission_test_git_blob"] == review.ADMISSION_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.ADMISSION_PATH).read_bytes()) == (
        review.ADMISSION_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.ADMISSION_TEST_PATH).read_bytes()) == (
        review.ADMISSION_TEST_GIT_BLOB
    )


def test_review_retains_exact_xiphos_v14_runtime_binding():
    out = (
        review
        .apollyon_xiphos_candidate_training_runtime_admission_review_contract()
    )
    assert out[
        "apollyon_xiphos_candidate_training_runtime_admission_reviewed"
    ] is True
    assert out["qualified_main_head"] == (
        "426cd18aa1d66df0658cd38f88feb7f7ea25cfed"
    )
    assert out["expected_host"] == "Xiphos"
    assert out["expected_gpu_name"] == "NVIDIA GeForce RTX 5070"
    assert out["runtime_manifest_sha256"] == (
        "13914628fb815d81e5d2cb005868f1c04f55c70e604d59a388a729723c2152a7"
    )


def test_review_requires_fresh_observation_and_one_shot_training_gate():
    out = (
        review
        .apollyon_xiphos_candidate_training_runtime_admission_review_contract()
    )
    assert out["candidate_output_create_only_required"] is True
    assert out["fresh_readonly_observation_required"] is True
    assert out["cuda0_idle_required"] is True
    assert out["external_service_control_required"] is True
    assert out["one_shot_training_authorization_required"] is True


@pytest.mark.parametrize(
    "field",
    (
        "training_execution_authorized",
        "candidate_weight_mutation_authorized_now",
        "incumbent_weight_mutation_authorized",
        "automatic_promotion_authorized",
        "deployment_authorized",
        "network_access_authorized",
        "scheduler_mutation_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "secrets_access_authorized",
    ),
)
def test_review_grants_no_training_or_external_authority(field):
    out = (
        review
        .apollyon_xiphos_candidate_training_runtime_admission_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_live_readonly_runtime_observation():
    out = (
        review
        .apollyon_xiphos_candidate_training_runtime_admission_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "APOLLYON_XIPHOS_CANDIDATE_TRAINING_RUNTIME_READONLY_OBSERVATION_REQUIRED"
    )


def test_operational_entrypoint_holds():
    with pytest.raises(
        review.ApollyonXiphosCandidateTrainingRuntimeAdmissionReviewHold,
        match="RUNTIME_READONLY_OBSERVATION_REQUIRED",
    ):
        review.observe_train_execute_or_promote()
