from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_proposal_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_proposal_and_tests_to_repository_bytes():
    out = review.pair06_v9_strict_visible_contact_policy_proposal_review_contract()

    assert out["proposal_path"] == review.PROPOSAL_PATH
    assert out["proposal_git_blob"] == review.PROPOSAL_GIT_BLOB
    assert out["proposal_test_path"] == review.PROPOSAL_TEST_PATH
    assert out["proposal_test_git_blob"] == review.PROPOSAL_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.PROPOSAL_PATH).read_bytes())
        == review.PROPOSAL_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.PROPOSAL_TEST_PATH).read_bytes())
        == review.PROPOSAL_TEST_GIT_BLOB
    )


def test_one_byte_proposal_drift_breaks_blob_identity():
    raw = (ROOT / review.PROPOSAL_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.PROPOSAL_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.PROPOSAL_GIT_BLOB


def test_review_preserves_hypothesis_boundary_and_no_causal_overclaim():
    out = review.pair06_v9_strict_visible_contact_policy_proposal_review_contract()

    assert (
        out["pair06_v9_strict_visible_contact_policy_proposal_reviewed"]
        is True
    )
    assert out["causal_claim_made"] is False
    assert out["action_level_causal_attribution_available"] is False
    assert out["recovery_mode_changed"] is False
    assert out["normal_mode_changed"] is False
    assert out["visible_contact_mode_changed"] is True
    assert (
        out["reinforcement_tools_allowed_during_strict_visible_contact"]
        is False
    )


def test_review_stays_source_only_and_opens_no_execution_request():
    out = review.pair06_v9_strict_visible_contact_policy_proposal_review_contract()

    assert out["implementation_present"] is False
    assert out["runtime_integration_present"] is False
    assert out["new_execution_request_opened"] is False
    for field in (
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_implementation():
    out = review.pair06_v9_strict_visible_contact_policy_proposal_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_strict_visible_contact_policy_implementation"
    )


def test_implement_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactProposalReviewHold,
        match="POLICY_IMPLEMENTATION_REQUIRED",
    ):
        review.implement_or_execute()
