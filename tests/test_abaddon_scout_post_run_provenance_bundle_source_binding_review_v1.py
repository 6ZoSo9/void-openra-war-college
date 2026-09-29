from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_post_run_provenance_bundle_source_binding_review_v1 as review


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_bundle_and_regression_to_actual_repository_bytes():
    out = review.scout_post_run_provenance_source_review_contract()
    expected = {
        review.BUNDLE_PATH: review.BUNDLE_GIT_BLOB,
        review.BUNDLE_TEST_PATH: review.BUNDLE_TEST_GIT_BLOB,
        review.BACKEND_REVIEW_PATH: review.BACKEND_REVIEW_GIT_BLOB,
    }
    assert out["source_references"] == expected
    for relative, expected_blob in expected.items():
        assert _git_blob_sha1((ROOT / relative).read_bytes()) == expected_blob


def test_one_byte_bundle_source_drift_breaks_blob_identity():
    raw = (ROOT / review.BUNDLE_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.BUNDLE_GIT_BLOB
    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.BUNDLE_GIT_BLOB


def test_review_closes_only_source_provenance_gap():
    out = review.scout_post_run_provenance_source_review_contract()

    assert out["provenance_bundle_source_binding_present"] is True
    assert out["provenance_bundle_regression_binding_present"] is True
    assert out["backend_review_binding_preserved"] is True
    assert out["historical_v1_state_schema_preserved"] is True
    assert out["accepted_war_college_commit_bound"] is True
    assert out["expected_engine_commit_bound"] is True
    assert out["engine_container_name_bound"] is True
    assert out["post_run_state_digest_bound"] is True
    assert out["source_only_provenance_gap_closed"] is True
    assert out["actual_host_observation_performed"] is False
    assert out["actual_scout_execution_authorized"] is False
    assert out["actual_scout_execution_performed"] is False
    assert out["final_result_acceptance"] is False
    assert out["next_gate"] == (
        "SCOUT_POST_RUN_PROVENANCE_AWARE_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION"
    )
    assert out["next_change_class"] == (
        "future_live_observation_launcher_or_result_acceptance_only"
    )


def test_review_preserves_private_local_marker_context():
    out = review.scout_post_run_provenance_source_review_contract()

    assert out["local_marker_path_raw_publication"] is False
    assert out["local_directory_identity_raw_publication"] is False
    provenance = out["provenance_contract"]
    assert provenance["attempt_marker_path_raw_publication"] is False
    assert provenance["attempt_directory_identity_raw_publication"] is False


def test_review_preserves_zero_follow_on_authority():
    out = review.scout_post_run_provenance_source_review_contract()

    assert set(out["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in out["authority"].values())
    provenance = out["provenance_contract"]
    assert provenance["automatic_host_backend_selection"] is False
    assert provenance["contract_call_performs_host_observation"] is False
    assert provenance["final_result_acceptance"] is False
    assert all(value is False for value in provenance["authority"].values())


@pytest.mark.parametrize(
    "entrypoint",
    (review.observe_live_host, review.authorize_or_execute, review.accept_result),
)
def test_effectful_or_acceptance_entrypoints_hold(entrypoint):
    with pytest.raises(
        review.ScoutPostRunProvenanceSourceReviewHold,
        match="PROVENANCE_AWARE_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION",
    ):
        entrypoint()
