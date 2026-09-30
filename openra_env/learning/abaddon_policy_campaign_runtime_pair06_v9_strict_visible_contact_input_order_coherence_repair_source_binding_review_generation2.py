"""Exact-blob review of the V9 input-order coherence repair.

Pins the order-canonicalization repair and focused regression suite. The review
confirms that the consumed V9 failure is preserved as historical evidence, that
the historical V9 policy source is unchanged, and that only order-only input
drift is repaired. Membership drift remains fail-closed.

This review grants no retry, new execution request, runtime activation,
execution, replay, training, promotion, deployment, chain, wallet/funds, or
scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_repair_generation2
    as repair,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-repair-"
    "review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "1dcef29fe922d6a4a7b6c8ff55ff7490433a2f98"

REPAIR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_repair_generation2.py"
)
REPAIR_GIT_BLOB = "917ed6c5800278abfb56f4afbae5349b3ad4b7d7"

REPAIR_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_repair_generation2.py"
)
REPAIR_TEST_GIT_BLOB = "731ae20fe7a6a1be52df749ef6178fe1473a2911"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "RUNTIME_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "runtime_integration"
)


class Pair06V9InputOrderCoherenceRepairReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceRepairReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = repair.pair06_v9_input_order_coherence_repair_contract()

    _require(
        out.get("pair06_v9_input_order_coherence_repair_implemented") is True,
        "V9 input-order repair missing",
    )
    _require(
        out.get("historical_policy_git_blob")
        == "e3930101947430deecc03013088ad9ccfd1d901e",
        "historical V9 policy identity drift",
    )
    _require(
        out.get("runtime_failure_signature")
        == "typed tools and offered_tool_names order or membership disagree",
        "V9 runtime failure signature drift",
    )
    for field in (
        "typed_tool_membership_exact_match_required",
        "typed_tool_duplicates_rejected",
        "offered_tool_duplicates_rejected",
        "typed_tool_order_may_differ_on_input",
        "typed_tool_order_canonicalized_to_offered_order",
        "membership_drift_still_fail_closed",
        "historical_policy_called_after_canonicalization",
        "normal_mode_tool_contract_identity_preserved_by_historical_policy",
        "production_function_coherence_preserved_by_historical_policy",
        "legality_reconstruction_preserved_by_historical_policy",
    ):
        _require(
            out.get(field) is True,
            "V9 input-order repair invariant drift: " + field,
        )

    _require(
        out.get("historical_v9_policy_source_modified") is False,
        "historical V9 policy unexpectedly modified",
    )

    for field in (
        "consumed_v9_attempt_retry_authorized",
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
            "V9 input-order repair authority drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_REPAIR_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 input-order repair review frontier drift",
    )

    return deepcopy(out)


def pair06_v9_input_order_coherence_repair_review_contract() -> dict[str, Any]:
    validated = _validated()

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "repair_path": REPAIR_PATH,
        "repair_git_blob": REPAIR_GIT_BLOB,
        "repair_test_path": REPAIR_TEST_PATH,
        "repair_test_git_blob": REPAIR_TEST_GIT_BLOB,
        "pair06_v9_input_order_coherence_repair_reviewed": True,
        "runtime_failure_signature": validated["runtime_failure_signature"],
        "historical_v9_policy_source_modified": False,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_may_differ_on_input": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "historical_policy_called_after_canonicalization": True,
        "normal_mode_tool_contract_identity_preserved_by_historical_policy": True,
        "production_function_coherence_preserved_by_historical_policy": True,
        "legality_reconstruction_preserved_by_historical_policy": True,
        "consumed_v9_attempt_retry_authorized": False,
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
        "validated_repair": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceRepairReviewHold(NEXT_GATE)
