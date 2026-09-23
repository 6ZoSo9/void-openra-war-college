from __future__ import annotations

import json
import socket
import struct

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_ipc_bridge_generation2
    as bridge,
)

ATTEMPT = "a" * 64


def hello(seq=1):
    return {
        "type": "HELLO",
        "seq": seq,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": ATTEMPT,
    }


def decide_request(seq=1):
    return {
        "type": "DECIDE_REQUEST",
        "seq": seq,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": ATTEMPT,
        "round_no": 1,
        "attempt_no": 1,
        "state": {"tick": 50},
        "typed_tools": [{"type": "function", "function": {"name": "advance"}}],
        "tool_contract": {"offered_tool_names": ["advance"]},
        "doctrine": "RUSHER",
        "feedback": "",
    }


def decide_response(seq=2):
    return {
        "type": "DECIDE_RESPONSE",
        "seq": seq,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": ATTEMPT,
        "round_no": 1,
        "attempt_no": 1,
        "campaign_action": {"tool": "advance", "arguments": {}},
        "host_mutation_performed": False,
    }


def test_contract_is_inert_and_bounded():
    out = bridge.pair06_v8_parent_child_ipc_bridge_contract()
    assert out["pair06_v8_parent_child_ipc_bridge_implemented"] is True
    assert out["pair06_v8_parent_child_ipc_bridge_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["protocol_version"] == 1
    assert out["transport_created_by_this_source"] is False
    assert out["duplicate_json_keys_rejected"] is True
    assert out["noncanonical_json_rejected"] is True
    assert out["unknown_message_type_rejected"] is True
    assert out["unknown_message_fields_rejected"] is True
    assert out["subprocess_spawn_implemented"] is False
    assert out["model_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False


def test_encode_decode_exact_hello_roundtrip():
    frame = bridge.encode_frame(
        hello(),
        direction="parent_to_child",
        expected_seq=1,
        expected_attempt_id=ATTEMPT,
    )
    out = bridge.decode_frame(
        frame,
        direction="parent_to_child",
        expected_seq=1,
        expected_attempt_id=ATTEMPT,
    )
    assert out == hello()


def test_socket_helpers_roundtrip_over_private_socketpair():
    left, right = socket.socketpair()
    try:
        bridge.send_message(
            left,
            decide_response(),
            direction="parent_to_child",
            expected_seq=2,
            expected_attempt_id=ATTEMPT,
        )
        out = bridge.recv_message(
            right,
            direction="parent_to_child",
            expected_seq=2,
            expected_attempt_id=ATTEMPT,
        )
        assert out == decide_response()
    finally:
        left.close()
        right.close()


def test_direction_field_and_sequence_drift_fail_closed():
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="not child-to-parent"):
        bridge.validate_message(hello(), direction="child_to_parent")

    bad = decide_request()
    bad["extra"] = True
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="field-set drift"):
        bridge.validate_message(bad, direction="child_to_parent")

    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="sequence mismatch"):
        bridge.validate_message(
            decide_request(seq=2),
            direction="child_to_parent",
            expected_seq=1,
        )


def test_pair_arm_round_attempt_and_attempt_id_are_bound():
    bad_pair = decide_request()
    bad_pair["pair_slot"] = 15
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="pair slot drift"):
        bridge.validate_message(bad_pair, direction="child_to_parent")

    bad_arm = decide_request()
    bad_arm["arm"] = "candidate"
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="arm drift"):
        bridge.validate_message(bad_arm, direction="child_to_parent")

    bad_round = decide_request()
    bad_round["round_no"] = 37
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="round number invalid"):
        bridge.validate_message(bad_round, direction="child_to_parent")

    bad_attempt = decide_request()
    bad_attempt["attempt_no"] = 7
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="attempt number invalid"):
        bridge.validate_message(bad_attempt, direction="child_to_parent")

    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="attempt_id mismatch"):
        bridge.validate_message(
            decide_request(),
            direction="child_to_parent",
            expected_attempt_id="b" * 64,
        )


def test_noncanonical_duplicate_and_oversized_payloads_fail_closed():
    raw = b'{"arm":"baseline","arm":"baseline"}'
    header = struct.pack(">I", len(raw))
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="invalid JSON payload"):
        bridge.decode_frame(header + raw, direction="parent_to_child")

    canonical = json.dumps(hello(), sort_keys=True, separators=(",", ":")).encode()
    noncanonical = canonical.replace(b',"arm"', b', "arm"', 1)
    frame = struct.pack(">I", len(noncanonical)) + noncanonical
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="not canonical JSON"):
        bridge.decode_frame(frame, direction="parent_to_child")

    huge = b"x" * (bridge.MAX_MESSAGE_BYTES + 1)
    frame = struct.pack(">I", len(huge)) + huge
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="frame length out of bounds"):
        bridge.decode_frame(frame, direction="parent_to_child")


def test_parent_response_cannot_claim_host_mutation():
    bad = decide_response()
    bad["host_mutation_performed"] = True
    with pytest.raises(bridge.Pair06V8IPCBridgeHold, match="cannot claim host mutation"):
        bridge.validate_message(bad, direction="parent_to_child")


def test_bridge_advances_only_to_separate_review():
    out = bridge.pair06_v8_parent_child_ipc_bridge_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        bridge.Pair06V8IPCBridgeHold,
        match="PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        bridge.spawn_or_execute()
