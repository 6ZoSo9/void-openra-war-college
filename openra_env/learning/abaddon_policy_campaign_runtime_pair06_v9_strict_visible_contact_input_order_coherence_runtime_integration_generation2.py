"""Source-only runtime integration for the V9 input-order coherence repair.

The historical V9 runtime integration remains byte-for-byte unchanged. This
module subclasses its reviewed decision hook and, for exactly one decision call,
temporarily substitutes only the V9 policy apply function with the reviewed
input-order coherence repair.

The repair canonicalizes typed-tool order to offered_tool_names only when exact
membership already matches. Membership drift and duplicates remain fail-closed.
The historical V9 policy then owns strict-contact filtering, production-function
coherence, legality reconstruction, NORMAL identity, and host-validation
boundaries exactly as before.

The consumed failed V9 attempt is not retryable. This source opens no execution
request and grants no runtime activation, game execution, replay, training,
promotion, deployment, chain, wallet/funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_repair_generation2
    as repair,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_repair_source_binding_review_generation2
    as repair_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_generation2
    as historical_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_source_binding_review_generation2
    as historical_integration_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "runtime-integration-contract.v1"
)

REPAIR_GIT_BLOB = "917ed6c5800278abfb56f4afbae5349b3ad4b7d7"
REPAIR_REVIEW_GIT_BLOB = "132ef2916e72cf25cafab1ee368c06083d918e20"
HISTORICAL_RUNTIME_INTEGRATION_GIT_BLOB = (
    "8aa8a3bae62a914dfa1c1b7daf2fca6b13ecf2ef"
)
HISTORICAL_RUNTIME_INTEGRATION_REVIEW_GIT_BLOB = (
    "9e92605527aeea59f9d99cfcb798adea569f7309"
)

ORIGINAL_V9_POLICY_APPLY = (
    historical_integration.strict_policy
    .apply_pair06_v9_strict_visible_contact_policy
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "runtime_integration_review"
)


class Pair06V9InputOrderCoherenceRuntimeIntegrationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceRuntimeIntegrationHold(message)


@lru_cache(maxsize=1)
def _dependencies() -> dict[str, Any]:
    repaired = repair_review.pair06_v9_input_order_coherence_repair_review_contract()
    historical = (
        historical_integration_review
        .pair06_v9_strict_visible_contact_runtime_integration_review_contract()
    )

    _require(
        repaired.get("pair06_v9_input_order_coherence_repair_reviewed") is True,
        "V9 input-order repair not reviewed",
    )
    _require(
        repaired.get("repair_git_blob") == REPAIR_GIT_BLOB,
        "V9 input-order repair source identity drift",
    )
    _require(
        repaired.get("typed_tool_membership_exact_match_required") is True
        and repaired.get("typed_tool_order_canonicalized_to_offered_order")
        is True
        and repaired.get("membership_drift_still_fail_closed") is True,
        "V9 input-order repair invariant drift",
    )
    _require(
        repaired.get("historical_v9_policy_source_modified") is False
        and repaired.get("consumed_v9_attempt_retry_authorized") is False
        and repaired.get("new_execution_request_opened") is False,
        "V9 repair lineage/authority drift",
    )
    _require(
        repaired.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "RUNTIME_INTEGRATION_REQUIRED"
        ),
        "V9 repair runtime-integration frontier drift",
    )

    _require(
        historical.get(
            "pair06_v9_strict_visible_contact_runtime_integration_reviewed"
        )
        is True,
        "historical V9 runtime integration not reviewed",
    )
    _require(
        historical.get("decision_hook_runtime_integration_implemented") is True
        and historical.get("coherent_filtered_surface_reviewed") is True
        and historical.get("unchanged_legacy_host_validator_reviewed") is True
        and historical.get("six_attempt_fail_closed_retry_reviewed") is True
        and historical.get("frozen_compact_state_reuse_reviewed") is True,
        "historical V9 runtime integration invariant drift",
    )
    _require(
        historical.get("runtime_execution_authorized") is False
        and historical.get("new_execution_request_opened") is False,
        "historical V9 runtime integration unexpectedly grants authority",
    )

    return {
        "repair_review": deepcopy(repaired),
        "historical_runtime_integration_review": deepcopy(historical),
    }


class Pair06V9InputOrderCoherentDecisionHooks(
    historical_integration.Pair06V9StrictVisibleContactDecisionHooks
):
    """Historical V9 decision hooks with scoped order-repair substitution."""

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
        _dependencies()

        current = (
            historical_integration.strict_policy
            .apply_pair06_v9_strict_visible_contact_policy
        )
        _require(
            current is ORIGINAL_V9_POLICY_APPLY,
            "historical V9 policy function drift before scoped substitution",
        )

        (
            historical_integration.strict_policy
            .apply_pair06_v9_strict_visible_contact_policy
        ) = repair.apply_pair06_v9_input_order_coherence_repair
        try:
            return super()._adapted_decision(
                base,
                helper,
                state,
                pending,
                pb2,
                doctrine,
                round_no,
            )
        finally:
            (
                historical_integration.strict_policy
                .apply_pair06_v9_strict_visible_contact_policy
            ) = ORIGINAL_V9_POLICY_APPLY


def pair06_v9_input_order_coherence_runtime_integration_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "repair_git_blob": REPAIR_GIT_BLOB,
        "repair_review_git_blob": REPAIR_REVIEW_GIT_BLOB,
        "historical_runtime_integration_git_blob": (
            HISTORICAL_RUNTIME_INTEGRATION_GIT_BLOB
        ),
        "historical_runtime_integration_review_git_blob": (
            HISTORICAL_RUNTIME_INTEGRATION_REVIEW_GIT_BLOB
        ),
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "input_order_coherence_runtime_integration_implemented": True,
        "historical_v9_policy_source_modified": False,
        "historical_v9_runtime_integration_source_modified": False,
        "scoped_policy_function_substitution_implemented": True,
        "policy_function_restored_in_finally": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "historical_strict_contact_filtering_reused": True,
        "historical_production_function_coherence_reused": True,
        "historical_legality_reconstruction_reused": True,
        "historical_normal_mode_contract_identity_reused": True,
        "unchanged_legacy_host_validator_reused": True,
        "six_attempt_fail_closed_loop_reused": True,
        "frozen_compact_state_reused": True,
        "consumed_v9_attempt_retry_authorized": False,
        "proto_child_repair_wiring_implemented": False,
        "parent_supervisor_repair_wiring_implemented": False,
        "operator_repair_wiring_implemented": False,
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
        "scheduler_mutation_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceRuntimeIntegrationHold(NEXT_GATE)
