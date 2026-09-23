from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_entrypoint_and_supervisor_sources():
    out = review.pair06_v8_parent_launcher_supervisor_review_contract()
    assert out["entrypoint_git_blob"] == "79123c0bc8d67d0001a17d4eff0162b8b9b18e0e"
    assert out["entrypoint_source_sha256"] == (
        "abf44c851df2e412cfc9b115a2467d703bbc17d75016403ba235f37f1c2162bf"
    )
    assert out["entrypoint_test_git_blob"] == "45cdb661fdb777076c2fb383f9b9ea93c6c98768"
    assert out["entrypoint_test_sha256"] == (
        "2a593cef0b481bf0444a60f2fd767704ba8aaad05231aa28dc148be7f4322e32"
    )
    assert out["supervisor_git_blob"] == "e88f3ef7d22aba630c9235ed32d0d57847afa3a0"
    assert out["supervisor_source_sha256"] == (
        "f924cdf1be34d2d21a2c07f2cd057231a7ec72339e0a4219d2f5d62864e4101b"
    )
    assert out["supervisor_test_git_blob"] == "7a0ef5837a2bba7e9e2abd29334f92eec693c78e"
    assert out["supervisor_test_sha256"] == (
        "2c1a4bef16cb0f5bbeb57254394168eb62d9e5207e7f5983bc7e51b7c3be8758"
    )


def test_review_confirms_complete_parent_child_supervision_surface():
    out = review.pair06_v8_parent_launcher_supervisor_review_contract()
    assert out["pair06_v8_parent_launcher_supervisor_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    for field in (
        "socketpair_creation_implemented",
        "child_spawn_with_inherited_fd_implemented",
        "child_private_process_group_implemented",
        "hello_ready_handshake_implemented",
        "parent_decision_service_loop_implemented",
        "authority_check_before_load_implemented",
        "authority_check_before_each_inference_implemented",
        "natural_exit_verification_implemented",
        "term_then_kill_retirement_implemented",
        "v8_reference_release_in_finally_implemented",
    ):
        assert out[field] is True


def test_review_leaves_claim_and_preparation_as_final_source_gate():
    out = review.pair06_v8_parent_launcher_supervisor_review_contract()
    assert out["attempt_claim_required_but_not_implemented"] is True
    assert out["worktree_materialization_required_but_not_implemented"] is True
    assert out["isolated_runs_root_required_but_not_created"] is True
    assert out["execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_review_preserves_non_escalation_boundaries():
    out = review.pair06_v8_parent_launcher_supervisor_review_contract()
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_claim_and_invocation():
    out = review.pair06_v8_parent_launcher_supervisor_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_CLAIM_AND_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_CLAIM_AND_INVOCATION_IMPLEMENTATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ParentSupervisorReviewHold,
        match="PAIR06_V8_BASELINE_ATTEMPT_CLAIM_AND_INVOCATION_IMPLEMENTATION_REQUIRED",
    ):
        review.execute_or_claim()
