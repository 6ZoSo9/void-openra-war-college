"""Pair-06 V8 adapter for the exact legacy Apollyon decision boundary.

The pinned warm-start runner exposes:
    apollyon_decision_typed(base, helper, state, pending, pb2, doctrine, round_no)

This adapter replaces only that in-memory decision function. It preserves:
* legacy current typed-tool construction via apollyon_tools_typed;
* the exact six-attempt fail-closed retry bound;
* unchanged frozen world state across rejected attempts;
* host action validation through decision_to_commands_typed;
* the legacy return shape consumed by the joint game loop.

It never calls helper.ollama_tool_call. V8 receives the compact current state,
current typed tools, current tool contract, doctrine, round number, and previous
host rejection feedback directly.

Import and contract inspection perform no model, runtime, game, host, network,
service, training, chain, wallet, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_game_coupled_runtime_source_binding_review_generation2
    as runtime_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-apollyon-decision-adapter-contract.v1"
)

RUNTIME_REVIEW_GIT_BLOB = "de3cb64a53c18765e5f0f27daabcd8c23cf4e916"
RUNTIME_REVIEW_SOURCE_SHA256 = (
    "cf3ac19c7d54206c6d3f6f02acfa0eaf412b69cea0d22c5c7f32d11818e47ecc"
)
LEGACY_WARM_START_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

PAIR_SLOT = 6
ARM = "baseline"
MAX_ATTEMPTS = 6

NEXT_GATE = "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_apollyon_decision_adapter_review"


class Pair06V8ApollyonDecisionAdapterHold(RuntimeError):
    pass


class ApollyonDecider(Protocol):
    def __call__(
        self,
        *,
        state: Mapping[str, Any],
        typed_tools: Any,
        tool_contract: Mapping[str, Any],
        doctrine: str,
        round_no: int,
        feedback: str = "",
    ) -> Mapping[str, Any]:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ApollyonDecisionAdapterHold(message)


def _runtime_review() -> dict[str, Any]:
    reviewed = runtime_review.pair06_v8_baseline_game_coupled_runtime_review_contract()
    _require(
        reviewed.get("pair06_v8_baseline_game_coupled_runtime_reviewed") is True,
        "pair06 V8 game-coupled runtime not reviewed",
    )
    _require(reviewed.get("pair_slot") == PAIR_SLOT, "pair06 runtime slot drift")
    _require(reviewed.get("arm") == ARM, "pair06 runtime arm drift")
    _require(
        reviewed.get("authority_check_before_each_inference_implemented") is True,
        "pair06 inference authority check missing",
    )
    _require(
        reviewed.get("game_execution_authorized") is False,
        "pair06 runtime review prematurely authorizes game execution",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_BASELINE_APOLLYON_DECISION_ADAPTER_IMPLEMENTATION_REQUIRED",
        "pair06 decision-adapter frontier drift",
    )
    return deepcopy(reviewed)


def _validate_legacy_shape(legacy: Any) -> None:
    for name in (
        "apollyon_tools_typed",
        "decision_to_commands_typed",
        "apollyon_decision_typed",
    ):
        _require(callable(getattr(legacy, name, None)), f"legacy callable missing: {name}")


class Pair06V8ApollyonDecisionHooks:
    """Temporarily replace only the reviewed legacy typed-decision function."""

    def __init__(self, legacy: Any, apollyon_decider: ApollyonDecider) -> None:
        _runtime_review()
        _validate_legacy_shape(legacy)
        _require(callable(apollyon_decider), "V8 Apollyon decider must be callable")
        self.legacy = legacy
        self.apollyon_decider = apollyon_decider
        self._original = legacy.apollyon_decision_typed
        self._installed = False
        self.decision_calls = 0
        self.host_validation_calls = 0
        self.rejected_attempts = 0

    def install(self) -> None:
        _require(not self._installed, "pair06 decision adapter already installed")
        self.legacy.apollyon_decision_typed = self._adapted_decision
        self._installed = True

    def restore(self) -> None:
        if self._installed:
            self.legacy.apollyon_decision_typed = self._original
            self._installed = False

    def _adapted_decision(
        self,
        base: Any,
        helper: Any,
        state: Mapping[str, Any],
        pending: Any,
        pb2: Any,
        doctrine: str,
        round_no: int,
    ):
        _require(self._installed, "pair06 decision adapter not installed")
        _require(type(round_no) is int and round_no >= 1, "pair06 round number invalid")
        _require(isinstance(doctrine, str) and bool(doctrine), "pair06 doctrine invalid")

        tools, contract = self.legacy.apollyon_tools_typed(base, state, pending)
        _require(isinstance(contract, Mapping), "pair06 typed-tool contract missing")
        offered_names = list(contract.get("offered_tool_names", ()))
        _require(bool(offered_names), "pair06 current tool list empty")
        offered = set(offered_names)

        compact_state = base.compact_state(state)
        _require(isinstance(compact_state, Mapping), "pair06 compact state missing")

        attempts = []
        feedback = ""
        for attempt in range(1, MAX_ATTEMPTS + 1):
            self.decision_calls += 1
            result = self.apollyon_decider(
                state=compact_state,
                typed_tools=tools,
                tool_contract=contract,
                doctrine=doctrine,
                round_no=round_no,
                feedback=feedback,
            )
            _require(isinstance(result, Mapping), "V8 decision result must be object")
            _require(
                result.get("host_mutation_performed") is False,
                "V8 decision mutated host before validation",
            )
            action = result.get("campaign_action")
            _require(isinstance(action, Mapping), "V8 campaign action missing")
            name = action.get("tool")
            args = action.get("arguments")
            _require(isinstance(name, str) and bool(name), "V8 campaign tool missing")
            _require(isinstance(args, Mapping), "V8 campaign arguments must be object")

            if name not in offered:
                ok = False
                reason = f"function_not_offered:{name}"
                commands = []
            else:
                self.host_validation_calls += 1
                ok, reason, commands = self.legacy.decision_to_commands_typed(
                    base,
                    name,
                    dict(args),
                    state,
                    pending,
                    pb2,
                    contract,
                )

            attempts.append(
                {
                    "attempt": attempt,
                    "tool": name,
                    "arguments": dict(args),
                    "accepted": bool(ok),
                    "host_reason": str(reason),
                    "function_was_offered": name in offered,
                    "world_mutated_before_validation": False,
                }
            )
            if ok:
                return (
                    name,
                    dict(args),
                    commands,
                    attempts,
                    deepcopy(dict(contract)),
                )

            self.rejected_attempts += 1
            feedback = str(reason)

        raise Pair06V8ApollyonDecisionAdapterHold(
            "Apollyon failed to produce a valid current-turn tool call "
            f"after {MAX_ATTEMPTS} attempts at round {round_no}; "
            f"last_reason={feedback}; allowed={offered_names}"
        )


def pair06_v8_apollyon_decision_adapter_contract() -> dict[str, Any]:
    reviewed = _runtime_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "runtime_review_git_blob": RUNTIME_REVIEW_GIT_BLOB,
        "runtime_review_source_sha256": RUNTIME_REVIEW_SOURCE_SHA256,
        "legacy_warm_start_runner_sha256": LEGACY_WARM_START_RUNNER_SHA256,
        "pair06_v8_apollyon_decision_adapter_implemented": True,
        "pair06_v8_apollyon_decision_adapter_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "legacy_hook_symbol": "apollyon_decision_typed",
        "legacy_typed_tool_builder_symbol": "apollyon_tools_typed",
        "legacy_host_validator_symbol": "decision_to_commands_typed",
        "legacy_ollama_tool_call_used": False,
        "max_attempts": MAX_ATTEMPTS,
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
        "runtime_review": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ApollyonDecisionAdapterHold(NEXT_GATE)
