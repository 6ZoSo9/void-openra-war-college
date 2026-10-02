from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out["acceptance_path"] == review.ACCEPTANCE_PATH
    assert out["acceptance_git_blob"] == review.ACCEPTANCE_GIT_BLOB
    assert out["acceptance_test_path"] == review.ACCEPTANCE_TEST_PATH
    assert out["acceptance_test_git_blob"] == review.ACCEPTANCE_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_PATH).read_bytes()) == (
        review.ACCEPTANCE_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.ACCEPTANCE_TEST_PATH).read_bytes()) == (
        review.ACCEPTANCE_TEST_GIT_BLOB
    )


def test_review_binds_exact_authorization_and_main_snapshot():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_reviewed"
    ] is True
    assert out["authorization_text_sha256"] == (
        "2364e9c7c7e9e11d9dcdacbe68722b202eb0d5790b5d54cac6b92a995fcb94e8"
    )
    assert out["authorization_text_bytes"] == 286
    assert out["authorized_main_head"] == (
        "e61d66b64eccc4f52a6a951e68a3df7cdf75ce0b"
    )
    assert out["authorized_main_tree"] == (
        "27f5520c3a4018a66d6cf180f80d35ef655647fe"
    )


def test_review_accepts_all_four_fresh_authorization_gates():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_adapter_rejection_evidence_namespace_required"] is True


@pytest.mark.parametrize(
    "field",
    (
        "automatic_retry",
        "attempt_marker_created_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "execution_authorization_reusable_after_attempt_claim",
        "policy_activation_authorization_reusable_after_attempt_claim",
        "order_coherence_activation_authorization_reusable_after_attempt_claim",
        "repair_activation_authorization_reusable_after_attempt_claim",
    ),
)
def test_review_performs_no_effect_and_grants_no_follow_on_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorized_launcher():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceReviewHold,
        match="ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED",
    ):
        review.execute()
