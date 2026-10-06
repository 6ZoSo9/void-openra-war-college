from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_generation2
    as preservation,
)


def test_contract_binds_second_v2_failure_exactly():
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()
    )

    assert out["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["attempt_marker_bytes"] == 2208
    assert out["warm_start_sha256"] == (
        "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    )
    assert out["warm_start_bytes"] == 229255
    assert out["trajectory_sha256"] == (
        "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    )
    assert out["trajectory_bytes"] == 58075
    assert out["authorized_attempt_main_head"] == (
        "4ac5f41ff7632e847e79e3d8ebfd632aeb0633f2"
    )
    assert out["authorized_attempt_main_tree"] == (
        "02d2f2ea0b81bf13981d8c49b7caf8ea4012f92a"
    )
    assert out["operator_source_sha256"] == (
        "fcc662cbaaa482651004523b73deb906947a73b296356cc291bb9150dddfc179"
    )


def test_contract_chains_without_reusing_first_v2_archive():
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()
    )
    assert out["archive_name"].endswith("ee1b4fc5")
    assert out["predecessor_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert out["first_v2_archive_must_remain_present"] is True
    assert out["first_v2_preservation_receipt_must_match"] is True


def test_contract_binds_terminal_failure():
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()
    )
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
def test_preservation_invariants(field):
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()
    )
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
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_contract_grants_no_execution_or_extra_authority(field):
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()
    )
    assert out[field] is False


def test_contract_stops_at_review():
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_second_exhaustion_preservation_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_FAILED_ATTEMPT_"
        "PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )

    with pytest.raises(
        preservation.Pair06V9ActionableFeedbackV2SecondExhaustionPreservationHold,
        match="PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        preservation.review_or_preserve()
