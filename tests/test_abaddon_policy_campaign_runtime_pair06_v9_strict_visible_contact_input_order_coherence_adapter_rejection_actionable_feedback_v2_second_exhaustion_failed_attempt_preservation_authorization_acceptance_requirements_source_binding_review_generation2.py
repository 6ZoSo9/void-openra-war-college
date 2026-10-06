from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_requirements_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_requirements_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_review_contract()
    )

    assert out["requirements_path"] == review.REQUIREMENTS_PATH
    assert out["requirements_git_blob"] == review.REQUIREMENTS_GIT_BLOB
    assert out["requirements_test_path"] == review.REQUIREMENTS_TEST_PATH
    assert out["requirements_test_git_blob"] == review.REQUIREMENTS_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.REQUIREMENTS_PATH).read_bytes()) == (
        review.REQUIREMENTS_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.REQUIREMENTS_TEST_PATH).read_bytes()) == (
        review.REQUIREMENTS_TEST_GIT_BLOB
    )


def test_review_binds_second_exhaustion_request_and_evidence():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_review_contract()
    )

    assert out[
        "pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_reviewed"
    ] is True
    assert isinstance(out["reviewed_request_sha256"], str)
    assert len(out["reviewed_request_sha256"]) == 64
    assert out["reviewed_request_bytes"] > 0
    assert out["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["warm_start_sha256"] == (
        "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    )
    assert out["trajectory_sha256"] == (
        "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    )
    assert out["predecessor_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )


def test_review_requires_fresh_specific_authorization_and_rejects_reuse():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_review_contract()
    )

    for field in (
        "exact_user_authorization_text_required",
        "authorization_text_sha256_binding_required",
        "authorization_text_byte_length_binding_required",
        "canonical_main_head_binding_required",
        "canonical_main_tree_binding_required",
        "canonical_main_must_be_bound_at_authorization_time",
        "authorization_must_reference_exact_reviewed_request",
    ):
        assert out[field] is True

    assert out["general_source_work_authorization_is_preservation_authorization"] is False
    assert out["prior_preservation_authorization_reusable"] is False
    assert out["prior_execution_authorization_reusable"] is False
    assert out["preservation_authorization_accepted"] is False
    assert out["preservation_performed"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["execution_request_opened"] is False


def test_review_stops_at_explicit_user_authorization():
    out = (
        review
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_review_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
        "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsReviewHold,
        match="PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        review.accept_or_preserve()
