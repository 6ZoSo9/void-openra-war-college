from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_source_binding_review_generation2
    as review,
)


def test_review_pins_all_four_merged_identities():
    out = review.pair06_v8_combat_priority_parent_supervisor_wiring_review_contract()
    assert out["merged_main_head"] == (
        "af870046fc4d3f3a791c6cd7fbe801dca3fbd39c"
    )
    assert out["child_entry_git_blob"] == (
        "ccc2591e018875c236207343e3d8e7a04c5873b7"
    )
    assert out["child_entry_source_sha256"] == (
        "bf21b64e71e7e7ad62087950366c24035ab15097b6f36b1187f77eafb24c66bf"
    )
    assert out["child_entry_test_git_blob"] == (
        "26618c99a84944e0223808bdf93ed06c7ef5ffa2"
    )
    assert out["child_entry_test_sha256"] == (
        "4566be9712cb6062c48ea5a09459302cfda78a1b5e52598608d29d4dad949a72"
    )
    assert out["parent_wiring_git_blob"] == (
        "c30cf75b26d5e0cecee08286717d8a856e2233bd"
    )
    assert out["parent_wiring_source_sha256"] == (
        "9af96b7e3923eeb221fdba2c34e946b0776124549af7ba22a62e83c5306d72b0"
    )
    assert out["parent_wiring_test_git_blob"] == (
        "98c83f63b8e72d8359913ec0f012545473a69a36"
    )
    assert out["parent_wiring_test_sha256"] == (
        "fbd547e71e2c8783b921783d9b419dc4f7845efa1f6b16c9aa76f8e985ffcd74"
    )


def test_review_selects_existing_receipt_bound_no_offload_gpu_lane():
    out = review.pair06_v8_combat_priority_parent_supervisor_wiring_review_contract()
    assert out["canonical_invocation_lane"] == (
        "receipt_bound_no_offload_fresh_preclaim_gpu"
    )
    assert out["maximum_attempts_required"] == 1
    assert out["automatic_retry_required"] is False
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out[
        "fresh_preclaim_gpu_observation_must_precede_attempt_marker"
    ] is True
    assert out["durable_create_only_attempt_marker_required"] is True
    assert out[
        "attempt_marker_must_precede_model_load_and_child_spawn"
    ] is True


def test_review_grants_no_attempt_or_runtime_authority():
    out = review.pair06_v8_combat_priority_parent_supervisor_wiring_review_contract()
    for field in (
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "attempt_marker_creation_authorized",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_combat_priority_invocation_source():
    out = review.pair06_v8_combat_priority_parent_supervisor_wiring_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8CombatPriorityParentWiringReviewHold,
        match="BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED",
    ):
        review.implement_invocation_or_execute()
