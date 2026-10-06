from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_authorization_acceptance_requirements_generation2
    as requirements,
)


def test_requirements_bind_exact_reviewed_request_and_consumed_evidence():
    out = (
        requirements
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract()
    )

    assert out["acceptance_requirements_implemented"] is True
    assert out["request_review_git_blob"] == requirements.REQUEST_REVIEW_GIT_BLOB
    assert isinstance(out["reviewed_request_sha256"], str)
    assert len(out["reviewed_request_sha256"]) == 64
    assert out["reviewed_request_bytes"] > 0
    assert out["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["warm_start_sha256"] == (
        "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    )
    assert out["trajectory_sha256"] == (
        "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    )
    assert out["predecessor_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )


def test_requirements_demand_exact_user_text_and_main_snapshot():
    out = (
        requirements
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract()
    )

    for field in (
        "exact_user_authorization_text_required",
        "authorization_text_sha256_binding_required",
        "authorization_text_byte_length_binding_required",
        "canonical_main_head_binding_required",
        "canonical_main_tree_binding_required",
        "canonical_main_must_be_bound_at_authorization_time",
        "authorization_must_reference_exact_reviewed_request",
    ):
        assert out[field] is True


def test_requirements_reject_old_or_generic_authority():
    out = (
        requirements
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract()
    )

    assert out["general_source_work_authorization_is_preservation_authorization"] is False
    assert out["matching_request_digest_grants_authority"] is False
    assert out["matching_request_bytes_grant_authority"] is False
    assert out["prior_preservation_authorization_reusable"] is False
    assert out["prior_execution_authorization_reusable"] is False


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
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_requirements_grant_no_authority(field):
    out = (
        requirements
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract()
    )
    assert out[field] is False


def test_requirements_stop_at_explicit_user_authorization():
    out = (
        requirements
        .pair06_v9_v2_second_exhaustion_preservation_acceptance_requirements_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
        "PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED"
    )

    with pytest.raises(
        requirements.Pair06V9V2SecondExhaustionPreservationAcceptanceRequirementsHold,
        match="PRESERVATION_EXPLICIT_USER_AUTHORIZATION_REQUIRED",
    ):
        requirements.accept_or_preserve()
