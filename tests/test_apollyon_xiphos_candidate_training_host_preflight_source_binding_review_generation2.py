from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    apollyon_xiphos_candidate_training_host_preflight_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_preflight_and_tests_to_exact_bytes():
    out = review.apollyon_xiphos_candidate_training_host_preflight_review_contract()
    assert out["preflight_git_blob"] == review.PREFLIGHT_GIT_BLOB
    assert out["preflight_test_git_blob"] == review.PREFLIGHT_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.PREFLIGHT_PATH).read_bytes()) == (
        review.PREFLIGHT_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.PREFLIGHT_TEST_PATH).read_bytes()) == (
        review.PREFLIGHT_TEST_GIT_BLOB
    )


def test_review_requires_live_xiphos_observation_before_qualification():
    out = review.apollyon_xiphos_candidate_training_host_preflight_review_contract()
    assert out[
        "apollyon_xiphos_candidate_training_host_preflight_reviewed"
    ] is True
    assert out["preferred_candidate_training_host"] == "Xiphos"
    assert out["expected_host_normalized"] == "xiphos"
    assert out["read_only_host_collection_reviewed"] is True
    assert out["venv_python_symlink_to_regular_executable_reviewed"] is True
    assert out["venv_python_broken_symlink_rejected"] is True
    assert out["readonly_subprocess_user_bus_binding_reviewed"] is True
    assert out["readonly_subprocess_environment_inherits_shell"] is False
    assert out["external_service_control_query_uses_user_bus_binding"] is True
    assert out[
        "candidate_training_host_qualification_requires_live_observation"
    ] is True
    assert out["candidate_training_host_qualified"] is False


def test_review_retains_gpu_and_external_shutdown_boundaries():
    out = review.apollyon_xiphos_candidate_training_host_preflight_review_contract()
    assert out["minimum_cuda0_free_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_fraction_denominator"] == 10
    assert out["shutdown_control_external_to_trainable_model"] is True


@pytest.mark.parametrize(
    "field",
    (
        "candidate_training_execution_authorized",
        "selfplay_execution_authorized",
        "training_performed",
        "weights_updated",
        "deployment_authorized",
        "promotion_authorized",
        "network_access_authorized",
        "scheduler_mutation_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ),
)
def test_review_grants_no_training_or_external_authority(field):
    out = review.apollyon_xiphos_candidate_training_host_preflight_review_contract()
    assert out[field] is False


def test_review_stops_at_live_readonly_xiphos_observation():
    out = review.apollyon_xiphos_candidate_training_host_preflight_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "APOLLYON_XIPHOS_CANDIDATE_TRAINING_HOST_READONLY_OBSERVATION_REQUIRED"
    )


def test_operational_entrypoint_holds():
    with pytest.raises(
        review.ApollyonXiphosCandidateTrainingHostPreflightReviewHold,
        match="XIPHOS_CANDIDATE_TRAINING_HOST_READONLY_OBSERVATION_REQUIRED",
    ):
        review.qualify_train_execute_or_promote()
