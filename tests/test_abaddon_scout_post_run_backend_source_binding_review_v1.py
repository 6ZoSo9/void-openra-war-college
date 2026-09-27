from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_post_run_backend_source_binding_review_v1 as review


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_every_source_to_actual_repository_bytes():
    out = review.scout_post_run_backend_source_binding_review_contract()
    expected = {
        review.BACKEND_PATH: review.BACKEND_GIT_BLOB,
        review.BACKEND_TEST_PATH: review.BACKEND_TEST_GIT_BLOB,
        review.OBSERVER_CONTRACT_PATH: review.OBSERVER_CONTRACT_GIT_BLOB,
        review.OBSERVER_IMPLEMENTATION_PATH: review.OBSERVER_IMPLEMENTATION_GIT_BLOB,
        review.OBSERVER_REVIEW_PATH: review.OBSERVER_REVIEW_GIT_BLOB,
        review.DERIVED_RUNNER_PATH: review.DERIVED_RUNNER_GIT_BLOB,
    }
    assert out["source_references"] == expected
    for relative, expected_blob in expected.items():
        assert _git_blob_sha1((ROOT / relative).read_bytes()) == expected_blob


def test_one_byte_backend_source_drift_breaks_blob_identity():
    raw = (ROOT / review.BACKEND_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.BACKEND_GIT_BLOB
    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.BACKEND_GIT_BLOB


def test_review_closes_only_source_backend_gap():
    out = review.scout_post_run_backend_source_binding_review_contract()
    assert out["backend_source_binding_present"] is True
    assert out["backend_regression_binding_present"] is True
    assert out["all_five_post_run_probe_mechanics_implemented"] is True
    assert out["source_only_backend_gap_closed"] is True
    assert out["actual_host_observation_required_for_future_result_acceptance"] is True
    assert out["actual_host_observation_performed"] is False
    assert out["actual_scout_execution_authorized"] is False
    assert out["actual_scout_execution_performed"] is False
    assert out["next_gate"] == (
        "SCOUT_POST_RUN_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION"
    )
    assert out["next_change_class"] == "future_launcher_or_live_observation_only"


def test_review_preserves_zero_follow_on_authority():
    out = review.scout_post_run_backend_source_binding_review_contract()
    assert set(out["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in out["authority"].values())
    backend = out["backend_contract"]
    assert backend["automatic_host_backend_selection"] is False
    assert backend["observation_requires_explicit_authority"] is True
    assert backend["scout_execution_authorized"] is False
    assert backend["automatic_retry"] is False
    assert backend["training_authorized"] is False
    assert backend["automatic_policy_promotion_authorized"] is False


@pytest.mark.parametrize(
    "entrypoint",
    (review.observe_live_host, review.authorize_or_execute, review.accept_result),
)
def test_effectful_or_acceptance_entrypoints_hold(entrypoint):
    with pytest.raises(
        review.ScoutPostRunBackendSourceBindingReviewHold,
        match="LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION",
    ):
        entrypoint()
