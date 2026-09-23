from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_runtime_split_design_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_design_source_and_tests():
    out = review.pair06_v8_parent_child_runtime_split_design_review_contract()
    assert out["design_git_blob"] == "d7d4e2636c0d5f3ce9061140adf9e7c7f1f4d596"
    assert out["design_source_sha256"] == (
        "3a6feb170189fcdf36e1f9f80bb31796e8541bdc58b7947a13765f3dad67032c"
    )
    assert out["design_test_git_blob"] == "69d4089d52be152446f2c216f21ddc52cd5811dc"
    assert out["design_test_sha256"] == (
        "bfc20fa4b7008079a261c8d1b0ff6fd70664fd1e504ef9907bc097b3e977e043"
    )


def test_review_confirms_parent_child_process_split():
    out = review.pair06_v8_parent_child_runtime_split_design_review_contract()
    assert out["pair06_v8_parent_child_runtime_split_design_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["separate_virtualenv_site_packages_preserved"] is True
    assert out["parent_child_process_split_required"] is True
    assert out["transport"] == "inherited_unix_socketpair"
    assert out["framing"] == "uint32_be_length_plus_utf8_canonical_json"


def test_review_confirms_bounded_ipc_and_parent_cleanup_ownership():
    out = review.pair06_v8_parent_child_runtime_split_design_review_contract()
    assert out["parent_to_child_message_types"] == (
        "HELLO",
        "DECIDE_RESPONSE",
        "ABORT",
    )
    assert out["child_to_parent_message_types"] == (
        "READY",
        "DECIDE_REQUEST",
        "GAME_RESULT",
        "ERROR",
    )
    assert out["terminal_child_message_types"] == ("GAME_RESULT", "ERROR")
    assert out["parent_owns_child_process_group_retirement"] is True
    assert out["create_only_game_attempt_claim_before_load_or_spawn"] is True
    assert out["single_authorization_covers_parent_and_child"] is True
    assert out["automatic_retry"] is False


def test_review_grants_no_execution_authority():
    out = review.pair06_v8_parent_child_runtime_split_design_review_contract()
    for field in (
        "parent_runtime_load_authorized",
        "parent_model_inference_authorized",
        "child_game_execution_authorized",
        "subprocess_spawn_authorized",
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


def test_review_advances_only_to_ipc_bridge_implementation():
    out = review.pair06_v8_parent_child_runtime_split_design_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_IMPLEMENTATION_REQUIRED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ParentChildRuntimeSplitDesignReviewHold,
        match="PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_IMPLEMENTATION_REQUIRED",
    ):
        review.execute_or_spawn()
