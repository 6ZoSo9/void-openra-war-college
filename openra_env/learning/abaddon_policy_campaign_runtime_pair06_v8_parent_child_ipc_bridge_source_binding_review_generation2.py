"""Source-only review of the pair-06 V8 parent/child IPC bridge."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_ipc_bridge_generation2
    as bridge,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-child-ipc-bridge-review-contract.v1"
)

BRIDGE_GIT_BLOB = "f33a068ab903f4f06bb4d6bc4505318331859c09"
BRIDGE_SOURCE_SHA256 = (
    "5ce3ccadb96b14e6191d00959fc14914016fbc2e5fb4168158fb57767a0a6537"
)
BRIDGE_TEST_GIT_BLOB = "734fc33013dac410ba726d40c89244ef11c29171"
BRIDGE_TEST_SHA256 = (
    "9feb2766c9cf3d7d721a19605642367d03cfd5beddf058d6ff0c418ae5e6693d"
)

NEXT_GATE = "PAIR06_V8_PROTO_GAME_CHILD_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_proto_game_child_implementation"


class Pair06V8IPCBridgeReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8IPCBridgeReviewHold(message)


@lru_cache(maxsize=1)
def _validate_bridge_cached() -> dict[str, Any]:
    contract = bridge.pair06_v8_parent_child_ipc_bridge_contract()
    _require(
        contract.get("pair06_v8_parent_child_ipc_bridge_implemented") is True,
        "pair06 IPC bridge missing",
    )
    _require(
        contract.get("pair06_v8_parent_child_ipc_bridge_reviewed") is False,
        "pair06 IPC bridge unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 IPC slot drift")
    _require(contract.get("arm") == "baseline", "pair06 IPC arm drift")
    _require(contract.get("protocol_version") == 1, "pair06 IPC protocol drift")
    _require(
        contract.get("transport_created_by_this_source") is False,
        "IPC bridge unexpectedly creates transport on inspection",
    )
    _require(
        contract.get("socketpair_required_by_reviewed_design") is True,
        "socketpair design binding missing",
    )
    _require(
        contract.get("framing") == "uint32_be_length_plus_utf8_canonical_json",
        "IPC framing drift",
    )
    _require(contract.get("header_bytes") == 4, "IPC header size drift")
    _require(contract.get("max_message_bytes") == 4 * 1024 * 1024, "IPC max size drift")

    for field in (
        "duplicate_json_keys_rejected",
        "noncanonical_json_rejected",
        "unknown_message_type_rejected",
        "unknown_message_fields_rejected",
        "sequence_validation_implemented",
        "attempt_id_validation_implemented",
        "pair_arm_round_attempt_binding_implemented",
        "socket_read_write_helpers_implemented",
    ):
        _require(contract.get(field) is True, f"IPC bridge invariant drift: {field}")

    _require(
        contract.get("subprocess_spawn_implemented") is False,
        "IPC bridge unexpectedly spawns child",
    )
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
        _require(contract.get(field) is False, f"IPC bridge authority drift: {field}")
    _require(contract.get("automatic_retry") is False, "IPC bridge automatic retry enabled")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_SOURCE_BINDING_REVIEW_REQUIRED",
        "IPC bridge review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_parent_child_ipc_bridge_review_contract() -> dict[str, Any]:
    validated = _validate_bridge_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "bridge_git_blob": BRIDGE_GIT_BLOB,
        "bridge_source_sha256": BRIDGE_SOURCE_SHA256,
        "bridge_test_git_blob": BRIDGE_TEST_GIT_BLOB,
        "bridge_test_sha256": BRIDGE_TEST_SHA256,
        "pair06_v8_parent_child_ipc_bridge_source_binding_present": True,
        "pair06_v8_parent_child_ipc_bridge_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "protocol_version": 1,
        "transport": "inherited_unix_socketpair",
        "framing": "uint32_be_length_plus_utf8_canonical_json",
        "max_message_bytes": 4 * 1024 * 1024,
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
        "validated_bridge": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def spawn_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8IPCBridgeReviewHold(NEXT_GATE)
