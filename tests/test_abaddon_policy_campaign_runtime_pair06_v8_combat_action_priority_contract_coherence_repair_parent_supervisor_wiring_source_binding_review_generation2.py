from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_parent_supervisor_wiring_source_binding_review_generation2
    as review,
)


def test_review_pins_all_four_merged_identities():
    out = review.pair06_v8_combat_priority_coherent_parent_wiring_review_contract()
    assert out["merged_main_head"] == (
        "fc29628d67bc51e17022a7b8a4e5e1cc4dc71ff4"
    )
    assert out["child_entry_git_blob"] == (
        "8a0161b4b6b80c74adc6d68e1fadf2e6c044c601"
    )
    assert out["child_entry_source_sha256"] == (
        "9b3fde2af21e01dc2cc13d01a2729c0565f663fbe6b39280c804186f8d1f2102"
    )
    assert out["child_entry_test_git_blob"] == (
        "339567f12c3b7f95d7280d333d97404b543c7872"
    )
    assert out["child_entry_test_sha256"] == (
        "13b56618c77b7b162b1f61d77296607ad91f4f9b28b91e0d0a4c1445ae8701bb"
    )
    assert out["parent_wiring_git_blob"] == (
        "fa3dcc13b9150a88e12c8fee005f7bf16670a236"
    )
    assert out["parent_wiring_source_sha256"] == (
        "114b4ce77abddb3ba9c856c78f1331ba22d807d4ecdf6a0fe0dc944773ff32c0"
    )
    assert out["parent_wiring_test_git_blob"] == (
        "24de93c5543319f063f51aae81a4f6e4ddd946af"
    )
    assert out["parent_wiring_test_sha256"] == (
        "3da302f685e0cd427e6375cf72e25cf3007d93e7d36080363346f2ebe40f718a"
    )


def test_review_selects_repaired_strong_invocation_lane():
    out = review.pair06_v8_combat_priority_coherent_parent_wiring_review_contract()
    assert out["canonical_invocation_lane"] == (
        "receipt_bound_no_offload_fresh_preclaim_gpu"
    )
    assert out["production_functions_filtered_to_offered_surface"] is True
    assert out["maximum_attempts_per_fresh_authorization"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out[
        "fresh_preclaim_gpu_observation_must_precede_attempt_marker"
    ] is True
    assert out["durable_create_only_attempt_marker_required"] is True
    assert out["attempt_marker_must_precede_model_load_and_child_spawn"] is True


def test_review_seals_failed_attempt_and_requires_fresh_authority():
    out = review.pair06_v8_combat_priority_coherent_parent_wiring_review_contract()
    assert out["consumed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_reusable_as_authority"] is False
    assert out["prior_authorization_reusable"] is False
    assert out["fresh_evidence_namespace_required"] is True
    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True


def test_review_grants_no_retry_or_runtime_authority():
    out = review.pair06_v8_combat_priority_coherent_parent_wiring_review_contract()
    for field in (
        "attempt_retry_authorized",
        "attempt_marker_creation_authorized",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_fresh_repaired_invocation():
    out = review.pair06_v8_combat_priority_coherent_parent_wiring_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityCoherentParentWiringReviewHold,
        match="REPAIR_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED",
    ):
        review.implement_invocation_or_execute()
