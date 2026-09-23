"""Source-only design for pair-06 V8 parent/child runtime split.

Compatibility evidence proved the accepted V8 venv cannot import the legacy
gRPC/proto toolchain without changing its accepted package set. This design
keeps the two accepted environments intact:

* parent process: accepted V8 Python, model load, inference, authority checks;
* child process: accepted proto/gRPC Python, exact legacy runner, OpenRA game;
* transport: inherited Unix socketpair, no listening TCP/Unix path;
* protocol: length-delimited canonical JSON messages with exact schemas;
* parent owns child process-group containment and terminal cleanup.

The durable one-shot game-attempt claim must be created before either the V8
load or child launch. One authorization must cover the coupled parent/child
attempt. No automatic retry is permitted.

This source grants no load, inference, game, subprocess, service, package,
training, deployment, VOID-chain, wallet, or funds authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_same_process_python_compat_evidence_source_binding_review_generation2
    as compat_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-child-runtime-split-design-contract.v1"
)

COMPAT_REVIEW_GIT_BLOB = "d49a13743a7fbbad2fddd7e0ddd597672308dc17"
COMPAT_REVIEW_SOURCE_SHA256 = (
    "c03b8aff0512101d88758a25499e6aa15ed8365e8a6196c9b93cf6ce4a8d3d9d"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
V8_PYTHON = (
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/"
    "venv/bin/python3.12"
)
PROTO_PYTHON = (
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)
TRANSPORT = "inherited_unix_socketpair"
FRAMING = "uint32_be_length_plus_utf8_canonical_json"
MAX_MESSAGE_BYTES = 4 * 1024 * 1024

PARENT_TO_CHILD_TYPES = (
    "HELLO",
    "DECIDE_RESPONSE",
    "ABORT",
)
CHILD_TO_PARENT_TYPES = (
    "READY",
    "DECIDE_REQUEST",
    "GAME_RESULT",
    "ERROR",
)
TERMINAL_CHILD_TYPES = (
    "GAME_RESULT",
    "ERROR",
)

ATTEMPT_SEQUENCE = (
    "fresh_v8_environment_and_asset_verification",
    "create_only_game_attempt_claim",
    "load_exact_v8_parent_runtime",
    "create_private_socketpair",
    "spawn_proto_game_child_private_process_group",
    "child_verify_exact_legacy_runtime_and_start_openra",
    "child_warm_start_to_controller_handoff",
    "bounded_decision_request_response_loop",
    "child_publish_game_result_terminal",
    "child_cleanup_openra_and_exit",
    "parent_retire_or_verify_absent_child_process_group",
    "parent_release_v8_runtime",
    "durable_attempt_result_publication",
)

NEXT_GATE = "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_child_runtime_split_design_review"


class Pair06V8ParentChildRuntimeSplitDesignHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ParentChildRuntimeSplitDesignHold(message)


@lru_cache(maxsize=1)
def _compatibility_cached() -> dict[str, Any]:
    reviewed = compat_review.pair06_v8_python_compat_evidence_review_contract()
    _require(
        reviewed.get("pair06_v8_same_process_python_compat_evidence_reviewed") is True,
        "pair06 Python compatibility evidence not reviewed",
    )
    _require(reviewed.get("pair_slot") == PAIR_SLOT, "pair06 compatibility slot drift")
    _require(reviewed.get("arm") == ARM, "pair06 compatibility arm drift")
    _require(reviewed.get("held_out") is False, "pair06 compatibility became held-out")
    _require(
        reviewed.get("v8_python") == V8_PYTHON,
        "pair06 V8 interpreter drift",
    )
    _require(
        reviewed.get("proto_python") == PROTO_PYTHON,
        "pair06 proto interpreter drift",
    )
    _require(
        reviewed.get("same_process_legacy_game_path_compatible") is False,
        "same-process legacy game path unexpectedly compatible",
    )
    _require(
        reviewed.get("parent_child_runtime_split_required") is True,
        "parent-child split no longer required",
    )
    _require(
        reviewed.get("package_install_into_v8_authorized") is False,
        "V8 package installation unexpectedly authorized",
    )
    _require(
        reviewed.get("cross_venv_site_packages_injection_authorized") is False,
        "cross-venv site-packages injection unexpectedly authorized",
    )
    _require(
        reviewed.get("next_gate") == "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED",
        "pair06 split-design frontier drift",
    )
    return deepcopy(reviewed)


def pair06_v8_parent_child_runtime_split_design_contract() -> dict[str, Any]:
    compatibility = _compatibility_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "compat_review_git_blob": COMPAT_REVIEW_GIT_BLOB,
        "compat_review_source_sha256": COMPAT_REVIEW_SOURCE_SHA256,
        "pair06_v8_parent_child_runtime_split_design_implemented": True,
        "pair06_v8_parent_child_runtime_split_design_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "v8_parent_python": V8_PYTHON,
        "game_child_python": PROTO_PYTHON,
        "separate_virtualenv_site_packages_preserved": True,
        "package_install_into_v8_required": False,
        "cross_venv_site_packages_injection_required": False,
        "v8_parent_owns_model_load": True,
        "v8_parent_owns_model_inference": True,
        "v8_parent_owns_authority_check_before_load": True,
        "v8_parent_owns_authority_check_before_each_inference": True,
        "game_child_owns_grpc_proto": True,
        "game_child_owns_openra": True,
        "game_child_owns_legacy_runner": True,
        "game_child_must_not_load_model": True,
        "game_child_must_not_call_legacy_ollama": True,
        "transport": TRANSPORT,
        "socketpair_inherited_fd_only": True,
        "filesystem_socket_path_created": False,
        "listening_network_socket_created": False,
        "framing": FRAMING,
        "max_message_bytes": MAX_MESSAGE_BYTES,
        "parent_to_child_message_types": PARENT_TO_CHILD_TYPES,
        "child_to_parent_message_types": CHILD_TO_PARENT_TYPES,
        "terminal_child_message_types": TERMINAL_CHILD_TYPES,
        "protocol_sequence_numbers_required": True,
        "protocol_pair_slot_bound": True,
        "protocol_arm_bound": True,
        "protocol_round_bound_1_to_36": True,
        "canonical_json_required": True,
        "unknown_message_type_rejected": True,
        "unknown_message_fields_rejected": True,
        "child_private_process_group_required": True,
        "parent_owns_child_process_group_retirement": True,
        "term_then_kill_escalation_required": True,
        "child_natural_zero_exit_required_for_clean_terminal": True,
        "create_only_game_attempt_claim_before_load_or_spawn": True,
        "single_authorization_covers_parent_and_child": True,
        "attempt_sequence": ATTEMPT_SEQUENCE,
        "automatic_retry": False,
        "parent_runtime_load_authorized": False,
        "parent_model_inference_authorized": False,
        "child_game_execution_authorized": False,
        "subprocess_spawn_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "compatibility_review": compatibility,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_spawn(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ParentChildRuntimeSplitDesignHold(NEXT_GATE)
