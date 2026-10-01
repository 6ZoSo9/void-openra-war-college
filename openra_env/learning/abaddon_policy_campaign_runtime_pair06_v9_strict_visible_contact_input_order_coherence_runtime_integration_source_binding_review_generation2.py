"""Exact-blob review of the V9 input-order repair runtime integration.

Pins the scoped runtime-integration wrapper and focused tests. The review
confirms that the historical V9 runtime integration remains unchanged, the
reviewed input-order repair is substituted only for one decision call and
restored in finally, and membership drift remains fail-closed.

The consumed V9 attempt remains consumed and non-retryable. This review opens no
new execution request and grants no runtime activation, execution, replay,
training, promotion, deployment, chain, wallet/funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "runtime-integration-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "4c5da4cc8f815a1571dae3a9fad927790b9eb42f"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "runtime_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "569c09ce225741ec2d38c36f8062da0bdbb16c1f"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "runtime_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "1afcebce2ca5b1196e019dd588cc5a78ca9d568c"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "PROTO_CHILD_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "proto_child_wiring"
)


class Pair06V9InputOrderCoherenceRuntimeIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceRuntimeIntegrationReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = integration.pair06_v9_input_order_coherence_runtime_integration_contract()

    _require(
        out.get("input_order_coherence_runtime_integration_implemented") is True,
        "V9 order-repair runtime integration missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 order-repair runtime integration scope drift",
    )
    for field in (
        "scoped_policy_function_substitution_implemented",
        "policy_function_restored_in_finally",
        "typed_tool_membership_exact_match_required",
        "typed_tool_order_canonicalized_to_offered_order",
        "membership_drift_still_fail_closed",
        "historical_strict_contact_filtering_reused",
        "historical_production_function_coherence_reused",
        "historical_legality_reconstruction_reused",
        "historical_normal_mode_contract_identity_reused",
        "unchanged_legacy_host_validator_reused",
        "six_attempt_fail_closed_loop_reused",
        "frozen_compact_state_reused",
    ):
        _require(
            out.get(field) is True,
            "V9 order-repair runtime invariant drift: " + field,
        )

    _require(
        out.get("historical_v9_policy_source_modified") is False
        and out.get("historical_v9_runtime_integration_source_modified")
        is False,
        "historical V9 runtime source unexpectedly modified",
    )

    for field in (
        "consumed_v9_attempt_retry_authorized",
        "proto_child_repair_wiring_implemented",
        "parent_supervisor_repair_wiring_implemented",
        "operator_repair_wiring_implemented",
        "new_execution_request_opened",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "V9 order-repair runtime authority drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 order-repair runtime review frontier drift",
    )

    return deepcopy(out)


def pair06_v9_input_order_coherence_runtime_integration_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "pair06_v9_input_order_coherence_runtime_integration_reviewed": True,
        "policy_id": validated["policy_id"],
        "historical_v9_policy_source_modified": False,
        "historical_v9_runtime_integration_source_modified": False,
        "scoped_policy_function_substitution_reviewed": True,
        "policy_function_restored_in_finally_reviewed": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
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
        "validated_integration": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceRuntimeIntegrationReviewHold(NEXT_GATE)
