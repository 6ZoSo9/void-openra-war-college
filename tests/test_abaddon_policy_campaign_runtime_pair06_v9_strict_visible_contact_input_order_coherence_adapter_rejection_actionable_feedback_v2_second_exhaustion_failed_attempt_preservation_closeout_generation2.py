from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_failed_attempt_preservation_closeout_generation2
    as closeout,
)


def test_closeout_binds_exact_host_preservation_result():
    out = closeout.pair06_v9_v2_second_exhaustion_preservation_closeout_contract()

    assert out["record_kind"] == "source_only_host_preservation_closeout"
    assert out["execution_control_main_head"] == (
        "0ee0d6df2ef617bc4c49cc4c73205a2f75f5ad31"
    )
    assert out["execution_control_main_tree"] == (
        "2dd40a6fcc537401315181728183720e094be445"
    )
    assert out["authorization_text_sha256"] == (
        "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
    )
    assert out["authorization_text_bytes"] == 682
    assert out["reviewed_request_sha256"] == (
        "dc9ed1487e2d218001d178eab66b29958d98c1fa7eb30760bfaf7998fe679dfc"
    )
    assert out["reviewed_request_bytes"] == 3473
    assert out["launcher_source_sha256"] == (
        "70642c23a73f4f25775519f2e53a3751ae40816be5e42ab4a8f611b811cbb00b"
    )


def test_closeout_binds_second_v2_preservation_receipt_and_evidence():
    out = closeout.pair06_v9_v2_second_exhaustion_preservation_closeout_contract()

    assert out["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["warm_start_sha256"] == (
        "03c8cb54d134bd5672892ce897e1bcad884db2ccfca3acd2473ea31b3210e1e0"
    )
    assert out["trajectory_sha256"] == (
        "da66ac0167f8e6c7afb02767fe7df05274ac1341d997a11abfc38aa587216c04"
    )
    assert out["preservation_receipt_sha256"] == (
        "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
    )
    assert out["predecessor_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )


def test_closeout_proves_preservation_and_spent_authority():
    out = closeout.pair06_v9_v2_second_exhaustion_preservation_closeout_contract()

    for field in (
        "archive_atomic_rename_performed",
        "attempt_marker_inode_preserved",
        "warm_start_inode_preserved",
        "trajectory_inode_preserved",
        "source_worktree_removed_non_force",
        "engine_worktree_removed_non_force",
        "single_authorized_preservation_consumed",
        "attempt_consumed",
        "preservation_authorization_consumed",
        "runtime_output_observed",
        "structured_correction_v3_required",
    ):
        assert out[field] is True

    assert out["attempt_reusable"] is False
    assert out["attempt_authorization_reusable"] is False
    assert out["preservation_authorization_reusable"] is False
    assert out["same_v2_retry_recommended"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "scheduler_mutation_performed",
        "repo_side_local_artifact_rehash_performed",
    ),
)
def test_closeout_grants_no_runtime_or_follow_on_authority(field):
    out = closeout.pair06_v9_v2_second_exhaustion_preservation_closeout_contract()
    assert out[field] is False


def test_closeout_advances_only_to_v3_structured_correction_source():
    out = closeout.pair06_v9_v2_second_exhaustion_preservation_closeout_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_SOURCE_REQUIRED"
    )

    with pytest.raises(
        RuntimeError,
        match="ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_SOURCE_REQUIRED",
    ):
        closeout.review_or_reopen()
