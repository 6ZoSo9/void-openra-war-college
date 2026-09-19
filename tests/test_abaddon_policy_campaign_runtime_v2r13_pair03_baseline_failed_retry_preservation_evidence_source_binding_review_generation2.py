from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_evidence_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_evidence_source_binding_review_generation2.py"
)


def test_exact_acceptance_identities_are_pinned():
    out = review.v2r13_pair03_failed_retry_preservation_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == (
        "6e35f4603cc2870d743193e78e977fedeb586c38"
    )
    assert out["acceptance_source_sha256"] == (
        "00e358ed9d0fc6b4c408d875a8ca716f50028e744360b59392e70c90d53ea8e1"
    )
    assert out["acceptance_test_git_blob"] == (
        "24e1025b4f800fa4502269e2ce92c79495368757"
    )
    assert out["acceptance_test_sha256"] == (
        "6154677d27a221ea5ec309a6fe5a5d20375e9aa69f5a636056d84257c693beb8"
    )


def test_review_keeps_additional_retry_closed():
    out = review.v2r13_pair03_failed_retry_preservation_evidence_review_contract()
    assert out["preservation_evidence_source_binding_present"] is True
    assert out["preservation_evidence_reviewed"] is True
    assert out["retry_authorization_consumed"] is True
    assert out["additional_retry_authorized"] is False
    assert out["additional_retry_performed"] is False
    assert out["runtime_execution_authorized_now"] is False
    assert out["automatic_retry"] is False


def test_review_does_not_expand_scope():
    out = review.v2r13_pair03_failed_retry_preservation_evidence_review_contract()
    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_additional_retry_authorization():
    out = review.v2r13_pair03_failed_retry_preservation_evidence_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED"
    )


def test_review_source_is_host_action_free():
    tree = ast.parse(
        REVIEW_SOURCE.read_text(encoding="utf-8"),
        filename=str(REVIEW_SOURCE),
    )
    forbidden = {
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "httpx",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_additional_retry_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03FailedRetryPreservationEvidenceReviewHold,
        match="V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_additional_retry()
