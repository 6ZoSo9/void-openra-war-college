"""Bounded IPC codec for pair-06 V8 parent/game-child composition.

This module implements only message validation and framing for an already
connected inherited Unix socketpair. It does not create sockets, spawn
processes, load a model, run inference, start OpenRA, call a service, mutate
packages, train, deploy, touch VOID-chain state, or touch wallets/funds.

Protocol rules:
* exact top-level field sets by message type;
* pair_slot=6, arm=baseline only;
* per-direction sequence numbers are positive integers;
* rounds are 1..36, attempts are 1..6;
* canonical UTF-8 JSON, duplicate keys rejected;
* 4 MiB payload maximum;
* uint32 big-endian length prefix;
* unknown message types/fields fail closed.
"""

from __future__ import annotations

from copy import deepcopy
import json
import struct
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_runtime_split_design_source_binding_review_generation2
    as design_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-child-ipc-bridge-contract.v1"
)
PROTOCOL_VERSION = 1
PAIR_SLOT = 6
ARM = "baseline"
MAX_ROUND = 36
MAX_ATTEMPT = 6
MAX_MESSAGE_BYTES = 4 * 1024 * 1024
HEADER_BYTES = 4

DESIGN_REVIEW_GIT_BLOB = "37a8810e6b83243bf23fda189cdcc67dfb0f2f0c"
DESIGN_REVIEW_SOURCE_SHA256 = (
    "ca97e3bdcbbd9bc22ae8c987e175363a2fcc6c40d147e778f057f885c5998503"
)

PARENT_TO_CHILD = frozenset({"HELLO", "DECIDE_RESPONSE", "ABORT"})
CHILD_TO_PARENT = frozenset({"READY", "DECIDE_REQUEST", "GAME_RESULT", "ERROR"})

FIELD_SETS = {
    "HELLO": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm", "attempt_id"
    }),
    "READY": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm",
        "attempt_id", "child_pid", "child_pgid"
    }),
    "DECIDE_REQUEST": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm", "attempt_id",
        "round_no", "attempt_no", "state", "typed_tools", "tool_contract",
        "doctrine", "feedback"
    }),
    "DECIDE_RESPONSE": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm", "attempt_id",
        "round_no", "attempt_no", "campaign_action", "host_mutation_performed"
    }),
    "GAME_RESULT": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm", "attempt_id",
        "result"
    }),
    "ERROR": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm", "attempt_id",
        "error_type", "error_message"
    }),
    "ABORT": frozenset({
        "type", "seq", "protocol_version", "pair_slot", "arm", "attempt_id",
        "reason"
    }),
}

NEXT_GATE = "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_child_ipc_bridge_review"


class Pair06V8IPCBridgeHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8IPCBridgeHold(message)


def _design() -> dict[str, Any]:
    reviewed = design_review.pair06_v8_parent_child_runtime_split_design_review_contract()
    _require(
        reviewed.get("pair06_v8_parent_child_runtime_split_design_reviewed") is True,
        "pair06 parent-child split design not reviewed",
    )
    _require(reviewed.get("pair_slot") == PAIR_SLOT, "pair06 split slot drift")
    _require(reviewed.get("arm") == ARM, "pair06 split arm drift")
    _require(
        reviewed.get("transport") == "inherited_unix_socketpair",
        "pair06 IPC transport drift",
    )
    _require(
        reviewed.get("framing") == "uint32_be_length_plus_utf8_canonical_json",
        "pair06 IPC framing drift",
    )
    _require(
        reviewed.get("max_message_bytes") == MAX_MESSAGE_BYTES,
        "pair06 IPC size bound drift",
    )
    _require(
        reviewed.get("next_gate") == "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_IMPLEMENTATION_REQUIRED",
        "pair06 IPC implementation frontier drift",
    )
    return deepcopy(reviewed)


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise Pair06V8IPCBridgeHold(f"message is not canonical-JSON encodable: {exc}") from exc
    raw = text.encode("utf-8")
    _require(len(raw) <= MAX_MESSAGE_BYTES, "message exceeds maximum payload size")
    return raw


def _no_duplicate_object(pairs):
    result = {}
    for key, value in pairs:
        _require(isinstance(key, str), "JSON object key must be string")
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_canonical_json(raw: bytes) -> dict[str, Any]:
    _require(isinstance(raw, (bytes, bytearray)), "payload must be bytes")
    _require(0 < len(raw) <= MAX_MESSAGE_BYTES, "payload size out of bounds")
    try:
        text = bytes(raw).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Pair06V8IPCBridgeHold("payload is not UTF-8") from exc
    try:
        value = json.loads(text, object_pairs_hook=_no_duplicate_object)
    except (json.JSONDecodeError, Pair06V8IPCBridgeHold) as exc:
        raise Pair06V8IPCBridgeHold(f"invalid JSON payload: {exc}") from exc
    _require(isinstance(value, dict), "message payload must be object")
    _require(
        _canonical_json_bytes(value) == bytes(raw),
        "message payload is not canonical JSON",
    )
    return value


def _is_hex64(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def validate_message(
    message: Mapping[str, Any],
    *,
    direction: str,
    expected_seq: int | None = None,
    expected_attempt_id: str | None = None,
) -> dict[str, Any]:
    _require(isinstance(message, Mapping), "message must be object")
    supplied = dict(message)
    msg_type = supplied.get("type")
    _require(isinstance(msg_type, str), "message type missing")
    _require(msg_type in FIELD_SETS, f"unsupported message type: {msg_type}")

    if direction == "parent_to_child":
        _require(msg_type in PARENT_TO_CHILD, f"message type not parent-to-child: {msg_type}")
    elif direction == "child_to_parent":
        _require(msg_type in CHILD_TO_PARENT, f"message type not child-to-parent: {msg_type}")
    else:
        raise Pair06V8IPCBridgeHold("direction must be parent_to_child or child_to_parent")

    _require(
        set(supplied) == set(FIELD_SETS[msg_type]),
        f"message field-set drift: {msg_type}",
    )
    _require(supplied["protocol_version"] == PROTOCOL_VERSION, "protocol version drift")
    _require(supplied["pair_slot"] == PAIR_SLOT, "pair slot drift")
    _require(supplied["arm"] == ARM, "arm drift")
    _require(type(supplied["seq"]) is int and supplied["seq"] >= 1, "sequence invalid")
    if expected_seq is not None:
        _require(supplied["seq"] == expected_seq, "sequence mismatch")

    attempt_id = supplied["attempt_id"]
    _require(_is_hex64(attempt_id), "attempt_id must be lowercase SHA-256")
    if expected_attempt_id is not None:
        _require(attempt_id == expected_attempt_id, "attempt_id mismatch")

    if msg_type == "READY":
        _require(
            type(supplied["child_pid"]) is int and supplied["child_pid"] > 1,
            "child_pid invalid",
        )
        _require(
            type(supplied["child_pgid"]) is int and supplied["child_pgid"] > 1,
            "child_pgid invalid",
        )
        _require(
            supplied["child_pid"] == supplied["child_pgid"],
            "child must lead private process group",
        )

    if msg_type in {"DECIDE_REQUEST", "DECIDE_RESPONSE"}:
        _require(
            type(supplied["round_no"]) is int
            and 1 <= supplied["round_no"] <= MAX_ROUND,
            "round number invalid",
        )
        _require(
            type(supplied["attempt_no"]) is int
            and 1 <= supplied["attempt_no"] <= MAX_ATTEMPT,
            "attempt number invalid",
        )

    if msg_type == "DECIDE_REQUEST":
        _require(isinstance(supplied["state"], dict), "state must be object")
        _require(isinstance(supplied["typed_tools"], list), "typed_tools must be list")
        _require(isinstance(supplied["tool_contract"], dict), "tool_contract must be object")
        _require(
            isinstance(supplied["doctrine"], str) and bool(supplied["doctrine"]),
            "doctrine invalid",
        )
        _require(isinstance(supplied["feedback"], str), "feedback invalid")
        _require("\x00" not in supplied["feedback"], "feedback contains NUL")

    if msg_type == "DECIDE_RESPONSE":
        _require(
            isinstance(supplied["campaign_action"], dict),
            "campaign_action must be object",
        )
        _require(
            supplied["host_mutation_performed"] is False,
            "parent response cannot claim host mutation",
        )

    if msg_type == "GAME_RESULT":
        _require(isinstance(supplied["result"], dict), "game result must be object")

    if msg_type == "ERROR":
        _require(
            isinstance(supplied["error_type"], str) and bool(supplied["error_type"]),
            "error_type invalid",
        )
        _require(
            isinstance(supplied["error_message"], str),
            "error_message invalid",
        )
        _require("\x00" not in supplied["error_message"], "error_message contains NUL")

    if msg_type == "ABORT":
        _require(isinstance(supplied["reason"], str) and bool(supplied["reason"]), "abort reason invalid")
        _require("\x00" not in supplied["reason"], "abort reason contains NUL")

    _canonical_json_bytes(supplied)
    return deepcopy(supplied)


def encode_frame(
    message: Mapping[str, Any],
    *,
    direction: str,
    expected_seq: int | None = None,
    expected_attempt_id: str | None = None,
) -> bytes:
    checked = validate_message(
        message,
        direction=direction,
        expected_seq=expected_seq,
        expected_attempt_id=expected_attempt_id,
    )
    payload = _canonical_json_bytes(checked)
    return struct.pack(">I", len(payload)) + payload


def decode_frame(
    frame: bytes,
    *,
    direction: str,
    expected_seq: int | None = None,
    expected_attempt_id: str | None = None,
) -> dict[str, Any]:
    _require(isinstance(frame, (bytes, bytearray)), "frame must be bytes")
    raw = bytes(frame)
    _require(len(raw) >= HEADER_BYTES + 1, "frame truncated")
    (size,) = struct.unpack(">I", raw[:HEADER_BYTES])
    _require(0 < size <= MAX_MESSAGE_BYTES, "frame length out of bounds")
    _require(len(raw) == HEADER_BYTES + size, "frame length mismatch")
    message = _parse_canonical_json(raw[HEADER_BYTES:])
    return validate_message(
        message,
        direction=direction,
        expected_seq=expected_seq,
        expected_attempt_id=expected_attempt_id,
    )


def _recv_exact(sock: Any, size: int) -> bytes:
    _require(type(size) is int and size >= 0, "recv size invalid")
    chunks = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        _require(isinstance(chunk, (bytes, bytearray)), "socket recv returned non-bytes")
        _require(bool(chunk), "socket closed before complete frame")
        chunks.append(bytes(chunk))
        remaining -= len(chunk)
    return b"".join(chunks)


def send_message(
    sock: Any,
    message: Mapping[str, Any],
    *,
    direction: str,
    expected_seq: int | None = None,
    expected_attempt_id: str | None = None,
) -> None:
    _require(callable(getattr(sock, "sendall", None)), "socket sendall missing")
    frame = encode_frame(
        message,
        direction=direction,
        expected_seq=expected_seq,
        expected_attempt_id=expected_attempt_id,
    )
    sock.sendall(frame)


def recv_message(
    sock: Any,
    *,
    direction: str,
    expected_seq: int | None = None,
    expected_attempt_id: str | None = None,
) -> dict[str, Any]:
    _require(callable(getattr(sock, "recv", None)), "socket recv missing")
    header = _recv_exact(sock, HEADER_BYTES)
    (size,) = struct.unpack(">I", header)
    _require(0 < size <= MAX_MESSAGE_BYTES, "frame length out of bounds")
    payload = _recv_exact(sock, size)
    message = _parse_canonical_json(payload)
    return validate_message(
        message,
        direction=direction,
        expected_seq=expected_seq,
        expected_attempt_id=expected_attempt_id,
    )


def pair06_v8_parent_child_ipc_bridge_contract() -> dict[str, Any]:
    reviewed = _design()
    return {
        "schema": CONTRACT_SCHEMA,
        "design_review_git_blob": DESIGN_REVIEW_GIT_BLOB,
        "design_review_source_sha256": DESIGN_REVIEW_SOURCE_SHA256,
        "pair06_v8_parent_child_ipc_bridge_implemented": True,
        "pair06_v8_parent_child_ipc_bridge_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "protocol_version": PROTOCOL_VERSION,
        "transport_created_by_this_source": False,
        "socketpair_required_by_reviewed_design": True,
        "framing": "uint32_be_length_plus_utf8_canonical_json",
        "header_bytes": HEADER_BYTES,
        "max_message_bytes": MAX_MESSAGE_BYTES,
        "duplicate_json_keys_rejected": True,
        "noncanonical_json_rejected": True,
        "unknown_message_type_rejected": True,
        "unknown_message_fields_rejected": True,
        "sequence_validation_implemented": True,
        "attempt_id_validation_implemented": True,
        "pair_arm_round_attempt_binding_implemented": True,
        "socket_read_write_helpers_implemented": True,
        "subprocess_spawn_implemented": False,
        "model_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_design": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def spawn_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8IPCBridgeHold(NEXT_GATE)
