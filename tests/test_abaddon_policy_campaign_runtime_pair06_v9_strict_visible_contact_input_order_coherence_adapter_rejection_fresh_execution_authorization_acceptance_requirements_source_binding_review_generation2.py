from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_requirements_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_requirements_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_review_contract()
    )

    assert out["requirements_path"] == review.REQUIREMENTS_PATH
    assert out["requirements_git_blob"] == review.REQUIREMENTS_GIT_BLOB
    assert out["requirements_test_path"] == review.REQUIREMENTS_TEST_PATH
    assert out["requirements_test_git_blob"] == review.REQUIREMENTS_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.REQUIREMENTS_PATH).read_bytes()) == (
        review.REQUIREMENTS_GIT_BLOB
    )
    assert _git_blob_sha1(
        (ROOT / review.REQUIREMENTS_TEST_PATH).read_bytes()
    ) == review.REQUIREMENTS_TEST_GIT_BLOB


def test_review_requires_fresh_explicit_authorization_for_all_four_gates():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_reviewed"
    ] is True

    assert out["exact_user_authorization_text_required"] is True
    assert out["authorization_text_sha256_binding_required"] is True
    assert out["authorization_text_byte_length_binding_required"] is True
    assert out["canonical_main_head_binding_required"] is True
    assert out["canonical_main_tree_binding_required"] is True

    assert out["authorization_must_explicitly_cover_execution"] is True
    assert out["authorization_must_explicitly_cover_policy_activation"] is True
    assert out["authorization_must_explicitly_cover_order_coherence_activation"] is True
    assert out["authorization_must_explicitly_cover_repair_activation"] is True
    assert out["four_distinct_confirmation_tokens_required"] is True


def test_review_refuses_all_prior_authority_reuse():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_review_contract()
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
def test_review_grants_no_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_review_contract()
    )
    assert out[field] is False


def test_review_stops_at_explicit_fresh_execution_authorization():
    out = (
        review
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FRESH_EXECUTION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_execute_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionFreshExecutionAcceptanceRequirementsReviewHold,
        match="FRESH_EXECUTION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        review.accept_or_execute()
