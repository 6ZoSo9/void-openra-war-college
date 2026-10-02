from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_requirements_generation2
    as requirements,
)


def test_contract_binds_exact_reviewed_request_without_accepting_authority():
    out = (
        requirements
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_contract()
    )

    assert out["acceptance_requirements_implemented"] is True
    assert isinstance(out["reviewed_request_sha256"], str)
    assert len(out["reviewed_request_sha256"]) == 64
    assert out["reviewed_request_bytes"] > 0

    assert out["execution_authorization_accepted"] is False
    assert out["policy_activation_authorization_accepted"] is False
    assert out["order_coherence_activation_authorization_accepted"] is False
    assert out["repair_activation_authorization_accepted"] is False


def test_acceptance_requires_exact_text_main_and_all_four_gates():
    out = (
        requirements
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_contract()
    )

    assert out["exact_user_authorization_text_required"] is True
    assert out["authorization_text_sha256_binding_required"] is True
    assert out["authorization_text_byte_length_binding_required"] is True
    assert out["canonical_main_head_binding_required"] is True
    assert out["canonical_main_tree_binding_required"] is True
    assert out["canonical_main_must_be_bound_at_authorization_time"] is True
    assert out["authorization_must_reference_exact_reviewed_request"] is True

    assert out["authorization_must_explicitly_cover_execution"] is True
    assert out["authorization_must_explicitly_cover_policy_activation"] is True
    assert out["authorization_must_explicitly_cover_order_coherence_activation"] is True
    assert out["authorization_must_explicitly_cover_repair_activation"] is True
    assert out["four_distinct_confirmation_tokens_required"] is True


def test_prior_authority_cannot_be_reused():
    out = (
        requirements
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_contract()
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
    assert out["matching_request_digest_grants_authority"] is False
    assert out["matching_request_bytes_grant_authority"] is False


def test_runtime_cardinality_remains_one_attempt_zero_retry():
    out = (
        requirements
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_contract()
    )

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_adapter_rejection_evidence_namespace_required"] is True


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
        "attempt_created",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_contract_grants_no_authority(field):
    out = (
        requirements
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_contract()
    )
    assert out[field] is False


def test_next_gate_is_explicit_fresh_execution_authorization():
    out = (
        requirements
        .pair06_v9_adapter_rejection_fresh_execution_acceptance_requirements_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_FRESH_EXECUTION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_execute_holds():
    with pytest.raises(
        requirements.Pair06V9AdapterRejectionFreshExecutionAcceptanceRequirementsHold,
        match="FRESH_EXECUTION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        requirements.accept_or_execute()
