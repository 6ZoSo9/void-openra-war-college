from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_child_source_and_tests():
    out = review.pair06_v8_proto_game_child_review_contract()
    assert out["child_git_blob"] == "7ea5d27c2d2bb499dfec4c00d2812d7ed043f8bc"
    assert out["child_source_sha256"] == (
        "d621ecd7a20c824ead5247d84fef5fb817df337063cd5ab558c68d42f346601a"
    )
    assert out["child_test_git_blob"] == "26b914adfbeba260b5ad3273567dc75673f3e2fa"
    assert out["child_test_sha256"] == (
        "3ef124bee59341961c1e58c289a6c265973bf4402bee5d30e2a00c9525f40066"
    )


def test_review_confirms_exact_pair06_proto_child_scope():
    out = review.pair06_v8_proto_game_child_review_contract()
    assert out["pair06_v8_proto_game_child_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800


def test_review_confirms_ollama_is_replaced_and_child_boundaries_remain():
    out = review.pair06_v8_proto_game_child_review_contract()
    assert out["hello_ready_handshake_implemented"] is True
    assert out["ipc_decision_loop_implemented"] is True
    assert out["reviewed_decision_hook_reused"] is True
    assert out["legacy_ollama_service_start_performed"] is False
    assert out["legacy_ollama_network_contact_performed"] is False
    assert out["portable_frozen_worktree_binding_implemented"] is True
    assert out["isolated_runs_root_required"] is True
    assert out["game_result_hashing_implemented"] is True
    assert out["socketpair_creation_implemented"] is False
    assert out["child_spawn_implemented"] is False
    assert out["worktree_materialization_implemented"] is False
    assert out["durable_attempt_claim_implemented"] is False
    assert out["v8_model_load_implemented"] is False
    assert out["v8_model_inference_implemented"] is False


def test_review_grants_no_execution_authority():
    out = review.pair06_v8_proto_game_child_review_contract()
    for field in (
        "game_execution_authorized",
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
    assert out["automatic_retry"] is False


def test_review_advances_only_to_parent_launcher_supervisor():
    out = review.pair06_v8_proto_game_child_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ProtoGameChildReviewHold,
        match="PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED",
    ):
        review.spawn_or_execute()
