from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    apollyon_controlled_autonomous_learning_policy_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_policy_and_tests_to_exact_bytes():
    out = review.apollyon_controlled_autonomous_learning_policy_review_contract()

    assert out["policy_path"] == review.POLICY_PATH
    assert out["policy_git_blob"] == review.POLICY_GIT_BLOB
    assert out["policy_test_path"] == review.POLICY_TEST_PATH
    assert out["policy_test_git_blob"] == review.POLICY_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.POLICY_PATH).read_bytes()) == (
        review.POLICY_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.POLICY_TEST_PATH).read_bytes()) == (
        review.POLICY_TEST_GIT_BLOB
    )


def test_review_binds_controlled_autonomy_authorization():
    out = review.apollyon_controlled_autonomous_learning_policy_review_contract()
    assert out["apollyon_controlled_autonomous_learning_policy_reviewed"] is True
    assert out["user_authorization_text_sha256"] == (
        "0d8f31326e2d737411b550a0d767b0011a0164618d5866cff1f083232be16a69"
    )
    assert out["user_authorization_text_bytes"] == 152


def test_review_preserves_external_shutdown_and_promotion_control():
    out = review.apollyon_controlled_autonomous_learning_policy_review_contract()
    assert out["authority_envelope_trainable"] is False
    assert out["operator_directive_precedence_required"] is True
    assert out["shutdown_control_external_to_trainable_model"] is True
    assert out["model_may_disable_revocation"] is False
    assert out["model_may_mutate_shutdown_control"] is False
    assert out["incumbent_weight_mutation_allowed"] is False
    assert out["automatic_promotion_allowed"] is False
    assert out["promotion_requires_external_operator_acceptance"] is True


def test_review_allows_only_quarantined_candidate_learning_after_host_preflight():
    out = review.apollyon_controlled_autonomous_learning_policy_review_contract()
    assert out["learning_scope"] == "tactical_competence_only"
    assert out["incumbent_host"] == "Precision"
    assert out["preferred_candidate_training_host"] == "Xiphos"
    assert out["candidate_training_allowed_after_external_host_preflight"] is True
    assert out["candidate_weight_mutation_allowed_in_quarantine"] is True


@pytest.mark.parametrize(
    "field",
    (
        "candidate_host_execution_authorized_now",
        "candidate_training_execution_authorized_now",
        "selfplay_execution_authorized_now",
        "network_access_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "deployment_authorized",
        "promotion_authorized",
    ),
)
def test_review_grants_no_immediate_external_or_runtime_authority(field):
    out = review.apollyon_controlled_autonomous_learning_policy_review_contract()
    assert out[field] is False


def test_review_stops_at_xiphos_host_qualification():
    out = review.apollyon_controlled_autonomous_learning_policy_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "APOLLYON_XIPHOS_CANDIDATE_TRAINING_HOST_QUALIFICATION_REQUIRED"
    )


def test_operational_review_entrypoint_holds():
    with pytest.raises(
        review.ApollyonControlledAutonomousLearningPolicyReviewHold,
        match="XIPHOS_CANDIDATE_TRAINING_HOST_QUALIFICATION_REQUIRED",
    ):
        review.qualify_train_execute_promote_or_disable_controls()
