"""Exact-blob review of Pair-06 V9 adapter-rejection operator integration.

Pins the source-only operator-composition builder and focused tests. The review
confirms reuse of the exact historical operator code object with copied-global
dependency and parent bindings, no process-global mutation, and no reopening of
the consumed input-order attempt namespace.

This review explicitly advances to a fresh-lineage operator requirement. It does
not open an execution request and grants no authorization, attempt claim,
runtime activation, execution, replay, training, deployment, chain,
wallet/funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_operator_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-operator-integration-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "b36cafe6044012656d9a122653c2ddb5b9831f63"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "adapter_rejection_operator_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "626e68168a1128c3a31ffebe8bba9efc58177cc9"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "adapter_rejection_operator_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "f3083822a99ca76f9a30bf0a20c25b9abe03a3b9"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FRESH_LINEAGE_OPERATOR_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_fresh_lineage_operator"
)


class Pair06V9InputOrderAdapterRejectionOperatorIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionOperatorIntegrationReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_operator_integration_contract()
    )

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-retry-v1",
        "adapter-rejection operator integration scope drift",
    )

    for field in (
        "adapter_rejection_operator_integration_implemented",
        "historical_operator_code_object_reused",
        "call_scoped_dependency_binding_implemented",
        "call_scoped_parent_binding_implemented",
        "reviewed_repaired_parent_used",
        "historical_preclaim_gpu_ordering_preserved",
        "historical_one_attempt_cardinality_preserved",
        "historical_automatic_retry_remains_false",
        "historical_execution_policy_order_authorizations_preserved",
        "fresh_attempt_namespace_required_before_execution_request",
        "fresh_repair_activation_authorization_required_before_execution_request",
        "fresh_operator_source_required_before_execution_request",
    ):
        _require(
            out.get(field) is True,
            "adapter-rejection operator integration invariant drift: " + field,
        )

    for field in (
        "historical_operator_source_modified",
        "process_global_operator_execute_mutated",
        "process_global_operator_dependencies_mutated",
        "process_global_operator_parent_binding_mutated",
        "builder_executes_operator",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "consumed_input_order_namespace_reusable",
        "consumed_input_order_attempt_retry_authorized",
        "new_execution_request_opened",
        "repair_activation_authorization_accepted",
        "attempt_claim_created",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
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
            "adapter-rejection operator integration boundary drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (INTEGRATION_PATH, INTEGRATION_GIT_BLOB),
        (INTEGRATION_TEST_PATH, INTEGRATION_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_input_order_adapter_rejection_operator_integration_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "pair06_v9_input_order_adapter_rejection_operator_integration_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "intervention_id": (
            "pair06-v9-input-order-coherence-adapter-rejection-retry-v1"
        ),
        "historical_operator_code_object_reused": True,
        "call_scoped_dependency_binding_reviewed": True,
        "call_scoped_parent_binding_reviewed": True,
        "historical_preclaim_gpu_ordering_preserved": True,
        "historical_one_attempt_cardinality_preserved": True,
        "consumed_input_order_namespace_reusable": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "fresh_attempt_namespace_required_before_execution_request": True,
        "fresh_repair_activation_authorization_required_before_execution_request": True,
        "fresh_operator_source_required_before_execution_request": True,
        "new_execution_request_opened": False,
        "repair_activation_authorization_accepted": False,
        "attempt_created": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
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


def execute_or_request(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderAdapterRejectionOperatorIntegrationReviewHold(
        NEXT_GATE
    )
