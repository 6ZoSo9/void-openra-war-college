"""Source-only review of the pair-06 V8 proto/gRPC game child."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as child,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-proto-game-child-review-contract.v1"
)

CHILD_GIT_BLOB = "061041126c8859ea77a1e131a87ab26af95291b8"
CHILD_SOURCE_SHA256 = (
    "429d9e76977d5fe734d3e714a4bad7ac5dc03f940d57dd106e23739feb23f9e2"
)
CHILD_TEST_GIT_BLOB = "26b914adfbeba260b5ad3273567dc75673f3e2fa"
CHILD_TEST_SHA256 = (
    "3ef124bee59341961c1e58c289a6c265973bf4402bee5d30e2a00c9525f40066"
)

NEXT_GATE = "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_launcher_supervisor_implementation"


class Pair06V8ProtoGameChildReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ProtoGameChildReviewHold(message)


@lru_cache(maxsize=1)
def _validate_child_cached() -> dict[str, Any]:
    contract = child.pair06_v8_proto_game_child_contract()
    _require(
        contract.get("pair06_v8_proto_game_child_implemented") is True,
        "pair06 proto game child missing",
    )
    _require(
        contract.get("pair06_v8_proto_game_child_reviewed") is False,
        "pair06 proto game child unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 child slot drift")
    _require(contract.get("arm") == "baseline", "pair06 child arm drift")
    _require(contract.get("held_out") is False, "pair06 child became held-out")
    _require(contract.get("doctrine") == "FEINTER", "pair06 child doctrine drift")
    _require(contract.get("seed") == 208354846, "pair06 child seed drift")
    _require(contract.get("rounds") == 36, "pair06 child rounds drift")
    _require(contract.get("ticks_per_round") == 25, "pair06 child tick bound drift")
    _require(contract.get("starter_infantry") == 4, "pair06 child infantry drift")
    _require(contract.get("staging_max_ticks") == 800, "pair06 child staging drift")
    _require(
        contract.get("legacy_runner_sha256")
        == "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901",
        "pair06 legacy runner identity drift",
    )

    for field in (
        "hello_ready_handshake_implemented",
        "ipc_decision_loop_implemented",
        "reviewed_decision_hook_reused",
        "legacy_start_ollama_replaced_in_memory",
        "legacy_cleanup_replaced_in_memory",
        "portable_frozen_worktree_binding_implemented",
        "isolated_runs_root_required",
        "game_result_hashing_implemented",
        "error_terminal_implemented",
    ):
        _require(contract.get(field) is True, f"proto child invariant drift: {field}")

    _require(
        contract.get("legacy_ollama_service_start_performed") is False
        and contract.get("legacy_ollama_network_contact_performed") is False,
        "proto child unexpectedly activates legacy Ollama",
    )

    for field in (
        "socketpair_creation_implemented_by_this_source",
        "child_spawn_implemented_by_this_source",
        "worktree_materialization_implemented_by_this_source",
        "durable_attempt_claim_implemented_by_this_source",
        "v8_model_load_implemented_by_this_source",
        "v8_model_inference_implemented_by_this_source",
    ):
        _require(contract.get(field) is False, f"proto child scope expanded: {field}")

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
        _require(contract.get(field) is False, f"proto child authority drift: {field}")
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PROTO_GAME_CHILD_SOURCE_BINDING_REVIEW_REQUIRED",
        "proto child review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_proto_game_child_review_contract() -> dict[str, Any]:
    validated = _validate_child_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "child_git_blob": CHILD_GIT_BLOB,
        "child_source_sha256": CHILD_SOURCE_SHA256,
        "child_test_git_blob": CHILD_TEST_GIT_BLOB,
        "child_test_sha256": CHILD_TEST_SHA256,
        "pair06_v8_proto_game_child_source_binding_present": True,
        "pair06_v8_proto_game_child_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "proto_python": validated["proto_python"],
        "legacy_runner": validated["legacy_runner"],
        "legacy_runner_sha256": validated["legacy_runner_sha256"],
        "hello_ready_handshake_implemented": True,
        "ipc_decision_loop_implemented": True,
        "reviewed_decision_hook_reused": True,
        "legacy_ollama_service_start_performed": False,
        "legacy_ollama_network_contact_performed": False,
        "portable_frozen_worktree_binding_implemented": True,
        "isolated_runs_root_required": True,
        "game_result_hashing_implemented": True,
        "socketpair_creation_implemented": False,
        "child_spawn_implemented": False,
        "worktree_materialization_implemented": False,
        "durable_attempt_claim_implemented": False,
        "v8_model_load_implemented": False,
        "v8_model_inference_implemented": False,
        "game_execution_authorized": False,
        "subprocess_spawn_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_child": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def spawn_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ProtoGameChildReviewHold(NEXT_GATE)
