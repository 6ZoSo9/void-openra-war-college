"""Scoped Pair-06 V9 adapter-rejection feedback overlay.

This source is a candidate-only overlay. It preserves the reviewed V9
strict-visible-contact decision loop and the input-order coherence policy, but
special-cases the exact adapter-rejection sentinel so the next bounded decision
attempt receives the original actionable host feedback: ``unit_ids invalid``.

The sentinel is never accepted, never host-validated, and never converted into
commands. Other unoffered tools and ordinary host validation paths retain the
historical behavior. Importing this module performs no game, model, service,
network, chain, wallet, training, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_generation2
    as historical_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_generation2
    as order_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_repair_generation2
    as order_repair,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-feedback-overlay-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
OBSERVED_RETRYABLE_ERROR = "unit_ids invalid"
SENTINEL_TOOL = "__v8_adapter_rejected_unit_ids_invalid__"

MAX_ATTEMPTS = historical_integration.MAX_ATTEMPTS
_require = historical_integration._require
Pair06V9StrictVisibleContactRuntimeIntegrationHold = (
    historical_integration.Pair06V9StrictVisibleContactRuntimeIntegrationHold
)

strict_policy = SimpleNamespace(
    apply_pair06_v9_strict_visible_contact_policy=(
        order_repair.apply_pair06_v9_input_order_coherence_repair
    )
)


class Pair06V9AdapterRejectionFeedbackDecisionHooks(
    order_integration.Pair06V9InputOrderCoherentDecisionHooks
):
    """Input-order hooks with one exact adapter-rejection feedback repair."""

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

            if name == "__v8_adapter_rejected_unit_ids_invalid__":
                ok = False
                reason = "unit_ids invalid"
                commands = []
            elif name not in offered:
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


def pair06_v9_adapter_rejection_feedback_overlay_contract() -> dict[str, Any]:
    """Describe the source-only overlay boundary without executing it."""
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "observed_retryable_error": OBSERVED_RETRYABLE_ERROR,
        "sentinel_tool": SENTINEL_TOOL,
        "adapter_rejection_feedback_overlay_implemented": True,
        "exact_sentinel_only": True,
        "sentinel_accepted": False,
        "sentinel_host_validation_performed": False,
        "sentinel_world_mutation_performed": False,
        "sentinel_retry_feedback": OBSERVED_RETRYABLE_ERROR,
        "other_unoffered_tool_behavior_preserved": True,
        "ordinary_host_validation_behavior_preserved": True,
        "six_attempt_bound_preserved": (
            MAX_ATTEMPTS == historical_integration.MAX_ATTEMPTS
        ),
        "historical_v8_v9_source_modified": False,
        "consumed_attempt_retry_authorized": False,
        "execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
