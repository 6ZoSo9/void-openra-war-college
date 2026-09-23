"""Source-only review of the pair-06 V8 parent/child runtime split design."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_runtime_split_design_generation2
    as design,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-child-runtime-split-design-review-contract.v1"
)

DESIGN_GIT_BLOB = "d7d4e2636c0d5f3ce9061140adf9e7c7f1f4d596"
DESIGN_SOURCE_SHA256 = (
    "3a6feb170189fcdf36e1f9f80bb31796e8541bdc58b7947a13765f3dad67032c"
)
DESIGN_TEST_GIT_BLOB = "69d4089d52be152446f2c216f21ddc52cd5811dc"
DESIGN_TEST_SHA256 = (
    "bfc20fa4b7008079a261c8d1b0ff6fd70664fd1e504ef9907bc097b3e977e043"
)

NEXT_GATE = "PAIR06_V8_PARENT_CHILD_IPC_BRIDGE_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_child_ipc_bridge_implementation"


class Pair06V8ParentChildRuntimeSplitDesignReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ParentChildRuntimeSplitDesignReviewHold(message)


@lru_cache(maxsize=1)
def _validate_design_cached() -> dict[str, Any]:
    contract = design.pair06_v8_parent_child_runtime_split_design_contract()
    _require(
        contract.get("pair06_v8_parent_child_runtime_split_design_implemented") is True,
        "pair06 parent-child split design missing",
    )
    _require(
        contract.get("pair06_v8_parent_child_runtime_split_design_reviewed") is False,
        "pair06 parent-child split design unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 split slot drift")
    _require(contract.get("arm") == "baseline", "pair06 split arm drift")
    _require(contract.get("held_out") is False, "pair06 split became held-out")

    for field in (
        "separate_virtualenv_site_packages_preserved",
        "v8_parent_owns_model_load",
        "v8_parent_owns_model_inference",
        "v8_parent_owns_authority_check_before_load",
        "v8_parent_owns_authority_check_before_each_inference",
        "game_child_owns_grpc_proto",
        "game_child_owns_openra",
        "game_child_owns_legacy_runner",
        "game_child_must_not_load_model",
        "game_child_must_not_call_legacy_ollama",
        "socketpair_inherited_fd_only",
        "protocol_sequence_numbers_required",
        "protocol_pair_slot_bound",
        "protocol_arm_bound",
        "protocol_round_bound_1_to_36",
        "canonical_json_required",
        "unknown_message_type_rejected",
        "unknown_message_fields_rejected",
        "child_private_process_group_required",
        "parent_owns_child_process_group_retirement",
        "term_then_kill_escalation_required",
        "child_natural_zero_exit_required_for_clean_terminal",
        "create_only_game_attempt_claim_before_load_or_spawn",
        "single_authorization_covers_parent_and_child",
    ):
        _require(contract.get(field) is True, f"pair06 split design drift: {field}")

    _require(
        contract.get("package_install_into_v8_required") is False
        and contract.get("cross_venv_site_packages_injection_required") is False,
        "pair06 split design mutates V8 environment",
    )
    _require(contract.get("transport") == "inherited_unix_socketpair", "transport drift")
    _require(
        contract.get("filesystem_socket_path_created") is False
        and contract.get("listening_network_socket_created") is False,
        "pair06 split unexpectedly opens listening transport",
    )
    _require(
        contract.get("framing") == "uint32_be_length_plus_utf8_canonical_json",
        "pair06 IPC framing drift",
    )
    _require(
        tuple(contract.get("parent_to_child_message_types", ()))
        == ("HELLO", "DECIDE_RESPONSE", "ABORT"),
        "parent-to-child message set drift",
    )
    _require(
        tuple(contract.get("child_to_parent_message_types", ()))
        == ("READY", "DECIDE_REQUEST", "GAME_RESULT", "ERROR"),
        "child-to-parent message set drift",
    )
    _require(
        tuple(contract.get("terminal_child_message_types", ()))
        == ("GAME_RESULT", "ERROR"),
        "terminal child message set drift",
    )
    _require(
        tuple(contract.get("attempt_sequence", ())) == design.ATTEMPT_SEQUENCE,
        "pair06 attempt sequence drift",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")

    for field in (
        "parent_runtime_load_authorized",
        "parent_model_inference_authorized",
        "child_game_execution_authorized",
        "subprocess_spawn_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 split authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 split review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_parent_child_runtime_split_design_review_contract() -> dict[str, Any]:
    validated = _validate_design_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "design_git_blob": DESIGN_GIT_BLOB,
        "design_source_sha256": DESIGN_SOURCE_SHA256,
        "design_test_git_blob": DESIGN_TEST_GIT_BLOB,
        "design_test_sha256": DESIGN_TEST_SHA256,
        "pair06_v8_parent_child_runtime_split_design_source_binding_present": True,
        "pair06_v8_parent_child_runtime_split_design_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "v8_parent_python": validated["v8_parent_python"],
        "game_child_python": validated["game_child_python"],
        "transport": "inherited_unix_socketpair",
        "framing": "uint32_be_length_plus_utf8_canonical_json",
        "max_message_bytes": validated["max_message_bytes"],
        "parent_to_child_message_types": validated["parent_to_child_message_types"],
        "child_to_parent_message_types": validated["child_to_parent_message_types"],
        "terminal_child_message_types": validated["terminal_child_message_types"],
        "separate_virtualenv_site_packages_preserved": True,
        "parent_child_process_split_required": True,
        "parent_owns_child_process_group_retirement": True,
        "create_only_game_attempt_claim_before_load_or_spawn": True,
        "single_authorization_covers_parent_and_child": True,
        "automatic_retry": False,
        "parent_runtime_load_authorized": False,
        "parent_model_inference_authorized": False,
        "child_game_execution_authorized": False,
        "subprocess_spawn_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_design": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_spawn(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ParentChildRuntimeSplitDesignReviewHold(NEXT_GATE)
