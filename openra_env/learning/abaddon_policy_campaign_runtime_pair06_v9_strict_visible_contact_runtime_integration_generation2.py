"""Source-only runtime integration for pair-06 V9 strict visible contact.

This module provides a drop-in Apollyon decision hook that preserves the
reviewed legacy decision boundary while inserting the reviewed coherent V9
tool-surface transform immediately before inference.

For one controller decision it:
1. obtains the current typed tools / tool contract from the legacy builder;
2. compacts the exact current state once;
3. applies the reviewed V9 coherent strict-contact policy;
4. sends copies of that filtered surface to the supplied decider;
5. rejects functions outside the filtered offered set without host mutation;
6. validates offered functions through the unchanged legacy host validator;
7. preserves the legacy five-value return shape.

The six-attempt fail-closed loop, rejection feedback, frozen compact state
across retries, and host validation boundary remain unchanged.

This module is not wired into the proto child or parent supervisor and grants no
runtime activation, execution, replay, training, promotion, deployment, chain,
wallet, transaction, funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_apollyon_decision_adapter_source_binding_review_generation2
    as decision_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_generation2
    as strict_policy,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_source_binding_review_generation2
    as policy_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-runtime-integration-contract.v1"
)

DECISION_REVIEW_GIT_BLOB = "6b9e4efdd7294392deefd5461a0403daaab3b90b"
POLICY_GIT_BLOB = "e3930101947430deecc03013088ad9ccfd1d901e"
POLICY_REVIEW_GIT_BLOB = "94eb0bf58ca5d4265ab8f45e8b0f067d3df53e58"

PAIR_SLOT = 6
ARM = "baseline"
MAX_ATTEMPTS = 6

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_RUNTIME_INTEGRATION_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_runtime_integration_review"
)


class Pair06V9StrictVisibleContactRuntimeIntegrationHold(RuntimeError):
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
        raise Pair06V9StrictVisibleContactRuntimeIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    decision = decision_review.pair06_v8_apollyon_decision_adapter_review_contract()
    reviewed_policy = policy_review.pair06_v9_strict_visible_contact_policy_review_contract()

    _require(
        decision.get("pair06_v8_apollyon_decision_adapter_reviewed") is True,
        "pair06 decision adapter not reviewed",
    )
    _require(
        decision.get("legacy_hook_symbol") == "apollyon_decision_typed",
        "pair06 legacy hook drift",
    )
    _require(
        decision.get("legacy_typed_tool_builder_symbol") == "apollyon_tools_typed",
        "pair06 typed tool builder drift",
    )
    _require(
        decision.get("legacy_host_validator_symbol") == "decision_to_commands_typed",
        "pair06 host validator drift",
    )
    _require(
        decision.get("max_attempts") == MAX_ATTEMPTS,
        "pair06 retry bound drift",
    )
    _require(
        decision.get("host_rejection_feedback_forwarded") is True
        and decision.get("world_mutation_before_host_validation") is False
        and decision.get("host_validation_unchanged") is True,
        "pair06 decision-adapter validation invariant drift",
    )

    _require(
        reviewed_policy.get(
            "pair06_v9_strict_visible_contact_policy_reviewed"
        )
        is True,
        "V9 strict-contact policy not reviewed",
    )
    _require(
        reviewed_policy.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 strict-contact policy id drift",
    )
    _require(
        reviewed_policy.get("implementation_layer")
        == "pure_pre_inference_coherent_tool_surface_transform",
        "V9 implementation layer drift",
    )
    for field in (
        "production_functions_filtered_to_offered_surface",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_invariant_required",
        "translator_legal_unit_mapping_invariant_required",
        "normal_mode_contract_identity_required",
        "v8_v1_v2_coherence_invariants_incorporated",
        "host_validation_unchanged",
    ):
        _require(
            reviewed_policy.get(field) is True,
            "V9 reviewed coherence invariant drift: " + field,
        )
    _require(
        reviewed_policy.get("runtime_integration_implemented") is False
        and reviewed_policy.get("runtime_execution_authorized") is False
        and reviewed_policy.get("training_authorized") is False,
        "V9 policy review unexpectedly grants runtime authority",
    )
    _require(
        reviewed_policy.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_RUNTIME_INTEGRATION_REQUIRED",
        "V9 runtime-integration frontier drift",
    )

    return {
        "decision_review": deepcopy(decision),
        "policy_review": deepcopy(reviewed_policy),
    }


def _validate_legacy_shape(legacy: Any) -> None:
    for name in (
        "apollyon_tools_typed",
        "decision_to_commands_typed",
        "apollyon_decision_typed",
    ):
        _require(
            callable(getattr(legacy, name, None)),
            "legacy callable missing: " + name,
        )


class Pair06V9StrictVisibleContactDecisionHooks:
    """Replace only the reviewed legacy Apollyon typed-decision hook."""

    def __init__(
        self,
        legacy: Any,
        apollyon_decider: ApollyonDecider,
    ) -> None:
        _dependencies()
        _validate_legacy_shape(legacy)
        _require(callable(apollyon_decider), "Apollyon decider must be callable")
        self.legacy = legacy
        self.apollyon_decider = apollyon_decider
        self._original = legacy.apollyon_decision_typed
        self._installed = False
        self.decision_calls = 0
        self.host_validation_calls = 0
        self.rejected_attempts = 0
        self.policy_applications = 0
        self.last_policy_mode: str | None = None

    def install(self) -> None:
        _require(not self._installed, "V9 strict-contact hook already installed")
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
        _require(self._installed, "V9 strict-contact hook not installed")
        _require(
            type(round_no) is int and round_no >= 1,
            "pair06 round number invalid",
        )
        _require(
            isinstance(doctrine, str) and bool(doctrine),
            "pair06 doctrine invalid",
        )

        typed_tools, tool_contract = self.legacy.apollyon_tools_typed(
            base,
            state,
            pending,
        )
        _require(
            isinstance(tool_contract, Mapping),
            "pair06 typed-tool contract missing",
        )

        compact_state = base.compact_state(state)
        _require(
            isinstance(compact_state, Mapping),
            "pair06 compact state missing",
        )

        adapted = strict_policy.apply_pair06_v9_strict_visible_contact_policy(
            state=compact_state,
            typed_tools=typed_tools,
            tool_contract=tool_contract,
        )
        self.policy_applications += 1
        self.last_policy_mode = str(adapted["mode"])

        filtered_tools = deepcopy(adapted["typed_tools"])
        filtered_contract = deepcopy(adapted["tool_contract"])
        offered_names = list(filtered_contract.get("offered_tool_names", ()))
        _require(bool(offered_names), "pair06 filtered tool list empty")
        offered = set(offered_names)

        frozen_compact_state = deepcopy(dict(compact_state))
        attempts = []
        feedback = ""

        for attempt in range(1, MAX_ATTEMPTS + 1):
            self.decision_calls += 1
            result = self.apollyon_decider(
                state=deepcopy(frozen_compact_state),
                typed_tools=deepcopy(filtered_tools),
                tool_contract=deepcopy(filtered_contract),
                doctrine=doctrine,
                round_no=round_no,
                feedback=feedback,
            )
            _require(
                isinstance(result, Mapping),
                "Apollyon decision result must be object",
            )
            _require(
                result.get("host_mutation_performed") is False,
                "Apollyon decision mutated host before validation",
            )

            action = result.get("campaign_action")
            _require(
                isinstance(action, Mapping),
                "Apollyon campaign action missing",
            )
            name = action.get("tool")
            args = action.get("arguments")
            _require(
                isinstance(name, str) and bool(name),
                "Apollyon campaign tool missing",
            )
            _require(
                isinstance(args, Mapping),
                "Apollyon campaign arguments must be object",
            )

            if name not in offered:
                ok = False
                reason = "function_not_offered:" + name
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
                    filtered_contract,
                )

            attempts.append({
                "attempt": attempt,
                "tool": name,
                "arguments": dict(args),
                "accepted": bool(ok),
                "host_reason": str(reason),
                "function_was_offered": name in offered,
                "policy_mode": self.last_policy_mode,
                "world_mutated_before_validation": False,
            })

            if ok:
                return (
                    name,
                    dict(args),
                    commands,
                    attempts,
                    deepcopy(filtered_contract),
                )

            self.rejected_attempts += 1
            feedback = str(reason)

        raise Pair06V9StrictVisibleContactRuntimeIntegrationHold(
            "Apollyon failed to produce a valid V9 strict-contact tool call "
            f"after {MAX_ATTEMPTS} attempts at round {round_no}; "
            f"last_reason={feedback}; allowed={offered_names}"
        )


def pair06_v9_strict_visible_contact_runtime_integration_contract() -> dict[str, Any]:
    deps = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "decision_review_git_blob": DECISION_REVIEW_GIT_BLOB,
        "policy_git_blob": POLICY_GIT_BLOB,
        "policy_review_git_blob": POLICY_REVIEW_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "legacy_hook_symbol": "apollyon_decision_typed",
        "legacy_typed_tool_builder_symbol": "apollyon_tools_typed",
        "legacy_host_validator_symbol": "decision_to_commands_typed",
        "policy_applied_after_tool_build_before_decider": True,
        "coherent_filtered_tools_and_contract_sent_to_decider": True,
        "accepted_action_validated_against_filtered_surface": True,
        "unchanged_legacy_host_validator_used": True,
        "legacy_five_value_return_shape_preserved": True,
        "max_attempts": MAX_ATTEMPTS,
        "host_rejection_feedback_forwarded": True,
        "world_mutation_before_host_validation": False,
        "frozen_compact_state_reused_across_rejected_attempts": True,
        "production_functions_filtered_to_offered_surface": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "normal_mode_contract_identity_preserved": True,
        "decision_hook_runtime_integration_implemented": True,
        "proto_game_child_wiring_implemented": False,
        "parent_supervisor_wiring_implemented": False,
        "operator_invocation_implemented": False,
        "new_execution_request_opened": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": deps,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_proto_child_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactRuntimeIntegrationHold(NEXT_GATE)
