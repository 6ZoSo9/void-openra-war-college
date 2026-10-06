from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_source_binding_review_generation2
    as review,
)

ROOT = Path(__file__).parents[1]

def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

def test_review_pins_preservation_and_tests_to_exact_bytes():
    out = review.pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract()
    assert out["preservation_path"] == review.PRESERVATION_PATH
    assert out["preservation_git_blob"] == review.PRESERVATION_GIT_BLOB
    assert out["preservation_test_path"] == review.PRESERVATION_TEST_PATH
    assert out["preservation_test_git_blob"] == review.PRESERVATION_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.PRESERVATION_PATH).read_bytes()) == review.PRESERVATION_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.PRESERVATION_TEST_PATH).read_bytes()) == review.PRESERVATION_TEST_GIT_BLOB

def test_review_binds_second_exhaustion_evidence_and_chain():
    out = review.pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract()
    assert out["pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_reviewed"] is True
    assert out["attempt_marker_sha256"] == "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    assert out["warm_start_sha256"] == "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    assert out["trajectory_sha256"] == "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    assert out["predecessor_preservation_receipt_sha256"] == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"

def test_review_accepts_no_authority():
    out = review.pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract()
    assert out["preservation_authorization_accepted"] is False
    assert out["preservation_performed"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["new_execution_request_opened"] is False

def test_review_stops_at_preservation_authorization_request():
    out = review.pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_FAILED_ATTEMPT_"
        "PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
    )
    with pytest.raises(
        review.Pair06V9ActionableFeedbackV2SecondExhaustionPreservationReviewHold,
        match="PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_or_preserve()
