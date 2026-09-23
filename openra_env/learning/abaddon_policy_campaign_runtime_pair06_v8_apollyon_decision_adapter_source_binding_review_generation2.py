"""Source-only review of the pair-06 V8 Apollyon typed-decision adapter."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_apollyon_decision_adapter_generation2
    as adapter,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-apollyon-decision-adapter-review-contract.v1"
)

ADAPTER_GIT_BLOB = "4c8296f6ca642bbaa72b88c1c308e56b8810ce62"
ADAPTER_SOURCE_SHA256 = (
    "13eb9fcceb18b168b54ee9468a4bb770a8cf2738db3982eb3ccdec8bb6ca0650"
)
ADAPTER_TEST_GIT_BLOB = "477476c84356c20c4df5a77ae9e15a37899ff6cf"
ADAPTER_TEST_SHA256 = (
    "39d7c1773a2fa726921912d22623b6f74c6a3d6ad6cfe12ad3973474e1eea656"
)

NEXT_GATE = "PAIR06_V8_BASELINE_LEGACY_GAME_RUNNER_COMPOSITION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_legacy_game_runner_composition"


class Pair06V8ApollyonDecisionAdapterReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ApollyonDecisionAdapterReviewHold(message)


@lru_cache(maxsize=1)
def _validate_adapter_cached() -> dict[str, Any]:
    contract = adapter.pair06_v8_apollyon_decision_adapter_contract()
    _require(
        contract.get("pair06_v8_apollyon_decision_adapter_implemented") is True,
        "pair06 V8 decision adapter missing",
    )
    _require(
        contract.get("pair06_v8_apollyon_decision_adapter_reviewed") is False,
        "pair06 V8 decision adapter unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 decision-adapter slot drift")
    _require(contract.get("arm") == "baseline", "pair06 decision-adapter arm drift")
    _require(
        contract.get("legacy_warm_start_runner_sha256")
        == "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901",
        "legacy warm-start runner identity drift",
    )
    _require(
        contract.get("legacy_hook_symbol") == "apollyon_decision_typed",
        "legacy Apollyon hook drift",
    )
    _require(
        contract.get("legacy_typed_tool_builder_symbol") == "apollyon_tools_typed",
        "legacy typed-tool builder drift",
    )
    _require(
        contract.get("legacy_host_validator_symbol") == "decision_to_commands_typed",
        "legacy host-validator drift",
    )
    _require(
        contract.get("legacy_ollama_tool_call_used") is False,
        "decision adapter unexpectedly uses legacy Ollama transport",
    )
    _require(contract.get("max_attempts") == 6, "legacy six-attempt bound drift")
    for field in (
        "current_compact_state_only",
        "current_typed_tool_list_only",
        "current_tool_contract_only",
        "host_rejection_feedback_forwarded",
        "host_validation_unchanged",
        "legacy_return_shape_preserved",
        "in_memory_hook_only",
    ):
        _require(contract.get(field) is True, f"decision-adapter contract drift: {field}")
    _require(
        contract.get("world_mutation_before_host_validation") is False,
        "world mutation allowed before host validation",
    )
    for field in (
        "game_runner_adapter_implemented",
        "durable_game_attempt_claim_implemented",
        "operator_invocation_implemented",
        "game_coupled_load_authorized",
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
        _require(contract.get(field) is False, f"decision-adapter authority drift: {field}")
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED",
        "decision-adapter review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_apollyon_decision_adapter_review_contract() -> dict[str, Any]:
    validated = _validate_adapter_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "adapter_git_blob": ADAPTER_GIT_BLOB,
        "adapter_source_sha256": ADAPTER_SOURCE_SHA256,
        "adapter_test_git_blob": ADAPTER_TEST_GIT_BLOB,
        "adapter_test_sha256": ADAPTER_TEST_SHA256,
        "pair06_v8_apollyon_decision_adapter_source_binding_present": True,
        "pair06_v8_apollyon_decision_adapter_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "legacy_warm_start_runner_sha256": validated["legacy_warm_start_runner_sha256"],
        "legacy_hook_symbol": "apollyon_decision_typed",
        "legacy_typed_tool_builder_symbol": "apollyon_tools_typed",
        "legacy_host_validator_symbol": "decision_to_commands_typed",
        "legacy_ollama_tool_call_used": False,
        "max_attempts": 6,
        "current_compact_state_only": True,
        "current_typed_tool_list_only": True,
        "current_tool_contract_only": True,
        "host_rejection_feedback_forwarded": True,
        "world_mutation_before_host_validation": False,
        "host_validation_unchanged": True,
        "legacy_return_shape_preserved": True,
        "in_memory_hook_only": True,
        "game_runner_adapter_implemented": False,
        "durable_game_attempt_claim_implemented": False,
        "operator_invocation_implemented": False,
        "game_coupled_load_authorized": False,
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
        "validated_adapter": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ApollyonDecisionAdapterReviewHold(NEXT_GATE)
