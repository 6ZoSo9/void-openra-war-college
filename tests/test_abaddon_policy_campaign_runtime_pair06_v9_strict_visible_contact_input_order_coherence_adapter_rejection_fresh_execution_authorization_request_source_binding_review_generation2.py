from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_request_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_request_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )

    assert out["request_path"] == review.REQUEST_PATH
    assert out["request_git_blob"] == review.REQUEST_GIT_BLOB
    assert out["request_test_path"] == review.REQUEST_TEST_PATH
    assert out["request_test_git_blob"] == review.REQUEST_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.REQUEST_PATH).read_bytes()) == (
        review.REQUEST_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.REQUEST_TEST_PATH).read_bytes()) == (
        review.REQUEST_TEST_GIT_BLOB
    )


def test_review_binds_preserved_prior_lineage_and_fresh_namespace():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_fresh_execution_request_reviewed"
    ] is True
    assert out["prior_attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["preservation_receipt_sha256"] == (
        "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
    )
    assert out["fresh_adapter_rejection_evidence_namespace_required"] is True


def test_review_preserves_runtime_safety_and_four_fresh_authorizations():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10

    assert out["quadruple_explicit_authorizations_required"] is True
    assert out["quadruple_distinct_confirmation_tokens_required"] is True
    assert out["fresh_user_authorization_text_required"] is True


def test_review_refuses_prior_or_general_authorization_reuse():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )

    assert (
        out["general_source_work_authorization_is_execution_authorization"]
        is False
    )
    assert out["prior_authorization_text_reusable"] is False
    assert (
        out["preservation_authorization_reusable_as_execution_authority"]
        is False
    )


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_execution_or_follow_on_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_fresh_execution_authorization():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_request_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FRESH_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_execute_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionFreshExecutionRequestReviewHold,
        match="ADAPTER_REJECTION_FRESH_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.accept_or_execute()
