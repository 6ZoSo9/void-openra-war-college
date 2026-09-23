from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_capability_source_and_tests():
    out = review.pair06_v8_runtime_capability_review_contract()
    assert out["capability_git_blob"] == (
        "e9f1157aa138ca9d084dab0297fc099d60905885"
    )
    assert out["capability_source_sha256"] == (
        "39e22020daa3081fb3b5a100896c8f0df104f643d011bc30aaa1763123efdbbc"
    )
    assert out["capability_test_git_blob"] == (
        "7c834237da0759412c846937703ed6fa9b615d9d"
    )
    assert out["capability_test_sha256"] == (
        "31474fbcf690b0fd1b6f4bfab12b369e7c4cf0194cfe7055a6a8afef2e96f456"
    )


def test_review_confirms_pair06_v8_capability_scope():
    out = review.pair06_v8_runtime_capability_review_contract()
    assert out["pair06_v8_runtime_capability_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arms"] == ("baseline", "candidate")
    assert out["held_out"] is False
    assert out["runtime_selection_key"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    assert out["activation_kind"] == "inprocess_accepted_v8_runtime"
    assert out["runtime_loader_callable_bound"] is True


def test_review_keeps_host_paths_and_runtime_load_unbound():
    out = review.pair06_v8_runtime_capability_review_contract()
    assert out["model_dir_path_bound"] is False
    assert out["adapter_dir_path_bound"] is False
    assert out["runtime_load_authorized"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["game_mutation_performed"] is False


def test_review_preserves_preload_safety_requirements():
    out = review.pair06_v8_runtime_capability_review_contract()
    assert out["runtime_environment_verification_required_before_load"] is True
    assert out["runtime_assets_hash_verification_required_before_load"] is True
    assert out["offline_only_model_load_required"] is True
    assert out["authority_callback_required"] is True
    assert out["automatic_retry"] is False


def test_review_keeps_heldout_replay_and_mutation_authority_closed():
    out = review.pair06_v8_runtime_capability_review_contract()
    assert out["pair15_execution_authorized"] is False
    assert out["pair03_replay_authorized"] is False
    assert out["pair09_replay_authorized"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_host_path_binding():
    out = review.pair06_v8_runtime_capability_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_HOST_PATH_BINDING_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_HOST_PATH_BINDING_REQUIRED"


def test_review_execution_entrypoints_hold():
    for fn, message in (
        (
            review.load_pair06_v8_runtime,
            "PAIR06_V8_HOST_PATH_BINDING_REQUIRED",
        ),
        (
            review.execute_pair06_game,
            "PAIR06_V8_GAME_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            review.execute_pair15,
            "PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            review.Pair06V8RuntimeCapabilityReviewHold,
            match=message,
        ):
            fn()
