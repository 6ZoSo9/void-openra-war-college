from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_authorization_source_binding_review_generation2
    as review,
)


def test_exact_retry_authorization_identities_are_pinned():
    out = review.v2r13_pair03_baseline_retry_authorization_review_contract()
    assert out["authorization_git_blob"] == (
        "083d41c66838e6795b4536253cd9546d3224e97c"
    )
    assert out["authorization_source_sha256"] == (
        "fc2b05c74feb95f5827e5d7e7e9785f4ca76724635c71ca41f74e03f765a84db"
    )
    assert out["authorization_test_git_blob"] == (
        "d2cc15422681acf866697634942433bdc501c6f9"
    )
    assert out["authorization_test_sha256"] == (
        "55b0863b076603565d3f23f1543d16e09ce76c45ebfac7779002e1ce6a68cd44"
    )


def test_review_keeps_retry_blocked_until_preservation_evidence():
    out = review.v2r13_pair03_baseline_retry_authorization_review_contract()
    assert out["authorization_source_binding_present"] is True
    assert out["authorization_reviewed"] is True
    assert out["single_pair03_baseline_retry_authorized_after_preservation"] is True
    assert out["max_retry_executions"] == 1
    assert out["automatic_retry"] is False
    assert out["retry_execution_authorized_now"] is False
    assert out["preservation_evidence_acceptance_required"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_PRESERVATION_EVIDENCE_ACCEPTANCE_REQUIRED",
    )


def test_retry_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineRetryAuthorizationReviewHold,
        match="V2R13_PAIR03_BASELINE_PRESERVATION_EVIDENCE_ACCEPTANCE_REQUIRED",
    ):
        review.execute_retry()
