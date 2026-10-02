from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_lineage_operator_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_fresh_operator_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_review_contract()
    )

    assert out["operator_path"] == review.OPERATOR_PATH
    assert out["operator_git_blob"] == review.OPERATOR_GIT_BLOB
    assert out["operator_test_path"] == review.OPERATOR_TEST_PATH
    assert out["operator_test_git_blob"] == review.OPERATOR_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.OPERATOR_PATH).read_bytes()) == (
        review.OPERATOR_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.OPERATOR_TEST_PATH).read_bytes()) == (
        review.OPERATOR_TEST_GIT_BLOB
    )


def test_review_binds_fresh_namespace_and_consumed_lineage():
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_review_contract()
    )

    assert out[
        "pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_reviewed"
    ] is True
    assert out["fresh_adapter_rejection_evidence_namespace_required"] is True
    assert out["prior_input_order_attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert out["prior_input_order_attempt_reusable"] is False
    assert out["prior_input_order_authorization_reusable"] is False
    assert out["quadruple_explicit_authorizations_required"] is True
    assert out["quadruple_distinct_confirmation_tokens_required"] is True


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "execution_request_created",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_authority(field):
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_review_contract()
    )
    assert out[field] is False


def test_preservation_is_required_before_any_execution_request():
    out = (
        review
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_review_contract()
    )

    assert out[
        "prior_failed_attempt_preservation_required_before_execution_request"
    ] is True
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
    )


def test_preserve_or_request_holds():
    with pytest.raises(
        review.Pair06V9InputOrderAdapterRejectionFreshLineageOperatorReviewHold,
        match="ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_REQUIRED",
    ):
        review.preserve_or_request()
