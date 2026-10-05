from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_requirements_generation2
    as requirements,
)


def test_contract_binds_exact_reviewed_v2_request_without_accepting_authority():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_contract()
    )

    assert out["acceptance_requirements_implemented"] is True
    assert isinstance(out["reviewed_request_sha256"], str)
    assert len(out["reviewed_request_sha256"]) == 64
    assert out["reviewed_request_bytes"] > 0
    assert out["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["attempt_marker_bytes"] == 2208
    assert out["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert out["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )

    assert out["preservation_authorization_accepted"] is False
    assert out["preservation_authorized"] is False
    assert out["preservation_performed"] is False


def test_acceptance_requires_exact_user_text_and_canonical_main_binding():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_contract()
    )

    assert out["exact_user_authorization_text_required"] is True
    assert out["authorization_text_sha256_binding_required"] is True
    assert out["authorization_text_byte_length_binding_required"] is True
    assert out["canonical_main_head_binding_required"] is True
    assert out["canonical_main_tree_binding_required"] is True
    assert out["canonical_main_must_be_bound_at_authorization_time"] is True
    assert out["authorization_must_reference_exact_reviewed_request"] is True


def test_general_source_work_permission_remains_non_authorizing():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_contract()
    )

    assert (
        out["general_source_work_authorization_is_preservation_authorization"]
        is False
    )
    assert out["matching_request_digest_grants_authority"] is False
    assert out["matching_request_bytes_grant_authority"] is False


@pytest.mark.parametrize(
    "field",
    (
        "preservation_authorization_accepted",
        "preservation_authorized",
        "filesystem_mutation_authorized",
        "git_worktree_mutation_authorized",
        "archive_rename_authorized",
        "preservation_receipt_creation_authorized",
        "preservation_performed",
        "runtime_retry_authorized",
        "execution_request_opened",
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
        "host_io_performed_by_contract_inspection",
    ),
)
def test_contract_grants_no_authority(field):
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_contract()
    )
    assert out[field] is False


def test_next_gate_is_explicit_v2_preservation_authorization():
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_preservation_acceptance_requirements_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
        "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )


def test_accept_or_preserve_holds():
    with pytest.raises(
        requirements.Pair06V9ActionableFeedbackV2PreservationAcceptanceRequirementsHold,
        match="PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        requirements.accept_or_preserve()
