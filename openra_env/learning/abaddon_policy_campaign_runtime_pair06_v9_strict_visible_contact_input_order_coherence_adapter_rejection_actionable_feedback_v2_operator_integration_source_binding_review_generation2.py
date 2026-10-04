"""Exact-blob review of Pair-06 V9 actionable-feedback V2 operator integration.

Pins the source-only V2 operator-composition builder and focused tests. The
review confirms reuse of the already-reviewed V1 operator integration with the
exact historical operator code object while only the copied dependency and
parent bindings are upgraded to the reviewed actionable-feedback V2 parent.

The consumed input-order namespace remains closed. This review advances only to
a fresh-lineage V2 operator requirement. It opens no execution request and
accepts no activation authorization or attempt authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_operator_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-actionable-feedback-v2-operator-integration-"
    "review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "bc15543eda1f89d208ac089cfb30c9164909c38e"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_operator_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "8a8b1114682940462934dfbfcf25e0dbd3a784a3"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_operator_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "ea598ba1b0229a9686ab14b02c00d92e985b641e"

V1_OPERATOR_INTEGRATION_GIT_BLOB = "fcf5cb87ef75f288dbcb5e83f236ea217db1db2d"
V1_OPERATOR_REVIEW_GIT_BLOB = "74590dce39f0c5bcab590db6df6e3f78475f74be"
V2_PARENT_INTEGRATION_GIT_BLOB = "22eb8708b600d15e6f3aa0e02e5697a7cf01a820"
V2_PARENT_REVIEW_GIT_BLOB = "c3a39dbb0a22d9350894a8f78b824af0b4e07a01"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_LINEAGE_OPERATOR_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_fresh_lineage_operator"
)


class Pair06V9ActionableFeedbackV2OperatorIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2OperatorIntegrationReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = integration.pair06_v9_actionable_feedback_v2_operator_integration_contract()

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "actionable-feedback V2 operator integration scope drift",
    )

    for field in (
        "actionable_feedback_v2_operator_integration_implemented",
        "reviewed_v1_operator_integration_reused",
        "historical_operator_code_object_reused",
        "call_scoped_dependency_binding_upgraded_to_v2",
        "call_scoped_parent_binding_upgraded_to_v2",
        "reviewed_actionable_feedback_v2_parent_used",
        "historical_preclaim_gpu_ordering_preserved",
        "historical_one_attempt_cardinality_preserved",
        "historical_automatic_retry_remains_false",
        "historical_execution_policy_order_authorizations_preserved",
        "feedback_requires_quoted_unit_ids_string",
        "feedback_rejects_json_array_unit_ids",
        "feedback_rejects_bare_integer_unit_ids",
        "fresh_attempt_namespace_required_before_execution_request",
        "fresh_actionable_feedback_v2_activation_authorization_required",
        "fresh_operator_source_required_before_execution_request",
    ):
        _require(
            out.get(field) is True,
            "actionable-feedback V2 operator invariant drift: " + field,
        )

    for field in (
        "v1_operator_integration_source_modified",
        "v2_parent_integration_source_modified",
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
        "actionable_feedback_v2_activation_authorization_accepted",
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
            "actionable-feedback V2 operator boundary drift: " + field,
        )

    _require(
        out.get("v1_operator_integration_git_blob")
        == V1_OPERATOR_INTEGRATION_GIT_BLOB
        and out.get("v1_operator_review_git_blob") == V1_OPERATOR_REVIEW_GIT_BLOB,
        "reviewed V1 operator lineage drift",
    )
    _require(
        out.get("v2_parent_integration_git_blob")
        == V2_PARENT_INTEGRATION_GIT_BLOB
        and out.get("v2_parent_review_git_blob") == V2_PARENT_REVIEW_GIT_BLOB,
        "reviewed actionable-feedback V2 parent lineage drift",
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


def pair06_v9_actionable_feedback_v2_operator_integration_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "v1_operator_integration_git_blob": V1_OPERATOR_INTEGRATION_GIT_BLOB,
        "v1_operator_review_git_blob": V1_OPERATOR_REVIEW_GIT_BLOB,
        "v2_parent_integration_git_blob": V2_PARENT_INTEGRATION_GIT_BLOB,
        "v2_parent_review_git_blob": V2_PARENT_REVIEW_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_operator_integration_reviewed": True,
        "policy_id": validated["policy_id"],
        "reviewed_v1_operator_integration_reused": True,
        "historical_operator_code_object_reused": True,
        "call_scoped_dependency_binding_upgraded_to_v2": True,
        "call_scoped_parent_binding_upgraded_to_v2": True,
        "reviewed_actionable_feedback_v2_parent_used": True,
        "historical_preclaim_gpu_ordering_preserved": True,
        "historical_one_attempt_cardinality_preserved": True,
        "consumed_input_order_namespace_reusable": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "fresh_attempt_namespace_required_before_execution_request": True,
        "fresh_actionable_feedback_v2_activation_authorization_required": True,
        "fresh_operator_source_required_before_execution_request": True,
        "new_execution_request_opened": False,
        "actionable_feedback_v2_activation_authorization_accepted": False,
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
    raise Pair06V9ActionableFeedbackV2OperatorIntegrationReviewHold(NEXT_GATE)
