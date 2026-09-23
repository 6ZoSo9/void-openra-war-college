from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_ipc_bridge_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_bridge_source_and_tests():
    out = review.pair06_v8_parent_child_ipc_bridge_review_contract()
    assert out["bridge_git_blob"] == "f33a068ab903f4f06bb4d6bc4505318331859c09"
    assert out["bridge_source_sha256"] == (
        "5ce3ccadb96b14e6191d00959fc14914016fbc2e5fb4168158fb57767a0a6537"
    )
    assert out["bridge_test_git_blob"] == "734fc33013dac410ba726d40c89244ef11c29171"
    assert out["bridge_test_sha256"] == (
        "9feb2766c9cf3d7d721a19605642367d03cfd5beddf058d6ff0c418ae5e6693d"
    )


def test_review_confirms_bounded_ipc_codec():
    out = review.pair06_v8_parent_child_ipc_bridge_review_contract()
    assert out["pair06_v8_parent_child_ipc_bridge_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["protocol_version"] == 1
    assert out["transport"] == "inherited_unix_socketpair"
    assert out["framing"] == "uint32_be_length_plus_utf8_canonical_json"
    assert out["max_message_bytes"] == 4 * 1024 * 1024
    assert out["duplicate_json_keys_rejected"] is True
    assert out["noncanonical_json_rejected"] is True
    assert out["unknown_message_type_rejected"] is True
    assert out["unknown_message_fields_rejected"] is True
    assert out["sequence_validation_implemented"] is True
    assert out["attempt_id_validation_implemented"] is True
    assert out["pair_arm_round_attempt_binding_implemented"] is True


def test_review_grants_no_execution_authority():
    out = review.pair06_v8_parent_child_ipc_bridge_review_contract()
    assert out["subprocess_spawn_implemented"] is False
    for field in (
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
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


def test_review_advances_only_to_proto_game_child_implementation():
    out = review.pair06_v8_parent_child_ipc_bridge_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PROTO_GAME_CHILD_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_PROTO_GAME_CHILD_IMPLEMENTATION_REQUIRED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8IPCBridgeReviewHold,
        match="PAIR06_V8_PROTO_GAME_CHILD_IMPLEMENTATION_REQUIRED",
    ):
        review.spawn_or_execute()
