from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_generation2
    as preservation,
)


def test_contract_binds_exact_consumed_v2_failure():
    out = preservation.pair06_v9_actionable_feedback_v2_failed_attempt_preservation_contract()

    assert out["attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert out["attempt_marker_bytes"] == 2208
    assert out["warm_start_sha256"] == (
        "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
    )
    assert out["warm_start_bytes"] == 229255
    assert out["trajectory_sha256"] == (
        "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
    )
    assert out["trajectory_bytes"] == 58075
    assert out["authorized_attempt_main_head"] == (
        "63a5077ba247a974d2696c479972efdf4cd0f6e8"
    )
    assert out["authorized_attempt_main_tree"] == (
        "e9a6bdf0423e739f97519515f62bd24ef65cf1a3"
    )
    assert out["operator_source_sha256"] == (
        "fcc662cbaaa482651004523b73deb906947a73b296356cc291bb9150dddfc179"
    )


def test_contract_binds_terminal_failure_shape():
    out = preservation.pair06_v9_actionable_feedback_v2_failed_attempt_preservation_contract()

    assert out["failure_class"] == "strict_contact_actionable_feedback_v2_exhausted"
    assert out["failure_round"] == 6
    assert out["maximum_decision_attempts"] == 6
    assert out["terminal_feedback"] == (
        "function_not_offered:"
        "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
        "not_json_array_or_bare_integer__"
    )


@pytest.mark.parametrize(
    "field",
    (
        "exact_consumed_marker_required",
        "exact_run_artifacts_required",
        "result_must_be_absent",
        "closeout_must_be_absent",
        "summary_must_be_absent",
        "exact_clean_detached_registered_worktrees_required",
        "non_force_worktree_removal_only",
        "engine_removed_before_source",
        "remaining_evidence_manifest_hashed",
        "atomic_baseline_archive_rename_implemented",
        "attempt_marker_inode_preserved",
        "run_artifact_inode_preserved",
        "create_only_preservation_receipt_implemented",
        "preservation_requires_explicit_authority",
        "preservation_confirmation_token_required",
    ),
)
def test_preservation_safety_invariants(field):
    out = preservation.pair06_v9_actionable_feedback_v2_failed_attempt_preservation_contract()
    assert out[field] is True


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_execution_authorized",
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
def test_contract_grants_no_retry_or_follow_on_authority(field):
    out = preservation.pair06_v9_actionable_feedback_v2_failed_attempt_preservation_contract()
    assert out[field] is False


def test_review_or_preserve_holds():
    with pytest.raises(
        preservation.Pair06V9ActionableFeedbackV2FailedAttemptPreservationHold,
        match="PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        preservation.review_or_preserve()
